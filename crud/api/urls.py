from expense import views
from django.urls import path

urlpatterns = [
    path('get_transections/',views.get_transection),
    path('transection/',views.TransectionAPI.as_view())
    
]