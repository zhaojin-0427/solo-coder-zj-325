from django.db import models


class Program(models.Model):
    STATUS_CHOICES = [
        ('planning', '筹备'),
        ('rehearsing', '排练'),
        ('performing', '演出'),
        ('archived', '归档'),
    ]
    TYPE_CHOICES = [
        ('beijing', '京剧'),
        ('henan', '豫剧'),
        ('kunqu', '昆曲'),
        ('yue', '越剧'),
        ('huangmei', '黄梅戏'),
        ('other', '其他'),
    ]
    name = models.CharField(max_length=200, verbose_name='节目名称')
    description = models.TextField(blank=True, verbose_name='节目描述')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='beijing', verbose_name='剧种')
    duration = models.IntegerField(help_text='分钟', verbose_name='总时长')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning', verbose_name='状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        ordering = ['-created_at']
        verbose_name = '节目'
        verbose_name_plural = '节目'

    def __str__(self):
        return self.name


class Aria(models.Model):
    ROLE_TYPE_CHOICES = [
        ('sheng', '生'),
        ('dan', '旦'),
        ('jing', '净'),
        ('mo', '末'),
        ('chou', '丑'),
    ]
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='arias', verbose_name='所属节目')
    name = models.CharField(max_length=200, verbose_name='唱段名称')
    lyrics = models.TextField(blank=True, verbose_name='歌词')
    order_index = models.IntegerField(verbose_name='演出顺序')
    duration = models.IntegerField(help_text='秒', verbose_name='唱段时长')
    role_type = models.CharField(max_length=20, choices=ROLE_TYPE_CHOICES, verbose_name='行当')
    accompaniment_required = models.TextField(blank=True, verbose_name='伴奏需求')

    class Meta:
        ordering = ['program', 'order_index']
        unique_together = ['program', 'order_index']
        verbose_name = '唱段'
        verbose_name_plural = '唱段'

    def __str__(self):
        return f'{self.program.name} - {self.name}'


class Role(models.Model):
    ROLE_TYPE_CHOICES = [
        ('sheng', '生'),
        ('dan', '旦'),
        ('jing', '净'),
        ('mo', '末'),
        ('chou', '丑'),
    ]
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='roles', verbose_name='所属节目')
    name = models.CharField(max_length=100, verbose_name='角色名称')
    role_type = models.CharField(max_length=20, choices=ROLE_TYPE_CHOICES, verbose_name='行当')
    description = models.TextField(blank=True, verbose_name='角色描述')

    class Meta:
        ordering = ['program', 'name']
        verbose_name = '角色'
        verbose_name_plural = '角色'

    def __str__(self):
        return f'{self.program.name} - {self.name}'


class Member(models.Model):
    ROLE_TYPE_CHOICES = [
        ('sheng', '生'),
        ('dan', '旦'),
        ('jing', '净'),
        ('mo', '末'),
        ('chou', '丑'),
    ]
    name = models.CharField(max_length=100, verbose_name='姓名')
    phone = models.CharField(max_length=20, verbose_name='联系电话')
    role_types = models.CharField(max_length=100, verbose_name='擅长行当')
    available_times = models.JSONField(default=dict, verbose_name='可排练时段')
    is_understudy = models.BooleanField(default=False, verbose_name='是否愿意替补')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        ordering = ['-created_at']
        verbose_name = '成员'
        verbose_name_plural = '成员'

    def __str__(self):
        return self.name

    def get_role_types_display(self):
        type_map = dict(self.ROLE_TYPE_CHOICES)
        types = self.role_types.split(',') if self.role_types else []
        return [type_map.get(t, t) for t in types]


class AriaAssignment(models.Model):
    STATUS_CHOICES = [
        ('confirmed', '确认'),
        ('pending', '待确认'),
        ('rejected', '拒绝'),
    ]
    aria = models.ForeignKey(Aria, on_delete=models.CASCADE, related_name='assignments', verbose_name='唱段')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='assignments', verbose_name='成员')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, related_name='assignments', verbose_name='角色')
    is_understudy = models.BooleanField(default=False, verbose_name='是否替补')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='分配时间')

    class Meta:
        ordering = ['-created_at']
        verbose_name = '唱段分配'
        verbose_name_plural = '唱段分配'

    def __str__(self):
        return f'{self.member.name} - {self.aria.name}'


