<template>
  <div class="page-container">
    <div class="page-header">
      <h2>
        <el-button link @click="router.back()">
          <el-icon><ArrowLeft /></el-icon>
        </el-button>
        物资详情 - {{ material?.name }}
      </h2>
    </div>

    <div v-if="material" class="material-detail">
      <div class="opera-card">
        <div class="material-info">
          <div class="info-row">
            <div class="info-item">
              <div class="detail-label">类别</div>
              <div class="detail-value">
                <el-tag type="info">{{ material.category_display || material.category }}</el-tag>
              </div>
            </div>
            <div class="info-item">
              <div class="detail-label">物资名称</div>
              <div class="detail-value">{{ material.name }}</div>
            </div>
            <div class="info-item">
              <div class="detail-label">编号</div>
              <div class="detail-value">{{ material.code || '-' }}</div>
            </div>
            <div class="info-item">
              <div class="detail-label">状态</div>
              <div class="detail-value">
                <el-tag :type="materialStatusTagType(material.status)">
                  {{ materialStatusText(material.status) }}
                </el-tag>
              </div>
            </div>
          </div>
          <div class="info-row">
            <div class="info-item">
              <div class="detail-label">所属节目</div>
              <div class="detail-value">{{ programName || '-' }}</div>
            </div>
            <div class="info-item">
              <div class="detail-label">适用角色</div>
              <div class="detail-value">{{ material.applicable_role || '-' }}</div>
            </div>
            <div class="info-item">
              <div class="detail-label">适用唱段</div>
              <div class="detail-value">{{ material.applicable_aria || '-' }}</div>
            </div>
            <div class="info-item">
              <div class="detail-label">适用行当</div>
              <div class="detail-value">{{ material.applicable_role_type_display || material.applicable_role_type || '-' }}</div>
            </div>
          </div>
          <div class="info-row">
            <div class="info-item">
              <div class="detail-label">规格尺码</div>
              <div class="detail-value">{{ material.size || '-' }}</div>
            </div>
            <div class="info-item">
              <div class="detail-label">颜色</div>
              <div class="detail-value">{{ material.color || '-' }}</div>
            </div>
            <div class="info-item">
              <div class="detail-label">材质</div>
              <div class="detail-value">{{ material.material || '-' }}</div>
            </div>
            <div class="info-item">
              <div class="detail-label">存放位置</div>
              <div class="detail-value">{{ material.storage_location || '-' }}</div>
            </div>
          </div>
          <div class="info-row">
            <div class="info-item">
              <div class="detail-label">总数量</div>
              <div class="detail-value">{{ material.total_quantity }}</div>
            </div>
            <div class="info-item">
              <div class="detail-label">可用数量</div>
              <div class="detail-value">
                <el-tag :type="material.available_quantity > 0 ? 'success' : 'danger'">
                  {{ material.available_quantity }}
                </el-tag>
              </div>
            </div>
            <div class="info-item">
              <div class="detail-label">负责人</div>
              <div class="detail-value">{{ memberName(material.responsible_member) || '-' }}</div>
            </div>
            <div class="info-item">
              <div class="detail-label">购置日期</div>
              <div class="detail-value">{{ material.purchase_date || '-' }}</div>
            </div>
          </div>
          <div class="info-row">
            <div class="info-item">
              <div class="detail-label">最近维护日期</div>
              <div class="detail-value">{{ material.last_maintenance_date || '-' }}</div>
            </div>
            <div class="info-item full-width">
              <div class="detail-label">维护备注</div>
              <div class="detail-value">{{ material.maintenance_notes || '暂无备注' }}</div>
            </div>
          </div>
          <div class="info-row">
            <div class="info-item full-width">
              <div class="detail-label">品相说明</div>
              <div class="detail-value">{{ material.condition_description || '暂无说明' }}</div>
            </div>
          </div>
          <div class="action-buttons">
            <el-button type="primary" size="small" :icon="ShoppingCart" :disabled="material.available_quantity <= 0" @click="openBorrowDialog">
              借用
            </el-button>
            <el-button type="success" size="small" :icon="RefreshRight" :disabled="!hasBorrowedRecords" @click="openReturnDialog">
              归还
            </el-button>
            <el-button type="warning" size="small" :icon="Warning" @click="openRepairDialog">
              报修
            </el-button>
            <el-button type="info" size="small" :icon="Edit" @click="openEditDialog">
              编辑
            </el-button>
            <el-button type="danger" size="small" :icon="Delete" @click="deleteMaterial">
              删除
            </el-button>
          </div>
        </div>
      </div>

      <el-tabs v-model="activeTab" class="material-tabs">
        <el-tab-pane label="借还记录" name="borrow">
          <div class="opera-card">
            <el-table :data="materialBorrowRecords" v-loading="store.loading" stripe empty-text="暂无借还记录">
              <el-table-column prop="borrower_name" label="借用人" width="100" />
              <el-table-column prop="rehearsal_check_name" label="关联联排" min-width="140" show-overflow-tooltip />
              <el-table-column prop="role_name" label="扮演角色" width="100" />
              <el-table-column prop="aria_name" label="演唱唱段" width="120" show-overflow-tooltip />
              <el-table-column prop="quantity" label="借用数量" width="90" />
              <el-table-column prop="purpose" label="用途" min-width="120" show-overflow-tooltip />
              <el-table-column prop="planned_pickup_date" label="计划取日期" width="110" />
              <el-table-column prop="planned_return_date" label="计划还日期" width="110" />
              <el-table-column prop="actual_pickup_date" label="实际取日期" width="110" />
              <el-table-column prop="actual_return_date" label="实际还日期" width="110" />
              <el-table-column prop="pickup_confirmer_name" label="取用人确认" width="100" />
              <el-table-column prop="return_confirmer_name" label="归还确认人" width="100" />
              <el-table-column label="状态" width="100">
                <template #default="{ row }">
                  <el-tag :type="borrowStatusTagType(row.status)">
                    {{ borrowStatusText(row.status) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="是否逾期" width="90">
                <template #default="{ row }">
                  <el-tag v-if="row.is_overdue" type="danger">逾期</el-tag>
                  <span v-else class="muted">-</span>
                </template>
              </el-table-column>
              <el-table-column prop="return_condition" label="归还品相" width="100" show-overflow-tooltip />
              <el-table-column label="是否损坏" width="90">
                <template #default="{ row }">
                  <el-tag v-if="row.is_damaged" type="danger">损坏</el-tag>
                  <span v-else class="muted">-</span>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="180" fixed="right">
                <template #default="{ row }">
                  <el-button
                    v-if="row.status === 'pending'"
                    type="success"
                    link
                    size="small"
                    @click="confirmPickup(row)"
                  >确认取用</el-button>
                  <el-button
                    v-if="row.status === 'borrowed'"
                    type="primary"
                    link
                    size="small"
                    @click="confirmReturn(row)"
                  >确认归还</el-button>
                  <el-button
                    v-if="row.status === 'pending'"
                    type="danger"
                    link
                    size="small"
                    @click="cancelBorrow(row)"
                  >取消</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>

        <el-tab-pane label="报修记录" name="repair">
          <div class="opera-card">
            <el-table :data="materialRepairRecords" v-loading="store.loading" stripe empty-text="暂无报修记录">
              <el-table-column prop="reporter_name" label="报修人" width="100" />
              <el-table-column prop="damage_type" label="损坏类型" width="100" />
              <el-table-column label="严重程度" width="100">
                <template #default="{ row }">
                  <el-tag type="danger">{{ row.severity_display || row.severity }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="damage_description" label="损坏描述/部位" min-width="180" show-overflow-tooltip />
              <el-table-column prop="estimated_cost" label="预估费用" width="100" />
              <el-table-column prop="actual_cost" label="实际费用" width="100" />
              <el-table-column prop="repair_vendor" label="维修方" width="120" show-overflow-tooltip />
              <el-table-column prop="repair_notes" label="维修备注" min-width="140" show-overflow-tooltip />
              <el-table-column label="状态" width="110">
                <template #default="{ row }">
                  <el-tag :type="repairStatusTagType(row.status)">
                    {{ repairStatusText(row.status) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="reported_at" label="报修时间" width="160">
                <template #default="{ row }">{{ formatTime(row.reported_at) }}</template>
              </el-table-column>
              <el-table-column prop="repair_started_at" label="开始维修时间" width="160">
                <template #default="{ row }">{{ formatTime(row.repair_started_at) }}</template>
              </el-table-column>
              <el-table-column prop="repair_completed_at" label="完成维修时间" width="160">
                <template #default="{ row }">{{ formatTime(row.repair_completed_at) }}</template>
              </el-table-column>
              <el-table-column prop="handler_name" label="处理人" width="100" />
              <el-table-column label="操作" width="160" fixed="right">
                <template #default="{ row }">
                  <el-button
                    v-if="row.status === 'reported'"
                    type="primary"
                    link
                    size="small"
                    @click="startRepair(row)"
                  >开始维修</el-button>
                  <el-button
                    v-if="row.status === 'in_progress'"
                    type="success"
                    link
                    size="small"
                    @click="completeRepair(row)"
                  >完成维修</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>

        <el-tab-pane label="替换申请" name="replace">
          <div class="opera-card">
            <el-table :data="materialReplaceRequests" v-loading="store.loading" stripe empty-text="暂无替换申请">
              <el-table-column prop="applicant_name" label="申请人" width="100" />
              <el-table-column prop="reason" label="申请原因" min-width="140" show-overflow-tooltip />
              <el-table-column prop="detailed_explanation" label="详细说明" min-width="180" show-overflow-tooltip />
              <el-table-column prop="required_size" label="要求尺码" width="100" />
              <el-table-column prop="required_spec" label="要求规格" width="120" show-overflow-tooltip />
              <el-table-column prop="required_date" label="需到位日期" width="110" />
              <el-table-column prop="replacement_material_name" label="替换物资名称" min-width="140" show-overflow-tooltip />
              <el-table-column label="状态" width="100">
                <template #default="{ row }">
                  <el-tag :type="replaceStatusTagType(row.status)">
                    {{ replaceStatusText(row.status) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="approver_name" label="审批人" width="100" />
              <el-table-column prop="approval_notes" label="审批备注" min-width="140" show-overflow-tooltip />
              <el-table-column prop="created_at" label="创建时间" width="160">
                <template #default="{ row }">{{ formatTime(row.created_at) }}</template>
              </el-table-column>
              <el-table-column prop="approved_at" label="审批时间" width="160">
                <template #default="{ row }">{{ formatTime(row.approved_at) }}</template>
              </el-table-column>
              <el-table-column prop="completed_at" label="完成时间" width="160">
                <template #default="{ row }">{{ formatTime(row.completed_at) }}</template>
              </el-table-column>
              <el-table-column label="操作" width="220" fixed="right">
                <template #default="{ row }">
                  <el-button
                    v-if="row.status === 'pending'"
                    type="primary"
                    link
                    size="small"
                    @click="approveReplace(row)"
                  >批准</el-button>
                  <el-button
                    v-if="row.status === 'pending'"
                    type="danger"
                    link
                    size="small"
                    @click="rejectReplace(row)"
                  >拒绝</el-button>
                  <el-button
                    v-if="row.status === 'approved'"
                    type="success"
                    link
                    size="small"
                    @click="completeReplace(row)"
                  >完成</el-button>
                  <el-button
                    v-if="row.status === 'pending'"
                    type="info"
                    link
                    size="small"
                    @click="cancelReplace(row)"
                  >取消</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>

        <el-tab-pane label="检查提醒" name="check">
          <div class="opera-card">
            <el-table :data="materialCheckItems" v-loading="store.loading" stripe empty-text="暂无检查待处理项">
              <el-table-column prop="rehearsal_check_name" label="关联联排批次" min-width="140" show-overflow-tooltip />
              <el-table-column prop="issue_type_display" label="问题类型" width="120" />
              <el-table-column prop="description" label="问题描述" min-width="180" show-overflow-tooltip />
              <el-table-column prop="aria_name" label="关联唱段" width="120" show-overflow-tooltip />
              <el-table-column prop="role_name" label="关联角色" width="100" />
              <el-table-column prop="member_name" label="关联成员" width="100" />
              <el-table-column prop="borrow_record_id" label="关联借还ID" width="100" />
              <el-table-column label="状态" width="100">
                <template #default="{ row }">
                  <el-tag :type="checkItemStatusTagType(row.status)">
                    {{ checkItemStatusText(row.status) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="handler_name" label="处理人" width="100" />
              <el-table-column prop="handler_note" label="处理备注" min-width="140" show-overflow-tooltip />
              <el-table-column prop="created_at" label="创建时间" width="160">
                <template #default="{ row }">{{ formatTime(row.created_at) }}</template>
              </el-table-column>
              <el-table-column prop="resolved_at" label="解决时间" width="160">
                <template #default="{ row }">{{ formatTime(row.resolved_at) }}</template>
              </el-table-column>
              <el-table-column label="操作" width="140" fixed="right">
                <template #default="{ row }">
                  <el-button
                    v-if="row.status === 'pending'"
                    type="success"
                    link
                    size="small"
                    @click="resolveCheckItem(row)"
                  >解决</el-button>
                  <el-button
                    v-if="row.status === 'pending'"
                    type="info"
                    link
                    size="small"
                    @click="waiveCheckItem(row)"
                  >忽略</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>

    <el-dialog v-model="borrowDialogVisible" title="借用物资" width="600px">
      <el-form :model="borrowForm" label-width="120px" ref="borrowFormRef">
        <el-form-item label="借用人" prop="borrower" :rules="[{ required: true, message: '请选择借用人', trigger: 'change' }]">
          <el-select v-model="borrowForm.borrower" placeholder="请选择成员" filterable style="width: 100%">
            <el-option v-for="m in store.members" :key="m.id" :label="m.name" :value="m.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="关联联排" prop="rehearsal_check">
          <el-select v-model="borrowForm.rehearsal_check" placeholder="请选择联排批次" filterable clearable style="width: 100%">
            <el-option v-for="c in programRehearsalChecks" :key="c.id" :label="c.name" :value="c.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="扮演角色" prop="role_name">
          <el-input v-model="borrowForm.role_name" placeholder="请输入扮演角色" />
        </el-form-item>
        <el-form-item label="演唱唱段" prop="aria_name">
          <el-input v-model="borrowForm.aria_name" placeholder="请输入演唱唱段" />
        </el-form-item>
        <el-form-item label="借用数量" prop="quantity" :rules="[{ required: true, message: '请输入借用数量', trigger: 'blur' }]">
          <el-input-number v-model="borrowForm.quantity" :min="1" :max="material?.available_quantity || 1" />
        </el-form-item>
        <el-form-item label="用途" prop="purpose">
          <el-input v-model="borrowForm.purpose" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="计划取日期" prop="planned_pickup_date">
          <el-date-picker v-model="borrowForm.planned_pickup_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
        <el-form-item label="计划还日期" prop="planned_return_date">
          <el-date-picker v-model="borrowForm.planned_return_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="borrowDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitBorrow">确认借用</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="returnDialogVisible" title="归还物资" width="600px">
      <el-form :model="returnForm" label-width="120px" ref="returnFormRef">
        <el-form-item label="选择借还记录" prop="borrow_record_id" :rules="[{ required: true, message: '请选择借还记录', trigger: 'change' }]">
          <el-select v-model="returnForm.borrow_record_id" placeholder="请选择借还记录" filterable style="width: 100%">
            <el-option
              v-for="r in borrowedRecords"
              :key="r.id"
              :label="`${r.borrower_name} - ${r.quantity}件 - ${r.planned_pickup_date || ''}`"
              :value="r.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="归还品相" prop="return_condition">
          <el-select v-model="returnForm.return_condition" placeholder="请选择品相" style="width: 100%">
            <el-option label="完好" value="完好" />
            <el-option label="轻微磨损" value="轻微磨损" />
            <el-option label="较旧" value="较旧" />
            <el-option label="损坏" value="损坏" />
          </el-select>
        </el-form-item>
        <el-form-item label="是否损坏" prop="is_damaged">
          <el-switch v-model="returnForm.is_damaged" />
        </el-form-item>
        <el-form-item label="备注" prop="notes">
          <el-input v-model="returnForm.notes" type="textarea" :rows="2" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="returnDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitReturn">确认归还</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="repairDialogVisible" title="报修物资" width="600px">
      <el-form :model="repairForm" label-width="120px" ref="repairFormRef">
        <el-form-item label="报修人" prop="reporter" :rules="[{ required: true, message: '请选择报修人', trigger: 'change' }]">
          <el-select v-model="repairForm.reporter" placeholder="请选择成员" filterable style="width: 100%">
            <el-option v-for="m in store.members" :key="m.id" :label="m.name" :value="m.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="损坏类型" prop="damage_type" :rules="[{ required: true, message: '请输入损坏类型', trigger: 'blur' }]">
          <el-input v-model="repairForm.damage_type" placeholder="如：开线、褪色、破损等" />
        </el-form-item>
        <el-form-item label="严重程度" prop="severity" :rules="[{ required: true, message: '请选择严重程度', trigger: 'change' }]">
          <el-select v-model="repairForm.severity" placeholder="请选择" style="width: 100%">
            <el-option label="轻微" value="minor" />
            <el-option label="中等" value="medium" />
            <el-option label="严重" value="severe" />
          </el-select>
        </el-form-item>
        <el-form-item label="损坏描述/部位" prop="damage_description" :rules="[{ required: true, message: '请输入损坏描述', trigger: 'blur' }]">
          <el-input v-model="repairForm.damage_description" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item label="预估费用" prop="estimated_cost">
          <el-input-number v-model="repairForm.estimated_cost" :min="0" :precision="2" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="repairDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitRepair">提交报修</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="editDialogVisible" :title="editingMaterial ? '编辑物资' : '编辑物资'" width="700px">
      <el-form :model="materialForm" label-width="110px" ref="materialFormRef">
        <el-form-item label="类别" prop="category" :rules="[{ required: true, message: '请选择类别', trigger: 'change' }]">
          <el-select v-model="materialForm.category" placeholder="请选择" style="width: 100%">
            <el-option label="戏服" value="costume" />
            <el-option label="头饰" value="headwear" />
            <el-option label="鞋靴" value="shoes" />
            <el-option label="道具" value="prop" />
            <el-option label="盔头" value="helmet" />
            <el-option label="髯口" value="beard" />
            <el-option label="把子" value="weapon" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="物资名称" prop="name" :rules="[{ required: true, message: '请输入物资名称', trigger: 'blur' }]">
          <el-input v-model="materialForm.name" />
        </el-form-item>
        <el-form-item label="编号" prop="code">
          <el-input v-model="materialForm.code" />
        </el-form-item>
        <el-form-item label="所属节目" prop="program" :rules="[{ required: true, message: '请选择节目', trigger: 'change' }]">
          <el-select v-model="materialForm.program" placeholder="请选择" filterable style="width: 100%">
            <el-option v-for="p in store.programs" :key="p.id" :label="p.name" :value="p.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="适用角色" prop="applicable_role">
          <el-input v-model="materialForm.applicable_role" placeholder="如：青衣、老生等" />
        </el-form-item>
        <el-form-item label="适用唱段" prop="applicable_aria">
          <el-input v-model="materialForm.applicable_aria" />
        </el-form-item>
        <el-form-item label="适用行当" prop="applicable_role_type">
          <el-select v-model="materialForm.applicable_role_type" placeholder="请选择" clearable style="width: 100%">
            <el-option label="生" value="sheng" />
            <el-option label="旦" value="dan" />
            <el-option label="净" value="jing" />
            <el-option label="末" value="mo" />
            <el-option label="丑" value="chou" />
          </el-select>
        </el-form-item>
        <el-form-item label="规格尺码" prop="size">
          <el-input v-model="materialForm.size" placeholder="如：L号、175等" />
        </el-form-item>
        <el-form-item label="颜色" prop="color">
          <el-input v-model="materialForm.color" />
        </el-form-item>
        <el-form-item label="材质" prop="material">
          <el-input v-model="materialForm.material" placeholder="如：丝绸、棉布等" />
        </el-form-item>
        <el-form-item label="存放位置" prop="storage_location">
          <el-input v-model="materialForm.storage_location" />
        </el-form-item>
        <el-form-item label="总数量" prop="total_quantity" :rules="[{ required: true, message: '请输入总数量', trigger: 'blur' }]">
          <el-input-number v-model="materialForm.total_quantity" :min="0" />
        </el-form-item>
        <el-form-item label="负责人" prop="responsible_member">
          <el-select v-model="materialForm.responsible_member" placeholder="请选择" filterable clearable style="width: 100%">
            <el-option v-for="m in store.members" :key="m.id" :label="m.name" :value="m.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status" :rules="[{ required: true, message: '请选择状态', trigger: 'change' }]">
          <el-select v-model="materialForm.status" placeholder="请选择" style="width: 100%">
            <el-option label="可用" value="available" />
            <el-option label="借用中" value="borrowed" />
            <el-option label="维修中" value="repairing" />
            <el-option label="报废" value="scrapped" />
            <el-option label="丢失" value="lost" />
          </el-select>
        </el-form-item>
        <el-form-item label="购置日期" prop="purchase_date">
          <el-date-picker v-model="materialForm.purchase_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
        <el-form-item label="最近维护日期" prop="last_maintenance_date">
          <el-date-picker v-model="materialForm.last_maintenance_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
        <el-form-item label="维护备注" prop="maintenance_notes">
          <el-input v-model="materialForm.maintenance_notes" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="品相说明" prop="condition_description">
          <el-input v-model="materialForm.condition_description" type="textarea" :rows="2" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="editDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitEdit">保存</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="startRepairDialogVisible" title="开始维修" width="500px">
      <el-form :model="startRepairForm" label-width="100px" ref="startRepairFormRef">
        <el-form-item label="处理人" prop="handler" :rules="[{ required: true, message: '请选择处理人', trigger: 'change' }]">
          <el-select v-model="startRepairForm.handler" placeholder="请选择成员" filterable style="width: 100%">
            <el-option v-for="m in store.members" :key="m.id" :label="m.name" :value="m.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="维修方" prop="repair_vendor">
          <el-input v-model="startRepairForm.repair_vendor" />
        </el-form-item>
        <el-form-item label="维修备注" prop="repair_notes">
          <el-input v-model="startRepairForm.repair_notes" type="textarea" :rows="2" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="startRepairDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitStartRepair">确认开始</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="completeRepairDialogVisible" title="完成维修" width="500px">
      <el-form :model="completeRepairForm" label-width="100px" ref="completeRepairFormRef">
        <el-form-item label="处理人" prop="handler" :rules="[{ required: true, message: '请选择处理人', trigger: 'change' }]">
          <el-select v-model="completeRepairForm.handler" placeholder="请选择成员" filterable style="width: 100%">
            <el-option v-for="m in store.members" :key="m.id" :label="m.name" :value="m.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="实际费用" prop="actual_cost">
          <el-input-number v-model="completeRepairForm.actual_cost" :min="0" :precision="2" />
        </el-form-item>
        <el-form-item label="维修备注" prop="repair_notes">
          <el-input v-model="completeRepairForm.repair_notes" type="textarea" :rows="2" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="completeRepairDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitCompleteRepair">确认完成</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="approveDialogVisible" title="批准替换申请" width="500px">
      <el-form :model="approveForm" label-width="100px" ref="approveFormRef">
        <el-form-item label="审批人" prop="approver" :rules="[{ required: true, message: '请选择审批人', trigger: 'change' }]">
          <el-select v-model="approveForm.approver" placeholder="请选择成员" filterable style="width: 100%">
            <el-option v-for="m in store.members" :key="m.id" :label="m.name" :value="m.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="审批备注" prop="approval_notes">
          <el-input v-model="approveForm.approval_notes" type="textarea" :rows="2" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="approveDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitApprove">确认批准</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="rejectDialogVisible" title="拒绝替换申请" width="500px">
      <el-form :model="rejectForm" label-width="100px" ref="rejectFormRef">
        <el-form-item label="审批人" prop="approver" :rules="[{ required: true, message: '请选择审批人', trigger: 'change' }]">
          <el-select v-model="rejectForm.approver" placeholder="请选择成员" filterable style="width: 100%">
            <el-option v-for="m in store.members" :key="m.id" :label="m.name" :value="m.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="拒绝原因" prop="approval_notes" :rules="[{ required: true, message: '请输入拒绝原因', trigger: 'blur' }]">
          <el-input v-model="rejectForm.approval_notes" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="rejectDialogVisible = false">取消</el-button>
        <el-button type="danger" @click="submitReject">确认拒绝</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="completeReplaceDialogVisible" title="完成替换" width="500px">
      <el-form :model="completeReplaceForm" label-width="100px" ref="completeReplaceFormRef">
        <el-form-item label="替换物资名称" prop="replacement_material_name">
          <el-input v-model="completeReplaceForm.replacement_material_name" />
        </el-form-item>
        <el-form-item label="完成备注" prop="completion_notes">
          <el-input v-model="completeReplaceForm.completion_notes" type="textarea" :rows="2" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="completeReplaceDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitCompleteReplace">确认完成</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="resolveDialogVisible" title="解决检查项" width="500px">
      <el-form :model="resolveForm" label-width="100px" ref="resolveFormRef">
        <el-form-item label="处理人" prop="handler" :rules="[{ required: true, message: '请选择处理人', trigger: 'change' }]">
          <el-select v-model="resolveForm.handler" placeholder="请选择成员" filterable style="width: 100%">
            <el-option v-for="m in store.members" :key="m.id" :label="m.name" :value="m.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="处理备注" prop="handler_note">
          <el-input v-model="resolveForm.handler_note" type="textarea" :rows="2" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="resolveDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitResolve">确认解决</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="waiveDialogVisible" title="忽略检查项" width="500px">
      <el-form :model="waiveForm" label-width="100px" ref="waiveFormRef">
        <el-form-item label="处理人" prop="handler" :rules="[{ required: true, message: '请选择处理人', trigger: 'change' }]">
          <el-select v-model="waiveForm.handler" placeholder="请选择成员" filterable style="width: 100%">
            <el-option v-for="m in store.members" :key="m.id" :label="m.name" :value="m.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="忽略原因" prop="handler_note" :rules="[{ required: true, message: '请输入忽略原因', trigger: 'blur' }]">
          <el-input v-model="waiveForm.handler_note" type="textarea" :rows="2" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="waiveDialogVisible = false">取消</el-button>
        <el-button type="info" @click="submitWaive">确认忽略</el-button>
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
  ArrowLeft, ShoppingCart, RefreshRight, Warning, Edit, Delete
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const store = useOperaStore()
const activeTab = ref('borrow')

const borrowDialogVisible = ref(false)
const returnDialogVisible = ref(false)
const repairDialogVisible = ref(false)
const editDialogVisible = ref(false)
const startRepairDialogVisible = ref(false)
const completeRepairDialogVisible = ref(false)
const approveDialogVisible = ref(false)
const rejectDialogVisible = ref(false)
const completeReplaceDialogVisible = ref(false)
const resolveDialogVisible = ref(false)
const waiveDialogVisible = ref(false)

const borrowFormRef = ref(null)
const returnFormRef = ref(null)
const repairFormRef = ref(null)
const materialFormRef = ref(null)
const startRepairFormRef = ref(null)
const completeRepairFormRef = ref(null)
const approveFormRef = ref(null)
const rejectFormRef = ref(null)
const completeReplaceFormRef = ref(null)
const resolveFormRef = ref(null)
const waiveFormRef = ref(null)

const material = computed(() => store.getMaterialById(route.params.id))
const programName = computed(() => {
  if (!material.value?.program) return ''
  const p = store.programs.find(x => x.id === material.value.program)
  return p ? p.name : ''
})
const materialBorrowRecords = computed(() => store.borrowRecords.filter(r => r.material === parseInt(route.params.id)))
const materialRepairRecords = computed(() => store.repairRecords.filter(r => r.material === parseInt(route.params.id)))
const materialReplaceRequests = computed(() => store.replaceRequests.filter(r => r.material === parseInt(route.params.id)))
const materialCheckItems = computed(() => store.materialCheckItems.filter(c => c.material === parseInt(route.params.id)))
const programRehearsalChecks = computed(() => {
  if (!material.value?.program) return []
  return store.rehearsalChecks.filter(c => c.program === material.value.program)
})
const hasBorrowedRecords = computed(() => materialBorrowRecords.value.some(r => r.status === 'borrowed'))
const borrowedRecords = computed(() => materialBorrowRecords.value.filter(r => r.status === 'borrowed'))

const editingMaterial = ref(null)
const editingRowId = ref(null)

const borrowForm = reactive({
  borrower: null,
  rehearsal_check: null,
  role_name: '',
  aria_name: '',
  quantity: 1,
  purpose: '',
  planned_pickup_date: '',
  planned_return_date: ''
})

const returnForm = reactive({
  borrow_record_id: null,
  return_condition: '完好',
  is_damaged: false,
  notes: ''
})

const repairForm = reactive({
  reporter: null,
  damage_type: '',
  severity: 'medium',
  damage_description: '',
  estimated_cost: 0
})

const materialForm = reactive({
  category: '',
  name: '',
  code: '',
  program: null,
  applicable_role: '',
  applicable_aria: '',
  applicable_role_type: '',
  size: '',
  color: '',
  material: '',
  storage_location: '',
  total_quantity: 0,
  responsible_member: null,
  status: 'available',
  purchase_date: '',
  last_maintenance_date: '',
  maintenance_notes: '',
  condition_description: ''
})

const startRepairForm = reactive({
  handler: null,
  repair_vendor: '',
  repair_notes: ''
})

const completeRepairForm = reactive({
  handler: null,
  actual_cost: 0,
  repair_notes: ''
})

const approveForm = reactive({
  approver: null,
  approval_notes: ''
})

const rejectForm = reactive({
  approver: null,
  approval_notes: ''
})

const completeReplaceForm = reactive({
  replacement_material_name: '',
  completion_notes: ''
})

const resolveForm = reactive({
  handler: null,
  handler_note: ''
})

const waiveForm = reactive({
  handler: null,
  handler_note: ''
})

onMounted(async () => {
  await Promise.all([
    store.loadMaterials(),
    store.loadPrograms(),
    store.loadMembers(),
    store.loadBorrowRecords(parseInt(route.params.id)),
    store.loadRepairRecords(parseInt(route.params.id)),
    store.loadReplaceRequests(),
    store.loadMaterialCheckItems(),
    store.loadRehearsalChecks()
  ])
})

function memberName(id) {
  if (!id) return ''
  const m = store.members.find(x => x.id === id)
  return m ? m.name : ''
}

function formatTime(value) {
  if (!value) return '-'
  return value.replace('T', ' ').substring(0, 16)
}

function materialStatusText(status) {
  const map = {
    'available': '可用',
    'borrowed': '借用中',
    'repairing': '维修中',
    'scrapped': '报废',
    'lost': '丢失'
  }
  return map[status] || status
}

function materialStatusTagType(status) {
  const map = {
    'available': 'success',
    'borrowed': 'primary',
    'repairing': 'warning',
    'scrapped': 'info',
    'lost': 'danger'
  }
  return map[status] || 'info'
}

function borrowStatusText(status) {
  const map = {
    'pending': '待取用',
    'borrowed': '借用中',
    'returned': '已归还',
    'overdue': '逾期',
    'lost': '丢失',
    'cancelled': '已取消'
  }
  return map[status] || status
}

function borrowStatusTagType(status) {
  const map = {
    'pending': 'warning',
    'borrowed': 'primary',
    'returned': 'success',
    'overdue': 'danger',
    'lost': 'info',
    'cancelled': 'info'
  }
  return map[status] || 'info'
}

function repairStatusText(status) {
  const map = {
    'reported': '已报修',
    'in_progress': '维修中',
    'completed': '已完成',
    'cannot_repair': '无法维修',
    'cancelled': '已取消'
  }
  return map[status] || status
}

function repairStatusTagType(status) {
  const map = {
    'reported': 'warning',
    'in_progress': 'primary',
    'completed': 'success',
    'cannot_repair': 'danger',
    'cancelled': 'info'
  }
  return map[status] || 'info'
}

function replaceStatusText(status) {
  const map = {
    'pending': '待审批',
    'approved': '已批准',
    'rejected': '已拒绝',
    'completed': '已完成',
    'cancelled': '已取消'
  }
  return map[status] || status
}

function replaceStatusTagType(status) {
  const map = {
    'pending': 'warning',
    'approved': 'primary',
    'rejected': 'danger',
    'completed': 'success',
    'cancelled': 'info'
  }
  return map[status] || 'info'
}

function checkItemStatusText(status) {
  const map = {
    'pending': '待处理',
    'resolved': '已解决',
    'waived': '已忽略'
  }
  return map[status] || status
}

function checkItemStatusTagType(status) {
  const map = {
    'pending': 'danger',
    'resolved': 'success',
    'waived': 'info'
  }
  return map[status] || 'info'
}

function openBorrowDialog() {
  Object.assign(borrowForm, {
    borrower: null,
    rehearsal_check: null,
    role_name: '',
    aria_name: '',
    quantity: 1,
    purpose: '',
    planned_pickup_date: '',
    planned_return_date: ''
  })
  borrowDialogVisible.value = true
}

async function submitBorrow() {
  try {
    await borrowFormRef.value.validate()
    const data = {
      ...borrowForm,
      material: parseInt(route.params.id)
    }
    await store.addBorrowRecord(data)
    ElMessage.success('借用申请已提交')
    borrowDialogVisible.value = false
    await Promise.all([
      store.loadMaterials(),
      store.loadBorrowRecords(parseInt(route.params.id))
    ])
  } catch (error) {
    if (error !== false && error?.message) {
      ElMessage.error('操作失败：' + error.message)
    } else if (error !== false) {
      ElMessage.error('操作失败')
    }
  }
}

function openReturnDialog() {
  Object.assign(returnForm, {
    borrow_record_id: null,
    return_condition: '完好',
    is_damaged: false,
    notes: ''
  })
  returnDialogVisible.value = true
}

async function submitReturn() {
  try {
    await returnFormRef.value.validate()
    await store.confirmReturnRecordById(returnForm.borrow_record_id, {
      return_condition: returnForm.return_condition,
      is_damaged: returnForm.is_damaged,
      notes: returnForm.notes
    })
    ElMessage.success('归还确认成功')
    returnDialogVisible.value = false
    await Promise.all([
      store.loadMaterials(),
      store.loadBorrowRecords(parseInt(route.params.id))
    ])
  } catch (error) {
    if (error !== false && error?.message) {
      ElMessage.error('操作失败：' + error.message)
    } else if (error !== false) {
      ElMessage.error('操作失败')
    }
  }
}

function openRepairDialog() {
  Object.assign(repairForm, {
    reporter: null,
    damage_type: '',
    severity: 'medium',
    damage_description: '',
    estimated_cost: 0
  })
  repairDialogVisible.value = true
}

async function submitRepair() {
  try {
    await repairFormRef.value.validate()
    await store.addRepairRecord({
      ...repairForm,
      material: parseInt(route.params.id)
    })
    ElMessage.success('报修已提交')
    repairDialogVisible.value = false
    await Promise.all([
      store.loadMaterials(),
      store.loadRepairRecords(parseInt(route.params.id))
    ])
  } catch (error) {
    if (error !== false && error?.message) {
      ElMessage.error('操作失败：' + error.message)
    } else if (error !== false) {
      ElMessage.error('操作失败')
    }
  }
}

function openEditDialog() {
  editingMaterial.value = material.value
  if (material.value) {
    Object.assign(materialForm, { ...material.value })
  }
  editDialogVisible.value = true
}

async function submitEdit() {
  try {
    await materialFormRef.value.validate()
    await store.editMaterial(parseInt(route.params.id), materialForm)
    ElMessage.success('物资更新成功')
    editDialogVisible.value = false
    await store.loadMaterials()
  } catch (error) {
    if (error !== false && error?.message) {
      ElMessage.error('操作失败：' + error.message)
    } else if (error !== false) {
      ElMessage.error('操作失败')
    }
  }
}

function deleteMaterial() {
  ElMessageBox.confirm(`确定要删除物资"${material.value.name}"吗？`, '删除确认', { type: 'warning' })
    .then(async () => {
      await store.removeMaterial(parseInt(route.params.id))
      ElMessage.success('删除成功')
      router.back()
    }).catch(() => {})
}

async function confirmPickup(row) {
  try {
    await store.confirmBorrowRecordById(row.id)
    ElMessage.success('取用确认成功')
    await Promise.all([
      store.loadMaterials(),
      store.loadBorrowRecords(parseInt(route.params.id))
    ])
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

async function confirmReturn(row) {
  try {
    await store.confirmReturnRecordById(row.id, {})
    ElMessage.success('归还确认成功')
    await Promise.all([
      store.loadMaterials(),
      store.loadBorrowRecords(parseInt(route.params.id))
    ])
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

async function cancelBorrow(row) {
  ElMessageBox.confirm('确定要取消该借用记录吗？', '取消确认', { type: 'warning' })
    .then(async () => {
      await store.cancelBorrowRecordById(row.id)
      ElMessage.success('取消成功')
      await Promise.all([
        store.loadMaterials(),
        store.loadBorrowRecords(parseInt(route.params.id))
      ])
    }).catch(() => {})
}

function startRepair(row) {
  editingRowId.value = row.id
  Object.assign(startRepairForm, {
    handler: null,
    repair_vendor: row.repair_vendor || '',
    repair_notes: ''
  })
  startRepairDialogVisible.value = true
}

async function submitStartRepair() {
  try {
    await startRepairFormRef.value.validate()
    await store.startRepairById(editingRowId.value, startRepairForm)
    ElMessage.success('维修已开始')
    startRepairDialogVisible.value = false
    await Promise.all([
      store.loadMaterials(),
      store.loadRepairRecords(parseInt(route.params.id))
    ])
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

function completeRepair(row) {
  editingRowId.value = row.id
  Object.assign(completeRepairForm, {
    handler: null,
    actual_cost: row.actual_cost || 0,
    repair_notes: ''
  })
  completeRepairDialogVisible.value = true
}

async function submitCompleteRepair() {
  try {
    await completeRepairFormRef.value.validate()
    await store.completeRepairById(editingRowId.value, completeRepairForm)
    ElMessage.success('维修已完成')
    completeRepairDialogVisible.value = false
    await Promise.all([
      store.loadMaterials(),
      store.loadRepairRecords(parseInt(route.params.id))
    ])
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

function approveReplace(row) {
  editingRowId.value = row.id
  Object.assign(approveForm, {
    approver: null,
    approval_notes: ''
  })
  approveDialogVisible.value = true
}

async function submitApprove() {
  try {
    await approveFormRef.value.validate()
    await store.approveReplaceRequestById(editingRowId.value, approveForm)
    ElMessage.success('已批准')
    approveDialogVisible.value = false
    await store.loadReplaceRequests()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

function rejectReplace(row) {
  editingRowId.value = row.id
  Object.assign(rejectForm, {
    approver: null,
    approval_notes: ''
  })
  rejectDialogVisible.value = true
}

async function submitReject() {
  try {
    await rejectFormRef.value.validate()
    await store.rejectReplaceRequestById(editingRowId.value, rejectForm)
    ElMessage.success('已拒绝')
    rejectDialogVisible.value = false
    await store.loadReplaceRequests()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

function completeReplace(row) {
  editingRowId.value = row.id
  Object.assign(completeReplaceForm, {
    replacement_material_name: row.replacement_material_name || '',
    completion_notes: ''
  })
  completeReplaceDialogVisible.value = true
}

async function submitCompleteReplace() {
  try {
    await completeReplaceFormRef.value.validate()
    await store.completeReplaceRequestById(editingRowId.value, completeReplaceForm)
    ElMessage.success('替换已完成')
    completeReplaceDialogVisible.value = false
    await store.loadReplaceRequests()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

async function cancelReplace(row) {
  ElMessageBox.confirm('确定要取消该替换申请吗？', '取消确认', { type: 'warning' })
    .then(async () => {
      await store.cancelReplaceRequestById(row.id)
      ElMessage.success('取消成功')
      await store.loadReplaceRequests()
    }).catch(() => {})
}

function resolveCheckItem(row) {
  editingRowId.value = row.id
  Object.assign(resolveForm, {
    handler: null,
    handler_note: ''
  })
  resolveDialogVisible.value = true
}

async function submitResolve() {
  try {
    await resolveFormRef.value.validate()
    await store.resolveCheckItemById(editingRowId.value, resolveForm)
    ElMessage.success('已解决')
    resolveDialogVisible.value = false
    await store.loadMaterialCheckItems()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

function waiveCheckItem(row) {
  editingRowId.value = row.id
  Object.assign(waiveForm, {
    handler: null,
    handler_note: ''
  })
  waiveDialogVisible.value = true
}

async function submitWaive() {
  try {
    await waiveFormRef.value.validate()
    await store.waiveCheckItemById(editingRowId.value, waiveForm)
    ElMessage.success('已忽略')
    waiveDialogVisible.value = false
    await store.loadMaterialCheckItems()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}
</script>

<style lang="scss" scoped>
.material-info {
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

.action-buttons {
  display: flex;
  gap: 12px;
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid #E8DCC8;
}

.material-tabs {
  :deep(.el-tabs__item.is-active) {
    color: #C41E3A !important;
  }
  
  :deep(.el-tabs__active-bar) {
    background-color: #D4AF37 !important;
  }
}

.muted {
  color: #999;
  font-size: 12px;
}
</style>
