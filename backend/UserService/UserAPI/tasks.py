from celery import shared_task
import requests
import random
from datetime import timedelta, datetime
from .models import User, OTP
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
@shared_task
def verify_mail_with_otp(email, otp):
    # otp = random.randint(100000, 999999)
    # user = User.objects.get(email=email)
    subject = "Verify your email with OTP"
    body = "Thanks for registering with us. Your OTP is: " + str(otp)
    # otp_obj = OTP.objects.create(email=email, otp=otp)
    send_mail(subject, 
              body, 
              settings.EMAIL_HOST_USER, 
              [email],
              fail_silently=False)
    print(f"✅ Sent OTP to {email}.")
@shared_task
def check_otp_expiry():
    curr_time = datetime.now()
    expired_otps = OTP.objects.filter(otp_expiry__lte=curr_time)
    count = expired_otps.count()
    expired_otps.delete()
    print(f"\n✅ Deleted {count} expired OTPs.\n")

@shared_task
def delete_expired_temp_users():
    expired_users = User.objects.filter(is_verified=False, date_joined__lte=datetime.now() - timedelta(minutes=5))
    count = expired_users.count()
    expired_users.delete()
    print(f"\n✅ Deleted {count} not verified users.\n")