from django.db.models import Count, Q, F
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
    Rehearsal, RehearsalFeedback, UnderstudyChange, Archive
)
from .serializers import (
    ProgramSerializer, AriaSerializer, RoleSerializer, MemberSerializer,
    AriaAssignmentSerializer, RehearsalSerializer, RehearsalFeedbackSerializer,
    UnderstudyChangeSerializer, ArchiveSerializer,
    AutoAssignRequestSerializer, AutoAssignResultSerializer
)


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
