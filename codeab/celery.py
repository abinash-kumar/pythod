from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.signals import setup_logging
from django.conf import settings
from billiard import einfo
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'codeab.settings')

app = Celery('codeab')

app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.update(CELERY_TIMEZONE='Asia/Calcutta')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


class _Frame(einfo._Frame):
    f_back = None

    def __init__(self, frame):
        super(_Frame, self).__init__(frame)
        # self.f_locals = frame.f_locals


def patch_celery_traceback():
    einfo.Traceback.Frame = _Frame


@setup_logging.connect
def configure_logging(sender=None, **kwargs):
    from django.utils.log import configure_logging
    configure_logging(settings.LOGGING_CONFIG, settings.LOGGING)
    patch_celery_traceback()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    from abutils.reporting.staff_reporting import generate_daily_notification, generate_monthly_notification
    sender.add_periodic_task(crontab(minute=45, hour=9), generate_daily_notification.s())
    sender.add_periodic_task(crontab(minute=45, hour=9, day_of_month='1'), generate_monthly_notification.s())

