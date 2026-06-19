<template>
  <div class="page-container">
    <div class="page-header">
      <h2>演出复盘</h2>
      <el-button type="primary" @click="openCreateDialog">
        <el-icon><Plus /></el-icon>
        新建复盘批次
      </el-button>
    </div>

    <div class="opera-card">
      <el-table :data="store.performanceReviews" v-loading="store.loading" stripe empty-text="暂无复盘批次">
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column label="批次名称" min-width="200">
          <template #default="{ row }">
            <el-button type="primary" link @click="goToDetail(row.id)">{{ row.name }}</el-button>
          </template>
        </el-table-column>
        <el-table-column prop="program_name" label="所属节目" min-width="160" />
        <el-table-column prop="performance_date" label="演出日期" width="130" />
        <el-table-column label="状态" width="110">
          <template #default="{ row }">
            <el-tag :type="statusTagType(row.status)">{{ row.status_display }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="唱段数" width="90">
          <template #default="{ row }">
            <el-tag type="info">{{ row.item_count }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="完成率" width="130">
          <template #default="{ row }">
            <el-progress 
              :percentage="row.completion_rate" 
              :stroke-width="10"
              :color="row.completion_rate >= 80 ? '#2E7D32' : row.completion_rate >= 50 ? '#FF9800' : '#C41E3A'"
            />
          </template>
        </el-table-column>
        <el-table-column label="改进任务" width="100">
          <template #default="{ row }">
            <el-tag type="warning">{{ row.improvement_task_count }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="170">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="goToDetail(row.id)">查看</el-button>
            <el-button type="danger" link size="small" @click="deleteReview(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog v-model="createDialogVisible" title="新建演出复盘批次" width="600px">
      <el-form :model="createForm" label-width="120px" ref="createFormRef">
        <el-alert
          title="创建后将自动汇总该节目最终唱段分配、联排确认结果、风险处理记录、排练反馈、替补发生记录和实际演出备注，生成演出复盘清单。"
          type="info"
          :closable="false"
          show-icon
          style="margin-bottom: 16px"
        />
        <el-form-item label="所属节目" prop="program_id" :rules="[{ required: true, message: '请选择节目', trigger: 'change' }]">
          <el-select v-model="createForm.program_id" style="width: 100%" @change="onProgramChange">
            <el-option
              v-for="p in store.programs"
              :key="p.id"
              :label="p.name"
              :value="p.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="批次名称" prop="name" :rules="[{ required: true, message: '请输入批次名称', trigger: 'blur' }]">
          <el-input v-model="createForm.name" placeholder="如：首演复盘" />
        </el-form-item>
        <el-form-item label="演出日期" prop="performance_date" :rules="[{ required: true, message: '请选择演出日期', trigger: 'change' }]">
          <el-date-picker v-model="createForm.performance_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
        <el-form-item label="关联归档版本" prop="archive_id">
          <el-select v-model="createForm.archive_id" style="width: 100%" clearable>
            <el-option
              v-for="a in programArchives"
              :key="a.id"
              :label="'v' + a.version"
              :value="a.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="演出备注" prop="actual_performance_note">
          <el-input v-model="createForm.actual_performance_note" type="textarea" :rows="3" placeholder="请输入实际演出备注" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="createDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitCreate">确定创建</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useOperaStore } from '@/stores/opera'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'

const router = useRouter()
const store = useOperaStore()
const createDialogVisible = ref(false)
const createFormRef = ref(null)

const createForm = reactive({
  program_id: null,
  name: '',
  performance_date: '',
  archive_id: null,
  actual_performance_note: ''
})

const programArchives = computed(() => {
  if (!createForm.program_id) return []
  return store.archives.filter(a => a.program === createForm.program_id)
})

onMounted(async () => {
  await Promise.all([
    store.loadPrograms(),
    store.loadPerformanceReviews(),
    store.loadArchives()
  ])
})

function goToDetail(id) {
  router.push(`/performance-reviews/${id}`)
}

function openCreateDialog() {
  Object.assign(createForm, {
    program_id: null,
    name: '',
    performance_date: '',
    archive_id: null,
    actual_performance_note: ''
  })
  createDialogVisible.value = true
}

function onProgramChange() {
  const program = store.getProgramById(createForm.program_id)
  if (program && !createForm.name) {
    createForm.name = `${program.name} 演出复盘`
  }
}

async function submitCreate() {
  try {
    await createFormRef.value.validate()
    const result = await store.addPerformanceReview({
      program_id: createForm.program_id,
      name: createForm.name,
      performance_date: createForm.performance_date,
      archive_id: createForm.archive_id || null,
      actual_performance_note: createForm.actual_performance_note
    })
    ElMessage.success(`复盘批次创建成功，已生成 ${result.item_count || 0} 个复盘清单项`)
    createDialogVisible.value = false
    await store.loadPerformanceReviews()
  } catch (error) {
    if (error !== false && error?.message) {
      ElMessage.error('操作失败：' + error.message)
    } else if (error !== false) {
      ElMessage.error('操作失败')
    }
  }
}

function deleteReview(row) {
  ElMessageBox.confirm(`确定要删除复盘批次"${row.name}"吗？`, '删除确认', { type: 'warning' })
    .then(async () => {
      await store.removePerformanceReview(row.id)
      ElMessage.success('删除成功')
    }).catch(() => {})
}

function statusTagType(status) {
  const map = {
    'draft': 'info',
    'teacher_reviewing': 'warning',
    'member_reviewing': 'primary',
    'completed': 'success'
  }
  return map[status] || 'info'
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  return dateStr.substring(0, 16).replace('T', ' ')
}
</script>

<style lang="scss" scoped>
</style>
