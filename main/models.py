from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.postgres.fields import IntegerRangeField, DecimalRangeField
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Company(models.Model):
    name = models.CharField(max_length=100)
    employees = IntegerRangeField()
    contact_info = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    title = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    salary_range = IntegerRangeField()
    required_experience_range = DecimalRangeField()
    description = models.TextField()
    responsibilities = models.TextField()
    requirements = models.TextField()
    benefits = models.TextField()

    class Meta:
        verbose_name_plural = "Vacancies"

    def __str__(self):
        return f"{self.title} at {self.company}"


class User(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField()
    password = models.CharField(max_length=64)
    profile_picture = models.IntegerField()
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    contact_info = models.CharField(max_length=200)


class Response(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает рассмотрения'),
        ('accepted', 'Принят'),
        ('rejected', 'Отклонён'),
    ]
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
