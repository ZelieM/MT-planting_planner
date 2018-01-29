from django.db import models


class Garden(models.Model):
    name = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return "Garden: " + self.name

    def get_absolute_url(self):
        return "/planner/%i/" % self.id


class Bed(models.Model):
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    length = models.IntegerField()
    width = models.IntegerField()

    def __str__(self):
        return self.name + " : "+ str(self.length)+ "x" + str(self.width)


class Vegetable(models.Model):
    name = models.CharField(unique= True,max_length=100)


class Event(models.Model):
    bed = models.ForeignKey(Bed,on_delete=models.CASCADE)
    vegetable = models.ForeignKey(Vegetable, on_delete=models.CASCADE)
    seeding_start = models.DateField()
    seeding_end = models.DateField()
    harvest_start = models.DateField()
    harvest_end = models.DateField()
