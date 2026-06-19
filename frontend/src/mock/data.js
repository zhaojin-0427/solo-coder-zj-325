let idCounter = 100

const programs = [
  { id: 1, name: '贵妃醉酒', description: '京剧经典剧目，讲述杨贵妃醉后情怀', type: '京剧', duration: 45, status: 'active' },
  { id: 2, name: '穆桂英挂帅', description: '传统京剧，巾帼英雄故事', type: '京剧', duration: 60, status: 'active' },
  { id: 3, name: '红楼梦·葬花', description: '越剧经典，林黛玉葬花', type: '越剧', duration: 30, status: 'active' },
  { id: 4, name: '天仙配', description: '黄梅戏经典剧目', type: '黄梅戏', duration: 50, status: 'inactive' },
  { id: 5, name: '花木兰', description: '豫剧经典，花木兰代父从军', type: '豫剧', duration: 55, status: 'active' }
]

const arias = [
  { id: 1, program: 1, name: '海岛冰轮初转腾', lyrics: '海岛冰轮初转腾，见玉兔，见玉兔又早东升...', order_index: 1, duration: 8, role_type: '旦角', accompaniment_required: true },
  { id: 2, program: 1, name: '杨玉环在殿前深深拜定', lyrics: '杨玉环在殿前深深拜定，秉虔诚一件件祝告神明...', order_index: 2, duration: 6, role_type: '旦角', accompaniment_required: true },
  { id: 3, program: 2, name: '猛听得金鼓响画角声震', lyrics: '猛听得金鼓响画角声震，唤起我破天门壮志凌云...', order_index: 1, duration: 10, role_type: '旦角', accompaniment_required: true },
  { id: 4, program: 2, name: '一家人闻边报雄心振奋', lyrics: '一家人闻边报雄心振奋，穆桂英为帅印再度出征...', order_index: 2, duration: 8, role_type: '旦角', accompaniment_required: true },
  { id: 5, program: 3, name: '花谢花飞飞满天', lyrics: '花谢花飞飞满天，红消香断有谁怜...', order_index: 1, duration: 7, role_type: '旦角', accompaniment_required: true },
  { id: 6, program: 3, name: '绕绿堤，拂柳丝，穿过花径', lyrics: '绕绿堤，拂柳丝，穿过花径，听何处，哀怨笛，风送声声...', order_index: 2, duration: 5, role_type: '旦角', accompaniment_required: true },
  { id: 7, program: 5, name: '刘大哥讲话理太偏', lyrics: '刘大哥讲话理太偏，谁说女子享清闲...', order_index: 1, duration: 6, role_type: '旦角', accompaniment_required: true },
  { id: 8, program: 5, name: '花木兰羞答答施礼拜上', lyrics: '花木兰羞答答施礼拜上，尊一声贺元帅细听端详...', order_index: 2, duration: 8, role_type: '旦角', accompaniment_required: true }
]

const roles = [
  { id: 1, program: 1, name: '杨贵妃', role_type: '旦角', description: '大唐贵妃，风华绝代' },
  { id: 2, program: 1, name: '高力士', role_type: '丑角', description: '太监总管' },
  { id: 3, program: 2, name: '穆桂英', role_type: '旦角', description: '巾帼英雄' },
  { id: 4, program: 2, name: '佘太君', role_type: '老旦', description: '杨家将老太君' },
  { id: 5, program: 3, name: '林黛玉', role_type: '旦角', description: '绛珠仙草转世' },
  { id: 6, program: 3, name: '贾宝玉', role_type: '小生', description: '神瑛侍者转世' },
  { id: 7, program: 5, name: '花木兰', role_type: '旦角', description: '代父从军巾帼英雄' }
]

