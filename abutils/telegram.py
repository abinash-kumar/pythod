import json
import requests
from codeab.celery import app
from django.conf import settings

TOKEN = "452618824:AAHf0swoohKW6dTye9R2TtAjk-X0wAgcQBE"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates():
    url = URL + "getUpdates"
    js = get_json_from_url(url)
    return js


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


@app.task
def send_message_in_async(text, chat_id=-259951852):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def send_message(msg):
    if not settings.DEBUG:
        send_message_in_async.delay(msg)
    else:
        print msg

def send_exception(msg):
    if not settings.DEBUG:
        send_message_in_async.delay(msg,-295104643)
    else:
        print msg