class Rehearsal(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='rehearsals', verbose_name='所属节目')
    date = models.DateField(verbose_name='排练日期')
    location = models.CharField(max_length=200, verbose_name='排练地点')
    notes = models.TextField(blank=True, verbose_name='排练备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        ordering = ['-date']
        verbose_name = '排练记录'
        verbose_name_plural = '排练记录'

    def __str__(self):
        return f'{self.program.name} - {self.date}'


class RehearsalFeedback(models.Model):
    rehearsal = models.ForeignKey(Rehearsal, on_delete=models.CASCADE, related_name='feedbacks', verbose_name='排练记录')
    aria = models.ForeignKey(Aria, on_delete=models.CASCADE, related_name='feedbacks', verbose_name='唱段')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='feedbacks', verbose_name='成员')
    audio_url = models.URLField(blank=True, verbose_name='录音链接')
    start_beat_issue = models.TextField(blank=True, verbose_name='起板问题')
    forgotten_lines = models.TextField(blank=True, verbose_name='忘词片段')
    teacher_comments = models.TextField(blank=True, verbose_name='老师点评')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        ordering = ['-created_at']
        verbose_name = '排练反馈'
        verbose_name_plural = '排练反馈'

    def __str__(self):
        return f'{self.rehearsal.date} - {self.aria.name} - {self.member.name}'


class UnderstudyChange(models.Model):
    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('approved', '已批准'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
        ('rejected', '已拒绝'),
    ]
    original_assignment = models.ForeignKey(AriaAssignment, on_delete=models.CASCADE, related_name='understudy_changes', verbose_name='原分配')
    substitute_member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='substitute_changes', verbose_name='替补成员')
    reason = models.TextField(verbose_name='调整原因')
    date = models.DateField(verbose_name='调整日期')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        ordering = ['-created_at']
        verbose_name = '替补调整记录'
        verbose_name_plural = '替补调整记录'

    def __str__(self):
        return f'{self.original_assignment.member.name} → {self.substitute_member.name}'


class Archive(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='archives', verbose_name='所属节目')
    version = models.CharField(max_length=50, verbose_name='版本号')
    final_assignments = models.JSONField(default=dict, verbose_name='最终分配记录')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='归档时间')

    class Meta:
        ordering = ['-created_at']
        verbose_name = '版本归档'
        verbose_name_plural = '版本归档'

    def __str__(self):
        return f'{self.program.name} - v{self.version}'


class RehearsalCheck(models.Model):
    STATUS_CHOICES = [
        ('open', '进行中'),
        ('closed', '已关闭'),
    ]
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='rehearsal_checks', verbose_name='所属节目')
    name = models.CharField(max_length=200, verbose_name='批次名称')
    planned_performance_date = models.DateField(null=True, blank=True, verbose_name='计划演出日期')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open', verbose_name='状态')
    notes = models.TextField(blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        ordering = ['-created_at']
        verbose_name = '联排确认批次'
        verbose_name_plural = '联排确认批次'

    def __str__(self):
        return f'{self.program.name} - {self.name}'


class RehearsalCheckItem(models.Model):
    RISK_CHOICES = [
        ('none', '无风险'),
        ('low', '低'),
        ('medium', '中'),
        ('high', '高'),
    ]
    ROLE_TYPE_CHOICES = Aria.ROLE_TYPE_CHOICES
    rehearsal_check = models.ForeignKey(RehearsalCheck, on_delete=models.CASCADE, related_name='items', verbose_name='联排批次')
    aria = models.ForeignKey(Aria, on_delete=models.CASCADE, related_name='rehearsal_check_items', verbose_name='唱段')
    order_index = models.IntegerField(verbose_name='唱段顺序快照')
    role_type = models.CharField(max_length=20, choices=ROLE_TYPE_CHOICES, verbose_name='行当快照')
    accompaniment_required = models.TextField(blank=True, verbose_name='伴奏需求快照')
    accompaniment_confirmed = models.BooleanField(default=False, verbose_name='伴奏已备齐')
    accompaniment_confirmed_by = models.ForeignKey(
        Member, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='accompaniment_confirmations', verbose_name='伴奏确认人'
    )
    risk_level = models.CharField(max_length=20, choices=RISK_CHOICES, default='none', verbose_name='风险等级')
    teacher_comment = models.TextField(blank=True, verbose_name='处理意见')
    risk_action_created = models.BooleanField(default=False, verbose_name='已生成待处理项')
    latest_feedback_date = models.DateField(null=True, blank=True, verbose_name='最近反馈日期')
    latest_start_beat_issue = models.TextField(blank=True, verbose_name='最近起板问题')
    latest_forgotten_lines = models.TextField(blank=True, verbose_name='最近忘词片段')
    latest_teacher_comments = models.TextField(blank=True, verbose_name='最近老师点评')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        ordering = ['rehearsal_check', 'order_index']
        unique_together = ['rehearsal_check', 'aria']
        verbose_name = '联排确认清单项'
        verbose_name_plural = '联排确认清单项'

    def __str__(self):
        return f'{self.rehearsal_check.name} - {self.aria.name}'


class RehearsalCheckConfirmation(models.Model):
    LYRICS_CHOICES = [
        ('unconfirmed', '未确认'),
        ('familiar', '熟练'),
        ('needs_practice', '需练习'),
    ]
    check_item = models.ForeignKey(RehearsalCheckItem, on_delete=models.CASCADE, related_name='confirmations', verbose_name='清单项')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='rehearsal_confirmations', verbose_name='成员')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, related_name='rehearsal_confirmations', verbose_name='角色')
    role_name = models.CharField(max_length=100, blank=True, verbose_name='角色名称快照')
    is_understudy = models.BooleanField(default=False, verbose_name='是否替补')
    attendance_confirmed = models.BooleanField(default=False, verbose_name='到场确认')
    lyrics_proficiency = models.CharField(max_length=20, choices=LYRICS_CHOICES, default='unconfirmed', verbose_name='歌词熟练度')
    needs_understudy_help = models.BooleanField(default=False, verbose_name='需要替补协助')
    note = models.TextField(blank=True, verbose_name='备注')
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name='确认时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        ordering = ['check_item', 'is_understudy', 'id']
        unique_together = ['check_item', 'member']
        verbose_name = '联排确认记录'
        verbose_name_plural = '联排确认记录'

    def __str__(self):
        return f'{self.check_item.aria.name} - {self.member.name}'


