# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from ..models.services.user import UserService
from ..models.services.blog_record import BlogRecordService
from ..forms import RegistrationForm
from ..models.meta import DBSession
from ..models.user import User


@view_config(route_name='home', renderer='pyramid_blogr:templates/index.jinja2')
def index_page(request):
    entries = BlogRecordService.first_posts()
    return {'entries': entries}


@view_config(route_name='login', renderer='pyramid_blogr:templates/login.jinja2')
def login_page(request):
    return {}


@view_config(route_name='auth', match_param='action=in', renderer='string', request_method='POST')
@view_config(route_name='auth', match_param='action=out', renderer='string')
def sign_in_out(request):
    username = request.POST.get('username')
    redirect_to = 'home'

    if username:
        user = UserService.by_name(username)
        if user and user.verify_password(request.POST.get('password')):
            headers = remember(request, user.name)
        else:
            headers = forget(request)
            redirect_to = 'login'
    else:
        headers = forget(request)
        redirect_to = 'login'

    return HTTPFound(location=request.route_url(redirect_to), headers=headers)
