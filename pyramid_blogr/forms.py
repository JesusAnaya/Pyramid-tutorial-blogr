# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from wtforms import Form, StringField, TextAreaField, validators, FileField
from wtforms import HiddenField, PasswordField
from .utils import VALID_IMAGE_ETX

def strip_filter(x):
    return x.strip() if x else None


class BlogCreateForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=255)], filters=[strip_filter])
    body = TextAreaField('Contents', [validators.Length(min=1)], filters=[strip_filter])
    image = FileField('Image File')

    def validate_image(form, field):
        if field.data:
            ext = field.data.filename.split('.')[-1]
            if not ext or ext.lower() not in VALID_IMAGE_ETX:
                raise validators.ValidationError('The file is not a valid image')


class BlogUpdateForm(BlogCreateForm):
    id = HiddenField()


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=1, max=255)], filters=[strip_filter])
    password = PasswordField('Password', [validators.Length(min=3)])
