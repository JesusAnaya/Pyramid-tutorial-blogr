import pytest
import os
import sqlalchemy
from pyramid.paster import get_appsettings, setup_logging
from ..models.meta import DBSession, Base


@pytest.fixture(scope='session')
def sqlengine(request):
    engine = sqlalchemy.create_engine('sqlite://')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

    def teardown():
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return engine


@pytest.fixture()
def dbtransaction(request, sqlengine):
    connection = sqlengine.connect()
    transaction = connection.begin()
    DBSession.configure(bind=connection)

    def teardown():
        transaction.rollback()
        connection.close()
        DBSession.remove()

    request.addfinalizer(teardown)

    return connection
