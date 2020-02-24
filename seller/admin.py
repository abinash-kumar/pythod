from django.contrib import admin
from .models import Seller, SellerBankDetails, SellerVatDetails, SellerOnboardingHistory
from .models import ShippingCharge
# Register your models here.


class SellerAdmin(admin.ModelAdmin):
    model = Seller


class SellerBankDetailsAdmin(admin.ModelAdmin):
    model = SellerBankDetails


class SellerVatDetailsAdmin(admin.ModelAdmin):
    model = SellerVatDetails


class SellerOnboardingHistoryAdmin(admin.ModelAdmin):
    model = SellerOnboardingHistory


class ShippingChargeAdmin(admin.ModelAdmin):
    model = ShippingCharge


admin.site.register(Seller, SellerAdmin)
admin.site.register(SellerBankDetails, SellerBankDetailsAdmin)
admin.site.register(SellerVatDetails, SellerVatDetailsAdmin)
admin.site.register(SellerOnboardingHistory, SellerOnboardingHistoryAdmin)
admin.site.register(ShippingCharge, ShippingChargeAdmin)
