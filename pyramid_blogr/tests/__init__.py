import pytest
import unittest
import transaction
import mock
from pyramid import testing


@pytest.mark.usefixtures("dbtransaction")
class TestCase(unittest.TestCase):
    def setup_method(self, method):
        self.config = testing.setUp()
        self.patches = []

    def add_patch(self, patch, name=''):
        patcher = mock.patch(patch, name=name)
        self.patches.append(patcher)
        return patcher.start()

    def teardown_method(self, method):
        transaction.abort()
        testing.tearDown()

        for patch in self.patches:
            patch.stop()
