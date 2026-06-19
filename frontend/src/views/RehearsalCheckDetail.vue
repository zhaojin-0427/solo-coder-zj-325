<template>
  <div class="page-container">
    <div class="page-header">
      <h2>
        <el-button link @click="router.back()">
          <el-icon><ArrowLeft /></el-icon>
        </el-button>
        联排确认 - {{ check?.name }}
      </h2>
      <div class="header-actions">
        <el-button :icon="Refresh" @click="loadAll">刷新</el-button>
        <el-button type="warning" :icon="MagicStick" :loading="generating" @click="handleGenerateActions">
          一键生成待处理项
        </el-button>
      </div>
    </div>

    <div v-if="check" class="opera-card check-info">
      <div class="info-row">
        <div class="info-item">
          <div class="detail-label">节目</div>
          <div class="detail-value">{{ check.program_name }}</div>
        </div>
        <div class="info-item">
          <div class="detail-label">计划演出日期</div>
          <div class="detail-value">{{ check.planned_performance_date || '-' }}</div>
        </div>
        <div class="info-item">
          <div class="detail-label">状态</div>
          <div class="detail-value">
            <el-tag :type="check.status === 'open' ? 'warning' : 'info'">{{ check.status_display }}</el-tag>
          </div>
        </div>
        <div class="info-item">
          <div class="detail-label">唱段数</div>
          <div class="detail-value">{{ dashboard?.summary?.total_items ?? '-' }}</div>
        </div>
        <div class="info-item">
          <div class="detail-label">备注</div>
          <div class="detail-value">{{ check.notes || '-' }}</div>
        </div>
      </div>
    </div>

    <div v-if="dashboard" class="dashboard-summary">
      <StatsCard :icon="Warning" label="风险唱段" :value="dashboard.summary.risk_aria_count" bgColor="linear-gradient(135deg, #FF9800, #F57C00)" />
      <StatsCard :icon="User" label="未确认到场" :value="flagCount('attendance')" bgColor="linear-gradient(135deg, #C41E3A, #8B0000)" />
      <StatsCard :icon="Switch" label="无替补" :value="flagCount('understudy')" bgColor="linear-gradient(135deg, #D4AF37, #B8860B)" />
      <StatsCard :icon="Microphone" label="伴奏未确认" :value="flagCount('accompaniment')" bgColor="linear-gradient(135deg, #1976D2, #0D47A1)" />
      <StatsCard :icon="Document" label="反馈问题" :value="flagCount('feedback')" bgColor="linear-gradient(135deg, #2E7D32, #1B5E20)" />
      <StatsCard :icon="Bell" label="老师标注风险" :value="flagCount('teacher_risk')" bgColor="linear-gradient(135deg, #7B1FA2, #4A148C)" />
    </div>

    <div class="opera-card">
      <div class="section-head">
        <h3 class="section-title">风险看板</h3>
        <div class="risk-tabs">
          <el-radio-group v-model="riskTab" size="small">
            <el-radio-button value="active">当前仍存在风险</el-radio-button>
            <el-radio-button value="history">历史已解除风险</el-radio-button>
          </el-radio-group>
        </div>
      </div>
      <el-table 
        :data="riskTab === 'active' ? activeRiskItems : historyRiskItems" 
        v-loading="loading" 
        stripe 
        empty-text="暂无风险唱段，状态良好"
      >
        <el-table-column prop="order_index" label="序号" width="70" />
        <el-table-column prop="aria_name" label="唱段" min-width="160" />
        <el-table-column label="风险等级" width="110">
          <template #default="{ row }">
            <el-tag :type="riskTagType(row.risk_level)">{{ row.risk_level_display }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="风险分值" width="90">
          <template #default="{ row }">
            <el-tag type="danger" effect="dark">{{ row.risk_score }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="风险标签" min-width="260">
          <template #default="{ row }">
            <el-tag
              v-for="label in row.flag_labels"
              :key="label"
              class="risk-flag"
              :type="flagTagType(label)"
              effect="plain"
            >
              {{ label }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="未确认成员" min-width="200">
          <template #default="{ row }">
            <span v-if="!row.unconfirmed_members.length" class="muted">-</span>
            <span v-else>
              <span v-for="(m, idx) in row.unconfirmed_members" :key="m.id">
                {{ m.name }}
                <span v-if="m.role_name" class="muted">（{{ m.role_name }}）</span>
                <span v-if="idx < row.unconfirmed_members.length - 1">、</span>
              </span>
            </span>
          </template>
        </el-table-column>
        <el-table-column label="最近反馈问题" min-width="220">
          <template #default="{ row }">
            <div v-if="row.latest_start_beat_issue || row.latest_forgotten_lines">
              <div v-if="row.latest_start_beat_issue">起板：{{ row.latest_start_beat_issue }}</div>
              <div v-if="row.latest_forgotten_lines">忘词：{{ row.latest_forgotten_lines }}</div>
              <div class="muted" v-if="row.latest_feedback_date">{{ row.latest_feedback_date }}</div>
            </div>
            <span v-else class="muted">无</span>
          </template>
        </el-table-column>
        <el-table-column label="伴奏" width="90">
          <template #default="{ row }">
            <el-tag :type="row.accompaniment_confirmed ? 'success' : 'danger'">
              {{ row.accompaniment_confirmed ? '已确认' : '未确认' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="老师意见" min-width="180" show-overflow-tooltip>
          <template #default="{ row }">{{ row.teacher_comment || '-' }}</template>
        </el-table-column>
        <el-table-column label="待处理项" width="100">
          <template #default="{ row }">
            <el-tag :type="row.risk_action_created ? 'success' : 'info'">
              {{ row.risk_action_created ? '已生成' : '未生成' }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <div class="opera-card">
      <div class="section-head">
        <h3 class="section-title">联排确认清单</h3>
        <span class="muted">成员确认到场 / 歌词熟练度 / 替补协助，伴奏负责人确认，老师标注风险</span>
      </div>
      <div v-loading="loading">
        <el-collapse v-model="activeCollapse">
          <el-collapse-item
            v-for="item in items"
            :key="item.id"
            :name="item.id"
          >
            <template #title>
              <div class="item-title">
                <span class="item-order">{{ item.order_index }}</span>
                <span class="item-name">{{ item.aria_name }}</span>
                <el-tag size="small" type="info">{{ item.role_type_display }}</el-tag>
                <el-tag size="small" :type="riskTagType(item.risk_level)">{{ item.risk_level_display }}</el-tag>
                <el-tag v-if="item.risk_flags.length" size="small" type="danger" effect="dark">风险 {{ item.risk_score }}</el-tag>
                <el-tag v-if="item.has_understudy" size="small" type="warning" effect="plain">有替补</el-tag>
                <el-tag v-else size="small" type="danger" effect="plain">无替补</el-tag>
                <el-tag size="small" :type="item.accompaniment_confirmed ? 'success' : 'danger'">
                  伴奏{{ item.accompaniment_confirmed ? '已备' : '未备' }}
                </el-tag>
              </div>
            </template>

            <div class="item-detail">
              <div class="detail-block">
                <div class="detail-label">伴奏需求</div>
                <div>{{ item.accompaniment_required || '无' }}</div>
              </div>
              <div class="detail-block" v-if="item.latest_feedback_date">
                <div class="detail-label">最近排练反馈</div>
                <div>
                  <span v-if="item.latest_start_beat_issue">起板：{{ item.latest_start_beat_issue }}；</span>
                  <span v-if="item.latest_forgotten_lines">忘词：{{ item.latest_forgotten_lines }}</span>
                  <span v-if="!item.latest_start_beat_issue && !item.latest_forgotten_lines">无明显问题</span>
                  <span class="muted">（{{ item.latest_feedback_date }}）</span>
                </div>
              </div>

              <div class="confirm-table-wrap">
                <el-table :data="item.confirmations" size="small" border>
                  <el-table-column prop="member_name" label="成员" min-width="100" />
                  <el-table-column prop="role_name" label="角色" min-width="100">
                    <template #default="{ row }">
                      <span class="muted" v-if="!row.role_name">-</span>
                      <span v-else>{{ row.role_name }}</span>
                    </template>
                  </el-table-column>
                  <el-table-column label="类型" width="80">
                    <template #default="{ row }">
                      <el-tag size="small" :type="row.is_understudy ? 'warning' : 'danger'" effect="plain">
                        {{ row.is_understudy ? '替补' : '正式' }}
                      </el-tag>
                    </template>
                  </el-table-column>
                  <el-table-column label="到场确认" width="120">
                    <template #default="{ row }">
                      <el-switch
                        :model-value="row.attendance_confirmed"
                        @change="(val) => updateConfirmationField(row, 'attendance_confirmed', val)"
                      />
                    </template>
                  </el-table-column>
                  <el-table-column label="歌词熟练度" width="160">
                    <template #default="{ row }">
                      <el-select
                        :model-value="row.lyrics_proficiency"
                        size="small"
                        @change="(val) => updateConfirmationField(row, 'lyrics_proficiency', val)"
                      >
                        <el-option label="未确认" value="unconfirmed" />
                        <el-option label="熟练" value="familiar" />
                        <el-option label="需练习" value="needs_practice" />
                      </el-select>
                    </template>
                  </el-table-column>
                  <el-table-column label="需替补协助" width="110">
                    <template #default="{ row }">
                      <el-switch
                        :model-value="row.needs_understudy_help"
                        @change="(val) => updateConfirmationField(row, 'needs_understudy_help', val)"
                      />
                    </template>
                  </el-table-column>
                  <el-table-column label="确认时间" width="160">
                    <template #default="{ row }">
                      <span class="muted">{{ formatTime(row.confirmed_at) }}</span>
                    </template>
                  </el-table-column>
                </el-table>
              </div>

              <div class="item-actions">
                <div class="action-group">
                  <span class="detail-label">伴奏确认</span>
                  <el-button
                    size="small"
                    :type="item.accompaniment_confirmed ? 'success' : 'primary'"
                    :disabled="item.accompaniment_confirmed"
                    @click="confirmAccompaniment(item)"
                  >
                    <el-icon><Check /></el-icon>
                    {{ item.accompaniment_confirmed ? `已确认${item.accompaniment_confirmed_by_name ? '（' + item.accompaniment_confirmed_by_name + '）' : ''}` : '确认伴奏已备齐' }}
                  </el-button>
                </div>
                <div class="action-group">
                  <span class="detail-label">老师标注风险</span>
                  <el-button size="small" type="warning" :icon="Edit" @click="openRiskDialog(item)">标注 / 修改</el-button>
                </div>
                <div class="action-group">
                  <span class="detail-label">风险复核</span>
                  <el-button size="small" type="info" :icon="Refresh" @click="reviewItemRisks(item)">复核风险</el-button>
                </div>
              </div>
            </div>
          </el-collapse-item>
        </el-collapse>
      </div>
    </div>

    <div class="opera-card">
      <div class="section-head">
        <h3 class="section-title">待处理风险项</h3>
        <div class="risk-actions-tabs">
          <el-radio-group v-model="actionTab" size="small">
            <el-radio-button value="active">待处理</el-radio-button>
            <el-radio-button value="history">历史已解除</el-radio-button>
          </el-radio-group>
        </div>
      </div>
      <el-table 
        :data="actionTab === 'active' ? activeActions : historyActions" 
        v-loading="loading" 
        stripe 
        empty-text="暂无记录"
      >
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column prop="aria_name" label="唱段" min-width="140" />
        <el-table-column label="类型" width="140">
          <template #default="{ row }">
            <el-tag :type="flagTagType(row.action_type)" effect="plain">{{ row.action_type_display }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="说明" min-width="200" show-overflow-tooltip />
        <el-table-column label="最新原因" min-width="200" show-overflow-tooltip>
          <template #default="{ row }">
            <span v-if="row.latest_reason" class="danger-text">{{ row.latest_reason }}</span>
            <span v-else class="muted">-</span>
          </template>
        </el-table-column>
        <el-table-column label="处理人" width="100">
          <template #default="{ row }">
            <span v-if="row.handler_name">{{ row.handler_name }}</span>
            <span v-else class="muted">-</span>
          </template>
        </el-table-column>
        <el-table-column label="处理备注" min-width="140" show-overflow-tooltip>
          <template #default="{ row }">
            <span v-if="row.handler_note">{{ row.handler_note }}</span>
            <span v-else class="muted">-</span>
          </template>
        </el-table-column>
        <el-table-column label="解除来源" width="130">
          <template #default="{ row }">
            <span v-if="row.resolution_source_display">
              <el-tag size="small" type="info">{{ row.resolution_source_display }}</el-tag>
            </span>
            <span v-else class="muted">-</span>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="130">
          <template #default="{ row }">
            <div class="status-wrap">
              <el-tag :type="getStatusType(row.status)" :effect="row.auto_resolve_pending ? 'dark' : 'plain'">
                {{ getStatusDisplay(row) }}
              </el-tag>
              <el-tag v-if="row.auto_resolve_pending" size="small" type="warning" effect="dark">待确认</el-tag>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="处理时长" width="100">
          <template #default="{ row }">
            <span v-if="row.processing_duration !== null">{{ row.processing_duration }}h</span>
            <span v-else class="muted">-</span>
          </template>
        </el-table-column>
        <el-table-column label="创建时间" width="160">
          <template #default="{ row }">
            <span class="muted">{{ formatTime(row.created_at) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="处理时间" width="160">
          <template #default="{ row }">
            <span class="muted">{{ formatTime(row.resolved_at) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="{ row }">
            <div class="action-buttons">
              <el-button
                v-if="row.status === 'pending'"
                type="success"
                link
                size="small"
                @click="openHandlerDialog(row, 'resolve')"
              >标记已处理</el-button>
              <el-button
                v-if="row.auto_resolve_pending"
                type="success"
                link
                size="small"
                @click="openHandlerDialog(row, 'confirm')"
              >确认关闭</el-button>
              <el-button
                v-if="row.auto_resolve_pending"
                type="danger"
                link
                size="small"
                @click="rejectAutoResolve(row)"
              >拒绝解除</el-button>
              <el-button
                type="primary"
                link
                size="small"
                @click="openHandlerDialog(row, 'handler')"
              >设置处理人</el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog v-model="riskDialogVisible" title="老师标注风险等级与处理意见" width="520px">
      <el-form :model="riskForm" label-width="100px">
        <el-form-item label="唱段">
          <span>{{ riskForm.aria_name }}</span>
        </el-form-item>
        <el-form-item label="风险等级">
          <el-radio-group v-model="riskForm.risk_level">
            <el-radio value="none">无风险</el-radio>
            <el-radio value="low">低</el-radio>
            <el-radio value="medium">中</el-radio>
            <el-radio value="high">高</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="处理意见">
          <el-input v-model="riskForm.teacher_comment" type="textarea" :rows="4" placeholder="针对该唱段的风险处理建议" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="riskDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitRisk">保存</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="handlerDialogVisible" :title="handlerDialogTitle" width="520px">
      <el-form :model="handlerForm" label-width="100px">
        <el-form-item label="风险项">
          <span>{{ handlerForm.aria_name }} - {{ handlerForm.action_type_display }}</span>
        </el-form-item>
        <el-form-item label="处理人" v-if="handlerDialogType !== 'reject'">
          <el-select v-model="handlerForm.handler_id" placeholder="请选择处理人" filterable>
            <el-option
              v-for="member in store.members"
              :key="member.id"
              :label="member.name"
              :value="member.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item :label="handlerDialogType === 'reject' ? '拒绝原因' : '处理备注'">
          <el-input v-model="handlerForm.handler_note" type="textarea" :rows="4" :placeholder="handlerDialogType === 'reject' ? '请输入拒绝解除的原因' : '请输入处理备注'" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="handlerDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitHandlerAction">{{ handlerDialogType === 'resolve' ? '标记已处理' : handlerDialogType === 'confirm' ? '确认关闭' : handlerDialogType === 'reject' ? '提交' : '保存' }}</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useOperaStore } from '@/stores/opera'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  ArrowLeft, Refresh, MagicStick, Warning, User, Switch, Microphone,
  Document, Bell, Check, Edit
} from '@element-plus/icons-vue'
import StatsCard from '@/components/StatsCard.vue'

const route = useRoute()
const router = useRouter()
const store = useOperaStore()

const check = computed(() => store.getRehearsalCheckById(route.params.id))
const items = ref([])
const dashboard = ref(null)
const loading = ref(false)
const generating = ref(false)
const activeCollapse = ref([])
const riskTab = ref('active')
const actionTab = ref('active')
const historyActions = ref([])

const riskDialogVisible = ref(false)
const riskForm = reactive({
  itemId: null,
  aria_name: '',
  risk_level: 'none',
  teacher_comment: ''
})

const handlerDialogVisible = ref(false)
const handlerDialogType = ref('')
const handlerForm = reactive({
  riskId: null,
  aria_name: '',
  action_type_display: '',
  handler_id: null,
  handler_note: ''
})

const handlerDialogTitle = computed(() => {
  const titles = {
    resolve: '标记风险已处理',
    confirm: '确认关闭风险',
    handler: '设置处理人',
    reject: '拒绝自动解除'
  }
  return titles[handlerDialogType.value] || '处理风险'
})

const activeRiskItems = computed(() => {
  if (!dashboard.value) return []
  return dashboard.value.risk_items.filter(item => item.has_active_risks)
})

const historyRiskItems = computed(() => {
  if (!dashboard.value) return []
  return dashboard.value.risk_items.filter(item => !item.has_active_risks)
})

const activeActions = computed(() => store.riskActions.filter(a => a.is_active))
const pendingActions = computed(() => store.riskActions.filter(a => a.status === 'pending'))

onMounted(async () => {
  await store.loadPrograms()
  await store.loadRehearsalChecks()
  await store.loadMembers()
  await loadAll()
})

async function loadAll() {
  loading.value = true
  try {
    const [itemsData, dashboardData] = await Promise.all([
      store.getRehearsalCheckItems(route.params.id),
      store.getRiskDashboard(route.params.id)
    ])
    items.value = itemsData
    dashboard.value = dashboardData
    if (itemsData.length && !activeCollapse.value.length) {
      activeCollapse.value = [itemsData[0].id]
    }
  } finally {
    loading.value = false
  }
  await store.loadRiskActions(route.params.id)
  historyActions.value = await store.loadHistoryRisks(route.params.id)
}

function flagCount(actionType) {
  if (!dashboard.value) return 0
  const item = dashboard.value.summary.flag_breakdown.find(f => f.action_type === actionType)
  return item ? item.count : 0
}

const FLAG_LABEL_MAP = {
  '未确认到场': 'attendance',
  '无替补': 'understudy',
  '排练反馈问题': 'feedback',
  '伴奏未确认': 'accompaniment',
  '老师标注风险': 'teacher_risk'
}

function flagTagType(labelOrType) {
  const type = FLAG_LABEL_MAP[labelOrType] || labelOrType
  const map = {
    attendance: 'danger',
    understudy: 'warning',
    feedback: 'success',
    accompaniment: 'primary',
    teacher_risk: 'danger'
  }
  return map[type] || 'info'
}

function riskTagType(level) {
  const map = { none: 'info', low: 'success', medium: 'warning', high: 'danger' }
  return map[level] || 'info'
}

function getStatusType(status) {
  const map = {
    pending: 'danger',
    auto_resolved: 'warning',
    manually_resolved: 'success',
    confirmed_closed: 'success'
  }
  return map[status] || 'info'
}

function getStatusDisplay(row) {
  const statusMap = {
    pending: '待处理',
    auto_resolved: '自动解除',
    manually_resolved: '手动解除',
    confirmed_closed: '已确认关闭'
  }
  return statusMap[row.status] || row.status
}

function formatTime(value) {
  if (!value) return '-'
  return value.replace('T', ' ').substring(0, 16)
}

function handleRiskReviewResults(results) {
  if (!results || results.length === 0) return
  
  const created = results.filter(r => r.action === 'created')
  if (created.length > 0) {
    ElMessage.info(`新增 ${created.length} 项风险待处理项`)
  }
  
  const autoResolved = results.filter(r => r.action === 'suggest_auto_resolve')
  if (autoResolved.length > 0) {
    ElMessage.success(`系统自动复核发现 ${autoResolved.length} 项风险已解除，待管理员确认`)
  }
  
  const keptPending = results.filter(r => r.action === 'keep_pending')
  if (keptPending.length > 0) {
    ElMessage.info(`${keptPending.length} 项风险仍然存在，已更新最新原因`)
  }
}

async function updateConfirmationField(confirmation, field, value) {
  const payload = { [field]: value }
  if (field === 'attendance_confirmed' && value) {
    payload.confirmed_at = new Date().toISOString()
  }
  try {
    const updated = await store.updateConfirmation(confirmation.id, payload)
    const item = items.value.find(i => i.id === confirmation.check_item)
    if (item) {
      const idx = item.confirmations.findIndex(c => c.id === confirmation.id)
      if (idx !== -1) item.confirmations[idx] = { ...item.confirmations[idx], ...updated }
    }
    
    if (updated.risk_review_results) {
      handleRiskReviewResults(updated.risk_review_results)
    }
    
    ElMessage.success('确认已更新')
    await refreshDashboard()
  } catch (e) {
    ElMessage.error('更新失败')
  }
}

async function confirmAccompaniment(item) {
  try {
    const updated = await store.confirmAccompanimentForItem(item.id)
    const idx = items.value.findIndex(i => i.id === item.id)
    if (idx !== -1) items.value[idx] = { ...items.value[idx], ...updated }
    
    if (updated.risk_review_results) {
      handleRiskReviewResults(updated.risk_review_results)
    }
    
    ElMessage.success('伴奏确认成功')
    await refreshDashboard()
  } catch (e) {
    ElMessage.error('伴奏确认失败')
  }
}

async function reviewItemRisks(item) {
  try {
    const result = await store.reviewRisksForItem(item.id)
    handleRiskReviewResults(result.results)
    ElMessage.success(`已复核 ${result.reviewed_count} 项风险`)
    await refreshDashboard()
  } catch (e) {
    ElMessage.error('复核失败')
  }
}

function openRiskDialog(item) {
  riskForm.itemId = item.id
  riskForm.aria_name = item.aria_name
  riskForm.risk_level = item.risk_level || 'none'
  riskForm.teacher_comment = item.teacher_comment || ''
  riskDialogVisible.value = true
}

async function submitRisk() {
  try {
    const updated = await store.setItemRisk(riskForm.itemId, {
      risk_level: riskForm.risk_level,
      teacher_comment: riskForm.teacher_comment
    })
    const idx = items.value.findIndex(i => i.id === riskForm.itemId)
    if (idx !== -1) items.value[idx] = { ...items.value[idx], ...updated }
    
    if (updated.risk_review_results) {
      handleRiskReviewResults(updated.risk_review_results)
    }
    
    ElMessage.success('风险标注已保存')
    riskDialogVisible.value = false
    await refreshDashboard()
  } catch (e) {
    ElMessage.error('保存失败')
  }
}

function openHandlerDialog(row, type) {
  handlerDialogType.value = type
  handlerForm.riskId = row.id
  handlerForm.aria_name = row.aria_name
  handlerForm.action_type_display = row.action_type_display
  handlerForm.handler_id = row.handler || null
  handlerForm.handler_note = row.handler_note || ''
  handlerDialogVisible.value = true
}

async function submitHandlerAction() {
  try {
    let result
    if (handlerDialogType.value === 'resolve') {
      result = await store.resolveRiskActionById(
        handlerForm.riskId,
        handlerForm.handler_id,
        handlerForm.handler_note
      )
      ElMessage.success('已标记为已处理')
    } else if (handlerDialogType.value === 'confirm') {
      result = await store.confirmCloseRiskActionById(
        handlerForm.riskId,
        handlerForm.handler_id,
        handlerForm.handler_note
      )
      ElMessage.success('已确认关闭')
    } else if (handlerDialogType.value === 'handler') {
      result = await store.updateRiskActionHandlerById(
        handlerForm.riskId,
        handlerForm.handler_id,
        handlerForm.handler_note
      )
      ElMessage.success('处理人已更新')
    }
    
    const idx = store.riskActions.findIndex(a => a.id === handlerForm.riskId)
    if (idx !== -1) store.riskActions[idx] = { ...store.riskActions[idx], ...result }
    
    handlerDialogVisible.value = false
    await refreshDashboard()
  } catch (e) {
    ElMessage.error('操作失败')
  }
}

async function rejectAutoResolve(row) {
  try {
    await ElMessageBox.prompt('请输入拒绝解除的原因', '拒绝确认', {
      confirmButtonText: '确认拒绝',
      cancelButtonText: '取消',
      inputType: 'textarea',
      inputPlaceholder: '请说明拒绝解除的原因...',
      type: 'warning'
    }).then(async ({ value: note }) => {
      await store.rejectAutoResolveById(row.id, note)
      ElMessage.success('已拒绝自动解除，风险重新标记为待处理')
      await refreshDashboard()
    }).catch(() => {})
  } catch (e) {
    ElMessage.error('操作失败')
  }
}

async function handleGenerateActions() {
  generating.value = true
  try {
    const result = await store.runGenerateRiskActions(route.params.id)
    ElMessage.success(`已生成待处理项，新增 ${result.created_count} 项`)
    await refreshDashboard()
  } catch (e) {
    ElMessage.error('生成失败')
  } finally {
    generating.value = false
  }
}

async function handleResolve(action) {
  openHandlerDialog(action, 'resolve')
}

async function refreshDashboard() {
  dashboard.value = await store.getRiskDashboard(route.params.id)
  await store.loadRehearsalChecks()
  await store.loadRiskActions(route.params.id)
  historyActions.value = await store.loadHistoryRisks(route.params.id)
}
</script>

<style lang="scss" scoped>
.header-actions {
  display: flex;
  gap: 12px;
}

.check-info {
  .info-row {
    display: flex;
    gap: 24px;
    flex-wrap: wrap;

    .info-item {
      flex: 1;
      min-width: 160px;
    }
  }
}

.dashboard-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}

.section-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;

  .muted {
    font-size: 13px;
  }
}

.risk-tabs, .risk-actions-tabs {
  margin-left: auto;
}

.muted {
  color: #999;
  font-size: 12px;
}

.danger-text {
  color: #C41E3A;
  font-size: 12px;
}

.risk-flag {
  margin-right: 6px;
  margin-bottom: 4px;
}

.item-title {
  display: flex;
  align-items: center;
  gap: 8px;

  .item-order {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: #C41E3A;
    color: #fff;
    font-size: 12px;
    font-weight: bold;
  }

  .item-name {
    font-weight: 600;
    color: #333;
  }
}

.item-detail {
  padding: 12px 8px;

  .detail-block {
    margin-bottom: 12px;
  }
}

.confirm-table-wrap {
  margin: 8px 0 16px;
}

.item-actions {
  display: flex;
  gap: 32px;
  flex-wrap: wrap;

  .action-group {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }
}

.status-wrap {
  display: flex;
  align-items: center;
  gap: 4px;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
</style>