const members = [
  { id: 1, name: '张素华', phone: '13800138001', role_types: ['旦角'], available_times: ['周一', '周三', '周五'], is_understudy: false },
  { id: 2, name: '李梅芳', phone: '13800138002', role_types: ['旦角', '老旦'], available_times: ['周二', '周四', '周六'], is_understudy: false },
  { id: 3, name: '王秀兰', phone: '13800138003', role_types: ['小生'], available_times: ['周一', '周三', '周六'], is_understudy: false },
  { id: 4, name: '赵彩云', phone: '13800138004', role_types: ['旦角'], available_times: ['周二', '周五', '周日'], is_understudy: true },
  { id: 5, name: '陈丽娟', phone: '13800138005', role_types: ['丑角', '老旦'], available_times: ['周一', '周四', '周六'], is_understudy: true },
  { id: 6, name: '刘凤英', phone: '13800138006', role_types: ['旦角', '小生'], available_times: ['周三', '周五', '周日'], is_understudy: false },
  { id: 7, name: '周桂兰', phone: '13800138007', role_types: ['旦角'], available_times: ['周一', '周二', '周四'], is_understudy: true },
  { id: 8, name: '孙淑珍', phone: '13800138008', role_types: ['老旦'], available_times: ['周三', '周六', '周日'], is_understudy: false }
]

const assignments = [
  { id: 1, aria: 1, member: 1, role: 1, is_understudy: false, status: 'confirmed' },
  { id: 2, aria: 1, member: 4, role: 1, is_understudy: true, status: 'confirmed' },
  { id: 3, aria: 2, member: 1, role: 1, is_understudy: false, status: 'confirmed' },
  { id: 4, aria: 3, member: 2, role: 3, is_understudy: false, status: 'confirmed' },
  { id: 5, aria: 4, member: 2, role: 3, is_understudy: false, status: 'confirmed' },
  { id: 6, aria: 5, member: 6, role: 5, is_understudy: false, status: 'confirmed' },
  { id: 7, aria: 5, member: 7, role: 5, is_understudy: true, status: 'confirmed' },
  { id: 8, aria: 6, member: 6, role: 5, is_understudy: false, status: 'confirmed' },
  { id: 9, aria: 7, member: 4, role: 7, is_understudy: false, status: 'confirmed' },
  { id: 10, aria: 8, member: 4, role: 7, is_understudy: false, status: 'pending' }
]

const rehearsals = [
  { id: 1, program: 1, date: '2024-06-15', location: '社区文化站', notes: '第一次排练，重点练习起板' },
  { id: 2, program: 1, date: '2024-06-20', location: '社区文化站', notes: '完整剧目联排' },
  { id: 3, program: 2, date: '2024-06-18', location: '老年活动中心', notes: '穆桂英挂帅重点排练' },
  { id: 4, program: 3, date: '2024-06-22', location: '社区文化站', notes: '红楼梦唱段排练' },
  { id: 5, program: 5, date: '2024-06-25', location: '社区文化站', notes: '花木兰首次排练' },
  { id: 6, program: 1, date: '2024-06-28', location: '社区剧场', notes: '彩排' },
  { id: 7, program: 2, date: '2024-06-30', location: '社区剧场', notes: '彩排' }
]

const feedbacks = [
  { id: 1, rehearsal: 1, aria: 1, member: 1, audio_url: '/mock/audio1.mp3', start_beat_issue: '起板慢了半拍，注意节奏', forgotten_lines: '第二段第三句忘词', teacher_comments: '整体表现不错，情绪到位。起板需要加强练习' },
  { id: 2, rehearsal: 1, aria: 2, member: 1, audio_url: '/mock/audio2.mp3', start_beat_issue: '节奏基本准确', forgotten_lines: '无', teacher_comments: '情感表达很好，继续保持' },
  { id: 3, rehearsal: 2, aria: 1, member: 1, audio_url: '/mock/audio3.mp3', start_beat_issue: '起板问题已改进', forgotten_lines: '无', teacher_comments: '进步明显，状态很好' },
  { id: 4, rehearsal: 3, aria: 3, member: 2, audio_url: '/mock/audio4.mp3', start_beat_issue: '快板部分节奏不稳', forgotten_lines: '无', teacher_comments: '气势很足，注意快板的节奏控制' },
  { id: 5, rehearsal: 4, aria: 5, member: 6, audio_url: '/mock/audio5.mp3', start_beat_issue: '无', forgotten_lines: '最后一段有两句忘词', teacher_comments: '情感细腻，多练熟歌词就更好了' },
  { id: 6, rehearsal: 5, aria: 7, member: 4, audio_url: '/mock/audio6.mp3', start_beat_issue: '起板准确', forgotten_lines: '无', teacher_comments: '豫剧韵味十足，非常好' }
]

