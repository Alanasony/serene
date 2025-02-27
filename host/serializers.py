from rest_framework import serializers
from .models import tbl_host
from rest_framework import serializers
from .models import tbl_host, PropertyImage

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id', 'image']

class HostSerializer(serializers.ModelSerializer):
    property_images = PropertyImageSerializer(many=True, required=False)

    class Meta:
        model = tbl_host
        fields = '__all__'

    def create(self, validated_data):
        """
        Override create method to handle multiple images.
        """
        images_data = self.context['request'].FILES.getlist('property_images')
        host = tbl_host.objects.create(**validated_data)
        
        for image_data in images_data:
            PropertyImage.objects.create(host=host, image=image_data)

        return host

    def update(self, instance, validated_data):
        """
        Override update method to allow adding multiple images.
        """
        images_data = self.context['request'].FILES.getlist('property_images')

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if images_data:
            for image_data in images_data:
                PropertyImage.objects.create(host=instance, image=image_data)

        instance.update_status()
        return instance


class LoginSerializer(serializers.Serializer):  # Use Serializer instead of ModelSerializer
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
