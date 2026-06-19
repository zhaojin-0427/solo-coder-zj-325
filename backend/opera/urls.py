from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ProgramViewSet, AriaViewSet, RoleViewSet, MemberViewSet,
    AriaAssignmentViewSet, RehearsalViewSet, RehearsalFeedbackViewSet,
    UnderstudyChangeViewSet, ArchiveViewSet,
    RehearsalCheckViewSet, RehearsalCheckItemViewSet,
    RehearsalCheckConfirmationViewSet, RiskActionItemViewSet,
    PerformanceReviewViewSet, PerformanceReviewItemViewSet,
    PerformanceReviewConclusionViewSet, MemberSelfReviewViewSet,
    ImprovementTaskViewSet,
    StatisticsView, AutoAssignView, ApplyAutoAssignView,
    CreatePerformanceReviewView, ConvertToTaskView
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
router.register(r'rehearsal-checks', RehearsalCheckViewSet)
router.register(r'rehearsal-check-items', RehearsalCheckItemViewSet)
router.register(r'rehearsal-check-confirmations', RehearsalCheckConfirmationViewSet)
router.register(r'risk-action-items', RiskActionItemViewSet)
router.register(r'performance-reviews', PerformanceReviewViewSet)
router.register(r'performance-review-items', PerformanceReviewItemViewSet)
router.register(r'performance-review-conclusions', PerformanceReviewConclusionViewSet)
router.register(r'member-self-reviews', MemberSelfReviewViewSet)
router.register(r'improvement-tasks', ImprovementTaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('statistics/', StatisticsView.as_view(), name='statistics'),
    path('auto-assign/', AutoAssignView.as_view(), name='auto-assign'),
    path('apply-auto-assign/', ApplyAutoAssignView.as_view(), name='apply-auto-assign'),
    path('create-performance-review/', CreatePerformanceReviewView.as_view(), name='create-performance-review'),
    path('convert-to-task/', ConvertToTaskView.as_view(), name='convert-to-task'),
]
