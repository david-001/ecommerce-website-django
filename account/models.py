from django.db import models
from django.contrib.auth.models import User
from payment.models import OrderItem
from payment.models import ShippingAddress
from django.contrib.auth.models import User
from store.models import Product

# Create your models here.


class Retailer(models.Model):
    # FK
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=300)
    open_time = models.CharField(max_length=300)
    close_time = models.CharField(max_length=300)
    address = models.TextField(max_length=10000)
    account_type = models.CharField(max_length=300)
    account_number = models.CharField(max_length=300)
    bank_name = models.CharField(max_length=300)

    def __str__(self):
        return self.user.username
