from django.db import models

# Create your models here.

class Pharmacy(models.Model) :
    category = models.CharField(max_length=25)

    def __str__(self) :
        return self.category

class Medicines(models.Model) :
    category = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    quantity = models.IntegerField()
    price = models.FloatField()
    image = models.ImageField()

    def __str__(self) :
        return self.name