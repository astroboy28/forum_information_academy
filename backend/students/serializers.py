
from rest_framework import serializers

from .models import AttendanceRecord, Student


# =====================================================
# ATTENDANCE RECORD SERIALIZER
# =====================================================

class AttendanceRecordSerializer(serializers.ModelSerializer):

    student_number = serializers.CharField(
        source="student.student_number",
        read_only=True,
    )

    class Meta:
        model = AttendanceRecord

        fields = [
            "id",
            "student",
            "student_number",
            "date",
            "status",
            "note",
            "recorded_by",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "student_number",
            "recorded_by",
            "created_at",
        ]


# =====================================================
# STUDENT LIST SERIALIZER
# =====================================================

class StudentListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for displaying
    students in a paginated list.
    """

    age = serializers.IntegerField(read_only=True)

    gender_display = serializers.CharField(
        source="get_gender_display",
        read_only=True,
    )

    grade_level_display = serializers.CharField(
        source="get_grade_level_display",
        read_only=True,
    )

    class Meta:
        model = Student

        fields = [
            "id",
            "student_number",
            "call_name",
            "full_name",
            "gender",
            "gender_display",
            "age",
            "nationality",
            "grade_level",
            "grade_level_display",
            "class_name",
            "jlpt_level",
            "is_active",
            "photo",
        ]

        read_only_fields = [
            "id",
            "age",
            "gender_display",
            "grade_level_display",
        ]


# =====================================================
# STUDENT DETAIL SERIALIZER
# =====================================================

class StudentDetailSerializer(serializers.ModelSerializer):
    """
    Full serializer for:
    - Retrieving student details
    - Creating students
    - Updating students
    """

    age = serializers.IntegerField(read_only=True)

    attendance_records = AttendanceRecordSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Student

        fields = [
            "id",
            "user",
            "student_number",
            "call_name",
            "full_name",
            "full_name_kana",
            "gender",
            "birthday",
            "age",
            "nationality",
            "telephone_number",
            "mobile_phone_number",
            "email",
            "address",
            "grade_level",
            "department",
            "class_name",
            "enrollment_date",
            "previous_school",
            "jlpt_level",
            "previous_school_attendance_rate",
            "present_school_attendance_rate",
            "photo",
            "is_active",
            "attendance_records",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "age",
            "attendance_records",
            "created_at",
            "updated_at",
        ]

    # -------------------------------------------------
    # ATTENDANCE RATE VALIDATION
    # -------------------------------------------------

    def _validate_rate(self, value):
        """
        Ensure attendance rate is between
        0 and 100 percent.
        """

        if value is not None and not (0 <= value <= 100):
            raise serializers.ValidationError(
                "Enter a percentage between 0 and 100."
            )

        return value

    def validate_previous_school_attendance_rate(
        self, value
    ):
        return self._validate_rate(value)

    def validate_present_school_attendance_rate(
        self, value
    ):
        return self._validate_rate(value)

    # -------------------------------------------------
    # EMAIL VALIDATION
    # -------------------------------------------------

    def validate_email(self, value):
        """
        Prevent duplicate email addresses,
        ignoring uppercase/lowercase differences.
        """

        value = value.strip().lower()

        qs = Student.objects.filter(
            email__iexact=value
        )

        if self.instance is not None:
            qs = qs.exclude(
                pk=self.instance.pk
            )

        if qs.exists():
            raise serializers.ValidationError(
                "A student with this email already exists."
            )

        return value
