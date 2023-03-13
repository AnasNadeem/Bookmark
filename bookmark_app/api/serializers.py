# from django.contrib.auth import password_validation
from django.contrib.auth.models import User

from rest_framework.serializers import ModelSerializer
from bookmark_app.models import (Platform, Tag, Bookmark)


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('id',
                  'email',
                  'username',
                  'first_name',
                  'last_name',
                  'is_staff',
                  'is_active',
                  'date_joined',
                  )


class PlatformSerializer(ModelSerializer):

    class Meta:
        model = Platform
        fields = '__all__'


class TagSerializer(ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class BookmarkSerializer(ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Bookmark
        fields = '__all__'
