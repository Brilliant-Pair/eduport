from django.db import models
from django.utils.translation import ugettext_lazy as _
from . import validators


class Teacher(models.Model):
    STATUS_CHOICES = (
        ("active", _("Active")),
        ("inactive", _("Inactive")),
    )

    user = models.OneToOneField(
        "CustomUser",
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
