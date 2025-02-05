from django.db import models

# Create your models here.

class UserProfile(models.Model):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('instructor', 'Instructor'),
        ('student', 'Student'),
    )

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='student')