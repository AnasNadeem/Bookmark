from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    BookmarkViewSet,
    TagViewSet,
    UserViewset,
)


router = routers.SimpleRouter(trailing_slash=False)
router.register(r"bookmark", BookmarkViewSet, basename="bookmark")
router.register(r"tag", TagViewSet, basename="tag")
router.register(r"user", UserViewset, basename="user")


urlpatterns = []

urlpatterns += router.urls
urlpatterns = format_suffix_patterns(urlpatterns)
