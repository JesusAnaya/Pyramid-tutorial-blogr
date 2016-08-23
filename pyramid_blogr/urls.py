# -*- coding: utf-8 -*-
from __future__ import unicode_literals


# Paths configuratiion
def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('test', '/test')
    config.add_route('auth', '/sign/{action}')
    config.add_route('login', '/login')
    config.include('pyramid_blogr.views.blog')
