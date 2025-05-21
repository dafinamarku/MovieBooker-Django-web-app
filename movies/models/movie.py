from django.db import models
from django.utils import timezone

from common.models.entity import Entity
from movies.models.genre import Genre


class Movie(Entity):
    title = models.CharField(max_length=255, unique=True)
    genres = models.ManyToManyField(Genre)
    description = models.TextField()
    photo = models.ImageField()
    release_date = models.DateTimeField(default=timezone.now)
    duration_in_minutes = models.PositiveIntegerField()
    age_limit = models.PositiveIntegerField(null=True)


    def __str__(self):
        return self.title
