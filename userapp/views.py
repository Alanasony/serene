from urllib import request
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate

from .models import *
from .serailzers import UserSerializer, LoginSerializer # type: ignore
from django.core.exceptions import ValidationError
# User Registration View
from rest_framework import generics, status,viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import traceback
from django.db.utils import IntegrityError
from rest_framework.exceptions import ValidationError
from .models import *
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
    queryset = tbl_user_register.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user



from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Booking, tbl_user_register, tbl_host
from .serailzers import BookingSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from userapp.models import tbl_user_register, tbl_host, Booking  # Ensure correct models
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
        user = tbl_user_register.objects.get(id=user_id)
    except tbl_user_register.DoesNotExist:
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


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Booking
from .serailzers import BookingSerializer

class BookingPaymentUpdateView(APIView):
    def patch(self, request, *args, **kwargs):
        """
        Updates payment status of a booking based on payment option.
        """
        booking_id = request.data.get('booking_id')
        payment_option = request.data.get('payment_option')

        # Validate required fields
        if not booking_id or not payment_option:
            return Response({"error": "booking_id and payment_option are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found."}, status=status.HTTP_404_NOT_FOUND)

        # Mapping payment options to booking status
        payment_status_mapping = {
            "COA": "pending",
            "upi": "success",
            "card": "success",
        }

        # Get the corresponding status
        new_status = payment_status_mapping.get(payment_option.lower())

        if new_status:
            booking.payment_status = new_status  # Update payment status
            if new_status == "success":
                booking.status = "booking completed"  # Update booking status if payment is successful
            booking.save()
            return Response({"message": "Payment updated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid payment option."}, status=status.HTTP_400_BAD_REQUEST)


from django.http import JsonResponse
import json
from .models import Booking


def check_in_guest(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON request
            booking_id = data.get('booking_id')

            if not booking_id:
                return JsonResponse({"error": "Missing booking_id"}, status=400)

            # Fetch booking record
            try:
                booking = Booking.objects.get(id=booking_id)
            except Booking.DoesNotExist:
                return JsonResponse({"error": "Booking not found"}, status=404)

            # If payment is 'cash on arrival', update the payment status to 'success'
            if booking.payment_option == 'cash_on_arrival':
                booking.payment_status = 'success'

            # Allow check-in only if payment status is 'success'
            if booking.payment_status == 'success':
                booking.booking_status = 'check_in'
                booking.save()
                return JsonResponse({"message": f"Booking {booking_id} checked in successfully!"})
            else:
                return JsonResponse({"error": "Payment not received, cannot check-in."}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Booking

@csrf_exempt
def check_out_guest(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON request
            booking_id = data.get('booking_id')

            if not booking_id:
                return JsonResponse({"error": "Missing booking_id"}, status=400)

            # Fetch the booking record
            try:
                booking = Booking.objects.get(id=booking_id)
            except Booking.DoesNotExist:
                return JsonResponse({"error": "Booking not found"}, status=404)

            # Allow check-out only if the current status is 'check_in'
            if booking.booking_status == 'check_in':
                booking.booking_status = 'check_out'
                booking.save()
                return JsonResponse({"message": f"Booking {booking_id} checked out successfully!"})
            else:
                return JsonResponse({"error": "Guest is not checked in, cannot check out."}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)




from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Booking

@csrf_exempt
def update_booking(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            booking_id = data.get("booking_id")
            new_start_date = data.get("new_start_date")  # New check-in date
            new_end_date = data.get("new_end_date")  # New check-out date
            new_total_cost = data.get("new_total_cost")  # New cost

            if not booking_id or not new_start_date or not new_end_date or not new_total_cost:
                return JsonResponse({"error": "Missing required fields"}, status=400)

            # Fetch the booking record
            try:
                booking = Booking.objects.get(id=booking_id)
            except Booking.DoesNotExist:
                return JsonResponse({"error": "Booking not found"}, status=404)

            # Ensure new booking date is before current check-in date
            if new_start_date >= str(booking.start_date):
                return JsonResponse({"error": "New booking date must be before the current check-in date"}, status=400)

            # Compare the new cost with the current cost
            if float(new_total_cost) > float(booking.total_cost):
                booking.total_cost = new_total_cost  # Update cost
                message = f"Total cost updated to {new_total_cost}"
            elif float(new_total_cost) < float(booking.total_cost):
                refund_amount = float(booking.total_cost) - float(new_total_cost)
                booking.refund_amount = refund_amount  # Partial refund
                message = f"Partial refund of {refund_amount} applied"

            # Update booking dates
            booking.start_date = new_start_date
            booking.end_date = new_end_date
            booking.save()

            return JsonResponse({"message": message})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import date
from .models import Booking

@csrf_exempt
def cancel_booking(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            booking_id = data.get("booking_id")

            if not booking_id:
                return JsonResponse({"error": "Missing booking_id"}, status=400)

            # Fetch the booking record
            try:
                booking = Booking.objects.get(id=booking_id)
            except Booking.DoesNotExist:
                return JsonResponse({"error": "Booking not found"}, status=404)

            # Ensure the cancellation is before the check-in date
            if date.today() >= booking.start_date:
                return JsonResponse({"error": "Booking cannot be canceled after the check-in date"}, status=400)

            # Apply refund and cancel booking
            booking.refund_amount = booking.total_cost  # Full refund
            booking.total_cost = 0  # Set total cost to zero
            booking.booking_status = 'canceled'  # Mark as canceled
            booking.save()

            return JsonResponse({"message": f"Booking {booking_id} canceled successfully! Refund: {booking.refund_amount}"})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
import json
from .models import Booking, BookingReport, BookingReportImage

@csrf_exempt
def submit_report(request):
    if request.method == "POST":
        try:
            data = request.POST
            files = request.FILES.getlist('images')

            booking_id = data.get("booking_id")
            user_id = data.get("user_id")
            star_rating = int(data.get("star_rating", 0))
            feedback = data.get("feedback", "")

            # Validate input
            if not (1 <= star_rating <= 5):
                return JsonResponse({"error": "Star rating must be between 1 and 5"}, status=400)

            # Get booking
            try:
                booking = Booking.objects.get(id=booking_id)
            except Booking.DoesNotExist:
                return JsonResponse({"error": "Booking not found"}, status=404)

            # Create report
            report = BookingReport.objects.create(
                booking=booking,
                user_id=user_id,
                star_rating=star_rating,
                feedback=feedback
            )

            # Save images (if any)
            for img in files:
                BookingReportImage.objects.create(report=report, image=img)

            return JsonResponse({"message": "Report submitted successfully!"})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)
