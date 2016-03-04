import transaction
from . import TestCase


class TestBlogViewSuccessCondition(TestCase):
    def test_passing_view(self):
        self.assertEquals(1 + 1, 2)
