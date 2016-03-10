# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from sqlalchemy import engine_from_config

from .models.meta import (
    DBSession,
    Base,
)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    # Starting DB Engine
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    # Auth system
    authentication_policy = AuthTktAuthenticationPolicy('somesecret', hashalg='sha512')
    authorization_policy = ACLAuthorizationPolicy()
    config = Configurator(settings=settings, authentication_policy=authentication_policy, authorization_policy=authorization_policy)

    # Apps includes
    config.include('pyramid_jinja2')
    config.include('pyramid_tm')
    config.include('pyramid_storage')
    config.include('pyramid_blogr.urls')

    config.scan()
    return config.make_wsgi_app()
