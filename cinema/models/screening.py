from django.core.exceptions import ValidationError
from datetime import timedelta
from django.db import models
from cinema.models import Room
from common.models.entity import Entity
from movies.models import Movie


class Screening(Entity):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_time = models.DateTimeField()

    def clean(self):
        if not self.movie or not self.room or not self.start_time:
            return

        if self.start_time < self.movie.release_date:
            formatted_date = self.movie.release_date.strftime("%d.%m.%Y %I:%M %p")
            raise ValidationError({
                'start_time': f"Start time must be after the movie's release date ({formatted_date})."
            })

        end_time = self.end_time

        overlapping = Screening.objects.filter(
            room=self.room,
            start_time__lt=end_time,
        )

        for screening in overlapping:
            other_end = screening.end_time
            if other_end > self.start_time:
                raise ValidationError({'room': "The room you chose was already booked for the selected time."})

    @property
    def end_time(self):
        return self.start_time + timedelta(minutes=self.movie.duration_in_minutes)
