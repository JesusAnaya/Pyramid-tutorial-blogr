# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
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
    body = Column(UnicodeText, default=u'')
    created = Column(DateTime, default=datetime.datetime.utcnow)
    edited = Column(DateTime, default=datetime.datetime.utcnow)
    deleted = Column(Boolean, default=False)

    @property
    def slug(self):
        return urlify(self.title)

    @property
    def created_in_words(self):
        return distance_of_time_in_words(self.created, datetime.datetime.utcnow())

    @property
    def description(self):
        text = strip_tags(self.body)
        if len(text) > 120:
            return '{0}...'.format(text[:120])
        return text
