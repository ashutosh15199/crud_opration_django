from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Transection
from .serializers import TransectionsSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_transection(request):
    queryset = Transection.objects.all().order_by('-pk')
    serializer = TransectionsSerializer(queryset, many=True)
    return Response({"data": serializer.data})

class TransectionAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Transection.objects.all().order_by('-pk')
        serializer = TransectionsSerializer(queryset, many=True)
        return Response({"data": serializer.data})

    def post(self, request):
        if request.user.role != 'admin':
            return Response({"error": "Only admins can create transactions"}, status=403)
        data = request.data.copy()
        data["user"] = request.user.id
        serializer = TransectionsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Transaction created", "data": serializer.data}, status=201)
        return Response({"errors": serializer.errors}, status=400)

    def put(self, request):
        data = request.data
        transaction = get_object_or_404(Transection, id=data.get('id'))
        if request.user.role != 'admin' and transaction.user != request.user:
            return Response({"error": "Unauthorized"}, status=403)
        serializer = TransectionsSerializer(transaction, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Updated", "data": serializer.data})
        return Response({"errors": serializer.errors}, status=400)

    def patch(self, request):
        data = request.data
        transaction = get_object_or_404(Transection, id=data.get('id'))
        serializer = TransectionsSerializer(transaction, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Partially updated", "data": serializer.data})
        return Response({"errors": serializer.errors}, status=400)

    def delete(self, request):
        transaction = get_object_or_404(Transection, id=request.data.get('id'))
        if request.user.role != 'admin':
            return Response({"error": "Only admins can delete transactions"}, status=403)
        transaction.delete()
        return Response({"message": "Deleted"}, status=200)
