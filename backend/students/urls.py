from rest_framework.routers import DefaultRouter

from .views import AttendanceRecordViewSet, StudentViewSet

router = DefaultRouter()
router.register("students", StudentViewSet, basename="student")
router.register("attendance", AttendanceRecordViewSet, basename="attendance")

urlpatterns = router.urls