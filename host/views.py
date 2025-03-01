from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import tbl_host
from .serializers import HostSerializer, LoginSerializer
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from .models import tbl_host
from .serializers import HostSerializer

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics,viewsets
from .models import tbl_host
from .serializers import HostSerializer



class HostCreateView(viewsets.ModelViewSet):
    queryset = tbl_host.objects.all()
    serializer_class = HostSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            response_data = {
                "status": "success",
                "message": " Registered successfully",
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


class HostUpdateView(generics.UpdateAPIView):
    queryset = tbl_host.objects.all()
    serializer_class = HostSerializer
    


# Host Retrieve, Update & Delete View
class HostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = tbl_host.objects.all()
    serializer_class = HostSerializer

# Login API
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")

            try:
                user = tbl_host.objects.get(email=email)
                if user.phone_number == password:  # Basic password check
                    return Response({"message": "Login successful!", "id": user.id, "status": user.status}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
            except tbl_host.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
