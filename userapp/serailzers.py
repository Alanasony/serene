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


from rest_framework import serializers
from .models import Booking

class PaymentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['payment_option', 'status']  # Only allow updating these fields

    def update(self, instance, validated_data):
        """
        Override update method to change payment status based on payment option.
        """
        payment_option = validated_data.get('payment_option', instance.payment_option)

        # Update status based on payment option
        if payment_option in ['upi', 'card']:
            validated_data['status'] = 'booking_completed'
        elif payment_option == 'COA':  # Cash on Arrival
            validated_data['status'] = 'pending'

        return super().update(instance, validated_data)
