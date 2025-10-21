import uuid

from django.db import models

from .constants import PENDING, IN_PROGRESS, DONE
from users.models import User


class Task(models.Model):
    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (IN_PROGRESS, "In Progress"),
        (DONE, "Done"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    due_date = models.DateTimeField()
    idempotency_key = models.CharField(
        max_length=255, blank=True, null=True, unique=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"User: {self.user} -- {self.id} {self.title} ({self.status})"
