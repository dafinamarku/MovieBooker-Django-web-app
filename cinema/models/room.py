from django.core.exceptions import ValidationError
from django.db import models
from common.models.entity import Entity


class Room(Entity):
    name = models.CharField(max_length=100)
    opening_time = models.TimeField()
    closing_time = models.TimeField()

    def __str__(self):
        return self.name

    def clean(self):
        if self.opening_time and self.closing_time:
            if self.opening_time >= self.closing_time:
                raise ValidationError({
                    'closing_time': 'Closing time must be after opening time.',
                })