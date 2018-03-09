from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models, transaction
from django.urls import reverse
from model_utils.managers import InheritanceManager
from django.utils.translation import gettext_lazy as _

NAME_MAX_LENGTH = 100


class Garden(models.Model):
    name = models.CharField(unique=True, max_length=NAME_MAX_LENGTH, verbose_name="Nom du jardin")
    users = models.ManyToManyField(User)
    notification_delay = models.IntegerField(default=5)

    def __str__(self):
        return "Garden: " + self.name

    def get_absolute_url(self):
        return reverse('planner:alerts_view', kwargs={'garden_id': self.id})


class Vegetable(models.Model):
    name = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.name


class ProductionPeriod(models.Model):
    """ A garden has a set of production period.s A production period can be a calendar year, but not only"""
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE, unique_for_date=start_date)
    label = models.CharField(max_length=100)

    def __str__(self):
        return "Production period starting :" + str(self.start_date)


class Surface(models.Model):
    """ A garden has a set of surfaces where the farmer can cultivate vegetables"""
    objects = InheritanceManager()
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE)

    @property
    def get_area(self):
        raise NotImplementedError()

    def __str__(self):
        return "Surface with area : " + str(self.get_area())


class Bed(Surface):
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    length = models.IntegerField()
    width = models.IntegerField()

    def get_area(self):
        return self.length * self.width

    def __str__(self):
        return self.name + " : " + str(self.length) + "x" + str(self.width)


class Area(Surface):
    area_surface = models.IntegerField()

    def get_area(self):
        return self.area_surface


class CulturalOperation(models.Model):
    objects = InheritanceManager()
    name = models.CharField(max_length=NAME_MAX_LENGTH, verbose_name=_('Nom de l\'action'))
    vegetable = models.ForeignKey(Vegetable, on_delete=models.CASCADE, verbose_name=_('Légume concerné'))
    duration = models.DurationField(verbose_name=_('Temps nécessaire par m²'), default=timedelta(seconds=0))
    is_initial = models.BooleanField(default=False)

    @transaction.atomic
    def save(self, *args, **kwargs):
        """  Ensure there is only one initial operation by vegetable """""
        if self.is_initial:
            CulturalOperation.objects.filter(vegetable_id=self.vegetable_id, is_initial=True).update(is_initial=False)
        super(CulturalOperation, self).save(*args, **kwargs)

    def get_date(self):
        pass

    def __str__(self):
        return self.vegetable.name + " : " + self.name


class COWithOffset(CulturalOperation):
    offset_in_days = models.IntegerField(verbose_name=_('Délai en jours'))
    previous_operation = models.ForeignKey(CulturalOperation, related_name='+', on_delete=models.CASCADE,
                                           verbose_name=_('Opération précédente'))

    def get_previous_operation(self):
        return CulturalOperation.objects.select_subclasses().get(pk=self.previous_operation.id)

    def get_date(self):
        return self.get_previous_operation().get_date() + timedelta(days=self.offset_in_days)


class COWithDate(CulturalOperation):
    absoluteDate = models.DateField(verbose_name=_('Date d\'échéance'))

    def get_date(self):
        return self.absoluteDate


class CultivatedArea(models.Model):
    vegetable = models.ForeignKey(Vegetable, null=True, on_delete=models.SET_NULL)
    production_period = models.ForeignKey(ProductionPeriod, on_delete=models.CASCADE)
    surface = models.ForeignKey(Surface, on_delete=models.CASCADE)
    label = models.TextField()
    is_active = models.BooleanField(default=True)


class ForthcomingOperation(models.Model):
    area_concerned = models.ForeignKey(CultivatedArea, on_delete=models.CASCADE)
    original_cultural_operation = models.ForeignKey(CulturalOperation, on_delete=models.CASCADE)
    postponement = models.IntegerField(default=0)
    execution_date = models.DateField(null=True)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return str(self.area_concerned.label) + " " + str(self.original_cultural_operation)


class History(models.Model):
    production_period = models.OneToOneField(ProductionPeriod, on_delete=models.CASCADE)


class HistoryItem(models.Model):
    objects = InheritanceManager()
    history = models.ForeignKey(History, on_delete=models.CASCADE)
    execution_date = models.DateField()
    vegetable = models.ForeignKey(Vegetable, on_delete=models.CASCADE)
    executor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Observation(HistoryItem):
    bed = models.ForeignKey(Surface, null=True, on_delete=models.SET_NULL)
    description = models.TextField()


class Operation(HistoryItem):
    bed = models.ForeignKey(Surface, on_delete=models.SET_NULL, null=True)
    name = models.TextField(max_length=NAME_MAX_LENGTH)
    note = models.TextField(null=True)
    duration = models.DurationField(null=True)
    is_deletion = models.BooleanField(default=False)
