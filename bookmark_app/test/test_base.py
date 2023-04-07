from bookmark_app.models import UserOTP


class ConstantMixin(object):
    DEFAULT_EMAIL = "test@gmail.com"
    DEFAULT_EMAIL2 = "test2@gmail.com"

    # UserViewset URLs
    REGISTER_URL = "/api/user"
    LOGIN_URL = "/api/user/login"
    USER_LIST_URL = "/api/user"
    USER_DATA = {"email": DEFAULT_EMAIL, "password": "Test@123"}
    USER2_DATA = {"email": DEFAULT_EMAIL2, "password": "Test@1234"}
    PASSWORD_CHANGE_URL = "/api/user/password_change"

    # TagViewSet URLs
    TAG_URL = "/api/tag"

    # BookmarkViewSet URLs
    BOOKMARK_URL = "/api/bookmark"

    def register_user(self, email=DEFAULT_EMAIL):
        user_data = {"email": email, "password": "Test@123"}
        # Register
        resp = self.client.post(self.REGISTER_URL, user_data)

        # UserOTP
        user_otp = UserOTP.objects.filter(is_verified=False).first()
        user_otp.is_verified = True
        user_otp.save()

        return resp

    def login_user(self, email=DEFAULT_EMAIL):
        user_data = {"email": email, "password": "Test@123"}
        login_resp = self.client.post(self.LOGIN_URL, user_data)
        token = login_resp.json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION=token)

    def create_tag(self, name, verify=True):
        tag_data = {"name": name}
        resp = self.client.post(self.TAG_URL, tag_data, format="json")
        if verify:
            self.assertEqual(resp.status_code, 201)
        return resp

    def create_bookmark(self, url, title, tags, user_id, verify=True):
        site = url.split("//")[1].split("/")[0]
        bookmark_data = {
            "url": url,
            "title": title,
            "site": site,
            "tags": tags,
            "user": user_id,
        }
        resp = self.client.post(self.BOOKMARK_URL, bookmark_data, format="json")
        if verify:
            self.assertEqual(resp.status_code, 201)
        return resp
