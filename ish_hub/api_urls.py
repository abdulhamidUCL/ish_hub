from rest_framework.routers import DefaultRouter
from jobs.api_views import JobViewSet
from companies.api_views import CompanyViewSet
from applications.api_views import ApplicationViewSet
from accounts.api_views import ResumeViewSet


router = DefaultRouter()

router.register("jobs", JobViewSet, basename="job")
router.register("companies", CompanyViewSet, basename="company")
router.register("applications", ApplicationViewSet, basename="application")
router.register("resumes", ResumeViewSet, basename="resume")

urlpatterns = router.urls