from django.contrib import admin

from .models import DishCleanerActuator
from .models import DishCleanerSensor

from .models import StoveSafetyActuator
from .models import StoveSafetySensor

from .models import CustomerActuator
from .models import CustomerSensor

class DishCleanerActuatorDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'timestamp')
    list_display_links = ('id', 'name')

class DishCleanerSensorDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'value', 'timestamp')
    list_display_links = ('id', 'name')

class StoveSafetyActuatorDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'timestamp')
    list_display_links = ('id', 'name')

class StoveSafetySensorDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'value', 'timestamp')
    list_display_links = ('id', 'name')

class CustomerActuatorDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'timestamp')
    list_display_links = ('id', 'name')

class CustomerSensorDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'value', 'timestamp')
    list_display_links = ('id', 'name')

admin.site.register(DishCleanerSensor, DishCleanerSensorDataAdmin)
admin.site.register(DishCleanerActuator, DishCleanerActuatorDataAdmin)
admin.site.register(StoveSafetySensor, StoveSafetySensorDataAdmin)
admin.site.register(StoveSafetyActuator, StoveSafetyActuatorDataAdmin)
admin.site.register(CustomerSensor, CustomerSensorDataAdmin)
admin.site.register(CustomerActuator, CustomerActuatorDataAdmin)