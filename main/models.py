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


class Country(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Countries"


class Company(models.Model):
    name = models.CharField(max_length=100)
    employees = IntegerRangeField()
    contact_info = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=32, null=True)
    last_name = models.CharField(max_length=32, null=True)
    expected_salary_range = IntegerRangeField(null=True)
    experience = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    profile_picture = models.ImageField(upload_to='pfp/', null=True)
    resume = models.FileField(upload_to='cv/', blank=True, null=True)
    contact_info = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.user.email


class HR(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    is_hr = models.BooleanField(default=True)
    first_name = models.CharField(max_length=32, null=True)
    last_name = models.CharField(max_length=32, null=True)
    profile_picture = models.ImageField(null=True)
    contact_info = models.CharField(max_length=200, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.user.email


class Vacancy(models.Model):
    WORK_STATUS_CHOICES = [
        ('fulltime', 'Полный рабочий день'),
        ('part-time', 'Частичная занятость'),
        ('remote', 'Удалённая работа'),
    ]

    ENGLISH_LEVEL_CHOICES = [
        ('B1', 'Intermediate'),
        ('B2', 'Upper-Intermediate'),
        ('C1', 'Advanced')
    ]

    title = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    salary_range = IntegerRangeField()
    required_experience_range = DecimalRangeField()
    description = models.TextField()
    responsibilities = models.TextField()
    requirements = models.TextField()
    benefits = models.TextField()
    country = models.ForeignKey(Country, on_delete=models.PROTECT, blank=True)
    work_status = models.CharField(max_length=32, choices=WORK_STATUS_CHOICES, default='fulltime')
    views = models.ManyToManyField(UserProfile, related_name='viewed_vacancies')
    responses = models.ManyToManyField(UserProfile, related_name='responded_vacancies')
    english_level = models.CharField(max_length=32, choices=ENGLISH_LEVEL_CHOICES, default='B2')
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False, blank=True)
    publisher = models.ForeignKey(HR, on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Vacancies"

    def __str__(self):
        return f"{self.title} at {self.company}"


class Response(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает рассмотрения'),
        ('accepted', 'Принят'),
        ('rejected', 'Отклонён'),
    ]
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
