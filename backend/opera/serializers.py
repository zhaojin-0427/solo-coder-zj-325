from rest_framework import serializers
from .models import (
    Program, Aria, Role, Member, AriaAssignment,
    Rehearsal, RehearsalFeedback, UnderstudyChange, Archive,
    RehearsalCheck, RehearsalCheckItem, RehearsalCheckConfirmation, RiskActionItem
)


class ProgramSerializer(serializers.ModelSerializer):
    aria_count = serializers.IntegerField(read_only=True, required=False)
    rehearsal_count = serializers.IntegerField(read_only=True, required=False)
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Program
        fields = '__all__'


class AriaSerializer(serializers.ModelSerializer):
    program_name = serializers.CharField(source='program.name', read_only=True)
    role_type_display = serializers.CharField(source='get_role_type_display', read_only=True)

    class Meta:
        model = Aria
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    program_name = serializers.CharField(source='program.name', read_only=True)
    role_type_display = serializers.CharField(source='get_role_type_display', read_only=True)

    class Meta:
        model = Role
        fields = '__all__'


class MemberSerializer(serializers.ModelSerializer):
    role_types_display = serializers.SerializerMethodField()
    assignment_count = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = Member
        fields = '__all__'

    def get_role_types_display(self, obj):
        return obj.get_role_types_display()


class AriaAssignmentSerializer(serializers.ModelSerializer):
    aria_name = serializers.CharField(source='aria.name', read_only=True)
    member_name = serializers.CharField(source='member.name', read_only=True)
    role_name = serializers.CharField(source='role.name', read_only=True, allow_null=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = AriaAssignment
        fields = '__all__'


class RehearsalSerializer(serializers.ModelSerializer):
    program_name = serializers.CharField(source='program.name', read_only=True)
    feedback_count = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = Rehearsal
        fields = '__all__'


class RehearsalFeedbackSerializer(serializers.ModelSerializer):
    rehearsal_date = serializers.DateField(source='rehearsal.date', read_only=True)
    aria_name = serializers.CharField(source='aria.name', read_only=True)
    member_name = serializers.CharField(source='member.name', read_only=True)

    class Meta:
        model = RehearsalFeedback
        fields = '__all__'


class UnderstudyChangeSerializer(serializers.ModelSerializer):
    original_member_name = serializers.CharField(source='original_assignment.member.name', read_only=True)
    substitute_member_name = serializers.CharField(source='substitute_member.name', read_only=True)
    aria_name = serializers.CharField(source='original_assignment.aria.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = UnderstudyChange
        fields = '__all__'


class ArchiveSerializer(serializers.ModelSerializer):
    program_name = serializers.CharField(source='program.name', read_only=True)

    class Meta:
        model = Archive
        fields = '__all__'


class AutoAssignRequestSerializer(serializers.Serializer):
    program_id = serializers.IntegerField()
    rehearsal_date = serializers.DateField(required=False, allow_null=True)


class AutoAssignResultSerializer(serializers.Serializer):
    aria_id = serializers.IntegerField()
    aria_name = serializers.CharField()
    member_id = serializers.IntegerField()
    member_name = serializers.CharField()
    role_id = serializers.IntegerField(allow_null=True)
    role_name = serializers.CharField(allow_null=True)
    is_understudy = serializers.BooleanField()
    match_score = serializers.IntegerField()


RISK_FLAG_LABELS = {
    'attendance': '未确认到场',
    'understudy': '无替补',
    'feedback': '排练反馈问题',
    'accompaniment': '伴奏未确认',
    'teacher_risk': '老师标注风险',
}


def compute_risk_flags(item):
    flags = []
    confirmations = list(item.confirmations.all())
    has_confirmations = len(confirmations) > 0
    has_understudy = any(c.is_understudy for c in confirmations)

    if has_confirmations and any(not c.attendance_confirmed for c in confirmations):
        flags.append('attendance')
    if not has_understudy:
        flags.append('understudy')
    if item.latest_start_beat_issue or item.latest_forgotten_lines:
        flags.append('feedback')
    if not item.accompaniment_confirmed:
        flags.append('accompaniment')
    if item.risk_level in ('medium', 'high'):
        flags.append('teacher_risk')
    return flags


class RehearsalCheckConfirmationSerializer(serializers.ModelSerializer):
    member_name = serializers.CharField(source='member.name', read_only=True)
    lyrics_proficiency_display = serializers.CharField(source='get_lyrics_proficiency_display', read_only=True)

    class Meta:
        model = RehearsalCheckConfirmation
        fields = '__all__'


class RiskActionItemSerializer(serializers.ModelSerializer):
    action_type_display = serializers.CharField(source='get_action_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    aria_name = serializers.CharField(source='check_item.aria.name', read_only=True)
    aria_id = serializers.IntegerField(source='check_item.aria_id', read_only=True)
    rehearsal_check = serializers.IntegerField(source='check_item.rehearsal_check_id', read_only=True)
    order_index = serializers.IntegerField(source='check_item.order_index', read_only=True)

    class Meta:
        model = RiskActionItem
        fields = '__all__'


class RehearsalCheckItemSerializer(serializers.ModelSerializer):
    aria_name = serializers.CharField(source='aria.name', read_only=True)
    aria_id = serializers.IntegerField(read_only=True)
    role_type_display = serializers.SerializerMethodField()
    risk_level_display = serializers.CharField(source='get_risk_level_display', read_only=True)
    accompaniment_confirmed_by_name = serializers.CharField(source='accompaniment_confirmed_by.name', read_only=True, allow_null=True)
    confirmations = RehearsalCheckConfirmationSerializer(many=True, read_only=True)
    risk_flags = serializers.SerializerMethodField()
    risk_score = serializers.SerializerMethodField()
    has_understudy = serializers.SerializerMethodField()

    class Meta:
        model = RehearsalCheckItem
        fields = '__all__'

    def get_role_type_display(self, obj):
        type_map = dict(Aria.ROLE_TYPE_CHOICES)
        return type_map.get(obj.role_type, obj.role_type)

    def get_risk_flags(self, obj):
        return compute_risk_flags(obj)

    def get_risk_score(self, obj):
        return len(compute_risk_flags(obj))

    def get_has_understudy(self, obj):
        return obj.confirmations.filter(is_understudy=True).exists()


class RehearsalCheckSerializer(serializers.ModelSerializer):
    program_name = serializers.CharField(source='program.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    item_count = serializers.SerializerMethodField()
    risk_aria_count = serializers.SerializerMethodField()

    class Meta:
        model = RehearsalCheck
        fields = '__all__'

    def get_item_count(self, obj):
        return obj.items.count()

    def get_risk_aria_count(self, obj):
        count = 0
        for item in obj.items.all():
            if compute_risk_flags(item):
                count += 1
        return count
