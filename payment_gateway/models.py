from django.apps import apps
from django.db import models
from django_extensions.db.fields import UUIDField
from jsonfield import JSONField
from django.utils.translation import ugettext_lazy as _


class PaymentGateway(models.Model):
    """The PaymentGateway class"""

    slug = models.SlugField(_('slug'), max_length=70)
    title = models.CharField(_('title'), max_length=200)
    body = models.TextField(_('body'), blank=True)
    is_active = models.BooleanField(default=False)
    created_on = models.DateTimeField(_('created'), auto_now_add=True)
    updated_on = models.DateTimeField(_('modified'), auto_now=True)

    def __unicode__(self):
        return u'%s' % self.title


class Payment(models.Model):
    """Payment class"""

    PENDING = _('PENDING')
    FAILED = _('FAILED')
    SUCCESS = _('SUCCESS')

    status_choices = (
        (PENDING, _('Pending')),
        (FAILED, _('Failed')),
        (SUCCESS, _('Success'))
    )

    payment_gateway = models.ForeignKey(PaymentGateway)
    _transaction_id = models.BigIntegerField(db_index=True)
    _transaction_app_label = models.CharField(max_length=250)
    _transaction_model_name = models.CharField(max_length=250)
    status = models.CharField(_('status'), max_length=20, default=PENDING, choices=status_choices)
    raw = JSONField(_('raw'), blank=True, default={})
    reference_id = models.CharField(max_length=250, blank=True)
    payment_id = UUIDField(unique=True)

    @property
    def transaction(self):
        Transaction = apps.get_model(self._transaction_app_label, self._transaction_model_name)
        return Transaction.objects.get(pk=self._transaction_id)

    @transaction.setter
    def transaction(self, txn):
        self._transaction_id = txn.id
        self._transaction_app_label = txn._meta.app_label
        self._transaction_model_name = txn._meta.model_name


class Request(models.Model):
    """Request class"""

    BROWSER = _('BROWSER')
    S2SQUERY = _('S2SQUERY')

    type_choices = (
        (BROWSER, _('Broswer')),
        (S2SQUERY, _('S2SQuery'))
    )
    payment = models.ForeignKey(Payment)
    data = JSONField(_('data'), blank=True, default={})
    type = models.CharField(_('request type'), max_length=20, default=BROWSER, choices=type_choices)


class Response(models.Model):
    """Response class"""

    BROWSER = _('BROWSER')
    S2S = _('S2S')
    S2SQUERY = _('S2SQUERY')

    type_choices = (
        (BROWSER, _('Broswer')),
        (S2S, _('S2S')),
        (S2SQUERY, _('S2SQuery'))
    )

    payment = models.ForeignKey(Payment)
    data = JSONField(_('data'), blank=True, default={})
    type = models.CharField(_('response type'), max_length=20, default=BROWSER, choices=type_choices)
