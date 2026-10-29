
import uuid

from django.conf import settings
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import models
from django.utils import timezone


# Phone number validation
phone_validator = RegexValidator(
    regex=r"^\+?[0-9\-() ]{7,20}$",
    message="Enter a valid phone number.",
)


class Student(models.Model):

    # Gender choices
    class Gender(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"
        OTHER = "O", "Other / Prefer not to say"

    # JLPT choices
    class JLPTLevel(models.TextChoices):
        NONE = "NONE", "Not taken"
        N5 = "N5", "N5"
        N4 = "N4", "N4"
        N3 = "N3", "N3"
        N2 = "N2", "N2"
        N1 = "N1", "N1"

    # Grade level choices
    class GradeLevel(models.TextChoices):
        YEAR_1 = "1", "1st Year"
        YEAR_2 = "2", "2nd Year"
        YEAR_3 = "3", "3rd Year"
        YEAR_4 = "4", "4th Year"
        GRADUATE = "G", "Graduate"

    # Primary key
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    # Linked user account
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="student_profile",
    )

    # Student identity
    student_number = models.CharField(
        max_length=20,
        unique=True,
    )

    call_name = models.CharField(max_length=100)

    full_name = models.CharField(max_length=200)

    full_name_kana = models.CharField(
        max_length=200,
        blank=True,
    )

    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
    )

    birthday = models.DateField()

    nationality = models.CharField(max_length=100)

    # Contact information
    telephone_number = models.CharField(
        max_length=20,
        blank=True,
        validators=[phone_validator],
    )

    mobile_phone_number = models.CharField(
        max_length=20,
        blank=True,
        validators=[phone_validator],
    )

    email = models.EmailField(unique=True)

    address = models.CharField(
        max_length=255,
        blank=True,
    )

    # Academic information
    grade_level = models.CharField(
        max_length=1,
        choices=GradeLevel.choices,
    )

    department = models.CharField(
        max_length=150,
        blank=True,
    )

    class_name = models.CharField(
        max_length=20,
        blank=True,
    )

    enrollment_date = models.DateField()

    previous_school = models.CharField(
        max_length=200,
        blank=True,
    )

    # JLPT information
    jlpt_level = models.CharField(
        max_length=4,
        choices=JLPTLevel.choices,
        default=JLPTLevel.NONE,
    )

    # Attendance percentage validation
    attendance_validators = [
        MinValueValidator(0),
        MaxValueValidator(100),
    ]

    previous_school_attendance_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=attendance_validators,
    )

    present_school_attendance_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=attendance_validators,
    )

    # Student photo
    photo = models.ImageField(
        upload_to="student_photos/",
        blank=True,
        null=True,
    )

    # Account status
    is_active = models.BooleanField(default=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["student_number"]

    def __str__(self):
        return f"{self.student_number} - {self.call_name}"

    @property
    def age(self):
        if not self.birthday:
            return None

        today = timezone.localdate()

        return (
            today.year
            - self.birthday.year
            - (
                (today.month, today.day)
                < (self.birthday.month, self.birthday.day)
            )
        )


class AttendanceRecord(models.Model):

    # Attendance status choices
    class Status(models.TextChoices):
        PRESENT = "PRESENT", "Present"
        ABSENT = "ABSENT", "Absent"
        LATE = "LATE", "Late"
        EXCUSED = "EXCUSED", "Excused"

    # Student relationship
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="attendance_records",
    )

    date = models.DateField()

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
    )

    note = models.CharField(
        max_length=255,
        blank=True,
    )

    # Teacher or administrator recording attendance
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

        constraints = [
            models.UniqueConstraint(
                fields=["student", "date"],
                name="unique_student_attendance_date",
            )
        ]

    def __str__(self):
        return (
            f"{self.student.student_number} - "
            f"{self.date} - {self.status}"
        )
