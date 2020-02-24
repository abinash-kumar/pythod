from django.contrib import admin

# Register your models here.
from .models import UserImage, UserPhysique, UserFbDetails, UserFbLikes, Tag, ProductTagMap, TagBanner

class UserImageView(admin.ModelAdmin):
    list_display = ["uploader", "upload_date", "image_for", "likes_top", "likes_bottom", "likes_whole", "riplicable"]


admin.site.register(UserImage, UserImageView)
admin.site.register(UserPhysique)
admin.site.register(UserFbDetails)
admin.site.register(UserFbLikes)
admin.site.register(Tag)
admin.site.register(ProductTagMap)
admin.site.register(TagBanner)