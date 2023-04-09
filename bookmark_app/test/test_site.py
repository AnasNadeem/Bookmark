import copy

from bookmark_app.models import Bookmark, Site
from .test_base import ConstantMixin
from rest_framework.test import APITestCase


class TestSite(APITestCase, ConstantMixin):

    ######################
    # ---- GET ---- #
    ######################
    def test_get_without_auth(self):
        site_resp = self.client.get(self.SITE_URL)
        self.assertEqual(site_resp.status_code, 403)

    def test_get_with_auth(self):
        self.register_user()
        self.login_user()
        site_resp = self.client.get(self.SITE_URL)
        self.assertEqual(site_resp.status_code, 200)
        self.assertEqual(site_resp.json(), [])

    ######################
    # ---- POST ---- #
    ######################
    def test_post_without_auth(self):
        self.register_user()
        site_resp = self.create_site(name='Test', verify=False)
        self.assertEqual(site_resp.status_code, 403)
        self.assertEqual(Site.objects.all().count(), 0)

    def test_post_with_auth(self):
        self.register_user()
        self.login_user()
        site_resp = self.create_site(name='Test', verify=False)
        self.assertEqual(site_resp.status_code, 201)
        self.assertEqual(Site.objects.all().count(), 1)

    ######################
    # ---- PUT ---- #
    ######################
    def test_put(self):
        self.register_user()
        self.login_user()
        site_resp = self.create_site(name='Test')
        site_id = site_resp.json()['id']
        site_data = copy.deepcopy(site_resp.json())
        site_data['name'] = 'Test2'
        site_resp = self.client.put(
            f'{self.SITE_URL}/{site_id}', site_data, format="json")
        self.assertEqual(site_resp.status_code, 200)
        self.assertEqual(Site.objects.all().count(), 1)
        self.assertEqual(Site.objects.all().first().name, 'Test2')

    ######################
    # ---- DELETE ---- #
    ######################
    def test_delete(self):
        self.register_user()
        self.login_user()
        site_resp = self.create_site(name='Test')
        site_id = site_resp.json()['id']
        site_resp = self.client.delete(f'{self.SITE_URL}/{site_id}')
        self.assertEqual(site_resp.status_code, 204)
        self.assertEqual(Site.objects.all().count(), 0)

    ######################
    # ---- BOOKMARKS ---- #
    ######################
    def test_get_bookmarks(self):
        self.register_user()
        self.login_user()
        self.create_bookmark(
            url='https://github.com/AnasNadeem',
            title='Anas Nadeem | Github',
        )
        self.create_bookmark(
            url='https://github.com/falakfatma',
            title='Falak Fatma | Github',
        )
        self.assertEqual(Bookmark.objects.all().count(), 2)
        self.assertEqual(Site.objects.all().count(), 1)
        site_id = Site.objects.all().first().id
        site_resp = self.client.get(f'{self.SITE_URL}/{site_id}/bookmarks')
        self.assertEqual(site_resp.status_code, 200)
        self.assertEqual(len(site_resp.json()), 2)
