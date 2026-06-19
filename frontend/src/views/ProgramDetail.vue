<template>
  <div class="page-container">
    <div class="page-header">
      <h2>
        <el-button link @click="router.back()">
          <el-icon><ArrowLeft /></el-icon>
        </el-button>
        节目详情 - {{ program?.name }}
      </h2>
    </div>

    <div v-if="program" class="program-detail">
      <div class="opera-card">
        <div class="program-info">
          <div class="info-row">
            <div class="info-item">
              <div class="detail-label">节目名称</div>
              <div class="detail-value">{{ program.name }}</div>
            </div>
            <div class="info-item">
              <div class="detail-label">剧种</div>
              <div class="detail-value">
                <el-tag type="info">{{ program.type_display || program.type }}</el-tag>
              </div>
            </div>
            <div class="info-item">
              <div class="detail-label">时长</div>
              <div class="detail-value">{{ program.duration }}分钟</div>
            </div>
            <div class="info-item">
              <div class="detail-label">状态</div>
              <div class="detail-value">
                <el-tag :type="programStatusTagType(program.status)">
                  {{ programStatusText(program.status) }}
                </el-tag>
              </div>
            </div>
          </div>
          <div class="info-row">
            <div class="info-item full-width">
              <div class="detail-label">简介</div>
              <div class="detail-value">{{ program.description || '暂无简介' }}</div>
            </div>
          </div>
        </div>
      </div>

      <el-tabs v-model="activeTab" class="program-tabs">
        <el-tab-pane label="唱段列表" name="arias">
          <div class="tab-header">
            <h3 class="section-title">唱段列表</h3>
            <el-button type="primary" size="small" @click="openAriaDialog">
              <el-icon><Plus /></el-icon>
              新增唱段
            </el-button>
          </div>
          <div class="opera-card">
            <el-table :data="programArias" v-loading="store.loading" stripe>
              <el-table-column prop="order_index" label="序号" width="80" />
              <el-table-column prop="name" label="唱段名称" min-width="180" />
              <el-table-column prop="role_type" label="角色类型" width="120">
                <template #default="{ row }">
                  <span class="tag active">{{ row.role_type_display || getRoleTypeDisplay(row.role_type) }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="duration" label="时长" width="100">
                <template #default="{ row }">{{ Math.ceil(row.duration / 60) }}分钟</template>
              </el-table-column>
              <el-table-column prop="lyrics" label="歌词" min-width="250" show-overflow-tooltip />
              <el-table-column prop="accompaniment_required" label="伴奏需求" min-width="150" show-overflow-tooltip>
                <template #default="{ row }">
                  <span>{{ row.accompaniment_required || '无' }}</span>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="150">
                <template #default="{ row }">
                  <el-button type="primary" link @click="openAriaDialog(row)">编辑</el-button>
                  <el-button type="danger" link @click="deleteAria(row)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>

        <el-tab-pane label="联排确认" name="rehearsal">
          <div class="tab-header">
            <h3 class="section-title">联排确认批次</h3>
            <el-button type="primary" size="small" @click="openCheckDialog">
              <el-icon><Plus /></el-icon>
              新建联排确认批次
            </el-button>
          </div>
          <div class="opera-card">
            <el-table :data="programChecks" v-loading="store.loading" stripe empty-text="暂无联排确认批次">
              <el-table-column prop="id" label="ID" width="70" />
              <el-table-column label="批次名称" min-width="200">
                <template #default="{ row }">
                  <el-button type="primary" link @click="goToCheckDetail(row.id)">{{ row.name }}</el-button>
                </template>
              </el-table-column>
              <el-table-column prop="planned_performance_date" label="计划演出日期" width="140" />
              <el-table-column label="状态" width="100">
                <template #default="{ row }">
                  <el-tag :type="row.status === 'open' ? 'warning' : 'info'">{{ row.status_display }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column label="唱段数" width="90">
                <template #default="{ row }">
                  <el-tag type="info">{{ row.item_count }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column label="风险唱段" width="100">
                <template #default="{ row }">
                  <el-tag :type="row.risk_aria_count > 0 ? 'danger' : 'success'">{{ row.risk_aria_count }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="120" fixed="right">
                <template #default="{ row }">
                  <el-button type="primary" link @click="goToCheckDetail(row.id)">风险看板</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>

          <el-dialog v-model="checkDialogVisible" title="新建联排确认批次" width="600px">
            <el-form :model="checkForm" label-width="120px" ref="checkFormRef">
              <el-alert
                title="创建后将按该节目当前唱段顺序自动拉取唱段、角色、正式/替补成员、伴奏需求与最近排练反馈，生成联排确认清单。"
                type="info"
                :closable="false"
                show-icon
                style="margin-bottom: 16px"
              />
              <el-form-item label="批次名称" prop="name" :rules="[{ required: true, message: '请输入批次名称', trigger: 'blur' }]">
                <el-input v-model="checkForm.name" placeholder="如：演出前联排确认" />
              </el-form-item>
              <el-form-item label="计划演出日期" prop="planned_performance_date">
                <el-date-picker v-model="checkForm.planned_performance_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
              </el-form-item>
              <el-form-item label="备注" prop="notes">
                <el-input v-model="checkForm.notes" type="textarea" :rows="3" />
              </el-form-item>
            </el-form>
            <template #footer>
              <el-button @click="checkDialogVisible = false">取消</el-button>
              <el-button type="primary" @click="submitCheck">确定</el-button>
            </template>
          </el-dialog>
        </el-tab-pane>

        <el-tab-pane label="角色列表" name="roles">
          <div class="tab-header">
            <h3 class="section-title">角色列表</h3>
            <el-button type="primary" size="small" @click="openRoleDialog">
              <el-icon><Plus /></el-icon>
              新增角色
            </el-button>
          </div>
          <div class="opera-card">
            <el-table :data="programRoles" v-loading="store.loading" stripe>
              <el-table-column prop="name" label="角色名称" min-width="150" />
              <el-table-column prop="role_type" label="角色类型" width="120">
                <template #default="{ row }">
                  <span class="tag active">{{ row.role_type_display || getRoleTypeDisplay(row.role_type) }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="description" label="角色描述" min-width="300" />
              <el-table-column label="操作" width="150">
                <template #default="{ row }">
                  <el-button type="primary" link @click="openRoleDialog(row)">编辑</el-button>
                  <el-button type="danger" link @click="deleteRole(row)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>

    <el-dialog v-model="ariaDialogVisible" :title="editingAria ? '编辑唱段' : '新增唱段'" width="600px">
      <el-form :model="ariaForm" label-width="100px" ref="ariaFormRef">
        <el-form-item label="序号" prop="order_index" :rules="[{ required: true }]">
          <el-input-number v-model="ariaForm.order_index" :min="1" />
        </el-form-item>
        <el-form-item label="唱段名称" prop="name" :rules="[{ required: true }]">
          <el-input v-model="ariaForm.name" />
        </el-form-item>
        <el-form-item label="角色类型" prop="role_type" :rules="[{ required: true }]">
          <el-select v-model="ariaForm.role_type" style="width: 100%">
            <el-option label="生" value="sheng" />
            <el-option label="旦" value="dan" />
            <el-option label="净" value="jing" />
            <el-option label="末" value="mo" />
            <el-option label="丑" value="chou" />
          </el-select>
        </el-form-item>
        <el-form-item label="时长(秒)" prop="duration" :rules="[{ required: true }]">
          <el-input-number v-model="ariaForm.duration" :min="1" /> 秒
        </el-form-item>
        <el-form-item label="歌词" prop="lyrics">
          <el-input v-model="ariaForm.lyrics" type="textarea" :rows="4" />
        </el-form-item>
        <el-form-item label="伴奏需求" prop="accompaniment_required">
          <el-input 
            v-model="ariaForm.accompaniment_required" 
            type="textarea" 
            :rows="2"
            placeholder="请输入伴奏需求，如：京胡、月琴、鼓板等" 
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="ariaDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitAria">确定</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="roleDialogVisible" :title="editingRole ? '编辑角色' : '新增角色'" width="600px">
      <el-form :model="roleForm" label-width="100px" ref="roleFormRef">
        <el-form-item label="角色名称" prop="name" :rules="[{ required: true }]">
          <el-input v-model="roleForm.name" />
        </el-form-item>
        <el-form-item label="角色类型" prop="role_type" :rules="[{ required: true }]">
          <el-select v-model="roleForm.role_type" style="width: 100%">
            <el-option label="生" value="sheng" />
            <el-option label="旦" value="dan" />
            <el-option label="净" value="jing" />
            <el-option label="末" value="mo" />
            <el-option label="丑" value="chou" />
          </el-select>
        </el-form-item>
        <el-form-item label="角色描述" prop="description">
          <el-input v-model="roleForm.description" type="textarea" :rows="4" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="roleDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitRole">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useOperaStore } from '@/stores/opera'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowLeft, Plus } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const store = useOperaStore()
const activeTab = ref('arias')

const ariaDialogVisible = ref(false)
const roleDialogVisible = ref(false)
const editingAria = ref(null)
const editingRole = ref(null)
const ariaFormRef = ref(null)
const roleFormRef = ref(null)
const checkDialogVisible = ref(false)
const checkFormRef = ref(null)

const program = computed(() => store.getProgramById(route.params.id))
const programArias = computed(() => store.arias.filter(a => a.program === parseInt(route.params.id)))
const programRoles = computed(() => store.roles.filter(r => r.program === parseInt(route.params.id)))
const programChecks = computed(() => store.rehearsalChecks.filter(c => c.program === parseInt(route.params.id)))

const ariaForm = reactive({
  order_index: 1,
  name: '',
  role_type: '',
  duration: 300,
  lyrics: '',
  accompaniment_required: ''
})

const roleForm = reactive({
  name: '',
  role_type: '',
  description: ''
})

const checkForm = reactive({
  name: '',
  planned_performance_date: '',
  notes: ''
})

onMounted(async () => {
  await Promise.all([
    store.loadPrograms(),
    store.loadArias(),
    store.loadRoles(),
    store.loadRehearsalChecks(parseInt(route.params.id))
  ])
  if (program.value && !checkForm.name) {
    checkForm.name = `${program.value.name} 演出前联排确认`
  }
})

function openAriaDialog(aria = null) {
  editingAria.value = aria
  if (aria) {
    Object.assign(ariaForm, { ...aria })
  } else {
    Object.assign(ariaForm, {
      order_index: programArias.value.length + 1,
      name: '',
      role_type: '',
      duration: 300,
      lyrics: '',
      accompaniment_required: ''
    })
  }
  ariaDialogVisible.value = true
}

async function submitAria() {
  try {
    await ariaFormRef.value.validate()
    const data = { ...ariaForm, program: parseInt(route.params.id) }
    if (editingAria.value) {
      await store.editAria(editingAria.value.id, data)
      ElMessage.success('唱段更新成功')
    } else {
      await store.addAria(data)
      ElMessage.success('唱段创建成功')
    }
    ariaDialogVisible.value = false
  } catch (error) {
    if (error !== false) {
      ElMessage.error('操作失败')
    }
  }
}

function deleteAria(row) {
  ElMessageBox.confirm(`确定要删除唱段"${row.name}"吗？`, '删除确认', { type: 'warning' })
    .then(async () => {
      await store.removeAria(row.id)
      ElMessage.success('删除成功')
    }).catch(() => {})
}

function openRoleDialog(role = null) {
  editingRole.value = role
  if (role) {
    Object.assign(roleForm, { ...role })
  } else {
    Object.assign(roleForm, { name: '', role_type: '', description: '' })
  }
  roleDialogVisible.value = true
}

async function submitRole() {
  try {
    await roleFormRef.value.validate()
    const data = { ...roleForm, program: parseInt(route.params.id) }
    if (editingRole.value) {
      await store.editRole(editingRole.value.id, data)
      ElMessage.success('角色更新成功')
    } else {
      await store.addRole(data)
      ElMessage.success('角色创建成功')
    }
    roleDialogVisible.value = false
  } catch (error) {
    if (error !== false) {
      ElMessage.error('操作失败')
    }
  }
}

function deleteRole(row) {
  ElMessageBox.confirm(`确定要删除角色"${row.name}"吗？`, '删除确认', { type: 'warning' })
    .then(async () => {
      await store.removeRole(row.id)
      ElMessage.success('删除成功')
    }).catch(() => {})
}

function openCheckDialog() {
  Object.assign(checkForm, {
    name: program.value ? `${program.value.name} 演出前联排确认` : '',
    planned_performance_date: '',
    notes: ''
  })
  checkDialogVisible.value = true
}

function goToCheckDetail(id) {
  router.push(`/rehearsal-checks/${id}`)
}

async function submitCheck() {
  try {
    await checkFormRef.value.validate()
    const result = await store.addRehearsalCheck({
      program: parseInt(route.params.id),
      name: checkForm.name,
      planned_performance_date: checkForm.planned_performance_date,
      status: 'open',
      notes: checkForm.notes
    })
    ElMessage.success(`联排批次创建成功，已生成 ${result.item_count || 0} 个唱段确认项`)
    checkDialogVisible.value = false
    await store.loadRehearsalChecks(parseInt(route.params.id))
  } catch (error) {
    if (error !== false && error?.message) {
      ElMessage.error('操作失败：' + error.message)
    } else if (error !== false) {
      ElMessage.error('操作失败')
    }
  }
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

function programStatusText(status) {
  const map = {
    'planning': '筹备',
    'rehearsing': '排练',
    'performing': '演出',
    'archived': '归档'
  }
  return map[status] || status
}

function programStatusTagType(status) {
  const map = {
    'planning': 'info',
    'rehearsing': 'warning',
    'performing': 'success',
    'archived': 'danger'
  }
  return map[status] || 'info'
}
</script>

<style lang="scss" scoped>
.program-info {
  .info-row {
    display: flex;
    gap: 24px;
    margin-bottom: 16px;
    
    &:last-child {
      margin-bottom: 0;
    }
  }
  
  .info-item {
    flex: 1;
    
    &.full-width {
      flex: 1 1 100%;
    }
  }
}

.tab-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.program-tabs {
  :deep(.el-tabs__item.is-active) {
    color: #C41E3A !important;
  }
  
  :deep(.el-tabs__active-bar) {
    background-color: #D4AF37 !important;
  }
}
</style>
