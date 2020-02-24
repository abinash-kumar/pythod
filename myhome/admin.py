from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.
from models import CategoryImage
from models import OtherBanners, Selfibaaz, SliderImages, DesignerImage
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.utils.html import escape
from django.core.urlresolvers import reverse, NoReverseMatch


action_names = {
    ADDITION: 'Addition',
    CHANGE: 'Change',
    DELETION: 'Deletion',
}


class FilterBase(admin.SimpleListFilter):
    def queryset(self, request, queryset):
        if self.value():
            dictionary = dict(((self.parameter_name, self.value()),))
            return queryset.filter(**dictionary)


class ActionFilter(FilterBase):
    title = 'action'
    parameter_name = 'action_flag'

    def lookups(self, request, model_admin):
        return action_names.items()


class UserFilter(FilterBase):
    """Use this filter to only show current users, who appear in the log."""
    title = 'user'
    parameter_name = 'user_id'

    def lookups(self, request, model_admin):
        return tuple((u.id, u.username)
            for u in User.objects.filter(pk__in =
                LogEntry.objects.values_list('user_id').distinct())
        )

class AdminFilter(UserFilter):
    """Use this filter to only show current Superusers."""
    title = 'admin'
    def lookups(self, request, model_admin):
        return tuple((u.id, u.username) for u in User.objects.filter(is_superuser=True))

class StaffFilter(UserFilter):
    """Use this filter to only show current Staff members."""
    title = 'staff'
    def lookups(self, request, model_admin):
        return tuple((u.id, u.username) for u in User.objects.filter(is_staff=True))


class LogEntryAdmin(admin.ModelAdmin):

    date_hierarchy = 'action_time'

    list_filter = [
        UserFilter,
        ActionFilter,
        'content_type',
        # 'user',
    ]

    search_fields = [
        'object_repr',
        'change_message'
    ]


    list_display = [
        'action_time',
        'user',
        'content_type',
        'object_link',
        'action_flag',
        'action_description',
        'change_message',
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser and request.method != 'POST'

    def has_delete_permission(self, request, obj=None):
        return False

    def object_link(self, obj):
        ct = obj.content_type
        repr_ = escape(obj.object_repr)
        try:
            href = reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id])
            link = u'<a href="%s">%s</a>' % (href, repr_)
        except NoReverseMatch:
            link = repr_
        return link if obj.action_flag != DELETION else repr_
    object_link.allow_tags = True
    object_link.admin_order_field = 'object_repr'
    object_link.short_description = u'object'

    def queryset(self, request):
        return super(LogEntryAdmin, self).queryset(request) \
            .prefetch_related('content_type')

    def action_description(self, obj):
        return action_names[obj.action_flag]
    action_description.short_description = 'Action'

UserAdmin.list_display += ('date_joined',)

class SelfibaazAdmin(admin.ModelAdmin):
    list_display = ["user", "selfi", "active"]


class SliderAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "image", "active",  "display_priority"]


class BannerAdmin(admin.ModelAdmin):
    list_display = ["name", "image", "active"]


class CategoryImageAdmin(admin.ModelAdmin):
    list_display = ["category", "image_on_page", "image_on_menu"]

class DesignerAdmin(admin.ModelAdmin):
    list_display = ["designer", "image_on_page"]

# class CustomerAddressAdmin(admin.ModelAdmin):
#     list_display = ["designer", "image_on_page"]

admin.site.register(Selfibaaz, SelfibaazAdmin)
admin.site.register(SliderImages, SliderAdmin)
admin.site.register(OtherBanners, BannerAdmin)
admin.site.register(CategoryImage, CategoryImageAdmin)
admin.site.register(DesignerImage, DesignerAdmin)
admin.site.register(LogEntry, LogEntryAdmin)
