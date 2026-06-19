<template>
  <div class="page-container">
    <div class="page-header">
      <h2>联排确认与风险看板</h2>
      <el-button type="primary" @click="openAddDialog">
        <el-icon><Plus /></el-icon>
        新建联排确认批次
      </el-button>
    </div>

    <div class="filter-bar">
      <el-select v-model="filterProgram" placeholder="按节目筛选" clearable style="width: 220px" @change="loadList">
        <el-option v-for="p in store.programs" :key="p.id" :label="p.name" :value="p.id" />
      </el-select>
      <el-select v-model="filterStatus" placeholder="按状态筛选" clearable style="width: 160px; margin-left: 12px" @change="filterList">
        <el-option label="进行中" value="open" />
        <el-option label="已关闭" value="closed" />
      </el-select>
    </div>

    <div class="stats-grid">
      <StatsCard :icon="Document" label="联排批次" :value="store.rehearsalChecks.length" bgColor="linear-gradient(135deg, #C41E3A, #8B0000)" />
      <StatsCard :icon="CircleCheck" label="进行中批次" :value="store.openRehearsalChecks.length" bgColor="linear-gradient(135deg, #D4AF37, #B8860B)" />
      <StatsCard :icon="Warning" label="风险唱段总数" :value="totalRiskArias" bgColor="linear-gradient(135deg, #FF9800, #F57C00)" />
      <StatsCard :icon="Bell" label="待处理风险项" :value="pendingRiskCount" bgColor="linear-gradient(135deg, #2E7D32, #1B5E20)" />
    </div>

    <div class="opera-card" v-loading="store.loading">
      <el-table :data="filteredChecks" stripe>
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column label="批次名称" min-width="200">
          <template #default="{ row }">
            <el-button type="primary" link @click="goToDetail(row.id)">{{ row.name }}</el-button>
          </template>
        </el-table-column>
        <el-table-column label="节目" min-width="150">
          <template #default="{ row }">{{ getProgramName(row.program) }}</template>
        </el-table-column>
        <el-table-column prop="planned_performance_date" label="计划演出日期" width="140">
          <template #default="{ row }">
            <el-icon><Calendar /></el-icon>
            {{ row.planned_performance_date || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'open' ? 'warning' : 'info'">
              {{ row.status === 'open' ? '进行中' : '已关闭' }}
            </el-tag>
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
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="goToDetail(row.id)">详情看板</el-button>
            <el-button type="warning" link @click="openEditDialog(row)">编辑</el-button>
            <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog v-model="dialogVisible" :title="editingCheck ? '编辑联排批次' : '新建联排确认批次'" width="600px">
      <el-form :model="formData" label-width="120px" ref="formRef">
        <el-alert
          v-if="!editingCheck"
          title="创建后将按该节目当前唱段顺序自动拉取唱段、角色、正式/替补成员、伴奏需求与最近排练反馈，生成联排确认清单。"
          type="info"
          :closable="false"
          show-icon
          style="margin-bottom: 16px"
        />
        <el-form-item label="节目" prop="program" :rules="[{ required: true, message: '请选择节目', trigger: 'change' }]">
          <el-select v-model="formData.program" style="width: 100%" :disabled="!!editingCheck" @change="onProgramChange">
            <el-option v-for="p in editablePrograms" :key="p.id" :label="p.name" :value="p.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="批次名称" prop="name" :rules="[{ required: true, message: '请输入批次名称', trigger: 'blur' }]">
          <el-input v-model="formData.name" placeholder="如：锁麟囊 演出前联排确认" />
        </el-form-item>
        <el-form-item label="计划演出日期" prop="planned_performance_date">
          <el-date-picker v-model="formData.planned_performance_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="formData.status" style="width: 100%">
            <el-option label="进行中" value="open" />
            <el-option label="已关闭" value="closed" />
          </el-select>
        </el-form-item>
        <el-form-item label="备注" prop="notes">
          <el-input v-model="formData.notes" type="textarea" :rows="3" placeholder="联排确认说明" />
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
import { useRouter } from 'vue-router'
import { useOperaStore } from '@/stores/opera'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Calendar, Document, CircleCheck, Warning, Bell } from '@element-plus/icons-vue'
import StatsCard from '@/components/StatsCard.vue'

const store = useOperaStore()
const router = useRouter()
const dialogVisible = ref(false)
const editingCheck = ref(null)
const formRef = ref(null)
const filterProgram = ref(null)
const filterStatus = ref(null)

const formData = reactive({
  program: null,
  name: '',
  planned_performance_date: '',
  status: 'open',
  notes: ''
})

const editablePrograms = computed(() => store.programs.filter(p => p.status !== 'archived'))
const filteredChecks = computed(() => {
  let list = store.rehearsalChecks
  if (filterProgram.value) list = list.filter(c => c.program === filterProgram.value)
  if (filterStatus.value) list = list.filter(c => c.status === filterStatus.value)
  return list
})
const totalRiskArias = computed(() => store.rehearsalChecks.reduce((sum, c) => sum + (c.risk_aria_count || 0), 0))
const pendingRiskCount = computed(() => store.riskActions.filter(a => a.status === 'pending').length)

onMounted(async () => {
  await Promise.all([
    store.loadPrograms(),
    store.loadRehearsalChecks(),
    store.loadRiskActions()
  ])
})

function loadList() {}

function filterList() {}

function getProgramName(programId) {
  const program = store.programs.find(p => p.id === programId)
  return program ? program.name : '未知节目'
}

function goToDetail(id) {
  router.push(`/rehearsal-checks/${id}`)
}

function onProgramChange(programId) {
  if (!editingCheck.value && programId) {
    const program = store.programs.find(p => p.id === programId)
    if (program && !formData.name) {
      formData.name = `${program.name} 演出前联排确认`
    }
  }
}

function openAddDialog() {
  editingCheck.value = null
  Object.assign(formData, {
    program: null,
    name: '',
    planned_performance_date: '',
    status: 'open',
    notes: ''
  })
  dialogVisible.value = true
}

function openEditDialog(check) {
  editingCheck.value = check
  Object.assign(formData, {
    program: check.program,
    name: check.name,
    planned_performance_date: check.planned_performance_date,
    status: check.status,
    notes: check.notes || ''
  })
  dialogVisible.value = true
}

async function handleSubmit() {
  try {
    await formRef.value.validate()
    if (editingCheck.value) {
      await store.editRehearsalCheck(editingCheck.value.id, { ...formData })
      ElMessage.success('联排批次更新成功')
    } else {
      const result = await store.addRehearsalCheck({ ...formData })
      ElMessage.success(`联排批次创建成功，已生成 ${result.item_count || 0} 个唱段确认项`)
    }
    dialogVisible.value = false
  } catch (error) {
    if (error !== false && error?.message) {
      ElMessage.error('操作失败：' + error.message)
    } else if (error !== false) {
      ElMessage.error('操作失败')
    }
  }
}

function handleDelete(row) {
  ElMessageBox.confirm(`确定要删除联排批次"${row.name}"吗？相关确认与风险项将一并删除。`, '删除确认', { type: 'warning' })
    .then(async () => {
      await store.removeRehearsalCheck(row.id)
      ElMessage.success('删除成功')
    }).catch(() => {})
}
</script>

<style lang="scss" scoped>
.filter-bar {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}
</style>
