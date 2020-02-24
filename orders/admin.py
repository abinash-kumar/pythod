from django.contrib import admin
from .models import Order, Transaction
# Register your models here.


class OrderInline(admin.TabularInline):
    model = Transaction.order.through


class OrderAdmin(admin.ModelAdmin):
    list_display = ['product_id', 'order_placed_time']
    model = Order


class TransactionAdmin(admin.ModelAdmin):
    readonly_fields = ('order', )
    list_display = ['payment_id', 'payment_amount', 'payment_status', 'payment_mode']
    model = Transaction

    inlines = [
        OrderInline,
    ]


admin.site.register(Order, OrderAdmin)
admin.site.register(Transaction, TransactionAdmin)
