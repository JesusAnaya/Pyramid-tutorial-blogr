import pytest
import unittest
import transaction
from pyramid import testing


@pytest.mark.usefixtures("dbtransaction")
class TestCase(unittest.TestCase):
    def setup_method(self, method):
        self.config = testing.setUp()

    def teardown_method(self, method):
        transaction.abort()
        testing.tearDown()
