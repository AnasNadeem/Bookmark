from django.contrib import admin
from .models import User, UserOTP, Tag, Bookmark


admin.site.register(User)
admin.site.register(UserOTP)
admin.site.register(Tag)
admin.site.register(Bookmark)
