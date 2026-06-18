<template>
  <div class="page-container">
    <div class="page-header">
      <h2>排练记录</h2>
      <el-button type="primary" @click="openAddDialog">
        <el-icon><Plus /></el-icon>
        新增排练
      </el-button>
    </div>

    <div class="filter-bar">
      <el-select v-model="filterProgram" placeholder="选择节目" clearable style="width: 200px" @change="filterRehearsals">
        <el-option v-for="p in store.programs" :key="p.id" :label="p.name" :value="p.id" />
      </el-select>
    </div>

    <div class="opera-card">
      <el-table :data="filteredRehearsals" v-loading="store.loading" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="program" label="节目" min-width="150">
          <template #default="{ row }">
            {{ getProgramName(row.program) }}
          </template>
        </el-table-column>
        <el-table-column prop="date" label="排练日期" width="150">
          <template #default="{ row }">
            <el-icon><Calendar /></el-icon>
            {{ row.date }}
          </template>
        </el-table-column>
        <el-table-column prop="location" label="地点" min-width="150">
          <template #default="{ row }">
            <el-icon><Location /></el-icon>
            {{ row.location }}
          </template>
        </el-table-column>
        <el-table-column prop="notes" label="备注" min-width="250" show-overflow-tooltip />
        <el-table-column label="反馈数" width="100">
          <template #default="{ row }">
            <el-tag type="info">{{ getFeedbackCount(row.id) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="goToDetail(row.id)">详情</el-button>
            <el-button type="primary" link @click="openEditDialog(row)">编辑</el-button>
            <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog v-model="dialogVisible" :title="editingRehearsal ? '编辑排练' : '新增排练'" width="600px">
      <el-form :model="formData" label-width="100px" ref="formRef">
        <el-form-item label="节目" prop="program" :rules="[{ required: true }]">
          <el-select v-model="formData.program" style="width: 100%">
            <el-option v-for="p in store.programs" :key="p.id" :label="p.name" :value="p.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="排练日期" prop="date" :rules="[{ required: true }]">
          <el-date-picker v-model="formData.date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
        <el-form-item label="地点" prop="location" :rules="[{ required: true }]">
          <el-input v-model="formData.location" placeholder="请输入排练地点" />
        </el-form-item>
        <el-form-item label="备注" prop="notes">
          <el-input v-model="formData.notes" type="textarea" :rows="4" placeholder="请输入排练备注" />
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
import { Plus, Calendar, Location } from '@element-plus/icons-vue'

const store = useOperaStore()
const router = useRouter()
const dialogVisible = ref(false)
const editingRehearsal = ref(null)
const formRef = ref(null)
const filterProgram = ref(null)

const formData = reactive({
  program: null,
  date: '',
  location: '',
  notes: ''
})

const filteredRehearsals = computed(() => {
  if (!filterProgram.value) return store.rehearsals
  return store.rehearsals.filter(r => r.program === filterProgram.value)
})

onMounted(async () => {
  await Promise.all([
    store.loadPrograms(),
    store.loadRehearsals(),
    store.loadFeedbacks()
  ])
})

function filterRehearsals() {
}

function getProgramName(programId) {
  const program = store.programs.find(p => p.id === programId)
  return program ? program.name : '未知节目'
}

function getFeedbackCount(rehearsalId) {
  return store.feedbacks.filter(f => f.rehearsal === rehearsalId).length
}

function goToDetail(id) {
  router.push(`/rehearsals/${id}`)
}

function openAddDialog() {
  editingRehearsal.value = null
  Object.assign(formData, {
    program: null,
    date: '',
    location: '',
    notes: ''
  })
  dialogVisible.value = true
}

function openEditDialog(rehearsal) {
  editingRehearsal.value = rehearsal
  Object.assign(formData, { ...rehearsal })
  dialogVisible.value = true
}

async function handleSubmit() {
  try {
    await formRef.value.validate()
    if (editingRehearsal.value) {
      await store.editRehearsal(editingRehearsal.value.id, formData)
      ElMessage.success('排练更新成功')
    } else {
      await store.addRehearsal(formData)
      ElMessage.success('排练创建成功')
    }
    dialogVisible.value = false
  } catch (error) {
    if (error !== false) {
      ElMessage.error('操作失败')
    }
  }
}

function handleDelete(row) {
  ElMessageBox.confirm(
    `确定要删除该排练记录吗？`,
    '删除确认',
    { type: 'warning' }
  ).then(async () => {
    await store.removeRehearsal(row.id)
    ElMessage.success('删除成功')
  }).catch(() => {})
}
</script>

<style lang="scss" scoped>
.filter-bar {
  margin-bottom: 20px;
}
</style>
