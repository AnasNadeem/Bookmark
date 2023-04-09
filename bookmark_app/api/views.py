import jwt

from django.conf import settings
from rest_framework import response, status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from .serializers import (
    # Bookmark
    BookmarkSerializer,
    BookmarkSerializerWithoutTagSerializer,
    # Site
    SiteSerializer,
    # Tag
    TagSerializer,
    # User
    ChangePasswordSerializer,
    LoginSerializer,
    OtpSerializer,
    RegisterSerializer,
    TokenSerializer,
    UserEmailSerializer,
    UserSerializer,
)
from bookmark_app.models import (Bookmark, Site, Tag, User)
from utils.helper_functions import send_or_verify_otp, site_extractor
from utils.permissions import (IsAuthenticated,
                               UserPermission,
                               )


class BaseModelViewSet(ModelViewSet):
    def _create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return serializer

    def _update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return serializer, partial


class UserViewset(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = ()

    def get_permissions(self):
        user_permission_map = {
            "update": UserPermission,
            'list': IsAuthenticated,
        }
        if self.action in user_permission_map:
            self.permission_classes = [user_permission_map.get(self.action)]
        return super().get_permissions()

    def get_serializer_class(self):
        user_serializer_map = {
            "create": RegisterSerializer,
            "login": LoginSerializer,
            "forget_password": UserEmailSerializer,
            "verify_otp": OtpSerializer,
            "token_login": TokenSerializer,
            "password_change": ChangePasswordSerializer,
        }
        return user_serializer_map.get(self.action.lower(), UserSerializer)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.filter(email=serializer.data.get('email')).first()
        resp_data, resp_status = send_or_verify_otp(request, user)
        return response.Response(resp_data, status=resp_status)

    @action(detail=False, methods=['post'])
    def login(self, request):
        data = request.data
        email = data.get('email', '')
        password = data.get('password', '')
        user = User.objects.filter(email=email).first()
        if not user:
            return response.Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        authenticated = user.check_password(password)
        if not authenticated:
            return response.Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        resp_data, resp_status = send_or_verify_otp(request, user)
        return response.Response(resp_data, status=resp_status)

    @action(detail=False, methods=['post'])
    def forget_password(self, request):
        data = request.data
        email = data.get('email', '')
        user = User.objects.filter(email=email).first()
        if not user:
            return response.Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        resp_data, resp_status = send_or_verify_otp(request, user, resent=True)
        return response.Response(resp_data, status=resp_status)

    @action(detail=False, methods=['post'])
    def token_login(self, request):
        data = request.data
        token = data.get('token')
        if not token:
            return response.Response({"status": "Token's field not provided"}, status=status.HTTP_400_BAD_REQUEST)

        payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
        user = User.objects.filter(email=payload['email']).first()
        if user:
            user_serializer_data = UserSerializer(user).data
            return response.Response(user_serializer_data, status=status.HTTP_200_OK)
        return response.Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def verify_otp(self, request):
        data = request.data
        email = data.get('email', '')
        if not email:
            return response.Response({'error': 'Email cannot be blank.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()
        if not user:
            return response.Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        otp = data.get('otp', '')
        if not otp:
            return response.Response({'error': 'OTP cannot be blank.'}, status=status.HTTP_400_BAD_REQUEST)

        resp_data, resp_status = send_or_verify_otp(request, user, otp)
        return response.Response(resp_data, status=resp_status)

    @action(detail=False, methods=['put'])
    def password_change(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response("password changed successfully ", status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagViewSet(BaseModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (UserPermission,)

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        serializer = self._create(request, *args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def bookmarks(self, request, pk=None):
        tag = self.get_object()
        bookmarks = tag.bookmarks.all()
        serializer = BookmarkSerializerWithoutTagSerializer(bookmarks, many=True)
        return response.Response(serializer.data)


class SiteViewSet(BaseModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    permission_classes = (UserPermission,)

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        serializer = self._create(request, *args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)


class BookmarkViewSet(BaseModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = (UserPermission,)

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        request = self._set_site(request)
        serializer = self._create(request, *args, **kwargs)
        tags = request.data.get('tags', [])
        if not tags:
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        for tag in tags:
            if not isinstance(tag, dict):
                continue
            name = tag.get('name', '')
            if not name:
                continue
            tag_obj, created = Tag.objects.get_or_create(name=name, user=request.user)
            serializer.instance.tags.add(tag_obj)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        request = self._set_site(request)
        serializer, partial = self._update(request, *args, **kwargs)
        tags = request.data.get('tags', [])
        if not tags:
            return response.Response(serializer.data)
        # HACK: This is a hack to remove all tags and add new tags
        if not partial:
            serializer.instance.tags.clear()
        for tag in tags:
            if not isinstance(tag, dict):
                continue
            name = tag.get('name', '')
            if not name:
                continue
            tag_obj, created = Tag.objects.get_or_create(name=name, user=request.user)
            serializer.instance.tags.add(tag_obj)
        return response.Response(serializer.data)

    def _set_site(self, request):
        url = request.data.get('url', '')
        if not url:
            return request
        site = site_extractor(url)
        if not site:
            return response.Response({'error': 'Invalid url'}, status=status.HTTP_400_BAD_REQUEST)
        site_obj, created = Site.objects.get_or_create(name=site, user=request.user)
        request.data['site'] = site_obj.id
        return request
