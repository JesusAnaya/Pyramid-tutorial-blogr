# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from ..models.services.user import UserService
from ..models.services.blog_record import BlogRecordService
from ..schemas import TestSchema
import colander


@view_config(route_name='home', attr='index', renderer='pyramid_blogr:templates/index.jinja2')
@view_config(route_name='login', attr='login', renderer='pyramid_blogr:templates/login.jinja2')
@view_config(route_name='auth', attr='sign_in_out', match_param='action=in', renderer='string', request_method='POST')
@view_config(route_name='auth', attr='sign_in_out', match_param='action=out', renderer='string')
@view_config(route_name='test', attr='test', renderer='json', request_method='POST')
class DefaultViews(object):
    def __init__(self, request):
        self.request = request

    def index(self):
        entries = BlogRecordService.first_posts()
        return {'entries': entries}

    def test(self):
        errors = None
        values = None
        try:
            values = TestSchema().deserialize(self.request.POST)
        except colander.Invalid, e:
            errors = e.asdict()
            print errors

        return {'values': values, 'errors': errors}

    def login(self):
        return {}

    def sign_in_out(self):
        username = self.request.POST.get('username')
        redirect_to = 'home'

        if username:
            user = UserService.by_name(username)
            if user and user.verify_password(self.request.POST.get('password')):
                headers = remember(self.request, user.name)
            else:
                headers = forget(self.request)
                redirect_to = 'login'
        else:
            headers = forget(self.request)
            redirect_to = 'login'

        return HTTPFound(location=self.request.route_url(redirect_to), headers=headers)
