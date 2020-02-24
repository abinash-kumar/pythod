from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import ArrayField
import sendgrid
from django.conf import settings
from sendgrid.helpers.mail import *
import urllib  # Python URL functions
import urllib2  # Python URL functions
from codeab.celery import app

# Create your models here.


class Notification(models.Model):
    MTA = (
        ('SENDGRID', 'sendgrid'),
    )
    STA = (
        ('MSG91', 'msg91'),
    )
    PRIORITY = (
        ('high', 'High'),
        ('normal', 'Normal'),
        ('low', 'Low'),
    )
    mta = models.CharField(max_length=100, choices=MTA, default=settings.DEFAULT_MTA)
    sta = models.CharField(max_length=100, choices=STA, default=settings.DEFAULT_STA)
    nid = models.CharField(max_length=150, null=False, blank=False)  # todo unique
    about = models.TextField()
    is_email = models.BooleanField(default=False)
    is_sms = models.BooleanField(default=False)
    email_template = models.TextField(blank=True, null=True)
    sms_template = models.CharField(max_length=500, null=True, blank=True)
    auto_send = models.BooleanField(default=False)
    email_to = ArrayField(models.EmailField(), default=[], blank=True, null=True,
                          help_text="The default receivers of email. Enter email address separated by ','")
    email_bcc = ArrayField(models.EmailField(), default=[], blank=True, null=True,
                           help_text="Email bcc. Enter email address separated by ','")
    subject_content = models.TextField(blank=True, help_text='Email subject content')
    numbers = ArrayField(models.CharField(max_length=12), default=[], blank=True, null=True,
                         help_text="The default receivers of sms. Enter numbers separated by ','")
    sender_name = models.CharField(max_length=100, default=settings.DEFAULT_FROM_NAME)
    sender_email = models.CharField(max_length=100, default=settings.DEFAULT_FROM_EMAIL)

    def get_email_content(self, email_arguments):
        tmp = self.email_template
        tmp = tmp.replace('{}', '&&&')
        tmp = tmp.replace('{', '$%')
        tmp = tmp.replace('}', '%$')
        tmp = tmp.replace('&&&', '{}')
        tmp = tmp.format(*email_arguments)
        tmp = tmp.replace('$%', '{')
        tmp = tmp.replace('%$', '}')
        return tmp

    def get_sms_content(self, sms_arguments):
        return self.sms_template.format(*sms_arguments)

    def send_email(self, email_arguments):
        send_email_async.delay(self.id, {'email_to': self.email_to, 'email_args': email_arguments})

    def send_sms(self, sms_arguments):
        if self.is_sms:
            if self.sta == 'MSG91':
                authkey = settings.MSG91_KEY
                message = self.get_sms_content(sms_arguments)
                sender = "ADDBZR"  # Sender ID,While using route4 sender id should be 6 characters long.
                route = "4"  # Define route
                url = "http://api.msg91.com/api/sendhttp.php"  # API URL
                for mobile in self.numbers:
                    # mobiles = "9999999999"
                    values = {
                        'authkey': authkey,
                        'mobiles': mobile,
                        'message': message,
                        'sender': sender,
                        'route': route
                    }
                    postdata = urllib.urlencode(values)  # URL encoding the data here.
                    req = urllib2.Request(url, postdata)
                    response = urllib2.urlopen(req)
                    NotificationStatus.objects.create(notification=self, from_user=sender, subject="NA", message=message, to_user=mobile, response=response.read())

    def send_notification(self, args):
        self.send_email(args)
        self.send_sms(args)

    def __unicode__(self):
        return unicode(self.nid)


@app.task
def send_email_async(id, d):
    print 'email_sent'
    email_to = d['email_to']
    email_arguments = d['email_args']
    notification = Notification.objects.get(id=id)
    if notification.mta == 'SENDGRID':
        sg = sendgrid.SendGridAPIClient(apikey='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')
        from_email = Email(notification.sender_email)
        subject = notification.subject_content
        content = Content("text/html", notification.get_email_content(email_arguments))
        for i in email_to:
            to_email = Email(i)
            mail = Mail(from_email, subject, to_email, content)
            response = sg.client.mail.send.post(request_body=mail.get())
            response_string = "Status Code: " + str(response.status_code) + "Body : " + response.body \
                + "Header : " + str(response.headers.dict)
            NotificationStatus.objects.create(notification=notification, from_user=from_email, subject=subject, message=content, to_user=i, response=response_string)


class NotificationStatus(models.Model):
    notification = models.ForeignKey(Notification, related_name='notification_status_for')
    from_user = models.CharField(max_length=100, blank=False, null=False)
    subject = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    to_user = models.CharField(max_length=100, blank=False, null=False)
    response = models.TextField(blank=True, null=True)
