from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Transection
from .serializers import TransectionsSerializer, CustomUserSerializer
from .permissions import IsAdminUser, IsManagerUser
from .utils import send_welcome_email
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
User = get_user_model()

# Register User
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            username = user.username
            password = request.data.get("password")
            email = user.email
            send_welcome_email( email,username, password)
            return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
        
        print("Serializer Errors:", serializer.errors)  # Now it will print errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login User & Get JWT Token
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(password):
            return Response({"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "role": user.role
        })
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        # Get the user's token
        token = Token.objects.get(user=request.user)
        token.delete()  # Delete the token (logout user)

        return Response({"message": "Logout successful"}, status=200)
    except Token.DoesNotExist:
        return Response({"error": "User is not logged in"}, status=400)


class ForgotPasswordView(APIView):
    def post(self,request):
        email=request.data.get("email")
        if not email:
            return Response({"error":"Email is required"},status=status.HTTP_404_NOT_FOUND)
        user = get_object_or_404(User,email=email)
        token = default_token_generator.make_token(user)
        reset_url = request.build_absolute_uri(reverse('reset-password',args=[user.pk,token]))
        send_mail(
            "Password Reset Request",
            f"Click theb link below to reset your password:\n{reset_url}",
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False
        )
        return Response({"message":"Password reset link has been sent to your mail"},status=status.HTTP_200_OK)
class ResetPasswordView(APIView):
    def post(self, request, user_id, token):
        user = get_object_or_404(User, pk=user_id)

        if not default_token_generator.check_token(user, token):
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

        new_password = request.data.get("password")
        if not new_password:
            return Response({"error": "New password is required"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)

# Get User Profile
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "email": user.email,
            "role": user.role
        })

# Dashboard Views
class AdminDashboardView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response({"message": "Welcome to the Admin Dashboard!"})

class ManagerDashboardView(APIView):
    permission_classes = [IsManagerUser]

    def get(self, request):
        return Response({"message": "Welcome to the Manager Dashboard!"})

class EmployeeDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Welcome to the Employee Dashboard!"})

# Expense Views
def expense_home(request):
    transactions = Transection.objects.all().values()
    template = loader.get_template('expense/home.html')
    context = {"mymembers": transactions}
    return HttpResponse(template.render(context, request))

def expense_details(request, id):
    transaction = Transection.objects.get(id=id)
    template = loader.get_template('expense/details.html')
    context = {"Transection": transaction}
    return HttpResponse(template.render(context, request))

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_transection(request):
     queryset =Transection.objects.all().order_by('-pk')
     serializer = TransectionsSerializer(queryset,many=True)
     return Response(
          {
               "data": serializer.data
          }
     )
# Transaction API
class TransectionAPI(APIView):
    permission_classes = [IsAuthenticated]

   
    def get(self, request):
        queryset = Transection.objects.all().order_by('-pk')
        serializer = TransectionsSerializer(queryset, many=True)
        return Response({"data": serializer.data})

    def post(self, request):
        if request.user.role != 'admin':
            return Response({"error": "Only admins can create transactions"}, status=status.HTTP_403_FORBIDDEN)

        data = request.data.copy()
        data["user"] = request.user.id
        serializer = TransectionsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Transaction created", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"message": "Data not saved", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        data = request.data
        if not data.get('id'):
            return Response({"message": "ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            transaction = Transection.objects.get(id=data.get('id'))
        except Transection.DoesNotExist:
            return Response({"message": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)

        if request.user.role != 'admin' and transaction.user != request.user:
            return Response({"error": "You can only update your own transactions."}, status=status.HTTP_403_FORBIDDEN)

        serializer = TransectionsSerializer(transaction, data=data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Transaction updated", "data": serializer.data})
        return Response({"message": "Data not saved", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        data = request.data
        if not data.get('id'):
            return Response({"message": "ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            transaction = Transection.objects.get(id=data.get('id'))
        except Transection.DoesNotExist:
            return Response({"message": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TransectionsSerializer(transaction, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Transaction updated", "data": serializer.data})
        return Response({"message": "Data not saved", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        data = request.data
        if not data.get('id'):
            return Response({"message": "ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        if request.user.role != 'admin':
            return Response({"error": "Only admins can delete transactions"}, status=status.HTTP_403_FORBIDDEN)

        try:
            Transection.objects.get(id=data.get('id')).delete()
        except Transection.DoesNotExist:
            return Response({"message": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "Transaction deleted"}, status=status.HTTP_200_OK)