const understudyChanges = [
  { id: 1, original_assignment: 1, substitute_member: 4, reason: '张素华身体不适', date: '2024-06-16', status: 'completed' },
  { id: 2, original_assignment: 6, substitute_member: 7, reason: '刘凤英有事请假', date: '2024-06-21', status: 'pending' },
  { id: 3, original_assignment: 4, substitute_member: 7, reason: '李梅芳家中有事', date: '2024-06-19', status: 'completed' }
]

const rehearsalChecks = [
  {
    id: 1, program: 1, name: '贵妃醉酒 演出前联排确认',
    planned_performance_date: '2024-07-10', status: 'open', notes: '演出前联排确认',
    created_at: '2024-06-25T10:00:00', item_count: 2, risk_aria_count: 1
  }
]

const rehearsalCheckItems = [
  {
    id: 1, rehearsal_check: 1, aria: 1, order_index: 1, role_type: 'dan',
    accompaniment_required: '京胡、月琴', accompaniment_confirmed: true, accompaniment_confirmed_by: 2,
    risk_level: 'none', teacher_comment: '', risk_action_created: false,
    latest_feedback_date: '2024-06-28', latest_start_beat_issue: '', latest_forgotten_lines: '',
    latest_teacher_comments: '整体不错', aria_name: '海岛冰轮初转腾', risk_flags: [], risk_score: 0,
    has_understudy: true, confirmations: [
      { id: 1, check_item: 1, member: 1, member_name: '张素华', is_understudy: false, attendance_confirmed: true, lyrics_proficiency: 'familiar', needs_understudy_help: false, note: '' }
    ]
  },
  {
    id: 2, rehearsal_check: 1, aria: 2, order_index: 2, role_type: 'dan',
    accompaniment_required: '京胡、二胡', accompaniment_confirmed: false, accompaniment_confirmed_by: null,
    risk_level: 'high', teacher_comment: '起板问题需强化', risk_action_created: true,
    latest_feedback_date: '2024-06-28', latest_start_beat_issue: '起板慢半拍', latest_forgotten_lines: '第二段忘词',
    latest_teacher_comments: '需重点练习', aria_name: '杨玉环在殿前深深拜定', risk_flags: ['attendance', 'feedback', 'accompaniment', 'teacher_risk'], risk_score: 4,
    has_understudy: false, confirmations: [
      { id: 2, check_item: 2, member: 1, member_name: '张素华', is_understudy: false, attendance_confirmed: false, lyrics_proficiency: 'unconfirmed', needs_understudy_help: true, note: '' }
    ]
  }
]

const riskActions = [
  { id: 1, check_item: 2, aria_name: '杨玉环在殿前深深拜定', aria_id: 2, rehearsal_check: 1, order_index: 2, action_type: 'feedback', action_type_display: '排练反馈问题', status: 'pending', status_display: '待处理', description: '起板问题需强化', created_at: '2024-06-26T10:00:00' }
]

