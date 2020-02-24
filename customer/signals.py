from .models import Customer
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from abutils.utils import get_shorten_url
from abutils.telegram import send_message as telegram


@receiver(post_save, sender=User)
def create_customer_profile(sender, **kwargs):
    if kwargs.get('created', False):
        customer_obj = Customer.objects.get_or_create(customer=kwargs.get('instance'))[0]
        coupon_obj = customer_obj.create_coupon_for_user()
        coupon_obj.create_campaign_for_user()
        customer_obj.share_link = get_shorten_url("https://www.addictionbazaar.com/register?code=" + coupon_obj.code)['id']
        customer_obj.save()
        telegram("New user signed up")
