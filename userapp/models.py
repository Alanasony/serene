from django.db import models

from host.models import tbl_host
    
class tbl_user_register(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True, max_length=191)  # Reduce to 191
    password = models.CharField(max_length=255)  
    address = models.TextField(blank=True, null=True) 
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username
    
from django.db import models
from django.contrib.auth import get_user_model  
from datetime import date

tbl_user_register = get_user_model()  

class Booking(models.Model):
    PAYMENT_OPTIONS = [
        ('cash_on_arrival', 'Cash on Arrival'),
        ('upi', 'UPI'),
        ('card', 'Card'),
    ]

    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('full_refund', 'Full Refund'),
        ('partial_refund', 'Partial Refund'),
    ]

    BOOKING_STATUS = [
        ('booking_initiated', 'Booking Initiated'),
        ('booking_completed', 'Booking Completed'),
        ('check_in', 'Checked In'),
        ('check_out', 'Checked Out'),
        ('canceled', 'Canceled'),
    ]

    user = models.ForeignKey(tbl_user_register, on_delete=models.CASCADE, related_name='bookings')    
    host = models.ForeignKey(tbl_host, on_delete=models.CASCADE, related_name='bookings')  

    start_date = models.DateField()  
    end_date = models.DateField()  
    no_of_guests = models.PositiveIntegerField()  
    
    total_cost = models.DecimalField(max_digits=10, decimal_places=2) 
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_option = models.CharField(max_length=20, choices=PAYMENT_OPTIONS, default='cash_on_arrival')  
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')  
    booking_status = models.CharField(max_length=20, choices=BOOKING_STATUS, default='booking_initiated')  
    booking_date = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"Booking {self.id} - {self.user} ({self.start_date} to {self.end_date})"

from django.db import models

class COD(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="cod")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Booking {self.booking} - {self.status}"


class Upi(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="upi")
    status = models.CharField(max_length=20, default="success")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    upi_id = models.CharField(max_length=100)

    def __str__(self):
        return f"UPI Payment for Booking {self.booking.id} - {self.status}"



class Card(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="card")
    status = models.CharField(max_length=20, default="pending")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    card_holder_name = models.CharField(max_length=100)
    card_number = models.CharField(max_length=16)
    expiry_date = models.CharField(max_length=7)  
    cvv = models.CharField(max_length=4)

    def __str__(self):
        return f"Card Payment for Booking {self.booking.id} - {self.status}"



class BookingReport(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='reports')
    user = models.ForeignKey(tbl_user_register, on_delete=models.CASCADE)  # Assuming user authentication
    star_rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 rating
    feedback = models.TextField(blank=True, null=True)  # Optional feedback
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for Booking {self.booking.id} - {self.star_rating} stars"

class BookingReportImage(models.Model):
    report = models.ForeignKey(BookingReport, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='report_images/')  # Store images in media folder

    def __str__(self):
        return f"Image for Report {self.report.id}"
