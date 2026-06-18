<template>
  <div class="page-container">
    <div class="page-header">
      <h2>唱段分配</h2>
      <div class="header-actions">
        <el-select v-model="selectedProgram" placeholder="选择节目" style="width: 200px; margin-right: 12px" @change="loadData">
          <el-option v-for="p in store.programs" :key="p.id" :label="p.name" :value="p.id" />
        </el-select>
        <el-button type="warning" @click="handleAutoAssign" :disabled="!selectedProgram">
          <el-icon><MagicStick /></el-icon>
          自动分配
        </el-button>
        <el-button type="primary" @click="openAddDialog">
          <el-icon><Plus /></el-icon>
          手动分配
        </el-button>
      </div>
    </div>

    <el-row :gutter="20">
      <el-col :span="12">
        <div class="opera-card">
          <h3 class="section-title">唱段列表</h3>
          <div v-if="programArias.length === 0" class="empty-state">
            <el-icon><VideoPlay /></el-icon>
            <p>请先选择节目查看唱段</p>
          </div>
          <div v-else class="aria-list">
            <div 
              v-for="aria in programArias" 
              :key="aria.id" 
              class="aria-item"
              :class="{ active: selectedAria?.id === aria.id }"
              @click="selectAria(aria)"
            >
              <div class="aria-header">
                <span class="aria-order">{{ aria.order_index }}</span>
                <div class="aria-info">
                  <div class="aria-name">{{ aria.name }}</div>
                  <div class="aria-meta">
                    <span class="tag active">{{ aria.role_type_display || getRoleTypeDisplay(aria.role_type) }}</span>
                    <span class="duration">{{ Math.ceil(aria.duration / 60) }}分钟</span>
                  </div>
                </div>
              </div>
              <div class="aria-lyrics">{{ aria.lyrics }}</div>
            </div>
          </div>
        </div>
      </el-col>

      <el-col :span="12">
        <div class="opera-card">
          <h3 class="section-title">成员报名 & 分配情况</h3>
          <div v-if="!selectedAria" class="empty-state">
            <el-icon><Pointer /></el-icon>
            <p>请选择左侧唱段查看分配详情</p>
          </div>
          <div v-else>
            <div class="selected-aria-info">
              <h4>{{ selectedAria.name }}</h4>
              <p>需要角色：<span class="tag active">{{ selectedAria.role_type_display || getRoleTypeDisplay(selectedAria.role_type) }}</span></p>
            </div>

            <div class="assignment-section">
              <h5>当前分配</h5>
              <div v-if="getAriaAssignments(selectedAria.id).length === 0" class="empty-state small">
                <p>暂无分配</p>
              </div>
              <div v-else class="assignment-list">
                <div 
                  v-for="assignment in getAriaAssignments(selectedAria.id)" 
                  :key="assignment.id"
                  class="assignment-item"
                >
                  <div class="assignment-info">
                    <div class="member-avatar">
                      {{ getMemberName(assignment.member).charAt(0) }}
                    </div>
                    <div class="member-info">
                      <div class="member-name">
                        {{ getMemberName(assignment.member) }}
                        <span :class="['tag', assignment.is_understudy ? 'understudy' : 'main']">
                          {{ assignment.is_understudy ? '替补' : '主演' }}
                        </span>
                      </div>
                      <div class="member-phone">{{ getMemberPhone(assignment.member) }}</div>
                    </div>
                  </div>
                  <div class="assignment-actions">
                    <span :class="['tag', assignment.status]">
                      {{ assignment.status === 'confirmed' ? '已确认' : '待确认' }}
                    </span>
                    <el-button type="primary" link size="small" @click="openEditDialog(assignment)">调整</el-button>
                    <el-button type="danger" link size="small" @click="removeAssignment(assignment)">删除</el-button>
                  </div>
                </div>
              </div>
            </div>

            <div class="assignment-section">
              <h5>适合成员（角色类型匹配）</h5>
              <div v-if="suitableMembers.length === 0" class="empty-state small">
                <p>暂无适合的成员</p>
              </div>
              <div v-else class="suitable-list">
                <div 
                  v-for="member in suitableMembers" 
                  :key="member.id"
                  class="suitable-item"
                >
                  <div class="member-avatar small">
                    {{ member.name.charAt(0) }}
                  </div>
                  <div class="member-info">
                    <div class="member-name">{{ member.name }}</div>
                    <div class="member-meta">
                      <span class="tag" :class="member.is_understudy ? 'understudy' : 'main'">
                        {{ member.is_understudy ? '替补成员' : '正式成员' }}
                      </span>
                      <span class="available">{{ member.available_times?.join('、') }}</span>
                    </div>
                  </div>
                  <el-button 
                    type="primary" 
                    size="small" 
                    @click="quickAssign(member)"
                    :disabled="isMemberAssigned(member.id)"
                  >
                    分配
                  </el-button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </el-col>
    </el-row>

    <el-dialog v-model="dialogVisible" :title="editingAssignment ? '调整分配' : '新增分配'" width="500px">
      <el-form :model="formData" label-width="100px" ref="formRef">
        <el-form-item label="唱段" prop="aria" :rules="[{ required: true }]">
          <el-select v-model="formData.aria" style="width: 100%">
            <el-option v-for="a in programArias" :key="a.id" :label="a.name" :value="a.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="成员" prop="member" :rules="[{ required: true }]">
          <el-select v-model="formData.member" style="width: 100%">
            <el-option v-for="m in store.members" :key="m.id" :label="m.name" :value="m.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="角色" prop="role" :rules="[{ required: true }]">
          <el-select v-model="formData.role" style="width: 100%">
            <el-option v-for="r in programRoles" :key="r.id" :label="r.name" :value="r.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="是否替补" prop="is_understudy">
          <el-switch v-model="formData.is_understudy" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="formData.status">
            <el-radio value="pending">待确认</el-radio>
            <el-radio value="confirmed">已确认</el-radio>
          </el-radio-group>
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
import { Plus, MagicStick, VideoPlay, Pointer } from '@element-plus/icons-vue'

