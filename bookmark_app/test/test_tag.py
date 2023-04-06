from bookmark_app.models import Tag
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
        register_resp = self.register_user()
        user_id = register_resp.json()['id']
        tag_resp = self.create_tag(
            user_id=user_id,
            name='Test',
        )
        self.assertEqual(tag_resp.status_code, 403)
        self.assertEqual(Tag.objects.all().count(), 0)

    def test_post_with_auth(self):
        register_resp = self.register_user()
        user_id = register_resp.json()['id']
        self.login_user()
        tag_resp = self.create_tag(
            user_id=user_id,
            name='Test',
        )
        self.assertEqual(tag_resp.status_code, 201)
        self.assertEqual(Tag.objects.all().count(), 1)
