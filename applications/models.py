from django.db import models
from jobs.models import Job
from django.contrib.auth.models import User
# Create your models here.

class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cover_letter = models.TextField(help_text='Space for your cover letter')
    cover_letter_file = models.FileField(upload_to='cover_letters/', null=True, blank=True)

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("reviewed", "Reviewed"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    applied_at = models.DateTimeField(auto_now_add=True)



