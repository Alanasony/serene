from django.db import models

class tbl_admin(models.Model):
    email = models.EmailField()  # Ensuring email uniqueness
    password = models.CharField(max_length=100)  # Consider hashing passwords instead of storing raw

    def __str__(self):
        return self.email
