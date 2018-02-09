from django.db import models
from model_utils.managers import InheritanceManager


NAME_MAX_LENGTH = 100


class Garden(models.Model):
    name = models.CharField(unique=True, max_length=NAME_MAX_LENGTH, verbose_name="Nom du jardin")

    def __str__(self):
        return "Garden: " + self.name

    def get_absolute_url(self):
        return "/planner/%i/" % self.id


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
    vegetable = models.ForeignKey(Vegetable, null=True, on_delete=models.SET_NULL)
    production_period = models.ForeignKey(ProductionPeriod, on_delete=models.CASCADE)

    @property
    def get_area(self):
        raise NotImplementedError()

    def __str__(self):
        return "Surface from production period starting :" + str(self.production_period) + " Area : " + self.get_area()


class Bed(Surface):
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    length = models.IntegerField()
    width = models.IntegerField()

    def get_area(self):
        return self.length*self.width

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

    def __str__(self):
        return self.name + " " + str(self.vegetable)


class COWithOffset(CulturalOperation):
    offset_in_days = models.IntegerField()
    previous_operation = models.ForeignKey(CulturalOperation, related_name='+', on_delete=models.CASCADE)


class COWithDate(CulturalOperation):
    absoluteDate = models.DateField()


class CompletedOperation(models.Model):
    production_period = models.ForeignKey(ProductionPeriod, on_delete=models.CASCADE)
    original_C_Operation = models.ForeignKey(CulturalOperation, on_delete=models.CASCADE)
    date = models.DateField()
    duration = models.IntegerField()
    surface_processed = models.IntegerField()
