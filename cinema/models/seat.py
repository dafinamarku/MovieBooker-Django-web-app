from django.db import models
from cinema.models import Room
from common.models.entity import Entity


class Seat(Entity):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='seats')
    row = models.CharField(max_length=5)  # example: 'A', 'B', 'C'
    number = models.PositiveIntegerField()

    class Meta:
        unique_together = ('room', 'row', 'number')
        ordering = ['row', 'number']

    def __str__(self):
        return f"{self.row}{self.number} - {self.room.name}"