from django.contrib import admin
from .models import CarMake, CarModel

# Registering models with their respective admins
admin.site.register(CarMake)

# CarMakeAdmin class with CarModelInline
admin.site.register(CarModel)
