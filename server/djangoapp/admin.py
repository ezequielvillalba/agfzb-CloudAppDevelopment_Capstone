from django.contrib import admin
from .models import CarMake, CarModel

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 1

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['dealerId', 'make', 'name', 'type', 'year']
    list_filter = ['make', 'name', 'type', 'dealerId']
    search_fields = ['make', 'name', 'type', 'year', 'dealerId']

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ['name', 'description']
    list_filter = ['name']
    search_fields = ['name', 'description']


# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)