from django.db import models
from django.db import models

from django.db import models

class tbl_host(models.Model):
    STATUS_CHOICES = [
        ('personal_details_entered', 'Personal Details Entered'),
        ('property_details_entering', 'Property Details Entering'),
        ('file_uploaded', 'File Uploaded'),
        ('pending', 'Pending'),
    ]
    
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)  # Plain text password (not recommended)
    
    property_type = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    place = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.DecimalField(max_digits=11, decimal_places=7, blank=True, null=True)  
    longitude = models.DecimalField(max_digits=11, decimal_places=7, blank=True, null=True) 

    description = models.TextField(blank=True, null=True)
    amenities = models.TextField(blank=True, null=True)
    
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    id_proof = models.ImageField(upload_to='id_proofs/', blank=True, null=True)
    
    rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='personal_details_entered')

    def update_status(self):
        """
        Automatically updates the status based on the fields that are filled.
        """
        if self.name and self.email and self.phone_number and self.password:
            self.status = 'personal_details_entered'
        
        if all([self.property_type, self.address, self.latitude, self.longitude, self.description, self.amenities]):
            self.status = 'property_details_entering'
        
        if self.id_proof and self.property_images.exists():
            self.status = 'file_uploaded'
        
        if self.rate is not None:
            self.status = 'pending'
        
        self.save()

class PropertyImage(models.Model):
    host = models.ForeignKey(tbl_host, related_name='property_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_images/')
