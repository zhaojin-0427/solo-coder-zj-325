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
        <el-tag type="danger">按风险分值排序</el-tag>
      </div>
      <el-table :data="dashboard?.risk_items || []" v-loading="loading" stripe empty-text="暂无风险唱段，状态良好">
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
        <el-table-column label="未确认成员" min-width="160">
          <template #default="{ row }">
            <span v-if="!row.unconfirmed_members.length" class="muted">-</span>
            <span v-else>{{ row.unconfirmed_members.map(m => m.name).join('、') }}</span>
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
              </div>
            </div>
          </el-collapse-item>
        </el-collapse>
      </div>
    </div>

    <div class="opera-card">
      <div class="section-head">
        <h3 class="section-title">待处理风险项</h3>
        <span class="muted">已生成 {{ pendingActions.length }} 项待处理</span>
      </div>
      <el-table :data="store.riskActions" v-loading="loading" stripe empty-text="暂无待处理项，可点击「一键生成待处理项」">
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column prop="aria_name" label="唱段" min-width="160" />
        <el-table-column label="类型" width="140">
          <template #default="{ row }">
            <el-tag :type="flagTagType(row.action_type)" effect="plain">{{ row.action_type_display }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="说明" min-width="280" show-overflow-tooltip />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'pending' ? 'danger' : 'success'">{{ row.status_display }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="{ row }">
            <el-button
              v-if="row.status === 'pending'"
              type="success"
              link
              @click="handleResolve(row)"
            >标记已处理</el-button>
            <span v-else class="muted">{{ formatTime(row.resolved_at) }}</span>
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

const riskDialogVisible = ref(false)
const riskForm = reactive({
  itemId: null,
  aria_name: '',
  risk_level: 'none',
  teacher_comment: ''
})

const pendingActions = computed(() => store.riskActions.filter(a => a.status === 'pending'))

onMounted(async () => {
  await store.loadPrograms()
  await store.loadRehearsalChecks()
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

function formatTime(value) {
  if (!value) return '-'
  return value.replace('T', ' ').substring(0, 16)
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
    ElMessage.success('伴奏确认成功')
    await refreshDashboard()
  } catch (e) {
    ElMessage.error('伴奏确认失败')
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
    ElMessage.success('风险标注已保存')
    riskDialogVisible.value = false
    await refreshDashboard()
  } catch (e) {
    ElMessage.error('保存失败')
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
  ElMessageBox.confirm(`确定将「${action.aria_name} - ${action.action_type_display}」标记为已处理？`, '处理确认', { type: 'success' })
    .then(async () => {
      await store.resolveRiskActionById(action.id)
      ElMessage.success('已标记为已处理')
    }).catch(() => {})
}

async function refreshDashboard() {
  dashboard.value = await store.getRiskDashboard(route.params.id)
  await store.loadRehearsalChecks()
  await store.loadRiskActions(route.params.id)
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

.muted {
  color: #999;
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
</style>
