from datetime import datetime, timedelta
import uuid
import random
from django.conf import settings
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.tokens import RefreshToken, TokenError, AccessToken
from django.contrib.auth import authenticate
from rest_framework.response import Response
from .models import User, OTP

def get_user_from_token(access_token):
    try:
        decoded_token = AccessToken(access_token) 
        user_id = decoded_token['user_id']  
        user = User.objects.get(id=user_id) 
        return user
    except (ObjectDoesNotExist, KeyError):
        return None
    
class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(
        write_only=True,
        min_length=settings.MIN_PASSWORD_LENGTH,
        required=True,
        error_messages={
            "blank": "Password cannot be empty",
            "min_length": f"Password must be at least {settings.MIN_PASSWORD_LENGTH} characters",
        },
    )
    password2 = serializers.CharField(
        write_only=True,
        min_length=settings.MIN_PASSWORD_LENGTH,
        required=True,
        error_messages={
            "blank": "Password cannot be empty",
            "min_length": f"Password re type must be at least {settings.MIN_PASSWORD_LENGTH} characters",
        },
    )
    class Meta:
        model=User
        fields = [
            "username", 
            "email", 
            "phone_number", 
            "password1", 
            "password2"
        ]
    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError("Passwords do not match!")
        return data
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            phone_number=validated_data["phone_number"],
            password=validated_data["password1"]
        )
        
        return user

class OTPSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(max_length=6, min_length=6)
    email = serializers.EmailField(max_length=255, min_length=6)
    note = serializers.ChoiceField(choices=OTP.NOTE_CHOICES)
    class Meta:
        model = OTP
        fields = ["otp", "email", "note"]

    def validate(self, data):
        otp_obj = OTP.objects.filter(email=data["email"], note=data["note"])
        if otp_obj.exists():
            raise serializers.ValidationError("OTP is already sent")  
        
        return data


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=6, allow_null=True)
    phone_number = serializers.CharField(max_length=10, min_length=10, allow_null=True)
    password = serializers.CharField(
        write_only=True,
        min_length=settings.MIN_PASSWORD_LENGTH,
        required=True,
        error_messages={
            "blank": "Password cannot be empty",
            "min_length": f"Password must be at least {settings.MIN_PASSWORD_LENGTH} characters",
        },
    )
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)
    class Meta:
        model = User
        fields = ["email", "phone_number", "password", "access_token", "refresh_token"]
    
    def validate(self, data):
        email = data.get("email")
        phone_number = data.get("phone_number")
        password = data.get("password")

        if not email and not phone_number:
            raise serializers.ValidationError("You must provide either an email or a phone number")

        user = None
        if email:
            user = User.objects.filter(email=email).first()
        elif phone_number:
            user = User.objects.filter(phone_number=phone_number).first()
        if not user or not user.check_password(password):
            raise serializers.ValidationError("Invalid credentials")

        if not user.is_verified:
            raise serializers.ValidationError("Email is not verified")

        token = user.token()
        return {
            "email": user.email,
            "access_token": str(token["access"]),
            "refresh_token": str(token["refresh"]),
        }

class PasswordValidatorMixin:
    def validate_passwords_match(self, password1, password2):
        if password1 != password2:
            raise serializers.ValidationError("Passwords do not match")
        return password1

    def validate_password_length(self, password):
        if len(password) < settings.MIN_PASSWORD_LENGTH:
            raise serializers.ValidationError(
                f"Password must be at least {settings.MIN_PASSWORD_LENGTH} characters"
            )
        return password

class ChangePasswordSerializer(serializers.ModelSerializer, PasswordValidatorMixin):
    old_password = serializers.CharField(write_only=True)
    new_password1 = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

    def validate(self, data):
        request = self.context.get('request')
        auth_header = request.headers.get('Authorization')
        if not auth_header or 'Bearer ' not in auth_header:
            raise serializers.ValidationError({'error': 'Invalid Authorization header'})
        access_token = auth_header.split('Bearer ')[1]
        user = get_user_from_token(access_token)
        if not user:
            raise serializers.ValidationError("Invalid access token")

        if not user.check_password(data['old_password']):
            raise serializers.ValidationError("Current password is incorrect")

        if data['old_password'] == data['new_password1']:
            raise serializers.ValidationError(
                "New password must be different from current password"
            )

        self.validate_password_length(data['new_password1'])
        self.validate_passwords_match(data['new_password1'], data['new_password2'])
        
        self.instance = user
        return data

    def save(self):
        self.instance.set_password(self.validated_data['new_password1'])
        self.instance.save()
        return self.instance

class ForgotPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['email']

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No account found with this email")
        return value

class ForgotPasswordVerifier(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(min_length=6, max_length=6)

class ForgotPasswordResetSerializer(serializers.ModelSerializer, PasswordValidatorMixin):
    new_password1 = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']

    def validate(self, data):
        request = self.context.get('request')
        auth_header = request.headers.get('Authorization')
        if not auth_header or 'Bearer ' not in auth_header:
            raise serializers.ValidationError({'error': 'Invalid Authorization header'})
        access_token = auth_header.split('Bearer ')[1]
        user = get_user_from_token(access_token)
        if not user:
            raise serializers.ValidationError("Invalid access token")

        self.validate_password_length(data['new_password1'])
        self.validate_passwords_match(data['new_password1'], data['new_password2'])
        
        self.instance = user
        return data

    def save(self):
        self.instance.set_password(self.validated_data['new_password1'])
        self.instance.save()
        return self.instance