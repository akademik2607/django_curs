from django.contrib.auth.models import AbstractBaseUser, AbstractUser, PermissionsMixin, _user_has_perm
from django.db import models
from users.managers import UserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _


from django.core.mail import send_mail
from django.utils import timezone


NULLABLE = {'blank': True, 'null': True}

class UserRoles(models.TextChoices):
    ADMIN = 'admin', _('admin')
    USER = 'user', _('user')


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    last_login = models.DateTimeField(_("date joined"), default=timezone.now)
    phone = PhoneNumberField(_("phone number"), blank=True)
    role = models.CharField(_("role"), choices=UserRoles.choices, max_length=5, default=UserRoles.USER)
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    image = models.ImageField(_("avatar"), **NULLABLE)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        swappable = "AUTH_USER_MODEL"

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def has_perm(self, perm, obj=None):
        print(self.role)
        if self.is_active and self.role == UserRoles.ADMIN:
            print("доступ разрешён")
            return True

        # Otherwise we need to check the backends.
        return _user_has_perm(self, perm, obj)
