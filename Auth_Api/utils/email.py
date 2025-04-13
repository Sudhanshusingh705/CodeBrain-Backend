# utils/email.py
from django.core.mail import send_mail
from django.conf import settings


def send_otp_email(email, otp):
    """Send an OTP email to the user."""
    subject = 'Your OTP Code'
    message = f'Your OTP code is: {otp}'
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )

def send_new_otp_email(email, otp):
    """Send a new OTP email to the user when the old one expires."""
    subject = 'Your New OTP Code'
    message = f'Your new OTP code is: {otp}'
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )