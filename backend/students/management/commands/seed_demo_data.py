import random
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.management.base import BaseCommand

from students.models import AttendanceRecord, Student

User = get_user_model()

FIRST_NAMES = ["Oshadha", "Kenji", "Maria", "Linh", "Arjun", "Yuki", "Carlos", "Fatima"]
LAST_NAMES = ["Paranamana", "Tanaka", "Santos", "Nguyen", "Sharma", "Sato", "Reyes", "Khan"]
NATIONALITIES = ["Sri Lanka", "Japan", "Philippines", "Vietnam", "India", "Nepal", "Indonesia"]
DEPARTMENTS = ["Information & Software / Global IT Course", "Business & IT Course"]
JLPT = ["NONE", "N5", "N4", "N3", "N2", "N1"]


class Command(BaseCommand):
    help = "Seed demo students, attendance records and the admin / staff1 / student1 logins."

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=25)

    def handle(self, *args, **options):
        count = options["count"]

        # --- Demo logins -------------------------------------------------
        #   admin    / AdminPass123!    superuser (React app + full Django admin)
        #   staff1   / StaffPass123!    staff     (React app admin features + limited Django admin)
        #   student1 / StudentPass123!  student   (sees ONLY their own record and stats)
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@example.com", "AdminPass123!")
            self.stdout.write(self.style.SUCCESS("Created admin / AdminPass123! (superuser)"))

        staff_user, created = User.objects.get_or_create(
            username="staff1", defaults={"email": "staff1@example.com", "is_staff": True}
        )
        if created:
            staff_user.set_password("StaffPass123!")
            staff_user.save()
            # Let staff1 use the Django admin site for the students app only.
            staff_user.user_permissions.set(Permission.objects.filter(content_type__app_label="students"))
            self.stdout.write(self.style.SUCCESS("Created staff1 / StaffPass123! (staff)"))

        demo_user, created = User.objects.get_or_create(
            username="student1", defaults={"email": "student1@example.com"}
        )
        if created:
            demo_user.set_password("StudentPass123!")
            demo_user.save()
            self.stdout.write(self.style.SUCCESS("Created student1 / StudentPass123! (student)"))

        created_count = 0
        demo_student = None
        for i in range(1, count + 1):
            student_number = f"2025{i:03d}"
            if Student.objects.filter(student_number=student_number).exists():
                continue
            first = random.choice(FIRST_NAMES)
            last = random.choice(LAST_NAMES)
            birth_year = random.randint(1998, 2007)
            s = Student.objects.create(
                student_number=student_number,
                call_name=first,
                full_name=f"{last.upper()} {first.upper()}",
                full_name_kana="",
                gender=random.choice(["M", "F"]),
                birthday=date(birth_year, random.randint(1, 12), random.randint(1, 28)),
                nationality=random.choice(NATIONALITIES),
                telephone_number="025-000-0000",
                mobile_phone_number="090-0000-0000",
                email=f"{first.lower()}.{last.lower()}{i}@example.com",
                address="Niigata, Japan",
                grade_level=random.choice(["1", "2", "3"]),
                department=random.choice(DEPARTMENTS),
                class_name=random.choice(["2-A", "2-B", "3-A"]),
                enrollment_date=date(2025, 4, 1),
                previous_school="Sample Senior High School",
                jlpt_level=random.choice(JLPT),
                previous_school_attendance_rate=round(random.uniform(85, 100), 2),
                present_school_attendance_rate=round(random.uniform(85, 100), 2),
            )
            if i == 1:
                s.user = demo_user
                s.save()
                demo_student = s
            for d in range(20 if i == 1 else 5):
                AttendanceRecord.objects.get_or_create(
                    student=s,
                    date=date.today() - timedelta(days=d),
                    defaults={"status": random.choice(["PRESENT", "PRESENT", "PRESENT", "LATE", "ABSENT"])},
                )
            created_count += 1

        # Make sure student1 is linked even if the students already existed.
        first = Student.objects.filter(student_number="2025001").first()
        if first and first.user_id is None:
            first.user = demo_user
            first.save()
        self.stdout.write(self.style.SUCCESS(f"Seeded {created_count} students."))