<template>
  <div class="page-container">
    <div class="page-header">
      <h2>节目档案</h2>
      <el-button type="primary" @click="openAddDialog">
        <el-icon><Plus /></el-icon>
        新增节目
      </el-button>
    </div>

    <div class="opera-card">
      <el-table :data="store.programs" v-loading="store.loading" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="节目名称" min-width="150">
          <template #default="{ row }">
            <router-link :to="`/programs/${row.id}`" class="program-link">
              {{ row.name }}
            </router-link>
          </template>
        </el-table-column>
        <el-table-column prop="type" label="剧种" width="120">
          <template #default="{ row }">
            <span class="tag active">{{ row.type_display || row.type }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="简介" min-width="250" show-overflow-tooltip />
        <el-table-column prop="duration" label="时长" width="100">
          <template #default="{ row }">
            {{ row.duration }}分钟
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <span :class="['tag', row.status]">
              {{ row.status_display || row.status }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="openEditDialog(row)">编辑</el-button>
            <el-button type="primary" link @click="goToDetail(row.id)">详情</el-button>
            <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog 
      v-model="dialogVisible" 
      :title="editingProgram ? '编辑节目' : '新增节目'"
      width="600px"
    >
      <el-form :model="formData" label-width="100px" ref="formRef">
        <el-form-item label="节目名称" prop="name" :rules="[{ required: true, message: '请输入节目名称' }]">
          <el-input v-model="formData.name" placeholder="请输入节目名称" />
        </el-form-item>
        <el-form-item label="剧种" prop="type" :rules="[{ required: true, message: '请选择剧种' }]">
          <el-select v-model="formData.type" placeholder="请选择剧种" style="width: 100%">
            <el-option label="京剧" value="beijing" />
            <el-option label="豫剧" value="henan" />
            <el-option label="昆曲" value="kunqu" />
            <el-option label="越剧" value="yue" />
            <el-option label="黄梅戏" value="huangmei" />
            <el-option label="评剧" value="ping" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="时长" prop="duration" :rules="[{ required: true, message: '请输入时长' }]">
          <el-input-number v-model="formData.duration" :min="1" :max="300" />
          <span style="margin-left: 8px">分钟</span>
        </el-form-item>
        <el-form-item label="简介" prop="description">
          <el-input 
            v-model="formData.description" 
            type="textarea" 
            :rows="4"
            placeholder="请输入节目简介" 
          />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="formData.status">
            <el-radio value="planning">筹备</el-radio>
            <el-radio value="rehearsing">排练</el-radio>
            <el-radio value="performing">演出</el-radio>
            <el-radio value="archived">归档</el-radio>
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
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useOperaStore } from '@/stores/opera'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'

const store = useOperaStore()
const router = useRouter()
const dialogVisible = ref(false)
const editingProgram = ref(null)
const formRef = ref(null)

const formData = reactive({
  name: '',
  type: '',
  duration: 30,
  description: '',
  status: 'planning'
})

onMounted(async () => {
  await store.loadPrograms()
})

function openAddDialog() {
  editingProgram.value = null
  Object.assign(formData, {
    name: '',
    type: '',
    duration: 30,
    description: '',
    status: 'planning'
  })
  dialogVisible.value = true
}

function openEditDialog(program) {
  editingProgram.value = program
  Object.assign(formData, { ...program })
  dialogVisible.value = true
}

function goToDetail(id) {
  router.push(`/programs/${id}`)
}

async function handleSubmit() {
  try {
    await formRef.value.validate()
    if (editingProgram.value) {
      await store.editProgram(editingProgram.value.id, formData)
      ElMessage.success('节目更新成功')
    } else {
      await store.addProgram(formData)
      ElMessage.success('节目创建成功')
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
    `确定要删除节目"${row.name}"吗？此操作不可恢复。`,
    '删除确认',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    await store.removeProgram(row.id)
    ElMessage.success('删除成功')
  }).catch(() => {})
}
</script>

<style lang="scss" scoped>
.program-link {
  color: #C41E3A;
  text-decoration: none;
  font-weight: 500;
  
  &:hover {
    text-decoration: underline;
  }
}
</style>
