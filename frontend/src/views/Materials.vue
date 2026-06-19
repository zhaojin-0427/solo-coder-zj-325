<template>
  <div class="page-container">
    <div class="page-header">
      <h2>物资管理</h2>
      <el-button type="primary" @click="openAddDialog">
        <el-icon><Plus /></el-icon>
        新增物资
      </el-button>
    </div>

    <div class="opera-card filter-section">
      <el-form :inline="true" :model="filterForm" class="filter-form">
        <el-form-item label="节目">
          <el-select v-model="filterForm.program" placeholder="全部节目" clearable style="width: 180px">
            <el-option v-for="p in store.programs" :key="p.id" :label="p.name" :value="p.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="类别">
          <el-select v-model="filterForm.category" placeholder="全部类别" clearable style="width: 160px">
            <el-option label="服装" value="costume" />
            <el-option label="头面" value="headgear" />
            <el-option label="道具" value="prop" />
            <el-option label="谱架" value="music_stand" />
            <el-option label="麦克风" value="microphone" />
            <el-option label="伴奏设备" value="accompaniment" />
            <el-option label="鞋靴" value="shoes" />
            <el-option label="配饰" value="accessory" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="filterForm.status" placeholder="全部状态" clearable style="width: 140px">
            <el-option label="可用" value="available" />
            <el-option label="借用中" value="borrowed" />
            <el-option label="维修中" value="repairing" />
            <el-option label="已报废" value="retired" />
            <el-option label="预留" value="reserved" />
          </el-select>
        </el-form-item>
        <el-form-item label="搜索">
          <el-input
            v-model="filterForm.keyword"
            placeholder="按名称/编号搜索"
            clearable
            style="width: 220px"
            :prefix-icon="Search"
          />
        </el-form-item>
      </el-form>
    </div>

    <div class="opera-card">
      <el-table :data="filteredMaterials" v-loading="store.loading" stripe>
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column prop="code" label="物资编号" width="120" />
        <el-table-column label="类别" width="100">
          <template #default="{ row }">
            <span class="tag active">{{ row.category_display || row.category }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="name" label="物资名称" min-width="150">
          <template #default="{ row }">
            <router-link :to="`/materials/${row.id}`" class="material-link">
              {{ row.name }}
            </router-link>
          </template>
        </el-table-column>
        <el-table-column prop="program_name" label="所属节目" width="140" />
        <el-table-column label="适用角色/行当" width="130">
          <template #default="{ row }">
            {{ row.role_name || row.role_type_display || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="规格尺码" width="110">
          <template #default="{ row }">
            {{ row.size_display || row.custom_size || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="storage_location" label="存放位置" width="130" show-overflow-tooltip />
        <el-table-column label="数量" width="110">
          <template #default="{ row }">
            <span>{{ row.available_qty || 0 }}/{{ row.quantity || 0 }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="responsible_member_name" label="负责人" width="100" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag
              :type="getStatusTagType(row.status)"
              effect="light"
            >
              {{ row.status_display || row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="last_maintenance_date" label="最近维护日期" width="130" />
        <el-table-column label="操作" width="280" fixed="right">
          <template #default="{ row }">
            <el-button
              v-if="row.status === 'available' && (row.available_qty || 0) > 0"
              type="primary"
              link
              @click="openBorrowDialog(row)"
            >借用</el-button>
            <el-button
              v-if="row.status === 'borrowed'"
              type="warning"
              link
              @click="openReturnDialog(row)"
            >归还</el-button>
            <el-button type="danger" link @click="openRepairDialog(row)">报修</el-button>
            <el-button type="primary" link @click="openEditDialog(row)">编辑</el-button>
            <el-button type="primary" link @click="goToDetail(row.id)">详情</el-button>
            <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog
      v-model="dialogVisible"
      :title="editingMaterial ? '编辑物资' : '新增物资'"
      width="700px"
    >
      <el-form :model="formData" label-width="110px" ref="formRef" label-position="right">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="所属节目" prop="program" :rules="[{ required: true, message: '请选择所属节目' }]">
              <el-select
                v-model="formData.program"
                placeholder="请选择节目"
                style="width: 100%"
                @change="handleProgramChange"
              >
                <el-option v-for="p in store.programs" :key="p.id" :label="p.name" :value="p.id" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="类别" prop="category" :rules="[{ required: true, message: '请选择类别' }]">
              <el-select v-model="formData.category" placeholder="请选择类别" style="width: 100%">
                <el-option label="服装" value="costume" />
                <el-option label="头面" value="headgear" />
                <el-option label="道具" value="prop" />
                <el-option label="谱架" value="music_stand" />
                <el-option label="麦克风" value="microphone" />
                <el-option label="伴奏设备" value="accompaniment" />
                <el-option label="鞋靴" value="shoes" />
                <el-option label="配饰" value="accessory" />
                <el-option label="其他" value="other" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="物资名称" prop="name" :rules="[{ required: true, message: '请输入物资名称' }]">
              <el-input v-model="formData.name" placeholder="请输入物资名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="物资编号" prop="code">
              <el-input v-model="formData.code" placeholder="请输入物资编号" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="适用角色" prop="role">
              <el-select v-model="formData.role" placeholder="请选择角色" style="width: 100%" clearable>
                <el-option v-for="r in programRoles" :key="r.id" :label="r.name" :value="r.id" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="适用唱段" prop="aria">
              <el-select v-model="formData.aria" placeholder="请选择唱段" style="width: 100%" clearable>
                <el-option v-for="a in programArias" :key="a.id" :label="a.name" :value="a.id" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="适用行当" prop="role_type">
              <el-select v-model="formData.role_type" placeholder="请选择行当" style="width: 100%" clearable>
                <el-option label="生" value="sheng" />
                <el-option label="旦" value="dan" />
                <el-option label="净" value="jing" />
                <el-option label="末" value="mo" />
                <el-option label="丑" value="chou" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="规格尺码" prop="size">
              <el-select v-model="formData.size" placeholder="请选择尺码" style="width: 100%" clearable>
                <el-option label="XS" value="XS" />
                <el-option label="S" value="S" />
                <el-option label="M" value="M" />
                <el-option label="L" value="L" />
                <el-option label="XL" value="XL" />
                <el-option label="XXL" value="XXL" />
                <el-option label="均码" value="one_size" />
                <el-option label="定制" value="custom" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item v-if="formData.size === 'custom'" label="自定义尺寸" prop="custom_size">
          <el-input v-model="formData.custom_size" placeholder="请输入自定义尺寸" />
        </el-form-item>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="颜色" prop="color">
              <el-input v-model="formData.color" placeholder="请输入颜色" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="材质" prop="material_texture">
              <el-input v-model="formData.material_texture" placeholder="请输入材质" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="存放位置" prop="storage_location">
              <el-input v-model="formData.storage_location" placeholder="请输入存放位置" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="数量" prop="quantity" :rules="[{ required: true, message: '请输入数量' }]">
              <el-input-number v-model="formData.quantity" :min="1" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="负责人" prop="responsible_member">
          <el-select v-model="formData.responsible_member" placeholder="请选择负责人" style="width: 100%" clearable>
            <el-option v-for="m in store.members" :key="m.id" :label="m.name" :value="m.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="可用状态" prop="status">
          <el-radio-group v-model="formData.status">
            <el-radio value="available">可用</el-radio>
            <el-radio value="reserved">预留</el-radio>
            <el-radio value="retired">已报废</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="购置日期" prop="purchase_date">
              <el-date-picker
                v-model="formData.purchase_date"
                type="date"
                placeholder="选择日期"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="最近维护日期" prop="last_maintenance_date">
              <el-date-picker
                v-model="formData.last_maintenance_date"
                type="date"
                placeholder="选择日期"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="下次维护日期" prop="next_maintenance_date">
              <el-date-picker
                v-model="formData.next_maintenance_date"
                type="date"
                placeholder="选择日期"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="维护备注" prop="maintenance_note">
          <el-input
            v-model="formData.maintenance_note"
            type="textarea"
            :rows="2"
            placeholder="请输入维护备注"
          />
        </el-form-item>
        <el-form-item label="品相说明" prop="condition_note">
          <el-input
            v-model="formData.condition_note"
            type="textarea"
            :rows="2"
            placeholder="请输入品相说明"
          />
        </el-form-item>
        <el-form-item label="图片链接" prop="image_url">
          <el-input v-model="formData.image_url" placeholder="请输入图片链接URL" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <el-dialog
      v-model="borrowDialogVisible"
      title="借用物资"
      width="550px"
    >
      <el-form :model="borrowForm" label-width="120px" ref="borrowFormRef">
        <el-form-item label="物资名称">
          <span>{{ borrowingMaterial?.name }}</span>
        </el-form-item>
        <el-form-item label="可用数量">
          <span>{{ borrowingMaterial?.available_qty || 0 }} 件</span>
        </el-form-item>
        <el-form-item label="借用人" prop="borrower_id" :rules="[{ required: true, message: '请选择借用人' }]">
          <el-select v-model="borrowForm.borrower_id" placeholder="请选择借用人" style="width: 100%">
            <el-option v-for="m in store.members" :key="m.id" :label="m.name" :value="m.id" />
          </el-select>
        </el-form-item>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="计划取用日期" prop="planned_borrow_date" :rules="[{ required: true, message: '请选择日期' }]">
              <el-date-picker
                v-model="borrowForm.planned_borrow_date"
                type="date"
                placeholder="选择日期"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="计划归还日期" prop="planned_return_date" :rules="[{ required: true, message: '请选择日期' }]">
              <el-date-picker
                v-model="borrowForm.planned_return_date"
                type="date"
                placeholder="选择日期"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="借用数量" prop="quantity" :rules="[{ required: true, message: '请输入数量' }]">
          <el-input-number
            v-model="borrowForm.quantity"
            :min="1"
            :max="borrowingMaterial?.available_qty || 1"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="借用用途" prop="purpose">
          <el-input
            v-model="borrowForm.purpose"
            type="textarea"
            :rows="3"
            placeholder="请输入借用用途"
          />
        </el-form-item>
        <el-form-item label="关联联排批次" prop="rehearsal_check_id">
          <el-select
            v-model="borrowForm.rehearsal_check_id"
            placeholder="请选择联排批次（可选）"
            style="width: 100%"
            clearable
          >
            <el-option
              v-for="c in store.rehearsalChecks"
              :key="c.id"
              :label="c.name || `联排#${c.id}`"
              :value="c.id"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="borrowDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleBorrowSubmit">确认借用</el-button>
      </template>
    </el-dialog>

    <el-dialog
      v-model="returnDialogVisible"
      title="归还物资"
      width="550px"
    >
      <el-form :model="returnForm" label-width="120px" ref="returnFormRef">
        <el-form-item label="物资名称">
          <span>{{ returningMaterial?.name }}</span>
        </el-form-item>
        <el-form-item label="归还确认人" prop="confirmed_by_id">
          <el-select v-model="returnForm.confirmed_by_id" placeholder="请选择确认人" style="width: 100%" clearable>
            <el-option v-for="m in store.members" :key="m.id" :label="m.name" :value="m.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="归还时品相" prop="return_condition">
          <el-input
            v-model="returnForm.return_condition"
            type="textarea"
            :rows="3"
            placeholder="请描述归还时的品相"
          />
        </el-form-item>
        <el-form-item label="是否发现损坏">
          <el-switch v-model="returnForm.damage_found" />
        </el-form-item>
        <el-form-item v-if="returnForm.damage_found" label="损坏说明" prop="damage_note">
          <el-input
            v-model="returnForm.damage_note"
            type="textarea"
            :rows="3"
            placeholder="请描述损坏情况"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="returnDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleReturnSubmit">确认归还</el-button>
      </template>
    </el-dialog>

    <el-dialog
      v-model="repairDialogVisible"
      title="报修物资"
      width="550px"
    >
      <el-form :model="repairForm" label-width="110px" ref="repairFormRef">
        <el-form-item label="物资名称">
          <span>{{ repairingMaterial?.name }}</span>
        </el-form-item>
        <el-form-item label="报修人" prop="reporter_id" :rules="[{ required: true, message: '请选择报修人' }]">
          <el-select v-model="repairForm.reporter_id" placeholder="请选择报修人" style="width: 100%">
            <el-option v-for="m in store.members" :key="m.id" :label="m.name" :value="m.id" />
          </el-select>
        </el-form-item>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="损坏类型" prop="repair_type">
              <el-select v-model="repairForm.repair_type" placeholder="请选择类型" style="width: 100%">
                <el-option label="破损/开线" value="tear" />
                <el-option label="污渍" value="stain" />
                <el-option label="变形" value="deformation" />
                <el-option label="配件缺失" value="missing_part" />
                <el-option label="褪色" value="fading" />
                <el-option label="电子故障" value="electronic" />
                <el-option label="结构性损坏" value="structural" />
                <el-option label="其他" value="other" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="严重程度" prop="severity">
              <el-select v-model="repairForm.severity" placeholder="请选择程度" style="width: 100%">
                <el-option label="轻微" value="minor" />
                <el-option label="中等" value="moderate" />
                <el-option label="严重" value="severe" />
                <el-option label="致命" value="critical" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="损坏描述" prop="description" :rules="[{ required: true, message: '请输入损坏描述' }]">
          <el-input
            v-model="repairForm.description"
            type="textarea"
            :rows="4"
            placeholder="请详细描述损坏情况"
          />
        </el-form-item>
        <el-form-item label="损坏部位" prop="location">
          <el-input v-model="repairForm.location" placeholder="请输入损坏部位" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="repairDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleRepairSubmit">提交报修</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useOperaStore } from '@/stores/opera'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search } from '@element-plus/icons-vue'

const store = useOperaStore()
const router = useRouter()
const dialogVisible = ref(false)
const borrowDialogVisible = ref(false)
const returnDialogVisible = ref(false)
const repairDialogVisible = ref(false)

const editingMaterial = ref(null)
const borrowingMaterial = ref(null)
const returningMaterial = ref(null)
const repairingMaterial = ref(null)

const formRef = ref(null)
const borrowFormRef = ref(null)
const returnFormRef = ref(null)
const repairFormRef = ref(null)

const filterForm = reactive({
  program: null,
  category: '',
  status: '',
  keyword: ''
})

const programRoles = ref([])
const programArias = ref([])

const formData = reactive({
  program: null,
  category: '',
  name: '',
  code: '',
  role: null,
  aria: null,
  role_type: '',
  size: '',
  custom_size: '',
  color: '',
  material_texture: '',
  storage_location: '',
  quantity: 1,
  responsible_member: null,
  status: 'available',
  purchase_date: '',
  last_maintenance_date: '',
  next_maintenance_date: '',
  maintenance_note: '',
  condition_note: '',
  image_url: ''
})

const borrowForm = reactive({
  borrower_id: null,
  planned_borrow_date: '',
  planned_return_date: '',
  quantity: 1,
  purpose: '',
  rehearsal_check_id: null
})

const returnForm = reactive({
  confirmed_by_id: null,
  return_condition: '',
  damage_found: false,
  damage_note: ''
})

const repairForm = reactive({
  reporter_id: null,
  repair_type: '',
  severity: '',
  description: '',
  location: ''
})

const filteredMaterials = computed(() => {
  let result = store.materials
  if (filterForm.program) {
    result = result.filter(m => m.program === filterForm.program || m.program_id === filterForm.program)
  }
  if (filterForm.category) {
    result = result.filter(m => m.category === filterForm.category)
  }
  if (filterForm.status) {
    result = result.filter(m => m.status === filterForm.status)
  }
  if (filterForm.keyword) {
    const kw = filterForm.keyword.toLowerCase()
    result = result.filter(m =>
      (m.name && m.name.toLowerCase().includes(kw)) ||
      (m.code && m.code.toLowerCase().includes(kw))
    )
  }
  return result
})

onMounted(async () => {
  await Promise.all([
    store.loadPrograms(),
    store.loadMembers(),
    store.loadMaterials(),
    store.loadRehearsalChecks()
  ])
})

async function handleProgramChange(programId) {
  if (programId) {
    const [roles, arias] = await Promise.all([
      store.loadRoles(programId),
      store.loadArias(programId)
    ])
    programRoles.value = store.roles
    programArias.value = store.arias
  } else {
    programRoles.value = []
    programArias.value = []
  }
  formData.role = null
  formData.aria = null
}

function getStatusTagType(status) {
  const map = {
    available: 'success',
    borrowed: 'warning',
    repairing: 'danger',
    retired: 'info',
    reserved: 'primary'
  }
  return map[status] || 'info'
}

function resetFormData() {
  Object.assign(formData, {
    program: null,
    category: '',
    name: '',
    code: '',
    role: null,
    aria: null,
    role_type: '',
    size: '',
    custom_size: '',
    color: '',
    material_texture: '',
    storage_location: '',
    quantity: 1,
    responsible_member: null,
    status: 'available',
    purchase_date: '',
    last_maintenance_date: '',
    next_maintenance_date: '',
    maintenance_note: '',
    condition_note: '',
    image_url: ''
  })
  programRoles.value = []
  programArias.value = []
}

function openAddDialog() {
  editingMaterial.value = null
  resetFormData()
  dialogVisible.value = true
}

function openEditDialog(material) {
  editingMaterial.value = material
  Object.assign(formData, { ...material })
  if (material.program || material.program_id) {
    handleProgramChange(material.program || material.program_id)
  }
  dialogVisible.value = true
}

function goToDetail(id) {
  router.push(`/materials/${id}`)
}

async function handleSubmit() {
  try {
    await formRef.value.validate()
    if (editingMaterial.value) {
      await store.editMaterial(editingMaterial.value.id, formData)
      ElMessage.success('物资更新成功')
    } else {
      await store.addMaterial(formData)
      ElMessage.success('物资创建成功')
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
    `确定要删除物资"${row.name}"吗？此操作不可恢复。`,
    '删除确认',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    await store.removeMaterial(row.id)
    ElMessage.success('删除成功')
  }).catch(() => {})
}

function resetBorrowForm() {
  Object.assign(borrowForm, {
    borrower_id: null,
    planned_borrow_date: '',
    planned_return_date: '',
    quantity: 1,
    purpose: '',
    rehearsal_check_id: null
  })
}

function openBorrowDialog(material) {
  borrowingMaterial.value = material
  resetBorrowForm()
  borrowDialogVisible.value = true
}

async function handleBorrowSubmit() {
  try {
    await borrowFormRef.value.validate()
    await store.borrowMaterialById(borrowingMaterial.value.id, borrowForm)
    ElMessage.success('借用申请提交成功')
    borrowDialogVisible.value = false
  } catch (error) {
    if (error !== false) {
      ElMessage.error('借用申请提交失败')
    }
  }
}

function resetReturnForm() {
  Object.assign(returnForm, {
    confirmed_by_id: null,
    return_condition: '',
    damage_found: false,
    damage_note: ''
  })
}

function openReturnDialog(material) {
  returningMaterial.value = material
  resetReturnForm()
  returnDialogVisible.value = true
}

async function handleReturnSubmit() {
  try {
    await store.returnMaterialById(returningMaterial.value.id, returnForm)
    ElMessage.success('归还确认成功')
    returnDialogVisible.value = false
  } catch (error) {
    ElMessage.error('归还确认失败')
  }
}

function resetRepairForm() {
  Object.assign(repairForm, {
    reporter_id: null,
    repair_type: '',
    severity: '',
    description: '',
    location: ''
  })
}

function openRepairDialog(material) {
  repairingMaterial.value = material
  resetRepairForm()
  repairDialogVisible.value = true
}

async function handleRepairSubmit() {
  try {
    await repairFormRef.value.validate()
    await store.reportDamageById(repairingMaterial.value.id, repairForm)
    ElMessage.success('报修提交成功')
    repairDialogVisible.value = false
  } catch (error) {
    if (error !== false) {
      ElMessage.error('报修提交失败')
    }
  }
}
</script>

<style lang="scss" scoped>
.material-link {
  color: #C41E3A;
  text-decoration: none;
  font-weight: 500;

  &:hover {
    text-decoration: underline;
  }
}

.filter-section {
  padding-bottom: 4px;
}

.filter-form {
  display: flex;
  flex-wrap: wrap;

  .el-form-item {
    margin-right: 0;
    margin-bottom: 16px;
  }
}
</style>
