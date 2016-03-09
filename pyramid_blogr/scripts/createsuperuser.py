# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sqlalchemy import engine_from_config
from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from pyramid_blogr.models import User
from pyramid_blogr.models.meta import DBSession, Base
import os
import sys
import transaction


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> <username> <password>\n'
          '(example: "%s development.ini username password")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    try:
        user, passwd = argv[2:4]
        with transaction.manager:
            admin = User(name=user)
            admin.set_password(passwd)
            DBSession.add(admin)

        print("User {0} created".format(user))
    except:
        usage(argv)
