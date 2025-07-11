# Generated by Django 5.1.3 on 2025-06-01 15:56

import apps.accounts.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="ApplyInstructor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "first_name",
                    models.CharField(max_length=255, verbose_name="first name"),
                ),
                (
                    "last_name",
                    models.CharField(max_length=255, verbose_name="last name"),
                ),
                (
                    "phone",
                    models.CharField(
                        max_length=11,
                        unique=True,
                        validators=[apps.accounts.validators.validate_phone],
                        verbose_name="profile phone",
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[("M", "MALE"), ("F", "FEMALE")],
                        max_length=10,
                        verbose_name="gender",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="email address"
                    ),
                ),
                ("address", models.TextField(verbose_name="address")),
                (
                    "resume",
                    models.FileField(
                        upload_to="Instructor_resume/", verbose_name="Resume"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PENDING", "PENDING"),
                            ("APPROVED", "APPROVED"),
                            ("REJECTED", "REJECTED"),
                        ],
                        default="PENDING",
                        max_length=20,
                        verbose_name="status",
                    ),
                ),
            ],
            options={
                "verbose_name": "Apply Instructor",
                "verbose_name_plural": "Apply Instructors",
            },
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "id",
                    models.BigAutoField(
                        editable=False, primary_key=True, serialize=False
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(
                        db_index=True, default=uuid.uuid4, editable=False, unique=True
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        help_text="Required. Must be a valid email address.",
                        max_length=255,
                        unique=True,
                        verbose_name="email",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        blank=True,
                        help_text="Optional. 255 characters or fewer.",
                        max_length=255,
                        null=True,
                        unique=True,
                        verbose_name="username",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(default=False, verbose_name="active status"),
                ),
                (
                    "is_staff",
                    models.BooleanField(default=False, verbose_name="staff status"),
                ),
                (
                    "is_superuser",
                    models.BooleanField(default=False, verbose_name="superuser status"),
                ),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "User",
                "verbose_name_plural": "Users",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Instructor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.BooleanField(
                        default=False, verbose_name="instructor status"
                    ),
                ),
                ("birthdate", models.DateField(verbose_name="date of birth")),
                (
                    "experience_year",
                    models.PositiveSmallIntegerField(verbose_name="experience years"),
                ),
                (
                    "job_title",
                    models.CharField(max_length=100, verbose_name="job title"),
                ),
                ("job_start_date", models.DateField(verbose_name="job start date")),
                (
                    "job_end_date",
                    models.DateField(
                        blank=True, null=True, verbose_name="job end date"
                    ),
                ),
                (
                    "resume",
                    models.FileField(
                        upload_to="Instructor_resume/", verbose_name="Resume"
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="instructor",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
            options={
                "verbose_name": "Instructor",
                "verbose_name_plural": "Instructors",
            },
        ),
        migrations.CreateModel(
            name="Experience",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "job_title",
                    models.CharField(max_length=255, verbose_name="job title"),
                ),
                ("company", models.CharField(max_length=255, verbose_name="company")),
                (
                    "level",
                    models.CharField(
                        choices=[
                            ("INTERN", "INTERN"),
                            ("JUNIOR", "JUNIOR"),
                            ("MID", "MID"),
                            ("SENIOR", "SENIOR"),
                        ],
                        verbose_name="job level",
                    ),
                ),
                ("start", models.DateField(verbose_name="job start date")),
                (
                    "end",
                    models.DateField(
                        blank=True, null=True, verbose_name="job end date"
                    ),
                ),
                (
                    "instructor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="experiences",
                        to="accounts.instructor",
                        verbose_name="instructor experience",
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at", "-updated_at"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Education",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "major",
                    models.CharField(max_length=255, verbose_name="education major"),
                ),
                (
                    "degree",
                    models.CharField(
                        choices=[
                            ("Bachelor", "Bachelor's Degree"),
                            ("Master", "Master's Degree"),
                            ("Doctorate", "Doctorate Degree"),
                            ("Professional", "Professional Degree"),
                            ("Diploma", "Diploma/Certificate"),
                            ("Other", "Other"),
                        ],
                        verbose_name="education degree",
                    ),
                ),
                (
                    "institution",
                    models.CharField(
                        max_length=255, verbose_name="education institution"
                    ),
                ),
                ("start", models.DateField(verbose_name="education start date")),
                (
                    "end",
                    models.DateField(
                        blank=True, null=True, verbose_name="education end date"
                    ),
                ),
                (
                    "instructor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="educations",
                        to="accounts.instructor",
                        verbose_name="instructor education",
                    ),
                ),
            ],
            options={
                "verbose_name": "Eduction",
                "verbose_name_plural": "Eductions",
            },
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="last name"
                    ),
                ),
                (
                    "avatar",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="avatars/",
                        verbose_name="profile avatar",
                    ),
                ),
                (
                    "caption",
                    models.TextField(
                        blank=True, null=True, verbose_name="profile caption"
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        blank=True,
                        max_length=11,
                        null=True,
                        validators=[apps.accounts.validators.validate_phone],
                        verbose_name="profile phone",
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        blank=True,
                        choices=[("M", "MALE"), ("F", "FEMALE")],
                        max_length=10,
                        null=True,
                        verbose_name="gender",
                    ),
                ),
                (
                    "full_address",
                    models.TextField(
                        blank=True, null=True, verbose_name="full address"
                    ),
                ),
                (
                    "facebook",
                    models.URLField(
                        blank=True,
                        max_length=255,
                        null=True,
                        validators=[django.core.validators.URLValidator()],
                        verbose_name="Facebook URL",
                    ),
                ),
                (
                    "github",
                    models.URLField(
                        blank=True,
                        max_length=255,
                        null=True,
                        validators=[django.core.validators.URLValidator()],
                        verbose_name="Github URL",
                    ),
                ),
                (
                    "linkedin",
                    models.URLField(
                        blank=True,
                        max_length=255,
                        null=True,
                        validators=[django.core.validators.URLValidator()],
                        verbose_name="Linkedin URL",
                    ),
                ),
                (
                    "twitter",
                    models.URLField(
                        blank=True,
                        max_length=255,
                        null=True,
                        validators=[django.core.validators.URLValidator()],
                        verbose_name="Twitter URL",
                    ),
                ),
                (
                    "website_url",
                    models.URLField(
                        blank=True,
                        max_length=255,
                        null=True,
                        validators=[django.core.validators.URLValidator()],
                        verbose_name="Website URL",
                    ),
                ),
                (
                    "is_public",
                    models.BooleanField(default=False, verbose_name="profile status"),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Profile",
                "verbose_name_plural": "Profiles",
            },
        ),
        migrations.CreateModel(
            name="Skill",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255, verbose_name="skill name")),
                (
                    "level",
                    models.CharField(
                        choices=[
                            ("Basic", "Basic"),
                            ("Intermediate", "Intermediate"),
                            ("Advanced", "Advanced"),
                        ],
                        verbose_name="skill level",
                    ),
                ),
                (
                    "instructor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="skills",
                        to="accounts.instructor",
                        verbose_name="instructor skill",
                    ),
                ),
            ],
            options={
                "verbose_name": "Skill",
                "verbose_name_plural": "Skills",
            },
        ),
    ]
