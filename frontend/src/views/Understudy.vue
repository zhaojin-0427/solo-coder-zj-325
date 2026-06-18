<template>
  <div class="page-container">
    <div class="page-header">
      <h2>替补调整</h2>
      <el-button type="primary" @click="openAddDialog">
        <el-icon><Plus /></el-icon>
        申请替补
      </el-button>
    </div>

    <el-tabs v-model="activeTab" class="understudy-tabs">
      <el-tab-pane label="待处理申请" name="pending">
        <div class="opera-card">
          <div v-if="pendingChanges.length === 0" class="empty-state">
            <el-icon><CircleCheck /></el-icon>
            <p>暂无待处理的替补申请</p>
          </div>
          <div v-else class="change-list">
            <div 
              v-for="item in pendingChanges" 
              :key="item.id" 
              class="change-card pending"
            >
              <div class="change-header">
                <div class="change-info">
                  <el-icon class="warning-icon" :size="24"><Warning /></el-icon>
                  <div>
                    <h4>替补申请</h4>
                    <p class="change-date">申请日期：{{ item.date }}</p>
                  </div>
                </div>
                <span class="tag pending">待处理</span>
              </div>
              
              <div class="change-body">
                <div class="members-row">
                  <div class="member-block">
                    <div class="block-label">原分配成员</div>
                    <div class="member-info">
                      <div class="member-avatar">
                        {{ getOriginalMemberName(item).charAt(0) }}
                      </div>
                      <div>
                        <div class="member-name">{{ getOriginalMemberName(item) }}</div>
                        <div class="member-role">{{ getAssignmentAria(item) }}</div>
                      </div>
                    </div>
                  </div>
                  
                  <div class="arrow-icon">
                    <el-icon :size="24"><Switch /></el-icon>
                  </div>
                  
                  <div class="member-block">
                    <div class="block-label">替补成员</div>
                    <div class="member-info">
                      <div class="member-avatar understudy">
                        {{ getMemberName(item.substitute_member).charAt(0) }}
                      </div>
                      <div>
                        <div class="member-name">{{ getMemberName(item.substitute_member) }}</div>
                        <div class="member-role">{{ getMemberPhone(item.substitute_member) }}</div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div class="reason-section">
                  <div class="block-label">替补原因</div>
                  <div class="reason-text">{{ item.reason }}</div>
                </div>
              </div>
              
              <div class="change-actions">
                <el-button type="success" @click="approveChange(item)">
                  <el-icon><Check /></el-icon>
                  同意
                </el-button>
                <el-button type="danger" @click="rejectChange(item)">
                  <el-icon><Close /></el-icon>
                  拒绝
                </el-button>
                <el-button @click="openEditDialog(item)">
                  <el-icon><Edit /></el-icon>
                  调整
                </el-button>
              </div>
            </div>
          </div>
        </div>
      </el-tab-pane>

      <el-tab-pane label="历史记录" name="history">
        <div class="opera-card">
          <div v-if="completedChanges.length === 0" class="empty-state">
            <el-icon><Document /></el-icon>
            <p>暂无历史记录</p>
          </div>
          <div v-else class="change-list">
            <div 
              v-for="item in completedChanges" 
              :key="item.id" 
              class="change-card history"
            >
              <div class="change-header">
                <div class="change-info">
                  <el-icon 
                    class="history-icon" 
                    :size="24"
                    :class="item.status === 'completed' ? 'success' : 'rejected'"
                  >
                    <component :is="item.status === 'completed' ? CircleCheck : CircleClose" />
                  </el-icon>
                  <div>
                    <h4>{{ item.status === 'completed' ? '已完成' : '已拒绝' }}</h4>
                    <p class="change-date">处理日期：{{ item.date }}</p>
                  </div>
                </div>
                <span :class="['tag', item.status === 'completed' ? 'confirmed' : 'inactive']">
                  {{ item.status === 'completed' ? '已完成' : '已拒绝' }}
                </span>
              </div>
              
              <div class="change-body">
                <div class="members-row">
                  <div class="member-block">
                    <div class="member-info">
                      <div class="member-avatar">
                        {{ getOriginalMemberName(item).charAt(0) }}
                      </div>
                      <div>
                        <div class="member-name">{{ getOriginalMemberName(item) }}</div>
                      </div>
                    </div>
                  </div>
                  
                  <div class="arrow-icon">
                    <el-icon :size="20"><ArrowRight /></el-icon>
                  </div>
                  
                  <div class="member-block">
                    <div class="member-info">
                      <div class="member-avatar understudy">
                        {{ getMemberName(item.substitute_member).charAt(0) }}
                      </div>
                      <div>
                        <div class="member-name">{{ getMemberName(item.substitute_member) }}</div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div class="reason-section">
                  <div class="reason-text">{{ item.reason }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>

    <el-dialog v-model="dialogVisible" :title="editingItem ? '调整申请' : '申请替补'" width="600px">
      <el-form :model="formData" label-width="120px" ref="formRef">
        <el-form-item label="原分配" prop="original_assignment" :rules="[{ required: true }]">
          <el-select v-model="formData.original_assignment" style="width: 100%">
            <el-option 
              v-for="a in confirmedAssignments" 
              :key="a.id" 
              :label="getAssignmentDisplay(a)" 
              :value="a.id" 
            />
          </el-select>
        </el-form-item>
        <el-form-item label="替补成员" prop="substitute_member" :rules="[{ required: true }]">
          <el-select v-model="formData.substitute_member" style="width: 100%">
            <el-option 
              v-for="m in understudyMembers" 
              :key="m.id" 
              :label="m.name" 
              :value="m.id" 
            />
          </el-select>
        </el-form-item>
        <el-form-item label="替补原因" prop="reason" :rules="[{ required: true }]">
          <el-input 
            v-model="formData.reason" 
            type="textarea" 
            :rows="4"
            placeholder="请说明替补原因" 
          />
        </el-form-item>
        <el-form-item label="日期" prop="date" :rules="[{ required: true }]">
          <el-date-picker v-model="formData.date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useOperaStore } from '@/stores/opera'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  Plus, Warning, CircleCheck, Document, Switch, Check, Close, Edit, ArrowRight, CircleClose 
} from '@element-plus/icons-vue'

