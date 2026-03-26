from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.recruitment.api.views.prospect import ProspectAPIView
from apps.recruitment.api.views.application import ApplicationViewSet

router = DefaultRouter(trailing_slash=False)

router.register(r'prospects', ProspectAPIView, basename='prospects')
router.register(r'applications', ApplicationViewSet, basename='applications')

api_urls = router.urls