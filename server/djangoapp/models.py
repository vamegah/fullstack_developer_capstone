# Uncomment the following imports before adding the Model code

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.


class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # Other fields as needed

    def __str__(self):
        return self.name  # Return the name as the string representation


class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('COUPE', 'Coupe'),
        ('CONVERTIBLE', 'Convertible'),
        ('HATCHBACK', 'Hatchback'),
        ('PICKUP', 'Pickup Truck'),
        ('VAN', 'Van'),
        ('MINIVAN', 'Minivan'),
        ('SPORTS', 'Sports Car'),
        ('HYBRID', 'Hybrid'),
        ('ELECTRIC', 'Electric'),
        ('CROSSOVER', 'Crossover'),
        ('LUXURY', 'Luxury Car'),
        ('OFFROAD', 'Off-Road Vehicle'),
        ('MOTORCYCLE', 'Motorcycle'),
        ('TRUCK', 'Truck'),
    ]

    type = models.CharField(max_length=15, choices=CAR_TYPES, default='SUV')
    year = models.IntegerField(default=2023,
                               validators=[
                                   MaxValueValidator(2023),
                                   MinValueValidator(2015)
                               ])
    # Other fields as needed

    def __str__(self):
        return self.name  # Return the name as the string representation
