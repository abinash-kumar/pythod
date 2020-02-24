from __future__ import unicode_literals

from django.db import models
from seller.models import ShippingCharge, Seller
from django.contrib.auth.models import User
from product.models import Product, ProductVarientList
from django_extensions.db.fields import UUIDField
from django.contrib.postgres.fields import HStoreField
from decimal import Decimal

# Create your models here.


class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        ('DRAFT', 'DRAFT'),
        ('PENDING', 'PENDING'),
        ('PAYMENT_DONE', 'PAYMENT_DONE'),
        ('COD', 'COD'),
        ('CONFIRMED', 'CONFIRMED'),
        ('SHIP_REQUEST', 'SHIP_REQUEST'),
        ('SHIPPED', 'SHIPPED'),
        ('DELIVERED', 'DELIVERED'),
        ('RETURNED', 'RETURNED'),
        ('CANCELLED', 'CANCELLED'),
    )
    user = models.ForeignKey(User, blank=True, null=True)  # todo
    order_placed_time = models.DateTimeField(blank=True, null=True, auto_now=True)
    product_id = models.ForeignKey(Product, null=True, blank=True)
    # product_name = models.CharField(max_length=250, blank=True)
    quantity = models.IntegerField(null=False, blank=False)

    price = models.IntegerField(null=False, blank=False)
    discount = models.IntegerField(null=False, blank=False)
    coupon_discount = models.IntegerField(null=False, blank=False, default=0)
    shipping_charge = models.IntegerField(null=False, blank=False, default=0)

    phone = models.CharField(max_length=250, blank=True)
    email = models.CharField(max_length=250, blank=True)
    shipping_firstname = models.CharField(max_length=250, blank=True)
    shipping_lastname = models.CharField(max_length=250, blank=True)
    shipping_address1 = models.CharField(max_length=250, blank=True)
    shipping_address2 = models.CharField(max_length=250, blank=True)
    shipping_city = models.CharField(max_length=250, blank=True)
    shipping_state = models.CharField(max_length=250, blank=True)
    shipping_country = models.CharField(max_length=250, blank=True)
    shipping_zipcode = models.CharField(max_length=250, blank=True)

    order_status = models.CharField(
        name="order_status",
        max_length=50,
        choices=ORDER_STATUS_CHOICES)
    track_code = models.CharField(max_length=250, blank=True)
    comment = models.CharField(max_length=1000, blank=True)
    order_other_detail = models.CharField(max_length=300, blank=True)
    process_by_seller = models.ForeignKey(Seller, blank=True, null=True)
    product_varient = models.ForeignKey(ProductVarientList)

    def calculate_shipping_charge(self):
        shipping_charge_obj = ShippingCharge.objects.get(seller=self.product_varient.sellers.all()[0])
        sum_amount = self.price * self.quantity - self.discount
        if sum_amount > shipping_charge_obj.free_shipping_minimum_amount:
            return 0
        else:
            return shipping_charge_obj.shipping_charge

    def save(self, *args, **kwargs):
        self.shipping_charge = self.calculate_shipping_charge()
        super(Order, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.product_id.name


class Transaction(models.Model):
    PAYMENT_MODE_CHOICES = (
        ('ONLINE', 'ONLINE'),
        ('COD', 'COD'),
        ('PAYTM', 'PAYTM'),
    )
    PAYMENT_STATUS_CHOICES = (
        ('DRAFT', 'DRAFT'),
        ('PENDING', 'PENDING'),
        ('DROP', 'DROP'),
        ('FAILED', 'FAILED'),
        ('TAMPERED', 'TAMPERED'),
        ('CANCELLED', 'CANCELLED'),
        ('COMPLETED', 'COMPLETED'),
    )
    order = models.ManyToManyField(Order, blank=False, null=False)
    payment_token = models.CharField(max_length=250, blank=True)
    payment_id = UUIDField(unique=True)
    payment_on = models.DateTimeField(blank=True, null=True)
    payment_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    payment_from_abmoney = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    payment_mode = models.CharField(max_length=50, blank=False, choices=PAYMENT_MODE_CHOICES)
    payment_status = models.CharField(max_length=250, blank=True, choices=PAYMENT_STATUS_CHOICES)
    coupon_applied = models.CharField(max_length=250, blank=True, null=True)
    discount = models.IntegerField(null=False, blank=False, default=0)
    taxes = models.IntegerField(null=False, blank=False, default=0)
    shipping_charge = models.IntegerField(null=False, blank=False, default=0)
    payment_request = models.TextField(default=None, null=True)
    payment_response = models.TextField(default=None, null=True)

    def save(self, *args, **kwargs):
        self.payment_amount = float(Decimal(self.payment_amount).quantize(Decimal("0.00")))
        super(Transaction, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.payment_id
