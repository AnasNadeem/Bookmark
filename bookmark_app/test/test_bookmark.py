from bookmark_app.models import Bookmark
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

    # def test_post_with_auth(self):
    #     self.register_user()
    #     self.login_user()
    #     bookmark_resp = self.create_bookmark(name='Test', verify=False)
    #     self.assertEqual(bookmark_resp.status_code, 201)
    #     self.assertEqual(Bookmark.objects.all().count(), 1)
