from django.db import models
from common.models.entity import Entity


class Genre(Entity):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name