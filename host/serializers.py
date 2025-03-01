from rest_framework import serializers
from .models import tbl_host
from rest_framework import serializers
from .models import tbl_host, PropertyImage
from .models import PropertyImage

from rest_framework import serializers
from .models import tbl_host, PropertyImage

from rest_framework import serializers
from .models import tbl_host, PropertyImage

class PropertyImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = PropertyImage
        fields = ['id', 'image']

    def get_image(self, obj):
        """Returns a relative media path instead of an absolute URL."""
        if obj.image:
            return f"media/{obj.image.name}"
        return None

class HostSerializer(serializers.ModelSerializer):
    property_images = serializers.SerializerMethodField()

    class Meta:
        model = tbl_host
        fields = '__all__'

    def get_property_images(self, obj):
        """Returns a list of relative media paths for property images."""
        images = obj.property_images.all()
        return [f"media/{image.image.name}" for image in images if image.image]

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
        Override update method to handle multiple images.
        """
        images_data = self.context['request'].FILES.getlist('property_images')

        # Update host instance fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # If there are new images, add them
        if images_data:
            PropertyImage.objects.filter(host=instance).delete()  # Delete old images
            for image_data in images_data:
                PropertyImage.objects.create(host=instance, image=image_data)

        return instance


class LoginSerializer(serializers.Serializer):  # Use Serializer instead of ModelSerializer
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
