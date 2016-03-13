# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from webhelpers2.text import urlify
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
    blog_slug = request.matchdict.get('slug', '')
    entry = BlogRecordService.by_slug(blog_slug)
    if not entry:
        return HTTPNotFound()
    return {'entry': entry}


@view_config(route_name='blog_create', renderer='pyramid_blogr:templates/edit_blog.jinja2', permission='create')
def blog_create(request):
    entry = BlogRecord()
    form = BlogCreateForm(request.POST)
    if request.method == 'POST' and form.validate():
        if form.image.data:
            form.image.data = request.storage.save(request.POST[form.image.name], folder='blog')
        form.populate_obj(entry)
        DBSession.add(entry)
        return HTTPFound(location=entry.url)
    return {'form': form}


@view_config(route_name='blog_edit', renderer='pyramid_blogr:templates/edit_blog.jinja2', permission='create')
def blog_edit(request):
    print "request.matchdict: ", request.matchdict

    blog_id = int(request.matchdict.get('id', -1))
    entry = BlogRecordService.by_id(blog_id)
    if not entry:
        return HTTPNotFound()
    form = BlogUpdateForm(request.POST, entry)
    if request.method == 'POST' and form.validate():
        if form.image.data:
            form.image.data = request.storage.save(request.POST[form.image.name], folder='blog')
        else:
            form.image.data = entry.image
        form.populate_obj(entry)
        return HTTPFound(location=entry.url)
    return {'form': form}
