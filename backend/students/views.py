from rest_framework import viewsets

from .filters import StudentFilter
from .models import AttendanceRecord, Student
from .serializers import (
    AttendanceRecordSerializer,
    StudentDetailSerializer,
    StudentListSerializer,
)


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().prefetch_related("attendance_records")
    filterset_class = StudentFilter
    search_fields = [
        "student_number", "call_name", "full_name", "full_name_kana",
        "email", "nationality", "previous_school",
    ]
    ordering_fields = ["student_number", "call_name", "birthday", "grade_level", "enrollment_date", "jlpt_level"]
    ordering = ["student_number"]

    def get_serializer_class(self):
        if self.action == "list":
            return StudentListSerializer
        return StudentDetailSerializer


class AttendanceRecordViewSet(viewsets.ModelViewSet):
    queryset = AttendanceRecord.objects.select_related("student")
    serializer_class = AttendanceRecordSerializer
    filterset_fields = ["student", "status", "date"]
    ordering_fields = ["date"]
    ordering = ["-date"]