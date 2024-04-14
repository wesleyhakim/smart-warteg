from django.db import models

class DishCleanerSensor(models.Model):
    name = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=5, decimal_places=1)
    timestamp = models.DateTimeField()

class DishCleanerActuator(models.Model):
    name = models.CharField(max_length=100)
    status = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    timestamp = models.DateTimeField()

class StoveSafetySensor(models.Model):
    name = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=5, decimal_places=1)
    timestamp = models.DateTimeField()

class StoveSafetyActuator(models.Model):
    name = models.CharField(max_length=100)
    status = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    timestamp = models.DateTimeField()

class CustomerSensor(models.Model):
    name = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=5, decimal_places=1)
    timestamp = models.DateTimeField()

class CustomerActuator(models.Model):
    name = models.CharField(max_length=100)
    status = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    timestamp = models.DateTimeField()
