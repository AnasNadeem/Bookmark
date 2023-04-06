from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from bookmark_app.models_manager import UserManager

from phonenumber_field.modelfields import PhoneNumberField


class TimeBaseModel(models.Model):
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractBaseUser, PermissionsMixin):

    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True, blank=False)
    phone_number = PhoneNumberField(null=True, blank=True, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    # def email_user(self, subject, message, from_email=None, **kwargs):
    #     """Send an email to this user."""
    #     send_mail(subject, message, from_email, [self.email], **kwargs)


class UserOTP(TimeBaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email


class Site(TimeBaseModel):
    name = models.CharField(max_length=100, unique=True)
    url = models.URLField()
    icon = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class Tag(TimeBaseModel):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'user')

    def __str__(self):
        return f"{self.name}"


class Bookmark(TimeBaseModel):
    url = models.URLField()
    title = models.TextField()
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='bookmarks', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('url', 'user')

    def __str__(self):
        return f"{self.site}: {self.title}"
