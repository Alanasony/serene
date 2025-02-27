from urllib import request
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate

from .models import tbl_register
from .serailzers import UserSerializer, LoginSerializer # type: ignore
from django.core.exceptions import ValidationError
# User Registration View
from rest_framework import generics, status,viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import traceback
from django.db.utils import IntegrityError
from rest_framework.exceptions import ValidationError
from .models import tbl_user_register
from .serailzers import UserSerializer


class RegisterUserView(viewsets.ModelViewSet):
    queryset = tbl_user_register.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            response_data = {
                "status": "success",
                "message": "Registered successfully",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                "status": "failed",
                "message": "Invalid Details",
                "errors": serializer.errors
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
# User Login View
class LoginUserView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(email=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "user": UserSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# Get User Profile (Authenticated Users Only)
class UserProfileView(generics.RetrieveAPIView):
    queryset = tbl_register.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user



from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Booking, tbl_register, tbl_host
from .serailzers import BookingSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from userapp.models import tbl_register, tbl_host, Booking  # Ensure correct models
from userapp.serailzers import BookingSerializer

from django.shortcuts import get_object_or_404

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    from django.http import JsonResponse

def create(self, request, *args, **kwargs):
    user_id = request.data.get('user')
    host_id = request.data.get('host')

    try:
        user_id = int(user_id)
        host_id = int(host_id)
    except ValueError:
        return JsonResponse({"error": "Invalid user or host ID format."}, status=400)

    try:
        user = tbl_register.objects.get(id=user_id)
    except tbl_register.DoesNotExist:
        return JsonResponse({"error": "User does not exist."}, status=404)

    try:
        host = tbl_host.objects.get(id=host_id)
    except tbl_host.DoesNotExist:
        return JsonResponse({"error": "Host does not exist."}, status=404)

    serializer = self.get_serializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=user, host=host)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework import viewsets
from .models import COD
from .serailzers import CODSerializer

class CODViewSet(viewsets.ModelViewSet):
    queryset = COD.objects.all()
    serializer_class = CODSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']  # Allow these methods


from rest_framework import viewsets
from .models import Upi
from .serailzers import UpiSerializer

class UpiViewSet(viewsets.ModelViewSet):
    queryset = Upi.objects.all()
    serializer_class = UpiSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']


from rest_framework import viewsets
from .models import Card
from .serailzers import CardSerializer

class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
