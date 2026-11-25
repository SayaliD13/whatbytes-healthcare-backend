from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import DoctorViewSet, MappingViewSet, PatientViewSet, RegisterView, login_view

router = DefaultRouter()
router.register("patients", PatientViewSet, basename="patient")
router.register("doctors", DoctorViewSet, basename="doctor")
router.register("mappings", MappingViewSet, basename="mapping")

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", login_view, name="login"),
    path("", include(router.urls)),
]
