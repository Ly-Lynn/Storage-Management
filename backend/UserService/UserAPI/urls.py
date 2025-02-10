from .views import (RegisterView, 
                    VerifyEmail,
                    LoginView,
                    ChangePasswordView,
                    ForgotPasswordResetView,
                    ForgotPasswordVerifyView,
                    ForgotPasswordView)
from django.urls import path, include
import djoser

urlpatterns = [
    path("user/register/", RegisterView.as_view({"post": "create"})),
    path("user/change-pass/", ChangePasswordView.as_view({"post": "create"})),
    path("user/forgot-pass/", ForgotPasswordView.as_view()),
    path("user/forgot-pass/verify/", ForgotPasswordVerifyView.as_view()),
    path("user/forgot-pass/reset/", ForgotPasswordResetView.as_view()),

    path("user/verify/", VerifyEmail.as_view()),
    path("user/login/", LoginView.as_view({"post": "create"})),
    path("auth/", include("djoser.urls")),    
]