const store = useOperaStore()
const activeTab = ref('pending')
const dialogVisible = ref(false)
const editingItem = ref(null)
const formRef = ref(null)

const formData = reactive({
  original_assignment: null,
  substitute_member: null,
  reason: '',
  date: '',
  status: 'pending'
})

const pendingChanges = computed(() => 
  store.understudyChanges.filter(c => c.status === 'pending')
    .sort((a, b) => new Date(b.date) - new Date(a.date))
)

const completedChanges = computed(() => 
  store.understudyChanges.filter(c => c.status !== 'pending')
    .sort((a, b) => new Date(b.date) - new Date(a.date))
)

const confirmedAssignments = computed(() => 
  store.assignments.filter(a => a.status === 'confirmed' && !a.is_understudy)
)

const understudyMembers = computed(() => 
  store.members.filter(m => m.is_understudy)
)

onMounted(async () => {
  await Promise.all([
    store.loadUnderstudyChanges(),
    store.loadAssignments(),
    store.loadMembers(),
    store.loadArias()
  ])
})

function getMemberName(memberId) {
  const member = store.members.find(m => m.id === memberId)
  return member ? member.name : '未知'
}

function getMemberPhone(memberId) {
  const member = store.members.find(m => m.id === memberId)
  return member ? member.phone : ''
}

function getOriginalMemberName(change) {
  const assignment = store.assignments.find(a => a.id === change.original_assignment)
  if (assignment) {
    return getMemberName(assignment.member)
  }
  return '未知'
}

function getAssignmentAria(change) {
  const assignment = store.assignments.find(a => a.id === change.original_assignment)
  if (assignment) {
    const aria = store.arias.find(a => a.id === assignment.aria)
    return aria ? aria.name : ''
  }
  return ''
}

