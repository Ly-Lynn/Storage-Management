from .models import (
    ProductBrand
)
from rest_framework import serializers
import re

def validate_link_web(value):
    pattern = r'^(https?:\/\/)?([\w\-]+(\.[\w\-]+)+)(\/[\w\-]*)*\/?$'
    if not re.match(pattern, value):
        raise serializers.ValidationError("Invalid website URL format")
    return value

class BrandSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    link_web = serializers.CharField(validators=[validate_link_web])
    image = serializers.ImageField()
    class Meta:
        model = ProductBrand
        fields = [
            'id', 'name', 'description', 'image', 'link_web', 'created_at', 'updated_at'
        ]
    