from datetime import timedelta

from django.db import models, transaction
from django.urls import reverse
from model_utils.managers import InheritanceManager

NAME_MAX_LENGTH = 100


class Garden(models.Model):
    name = models.CharField(unique=True, max_length=NAME_MAX_LENGTH, verbose_name="Nom du jardin")

    def __str__(self):
        return "Garden: " + self.name

    def get_absolute_url(self):
        return reverse('planner:alerts_view', kwargs={'garden_id': self.id})


class Vegetable(models.Model):
    name = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.name


class ProductionPeriod(models.Model):
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE, unique_for_date=start_date)
    label = models.CharField(max_length=100)

    def __str__(self):
        return "Production period starting :" + str(self.start_date)


class Surface(models.Model):
    objects = InheritanceManager()
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE)

    @property
    def get_area(self):
        raise NotImplementedError()

    def __str__(self):
        return "Surface with area : " + self.get_area()


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
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    vegetable = models.ForeignKey(Vegetable, on_delete=models.CASCADE)
    duration = models.IntegerField()
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
    offset_in_days = models.IntegerField()
    previous_operation = models.ForeignKey(CulturalOperation, related_name='+', on_delete=models.CASCADE)

    def get_previous_operation(self):
        return CulturalOperation.objects.select_subclasses().get(pk=self.previous_operation.id)

    def get_date(self):
        return self.get_previous_operation().get_date() + timedelta(days=self.offset_in_days)


class COWithDate(CulturalOperation):
    absoluteDate = models.DateField()

    def get_date(self):
        return self.absoluteDate


class CulturalOperationHistory(models.Model):
    production_period = models.ForeignKey(ProductionPeriod, on_delete=models.CASCADE)
    original_C_Operation = models.ForeignKey(CulturalOperation, on_delete=models.CASCADE)
    date = models.DateField()
    duration = models.IntegerField()
    surface_processed = models.IntegerField()

    def __str__(self):
        return str(self.original_C_Operation) + " Fait le : " + str(self.date)


class CultivatedArea(models.Model):
    vegetable = models.ForeignKey(Vegetable, null=True, on_delete=models.SET_NULL)
    production_period = models.ForeignKey(ProductionPeriod, on_delete=models.CASCADE)
    surface = models.ForeignKey(Surface, on_delete=models.CASCADE)
    label = models.TextField()


class Alerts(models.Model):
    # TODO : use this model an delete the history model
    area_concerned = models.ForeignKey(CultivatedArea, on_delete=models.CASCADE)
    original_cultural_operation = models.ForeignKey(CulturalOperation, on_delete=models.CASCADE)
    postponement = models.IntegerField(default=0)
    date = models.DateField(null=True)
    duration = models.IntegerField(null=True)
    done = models.BooleanField(default=False)

    def __str__(self):
        return str(self.original_C_Operation) + " Reporté de " + str(self.postponement)

