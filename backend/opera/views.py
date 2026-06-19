from django.db.models import Count, Q, F, Avg, ExpressionWrapper, DurationField
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime, timedelta
from collections import defaultdict
import json

from .models import (
    Program, Aria, Role, Member, AriaAssignment,
    Rehearsal, RehearsalFeedback, UnderstudyChange, Archive,
    RehearsalCheck, RehearsalCheckItem, RehearsalCheckConfirmation, RiskActionItem
)
from .serializers import (
    ProgramSerializer, AriaSerializer, RoleSerializer, MemberSerializer,
    AriaAssignmentSerializer, RehearsalSerializer, RehearsalFeedbackSerializer,
    UnderstudyChangeSerializer, ArchiveSerializer,
    AutoAssignRequestSerializer, AutoAssignResultSerializer,
    RehearsalCheckSerializer, RehearsalCheckItemSerializer,
    RehearsalCheckConfirmationSerializer, RiskActionItemSerializer,
    compute_risk_flags, RISK_FLAG_LABELS
)


def build_latest_reason(item, action_type):
    aria_name = item.aria.name
    if action_type == 'attendance':
        members = [c.member.name for c in item.confirmations.all() if not c.attendance_confirmed]
        if members:
            return f'唱段「{aria_name}」仍有未确认到场的成员：{"、".join(members)}。'
        return ''
    if action_type == 'understudy':
        return f'唱段「{aria_name}」暂无替补成员。'
    if action_type == 'feedback':
        detail = []
        if item.latest_start_beat_issue:
            detail.append(f'起板问题：{item.latest_start_beat_issue}')
        if item.latest_forgotten_lines:
            detail.append(f'忘词片段：{item.latest_forgotten_lines}')
        if detail:
            return f'唱段「{aria_name}」仍存在排练反馈问题（{"；".join(detail)}）。'
        return ''
    if action_type == 'accompaniment':
        return f'唱段「{aria_name}」伴奏尚未确认备齐（需求：{item.accompaniment_required or "未填写"}）。'
    if action_type == 'teacher_risk':
        return f'唱段「{aria_name}」仍被老师标注为{dict(RehearsalCheckItem.RISK_CHOICES).get(item.risk_level, "未知")}风险，处理意见：{item.teacher_comment or "待补充"}。'
    return ''


def review_risk_action_for_item(item, action_type, trigger_source=None):
    flags = compute_risk_flags(item)
    risk_action = RiskActionItem.objects.filter(
        check_item=item,
        action_type=action_type
    ).first()

    if not risk_action:
        return None

    now = timezone.now()
    risk_action.last_reviewed_at = now

    is_risk_still_exists = action_type in flags

    if is_risk_still_exists:
        if risk_action.status != 'pending':
            risk_action.status = 'pending'
            risk_action.auto_resolve_pending = False
            risk_action.auto_resolve_suggested_at = None
            risk_action.resolved_at = None
            risk_action.resolution_source = None
        risk_action.latest_reason = build_latest_reason(item, action_type)
        risk_action.save(update_fields=[
            'status', 'auto_resolve_pending', 'auto_resolve_suggested_at',
            'resolved_at', 'resolution_source', 'latest_reason', 'last_reviewed_at'
        ])
        return {'action': 'keep_pending', 'risk_action': risk_action}
    else:
        if risk_action.status == 'pending':
            risk_action.status = 'auto_resolved'
            risk_action.auto_resolve_pending = True
            risk_action.auto_resolve_suggested_at = now
            risk_action.resolved_at = now
            risk_action.resolution_source = trigger_source
            risk_action.latest_reason = ''
            risk_action.save(update_fields=[
                'status', 'auto_resolve_pending', 'auto_resolve_suggested_at',
                'resolved_at', 'resolution_source', 'latest_reason', 'last_reviewed_at'
            ])
            return {'action': 'suggest_auto_resolve', 'risk_action': risk_action}

    risk_action.save(update_fields=['last_reviewed_at'])
    return {'action': 'no_change', 'risk_action': risk_action}


def ensure_risk_action_items_for_item(item):
    flags = compute_risk_flags(item)
    created_items = []
    for flag in flags:
        description = build_action_description(item, flag)
        reason = build_latest_reason(item, flag)
        obj, created = RiskActionItem.objects.get_or_create(
            check_item=item,
            action_type=flag,
            defaults={
                'description': description,
                'latest_reason': reason,
                'status': 'pending',
            },
        )
        if created:
            created_items.append(obj)
    if flags:
        item.risk_action_created = True
        item.save(update_fields=['risk_action_created'])
    return created_items


