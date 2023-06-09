import copy

from bookmark_app.models import (Bookmark, Site, Tag)
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
        self.assertEqual(Bookmark.objects.all().first().site.name, 'google')
        self.assertEqual(Site.objects.all().count(), 1)

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
        self.assertEqual(Bookmark.objects.all().first().site.name, 'google')

    def test_post_with_new_tags(self):
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

    def test_post_with_existing_tags(self):
        self.register_user()
        self.login_user()
        self.create_tag(name='search')
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

    ######################
    # ---- PUT ---- #
    ######################
    def test_put_without_auth(self):
        self.register_user()
        self.login_user()
        bookmark = self.create_bookmark(
            url='https://www.google.com',
            title='Google Search',
            verify=False
        )
        self.logout_user()
        bookmark_data = copy.deepcopy(bookmark.json())
        bookmark_resp = self.update_bookmark(
            bookmark_id=bookmark.json()['id'],
            bookmark_data=bookmark_data,
            verify=False
        )
        self.assertEqual(bookmark_resp.status_code, 403)
        self.assertEqual(Bookmark.objects.first().title, 'Google Search')

    def test_put_with_partial_data(self):
        self.register_user()
        self.login_user()
        bookmark = self.create_bookmark(
            url='https://www.google.com',
            title='Google Search',
        )

        partial_bookmark_data = {
            'url': 'https://www.bing.com',
            'title': 'Bing Search',
        }
        bookmark_resp = self.update_bookmark(
            bookmark_id=bookmark.json()['id'],
            bookmark_data=partial_bookmark_data,
            verify=False
        )
        self.assertEqual(bookmark_resp.status_code, 400)
        bookmark = Bookmark.objects.first()
        self.assertEqual(bookmark.title, 'Google Search')
        self.assertEqual(bookmark.site.name, 'google')

    def test_put_with_full_data(self):
        self.register_user()
        self.login_user()
        bookmark = self.create_bookmark(
            url='https://www.google.com',
            title='Google Search',
        )

        bookmark_data = copy.deepcopy(bookmark.json())
        bookmark_data['url'] = 'https://www.bing.com'
        bookmark_data['title'] = 'Bing Search'
        bookmark_resp = self.update_bookmark(
            bookmark_id=bookmark.json()['id'],
            bookmark_data=bookmark_data,
            verify=False
        )
        self.assertEqual(bookmark_resp.status_code, 200)
        bookmark = Bookmark.objects.first()
        self.assertEqual(bookmark.title, 'Bing Search')
        self.assertEqual(bookmark.site.name, 'bing')

    def test_put_with_new_tags(self):
        self.register_user()
        self.login_user()
        bookmark = self.create_bookmark(
            url='https://www.google.com',
            title='Google Search',
        )

        tag1 = {'name': 'search'}
        tag2 = {'name': 'engine'}
        bookmark_data = copy.deepcopy(bookmark.json())
        bookmark_data['tags'] = [tag1, tag2]
        bookmark_resp = self.update_bookmark(
            bookmark_id=bookmark.json()['id'],
            bookmark_data=bookmark_data,
            verify=False
        )
        self.assertEqual(bookmark_resp.status_code, 200)
        bookmrks = Bookmark.objects.all()
        tags = Tag.objects.all()
        self.assertEqual(bookmrks.count(), 1)
        self.assertEqual(tags.count(), 2)
        self.assertEqual(bookmrks.first().tags.count(), 2)
        self.assertEqual(Site.objects.all().count(), 1)

    def test_put_with_existing_tags(self):
        self.register_user()
        self.login_user()
        tag1 = {'name': 'search'}
        bookmark = self.create_bookmark(
            url='https://www.google.com',
            title='Google Search',
            tags=[tag1],
            verify=False
        )
        bookmarks = Bookmark.objects.all()
        self.assertEqual(bookmarks.first().tags.count(), 1)
        self.assertEqual(bookmarks.first().tags.first().name, 'search')

        tag2 = {'name': 'engine'}
        bookmark_data = copy.deepcopy(bookmark.json())
        bookmark_data['tags'] = [tag2]
        bookmark_resp = self.update_bookmark(
            bookmark_id=bookmark.json()['id'],
            bookmark_data=bookmark_data,
            verify=False
        )
        self.assertEqual(bookmark_resp.status_code, 200)
        bookmarks = Bookmark.objects.all()
        self.assertEqual(bookmarks.first().tags.count(), 1)
        self.assertEqual(bookmarks.first().tags.first().name, 'engine')
        self.assertEqual(Tag.objects.count(), 2)

    ######################
    # ---- PATCH ---- #
    ######################
    def test_patch_without_auth(self):
        self.register_user()
        self.login_user()
        bookmark = self.create_bookmark(
            url='https://www.google.com',
            title='Google Search',
        )
        self.logout_user()
        bookmark_data = copy.deepcopy(bookmark.json())
        bookmark_data['title'] = 'Bing Search'
        bookmark_resp = self.update_bookmark(
            bookmark_id=bookmark.json()['id'],
            bookmark_data=bookmark_data,
            patch=True,
            verify=False
        )
        self.assertEqual(bookmark_resp.status_code, 403)
        self.assertEqual(Bookmark.objects.first().title, 'Google Search')

    def test_patch_with_incorrect_title(self):
        self.register_user()
        self.login_user()
        bookmark = self.create_bookmark(
            url='https://www.google.com',
            title='Google Search',
        )
        self.assertEqual(Bookmark.objects.first().title, 'Google Search')
        self.assertEqual(Bookmark.objects.first().site.name, 'google')
        self.assertEqual(Site.objects.all().count(), 1)

        bookmark_data = {
            'title': 'Bing Search',
        }
        bookmark_resp = self.update_bookmark(
            bookmark_id=bookmark.json()['id'],
            bookmark_data=bookmark_data,
            patch=True,
            verify=False
        )
        self.assertEqual(bookmark_resp.status_code, 200)
        self.assertEqual(Bookmark.objects.first().title, 'Bing Search')
        self.assertEqual(Bookmark.objects.first().site.name, 'google')
        self.assertEqual(Bookmark.objects.first().url, 'https://www.google.com')
        self.assertEqual(Site.objects.all().count(), 1)

    def test_patch_with_tags(self):
        self.register_user()
        self.login_user()
        bookmark = self.create_bookmark(
            url='https://www.google.com',
            title='Google Search',
            tags=[{'name': 'test'}],
        )
        bookmark_data = {
            'tags': [
                {'name': 'search'},
                {'name': 'engine'},
            ]
        }
        bookmark_resp = self.update_bookmark(
            bookmark_id=bookmark.json()['id'],
            bookmark_data=bookmark_data,
            patch=True,
            verify=False
        )
        self.assertEqual(bookmark_resp.status_code, 200)
        bookmarks = Bookmark.objects.all()
        tags = Tag.objects.all()
        self.assertEqual(bookmarks.count(), 1)
        self.assertEqual(tags.count(), 3)
        self.assertEqual(bookmarks.first().tags.count(), 3)
        self.assertEqual(bookmarks.first().tags.first().name, 'test')
        self.assertEqual(bookmarks.first().tags.last().name, 'engine')
        self.assertEqual(Site.objects.all().count(), 1)

    ######################
    # ---- DELETE ---- #
    ######################
    def test_delete_without_auth(self):
        self.register_user()
        self.login_user()
        bookmark = self.create_bookmark(
            url='https://www.google.com',
            title='Google Search',
        )
        self.logout_user()
        bookmark_resp = self.delete_bookmark(
            bookmark_id=bookmark.json()['id'],
            verify=False
        )
        self.assertEqual(bookmark_resp.status_code, 403)
        self.assertEqual(Bookmark.objects.all().count(), 1)

    def test_delete(self):
        self.register_user()
        self.login_user()
        bookmark = self.create_bookmark(
            url='https://www.google.com',
            title='Google Search',
        )
        bookmark_resp = self.delete_bookmark(
            bookmark_id=bookmark.json()['id'],
            verify=False
        )
        self.assertEqual(bookmark_resp.status_code, 204)
        self.assertEqual(Bookmark.objects.all().count(), 0)
        self.assertEqual(Site.objects.all().count(), 1)

    def test_delete_check_tags(self):
        self.register_user()
        self.login_user()
        self.create_tag(name='tag1')
        tag1 = {'name': 'tag1'}
        tag2 = {'name': 'tag2'}

        bookmark = self.create_bookmark(
            url='https://www.google.com',
            title='Google Search',
            tags=[tag1, tag2],
        )
        bookmark_resp = self.delete_bookmark(
            bookmark_id=bookmark.json()['id'],
            verify=False
        )
        self.assertEqual(bookmark_resp.status_code, 204)
        self.assertEqual(Bookmark.objects.all().count(), 0)
        self.assertEqual(Tag.objects.all().count(), 2)
        self.assertEqual(Site.objects.all().count(), 1)
