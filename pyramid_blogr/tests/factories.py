# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import factory
import datetime
from pyramid_blogr.models import BlogRecord
from pyramid_blogr.models.meta import DBSession


class BlogRecordFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = BlogRecord
        sqlalchemy_session = DBSession

    id = factory.Sequence(lambda n: n)
    title = factory.Sequence(lambda n: 'Test Post %d' % n)
    body = 'Test Body'
    created = datetime.datetime.utcnow()
    edited = datetime.datetime.utcnow()
