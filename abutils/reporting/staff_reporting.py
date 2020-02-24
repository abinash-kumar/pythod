import datetime
from codeab.celery import app
from artist.models import ArtistDetail
from customer.models import Customer
from orders.models import Order
from abutils.telegram import send_message as telegram

today = datetime.datetime.now()
yesterday = today - datetime.timedelta(days=1)
last_month = (today.replace(day=1) - datetime.timedelta(days=1)).replace(day=1)


def get_user_count_last_day():
    return Customer.objects.filter(customer__date_joined__date=yesterday).count()


def get_user_count_last_month():
    return Customer.objects.filter(customer__date_joined__gte=last_month).count()


def get_total_user_count():
    return Customer.objects.all().count()


def get_artist_count_last_day():
    return ArtistDetail.objects.filter(customer__customer__date_joined__date=yesterday).count()


def get_artist_count_last_month():
    return ArtistDetail.objects.filter(customer__customer__date_joined__gte=last_month).count()


def get_total_artist_count():
    return ArtistDetail.objects.all().count()


def get_total_processed_order_last_day():
    return Order.objects.filter(order_placed_time__date=yesterday, order_status__in=['PAYMENT_DONE', 'DELIVERED']).count()


def get_total_processed_order_last_month():
    return Order.objects.filter(order_placed_time__gte=last_month, order_status__in=['PAYMENT_DONE', 'DELIVERED']).count()


def get_total_processed_orders():
    return Order.objects.filter(order_status__in=['PAYMENT_DONE', 'DELIVERED']).count()


@app.task
def generate_daily_notification():
    msg = """
        ***  LAST DAY STATUS ***
            User SignUp - """ + str(get_user_count_last_day()) + """
            Artist SignUp - """ + str(get_artist_count_last_day()) + """
            Order Processed - """ + str(get_total_processed_order_last_day()) + """
    """
    telegram(msg)


@app.task
def generate_monthly_notification():
    msg = """
        ***  LAST MONTH STATUS ***
            User SignUp - """ + str(get_user_count_last_month()) + """
            Artist SignUp - """ + str(get_artist_count_last_month()) + """
            Order Processed - """ + str(get_total_processed_order_last_month()) + """
    """
    telegram(msg)