const statistics = {
  program_rehearsal_counts: [
    { name: '贵妃醉酒', count: 3 },
    { name: '穆桂英挂帅', count: 2 },
    { name: '红楼梦·葬花', count: 1 },
    { name: '天仙配', count: 0 },
    { name: '花木兰', count: 2 }
  ],
  understudy_frequency: [
    { name: '身体不适', value: 5 },
    { name: '有事请假', value: 8 },
    { name: '临时有事', value: 3 },
    { name: '其他原因', value: 2 }
  ],
  mistake_segments: [
    { name: '海岛冰轮初转腾-第二段', count: 5 },
    { name: '猛听得金鼓响-快板部分', count: 4 },
    { name: '花谢花飞-结尾段', count: 3 },
    { name: '刘大哥讲话-起板', count: 3 },
    { name: '杨玉环在殿前-长腔', count: 2 }
  ],
  member_activity: [
    { name: '张素华', values: { rehearsal_count: 8, assignment_count: 2, feedback_count: 3, on_time_rate: 95, performance_score: 88 } },
    { name: '李梅芳', values: { rehearsal_count: 6, assignment_count: 2, feedback_count: 2, on_time_rate: 90, performance_score: 85 } },
    { name: '王秀兰', values: { rehearsal_count: 4, assignment_count: 0, feedback_count: 0, on_time_rate: 100, performance_score: 80 } },
    { name: '赵彩云', values: { rehearsal_count: 7, assignment_count: 2, feedback_count: 1, on_time_rate: 88, performance_score: 82 } },
    { name: '陈丽娟', values: { rehearsal_count: 5, assignment_count: 0, feedback_count: 0, on_time_rate: 92, performance_score: 78 } },
    { name: '刘凤英', values: { rehearsal_count: 6, assignment_count: 2, feedback_count: 1, on_time_rate: 85, performance_score: 90 } }
  ],
  pre_performance_risk: {
    open_check_count: 1,
    risk_aria_count: 1,
    pending_risk_actions: 1,
    flag_breakdown: [
      { action_type: 'attendance', label: '未确认到场', count: 1 },
      { action_type: 'accompaniment', label: '伴奏未确认', count: 1 },
      { action_type: 'feedback', label: '排练反馈问题', count: 1 },
      { action_type: 'teacher_risk', label: '老师标注风险', count: 1 }
    ],
    risk_action_breakdown: [
      { action_type: 'feedback', label: '排练反馈问题', count: 1 }
    ],
    program_risk: [
      { program_id: 1, program_name: '贵妃醉酒', risk_aria_count: 1, open_check_count: 1 }
    ]
  }
}

const handleRequest = function(method, url, data, params) {
  if (url.startsWith('/programs')) {
    return handlePrograms(method, url, data, params)
  } else if (url.startsWith('/arias')) {
    return handleArias(method, url, data, params)
  } else if (url.startsWith('/roles')) {
    return handleRoles(method, url, data, params)
  } else if (url.startsWith('/members')) {
    return handleMembers(method, url, data, params)
  } else if (url.startsWith('/assignments/auto-assign')) {
    return handleAutoAssign(data)
  } else if (url.startsWith('/assignments')) {
    return handleAssignments(method, url, data, params)
  } else if (url.startsWith('/rehearsals')) {
    return handleRehearsals(method, url, data, params)
  } else if (url.startsWith('/feedbacks')) {
    return handleFeedbacks(method, url, data, params)
  } else if (url.startsWith('/understudy-changes')) {
    return handleUnderstudyChanges(method, url, data, params)
  } else if (url.startsWith('/rehearsal-checks')) {
    return handleRehearsalChecks(method, url, data, params)
  } else if (url.startsWith('/rehearsal-check-items')) {
    return handleRehearsalCheckItems(method, url, data)
  } else if (url.startsWith('/rehearsal-check-confirmations')) {
    return handleRehearsalCheckConfirmations(method, url, data)
  } else if (url.startsWith('/risk-action-items')) {
    return handleRiskActionItems(method, url, data, params)
  } else if (url.startsWith('/statistics')) {
    return statistics
  }
  return []
}

function handlePrograms(method, url, data, params) {
  const idMatch = url.match(/\/programs\/(\d+)/)
  if (idMatch) {
    const id = parseInt(idMatch[1])
    if (method === 'GET') {
      return programs.find(p => p.id === id)
    } else if (method === 'PUT') {
      const index = programs.findIndex(p => p.id === id)
      if (index !== -1) {
        programs[index] = { ...programs[index], ...data }
        return programs[index]
      }
    } else if (method === 'DELETE') {
      const index = programs.findIndex(p => p.id === id)
      if (index !== -1) {
        programs.splice(index, 1)
      }
      return { success: true }
    }
  } else {
    if (method === 'GET') {
      return [...programs]
    } else if (method === 'POST') {
      const newItem = { id: ++idCounter, ...data }
      programs.push(newItem)
      return newItem
    }
  }
  return null
}

