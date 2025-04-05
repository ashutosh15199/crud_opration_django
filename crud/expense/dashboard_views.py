from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .permissions import IsAdminUser, IsManagerUser

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
