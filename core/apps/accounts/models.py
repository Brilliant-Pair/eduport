import uuid
from typing import Optional

from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator, validate_email
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from . import validators


class BaseModel(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, db_index=True
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):

    def email_validator(self, email: str) -> None:
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("You must provide a valid email address."))

    def create_user(
        self,
        *,
        username: str,
        email: str,
        password: Optional[str] = None,
        **extra_fields,
    ):
        """
        Creates and saves a new user with given username, email and password
        """

        if not username:
            raise ValueError(_("Users must have an username."))

        if not email:
            raise ValueError(_("Users must have an email address."))

        email = self.normalize_email(email)
        self.email_validator(email)

        user = self.model(username=username, email=email, **extra_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        user.save(using=self._db)
        return user

    def create_superuser(
        self, *, username: str, email: str, password: str, **extra_fields
    ):
        """
        Creates and saves a new super user with given username, email and password
        """
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(
                _("Superusers must have 'is_staff' attribute set to True.")
            )

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                _("Superusers must have 'is_superuser' attribute set to True.")
            )

        if not password:
            raise ValueError(_("Superuser must have password."))

        return self.create_user(
            username=username, email=email, password=password, **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    class Role(models.TextChoices):
        STUDENT = "S", _("STUDENT")
        INSTRUCTOR = "I", _("INSTRUCTOR")
        ADMIN = "A", _("ADMIN")

    email = models.EmailField(
        verbose_name=_("email"),
        max_length=255,
        unique=True,
        help_text=_("Required. Must be a valid email address."),
    )
    username = models.CharField(
        verbose_name=_("username"),
        max_length=255,
        unique=True,
        blank=True,
        null=True,
        help_text=_("Optional. 255 characters or fewer."),
    )
    role = models.CharField(verbose_name=_("role"), choices=Role.choices)

    is_active = models.BooleanField(verbose_name=_("active status"), default=False)
    is_staff = models.BooleanField(verbose_name=_("staff status"), default=False)
    is_superuser = models.BooleanField(
        verbose_name=_("superuser status"), default=False
    )

    last_login = models.DateTimeField(_("last login"), blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

    objects = UserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.username}" if username else f"{self.email}"


class Profile(models.Model):
    class Gender(models.TextChoices):
        MALE = (
            "M",
            _("MALE"),
        )
        FEMALE = "F", _("FEMALE")

    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, related_name="profile"
    )
    first_name = models.CharField(
        verbose_name=_("first name"), max_length=255, blank=True, null=True
    )
    last_name = models.CharField(
        verbose_name=_("last name"), max_length=255, blank=True, null=True
    )
    avatar = models.ImageField(
        verbose_name="profile avatar", upload_to="avatars/", blank=True, null=True
    )
    caption = models.TextField(verbose_name="profile caption", blank=True, null=True)
    phone = models.CharField(
        verbose_name="profile phone",
        max_length=11,
        null=True,
        blank=True,
        validators=[validators.validate_phone],
    )
    gender = models.CharField(
        verbose_name=_("gender"),
        max_length=10,
        choices=Gender.choices,
        blank=True,
        null=True,
    )
    full_address = models.TextField(verbose_name="full address", null=True, blank=True)
    facebook = models.URLField(
        verbose_name=_("Facebook URL"),
        max_length=255,
        blank=True,
        null=True,
        validators=[URLValidator()],
    )
    github = models.URLField(
        verbose_name=_("Github URL"),
        max_length=255,
        blank=True,
        null=True,
        validators=[URLValidator()],
    )
    linkedin = models.URLField(
        verbose_name=_("Linkedin URL"),
        max_length=255,
        blank=True,
        null=True,
        validators=[URLValidator()],
    )
    twitter = models.URLField(
        verbose_name=_("Twitter URL"),
        max_length=255,
        blank=True,
        null=True,
        validators=[URLValidator()],
    )
    website_url = models.URLField(
        verbose_name=_("Website URL"),
        max_length=255,
        blank=True,
        null=True,
        validators=[URLValidator()],
    )
    is_public = models.BooleanField(verbose_name="profile status", default=False)

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self):
        return f"{self.user.username}'s Profile" if self.user else "Profile"

    def get_full_name(self):
        """Returns the user's full name (if available)."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.user.get_full_name() if self.user else ""


class Teacher(models.Model):
    STATUS_CHOICES = (
        ("active", _("Active")),
        ("inactive", _("Inactive")),
    )

    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name=_("User"),
        related_name="teacher",
    )
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=STATUS_CHOICES,
        default="active",
    )

    experience_year = models.PositiveIntegerField(
        _("Experience Year"),
    )
    job_title = models.CharField(_("Job Title"), max_length=100)
    job_start_date = models.DateField(_("Job Start Date"))
    job_end_date = models.DateField(_("Job End Date"), null=True, blank=True)
    birthdate = models.DateField(_("Date of Birth"))

    resume = models.FileField(
        _("Resume"),
        upload_to="teacher_files/",
    )

    is_valid = models.BooleanField(
        _("Is Valid"),
        default=True,
    )

    class Meta:
        verbose_name = _("Teacher")
        verbose_name_plural = _("Teachers")

    def __str__(self):
        return f"Teacher: {self.user.username} - {self.job_title}"


class ApplyTeacher(models.Model):
    GENDER_CHOICES = (
        ("M", _("Male")),
        ("F", _("Female")),
    )

    STATUS_CHOICES = (
        ("pending", _("Pending")),
        ("approved", _("Approved")),
        ("rejected", _("Rejected")),
    )

    first_name = models.CharField(_("First Name"), max_length=100)
    last_name = models.CharField(_("Last Name"), max_length=100)
    gender = models.CharField(
        _("Gender"), max_length=1, choices=GENDER_CHOICES, default="M"
    )

    phone = models.CharField(
        _("Phone"), max_length=11, unique=True, validators=[validators.validate_phone]
    )
    email = models.EmailField(_("Email"), unique=True)
    address = models.TextField(_("Address"))

    resume = models.FileField(
        _("Resume"),
        upload_to="teacher_files/",
    )

    status = models.CharField(
        _("Status"), max_length=20, choices=STATUS_CHOICES, default="pending"
    )
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Apply Teacher")
        verbose_name_plural = _("Apply Teachers")
        ordering = ("-updated_at",)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.status}"
