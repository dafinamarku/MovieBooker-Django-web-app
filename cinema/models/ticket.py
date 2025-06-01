from django.contrib.auth.models import User
from django.db import models
from cinema.models import Seat
from cinema.models.screening import Screening


class Ticket(models.Model):
    screening = models.ForeignKey(Screening, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('screening', 'seat')
