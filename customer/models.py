from __future__ import unicode_literals

import random
import string
import os
import datetime
import pytz

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from multiselectfield import MultiSelectField
from django_extensions.db.fields import UUIDField


# Create your models here.

utc = pytz.UTC


def get_user_image_path(instance, filename):
    reqpath = "user_photo/"
    filepath = settings.BASE_DIR + "/uploads/" + reqpath
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    ext = filename.split('.')[-1]
    name = str(instance.customer.first_name).lower() + "_" \
        + str(instance.id + 47)[:2] + ''.join(random.SystemRandom().choice(
            string.ascii_uppercase + string.digits) for _ in range(2))
    return reqpath + '{}.{}'.format(name, ext)


def generate_unique_share_code():
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(7))


class Customer(models.Model):
    """docstring for Customer"""
    GENDER = (
        ("MALE", "male"),
        ("FEMALE", "female")
    )
    ARTIST_TYPE = (
        ("TSHIRT DESIGNER", "tshirt_designer"),
        ("HOMEPRENEUR", "homepreneur"),
    )
    # check username(unique) is already present in emails or phone
    customer = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='ab_customer')
    is_artist = models.BooleanField(default=False)
    dob = models.DateTimeField(null=True, blank=True)
    artist_type = MultiSelectField(
        max_length=60, choices=ARTIST_TYPE, blank=True, null=True)
    mobile = models.CharField(max_length=60, blank=False, null=True)
    gender = models.CharField(
        max_length=60, choices=GENDER, blank=True, null=True)
    points = models.IntegerField(null=True, default=0)
    is_mobile_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    share_link = models.CharField(max_length=200, blank=False, null=True)
    user_photo = models.ImageField(upload_to=get_user_image_path,
                                   default='uploads/user_dummy.jpg',
                                   blank=True,
                                   null=True)

    def __unicode__(self):
        return self.customer.first_name

    def create_coupon_for_user(self):
        coupon_code = self.customer.username[:4] + str(self.id + 47)[:2] + ''.join(
            random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(2))
        obj = Coupon.objects.create(code=coupon_code, active=True, user=self,
                                    redeem_amount=100, redeem_amount_in='FLAT', redeem_amount_type='PROMOTIONAL')
        return obj


