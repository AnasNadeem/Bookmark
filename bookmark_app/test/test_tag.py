import copy

from bookmark_app.models import Bookmark, Tag
from .test_base import ConstantMixin
from rest_framework.test import APITestCase


class TestTag(APITestCase, ConstantMixin):

    ######################
    # ---- GET ---- #
    ######################
    def test_get_without_auth(self):
        tag_resp = self.client.get(self.TAG_URL)
        self.assertEqual(tag_resp.status_code, 403)

    def test_get_with_auth(self):
        self.register_user()
        self.login_user()
        tag_resp = self.client.get(self.TAG_URL)
        self.assertEqual(tag_resp.status_code, 200)
        self.assertEqual(tag_resp.json(), [])

    ######################
    # ---- POST ---- #
    ######################
    def test_post_without_auth(self):
        self.register_user()
        tag_resp = self.create_tag(name='Test', verify=False)
        self.assertEqual(tag_resp.status_code, 403)
        self.assertEqual(Tag.objects.all().count(), 0)

    def test_post_with_auth(self):
        self.register_user()
        self.login_user()
        tag_resp = self.create_tag(name='Test', verify=False)
        self.assertEqual(tag_resp.status_code, 201)
        self.assertEqual(Tag.objects.all().count(), 1)

    ######################
    # ---- PUT ---- #
    ######################
    def test_put(self):
        self.register_user()
        self.login_user()
        tag_resp = self.create_tag(name='Test')
        tag_id = tag_resp.json()['id']
        tag_data = copy.deepcopy(tag_resp.json())
        tag_data['name'] = 'Test2'
        tag_resp = self.client.put(
            f'{self.TAG_URL}/{tag_id}', tag_data, format="json")
        self.assertEqual(tag_resp.status_code, 200)
        self.assertEqual(Tag.objects.all().count(), 1)
        self.assertEqual(Tag.objects.all().first().name, 'Test2')

    ######################
    # ---- DELETE ---- #
    ######################
    def test_delete(self):
        self.register_user()
        self.login_user()
        tag_resp = self.create_tag(name='Test')
        tag_id = tag_resp.json()['id']
        tag_resp = self.client.delete(f'{self.TAG_URL}/{tag_id}')
        self.assertEqual(tag_resp.status_code, 204)
        self.assertEqual(Tag.objects.all().count(), 0)

    ######################
    # ---- BOOKMARKS ---- #
    ######################
    def test_get_bookmarks(self):
        self.register_user()
        self.login_user()
        tag_resp = self.create_tag(name='search')
        tag_data = copy.deepcopy(tag_resp.json())
        tag_id = tag_resp.json()['id']
        tag_bookmark_resp = self.client.get(f'{self.TAG_URL}/{tag_id}/bookmarks')
        self.assertEqual(tag_bookmark_resp.status_code, 200)
        self.assertEqual(tag_bookmark_resp.json(), [])

        self.create_bookmark(
            url='https://www.google.com',
            title='Google Search',
            tags=[tag_data]
        )
        self.create_bookmark(
            url='https://www.bing.com',
            title='Bing Search',
            tags=[tag_data]
        )
        self.create_bookmark(
            url='https://www.duck.com',
            title='duckduckgo Search',
            tags=[]
        )
        self.assertEqual(Tag.objects.all().count(), 1)
        self.assertEqual(Bookmark.objects.all().count(), 3)

        tag_bookmark_resp = self.client.get(f'{self.TAG_URL}/{tag_id}/bookmarks')
        self.assertEqual(tag_bookmark_resp.status_code, 200)
        self.assertEqual(len(tag_bookmark_resp.json()), 2)
