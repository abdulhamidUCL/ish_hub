from django.db import models
from companies.models import Company


# Create your models here.
class Job(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()

    employment_choices = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('remote', 'Remote'),
    ]

    employment_type = models.CharField(choices=employment_choices, max_length=50, default='full_time')

    city = models.CharField(max_length=50)
    category = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title