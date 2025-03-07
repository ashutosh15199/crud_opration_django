from django.shortcuts import render
from rest_framework.views import APIView
from .models import Transection
from rest_framework.response import Response
from .serializers import TransectionsSerializer
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
@api_view(['GET','POST'])
def get_transection(request):
     queryset =Transection.objects.all().order_by('-pk')
     serializer = TransectionsSerializer(queryset,many=True)
     return Response(
          {
               "data": serializer.data
          }
     )


class TransectionAPI(APIView):
     permission_classes = [AllowAny] 
     def get(self,request):
           queryset =Transection.objects.all().order_by('-pk')
           serializer = TransectionsSerializer(queryset,many=True)
           return Response(
               {
               "data": serializer.data
              }
           )

     def post(self,request):
          data=request.data
          print(data)
          serializer= TransectionsSerializer(data=data)
          if not serializer.is_valid():
               return Response({
                    "message":"Data not saved",
                    "errors":serializer.errors,
               })
          serializer.save()
          return Response({
               "message":"Data  saved",
               "data":serializer.data
          })
     

     def put(self,request):
          data=request.data
          serializer=TransectionsSerializer(data=data)
          if not data.get('id'):
               return Response({
                    "message":"Data is not update",
                    "error":"id is required",
               })
          transection = Transection.objects.get(id=data.get('id'))
          serializer=TransectionsSerializer(transection,data=data,partial=False)
          if not serializer.is_valid():
               return Response({
                    "message":"Data not saved",
                    "error":serializer.errors
               })
          serializer.save()
          return Response({
               "message":"Data update",
               "data":serializer.data
          })
     

     def patch(self,request):

          data=request.data
          serializer = TransectionsSerializer(data=data)
          if not data.get('id'):
           return Response({
               "message":"Data is not Updated",
               "error":"id is required"
           })
          
          transection=Transection.objects.get(id=data.get('id'))
          serializer = TransectionsSerializer(transection, data=data, partial=True)
          if not serializer.is_valid(): 
               return Response({
                    "message":"Data not saved",
                    "error":serializer.errors,
               })
          serializer.save()
          return Response({
               "message":"Data Update",
               "data":serializer.data
          })
     

     def delete(self,request):
          data = request.data
          if not data.get('id'):
               return Response({
                    "message":"Data not delete",
                    "error":"id is required"
               })
          transection=Transection.objects.get(id=data.get('id')).delete()
          return Response({
               "message":"Data Deleted",
               "data":{}
          })
