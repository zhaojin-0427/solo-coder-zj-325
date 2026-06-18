from django.contrib import admin
from .models import (
    Program, Aria, Role, Member, AriaAssignment,
    Rehearsal, RehearsalFeedback, UnderstudyChange, Archive
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