function handleArias(method, url, data, params) {
  const idMatch = url.match(/\/arias\/(\d+)/)
  if (idMatch) {
    const id = parseInt(idMatch[1])
    if (method === 'GET') {
      return arias.find(a => a.id === id)
    } else if (method === 'PUT') {
      const index = arias.findIndex(a => a.id === id)
      if (index !== -1) {
        arias[index] = { ...arias[index], ...data }
        return arias[index]
      }
    } else if (method === 'DELETE') {
      const index = arias.findIndex(a => a.id === id)
      if (index !== -1) {
        arias.splice(index, 1)
      }
      return { success: true }
    }
  } else {
    if (method === 'GET') {
      if (params && params.program) {
        return arias.filter(a => a.program === parseInt(params.program))
      }
      return [...arias]
    } else if (method === 'POST') {
      const newItem = { id: ++idCounter, ...data }
      arias.push(newItem)
      return newItem
    }
  }
  return null
}

function handleRoles(method, url, data, params) {
  const idMatch = url.match(/\/roles\/(\d+)/)
  if (idMatch) {
    const id = parseInt(idMatch[1])
    if (method === 'GET') {
      return roles.find(r => r.id === id)
    } else if (method === 'PUT') {
      const index = roles.findIndex(r => r.id === id)
      if (index !== -1) {
        roles[index] = { ...roles[index], ...data }
        return roles[index]
      }
    } else if (method === 'DELETE') {
      const index = roles.findIndex(r => r.id === id)
      if (index !== -1) {
        roles.splice(index, 1)
      }
      return { success: true }
    }
  } else {
    if (method === 'GET') {
      if (params && params.program) {
        return roles.filter(r => r.program === parseInt(params.program))
      }
      return [...roles]
    } else if (method === 'POST') {
      const newItem = { id: ++idCounter, ...data }
      roles.push(newItem)
      return newItem
    }
  }
  return null
}

function handleMembers(method, url, data, params) {
  const idMatch = url.match(/\/members\/(\d+)/)
  if (idMatch) {
    const id = parseInt(idMatch[1])
    if (method === 'GET') {
      return members.find(m => m.id === id)
    } else if (method === 'PUT') {
      const index = members.findIndex(m => m.id === id)
      if (index !== -1) {
        members[index] = { ...members[index], ...data }
        return members[index]
      }
    } else if (method === 'DELETE') {
      const index = members.findIndex(m => m.id === id)
      if (index !== -1) {
        members.splice(index, 1)
      }
      return { success: true }
    }
  } else {
    if (method === 'GET') {
      return [...members]
    } else if (method === 'POST') {
      const newItem = { id: ++idCounter, ...data }
      members.push(newItem)
      return newItem
    }
  }
  return null
}

function handleAssignments(method, url, data, params) {
  const idMatch = url.match(/\/assignments\/(\d+)/)
  if (idMatch) {
    const id = parseInt(idMatch[1])
    if (method === 'GET') {
      return assignments.find(a => a.id === id)
    } else if (method === 'PUT') {
      const index = assignments.findIndex(a => a.id === id)
      if (index !== -1) {
        assignments[index] = { ...assignments[index], ...data }
        return assignments[index]
      }
    } else if (method === 'DELETE') {
      const index = assignments.findIndex(a => a.id === id)
      if (index !== -1) {
        assignments.splice(index, 1)
      }
      return { success: true }
    }
  } else {
    if (method === 'GET') {
      if (params && params.program) {
        const programArias = arias.filter(a => a.program === parseInt(params.program)).map(a => a.id)
        return assignments.filter(a => programArias.includes(a.aria))
      }
      return [...assignments]
    } else if (method === 'POST') {
      const newItem = { id: ++idCounter, ...data }
      assignments.push(newItem)
      return newItem
    }
  }
  return null
}