const store = useOperaStore()
const selectedProgram = ref(null)
const selectedAria = ref(null)
const dialogVisible = ref(false)
const editingAssignment = ref(null)
const formRef = ref(null)

const formData = reactive({
  aria: null,
  member: null,
  role: null,
  is_understudy: false,
  status: 'pending'
})

const programArias = computed(() => {
  if (!selectedProgram.value) return []
  return store.arias.filter(a => a.program === selectedProgram.value).sort((a, b) => a.order_index - b.order_index)
})

const programRoles = computed(() => {
  if (!selectedProgram.value) return []
  return store.roles.filter(r => r.program === selectedProgram.value)
})

const suitableMembers = computed(() => {
  if (!selectedAria.value) return []
  return store.members.filter(m => m.role_types?.includes(selectedAria.value.role_type))
})

onMounted(async () => {
  await Promise.all([
    store.loadPrograms(),
    store.loadArias(),
    store.loadRoles(),
    store.loadMembers(),
    store.loadAssignments()
  ])
  if (store.programs.length > 0) {
    selectedProgram.value = store.programs[0].id
    await loadData()
  }
})

async function loadData() {
  if (selectedProgram.value) {
    await Promise.all([
      store.loadArias(selectedProgram.value),
      store.loadRoles(selectedProgram.value),
      store.loadAssignments(selectedProgram.value)
    ])
    selectedAria.value = null
  }
}

function selectAria(aria) {
  selectedAria.value = aria
}

function getAriaAssignments(ariaId) {
  return store.assignments.filter(a => a.aria === ariaId)
}

function getMemberName(memberId) {
  const member = store.members.find(m => m.id === memberId)
  return member ? member.name : '未知'
}

function getMemberPhone(memberId) {
  const member = store.members.find(m => m.id === memberId)
  return member ? member.phone : ''
}

function isMemberAssigned(memberId) {
  if (!selectedAria.value) return false
  return getAriaAssignments(selectedAria.value).some(a => a.member === memberId)
}

function openAddDialog() {
  editingAssignment.value = null
  Object.assign(formData, {
    aria: selectedAria.value?.id || null,
    member: null,
    role: null,
    is_understudy: false,
    status: 'pending'
  })
  dialogVisible.value = true
}

function openEditDialog(assignment) {
  editingAssignment.value = assignment
  Object.assign(formData, { ...assignment })
  dialogVisible.value = true
}