function getAssignmentDisplay(assignment) {
  const aria = store.arias.find(a => a.id === assignment.aria)
  const member = store.members.find(m => m.id === assignment.member)
  const ariaName = aria ? aria.name : '未知唱段'
  const memberName = member ? member.name : '未知成员'
  return `${ariaName} - ${memberName}`
}

function openAddDialog() {
  editingItem.value = null
  Object.assign(formData, {
    original_assignment: null,
    substitute_member: null,
    reason: '',
    date: new Date().toISOString().split('T')[0],
    status: 'pending'
  })
  dialogVisible.value = true
}

function openEditDialog(item) {
  editingItem.value = item
  Object.assign(formData, { ...item })
  dialogVisible.value = true
}

async function handleSubmit() {
  try {
    await formRef.value.validate()
    if (editingItem.value) {
      await store.editUnderstudyChange(editingItem.value.id, formData)
      ElMessage.success('申请更新成功')
    } else {
      await store.addUnderstudyChange(formData)
      ElMessage.success('申请提交成功')
    }
    dialogVisible.value = false
  } catch (error) {
    if (error !== false) {
      ElMessage.error('操作失败')
    }
  }
}

async function approveChange(item) {
  ElMessageBox.confirm('确定同意该替补申请吗？', '确认', { type: 'success' })
    .then(async () => {
      await store.editUnderstudyChange(item.id, { status: 'completed' })
      ElMessage.success('已同意')
    }).catch(() => {})
}

async function rejectChange(item) {
  ElMessageBox.confirm('确定拒绝该替补申请吗？', '确认', { type: 'warning' })
    .then(async () => {
      await store.editUnderstudyChange(item.id, { status: 'rejected' })
      ElMessage.success('已拒绝')
    }).catch(() => {})
}
</script>

<style lang="scss" scoped>
.understudy-tabs {
  :deep(.el-tabs__item.is-active) {
    color: #C41E3A !important;
  }
  
  :deep(.el-tabs__active-bar) {
    background-color: #D4AF37 !important;
  }
}

.change-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.change-card {
  background: #FDF6E3;
  border-radius: 12px;
  border: 1px solid #E8DCC8;
  overflow: hidden;
  
  &.pending {
    border-left: 4px solid #FF9800;
  }
  
  &.history {
    border-left: 4px solid #D4AF37;
  }
}

.change-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: linear-gradient(to right, rgba(212, 175, 55, 0.1), transparent);
  border-bottom: 1px solid #E8DCC8;
}

.change-info {
  display: flex;
  align-items: center;
  gap: 12px;
  
  h4 {
    margin: 0 0 4px 0;
    color: #333;
    font-size: 16px;
  }
  
  .change-date {
    margin: 0;
    font-size: 13px;
    color: #666;
  }
}

.warning-icon {
  color: #FF9800;
}

.history-icon {
  &.success {
    color: #2e7d32;
  }
  
  &.rejected {
    color: #C41E3A;
  }
}

.change-body {
  padding: 20px;
}

.members-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 24px;
  margin-bottom: 16px;
}

.member-block {
  text-align: center;
  
  .block-label {
    font-size: 12px;
    color: #999;
    margin-bottom: 8px;
  }
}

.member-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.member-avatar {
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, #C41E3A, #8B0000);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 20px;
  
  &.understudy {
    background: linear-gradient(135deg, #D4AF37, #B8860B);
  }
}

.member-name {
  font-weight: 600;
  color: #333;
  font-size: 15px;
}

.member-role {
  font-size: 13px;
  color: #666;
}

.arrow-icon {
  color: #D4AF37;
}

.reason-section {
  background: white;
  padding: 12px 16px;
  border-radius: 8px;
  border-left: 3px solid #D4AF37;
  
  .block-label {
    font-size: 12px;
    color: #999;
    margin-bottom: 4px;
  }
  
  .reason-text {
    color: #333;
    font-size: 14px;
  }
}

.change-actions {
  display: flex;
  justify-content: center;
  gap: 12px;
  padding: 16px 20px;
  background: white;
  border-top: 1px solid #E8DCC8;
}
</style>
