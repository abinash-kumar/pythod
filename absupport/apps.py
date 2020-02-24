from __future__ import unicode_literals

from django.apps import AppConfig


class AbsupportConfig(AppConfig):
    name = 'absupport'

    def ready(self):
        import absupport.signals

