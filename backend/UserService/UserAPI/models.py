from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid
from django.core.validators import RegexValidator
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timedelta
from django.utils import timezone
phone_regex = RegexValidator(
    regex=r"^\d{10}$", message="Phone number must be 10 digits only."
)

class UserManager(BaseUserManager):
    def create_user(self, username, phone_number, password=None, **extra_fields):
        if not username:
            raise ValueError("Users must have a username")
        if not phone_number:
            raise ValueError("Users must have a phone number")

        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)

        user = self.model(username=username, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, phone_number, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(username, phone_number, password, **extra_fields)

class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    phone_number = models.CharField(
        validators=[phone_regex], max_length=10, blank=False, null=False, unique=True
    )
    last_login = models.DateTimeField(auto_now=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = "username"  
    REQUIRED_FIELDS = ["phone_number"]

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def __str__(self):
        return self.username


class OTP(models.Model):
    email = models.CharField(max_length=255, default="")
    otp = models.CharField(max_length=6)
    otp_expiry = models.DateTimeField(default=timezone.now() + timedelta(minutes=settings.MAX_OTP_TIME))
    # max_otp_try = models.IntegerField(default=settings.MAX_OTP_TRY)
    # otp_try = models.IntegerField(default=0)

    REGISTER = "register"
    CHANGE_PASSWORD = "change_password"
    CHANGE_EMAIL = "change_email"
    CHANGE_PHONE_NUMBER = "change_phone_number"

    NOTE_CHOICES = [
        (REGISTER, "Register"),
        (CHANGE_PASSWORD, "Change Password"),
        (CHANGE_EMAIL, "Change Email"),
        (CHANGE_PHONE_NUMBER, "Change Phone Number"),
    ]

    note = models.CharField(max_length=20, choices=NOTE_CHOICES, default=REGISTER)

    def __str__(self):
        return self.email + " | " + self.note
