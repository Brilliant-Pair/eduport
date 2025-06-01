from django.contrib import admin

from . import models


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
