from bookmark_app.models import Bookmark, Tag
from .test_base import ConstantMixin
from rest_framework.test import APITestCase


class TestBookmark(APITestCase, ConstantMixin):

    ######################
    # ---- GET ---- #
    ######################
    def test_get_without_auth(self):
        bookmark_resp = self.client.get(self.BOOKMARK_URL)
        self.assertEqual(bookmark_resp.status_code, 403)

    def test_get_with_auth(self):
        self.register_user()
        self.login_user()
        bookmark_resp = self.client.get(self.BOOKMARK_URL)
        self.assertEqual(bookmark_resp.status_code, 200)
        self.assertEqual(bookmark_resp.json(), [])

    ######################
    # ---- POST ---- #
    ######################
    def test_post_without_auth(self):
        self.register_user()
        bookmark_resp = self.create_bookmark(
            url='https://www.google.com',
            title='Google Search',
            verify=False
        )
        self.assertEqual(bookmark_resp.status_code, 403)
        self.assertEqual(Bookmark.objects.all().count(), 0)

    def test_post_with_incorrect_site(self):
        # Having incorrect site doesn't raise error, instead it will be set correctly
        self.register_user()
        self.login_user()
        bookmark_resp = self.create_bookmark(
            url='https://www.google.com',
            title='Google Search',
            site='bing',
            verify=False
        )
        self.assertEqual(bookmark_resp.status_code, 201)
        self.assertEqual(Bookmark.objects.all().count(), 1)
        self.assertEqual(Bookmark.objects.all().first().site, 'google')

    def test_post_without_site(self):
        # If site is not provided, it will be set correctly
        self.register_user()
        self.login_user()
        bookmark_resp = self.create_bookmark(
            url='https://www.google.com',
            title='Google Search',
            verify=False
        )
        self.assertEqual(bookmark_resp.status_code, 201)
        self.assertEqual(Bookmark.objects.all().count(), 1)
        self.assertEqual(Bookmark.objects.all().first().site, 'google')

    def test_post_with_tags(self):
        self.register_user()
        self.login_user()
        tag1 = {'name': 'search'}
        tag2 = {'name': 'engine'}
        bookmark_resp = self.create_bookmark(
            url='https://www.google.com',
            title='Google Search',
            tags=[tag1, tag2],
            verify=False
        )
        self.assertEqual(bookmark_resp.status_code, 201)
        bookmrks = Bookmark.objects.all()
        tags = Tag.objects.all()
        self.assertEqual(bookmrks.count(), 1)
        self.assertEqual(tags.count(), 2)
        self.assertEqual(bookmrks.first().tags.count(), 2)
