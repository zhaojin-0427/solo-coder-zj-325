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
