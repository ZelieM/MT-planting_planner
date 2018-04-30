from datetime import timedelta

from django.db import models, transaction
from model_utils.managers import InheritanceManager
from django.utils.translation import gettext_lazy as _

NAME_MAX_LENGTH = 100

# Vegetables type
FRUIT = 'fruit'
GRAINE = 'graine'
RACINE = 'racine'
FEUILLE = 'feuille'
AUTRE = 'autre'
VEGETABLE_TYPE_CHOICES = (
    (FRUIT, FRUIT),
    (GRAINE, GRAINE),
    (RACINE, RACINE),
    (FEUILLE, FEUILLE),
    (AUTRE, AUTRE)
)

AIZOACEES = 'Aizoacées'
AMARANTHACEES = 'Amaranthacées'
AMARYLLIDACEES = 'Amaryllidacées'
APIACEES = 'Apiacées'
ASTERACEES = 'Astéracées'
BORAGINACEES = 'Boraginacées'
BRASSICACEES = 'Brassicacées'
CHENOPODIACEES = 'Chénopodiacées'
CUCURBITACEES = 'Cucurbitacées'
FABACEES = 'Fabacées'
LABIEES = 'Labiées'
LAMIACEES = 'Lamiacées'
LEGUMINEUSES = 'Légumineuses'
LILIACEES = 'Liliacées'
PAPILIONACEES = 'Papilionacées'
POACEES = 'Poacées'
POLYGONACEES = 'Polygonacées'
SOLANACEES = 'Solanacées'
VALERIANACEES = 'Valérianacées'
FAMILY_CHOICES = (
    (AIZOACEES, AIZOACEES),
    (AMARANTHACEES, AMARANTHACEES),
    (AMARYLLIDACEES, AMARYLLIDACEES),
    (APIACEES, APIACEES),
    (ASTERACEES, ASTERACEES),
    (BORAGINACEES, BORAGINACEES),
    (BRASSICACEES, BRASSICACEES),
    (CHENOPODIACEES, CHENOPODIACEES),
    (CUCURBITACEES, CUCURBITACEES),
    (FABACEES, FABACEES),
    (LABIEES, LABIEES),
    (LAMIACEES, LAMIACEES),
    (LEGUMINEUSES, LEGUMINEUSES),
    (LILIACEES, LILIACEES),
    (PAPILIONACEES, PAPILIONACEES),
    (POACEES, POACEES),
    (POLYGONACEES, POLYGONACEES),
    (SOLANACEES, SOLANACEES),
    (VALERIANACEES, VALERIANACEES),
    (AUTRE, AUTRE)
)


class Species(models.Model):
    """ A species is classification level on top of a variety. A species can be for example a Tomato,
    which belong to Solanacea's family and is a vegetable of type fruit"""
    french_name = models.CharField(max_length=NAME_MAX_LENGTH)
    latin_name = models.CharField(max_length=NAME_MAX_LENGTH, null=True, blank=True)
    family = models.CharField(max_length=NAME_MAX_LENGTH, choices=FAMILY_CHOICES, default=AUTRE)
    vegetable_type = models.CharField(max_length=50, choices=VEGETABLE_TYPE_CHOICES, default=AUTRE)

    def __str__(self):
        return self.french_name


class GroundSeeding(models.Model):
    """ Main dates when sowing in open ground """
    seeding_start = models.DateField()
    seeding_end = models.DateField()
    harvest_start = models.DateField()
    harvest_end = models.DateField()
    cycle_duration = models.IntegerField()

    def __str__(self):
        return "Seeding : " + str(self.seeding_start) + " -> " + str(self.seeding_end) + ' Harvest : ' + \
               str(self.harvest_start) + " -> " + str(self.harvest_end)


class OutOfCupSeeding(models.Model):
    """ Main dates when sowing out of cup """
    seeding_start = models.DateField()
    seeding_end = models.DateField()
    transplant_start = models.DateField(null=True, blank=True)
    transplant_end = models.DateField(null=True, blank=True)
    pots_cycle_duration = models.IntegerField(null=True, blank=True)
    harvest_start = models.DateField()
    harvest_end = models.DateField()
    ground_cycle_duration = models.IntegerField()


class Variety(models.Model):
    """ A variety is a classification level which describe a cultivated vegetable.
    For example: Celebrity is a variety of Tomato"""
    french_name = models.CharField(max_length=NAME_MAX_LENGTH)
    latin_name = models.CharField(max_length=NAME_MAX_LENGTH, null=True, blank=True)
    species = models.ForeignKey(Species, on_delete=models.CASCADE, null=True)
    open_ground_seeding = models.ForeignKey(GroundSeeding, on_delete=models.SET_NULL, null=True)
    out_of_cup_seeding = models.ForeignKey(OutOfCupSeeding, on_delete=models.SET_NULL, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    # TODO ensure that there is at least open ground seeding or out of cup seeding not null

    def __str__(self):
        if self.latin_name:
            return self.french_name + " - " + self.latin_name
        else:
            return self.french_name

    class Meta:
        unique_together = ('french_name', 'species',)


class CulturalOperation(models.Model):
    objects = InheritanceManager()
    name = models.CharField(max_length=NAME_MAX_LENGTH, verbose_name=_('Nom de l\'action'))
    vegetable = models.ForeignKey(Variety, on_delete=models.CASCADE, verbose_name=_('Légume concerné'))
    duration = models.DurationField(verbose_name=_('Temps nécessaire par m²'), default=timedelta(seconds=0))

    # is_initial = models.BooleanField(default=False)

    # @transaction.atomic
    # def save(self, *args, **kwargs):
    #     """  Ensure there is only one initial operation by vegetable """""
    #     if self.is_initial:
    #         CulturalOperation.objects.filter(vegetable_id=self.vegetable_id, is_initial=True).update(is_initial=False)
    #     super(CulturalOperation, self).save(*args, **kwargs)

    def get_date(self):
        pass

    def __str__(self):
        return self.vegetable.french_name + " : " + self.name


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