def auto_review_all_risks_for_item(item, trigger_source=None):
    created_items = ensure_risk_action_items_for_item(item)
    created_action_types = {ci.action_type for ci in created_items}
    results = []
    for action_type in ['attendance', 'understudy', 'feedback', 'accompaniment', 'teacher_risk']:
        result = review_risk_action_for_item(item, action_type, trigger_source)
        if result:
            if result['action'] == 'keep_pending' and result['risk_action'].action_type in created_action_types:
                result['action'] = 'created'
            results.append(result)
    return results


class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        type_filter = self.request.query_params.get('type')
        if type_filter:
            queryset = queryset.filter(type=type_filter)
        return queryset.annotate(
            aria_count=Count('arias', distinct=True),
            rehearsal_count=Count('rehearsals', distinct=True)
        )


class AriaViewSet(viewsets.ModelViewSet):
    queryset = Aria.objects.all()
    serializer_class = AriaSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        program_id = self.request.query_params.get('program_id')
        if program_id:
            queryset = queryset.filter(program_id=program_id)
        role_type = self.request.query_params.get('role_type')
        if role_type:
            queryset = queryset.filter(role_type=role_type)
        return queryset


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        program_id = self.request.query_params.get('program_id')
        if program_id:
            queryset = queryset.filter(program_id=program_id)
        return queryset


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        is_understudy = self.request.query_params.get('is_understudy')
        if is_understudy is not None:
            queryset = queryset.filter(is_understudy=(is_understudy.lower() == 'true'))
        return queryset.annotate(
            assignment_count=Count('assignments', distinct=True)
        )


class AriaAssignmentViewSet(viewsets.ModelViewSet):
    queryset = AriaAssignment.objects.all()
    serializer_class = AriaAssignmentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        aria_id = self.request.query_params.get('aria_id')
        if aria_id:
            queryset = queryset.filter(aria_id=aria_id)
        member_id = self.request.query_params.get('member_id')
        if member_id:
            queryset = queryset.filter(member_id=member_id)
        program_id = self.request.query_params.get('program_id')
        if program_id:
            queryset = queryset.filter(aria__program_id=program_id)
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset


class RehearsalViewSet(viewsets.ModelViewSet):
    queryset = Rehearsal.objects.all()
    serializer_class = RehearsalSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        program_id = self.request.query_params.get('program_id')
        if program_id:
            queryset = queryset.filter(program_id=program_id)
        start_date = self.request.query_params.get('start_date')
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        end_date = self.request.query_params.get('end_date')
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        return queryset.annotate(
            feedback_count=Count('feedbacks', distinct=True)
        )


class RehearsalFeedbackViewSet(viewsets.ModelViewSet):
    queryset = RehearsalFeedback.objects.all()
    serializer_class = RehearsalFeedbackSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        rehearsal_id = self.request.query_params.get('rehearsal_id')
        if rehearsal_id:
            queryset = queryset.filter(rehearsal_id=rehearsal_id)
        aria_id = self.request.query_params.get('aria_id')
        if aria_id:
            queryset = queryset.filter(aria_id=aria_id)
        member_id = self.request.query_params.get('member_id')
        if member_id:
            queryset = queryset.filter(member_id=member_id)
        return queryset


class UnderstudyChangeViewSet(viewsets.ModelViewSet):
    queryset = UnderstudyChange.objects.all()
    serializer_class = UnderstudyChangeSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        member_id = self.request.query_params.get('member_id')
        if member_id:
            queryset = queryset.filter(
                Q(original_assignment__member_id=member_id) | Q(substitute_member_id=member_id)
            )
        return queryset


class ArchiveViewSet(viewsets.ModelViewSet):
    queryset = Archive.objects.all()
    serializer_class = ArchiveSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        program_id = self.request.query_params.get('program_id')
        if program_id:
            queryset = queryset.filter(program_id=program_id)
        return queryset


def build_action_description(item, action_type):
    aria_name = item.aria.name
    if action_type == 'attendance':
        members = [c.member.name for c in item.confirmations.all() if not c.attendance_confirmed]
        return f'唱段「{aria_name}」存在未确认到场的成员：{"、".join(members)}，需在演出前落实到场。'
    if action_type == 'understudy':
        return f'唱段「{aria_name}」暂无替补成员，建议尽快安排替补以防演出风险。'
    if action_type == 'feedback':
        detail = []
        if item.latest_start_beat_issue:
            detail.append(f'起板问题：{item.latest_start_beat_issue}')
        if item.latest_forgotten_lines:
            detail.append(f'忘词片段：{item.latest_forgotten_lines}')
        return f'唱段「{aria_name}」最近排练反馈仍有问题（{"；".join(detail)}），需重点强化。'
    if action_type == 'accompaniment':
        return f'唱段「{aria_name}」伴奏尚未确认备齐（需求：{item.accompaniment_required or "未填写"}），需伴奏负责人落实。'
    if action_type == 'teacher_risk':
        return f'唱段「{aria_name}」被老师标注为高风险，处理意见：{item.teacher_comment or "待补充"}。'
    return f'唱段「{aria_name}」存在待处理风险。'


