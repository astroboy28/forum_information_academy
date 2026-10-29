import django_filters as filters

from .models import Student


class StudentFilter(filters.FilterSet):
    grade_level = filters.CharFilter(field_name="grade_level")
    gender = filters.CharFilter(field_name="gender")
    jlpt_level = filters.CharFilter(field_name="jlpt_level")
    nationality = filters.CharFilter(field_name="nationality", lookup_expr="icontains")
    enrolled_after = filters.DateFilter(field_name="enrollment_date", lookup_expr="gte")
    enrolled_before = filters.DateFilter(field_name="enrollment_date", lookup_expr="lte")
    is_active = filters.BooleanFilter(field_name="is_active")

    class Meta:
        model = Student
        fields = ["grade_level", "gender", "jlpt_level", "nationality", "is_active", "class_name"]