
from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    card_number = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    added_by = models.CharField(max_length=150)
    
    def __str__(self):
        return self.name