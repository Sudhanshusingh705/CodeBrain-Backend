from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import random
from django.utils import timezone
from django.db import models


class StudentManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone_number, password=None):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, first_name, last_name, phone_number, password=None):
        user = self.create_user(email, first_name, last_name, phone_number, password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True  # Ensure superuser is active
        user.save(using=self._db)
        return user
    
class Student(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('trainer', 'Trainer'),
        ('counselor', 'Counselor'),
    ]
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True, max_length=255)
    phone_number = models.CharField(max_length=15)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    is_verified = models.BooleanField(default=False) 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']
    objects = StudentManager()

    def __str__(self):
        return self.email
    
    def generate_otp(self):
        self.otp = str(random.randint(100000, 999999))
        self.otp_created_at = timezone.now()
        self.save()

class Trainer(models.Model):
    user = models.OneToOneField(Student, on_delete=models.CASCADE)
    expertise = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

class Counsellor(models.Model):
    user = models.OneToOneField(Student, on_delete=models.CASCADE)
    expertise = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)