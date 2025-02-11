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


class Courses(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    instructor = models.ForeignKey(UserProfile, on_delete=models.CASCADE, limit_choices_to={'role': 'instructor'})
    created_at = models.DateTimeField(auto_now_add=True)


class Enrollment(models.Model):
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