function handleAutoAssign(data) {
  const programId = data.program
  const programArias = arias.filter(a => a.program === programId)
  const programRoles = roles.filter(r => r.program === programId)
  
  const newAssignments = []
  
  programArias.forEach(aria => {
    const matchingRole = programRoles.find(r => r.role_type === aria.role_type)
    if (matchingRole) {
      const suitableMembers = members.filter(m => m.role_types.includes(aria.role_type))
      if (suitableMembers.length > 0) {
        const mainMember = suitableMembers[0]
        newAssignments.push({
          id: ++idCounter,
          aria: aria.id,
          member: mainMember.id,
          role: matchingRole.id,
          is_understudy: false,
          status: 'confirmed'
        })
        
        if (suitableMembers.length > 1) {
          const understudyMember = suitableMembers.find(m => m.is_understudy) || suitableMembers[1]
          newAssignments.push({
            id: ++idCounter,
            aria: aria.id,
            member: understudyMember.id,
            role: matchingRole.id,
            is_understudy: true,
            status: 'confirmed'
          })
        }
      }
    }
  })
  
  assignments.push(...newAssignments)
  return { success: true, assignments: newAssignments, count: newAssignments.length }
}

function handleRehearsals(method, url, data, params) {
  const idMatch = url.match(/\/rehearsals\/(\d+)/)
  if (idMatch) {
    const id = parseInt(idMatch[1])
    if (method === 'GET') {
      return rehearsals.find(r => r.id === id)
    } else if (method === 'PUT') {
      const index = rehearsals.findIndex(r => r.id === id)
      if (index !== -1) {
        rehearsals[index] = { ...rehearsals[index], ...data }
        return rehearsals[index]
      }
    } else if (method === 'DELETE') {
      const index = rehearsals.findIndex(r => r.id === id)
      if (index !== -1) {
        rehearsals.splice(index, 1)
      }
      return { success: true }
    }
  } else {
    if (method === 'GET') {
      if (params && params.program) {
        return rehearsals.filter(r => r.program === parseInt(params.program))
      }
      return [...rehearsals]
    } else if (method === 'POST') {
      const newItem = { id: ++idCounter, ...data }
      rehearsals.push(newItem)
      return newItem
    }
  }
  return null
}

function handleFeedbacks(method, url, data, params) {
  const idMatch = url.match(/\/feedbacks\/(\d+)/)
  if (idMatch) {
    const id = parseInt(idMatch[1])
    if (method === 'GET') {
      return feedbacks.find(f => f.id === id)
    } else if (method === 'PUT') {
      const index = feedbacks.findIndex(f => f.id === id)
      if (index !== -1) {
        feedbacks[index] = { ...feedbacks[index], ...data }
        return feedbacks[index]
      }
    } else if (method === 'DELETE') {
      const index = feedbacks.findIndex(f => f.id === id)
      if (index !== -1) {
        feedbacks.splice(index, 1)
      }
      return { success: true }
    }
  } else {
    if (method === 'GET') {
      if (params && params.rehearsal) {
        return feedbacks.filter(f => f.rehearsal === parseInt(params.rehearsal))
      }
      return [...feedbacks]
    } else if (method === 'POST') {
      const newItem = { id: ++idCounter, ...data }
      feedbacks.push(newItem)
      return newItem
    }
  }
  return null
}

function handleUnderstudyChanges(method, url, data, params) {
  const idMatch = url.match(/\/understudy-changes\/(\d+)/)
  if (idMatch) {
    const id = parseInt(idMatch[1])
    if (method === 'PUT') {
      const index = understudyChanges.findIndex(u => u.id === id)
      if (index !== -1) {
        understudyChanges[index] = { ...understudyChanges[index], ...data }
        return understudyChanges[index]
      }
    }
  } else {
    if (method === 'GET') {
      return [...understudyChanges]
    } else if (method === 'POST') {
      const newItem = { id: ++idCounter, ...data }
      understudyChanges.push(newItem)
      return newItem
    }
  }
  return null
}

