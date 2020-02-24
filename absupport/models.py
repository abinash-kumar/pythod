from __future__ import unicode_literals

from django.db import models

from customer.models import Customer, CustomerAddress
from orders.models import Order
from seller.models import Seller


# Create your models here.
class SellerPickupAddress(models.Model):
    seller = models.OneToOneField(Seller, on_delete=models.CASCADE)
    psi = models.CharField(max_length=100, blank=True)#balnk False
    status = models.CharField(max_length=50, blank=False)
    request_data = models.TextField(blank=False)
    response_json = models.CharField(max_length=500, blank=True)
    delivery_partner = models.CharField(max_length=500, blank=True)
    def __unicode__(self):
        return unicode(self.psi)


class DeliveryOrders(models.Model):
    seller = models.ForeignKey(SellerPickupAddress)
    order = models.ForeignKey(Order)
    success = models.BooleanField(default=True)
    date = models.DateField(auto_now=False, auto_now_add=True)
    aipex_number = models.CharField(max_length=100, blank=True)
    api_id = models.CharField(max_length=100, blank=True)
    ship_label = models.TextField(blank=True)
    cod_label = models.TextField(blank=True)
    way_bill_no = models.TextField(blank=True)
    request_json = models.TextField(blank=False)
    response_json = models.TextField(blank=False)

    def __unicode__(self):
        return unicode(str(self.seller) + "-" + str(self.order))


class Pincode(models.Model):
    pincode = models.CharField(max_length=7, unique=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)

    def __unicode__(self):
        return unicode(self.pincode)


class DeliveryPartnerDetails(models.Model):
    pincode = models.ForeignKey(Pincode)
    provider = models.CharField(max_length=100, blank=True)
    delivery_available = models.BooleanField(default=True)
    pickup_available = models.BooleanField(default=True)
    cod_available = models.BooleanField(default=True)
    prepaid_available = models.BooleanField(default=True)
    cod_charge = models.IntegerField(null=True, blank=True)
    surface_charge = models.IntegerField(null=True, blank=True)
    air_charge = models.IntegerField(null=True, blank=True)
    cargo_available = models.BooleanField(default=True)
    cargo_charge = models.IntegerField(null=True, blank=True)



class PageCacheForSEO(models.Model):
    path = models.CharField(max_length=275)
    file_name = models.CharField(max_length=275)
    file_name_mobile = models.CharField(max_length=275, default="home.html", null=True, blank=True)
    created_date = models.DateField(auto_now=False, auto_now_add=True)
    updated_date = models.DateField(auto_now=True, auto_now_add=False)
