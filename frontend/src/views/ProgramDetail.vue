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
                <span class="tag active">{{ program.type }}</span>
              </div>
            </div>
            <div class="info-item">
              <div class="detail-label">时长</div>
              <div class="detail-value">{{ program.duration }}分钟</div>
            </div>
            <div class="info-item">
              <div class="detail-label">状态</div>
              <div class="detail-value">
                <span :class="['tag', program.status]">
                  {{ program.status === 'active' ? '进行中' : '已暂停' }}
                </span>
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
                  <span class="tag active">{{ row.role_type }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="duration" label="时长" width="100">
                <template #default="{ row }">{{ row.duration }}分钟</template>
              </el-table-column>
              <el-table-column prop="lyrics" label="歌词" min-width="250" show-overflow-tooltip />
              <el-table-column prop="accompaniment_required" label="伴奏" width="100">
                <template #default="{ row }">
                  <el-tag :type="row.accompaniment_required ? 'success' : 'info'">
                    {{ row.accompaniment_required ? '需要' : '不需要' }}
                  </el-tag>
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
                  <span class="tag active">{{ row.role_type }}</span>
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
            <el-option label="生角" value="生角" />
            <el-option label="旦角" value="旦角" />
            <el-option label="净角" value="净角" />
            <el-option label="丑角" value="丑角" />
            <el-option label="老旦" value="老旦" />
            <el-option label="小生" value="小生" />
          </el-select>
        </el-form-item>
        <el-form-item label="时长" prop="duration" :rules="[{ required: true }]">
          <el-input-number v-model="ariaForm.duration" :min="1" /> 分钟
        </el-form-item>
        <el-form-item label="歌词" prop="lyrics">
          <el-input v-model="ariaForm.lyrics" type="textarea" :rows="4" />
        </el-form-item>
        <el-form-item label="需要伴奏" prop="accompaniment_required">
          <el-switch v-model="ariaForm.accompaniment_required" />
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
            <el-option label="生角" value="生角" />
            <el-option label="旦角" value="旦角" />
            <el-option label="净角" value="净角" />
            <el-option label="丑角" value="丑角" />
            <el-option label="老旦" value="老旦" />
            <el-option label="小生" value="小生" />
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

const program = computed(() => store.getProgramById(route.params.id))
const programArias = computed(() => store.arias.filter(a => a.program === parseInt(route.params.id)))
const programRoles = computed(() => store.roles.filter(r => r.program === parseInt(route.params.id)))

const ariaForm = reactive({
  order_index: 1,
  name: '',
  role_type: '',
  duration: 5,
  lyrics: '',
  accompaniment_required: true
})

const roleForm = reactive({
  name: '',
  role_type: '',
  description: ''
})

onMounted(async () => {
  await Promise.all([
    store.loadPrograms(),
    store.loadArias(),
    store.loadRoles()
  ])
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
      duration: 5,
      lyrics: '',
      accompaniment_required: true
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