function handleRehearsalChecks(method, url, data, params) {
  const idMatch = url.match(/\/rehearsal-checks\/(\d+)/)
  if (idMatch) {
    const id = parseInt(idMatch[1])
    if (url.includes('/items/')) {
      return rehearsalCheckItems.filter(i => i.rehearsal_check === id)
    }
    if (url.includes('/risk_dashboard/')) {
      const items = rehearsalCheckItems.filter(i => i.rehearsal_check === id)
      const riskItems = items.filter(i => i.risk_flags && i.risk_flags.length > 0)
      return {
        check_id: id, check_name: (rehearsalChecks.find(c => c.id === id) || {}).name, status: 'open',
        risk_items: riskItems,
        summary: { total_items: items.length, risk_aria_count: riskItems.length, flag_breakdown: [] }
      }
    }
    if (url.includes('/generate_actions/')) {
      return { created_count: 0, items: [] }
    }
    if (method === 'GET') {
      return rehearsalChecks.find(c => c.id === id)
    } else if (method === 'PUT') {
      const index = rehearsalChecks.findIndex(c => c.id === id)
      if (index !== -1) {
        rehearsalChecks[index] = { ...rehearsalChecks[index], ...data }
        return rehearsalChecks[index]
      }
    } else if (method === 'DELETE') {
      const index = rehearsalChecks.findIndex(c => c.id === id)
      if (index !== -1) rehearsalChecks.splice(index, 1)
      return { success: true }
    }
  } else {
    if (method === 'GET') {
      if (params && params.program_id) {
        return rehearsalChecks.filter(c => c.program === parseInt(params.program_id))
      }
      return [...rehearsalChecks]
    } else if (method === 'POST') {
      const newItem = { id: ++idCounter, item_count: 0, risk_aria_count: 0, status: 'open', ...data }
      rehearsalChecks.push(newItem)
      return newItem
    }
  }
  return null
}

function handleRehearsalCheckItems(method, url, data) {
  const idMatch = url.match(/\/rehearsal-check-items\/(\d+)/)
  if (idMatch) {
    const id = parseInt(idMatch[1])
    const index = rehearsalCheckItems.findIndex(i => i.id === id)
    if (index === -1) return null
    if (url.includes('/confirm_accompaniment/')) {
      rehearsalCheckItems[index] = {
        ...rehearsalCheckItems[index],
        accompaniment_confirmed: true,
        accompaniment_confirmed_by: data.member_id || null
      }
      return rehearsalCheckItems[index]
    }
    if (url.includes('/set_risk/')) {
      rehearsalCheckItems[index] = {
        ...rehearsalCheckItems[index],
        risk_level: data.risk_level !== undefined ? data.risk_level : rehearsalCheckItems[index].risk_level,
        teacher_comment: data.teacher_comment !== undefined ? data.teacher_comment : rehearsalCheckItems[index].teacher_comment
      }
      return rehearsalCheckItems[index]
    }
  }
  return null
}

function handleRehearsalCheckConfirmations(method, url, data) {
  const idMatch = url.match(/\/rehearsal-check-confirmations\/(\d+)/)
  if (idMatch && method === 'PUT') {
    const id = parseInt(idMatch[1])
    for (const item of rehearsalCheckItems) {
      const idx = item.confirmations.findIndex(c => c.id === id)
      if (idx !== -1) {
        item.confirmations[idx] = { ...item.confirmations[idx], ...data }
        return item.confirmations[idx]
      }
    }
  }
  return null
}

function handleRiskActionItems(method, url, data, params) {
  const idMatch = url.match(/\/risk-action-items\/(\d+)/)
  if (idMatch) {
    const id = parseInt(idMatch[1])
    if (url.includes('/resolve/')) {
      const index = riskActions.findIndex(a => a.id === id)
      if (index !== -1) {
        riskActions[index] = { ...riskActions[index], status: 'resolved', status_display: '已处理' }
        return riskActions[index]
      }
    }
  } else {
    if (method === 'GET') {
      if (params && params.rehearsal_check) {
        return riskActions.filter(a => a.rehearsal_check === parseInt(params.rehearsal_check))
      }
      return [...riskActions]
    }
  }
  return null
}

export default { handleRequest }
