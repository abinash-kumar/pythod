import hashlib
from payment_gateway import models
from payment_gateway.payment_gateway import PaymentGateway
from django.conf import settings
from payment_gateway.helpers import payu as payu_data
from django.utils.translation import ugettext_lazy as _


class Payu(PaymentGateway):
    SLUG = _('payu')
    REQUEST = _('request')
    RESPONSE = _('response')
    CONFIG_DICT = settings.PAYMENT_GATEWAYS
    REQUEST_URL = payu_data.get_request_url(production=settings.PRODUCTION)
    REQUIRED_REQUEST_KEYS = payu_data.required_request_keys()
    REQUIRED_RESPONSE_KEYS = payu_data.required_response_keys()
    REQUIRED_CONFIG_KEYS = payu_data.required_config_keys()
    REQUEST_KEYS = payu_data.request_keys()
    RESPONSE_KEYS = payu_data.response_keys()
    HASH_KEYS = payu_data.keys_required_for_hash()

    def __init__(self, data, config):
        self.data = data
        self.config = config

    @classmethod
    def slug(cls):
        """"Return a slug representing of the name."""
        return cls.SLUG.__unicode__()

    @classmethod
    def payment_gateway(cls):
        if '_gateway' not in cls.__dict__:
            cls._gateway = models.PaymentGateway.objects.get(slug=cls.SLUG.__unicode__())
        return cls.__dict__['_gateway']

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

    @staticmethod
    def get_checksum(message, digestmod=hashlib.sha512):
        return digestmod(message).hexdigest()

    def validate_checksum(self):
        hash_param_list = [self.data.get(key, "") for key in self.HASH_KEYS]
        hash_param_list.reverse()
        hash_param_str = "{}|{}||||||{}".format(
            self.config['SALT'],
            self.data.get('status', ""),
            '|'.join(hash_param_list)
        )
        hash_val = self.get_checksum(hash_param_str)
        return self.data.get('hash') == hash_val

    @classmethod
    def get_config(cls, insurer_slug):
        return cls.CONFIG_DICT[cls.slug()][insurer_slug]

    def get_request_data(self):
        payment = models.Payment.objects.create(
            payment_gateway=self.payment_gateway(),
            transaction=self.data.get('transaction'),
            reference_id=self.data.get('reference_id')
        )
        data = {
            'key': self.config.get('MERCHANT_ID'),
            'txnid': payment.payment_id,
            'amount': self.data.get('amount'),
            'productinfo': self.data.get('productinfo'),
            'firstname': self.data.get('firstname'),
            'email': self.data.get('email'),
            'phone': self.data.get('phone'),
            'surl': self.data.get('surl'),
            'furl': self.data.get('furl')
        }
        hash_param_list = [data.get(key, "") for key in self.HASH_KEYS]
        hash_param_str = "{}||||||{}".format('|'.join(hash_param_list), self.config['SALT'])
        data['hash'] = hashlib.sha512(hash_param_str).hexdigest()
        return data, self.REQUEST_URL
