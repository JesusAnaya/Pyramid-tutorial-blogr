# -*- coding: utf-8 -*-
from __future__ import unicode_literals


# Paths configuratiion
def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('blog_post_list', '/blog')
    config.add_route('blog_create', '/blog/create', factory='pyramid_blogr.security.BlogRecordFactory')
    config.add_route('blog_edit', '/blog/{id:\d+}/edit', factory='pyramid_blogr.security.BlogRecordFactory')
    config.add_route('blog', '/blog/{slug}')
    config.add_route('auth', '/sign/{action}')
    config.add_route('login', '/login')
