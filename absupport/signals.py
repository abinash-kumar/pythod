from .models import Customer
from absupport.models import PageCacheForSEO
from django.db.models.signals import post_save
from django.dispatch import receiver
from abutils.utils import get_shorten_url
from abutils.telegram import send_message as telegram
from abutils import utils

@receiver(post_save, sender=PageCacheForSEO)
def create_prerender_page(sender, **kwargs):
    page_instance = kwargs.get('instance')
    utils.prerender_page_create.delay(page_instance.path, page_instance.file_name, page_instance.file_name_mobile)
    telegram("Changes in page {} recorded, updating the site".format(page_instance.path))
