from django.contrib import admin
from .models import Customer, CustomerAddress, Coupon, Campaign, ABMoney, CustomerEmailVerify
# Register your models here.


class CustomerAdmin(admin.ModelAdmin):
    search_fields = ('mobile', )
    model = Customer
    list_display = [
        'customer',
        'is_mobile_verified',
        'dob',
        'gender',
        'mobile',
        'points',
        'is_email_verified',
    ]


class CustomerAddressAdmin(admin.ModelAdmin):
    model = CustomerAddress


class CouponAdmin(admin.ModelAdmin):
    model = Coupon


class CampaignAdmin(admin.ModelAdmin):
    model = Campaign


class ABMoneyAdmin(admin.ModelAdmin):
    model = ABMoney


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(Campaign, CampaignAdmin)
admin.site.register(ABMoney, ABMoneyAdmin)
admin.site.register(CustomerAddress, CustomerAddressAdmin)
admin.site.register(CustomerEmailVerify)
