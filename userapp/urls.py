from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from .views import BookingPaymentUpdateView, CODViewSet, UpiViewSet,CardViewSet, check_in_guest, submit_report

# Import views
from .views import BookingViewSet, RegisterUserView, LoginUserView, UserProfileView
from . import views  # Import views.py

# Router Configuration
router = DefaultRouter()
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'register', RegisterUserView, basename='register')
router.register(r'cod', CODViewSet, basename='cod')
router.register(r'upi', UpiViewSet, basename='upi')
router.register(r'card', CardViewSet, basename='card')

# URL Patterns
urlpatterns = [
    # Schema Endpoints
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # API Endpoints
    path('login/', LoginUserView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    # path('update-payment/', PaymentUpdateView.as_view(), name='update-payment'),
    path('booking/payment/', BookingPaymentUpdateView.as_view(), name='booking-payment-update'),
    path('check-in/', views.check_in_guest, name='check-in'),
    path('check-out/', views.check_out_guest, name='check-out'),
    path('update-booking/', views.update_booking, name='update-booking'),
    path('cancel-booking/', views.cancel_booking, name='cancel-booking'),
    path('submit-report/', views.submit_report, name='submit-report'),

    # Include other router-based views
    path('', include(router.urls)),
    path('userapp/', include(router.urls)),

]
