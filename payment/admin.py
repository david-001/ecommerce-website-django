from django.contrib import admin
from . models import ShippingAddress, Order, OrderItem, Status

# Register your models here.
admin.site.register(ShippingAddress)
admin.site.register(Status)
admin.site.register(Order)
admin.site.register(OrderItem)
