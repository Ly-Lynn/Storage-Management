from django.shortcuts import render
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
import random
from django.core.cache import cache
from .models import User, OTP
from .serializers import (RegisterSerializer, 
                          OTPSerializer,
                          LoginSerializer,
                          ChangePasswordSerializer,
                          ForgotPasswordSerializer,
                          ForgotPasswordVerifier,
                          ForgotPasswordResetSerializer)
from .tasks import verify_mail_with_otp
from datetime import datetime
from django.conf import settings
# Create your views here.

class VerifyOTPMixin:
    def _handle_invalid_otp(self, email, cache_key):
        if OTP.objects.filter(email=email).exists():
            cache_data = cache.get(cache_key) or {'attempts': 0}
        else: 
            return Response("OTP is already expired, please try again", status=status.HTTP_404_NOT_FOUND)
        attempts = cache_data['attempts'] + 1
        cache_data['attempts'] = attempts
        cache.set(cache_key, cache_data, timeout=300)

        if attempts >= (settings.MAX_OTP_TRY+1):
            cache.delete(cache_key)
            OTP.objects.filter(email=email).delete()
            return Response(
                {"message": "Maximum OTP attempts reached. Please request a new OTP."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({
            "message": f"Invalid OTP. {settings.MAX_OTP_TRY - attempts} attempts remaining"
        }, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(viewsets.ViewSet):
    serializer_class = RegisterSerializer

    def create(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        if serializer.is_valid(raise_exception=True):
            cache_key = f"user_registration_{user['email']}"
            cache.set(cache_key, user, timeout=300)

            otp = str(random.randint(100000, 999999))
              # 5 minutes expiry

            if not OTP.objects.filter(email=user["email"], otp=otp).exists():
                otp_serializer = OTPSerializer(data={"otp": otp, "email": user["email"], "note":"register"})
                cache_key = f"cache_user_registration_{user["email"]}"
                cache.set(cache_key, {
                    'email': user["email"],
                    'otp': otp,
                    'attempts': 0
                }, timeout=settings.MAX_OTP_TIME * 60)  # 5 minutes expiry
                if otp_serializer.is_valid():
                    otp_serializer.save()
                    
                else:
                    return Response(otp_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Send mail
            verify_mail_with_otp(user["email"], otp)

            return Response("Verification email has been sent", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class VerifyEmail(generics.GenericAPIView):
    """
        Verify the email with OTP POST request
    """
    serializer_class = RegisterSerializer
    handle_invalid_otp = VerifyOTPMixin._handle_invalid_otp
    def post(self, request):
        data = request.data
        otp = data["otp"]
        email = data["email"]
        otp_user_obj = OTP.objects.filter(email=email, otp=otp, note=OTP.REGISTER).first()

        if otp_user_obj:
            cache_key = f"user_registration_{email}"
            user_data = cache.get(cache_key)
            if user_data:
                serializer = self.serializer_class(data=user_data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()

                cache.delete(cache_key)
                otp_user_obj.delete()
                return Response("Email verified", status=status.HTTP_200_OK)
            return Response("Lost registration information", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return self.handle_invalid_otp(email=email, cache_key=f"cache_user_registration_{email}")
            # user = OTP.objects.get(email=email)
            # if user:
            #     user.otp_try += 1
            #     user.save()
            #     if user.otp_try >= user.max_otp_try:
            #         user.delete()
            #         return Response("Invalid OTP, max OTP try reached, please resend the OTP", status=status.HTTP_400_BAD_REQUEST)
            #     return Response(f"Invalid OTP, please try again, {user.max_otp_try - user.otp_try} times left", status=status.HTTP_406_NOT_ACCEPTABLE)
            # return Response("OTP is already expired, please try again", status=status.HTTP_404_NOT_FOUND)

class LoginView(viewsets.ViewSet):
    serializer_class = LoginSerializer

    def create(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ChangePasswordView(viewsets.ViewSet):
    serializer_class = ChangePasswordSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()  # Using the serializer's update method
            return Response(
                {"message": "Password changed successfully"},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            # Generate and save OTP
            otp = str(random.randint(100000, 999999))
            cache_key = f"cache_forgot_password_{email}"
            cache.set(cache_key, {
                'email': email,
                'otp': otp,
                'attempts': 0
            }, timeout=300)  # 5 minutes expiry

            # Create OTP record
            otp_serializer = OTPSerializer(data={
                "otp": otp,
                "email": email,
                "note": OTP.CHANGE_PASSWORD
            })
            if otp_serializer.is_valid():
                otp_serializer.save()
                # Send verification email
                verify_mail_with_otp(email, otp)
                return Response(
                    {"message": "Password reset verification email has been sent"},
                    status=status.HTTP_201_CREATED
                )
            return Response(otp_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ForgotPasswordVerifyView(generics.GenericAPIView):
    serializer_class = ForgotPasswordVerifier
    handle_invalid_otp = VerifyOTPMixin._handle_invalid_otp

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']
        
        # Verify OTP
        otp_record = OTP.objects.filter(
            email=email,
            otp=otp,
            note=OTP.CHANGE_PASSWORD
        ).first()

        if not otp_record:
            return self.handle_invalid_otp(email=email, cache_key=f"cache_forgot_password_{email}")

        # OTP is valid
        user = User.objects.get(email=email)
        access_token = user.token()["access"]
        otp_record.delete()
        
        return Response({
            "access_token": access_token,
            "message": "OTP verified successfully"
        }, status=status.HTTP_200_OK)

    
class ForgotPasswordResetView(generics.GenericAPIView):
    serializer_class = ForgotPasswordResetSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Password reset successfully"},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)