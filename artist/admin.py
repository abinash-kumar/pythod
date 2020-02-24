from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import ArtistBankDetail, ArtistDesign, ArtistDetail, SocialLink, ProductArtistDesignMap, ArtistCoupon
from product.models import ProductImage
# Register your models here.


class ArtistDetailAdmin(admin.ModelAdmin):
    model = ArtistDetail
    list_display = [
        'customer',
        'artist_type',
        'email',
        'mobile',
    ]

    def email(self, obj):
        return '%s' % (obj.customer.customer.email)

    def mobile(self, obj):
        return '%s' % (obj.customer.mobile)


class ArtistDesignAdmin(admin.ModelAdmin):
    list_display = ["title", "comment", "tags", "status", "design_image"]
    search_fields = ('tags', 'title', 'comment')

    def design_image(self, obj):
        if obj.design:
            return mark_safe('<img src="%s" height="200" />' % (obj.get_thumbname_url()))
        else:
            return 'No Design'


class ProductArtistDesignMapAdmin(admin.ModelAdmin):
    list_display = [
        'product',
        'product_type',
        'product_image',
    ]

    list_editable = ['product_type']

    def product_type(self, obj):
        return '%s' % (obj.product_type)

    def product_image(self, obj):
        product_image_obj = ProductImage.objects.filter(product=obj.product)
        if product_image_obj:
            return mark_safe('<img src="%s" />' % (product_image_obj[0].image_img()))
        else:
            return '(Sin imagen)'
        product_image.short_description = 'Thumb'


admin.site.register(ArtistDetail, ArtistDetailAdmin)
admin.site.register(ArtistCoupon)
admin.site.register(ArtistBankDetail)
admin.site.register(SocialLink)
admin.site.register(ArtistDesign, ArtistDesignAdmin)
admin.site.register(ProductArtistDesignMap, ProductArtistDesignMapAdmin)
