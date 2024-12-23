from rest_framework import serializers
from .models import PointCloudFile

class PointCloudFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointCloudFile
        fields = '__all__'