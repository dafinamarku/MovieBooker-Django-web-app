from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Entity(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_%(class)s")
    created_on = models.DateTimeField(default=timezone.now)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="changed_%(class)s")
    changed_on = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True
