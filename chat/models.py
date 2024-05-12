from django.db import models
from main.models import CustomUser


class Room(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(CustomUser)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Чаты'


class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at', )
