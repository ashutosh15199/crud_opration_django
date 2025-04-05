from rest_framework import serializers
from .models import Transection

from rest_framework import serializers
from django.contrib.auth import get_user_model

CustomUser   = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser  
        fields = ('id', 'username', 'email', 'password', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', 'user')  # Default role
        )
        return user


class TransectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Transection
        fields = [
            "id",
            "title",
            "amount",
            "transection_type",
        ]