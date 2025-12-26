from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import HabitViewSet, PublicHabitListView

router = DefaultRouter()
router.register("habits", HabitViewSet, basename="habits")

urlpatterns = router.urls + [
    path("habits/public/", PublicHabitListView.as_view(), name="public-habits"),
]
