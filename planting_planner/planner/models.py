from django.db import models

class Garden(models.Model):
    name = models.CharField(unique=True, max_length=100)
    def __str__(self):
        return "Garden: " + self.name

class Bed(models.Model):
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    length = models.IntegerField()
    width = models.IntegerField()

    def __str__(self):
        return self.name + " : "+ str(self.length)+ "x" + str(self.width)
