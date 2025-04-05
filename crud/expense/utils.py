from django.core.mail import send_mail
from django.conf import settings

def send_welcome_email(email,username,password):
    subject= "Welcome mail To New User"
    message= f"Hello {username},\n\nYour account has been created successfully.\n\nUsername:{username}\nPassword:{password}\n\nPlease change your password after login."
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False
    )