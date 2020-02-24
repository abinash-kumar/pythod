from django.db import models
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

# Create your models here.


def get_file_path(instance, filename):
    return "files/seller/" + str(instance.id) + "/" + filename


class Seller(models.Model):
    GENDER = (
        ("MALE", "male"),
        ("FEMALE", "female")
    )
    seller = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateTimeField(null=True, blank=True)
    display_name = models.CharField(max_length=100, blank=False, null=False)
    mobile = models.CharField(max_length=60, blank=False, null=False)
    gender = models.CharField(max_length=60, choices=GENDER, blank=True, null=True)
    shop_address = models.CharField(max_length=200, blank=True, null=True)
    shop_pin_code = models.IntegerField(null=True, blank=True)
    shop_city = models.CharField(max_length=60, blank=True, null=True)
    shop_state = models.CharField(max_length=60, blank=True, null=True)
    shop_country = models.CharField(max_length=60, default='India')
    pickup_address = models.CharField(max_length=200, blank=True, null=True)
    pickup_pin_code = models.IntegerField(null=True, blank=True)
    pickup_city = models.CharField(max_length=60, blank=True, null=True)
    pickup_state = models.CharField(max_length=60, blank=True, null=True)
    pickup_country = models.CharField(max_length=60, default='India')
    average_dispatch_time = models.IntegerField(null=True, blank=True)
    is_mobile_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    def __unicode__(self):
        return self.seller.first_name

    def get_detailed_json(self):
        json = model_to_dict(self)
        json.update({"seller_name":  self.seller.first_name + " " + self.seller.last_name})
        return json


class SellerBankDetails(models.Model):
    seller = models.ForeignKey(Seller, null=False, blank=False)
    account_holder_name = models.CharField(max_length=60, blank=False, null=False)
    bank_name = models.CharField(max_length=100, blank=False, null=False)
    branch_name = models.CharField(max_length=100, blank=False, null=False)
    pan = models.CharField(max_length=15, blank=False, null=False)
    ifsc_code = models.CharField(max_length=15, blank=False, null=False)
    account_no = models.CharField(max_length=30, blank=False, null=False)
    bank_branch_address = models.CharField(max_length=200, blank=False, null=False)
    cheque = models.FileField(upload_to=get_file_path, blank=True)


class SellerVatDetails(models.Model):
    seller = models.ForeignKey(Seller, null=False, blank=False)
    has_tin = models.BooleanField(default=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    cin_no = models.CharField(max_length=50, blank=True, null=True)
    gst_no = models.CharField(max_length=15, blank=True, null=True)
    sign = models.FileField(upload_to=get_file_path, blank=True)
    cin_memo = models.FileField(upload_to=get_file_path, blank=True)
    gst_certificate = models.FileField(upload_to=get_file_path, blank=True)


class SellerOnboardingHistory(models.Model):
    STATUS = (
        ("REGISTERED", "Registered"),
        ("PENDING_APPROVAL", "pending_approval"),
        ("APPROVED", "approved")
    )
    seller = models.ForeignKey(Seller, null=False, blank=False)
    timespam = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS, default=STATUS)
    active_status = models.BooleanField(default=False)
    # by_user = models.ForeignKey(User, null=False, blank=False, default=User.objects.get(id=1))



class ShippingCharge(models.Model):
    seller = models.ForeignKey(Seller)
    shipping_charge = models.IntegerField(null=False, blank=False)
    free_shipping_minimum_amount = models.IntegerField(null=False, blank=False)
