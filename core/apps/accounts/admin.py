from django.contrib import admin
from . import models


@admin.register(models.Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "job_title",
        "status",
        "experience_year",
        "job_start_date",
        "is_valid",
    )
    list_editable = ("status", "is_valid")
    list_filter = ("status", "is_valid", "job_start_date")
    search_fields = ("user__username", "user__email", "job_title")


@admin.register(models.ApplyTeacher)
class ApplyTeacherAdmin(admin.ModelAdmin):
    list_display = (
        "phone",
        "email",
        "gender",
        "status",    
        "updated_at",
    )
    list_editable = ("status",)
    list_filter = ("gender", "status")
    search_fields = ("first_name", "last_name", "email", "phone")
