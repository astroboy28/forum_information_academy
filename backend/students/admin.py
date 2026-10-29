from django.contrib import admin

from .models import AttendanceRecord, Student


class AttendanceInline(admin.TabularInline):
    model = AttendanceRecord
    extra = 0
    fields = ("date", "status", "note", "recorded_by")
    readonly_fields = ("created_at",)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "student_number", "call_name", "full_name", "gender", "age",
        "nationality", "grade_level", "class_name", "jlpt_level", "is_active",
    )
    list_filter = ("gender", "grade_level", "jlpt_level", "nationality", "is_active")
    search_fields = ("student_number", "call_name", "full_name", "full_name_kana", "email", "nationality")
    readonly_fields = ("id", "created_at", "updated_at")
    inlines = [AttendanceInline]


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ("student", "date", "status", "recorded_by")
    list_filter = ("status", "date")
    search_fields = ("student__student_number", "student__call_name")