async function handleSubmit() {
  try {
    await formRef.value.validate()
    if (editingAssignment.value) {
      await store.editAssignment(editingAssignment.value.id, formData)
      ElMessage.success('分配更新成功')
    } else {
      await store.addAssignment(formData)
      ElMessage.success('分配创建成功')
    }
    dialogVisible.value = false
  } catch (error) {
    if (error !== false) {
      ElMessage.error('操作失败')
    }
  }
}

function quickAssign(member) {
  if (!selectedAria.value) return
  const matchingRole = programRoles.value.find(r => r.role_type === selectedAria.value.role_type)
  const data = {
    aria: selectedAria.value.id,
    member: member.id,
    role: matchingRole?.id || null,
    is_understudy: member.is_understudy,
    status: 'confirmed'
  }
  store.addAssignment(data).then(() => {
    ElMessage.success('分配成功')
  })
}

function removeAssignment(assignment) {
  ElMessageBox.confirm(`确定要取消该分配吗？`, '删除确认', { type: 'warning' })
    .then(async () => {
      await store.removeAssignment(assignment.id)
      ElMessage.success('已取消分配')
    }).catch(() => {})
}

async function handleAutoAssign() {
  if (!selectedProgram.value) return
  ElMessageBox.confirm(
    '自动分配将根据角色类型和成员能力自动匹配，确定要执行吗？',
    '自动分配确认',
    { type: 'warning' }
  ).then(async () => {
    const result = await store.runAutoAssign(selectedProgram.value)
    ElMessage.success(`自动分配完成，共分配 ${result.count} 个唱段`)
  }).catch(() => {})
}

function getRoleTypeDisplay(roleType) {
  const typeMap = {
    'sheng': '生',
    'dan': '旦',
    'jing': '净',
    'mo': '末',
    'chou': '丑'
  }
  return typeMap[roleType] || roleType
}
</script>

<style lang="scss" scoped>
.header-actions {
  display: flex;
  align-items: center;
}

.aria-list {
  max-height: 600px;
  overflow-y: auto;
}

.aria-item {
  padding: 16px;
  background: #FDF6E3;
  border-radius: 8px;
  margin-bottom: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  
  &:hover {
    background: #F5E6D3;
  }
  
  &.active {
    border-color: #C41E3A;
    background: #FFF5F5;
  }
}

.aria-header {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 8px;
}

.aria-order {
  width: 28px;
  height: 28px;
  background: linear-gradient(135deg, #C41E3A, #8B0000);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 14px;
  flex-shrink: 0;
}

.aria-info {
  flex: 1;
}

.aria-name {
  font-weight: 600;
  color: #C41E3A;
  font-size: 16px;
  margin-bottom: 4px;
}

.aria-meta {
  display: flex;
  align-items: center;
  gap: 12px;
}

.duration {
  font-size: 13px;
  color: #666;
}

.aria-lyrics {
  color: #666;
  font-size: 13px;
  line-height: 1.6;
  padding-left: 40px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.selected-aria-info {
  background: linear-gradient(135deg, #FFF5F5, #FDF6E3);
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 20px;
  
  h4 {
    margin: 0 0 8px 0;
    color: #C41E3A;
    font-size: 18px;
  }
  
  p {
    margin: 0;
    color: #666;
  }
}

.assignment-section {
  margin-bottom: 24px;
  
  &:last-child {
    margin-bottom: 0;
  }
  
  h5 {
    margin: 0 0 12px 0;
    color: #333;
    font-size: 15px;
    padding-left: 10px;
    border-left: 3px solid #D4AF37;
  }
}

.assignment-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.assignment-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  background: #FDF6E3;
  border-radius: 8px;
}

.assignment-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.member-avatar {
  width: 44px;
  height: 44px;
  background: linear-gradient(135deg, #C41E3A, #8B0000);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 16px;
  
  &.small {
    width: 36px;
    height: 36px;
    font-size: 14px;
  }
}

.member-info {
  .member-name {
    font-weight: 500;
    color: #333;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  
  .member-phone {
    font-size: 13px;
    color: #666;
  }
  
  .member-meta {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    color: #666;
    
    .available {
      color: #999;
    }
  }
}

.assignment-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.suitable-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.suitable-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  background: #FDF6E3;
  border-radius: 8px;
  
  .member-info {
    flex: 1;
  }
}

.empty-state.small {
  padding: 30px 20px;
  
  .el-icon {
    font-size: 32px;
  }
  
  p {
    font-size: 14px;
  }
}
</style>
