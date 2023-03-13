from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns


router = routers.SimpleRouter(trailing_slash=False)
# router.register(r"account", AccountViewset, basename="account")

urlpatterns = []

urlpatterns += router.urls
urlpatterns = format_suffix_patterns(urlpatterns)
