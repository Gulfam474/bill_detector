from rest_framework import serializers
from .models import BillImage

class BillImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillImage
        fields = '__all__'
