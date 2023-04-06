import jwt

from django.conf import settings
from rest_framework import response, status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from .serializers import (
    BookmarkSerializer,
    SiteSerializer,
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
from bookmark_app.models import (User, Bookmark, Site, Tag)
from utils.helper_functions import send_or_verify_otp
from utils.permissions import (IsAuthenticated,
                               UserPermission,
                               )


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


class SiteViewSet(ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class BookmarkViewSet(ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
