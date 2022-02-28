from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
import uuid as uuid_lib

class Department(models.Model):
    """所属モデル 兼任可"""

    name = models.CharField(_('Teams'), max_length=100, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Teams')
        verbose_name_plural = _('Teams')


class User(AbstractBaseUser, PermissionsMixin):
    """カスタムユーザモデル"""

    uuid = models.UUIDField(default=uuid_lib.uuid4,
                            primary_key=True, editable=False)

    username = models.CharField(
        _('username'),
        max_length=100,
        unique=True,
        help_text=_(
            'Required. 100 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[UnicodeUsernameValidator()],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    full_name = models.CharField(_('Full Name'), max_length=100, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    departments = models.ManyToManyField(
        Department,
        verbose_name=_('Teams'),
        blank=True,
        help_text=_('Specific Departments for this user.'),
        related_name="user_set",
        related_query_name="user",
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=True,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    # get_full_name()の変更
    def get_full_name(self):
        if self.full_name:
            return self.full_name
        else:
            return self.username + '（No name）'

    # 選択リストでの表示
    def __str__(self):
        return self.get_full_name()
