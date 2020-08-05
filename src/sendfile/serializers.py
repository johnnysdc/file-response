from rest_framework import serializers
from .models import UploadFileAnalisador
from datetime import datetime
from rest_framework import serializers

class UploadSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UploadFileAnalisador
        fields = ('id',
                  'analisador_name',
                  'scaler_data',
                  'modelo'
                  )

    def update(self, instance, validated_data):
        instance.analisador_name = validated_data.get('analisador_name', instance.analisador_name)
        instance.scaler_data = validated_data.get(
            'scaler_data', instance.scaler_data)
        instance.modelo = validated_data.get(
            'modelo', instance.modelo)
        
        instance.save()

        return instance