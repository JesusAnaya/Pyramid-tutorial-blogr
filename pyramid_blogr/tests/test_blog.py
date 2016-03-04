import transaction
import datetime
from mock import patch, MagicMock
from . import TestCase, factories


class TestBlogModelMethods(TestCase):
    def test_blog_post_slug(self):
        blog_record = factories.BlogRecordFactory.create(id=1)
        self.assertEquals(blog_record.slug, 'test-post-1')

    def test_blog_post_created_in_words(self):
        datetime_patched = self.add_patch('pyramid_blogr.models.blog_record.datetime')
        datetime_patched.datetime.utcnow.return_value = datetime.datetime(2016, 2, 10)

        blog_record = factories.BlogRecordFactory.create(created=datetime.datetime(2015, 10, 10))

        self.assertEquals(blog_record.created_in_words, '4 months')
