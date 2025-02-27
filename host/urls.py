from django.urls import path,include
from .views import HostCreateView, HostRetrieveUpdateDestroyView, LoginView,HostUpdateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'hosts', HostCreateView, basename='hosts')


urlpatterns = [
    path('', include(router.urls)),
    path('hosts/<int:pk>/', HostRetrieveUpdateDestroyView.as_view(), name='host-detail'),
    path('login/', LoginView.as_view(), name='login'),
    path('hosts/<int:pk>/', HostUpdateView.as_view(), name='host-update'),  # PUT
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
