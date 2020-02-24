from codeab.celery import app
from django_redis import get_redis_connection
from django.conf import settings


@app.task
def update_data_in_vyom(data):
    redis = get_redis_connection(settings.REDIS_CLIENT)
    redis.publish('USER_TRAKING', data)
