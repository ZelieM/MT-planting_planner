from datetime import timedelta

from django.db import models, transaction
from model_utils.managers import InheritanceManager
from django.utils.translation import gettext_lazy as _

NAME_MAX_LENGTH = 100


class Vegetable(models.Model):
    name = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.name


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
