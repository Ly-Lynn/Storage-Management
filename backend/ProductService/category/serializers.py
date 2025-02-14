from rest_framework import serializers
from .models import (
    Category
)
class CategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'description', 'created_at', 'updated_at'
        ]
    