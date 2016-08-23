# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from webhelpers2.text import urlify
from deform import Form, ValidationFailure
from pyramid_blogr.models.services.blog_record import BlogRecordService
from pyramid_blogr.security import BlogRecordFactory
from pyramid_blogr.forms import BlogCreateForm, BlogUpdateForm
from pyramid_blogr.schemas import BlogCreateSchema


def includeme(config):
    config.add_route('blog.list', '/blog')
    config.add_route('blog.create', '/blog/create', factory=BlogRecordFactory)
    config.add_route('blog.edit', '/blog/{id:\d+}/edit', factory=BlogRecordFactory)
    config.add_route('blog.retrive', '/blog/{slug}')


class BlogView(object):
    def __init__(self, request):
        self.request = request

    @property
    def form(self):
        schema = BlogCreateSchema()
        return Form(schema, buttons=('submit',))

    @view_config(route_name='blog.list', renderer='templates/blog/list.jinja2')
    def list(self):
        page = int(self.request.params.get('page', 1))
        paginator = BlogRecordService.get_paginator(self.request, page)
        return {'paginator': paginator}

    @view_config(route_name='blog.retrive', renderer='templates/blog/retrive.jinja2')
    def retrive(self):
        blog_slug = self.request.matchdict.get('slug', '')
        entry = BlogRecordService.by_slug(blog_slug)
        if not entry:
            return HTTPNotFound()
        return {'entry': entry}

    @view_config(route_name='blog.create', request_method='GET', permission='create', renderer='templates/blog/form.jinja2')
    def create_form(self):
        return {'form': self.form.render()}

    @view_config(route_name='blog.create', request_method='POST', permission='create', renderer='templates/blog/form.jinja2')
    def create(self):
        try:
            entry_data = self.form.validate(self.request.POST.items())
            entry = BlogRecordService.create(entry_data)
            return HTTPFound(location=entry.url)
        except ValidationFailure as e:
            return {'form': e.render()}

    @view_config(route_name='blog.edit', renderer='templates/blog/form.jinja2', permission='create')
    def edit(self):
        blog_id = int(self.request.matchdict.get('id', -1))
        entry = BlogRecordService.by_id(blog_id)
        if not entry:
            return HTTPNotFound()

        form = Form(BlogCreateSchema(), buttons=('submit',))

        form = BlogUpdateForm(self.request.POST, entry)
        if self.request.method == 'POST' and form.validate():
            if form.image.data:
                form.image.data = self.request.storage.save(self.request.POST[form.image.name], folder='blog')
            else:
                form.image.data = entry.image
            form.populate_obj(entry)
            return HTTPFound(location=entry.url)
        return {'form': form}
