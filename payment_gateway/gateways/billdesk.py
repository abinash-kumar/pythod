import hashlib
import hmac
from payment_gateway import models
from payment_gateway.payment_gateway import PaymentGateway
from django.conf import settings
from django.core.urlresolvers import reverse
from payment_gateway.helpers import billdesk as bd_data
from django.utils.translation import ugettext_lazy as _


class Billdesk(PaymentGateway):
    """Billdesk class, child of PaymentGateway class

    Attributes:
    data: request / response data
    config: Insurer config for billdesk
    """

    SLUG = _('billdesk')
    REQUEST = _('request')
    RESPONSE = _('response')
    CONFIG_DICT = settings.PAYMENT_GATEWAYS
    REQUEST_URL = bd_data.get_request_url(production=settings.PRODUCTION)
    REQUIRED_REQUEST_KEYS = bd_data.required_request_keys()
    REQUIRED_RESPONSE_KEYS = bd_data.required_response_keys()
    REQUIRED_CONFIG_KEYS = bd_data.required_config_keys()
    REQUEST_KEYS = bd_data.request_keys()
    RESPONSE_KEYS = bd_data.response_keys()
    RESPONSE_DATA_KEYS = bd_data.response_data_keys()

    def __init__(self, data, config):
        self.data = data
        self.config = config

    @classmethod
    def payment_gateway(cls):
        if '_gateway' not in cls.__dict__:
            cls._gateway = models.PaymentGateway.objects.get(slug=cls.SLUG.__unicode__())
        return cls.__dict__['_gateway']

    @classmethod
    def parse_response(cls, data):
        return dict(zip(cls.RESPONSE_KEYS, data[cls.REQUIRED_RESPONSE_KEYS[0]].split('|')))

    @staticmethod
    def keys_validator(data, keys):
        return set(keys).issubset(data) and data

    @classmethod
    def type_validator(cls, data):
        if cls.keys_validator(data, cls.REQUIRED_REQUEST_KEYS):
            return cls.REQUEST, data
        elif cls.keys_validator(data, cls.REQUIRED_RESPONSE_KEYS):
            return cls.RESPONSE, data
        else:
            return False

    @classmethod
    def get_config(cls, insurer_slug):
        return cls.CONFIG_DICT[cls.slug()][insurer_slug]

    @property
    def data_type(self):
        return self._data_type.__unicode__()

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config):
        self._config = self.keys_validator(config, self.REQUIRED_CONFIG_KEYS)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data_type, self._data = self.type_validator(data)

    @staticmethod
    def get_checksum(message, key, digestmod=hashlib.sha256):
        return hmac.new(key, msg=message, digestmod=digestmod).hexdigest().upper()

    @classmethod
    def slug(cls):
        """"Return a slug representing of the name."""
        return cls.SLUG.__unicode__()

    @classmethod
    def return_url(cls):
        return u'%s%s' % (
            settings.SITE_URL.strip('/'),
            reverse('pg-response', kwargs={'gateway': cls.slug()})
        )

    def validate_checksum(self):
        response_data = self.data[self.REQUIRED_RESPONSE_KEYS[0]].split('|')
        response_checksum = response_data[-1]
        response_data = response_data[:-1]
        data_checksum = self.get_checksum(
            '|'.join(response_data),
            self.config['CHECKSUM_KEY']
        )
        return response_checksum == data_checksum

    def get_response_data(self):
        response = self.parse_response(self.data)
        return {value: response[key] for key, value in self.RESPONSE_DATA_KEYS.items()}

    def get_request_data(self):
        payment = models.Payment.objects.create(
            payment_gateway=self.payment_gateway(),
            transaction=self.data.get('transaction'),
            reference_id=self.data.get('reference_id')
        )
        data = {
            'MerchantID': self.config.get('MERCHANT_ID'),
            'CustomerID': payment.payment_id,
            'TxnAmount': self.data.get('amount'),
            'CurrencyType': 'INR',
            'TypeField1': 'R',
            'SecurityID': self.config.get('SECURITY_ID'),
            'TypeField2': 'F',
            'AdditionalInfo1': self.data.get('reference_id'),
            'AdditionalInfo2': self.data.get('phone'),
            'AdditionalInfo3': self.data.get('email'),
            'RU': self.return_url(),
        }
        request = [unicode(data[key]) if key in data else 'NA' for key in self.REQUEST_KEYS[:-1]]
        request.append(
            self.get_checksum(
                '|'.join(request),
                self.config.get('CHECKSUM_KEY')
            )
        )
        payment.request_set.create(
            data={'request_data': {'msg': '|'.join(request)}, 'url': self.REQUEST_URL}
        )
        return {'msg': '|'.join(request)}, self.REQUEST_URL
