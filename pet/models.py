# app/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Species(models.Model):
    name = models.CharField(max_length=255)
    sprite_sheet = models.CharField(max_length=255, default='default.png')
    sprite = models.CharField(max_length=255, default='default.png')

    def __str__(self):
        return self.name



class Pet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='pet')
    name = models.CharField(max_length=255)
    level = models.IntegerField(default=1)
    species = models.ForeignKey(Species, on_delete=models.CASCADE)
