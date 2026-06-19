from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ProgramViewSet, AriaViewSet, RoleViewSet, MemberViewSet,
    AriaAssignmentViewSet, RehearsalViewSet, RehearsalFeedbackViewSet,
    UnderstudyChangeViewSet, ArchiveViewSet,
    StatisticsView, AutoAssignView, ApplyAutoAssignView
)

router = DefaultRouter()
router.register(r'programs', ProgramViewSet)
router.register(r'arias', AriaViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'members', MemberViewSet)
router.register(r'aria-assignments', AriaAssignmentViewSet)
router.register(r'rehearsals', RehearsalViewSet)
router.register(r'rehearsal-feedbacks', RehearsalFeedbackViewSet)
router.register(r'understudy-changes', UnderstudyChangeViewSet)
router.register(r'archives', ArchiveViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('statistics/', StatisticsView.as_view(), name='statistics'),
    path('auto-assign/', AutoAssignView.as_view(), name='auto-assign'),
    path('apply-auto-assign/', ApplyAutoAssignView.as_view(), name='apply-auto-assign'),
]
