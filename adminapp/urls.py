from django.urls import path
from . import views


urlpatterns = [
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('admin_pending/', views.admin_pending, name='admin_pending'),
    path('admin_approve/', views.admin_approve, name='admin_approve'),
    path('admin_reject/', views.admin_reject, name='admin_reject'),
]