class RiskActionItem(models.Model):
    ACTION_TYPE_CHOICES = [
        ('attendance', '未确认到场'),
        ('understudy', '无替补'),
        ('feedback', '排练反馈问题'),
        ('accompaniment', '伴奏未确认'),
        ('teacher_risk', '老师标注风险'),
    ]
    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('auto_resolved', '自动解除'),
        ('manually_resolved', '手动解除'),
        ('confirmed_closed', '管理员确认关闭'),
    ]
    RESOLUTION_SOURCE_CHOICES = [
        ('attendance_confirm', '成员到场确认'),
        ('lyrics_update', '歌词熟练度更新'),
        ('accompaniment_confirm', '伴奏确认'),
        ('teacher_risk_adjust', '老师风险等级调整'),
        ('feedback_clear', '排练反馈问题清除'),
        ('understudy_add', '替补成员添加'),
        ('manual_close', '管理员手动处理'),
        ('system_auto', '系统自动复核'),
    ]
    check_item = models.ForeignKey(RehearsalCheckItem, on_delete=models.CASCADE, related_name='risk_actions', verbose_name='清单项')
    action_type = models.CharField(max_length=20, choices=ACTION_TYPE_CHOICES, verbose_name='待处理类型')
    description = models.TextField(verbose_name='描述')
    latest_reason = models.TextField(blank=True, verbose_name='最新风险原因')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    handler = models.ForeignKey(
        Member, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='handled_risk_actions', verbose_name='处理人'
    )
    handler_note = models.TextField(blank=True, verbose_name='处理备注')
    resolution_source = models.CharField(
        max_length=30, choices=RESOLUTION_SOURCE_CHOICES,
        null=True, blank=True, verbose_name='解除来源'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    resolved_at = models.DateTimeField(null=True, blank=True, verbose_name='处理时间')
    last_reviewed_at = models.DateTimeField(null=True, blank=True, verbose_name='最近复核时间')
    auto_resolve_pending = models.BooleanField(default=False, verbose_name='待管理员确认解除')
    auto_resolve_suggested_at = models.DateTimeField(null=True, blank=True, verbose_name='建议解除时间')

    class Meta:
        ordering = ['-created_at']
        unique_together = ['check_item', 'action_type']
        verbose_name = '风险待处理项'
        verbose_name_plural = '风险待处理项'

    def __str__(self):
        return f'{self.check_item.aria.name} - {self.get_action_type_display()}'

    def is_active(self):
        return self.status == 'pending'
