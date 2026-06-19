from django.contrib import admin
from .models import (
    Program, Aria, Role, Member, AriaAssignment,
    Rehearsal, RehearsalFeedback, UnderstudyChange, Archive,
    RehearsalCheck, RehearsalCheckItem, RehearsalCheckConfirmation, RiskActionItem
)


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'duration', 'status', 'created_at')
    list_filter = ('status', 'type')
    search_fields = ('name', 'description')


@admin.register(Aria)
class AriaAdmin(admin.ModelAdmin):
    list_display = ('program', 'name', 'role_type', 'order_index', 'duration')
    list_filter = ('role_type', 'program')
    search_fields = ('name', 'lyrics')


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('program', 'name', 'role_type')
    list_filter = ('role_type', 'program')
    search_fields = ('name', 'description')


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'role_types', 'is_understudy', 'created_at')
    list_filter = ('is_understudy',)
    search_fields = ('name', 'phone')


@admin.register(AriaAssignment)
class AriaAssignmentAdmin(admin.ModelAdmin):
    list_display = ('aria', 'member', 'role', 'is_understudy', 'status', 'created_at')
    list_filter = ('status', 'is_understudy')
    search_fields = ('aria__name', 'member__name')


@admin.register(Rehearsal)
class RehearsalAdmin(admin.ModelAdmin):
    list_display = ('program', 'date', 'location', 'created_at')
    list_filter = ('date', 'program')
    search_fields = ('location', 'notes')


@admin.register(RehearsalFeedback)
class RehearsalFeedbackAdmin(admin.ModelAdmin):
    list_display = ('rehearsal', 'aria', 'member', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('teacher_comments', 'forgotten_lines')


@admin.register(UnderstudyChange)
class UnderstudyChangeAdmin(admin.ModelAdmin):
    list_display = ('original_assignment', 'substitute_member', 'date', 'status', 'created_at')
    list_filter = ('status', 'date')
    search_fields = ('reason',)


@admin.register(Archive)
class ArchiveAdmin(admin.ModelAdmin):
    list_display = ('program', 'version', 'created_at')
    list_filter = ('program',)
    search_fields = ('version',)


class RehearsalCheckItemInline(admin.TabularInline):
    model = RehearsalCheckItem
    extra = 0
    readonly_fields = ('aria', 'order_index', 'role_type', 'latest_feedback_date')
    fields = ('aria', 'order_index', 'role_type', 'accompaniment_required', 'accompaniment_confirmed',
              'risk_level', 'teacher_comment', 'risk_action_created', 'latest_feedback_date',
              'latest_start_beat_issue', 'latest_forgotten_lines')


@admin.register(RehearsalCheck)
class RehearsalCheckAdmin(admin.ModelAdmin):
    list_display = ('program', 'name', 'planned_performance_date', 'status', 'created_at')
    list_filter = ('status', 'program')
    search_fields = ('name', 'notes')
    inlines = [RehearsalCheckItemInline]


@admin.register(RehearsalCheckItem)
class RehearsalCheckItemAdmin(admin.ModelAdmin):
    list_display = ('rehearsal_check', 'aria', 'order_index', 'accompaniment_confirmed', 'risk_level', 'risk_action_created')
    list_filter = ('risk_level', 'accompaniment_confirmed')
    search_fields = ('aria__name', 'teacher_comment')


class RehearsalCheckConfirmationInline(admin.TabularInline):
    model = RehearsalCheckConfirmation
    extra = 0


@admin.register(RehearsalCheckConfirmation)
class RehearsalCheckConfirmationAdmin(admin.ModelAdmin):
    list_display = ('check_item', 'member', 'is_understudy', 'attendance_confirmed', 'lyrics_proficiency', 'needs_understudy_help')
    list_filter = ('is_understudy', 'attendance_confirmed', 'lyrics_proficiency')
    search_fields = ('member__name',)


@admin.register(RiskActionItem)
class RiskActionItemAdmin(admin.ModelAdmin):
    list_display = ('check_item', 'action_type', 'status', 'created_at', 'resolved_at')
    list_filter = ('action_type', 'status')
    search_fields = ('description',)
