from django.contrib.auth.models import User
from .serializers import (
    BookmarkSerializer,
    PlatformSerializer,
    TagSerializer,
    UserSerializer,
)
from bookmark_app.models import (Bookmark, Platform, Tag)
from rest_framework.viewsets import ModelViewSet


class UserViewset(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PlatformViewSet(ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class BookmarkViewSet(ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
