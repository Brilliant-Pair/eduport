from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from . import models
from django.utils.translation import gettext_lazy as _


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "email",
        "username",
        "is_active",
        "is_staff",
        "is_superuser",
        "last_login",
    )
    list_filter = ("is_active", "is_staff", "is_superuser")
    search_fields = ("email", "username")
    readonly_fields = ("last_login", "created_at", "updated_at")
    ordering = ["-created_at"]

    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
        (_("Metadata"), {"fields": ("created_at", "updated_at")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "first_name",
        "last_name",
        "gender",
        "phone",
        "is_public",
    )
    list_filter = ("gender", "is_public")
    search_fields = (
        "user__email",
        "user__username",
        "first_name",
        "last_name",
        "phone",
    )
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ("user",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "first_name",
                    "last_name",
                    "avatar",
                    "caption",
                    "phone",
                    "gender",
                    "full_address",
                    "is_public",
                )
            },
        ),
        (
            _("Social Links"),
            {"fields": ("facebook", "github", "linkedin", "twitter", "website_url")},
        ),
        (_("Metadata"), {"fields": ("created_at", "updated_at")}),
    )


@admin.register(models.Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "job_title",
        "status",
        "experience_year",
        "job_start_date",
    )
    list_editable = ["status"]
    list_filter = ["status", "job_title", "job_start_date"]
    search_fields = ["user__username", "user__email", "job_title"]


@admin.register(models.ApplyInstructor)
class ApplyInstructorAdmin(admin.ModelAdmin):
    list_display = (
        "phone",
        "email",
        "gender",
        "status",
        "updated_at",
    )
    list_editable = [
        "status",
    ]
    list_filter = ["gender", "status"]
    search_fields = ["first_name", "last_name", "email", "phone"]


@admin.register(models.Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("instructor", "name", "level", "created_at")
    list_filter = ("level",)
    search_fields = ("instructor__user__email", "name")
    autocomplete_fields = ("instructor",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(models.Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = (
        "instructor",
        "major",
        "degree",
        "institution",
        "start",
        "end",
        "is_finished",
    )
    list_filter = ("degree", "institution")
    search_fields = ("instructor__user__email", "major", "institution")
    autocomplete_fields = ("instructor",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(models.Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = (
        "instructor",
        "job_title",
        "company",
        "level",
        "start",
        "end",
        "is_finished",
    )
    list_filter = ("level", "company")
    search_fields = ("instructor__user__email", "job_title", "company")
    autocomplete_fields = ("instructor",)
    readonly_fields = ("created_at", "updated_at")
