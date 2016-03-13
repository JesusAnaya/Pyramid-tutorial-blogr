# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from sqlalchemy.event import listen
from pyramid_blogr.models.meta import Base

from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    UnicodeText,
    DateTime,
    Boolean,
)
from webhelpers2.text import urlify
from webhelpers2.date import distance_of_time_in_words
from webhelpers2.html.tools import strip_tags


class BlogRecord(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(255), unique=True, nullable=False)
    slug = Column(Unicode(255), unique=True, nullable=False)
    body = Column(UnicodeText, default='')
    image = Column(Unicode(255), default='')
    created = Column(DateTime, default=datetime.datetime.utcnow)
    edited = Column(DateTime, default=datetime.datetime.utcnow)
    deleted = Column(Boolean, default=False)

    @property
    def url(self):
        return '/blog/{0}'.format(self.slug or urlify(self.title))

    @property
    def image_url(self):
        if self.image:
            return '/static/media/{0}'.format(self.image)
        else:
            return None

    @property
    def created_in_words(self):
        return distance_of_time_in_words(self.created, datetime.datetime.utcnow())

    @property
    def description(self):
        text = strip_tags(self.body)
        if len(text) > 120:
            return '{0}...'.format(text[:120])
        return text


def generate_blog_post_slug(mapper, connect, target):
    if not target.slug:
        target.slug = urlify(target.title)


listen(BlogRecord, 'before_insert', generate_blog_post_slug)
listen(BlogRecord, 'before_update', generate_blog_post_slug)
