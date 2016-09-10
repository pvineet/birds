from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

class Family(models.Model):
    name = models.CharField(max_length=200)

class Specie(models.Model):
    name = models.CharField(max_length=200)
