from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = tbl_user_register
        fields = '__all__'

    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'  # Includes all model fields


from rest_framework import serializers
from .models import COD

class CODSerializer(serializers.ModelSerializer):
    class Meta:
        model = COD
        fields = '__all__'  # Or specify required fields explicitly

from rest_framework import serializers
from .models import Upi

class UpiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upi
        fields = '__all__'  # You can specify required fields explicitly if needed

from rest_framework import serializers
from .models import Card

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'  # You can explicitly list required fields if needed
