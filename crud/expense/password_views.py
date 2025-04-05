from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()

class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_404_NOT_FOUND)
        user = get_object_or_404(User, email=email)
        token = default_token_generator.make_token(user)
        reset_url = request.build_absolute_uri(reverse('reset-password', args=[user.pk, token]))
        send_mail("Password Reset Request", f"Reset link:\n{reset_url}", settings.EMAIL_HOST_USER, [user.email])
        return Response({"message": "Reset link sent"}, status=200)

class ResetPasswordView(APIView):
    def post(self, request, user_id, token):
        user = get_object_or_404(User, pk=user_id)
        if not default_token_generator.check_token(user, token):
            return Response({"error": "Invalid or expired token"}, status=400)
        new_password = request.data.get("password")
        if not new_password:
            return Response({"error": "New password is required"}, status=400)
        user.set_password(new_password)
        user.save()
        return Response({"message": "Password has been reset."}, status=200)
