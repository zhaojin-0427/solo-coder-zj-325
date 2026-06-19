from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
import json

from opera.models import (
    Program, Aria, Role, Member, AriaAssignment,
    Rehearsal, RehearsalFeedback, UnderstudyChange, Archive,
    RehearsalCheck, RehearsalCheckItem, RehearsalCheckConfirmation, RiskActionItem
)


class Command(BaseCommand):
    help = '初始化戏曲票友平台测试数据'

    def handle(self, *args, **options):
        self.stdout.write('开始初始化测试数据...')

        Program.objects.all().delete()
        Aria.objects.all().delete()
        Role.objects.all().delete()
        Member.objects.all().delete()
        AriaAssignment.objects.all().delete()
        Rehearsal.objects.all().delete()
        RehearsalFeedback.objects.all().delete()
        UnderstudyChange.objects.all().delete()
        Archive.objects.all().delete()
        RehearsalCheck.objects.all().delete()
        RehearsalCheckItem.objects.all().delete()
        RehearsalCheckConfirmation.objects.all().delete()
        RiskActionItem.objects.all().delete()

        programs_data = [
            {
                'name': '锁麟囊',
                'description': '京剧程派经典剧目，讲述富家小姐薛湘灵在富贵无常的人世中，如何因当年的仗义助人而得报恩和救助的感人故事。',
                'type': 'beijing',
                'duration': 150,
                'status': 'rehearsing',
            },
            {
                'name': '穆桂英挂帅',
                'description': '豫剧经典剧目，讲述北宋时期，西夏犯境，佘太君派遣曾孙杨文广、曾孙女杨金花回京探事，文广在校场刀劈王伦，夺得帅印。穆桂英深明大义，以国事为重，挂帅出征的故事。',
                'type': 'henan',
                'duration': 120,
                'status': 'planning',
            },
            {
                'name': '牡丹亭',
                'description': '昆曲经典剧目，讲述杜丽娘与柳梦梅的爱情故事。',
                'type': 'kunqu',
                'duration': 180,
                'status': 'performing',
            },
            {
                'name': '天仙配',
                'description': '黄梅戏经典剧目，讲述七仙女与董永的爱情故事。',
                'type': 'huangmei',
                'duration': 110,
                'status': 'archived',
            },
        ]

        programs = []
        for prog_data in programs_data:
            prog = Program.objects.create(**prog_data)
            programs.append(prog)
            self.stdout.write(f'  创建节目: {prog.name}')

        arias_data = {
            '锁麟囊': [
                {'name': '春秋亭外风雨暴', 'lyrics': '春秋亭外风雨暴，何处悲声破寂寥...', 'order_index': 1, 'duration': 240, 'role_type': 'dan', 'accompaniment_required': '京胡、月琴、三弦'},
                {'name': '一霎时把七情俱已昧尽', 'lyrics': '一霎时把七情俱已昧尽，参透了酸辛处泪湿衣襟...', 'order_index': 2, 'duration': 320, 'role_type': 'dan', 'accompaniment_required': '京胡、二胡、月琴'},
                {'name': '这才是今生难预料', 'lyrics': '这才是今生难预料，不想团圆在今朝...', 'order_index': 3, 'duration': 180, 'role_type': 'dan', 'accompaniment_required': '京胡、月琴'},
                {'name': '当日里好风光忽觉转变', 'lyrics': '当日里好风光忽觉转变，霎时间日色淡似坠西山...', 'order_index': 4, 'duration': 260, 'role_type': 'sheng', 'accompaniment_required': '京胡、三弦'},
            ],
            '穆桂英挂帅': [
                {'name': '辕门外三声炮如同雷震', 'lyrics': '辕门外三声炮如同雷震，天波府里走出来我保国臣...', 'order_index': 1, 'duration': 280, 'role_type': 'dan', 'accompaniment_required': '板胡、二胡、琵琶'},
                {'name': '猛听得金鼓响画角声震', 'lyrics': '猛听得金鼓响画角声震，唤起我破天门壮志凌云...', 'order_index': 2, 'duration': 220, 'role_type': 'dan', 'accompaniment_required': '板胡、月琴'},
                {'name': '威风凛凛出府门', 'lyrics': '威风凛凛出府门，我去到校场选能人...', 'order_index': 3, 'duration': 200, 'role_type': 'sheng', 'accompaniment_required': '板胡、三弦'},
                {'name': '老身祖居在河东', 'lyrics': '老身祖居在河东，佘氏太君受皇封...', 'order_index': 4, 'duration': 240, 'role_type': 'jing', 'accompaniment_required': '板胡、大锣'},
            ],
            '牡丹亭': [
                {'name': '原来姹紫嫣红开遍', 'lyrics': '原来姹紫嫣红开遍，似这般都付与断井颓垣...', 'order_index': 1, 'duration': 300, 'role_type': 'dan', 'accompaniment_required': '曲笛、三弦、琵琶'},
                {'name': '良辰美景奈何天', 'lyrics': '良辰美景奈何天，赏心乐事谁家院...', 'order_index': 2, 'duration': 260, 'role_type': 'dan', 'accompaniment_required': '曲笛、箫'},
                {'name': '则为你如花美眷', 'lyrics': '则为你如花美眷，似水流年...', 'order_index': 3, 'duration': 200, 'role_type': 'sheng', 'accompaniment_required': '曲笛、月琴'},
                {'name': '惊梦', 'lyrics': '那书生可意啊，咱不是晓来庭院闲凝眄...', 'order_index': 4, 'duration': 320, 'role_type': 'dan', 'accompaniment_required': '曲笛、三弦'},
            ],
            '天仙配': [
                {'name': '树上的鸟儿成双对', 'lyrics': '树上的鸟儿成双对，绿水青山带笑颜...', 'order_index': 1, 'duration': 180, 'role_type': 'dan', 'accompaniment_required': '高胡、扬琴'},
                {'name': '夫妻双双把家还', 'lyrics': '你耕田来我织布，我挑水来你浇园...', 'order_index': 2, 'duration': 160, 'role_type': 'sheng', 'accompaniment_required': '高胡、琵琶'},
                {'name': '神仙岁月我不爱', 'lyrics': '神仙岁月我不爱，愿做鸳鸯比翼飞...', 'order_index': 3, 'duration': 200, 'role_type': 'dan', 'accompaniment_required': '高胡、三弦'},
                {'name': '父王命我回天庭', 'lyrics': '父王命我回天庭，心如刀绞泪淋淋...', 'order_index': 4, 'duration': 220, 'role_type': 'dan', 'accompaniment_required': '高胡、大锣'},
            ],
        }

        roles_data = {
            '锁麟囊': [
                {'name': '薛湘灵', 'role_type': 'dan', 'description': '富家小姐，善良慷慨'},
                {'name': '赵禄寒', 'role_type': 'sheng', 'description': '贫穷书生'},
                {'name': '薛良', 'role_type': 'jing', 'description': '薛家老仆'},
                {'name': '梅香', 'role_type': 'chou', 'description': '薛湘灵丫鬟'},
            ],
            '穆桂英挂帅': [
                {'name': '穆桂英', 'role_type': 'dan', 'description': '杨家媳妇，巾帼英雄'},
                {'name': '杨宗保', 'role_type': 'sheng', 'description': '杨家将，穆桂英丈夫'},
                {'name': '佘太君', 'role_type': 'jing', 'description': '杨家老祖母'},
                {'name': '杨文广', 'role_type': 'sheng', 'description': '穆桂英之子'},
            ],
            '牡丹亭': [
                {'name': '杜丽娘', 'role_type': 'dan', 'description': '南安太守杜宝之女'},
                {'name': '柳梦梅', 'role_type': 'sheng', 'description': '岭南书生'},
                {'name': '春香', 'role_type': 'chou', 'description': '杜丽娘侍女'},
                {'name': '杜宝', 'role_type': 'jing', 'description': '南安太守'},
            ],
            '天仙配': [
                {'name': '七仙女', 'role_type': 'dan', 'description': '玉帝第七女'},
                {'name': '董永', 'role_type': 'sheng', 'description': '卖身葬父的孝子'},
                {'name': '玉帝', 'role_type': 'jing', 'description': '天庭之主'},
                {'name': '土地公公', 'role_type': 'chou', 'description': '地方小神'},
            ],
        }

        for prog in programs:
            for aria_data in arias_data.get(prog.name, []):
                Aria.objects.create(program=prog, **aria_data)
            self.stdout.write(f'  创建唱段: {prog.name} 共 {len(arias_data.get(prog.name, []))} 个')

            for role_data in roles_data.get(prog.name, []):
                Role.objects.create(program=prog, **role_data)
            self.stdout.write(f'  创建角色: {prog.name} 共 {len(roles_data.get(prog.name, []))} 个')

        members_data = [
            {'name': '张玉兰', 'phone': '13800138001', 'role_types': 'dan,sheng', 'is_understudy': True},
            {'name': '李秀英', 'phone': '13800138002', 'role_types': 'dan', 'is_understudy': False},
            {'name': '王建国', 'phone': '13800138003', 'role_types': 'sheng,jing', 'is_understudy': True},
            {'name': '赵志强', 'phone': '13800138004', 'role_types': 'sheng', 'is_understudy': False},
            {'name': '刘美丽', 'phone': '13800138005', 'role_types': 'dan,chou', 'is_understudy': True},
            {'name': '陈明华', 'phone': '13800138006', 'role_types': 'jing,mo', 'is_understudy': False},
            {'name': '杨丽华', 'phone': '13800138007', 'role_types': 'dan', 'is_understudy': True},
            {'name': '黄志远', 'phone': '13800138008', 'role_types': 'sheng,chou', 'is_understudy': True},
            {'name': '周芳芳', 'phone': '13800138009', 'role_types': 'dan,sheng', 'is_understudy': False},
            {'name': '吴海涛', 'phone': '13800138010', 'role_types': 'jing', 'is_understudy': True},
        ]

        today = date.today()
        members = []
        for idx, member_data in enumerate(members_data):
            available_times = {}
            for i in range(14):
                day = today + timedelta(days=i)
                if i % 3 != 0:
                    available_times[day.strftime('%Y-%m-%d')] = ['14:00-16:00', '19:00-21:00']
                elif i % 5 == 0:
                    available_times[day.strftime('%Y-%m-%d')] = ['09:00-11:00']
            member = Member.objects.create(
                **member_data,
                available_times=available_times
            )
            members.append(member)
            self.stdout.write(f'  创建成员: {member.name}')

        program = programs[0]
        arias = Aria.objects.filter(program=program).order_by('order_index')
        roles = Role.objects.filter(program=program)

        assignments = []
        for i, aria in enumerate(arias):
            main_member = members[i % len(members)]
            matching_role = roles.filter(role_type=aria.role_type).first()

            assignment = AriaAssignment.objects.create(
                aria=aria,
                member=main_member,
                role=matching_role,
                is_understudy=False,
                status='confirmed'
            )
            assignments.append(assignment)
            self.stdout.write(f'  分配主角色: {aria.name} -> {main_member.name}')

            if i % 2 == 0:
                understudy_idx = (i + 3) % len(members)
                understudy_member = members[understudy_idx]
                if understudy_member.is_understudy:
                    AriaAssignment.objects.create(
                        aria=aria,
                        member=understudy_member,
                        role=matching_role,
                        is_understudy=True,
                        status='confirmed'
                    )
                    self.stdout.write(f'  分配替补: {aria.name} -> {understudy_member.name}')

        rehearsal_dates = [today - timedelta(days=14), today - timedelta(days=7), today]
        for rehearsal_date in rehearsal_dates:
            rehearsal = Rehearsal.objects.create(
                program=program,
                date=rehearsal_date,
                location='社区文化活动中心戏曲排练厅',
                notes=f'{program.name} 日常排练'
            )
            self.stdout.write(f'  创建排练记录: {rehearsal.date}')

            for i, aria in enumerate(arias[:3]):
                member = members[i % len(members)]
                feedback = RehearsalFeedback.objects.create(
                    rehearsal=rehearsal,
                    aria=aria,
                    member=member,
                    audio_url=f'https://example.com/audio/{rehearsal.id}/{aria.id}.mp3',
                    start_beat_issue='第3小节起板稍慢' if i == 0 else '',
                    forgotten_lines='第二段第2句忘词' if i == 1 else '',
                    teacher_comments='整体表现不错，注意情感表达' if i == 2 else '继续保持'
                )
                self.stdout.write(f'    创建反馈: {aria.name} - {member.name}')

        if assignments:
            original = assignments[0]
            substitute = members[5]
            if substitute.is_understudy:
                change = UnderstudyChange.objects.create(
                    original_assignment=original,
                    substitute_member=substitute,
                    reason='原演员临时有事',
                    date=today - timedelta(days=5),
                    status='completed'
                )
                self.stdout.write(f'  创建替补记录: {original.member.name} -> {substitute.name}')

        archived_program = programs[3]
        archive = Archive.objects.create(
            program=archived_program,
            version='1.0',
            final_assignments={
                'program': archived_program.name,
                'assignments': [
                    {'aria': '树上的鸟儿成双对', 'member': '张玉兰', 'role': '七仙女'},
                    {'aria': '夫妻双双把家还', 'member': '王建国', 'role': '董永'},
                ]
            }
        )
        self.stdout.write(f'  创建归档: {archive.program.name} v{archive.version}')

        second_seed_aria = arias.order_by('order_index')[1] if arias.count() > 1 else None
        if second_seed_aria:
            understudy_candidate = next(
                (m for m in members
                 if m.is_understudy and not AriaAssignment.objects.filter(aria=second_seed_aria, member=m).exists()),
                None
            )
            if understudy_candidate:
                matching_understudy_role = roles.filter(role_type=second_seed_aria.role_type).first()
                AriaAssignment.objects.get_or_create(
                    aria=second_seed_aria,
                    member=understudy_candidate,
                    is_understudy=True,
                    defaults={'role': matching_understudy_role, 'status': 'confirmed'}
                )

        check = RehearsalCheck.objects.create(
            program=program,
            name=f'{program.name} 演出前联排确认',
            planned_performance_date=today + timedelta(days=10),
            status='open',
            notes='演出前最后一次联排确认，请各负责人尽快完成确认。'
        )
        self.stdout.write(f'  创建联排确认批次: {check.name}')

        for aria in arias.order_by('order_index'):
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
            for assignment in AriaAssignment.objects.filter(aria=aria, status='confirmed').select_related('role'):
                RehearsalCheckConfirmation.objects.create(
                    check_item=item,
                    member=assignment.member,
                    role=assignment.role,
                    role_name=assignment.role.name if assignment.role else '',
                    is_understudy=assignment.is_understudy,
                )

        first_item = check.items.order_by('order_index').first()
        if first_item:
            for conf in first_item.confirmations.all():
                conf.attendance_confirmed = True
                conf.lyrics_proficiency = 'familiar'
                conf.save()
            first_item.accompaniment_confirmed = True
            first_item.accompaniment_confirmed_by = members[0]
            first_item.save()

        second_item = check.items.order_by('order_index')[1] if check.items.count() > 1 else None
        if second_item:
            second_item.risk_level = 'high'
            second_item.teacher_comment = '起板问题尚未解决且存在忘词，需重点强化，必要时启用替补。'
            second_item.risk_action_created = True
            second_item.save()

        if second_item:
            RiskActionItem.objects.create(
                check_item=second_item,
                action_type='feedback',
                description='唱段「一霎时把七情俱已昧尽」最近排练反馈仍有问题，需重点强化。',
                status='pending'
            )

        self.stdout.write(self.style.SUCCESS('测试数据初始化完成！'))
        self.stdout.write(f'  节目: {Program.objects.count()} 个')
        self.stdout.write(f'  唱段: {Aria.objects.count()} 个')
        self.stdout.write(f'  角色: {Role.objects.count()} 个')
        self.stdout.write(f'  成员: {Member.objects.count()} 个')
        self.stdout.write(f'  分配记录: {AriaAssignment.objects.count()} 条')
        self.stdout.write(f'  排练记录: {Rehearsal.objects.count()} 条')
        self.stdout.write(f'  反馈记录: {RehearsalFeedback.objects.count()} 条')
        self.stdout.write(f'  替补记录: {UnderstudyChange.objects.count()} 条')
        self.stdout.write(f'  归档记录: {Archive.objects.count()} 条')
        self.stdout.write(f'  联排确认批次: {RehearsalCheck.objects.count()} 个')
        self.stdout.write(f'  联排清单项: {RehearsalCheckItem.objects.count()} 个')
        self.stdout.write(f'  联排确认记录: {RehearsalCheckConfirmation.objects.count()} 条')
        self.stdout.write(f'  风险待处理项: {RiskActionItem.objects.count()} 条')