class RehearsalCheckViewSet(viewsets.ModelViewSet):
    queryset = RehearsalCheck.objects.all()
    serializer_class = RehearsalCheckSerializer

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related('items__confirmations')
        program_id = self.request.query_params.get('program_id')
        if program_id:
            queryset = queryset.filter(program_id=program_id)
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def perform_create(self, serializer):
        program = serializer.validated_data.get('program')
        if program.status == 'archived':
            from rest_framework.exceptions import ValidationError
            raise ValidationError({'program': '已归档的节目不能创建联排确认批次'})
        check = serializer.save()
        self._generate_checklist(check)

    def _generate_checklist(self, check):
        arias = Aria.objects.filter(program=check.program).order_by('order_index')
        for aria in arias:
            latest_fb = RehearsalFeedback.objects.filter(aria=aria).select_related('rehearsal').order_by('-created_at').first()
            item = RehearsalCheckItem.objects.create(
                rehearsal_check=check,
                aria=aria,
                order_index=aria.order_index,
                role_type=aria.role_type,
                accompaniment_required=aria.accompaniment_required,
                latest_feedback_date=latest_fb.rehearsal.date if latest_fb else None,
                latest_start_beat_issue=latest_fb.start_beat_issue if latest_fb else '',
                latest_forgotten_lines=latest_fb.forgotten_lines if latest_fb else '',
                latest_teacher_comments=latest_fb.teacher_comments if latest_fb else '',
            )
            assignments = AriaAssignment.objects.filter(aria=aria, status='confirmed').select_related('role')
            for assignment in assignments:
                RehearsalCheckConfirmation.objects.create(
                    check_item=item,
                    member=assignment.member,
                    role=assignment.role,
                    role_name=assignment.role.name if assignment.role else '',
                    is_understudy=assignment.is_understudy,
                )

    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        check = self.get_object()
        items = check.items.prefetch_related('confirmations', 'risk_actions', 'aria', 'accompaniment_confirmed_by').order_by('order_index')
        serializer = RehearsalCheckItemSerializer(items, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def risk_dashboard(self, request, pk=None):
        check = self.get_object()
        items = check.items.prefetch_related('confirmations', 'risk_actions', 'aria').order_by('order_index')
        risk_items = []
        flag_counter = defaultdict(int)
        for item in items:
            flags = compute_risk_flags(item)
            risk_actions = list(item.risk_actions.all())
            if not flags and not risk_actions:
                continue
            for flag in flags:
                flag_counter[flag] += 1
            confirmations = list(item.confirmations.all())
            unconfirmed_members = [
                {'id': c.member_id, 'name': c.member.name, 'role_name': c.role_name or ''}
                for c in confirmations if not c.attendance_confirmed
            ]
            has_pending_actions = any(ra.status == 'pending' for ra in risk_actions)
            risk_items.append({
                'item_id': item.id,
                'aria_id': item.aria_id,
                'aria_name': item.aria.name,
                'order_index': item.order_index,
                'role_type': item.role_type,
                'risk_level': item.risk_level,
                'risk_level_display': item.get_risk_level_display(),
                'flags': flags,
                'flag_labels': [RISK_FLAG_LABELS.get(f, f) for f in flags],
                'risk_score': len(flags),
                'has_active_risks': len(flags) > 0 or has_pending_actions,
                'has_understudy': any(c.is_understudy for c in confirmations),
                'unconfirmed_members': unconfirmed_members,
                'latest_start_beat_issue': item.latest_start_beat_issue,
                'latest_forgotten_lines': item.latest_forgotten_lines,
                'latest_feedback_date': item.latest_feedback_date,
                'accompaniment_confirmed': item.accompaniment_confirmed,
                'teacher_comment': item.teacher_comment,
                'risk_action_created': item.risk_action_created,
            })
        risk_items.sort(key=lambda x: x['risk_score'], reverse=True)
        summary = {
            'total_items': check.items.count(),
            'risk_aria_count': sum(1 for r in risk_items if r['has_active_risks']),
            'flag_breakdown': [
                {'action_type': flag, 'label': RISK_FLAG_LABELS.get(flag, flag), 'count': flag_counter[flag]}
                for flag in ['attendance', 'understudy', 'feedback', 'accompaniment', 'teacher_risk']
                if flag_counter[flag] > 0
            ],
        }
        return Response({
            'check_id': check.id,
            'check_name': check.name,
            'status': check.status,
            'risk_items': risk_items,
            'summary': summary,
        })

    @action(detail=True, methods=['post'])
    def generate_actions(self, request, pk=None):
        check = self.get_object()
        created_items = []
        for item in check.items.prefetch_related('confirmations', 'aria').all():
            flags = compute_risk_flags(item)
            for flag in flags:
                description = build_action_description(item, flag)
                reason = build_latest_reason(item, flag)
                obj, created = RiskActionItem.objects.get_or_create(
                    check_item=item,
                    action_type=flag,
                    defaults={
                        'description': description,
                        'latest_reason': reason,
                    },
                )
                if not created and obj.status == 'pending' and not obj.latest_reason:
                    obj.latest_reason = reason
                    obj.save(update_fields=['latest_reason'])
                if created:
                    created_items.append({
                        'id': obj.id,
                        'check_item': item.id,
                        'aria_name': item.aria.name,
                        'action_type': flag,
                        'description': description,
                    })
            if flags:
                item.risk_action_created = True
                item.save(update_fields=['risk_action_created'])
        return Response({
            'created_count': len(created_items),
            'items': created_items,
        })


class RehearsalCheckItemViewSet(viewsets.ModelViewSet):
    queryset = RehearsalCheckItem.objects.all()
    serializer_class = RehearsalCheckItemSerializer

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related('confirmations', 'risk_actions', 'aria', 'accompaniment_confirmed_by')
        rehearsal_check = self.request.query_params.get('rehearsal_check')
        if rehearsal_check:
            queryset = queryset.filter(rehearsal_check_id=rehearsal_check)
        aria_id = self.request.query_params.get('aria_id')
        if aria_id:
            queryset = queryset.filter(aria_id=aria_id)
        return queryset

    @action(detail=True, methods=['post'])
    def confirm_accompaniment(self, request, pk=None):
        item = self.get_object()
        member_id = request.data.get('member_id')
        member = Member.objects.filter(id=member_id).first() if member_id else None
        item.accompaniment_confirmed = True
        item.accompaniment_confirmed_by = member
        item.save(update_fields=['accompaniment_confirmed', 'accompaniment_confirmed_by'])

        review_results = auto_review_all_risks_for_item(item, trigger_source='accompaniment_confirm')

        response_data = RehearsalCheckItemSerializer(item).data
        response_data['risk_review_results'] = [
            {
                'action': r['action'],
                'risk_action_id': r['risk_action'].id,
                'action_type': r['risk_action'].action_type,
                'status': r['risk_action'].status,
            }
            for r in review_results
        ]
        return Response(response_data)

    @action(detail=True, methods=['post'])
    def set_risk(self, request, pk=None):
        item = self.get_object()
        if 'risk_level' in request.data:
            item.risk_level = request.data['risk_level']
        if 'teacher_comment' in request.data:
            item.teacher_comment = request.data['teacher_comment']
        item.save(update_fields=['risk_level', 'teacher_comment'])

        review_results = auto_review_all_risks_for_item(item, trigger_source='teacher_risk_adjust')

        response_data = RehearsalCheckItemSerializer(item).data
        response_data['risk_review_results'] = [
            {
                'action': r['action'],
                'risk_action_id': r['risk_action'].id,
                'action_type': r['risk_action'].action_type,
                'status': r['risk_action'].status,
            }
            for r in review_results
        ]
        return Response(response_data)

    @action(detail=True, methods=['post'])
    def review_risks(self, request, pk=None):
        item = self.get_object()
        review_results = auto_review_all_risks_for_item(item, trigger_source='system_auto')
        return Response({
            'reviewed_count': len(review_results),
            'results': [
                {
                    'action': r['action'],
                    'risk_action_id': r['risk_action'].id,
                    'action_type': r['risk_action'].action_type,
                    'status': r['risk_action'].status,
                }
                for r in review_results
            ]
        })


class RehearsalCheckConfirmationViewSet(viewsets.ModelViewSet):
    queryset = RehearsalCheckConfirmation.objects.all()
    serializer_class = RehearsalCheckConfirmationSerializer

    def get_queryset(self):
        queryset = super().get_queryset().select_related('member')
        check_item = self.request.query_params.get('check_item')
        if check_item:
            queryset = queryset.filter(check_item_id=check_item)
        member_id = self.request.query_params.get('member_id')
        if member_id:
            queryset = queryset.filter(member_id=member_id)
        return queryset

    def perform_update(self, serializer):
        old_attendance = serializer.instance.attendance_confirmed
        old_lyrics = serializer.instance.lyrics_proficiency
        instance = serializer.save()

        attendance = instance.attendance_confirmed
        lyrics = instance.lyrics_proficiency
        if attendance and lyrics != 'unconfirmed':
            instance.confirmed_at = timezone.now()
            instance.save(update_fields=['confirmed_at'])

        trigger_source = None
        if attendance != old_attendance and attendance:
            trigger_source = 'attendance_confirm'
        elif lyrics != old_lyrics:
            trigger_source = 'lyrics_update'

        if trigger_source:
            item = instance.check_item
            auto_review_all_risks_for_item(item, trigger_source=trigger_source)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        old_attendance = instance.attendance_confirmed
        old_lyrics = instance.lyrics_proficiency

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        response_data = serializer.data

        new_attendance = response_data.get('attendance_confirmed')
        new_lyrics = response_data.get('lyrics_proficiency')
        if (new_attendance != old_attendance) or (new_lyrics != old_lyrics):
            item = instance.check_item
            review_results = auto_review_all_risks_for_item(item, trigger_source='attendance_confirm' if new_attendance != old_attendance else 'lyrics_update')
            response_data['risk_review_results'] = [
                {
                    'action': r['action'],
                    'risk_action_id': r['risk_action'].id,
                    'action_type': r['risk_action'].action_type,
                    'status': r['risk_action'].status,
                }
                for r in review_results
            ]

        return Response(response_data)


class RiskActionItemViewSet(viewsets.ModelViewSet):
    queryset = RiskActionItem.objects.all()
    serializer_class = RiskActionItemSerializer

    def get_queryset(self):
        queryset = super().get_queryset().select_related('check_item__aria', 'handler')
        rehearsal_check = self.request.query_params.get('rehearsal_check')
        if rehearsal_check:
            queryset = queryset.filter(check_item__rehearsal_check_id=rehearsal_check)
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            if is_active.lower() == 'true':
                queryset = queryset.filter(status='pending')
            else:
                queryset = queryset.exclude(status='pending')
        return queryset

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        action = self.get_object()
        handler_id = request.data.get('handler_id')
        handler_note = request.data.get('handler_note', '')

        action.status = 'manually_resolved'
        action.resolved_at = timezone.now()
        action.handler = Member.objects.filter(id=handler_id).first() if handler_id else None
        action.handler_note = handler_note
        action.resolution_source = 'manual_close'
        action.auto_resolve_pending = False
        action.save(update_fields=[
            'status', 'resolved_at', 'handler', 'handler_note',
            'resolution_source', 'auto_resolve_pending'
        ])
        return Response(RiskActionItemSerializer(action).data)

    @action(detail=True, methods=['post'])
    def confirm_close(self, request, pk=None):
        action = self.get_object()
        if not action.auto_resolve_pending:
            return Response(
                {'error': '该风险项不需要管理员确认关闭'},
                status=status.HTTP_400_BAD_REQUEST
            )

        handler_id = request.data.get('handler_id')
        handler_note = request.data.get('handler_note', '')

        action.status = 'confirmed_closed'
        action.auto_resolve_pending = False
        action.handler = Member.objects.filter(id=handler_id).first() if handler_id else None
        action.handler_note = handler_note
        if not action.resolved_at:
            action.resolved_at = timezone.now()
        action.save(update_fields=[
            'status', 'auto_resolve_pending', 'handler', 'handler_note', 'resolved_at'
        ])
        return Response(RiskActionItemSerializer(action).data)

    @action(detail=True, methods=['post'])
    def reject_auto_resolve(self, request, pk=None):
        action = self.get_object()
        if not action.auto_resolve_pending:
            return Response(
                {'error': '该风险项不处于待确认解除状态'},
                status=status.HTTP_400_BAD_REQUEST
            )

        handler_note = request.data.get('handler_note', '')

        action.status = 'pending'
        action.auto_resolve_pending = False
        action.auto_resolve_suggested_at = None
        action.handler_note = handler_note
        action.resolved_at = None
        action.resolution_source = None
        action.latest_reason = build_latest_reason(action.check_item, action.action_type)
        action.save(update_fields=[
            'status', 'auto_resolve_pending', 'auto_resolve_suggested_at',
            'handler_note', 'resolved_at', 'resolution_source', 'latest_reason'
        ])
        return Response(RiskActionItemSerializer(action).data)

    @action(detail=True, methods=['post'])
    def update_handler(self, request, pk=None):
        action = self.get_object()
        handler_id = request.data.get('handler_id')
        handler_note = request.data.get('handler_note', '')

        if handler_id:
            action.handler = Member.objects.filter(id=handler_id).first()
        if handler_note:
            action.handler_note = handler_note
        action.save(update_fields=['handler', 'handler_note'])
        return Response(RiskActionItemSerializer(action).data)

    @action(detail=False, methods=['get'])
    def active_risks(self, request):
        queryset = self.get_queryset().filter(status='pending')
        return Response(RiskActionItemSerializer(queryset, many=True).data)

    @action(detail=False, methods=['get'])
    def history_risks(self, request):
        queryset = self.get_queryset().exclude(status='pending')
        return Response(RiskActionItemSerializer(queryset, many=True).data)


class StatisticsView(APIView):
    def get(self, request):
        data = {}

        rehearsal_counts = Rehearsal.objects.values(
            prog_name=F('program__name'),
            prog_id=F('program_id')
        ).annotate(
            count=Count('id')
        ).order_by('-count')
        rehearsal_list = []
        for item in rehearsal_counts:
            rehearsal_list.append({
                'program_id': item['prog_id'],
                'program_name': item['prog_name'],
                'count': item['count']
            })
        data['program_rehearsal_counts'] = rehearsal_list

        understudy_frequency = UnderstudyChange.objects.values(
            prog_name=F('original_assignment__aria__program__name'),
            prog_id=F('original_assignment__aria__program_id')
        ).annotate(
            count=Count('id')
        ).order_by('-count')
        understudy_list = []
        for item in understudy_frequency:
            understudy_list.append({
                'program_id': item['prog_id'],
                'program_name': item['prog_name'],
                'count': item['count']
            })
        data['understudy_frequency'] = understudy_list

        error_issues = defaultdict(lambda: {'start_beat': 0, 'forgotten_lines': 0, 'total': 0})
        feedbacks = RehearsalFeedback.objects.select_related('aria')
        for fb in feedbacks:
            key = f'{fb.aria.id}'
            if fb.start_beat_issue:
                error_issues[key]['start_beat'] += 1
                error_issues[key]['total'] += 1
            if fb.forgotten_lines:
                error_issues[key]['forgotten_lines'] += 1
                error_issues[key]['total'] += 1

        sorted_errors = sorted(
            [{'aria_id': int(k), **v} for k, v in error_issues.items()],
            key=lambda x: x['total'],
            reverse=True
        )[:10]

        aria_ids = [e['aria_id'] for e in sorted_errors]
        arias = Aria.objects.filter(id__in=aria_ids).values('id', 'name')
        aria_map = {a['id']: a['name'] for a in arias}
        for e in sorted_errors:
            e['aria_name'] = aria_map.get(e['aria_id'], 'Unknown')
        data['frequent_error_arias'] = sorted_errors

        thirty_days_ago = timezone.now() - timedelta(days=30)
        member_activity = Member.objects.annotate(
            assignment_count=Count('assignments', filter=Q(assignments__created_at__gte=thirty_days_ago)),
            feedback_count=Count('feedbacks', filter=Q(feedbacks__created_at__gte=thirty_days_ago)),
            understudy_count=Count('substitute_changes', filter=Q(substitute_changes__created_at__gte=thirty_days_ago))
        ).values(
            'id', 'name', 'assignment_count', 'feedback_count', 'understudy_count'
        ).order_by('-assignment_count', '-feedback_count')
        data['member_activity'] = list(member_activity)

        data['total_programs'] = Program.objects.count()
        data['total_arias'] = Aria.objects.count()
        data['total_members'] = Member.objects.count()
        data['total_rehearsals'] = Rehearsal.objects.count()
        data['total_assignments'] = AriaAssignment.objects.count()

        status_counts = Program.objects.values('status').annotate(count=Count('id'))
        data['program_status_distribution'] = {
            item['status']: item['count'] for item in status_counts
        }

        open_checks = RehearsalCheck.objects.filter(status='open').select_related('program')
        open_check_list = list(open_checks)
        risk_aria_total = 0
        flag_counter = defaultdict(int)
        program_risk = defaultdict(lambda: {'program_id': None, 'program_name': '', 'risk_aria_count': 0, 'open_check_count': 0})
        for check in open_check_list:
            prog_key = check.program_id
            program_risk[prog_key]['program_id'] = prog_key
            program_risk[prog_key]['program_name'] = check.program.name
            program_risk[prog_key]['open_check_count'] += 1
            for item in check.items.prefetch_related('confirmations').all():
                flags = compute_risk_flags(item)
                if flags:
                    risk_aria_total += 1
                    program_risk[prog_key]['risk_aria_count'] += 1
                    for flag in flags:
                        flag_counter[flag] += 1

        risk_action_breakdown = RiskActionItem.objects.values('action_type').annotate(
            count=Count('id')
        ).order_by('-count')
        pending_risk_actions = RiskActionItem.objects.filter(status='pending').count()

        unresolved_risks = RiskActionItem.objects.filter(status='pending').count()
        resolved_risks = RiskActionItem.objects.exclude(status='pending').count()
        total_risks = unresolved_risks + resolved_risks
        overall_resolution_rate = (resolved_risks / total_risks * 100) if total_risks > 0 else 0

        avg_processing_time = RiskActionItem.objects.filter(
            resolved_at__isnull=False,
            created_at__isnull=False
        ).exclude(
            status='pending'
        ).annotate(
            duration=ExpressionWrapper(
                F('resolved_at') - F('created_at'),
                output_field=DurationField()
            )
        ).aggregate(avg_duration=Avg('duration'))

        avg_hours = None
        if avg_processing_time['avg_duration']:
            avg_hours = round(avg_processing_time['avg_duration'].total_seconds() / 3600, 2)

        program_risk_stats = defaultdict(lambda: {
            'program_id': None,
            'program_name': '',
            'total_risks': 0,
            'resolved_risks': 0,
            'unresolved_risks': 0,
            'resolution_rate': 0,
            'avg_processing_hours': None,
            'processing_times': []
        })

        all_resolved_risks = RiskActionItem.objects.filter(
            resolved_at__isnull=False
        ).select_related('check_item__aria__program', 'handler')

        for risk in all_resolved_risks:
            program_id = risk.check_item.aria.program_id
            program_name = risk.check_item.aria.program.name
            key = program_id
            program_risk_stats[key]['program_id'] = program_id
            program_risk_stats[key]['program_name'] = program_name
            program_risk_stats[key]['total_risks'] += 1
            if risk.status == 'pending':
                program_risk_stats[key]['unresolved_risks'] += 1
            else:
                program_risk_stats[key]['resolved_risks'] += 1
                if risk.created_at and risk.resolved_at:
                    hours = (risk.resolved_at - risk.created_at).total_seconds() / 3600
                    program_risk_stats[key]['processing_times'].append(hours)

        all_pending_risks = RiskActionItem.objects.filter(
            status='pending'
        ).select_related('check_item__aria__program')

        for risk in all_pending_risks:
            program_id = risk.check_item.aria.program_id
            program_name = risk.check_item.aria.program.name
            key = program_id
            program_risk_stats[key]['program_id'] = program_id
            program_risk_stats[key]['program_name'] = program_name
            program_risk_stats[key]['total_risks'] += 1
            program_risk_stats[key]['unresolved_risks'] += 1

        for key in program_risk_stats:
            stat = program_risk_stats[key]
            if stat['total_risks'] > 0:
                stat['resolution_rate'] = round(stat['resolved_risks'] / stat['total_risks'] * 100, 2)
            if stat['processing_times']:
                stat['avg_processing_hours'] = round(sum(stat['processing_times']) / len(stat['processing_times']), 2)
            del stat['processing_times']

        thirty_days_ago = timezone.now() - timedelta(days=30)
        risk_type_trend = RiskActionItem.objects.filter(
            created_at__gte=thirty_days_ago
        ).values('action_type').annotate(
            count=Count('id')
        ).order_by('-count')

        daily_risk_trend = []
        for i in range(30):
            day_start = timezone.now() - timedelta(days=30 - i)
            day_end = day_start + timedelta(days=1)
            day_start = day_start.replace(hour=0, minute=0, second=0, microsecond=0)
            day_end = day_end.replace(hour=0, minute=0, second=0, microsecond=0)

            created_count = RiskActionItem.objects.filter(
                created_at__gte=day_start,
                created_at__lt=day_end
            ).count()

            resolved_count = RiskActionItem.objects.filter(
                resolved_at__gte=day_start,
                resolved_at__lt=day_end
            ).exclude(status='pending').count()

            daily_risk_trend.append({
                'date': day_start.strftime('%Y-%m-%d'),
                'created': created_count,
                'resolved': resolved_count
            })

        resolution_source_breakdown = RiskActionItem.objects.filter(
            resolution_source__isnull=False
        ).values('resolution_source').annotate(
            count=Count('id')
        ).order_by('-count')

        data['pre_performance_risk'] = {
            'open_check_count': len(open_check_list),
            'risk_aria_count': risk_aria_total,
            'pending_risk_actions': pending_risk_actions,
            'flag_breakdown': [
                {'action_type': flag, 'label': RISK_FLAG_LABELS.get(flag, flag), 'count': flag_counter[flag]}
                for flag in ['attendance', 'understudy', 'feedback', 'accompaniment', 'teacher_risk']
                if flag_counter[flag] > 0
            ],
            'risk_action_breakdown': [
                {'action_type': item['action_type'], 'label': dict(RiskActionItem.ACTION_TYPE_CHOICES).get(item['action_type'], item['action_type']), 'count': item['count']}
                for item in risk_action_breakdown
            ],
            'program_risk': sorted(program_risk.values(), key=lambda x: x['risk_aria_count'], reverse=True),
        }

        data['risk_closure_stats'] = {
            'total_risks': total_risks,
            'unresolved_risks': unresolved_risks,
            'resolved_risks': resolved_risks,
            'overall_resolution_rate': round(overall_resolution_rate, 2),
            'avg_processing_hours': avg_hours,
            'program_risk_stats': sorted(
                program_risk_stats.values(),
                key=lambda x: x['resolution_rate'],
                reverse=True
            ),
            'risk_type_trend': [
                {
                    'action_type': item['action_type'],
                    'label': dict(RiskActionItem.ACTION_TYPE_CHOICES).get(item['action_type'], item['action_type']),
                    'count': item['count']
                }
                for item in risk_type_trend
            ],
            'daily_risk_trend': daily_risk_trend,
            'resolution_source_breakdown': [
                {
                    'source': item['resolution_source'],
                    'label': dict(RiskActionItem.RESOLUTION_SOURCE_CHOICES).get(item['resolution_source'], item['resolution_source']),
                    'count': item['count']
                }
                for item in resolution_source_breakdown
            ]
        }

        return Response(data)


class AutoAssignView(APIView):
    def post(self, request):
        serializer = AutoAssignRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        program_id = serializer.validated_data['program_id']
        rehearsal_date = serializer.validated_data.get('rehearsal_date')

        try:
            program = Program.objects.get(id=program_id)
        except Program.DoesNotExist:
            return Response({'error': '节目不存在'}, status=status.HTTP_404_NOT_FOUND)

        arias = Aria.objects.filter(program=program).order_by('order_index')
        members = Member.objects.all()

        existing_assignments = AriaAssignment.objects.filter(
            aria__program=program,
            status='confirmed'
        ).select_related('member', 'aria')
        assigned_pairs = set(
            (a.aria_id, a.member_id, a.is_understudy)
            for a in existing_assignments
        )

        results = []

        for aria in arias:
            candidates = []
            aria_role_type = aria.role_type

            matching_role = Role.objects.filter(
                program=program,
                role_type=aria_role_type
            ).first()

            for member in members:
                member_roles = member.role_types.split(',') if member.role_types else []

                match_score = 0

                if aria_role_type in member_roles:
                    match_score += 50

                if rehearsal_date:
                    date_str = rehearsal_date.strftime('%Y-%m-%d')
                    available = member.available_times.get(date_str, [])
                    if available:
                        match_score += 30
                else:
                    match_score += 15

                if member.is_understudy:
                    match_score += 10

                existing_count = AriaAssignment.objects.filter(
                    aria__program=program,
                    member=member,
                    status='confirmed'
                ).count()
                if existing_count == 0:
                    match_score += 10
                elif existing_count < 3:
                    match_score += 5

                if match_score > 0:
                    candidates.append({
                        'member': member,
                        'score': match_score,
                        'role': matching_role
                    })

            candidates.sort(key=lambda x: x['score'], reverse=True)

            assigned_main = False
            for candidate in candidates[:3]:
                if not assigned_main and (aria.id, candidate['member'].id, False) not in assigned_pairs:
                    results.append({
                        'aria_id': aria.id,
                        'aria_name': aria.name,
                        'member_id': candidate['member'].id,
                        'member_name': candidate['member'].name,
                        'role_id': candidate['role'].id if candidate['role'] else None,
                        'role_name': candidate['role'].name if candidate['role'] else None,
                        'is_understudy': False,
                        'match_score': candidate['score']
                    })
                    assigned_main = True
                elif candidate['member'].is_understudy and (aria.id, candidate['member'].id, True) not in assigned_pairs:
                    results.append({
                        'aria_id': aria.id,
                        'aria_name': aria.name,
                        'member_id': candidate['member'].id,
                        'member_name': candidate['member'].name,
                        'role_id': candidate['role'].id if candidate['role'] else None,
                        'role_name': candidate['role'].name if candidate['role'] else None,
                        'is_understudy': True,
                        'match_score': candidate['score']
                    })

        return Response({
            'program_id': program_id,
            'program_name': program.name,
            'rehearsal_date': rehearsal_date,
            'assignments': results,
            'total_suggestions': len(results)
        })


class ApplyAutoAssignView(APIView):
    def post(self, request):
        assignments_data = request.data.get('assignments', [])
        created_count = 0

        for assignment in assignments_data:
            aria_id = assignment.get('aria_id')
            member_id = assignment.get('member_id')
            role_id = assignment.get('role_id')
            is_understudy = assignment.get('is_understudy', False)

            if not aria_id or not member_id:
                continue

            existing = AriaAssignment.objects.filter(
                aria_id=aria_id,
                member_id=member_id,
                is_understudy=is_understudy
            ).first()

            if existing:
                continue

            AriaAssignment.objects.create(
                aria_id=aria_id,
                member_id=member_id,
                role_id=role_id,
                is_understudy=is_understudy,
                status='pending'
            )
            created_count += 1

        return Response({
            'message': f'成功创建 {created_count} 条分配记录',
            'created_count': created_count
        })
