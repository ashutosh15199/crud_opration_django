from rest_framework import serializers
from .models import Transection

class TransectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Transection
        fields = [
            "id",
            "title",
            "amount",
            "transection_type",
        ]