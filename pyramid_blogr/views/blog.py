# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from ..models.meta import DBSession
from ..models.blog_record import BlogRecord
from ..models.services.blog_record import BlogRecordService
from ..forms import BlogCreateForm, BlogUpdateForm


@view_config(route_name='blog_post_list', renderer='pyramid_blogr:templates/blog_post_list.jinja2')
def blog_post_list_view(request):
    page = int(request.params.get('page', 1))
    paginator = BlogRecordService.get_paginator(request, page)
    return {'paginator': paginator}


@view_config(route_name='blog', renderer='pyramid_blogr:templates/view_blog.jinja2')
def blog_view(request):
    blog_id = int(request.matchdict.get('id', -1))
    entry = BlogRecordService.by_id(blog_id)
    if not entry:
        return HTTPNotFound()
    return {'entry': entry}


@view_config(route_name='blog_action', match_param='action=create', renderer='pyramid_blogr:templates/edit_blog.jinja2', permission='create')
def blog_create(request):
    entry = BlogRecord()
    form = BlogCreateForm(request.POST)
    if request.method == 'POST' and form.validate():
        form.populate_obj(entry)
        DBSession.add(entry)
        return HTTPFound(location=request.route_url('blog_post_list'))
    return {'form': form, 'action': request.matchdict.get('action')}


@view_config(route_name='blog_action', match_param='action=edit', renderer='pyramid_blogr:templates/edit_blog.jinja2', permission='create')
def blog_update(request):
    blog_id = int(request.params.get('id', -1))
    entry = BlogRecordService.by_id(blog_id)
    if not entry:
        return HTTPNotFound()
    form = BlogUpdateForm(request.POST, entry)
    if request.method == 'POST' and form.validate():
        form.populate_obj(entry)
        return HTTPFound(location=request.route_url('blog', id=entry.id, slug=entry.slug))
    return {'form': form, 'action': request.matchdict.get('action')}
