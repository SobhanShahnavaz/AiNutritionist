from django.db import models

class ExercieMaps(models.Model):
  Label = models.IntegerField(default=0)
  TextEnglish = models.CharField(max_length=255)
  TextPersian = models.CharField(max_length=255)

class DietMaps(models.Model):
  Label = models.IntegerField(default=0)
  TextEnglish = models.CharField(max_length=511)
  Veggies = models.CharField(max_length=255)
  Protein = models.CharField(max_length=255)
  Juice = models.CharField(max_length=255)