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
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at", "-updated_at"]


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
    id = models.BigAutoField(primary_key=True, editable=False)
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, db_index=True
    )
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
        return self.email


class Profile(BaseModel):
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


class Instructor(BaseModel):

    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name=_("User"),
        related_name="instructor",
    )
    status = models.BooleanField(verbose_name="instructor status", default=False)
    birthdate = models.DateField(verbose_name=_("date of birth"))
    experience_year = models.PositiveSmallIntegerField(
        verbose_name=_("experience years")
    )
    job_title = models.CharField(verbose_name=_("job title"), max_length=100)
    job_start_date = models.DateField(verbose_name=_("job start date"))
    job_end_date = models.DateField(
        verbose_name=_("job end date"), null=True, blank=True
    )
    resume = models.FileField(verbose_name=_("Resume"), upload_to="Instructor_resume/")

    class Meta:
        verbose_name = _("Instructor")
        verbose_name_plural = _("Instructors")

    def __str__(self):
        return f"Teacher: {self.user.username} - {self.job_title}"


class ApplyInstructor(BaseModel):
    class Gender(models.TextChoices):
        MALE = (
            "M",
            _("MALE"),
        )
        FEMALE = "F", _("FEMALE")

    class STATUS(models.TextChoices):
        PENDING = "PENDING", _("PENDING")
        APPROVED = "APPROVED", _("APPROVED")
        REJECTED = "REJECTED", _("REJECTED")

    first_name = models.CharField(verbose_name=_("first name"), max_length=255)
    last_name = models.CharField(verbose_name=_("last name"), max_length=255)

    phone = models.CharField(
        verbose_name="profile phone",
        max_length=11,
        validators=[validators.validate_phone],
        unique=True,
    )
    gender = models.CharField(
        verbose_name=_("gender"),
        max_length=10,
        choices=Gender.choices,
    )
    email = models.EmailField(verbose_name=_("email address"), unique=True)
    address = models.TextField(verbose_name=_("address"))

    resume = models.FileField(verbose_name=_("Resume"), upload_to="Instructor_resume/")

    status = models.CharField(
        verbose_name=_("status"),
        max_length=20,
        choices=STATUS.choices,
        default=STATUS.PENDING,
    )

    class Meta:
        verbose_name = _("Apply Instructor")
        verbose_name_plural = _("Apply Instructors")

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.status}"


class Skill(BaseModel):
    class Level(models.TextChoices):
        basic = "Basic", _("Basic")
        intermediate = "Intermediate", _("Intermediate")
        advanced = "Advanced", _("Advanced")

    instructor = models.ForeignKey(
        Instructor,
        verbose_name="instructor skill",
        on_delete=models.CASCADE,
        related_name="skills",
    )
    name = models.CharField(verbose_name=_("skill name"), max_length=255)
    level = models.CharField(verbose_name="skill level", choices=Level.choices)

    class Meta:
        verbose_name = _("Skill")
        verbose_name_plural = _("Skills")


class Education(BaseModel):
    class Degree(models.TextChoices):
        BACHELOR = "Bachelor", _("Bachelor's Degree")
        MASTER = "Master", _("Master's Degree")
        DOCTORATE = "Doctorate", _("Doctorate Degree")
        PROFESSIONAL = "Professional", _("Professional Degree")
        DIPLOMA = "Diploma", _("Diploma/Certificate")
        OTHER = "Other", _("Other")

    instructor = models.ForeignKey(
        Instructor,
        verbose_name="instructor education",
        on_delete=models.CASCADE,
        related_name="educations",
    )
    major = models.CharField(verbose_name="education major", max_length=255)
    degree = models.CharField(verbose_name="education degree", choices=Degree.choices)
    institution = models.CharField(verbose_name="education institution", max_length=255)
    start = models.DateField(verbose_name="education start date")
    end = models.DateField(verbose_name="education end date", blank=True, null=True)

    class Meta:
        verbose_name = _("Eduction")
        verbose_name_plural = _("Eductions")

    @property
    def is_finished(self):
        return self.end is not None


class Experience(BaseModel):
    class Level(models.TextChoices):
        INTERN = "INTERN", _("INTERN")
        JUNIOR = "JUNIOR", _("JUNIOR")
        MID = "MID", _("MID")
        SENIOR = "SENIOR", _("SENIOR")

    instructor = models.ForeignKey(
        Instructor,
        verbose_name=_("instructor experience"),
        on_delete=models.CASCADE,
        related_name="experiences",
    )
    job_title = models.CharField(verbose_name=_("job title"), max_length=255)
    company = models.CharField(verbose_name=_("company"), max_length=255)
    level = models.CharField(verbose_name=_("job level"), choices=Level.choices)
    start = models.DateField(verbose_name="job start date")
    end = models.DateField(verbose_name="job end date", blank=True, null=True)

    @property
    def is_finished(self):
        return self.end is not None
