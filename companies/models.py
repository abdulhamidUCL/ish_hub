from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Company(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company')
    name = models.CharField(max_length=200)
    description = models.TextField()
    industry = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    website = models.URLField(max_length=200)
    logo = models.ImageField(upload_to='companies/')
    employee_count = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name
