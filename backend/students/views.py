from rest_framework import viewsets

from .models import AttendanceRecord, Student
from .serializers import (
    AttendanceRecordSerializer,
    StudentDetailSerializer,
    StudentListSerializer,
)


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().prefetch_related("attendance_records")

    def get_serializer_class(self):
        if self.action == "list":
            return StudentListSerializer
        return StudentDetailSerializer


class AttendanceRecordViewSet(viewsets.ModelViewSet):
    queryset = AttendanceRecord.objects.select_related("student")
    serializer_class = AttendanceRecordSerializer
