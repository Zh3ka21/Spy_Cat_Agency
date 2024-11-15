from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SpyCatViewSet, MissionViewSet

router = DefaultRouter()
router.register(r'spycats', SpyCatViewSet)
router.register(r'missions', MissionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('missions/<int:pk>/assign_cat/', MissionViewSet.as_view({'post': 'assign_cat'})),
    path('missions/<int:pk>/update_targets/', MissionViewSet.as_view({'post': 'update_targets'})),
]
