# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class TweenStartRequestAttributes(object):
    def __init__(self, handler, registry):
        self.handler = handler
        self.registry = registry

    def __call__(self, request):
        public_domain = self.registry.settings.get('public_domain')
        google_analytics_id = self.registry.settings.get('google_analytics_id')

        if public_domain:
            setattr(request, 'public_domain', public_domain)

        if google_analytics_id:
            setattr(request, 'google_analytics_id', google_analytics_id)

        return self.handler(request)
