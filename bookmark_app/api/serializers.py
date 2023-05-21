from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from bookmark_app.models import (Bookmark, Site, Tag, User)


######################
# ---- USER ---- #
######################
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id',
                  'email',
                  'first_name',
                  'last_name',
                  'is_staff',
                  'is_active',
                  'date_joined',
                  )


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=50, min_length=4, write_only=True)
    email = serializers.EmailField(max_length=100)

    class Meta:
        model = User
        fields = ('email', 'password')

    def validate(self, attrs):
        email = attrs.get('email', '')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': ('User already exist with this email')})
        return super().validate(attrs)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=50, min_length=4)
    email = serializers.EmailField(max_length=100)

    class Meta:
        model = User
        fields = ('email', 'password')
        read_only_fields = ('password', )


class OtpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=100)
    otp = serializers.CharField(max_length=10)

    class Meta:
        model = User
        fields = ('email', 'otp')


class UserEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=100)

    class Meta:
        model = User
        fields = ('email',)


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=250)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    password = serializers.CharField(max_length=128, write_only=True, required=True)
    confirm_password = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Your old password was entered Incorrectly. Please enter it again. ")
        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({'Confirm_password': _("The password fields didn't match.")})
        password_validation.validate_password(data['password'], self.context['request'].user)
        return data

    def save(self, **kwargs):
        password = self.validated_data['password']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user


######################
# ---- TAG ---- #
######################
class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class TagSerializerWithBookmarkCount(serializers.ModelSerializer):
    bookmark_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'bookmark_count',
        )


######################
# ---- SITE ---- #
######################
class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = '__all__'


######################
# ---- BOOKMARK ---- #
######################
class BookmarkSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Bookmark
        fields = '__all__'


class BookmarkSerializerWithoutTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bookmark
        fields = '__all__'
