from rest_framework import serializers
from .models import (
    Program, Aria, Role, Member, AriaAssignment,
    Rehearsal, RehearsalFeedback, UnderstudyChange, Archive
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
