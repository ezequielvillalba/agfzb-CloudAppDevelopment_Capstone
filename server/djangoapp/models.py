# from django.db import models
# from django.utils.timezone import now
# from django.contrib import admin
# from django.core import serializers 
# import uuid
# import json
# Create your models here.

import sys
from django.utils.timezone import now
try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()
import datetime
# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
# Car Make model:
class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    another = models.CharField(max_length=200, blank=True) #Another Field not required
    def __str__(self):
        return self.name

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
# Car Model model:
class CarModel(models.Model):
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'WAGON'
    COUPE = 'COUPE'
    SPORT = 'SPORT'
    HATCHBACK = 'HATCHBACK'
    CONVERTIBLE = 'CONVERTIBLE'
    MINIVAN = 'MINIVAN'
    TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'WAGON'),
        (COUPE, 'Coupe'),
        (SPORT, 'Sport'),
        (HATCHBACK, 'Hatchback'),
        (CONVERTIBLE, 'Convertible'),
        (MINIVAN, 'Mini Van'),
    ]
    YEAR_CHOICES = [(r,r) for r in range(1900, datetime.date.today().year+1)]

    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dealerId = models.IntegerField(default=0)
    type = models.CharField(null=False,max_length=20,choices=TYPE_CHOICES,default=SEDAN)
    year = models.IntegerField(('year'), choices=YEAR_CHOICES, default=datetime.datetime.now().year)

    def __str__(self):
        return self.type + ' - ' + self.name

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer(models.Model):

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        self.address = address          # Dealer address
        self.city = city                # Dealer city
        self.full_name = full_name      # Dealer Full Name
        self.id = id                    # Dealer id
        self.lat = lat                  # Location lat
        self.long = long                # Location long
        self.short_name = short_name    # Dealer short name
        self.st = st                    # Dealer state
        self.zip = zip                  # Dealer zip

    def __str__(self):
        return "Dealer name: " + self.full_name
    
# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview(models.Model):

    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id

    def __str__(self):
        return "id: " + self.full_name + " - Review: " + self.review
