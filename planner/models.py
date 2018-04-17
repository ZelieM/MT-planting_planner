from datetime import timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, transaction
from django.urls import reverse
from model_utils.managers import InheritanceManager
from django.utils.translation import gettext_lazy as _

from vegetables_library import models as library_models

NAME_MAX_LENGTH = 100
TYPE_MAX_LENGTH = 100


class Garden(models.Model):
    name = models.CharField(unique=True, max_length=NAME_MAX_LENGTH, verbose_name="Nom du jardin")
    postal_code = models.IntegerField(validators=[MaxValueValidator(9999), MinValueValidator(1000)])
    users = models.ManyToManyField(User)
    reference_email = models.EmailField(_('email address'), blank=True)
    notification_delay = models.IntegerField(default=5)
    comment = models.TextField(blank=True, default="", verbose_name="Description libre du jardin")
    soil_type = models.CharField(max_length=TYPE_MAX_LENGTH, blank=True, default="", verbose_name='Type de sol')
    culture_type = models.CharField(max_length=TYPE_MAX_LENGTH, blank=True, default="",
                                    verbose_name='Type d\'agriculture pratiquée sur ce jardin')
    # Confidentiality fields, if set to true, the garden's data are accessible for research
    details_available_for_research = models.BooleanField(default=True,
                                                         verbose_name="J'accepte que les données de mon jardin soient accessibles pour la recherche universitaire")
    activity_data_available_for_research = models.BooleanField(default=True,
                                                               verbose_name="J'accepte que les données de mes récoltes soient accessibles pour la recherche universitaire")

    def __str__(self):
        return "Garden: " + self.name

    def get_absolute_url(self):
        return reverse('planner:alerts_view', kwargs={'garden_id': self.id})


class Vegetable(models.Model):
    name = models.CharField(max_length=100)
    variety = models.CharField(max_length=100, blank=True, default="")
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE)
    # Field filled with primary key of vegetable from the library when exporting
    extern_id = models.IntegerField(null=True)

    def __str__(self):
        if self.variety:
            return self.name + " - " + self.variety
        else:
            return self.name

    class Meta:
        unique_together = ('name', 'variety', 'garden')


class CulturalOperation(models.Model):
    objects = InheritanceManager()
    name = models.CharField(max_length=NAME_MAX_LENGTH, verbose_name=_('Nom de l\'action'))
    vegetable = models.ForeignKey(Vegetable, on_delete=models.CASCADE, verbose_name=_('Légume concerné'))
    duration = models.DurationField(verbose_name=_('Temps nécessaire par m²'), default=timedelta(seconds=0))

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


class Bed(models.Model):
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE)
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    length = models.IntegerField()
    width = models.IntegerField()

    comment = models.TextField(blank=True, default="")
    soil_type = models.CharField(max_length=TYPE_MAX_LENGTH, blank=True, default="")

    NORTH = 'N'
    SOUTH = 'S'
    WEST = 'O'
    EAST = 'E'
    NE = 'NE'
    SE = 'SE'
    SW = 'SO'
    NW = 'NO'
    EXPOSITION_CHOICES = (
        (NORTH, 'Nord'),
        (SOUTH, 'Sud'),
        (WEST, 'Ouest'),
        (EAST, 'Est'),
        (NE, 'Nord-Est'),
        (SE, 'Sud-Est'),
        (SW, 'Sud-Ouest'),
        (NW, 'Nord-Ouest')
    )

    exposition = models.CharField(max_length=2, choices=EXPOSITION_CHOICES, default=NORTH)

    @property
    def get_area(self):
        return (self.length * self.width) / 10000  # Division to have m² instead of cm²

    def __str__(self):
        return self.name + " : " + str(self.length) + "x" + str(self.width)


class CultivatedArea(models.Model):
    vegetable = models.ForeignKey(Vegetable, blank=True, null=True, on_delete=models.SET_NULL)
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE)
    surface = models.ForeignKey(Bed, on_delete=models.CASCADE)
    label = models.TextField()
    # Following attributes are related to the harvest of this cultivated area
    is_active = models.BooleanField(default=True)  # Set to false when we harvest this cropping
    harvest_date = models.DateField(null=True)
    executor = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    kg_produced = models.IntegerField(blank=True, default=0)
    total_selling_price = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.label


class ForthcomingOperation(models.Model):
    area_concerned = models.ForeignKey(CultivatedArea, on_delete=models.CASCADE)
    original_cultural_operation = models.ForeignKey(CulturalOperation, on_delete=models.CASCADE)
    postponement = models.IntegerField(default=0)
    execution_date = models.DateField(blank=True, null=True)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return str(self.area_concerned.label) + " " + str(self.original_cultural_operation)


class History(models.Model):
    garden = models.OneToOneField(Garden, on_delete=models.CASCADE)


class HistoryItem(models.Model):
    objects = InheritanceManager()
    history = models.ForeignKey(History, on_delete=models.CASCADE)
    execution_date = models.DateField()
    executor = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    area_concerned = models.ForeignKey(CultivatedArea, on_delete=models.SET_NULL, blank=True, null=True)


class Observation(HistoryItem):
    description = models.TextField()


class Operation(HistoryItem):
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    note = models.TextField(blank=True, default="")
    duration = models.DurationField(blank=True, null=True)
    is_deletion = models.BooleanField(default=False)
    original_alert = models.ForeignKey(ForthcomingOperation, on_delete=models.SET_NULL, blank=True, null=True)
