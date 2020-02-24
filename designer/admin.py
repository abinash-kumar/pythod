from django.contrib import admin
from .models import Designer, DesignerSocialLinks, DesignerSliderImages, DesignercollageImages, DesignerContactDetails
# Register your models here.


class DesignerAdmin(admin.ModelAdmin):
    model = Designer


class DesignerSocialLinkAdmin(admin.ModelAdmin):
    model = DesignerSocialLinks


class DesignerImageAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "image", "active", "display_priority"]


class DesignercollageImagesAdmin(admin.ModelAdmin):
    model = DesignercollageImages

class DesignerContactDetailsAdmin(admin.ModelAdmin):
    list_display = ["name", "status", "contact_channel", "mobile", "email"]
    
admin.site.register(Designer, DesignerAdmin)
admin.site.register(DesignerSocialLinks, DesignerSocialLinkAdmin)
admin.site.register(DesignerSliderImages, DesignerImageAdmin)
admin.site.register(DesignercollageImages, DesignercollageImagesAdmin)
admin.site.register(DesignerContactDetails, DesignerContactDetailsAdmin)
