from django.contrib import admin
# from .models import related models
from .models import CarModel, CarMake
#from .models import Course, Lesson

# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 1

# # CarModelAdmin class

class CarModelAdmin(admin.ModelAdmin):
    fields = ['dealerID', 'model_name', 'car_type', 'make', 'year']
    
# # CarMakeAdmin class with CarModelInline

class CarMakeAdmin(admin.ModelAdmin):
    fields = ['name', 'description']
    inlines = [CarModelInline]

# # Register models here
admin.site.register(CarMake,CarMakeAdmin)
admin.site.register(CarModel,CarModelAdmin)
