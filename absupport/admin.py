from django.contrib import admin
from .models import DeliveryOrders, SellerPickupAddress, PageCacheForSEO

# Register your models here.
admin.site.register(PageCacheForSEO)
admin.site.register(DeliveryOrders)
admin.site.register(SellerPickupAddress)