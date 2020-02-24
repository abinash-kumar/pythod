from django.contrib import admin
from .models import Notification, NotificationStatus
# Register your models here.



class NotificationAdmin(admin.ModelAdmin):
    model = Notification

class NotificationStatusAdmin(admin.ModelAdmin):
    model = NotificationStatus
    list_display = ["notification", "to_user", ]

admin.site.register(Notification, NotificationAdmin)
admin.site.register(NotificationStatus,NotificationStatusAdmin)
