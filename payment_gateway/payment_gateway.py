from abc import ABCMeta, abstractmethod


class PaymentGateway(object):
    """Parent PaymentGateway class.

    Attributes:

    """

    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def slug(self):
        """"Return a slug representing of the name of PaymentGateway"""
        pass
