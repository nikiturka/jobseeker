from django.db import models
from main.models import CustomUser


class Room(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(CustomUser)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Чаты'