class CustomerAddress(models.Model):
    customer = models.ForeignKey(Customer, related_name='ab_customer_address')
    name = models.CharField(max_length=60, null=True)
    mobile = models.CharField(max_length=10, blank=False, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    pin_code = models.IntegerField(null=True)
    city = models.CharField(max_length=60, blank=True, null=True)
    state = models.CharField(max_length=60, blank=True, null=True)
    email = models.CharField(max_length=250, blank=True, null=True)

    def __unicode__(self):
        return self.customer.customer.first_name


class CustomerEmailVerify(models.Model):
    customer = models.ForeignKey(
        Customer, related_name='ab_customer_email_verify')
    link = UUIDField(unique=True)
    is_clicked = models.BooleanField(default=False)
    created_on = models.DateField(auto_now=False, auto_now_add=True)


class Coupon(models.Model):
    REDEEM_AMOUNT_TYPE = (
        ("FLAT", "FLAT"),
        ("PERCENTAGE", "PERCENTAGE")
    )
    REDEEM_TYPE = (
        ("PROMOTIONAL", "PROMOTIONAL"),
        ("TRANSACTIONAL", "TRANSACTIONAL")
    )
    code = models.CharField(max_length=150, unique=True)
    active = models.BooleanField(default=False)
    user = models.ForeignKey(Customer)
    redeem_amount = models.IntegerField(default=0)
    redeem_amount_in = models.CharField(
        max_length=150, choices=REDEEM_AMOUNT_TYPE)
    redeem_amount_type = models.CharField(max_length=150, choices=REDEEM_TYPE)

    def __unicode__(self):
        return self.code

    def calculate_redeem_amount(self, subtotal=0):
        amount = 0
        if self.redeem_amount_in == 'PERCENTAGE':
            amount = subtotal * self.redeem_amount / 100
        else:
            amount = self.redeem_amount
        return amount

    def create_campaign_for_user(self):
        obj = Campaign.objects.create(
            campaign_type='REFERRAL',
            coupon=self,
            amount=100,
            amount_in='FLAT',
            maximum_amount=500,
            total_applicability=5,
            each_user_applicability=1,
            active=True,
            active_days=60,
        )
        return obj

    def save(self, *args, **kwargs):
        self.code = self.code.upper()
        super(Coupon, self).save(*args, **kwargs)



class Campaign(models.Model):
    CAMPAIGN_TYPE = (
        ("ADVERTISER", "ADVERTISER"),
        ("AB", "AB"),
        ("REFERRAL", "REFERRAL"),
    )
    AMOUNT_TYPE = (
        ("FLAT", "FLAT"),
        ("PERCENTAGE", "PERCENTAGE")
    )
    campaign_type = models.CharField(max_length=150, choices=CAMPAIGN_TYPE)
    coupon = models.OneToOneField(Coupon)
    amount = models.IntegerField(default=0)
    amount_in = models.CharField(max_length=150, choices=AMOUNT_TYPE)
    maximum_amount = models.IntegerField(default=0)
    total_applicability = models.IntegerField(default=0)
    each_user_applicability = models.IntegerField(default=1)
    active = models.BooleanField(default=False)
    started_on = models.DateTimeField(auto_now_add=True)
    active_days = models.IntegerField(default=0)
    promotional_money_expiry = models.IntegerField(default=30)
    created_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.coupon.user.customer.username

    def is_campaign_expired(self):
        expire_on = self.created_on + datetime.timedelta(days=self.active_days)
        if datetime.datetime.today().replace(tzinfo=utc) <= expire_on.replace(tzinfo=utc):
            return False
        else:
            return True

    def campaign_expired_in(self):
        expire_on = self.created_on + datetime.timedelta(days=self.active_days)
        return expire_on

    def get_total_amount_used_by_users(self):
        value = 0
        total = [
            value + i.amount for i in ABMoney.objects.filter(campaign=self)]
        return total[0] if total else 0


class ABMoney(models.Model):
    MONEY_TYPE = (
        ('PROMOTIONAL', 'PROMOTIONAL'),
        ('CASH', 'CASH'),
        ('TRANSACTIONAL', 'TRANSACTIONAL'),
    )
    customer = models.ForeignKey(Customer)
    amount = models.IntegerField(null=False)
    amount_type = models.CharField(
        max_length=60, choices=MONEY_TYPE, blank=False, null=False)
    expiry = models.DateTimeField(null=True, blank=True)
    particular = models.CharField(max_length=100, null=False, blank=False)
    campaign = models.ForeignKey(Campaign, null=True)
    _closing_promotional_money = models.IntegerField(null=False, default=0)
    _closing_cash_money = models.IntegerField(null=False, default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super(ABMoney, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.customer.customer.username

    @property
    def closing_promotional_money(self):
        ab_money_objs = ABMoney.objects.filter(
            customer=self.customer).order_by('created_on')
        value = 0
        for m in ab_money_objs:
            if m.amount_type == 'PROMOTIONAL':
                if m.campaign and not m.campaign.is_campaign_expired():
                    m._closing_promotional_money = value + m.amount
                elif m.amount < 0:
                    m._closing_promotional_money = value + m.amount
                else:
                    m._closing_promotional_money = value
                value = m._closing_promotional_money
                m.save()
        return value

    @property
    def closing_cash_money(self):
        ab_money_objs = ABMoney.objects.filter(
            customer=self.customer).order_by('created_on')
        value = 0
        for m in ab_money_objs:
            if m.amount_type == 'CASH':
                m._closing_cash_money = value + m.amount
                value = m._closing_cash_money
                m.save()
        return value
