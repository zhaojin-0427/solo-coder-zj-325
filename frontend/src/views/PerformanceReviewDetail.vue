<template>
  <div class="page-container">
    <div class="page-header">
      <h2>
        <el-button link @click="router.back()">
          <el-icon><ArrowLeft /></el-icon>
        </el-button>
        复盘详情 - {{ review?.name }}
      </h2>
      <div class="header-actions">
        <el-button v-if="review?.status === 'draft'" type="warning" @click="handleStartTeacherReview">
          开始老师复盘
        </el-button>
        <el-button v-if="review?.status === 'teacher_reviewing'" type="primary" @click="handleStartMemberReview">
          开始成员自评
        </el-button>
        <el-button v-if="review?.status === 'member_reviewing'" type="success" @click="handleCompleteReview">
          完成复盘
        </el-button>
      </div>
    </div>

    <div v-if="review" class="review-detail">
      <div class="opera-card">
        <div class="review-header">
          <div class="review-info-row">
            <div class="info-item">
              <div class="detail-label">节目名称</div>
              <div class="detail-value">{{ review.program_name }}</div>
            </div>
            <div class="info-item">
              <div class="detail-label">演出日期</div>
              <div class="detail-value">{{ review.performance_date }}</div>
            </div>
            <div class="info-item">
              <div class="detail-label">状态</div>
              <div class="detail-value">
                <el-tag :type="statusTagType(review.status)">{{ review.status_display }}</el-tag>
              </div>
            </div>
            <div class="info-item">
              <div class="detail-label">归档版本</div>
              <div class="detail-value">{{ review.archive_version ? 'v' + review.archive_version : '未关联' }}</div>
            </div>
          </div>
          <div class="review-stats">
            <div class="stat-item">
              <div class="stat-value">{{ review.item_count }}</div>
              <div class="stat-label">复盘唱段</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ review.conclusion_count }}</div>
              <div class="stat-label">老师点评</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ review.self_review_total }}</div>
              <div class="stat-label">成员自评</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ review.improvement_task_count }}</div>
              <div class="stat-label">改进任务</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ review.completion_rate }}%</div>
              <div class="stat-label">完成率</div>
            </div>
          </div>
        </div>
        <div v-if="review.actual_performance_note" class="performance-note">
          <div class="detail-label">演出备注</div>
          <div class="detail-value">{{ review.actual_performance_note }}</div>
        </div>
      </div>

      <el-tabs v-model="activeTab" class="review-tabs">
        <el-tab-pane label="复盘清单" name="items">
          <div class="opera-card">
            <h3 class="section-title">复盘清单</h3>
            <el-table :data="store.reviewItems" v-loading="store.loading" stripe>
              <el-table-column prop="order_index" label="序号" width="70" />
              <el-table-column prop="aria_name" label="唱段名称" min-width="180" />
              <el-table-column prop="role_type_display" label="行当" width="90" />
              <el-table-column label="最终分配" min-width="200">
                <template #default="{ row }">
                  <div class="assignment-tags">
                    <el-tag 
                      v-for="a in row.final_assignments" 
                      :key="a.member_id"
                      :type="a.is_understudy ? 'warning' : 'primary'"
                      size="small"
                      style="margin-right: 4px; margin-bottom: 4px"
                    >
                      {{ a.member_name }}{{ a.is_understudy ? '(替补)' : '' }}
                    </el-tag>
                  </div>
                </template>
              </el-table-column>
              <el-table-column label="老师复盘" width="100">
                <template #default="{ row }">
                  <el-tag :type="row.has_conclusion ? 'success' : 'info'">
                    {{ row.has_conclusion ? '已完成' : '待填写' }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="成员自评" width="100">
                <template #default="{ row }">
                  <el-tag type="warning">{{ row.self_review_count }}条</el-tag>
                </template>
              </el-table-column>
              <el-table-column label="改进任务" width="100">
                <template #default="{ row }">
                  <el-tag type="danger">{{ row.improvement_task_count }}个</el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="200" fixed="right">
                <template #default="{ row }">
                  <el-button type="primary" link size="small" @click="openItemDetail(row)">详情</el-button>
                  <el-button 
                    v-if="canAddConclusion" 
                    type="warning" 
                    link 
                    size="small" 
                    @click="openConclusionDialog(row)"
                  >
                    {{ row.has_conclusion ? '编辑点评' : '添加点评' }}
                  </el-button>
                  <el-button type="danger" link size="small" @click="openConvertTaskDialog(row)">
                    转任务
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>

        <el-tab-pane label="改进任务" name="tasks">
          <div class="tab-header">
            <h3 class="section-title">改进训练任务</h3>
            <el-button type="primary" size="small" @click="openTaskDialog">
              <el-icon><Plus /></el-icon>
              新建任务
            </el-button>
          </div>
          <div class="opera-card">
            <el-table :data="store.improvementTasks" v-loading="store.loading" stripe>
              <el-table-column prop="task_title" label="任务标题" min-width="200" />
              <el-table-column prop="aria_name" label="关联唱段" width="140" />
              <el-table-column label="来源类型" width="120">
                <template #default="{ row }">
                  <el-tag size="small">{{ row.source_type_display }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column label="优先级" width="90">
                <template #default="{ row }">
                  <el-tag :type="priorityTagType(row.priority)" size="small">{{ row.priority_display }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column label="状态" width="100">
                <template #default="{ row }">
                  <el-tag :type="taskStatusTagType(row.status)" size="small">{{ row.status_display }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="assignee_name" label="责任人" width="100" />
              <el-table-column prop="deadline" label="截止时间" width="120" />
              <el-table-column label="操作" width="200" fixed="right">
                <template #default="{ row }">
                  <el-button v-if="row.status === 'pending'" type="primary" link size="small" @click="handleStartTask(row)">开始</el-button>
                  <el-button v-if="row.status === 'in_progress'" type="success" link size="small" @click="handleCompleteTask(row)">完成</el-button>
                  <el-button type="warning" link size="small" @click="openTaskDialog(row)">编辑</el-button>
                  <el-button type="danger" link size="small" @click="deleteTask(row)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>

    <el-dialog v-model="itemDetailVisible" :title="currentItem?.aria_name + ' - 复盘详情'" width="900px">
      <div v-if="currentItem" class="item-detail-dialog">
        <el-tabs v-model="itemDetailTab">
          <el-tab-pane label="基本信息" name="basic">
            <div class="detail-section">
              <h4>唱段信息</h4>
              <div class="info-grid">
                <div class="info-item">
                  <div class="detail-label">唱段名称</div>
                  <div class="detail-value">{{ currentItem.aria_name }}</div>
                </div>
                <div class="info-item">
                  <div class="detail-label">行当</div>
                  <div class="detail-value">{{ currentItem.role_type_display }}</div>
                </div>
                <div class="info-item">
                  <div class="detail-label">演出顺序</div>
                  <div class="detail-value">第 {{ currentItem.order_index }} 段</div>
                </div>
              </div>
            </div>
            <div class="detail-section">
              <h4>最终分配</h4>
              <div class="assignment-list">
                <div v-for="a in currentItem.final_assignments" :key="a.member_id" class="assignment-item">
                  <el-tag :type="a.is_understudy ? 'warning' : 'primary'">
                    {{ a.member_name }}{{ a.is_understudy ? '（替补）' : '' }}
                  </el-tag>
                  <span class="role-name">{{ a.role_name }}</span>
                </div>
              </div>
            </div>
          </el-tab-pane>

          <el-tab-pane label="联排确认汇总" name="rehearsal">
            <div v-if="currentItem.rehearsal_check_summary?.check_name" class="detail-section">
              <h4>{{ currentItem.rehearsal_check_summary.check_name }}</h4>
              <div class="info-grid">
                <div class="info-item">
                  <div class="detail-label">风险等级</div>
                  <div class="detail-value">
                    <el-tag :type="riskTagType(currentItem.rehearsal_check_summary.risk_level)">
                      {{ currentItem.rehearsal_check_summary.risk_level_display }}
                    </el-tag>
                  </div>
                </div>
                <div class="info-item">
                  <div class="detail-label">伴奏确认</div>
                  <div class="detail-value">
                    {{ currentItem.rehearsal_check_summary.accompaniment_confirmed ? '已确认' : '未确认' }}
                  </div>
                </div>
                <div class="info-item full-width">
                  <div class="detail-label">老师处理意见</div>
                  <div class="detail-value">{{ currentItem.rehearsal_check_summary.teacher_comment || '无' }}</div>
                </div>
              </div>
            </div>
            <div v-else class="empty-state">
              <el-icon><Document /></el-icon>
              <p>暂无联排确认记录</p>
            </div>
          </el-tab-pane>

          <el-tab-pane label="风险处理记录" name="risks">
            <div v-if="currentItem.risk_record_summary?.length" class="detail-section">
              <el-table :data="currentItem.risk_record_summary" size="small" stripe>
                <el-table-column prop="action_type_display" label="风险类型" width="140" />
                <el-table-column prop="description" label="描述" min-width="250" show-overflow-tooltip />
                <el-table-column prop="status_display" label="状态" width="100">
                  <template #default="{ row }">
                    <el-tag :type="row.status === 'pending' ? 'danger' : 'success'" size="small">
                      {{ row.status_display }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="handler_name" label="处理人" width="100" />
                <el-table-column prop="handler_note" label="处理备注" min-width="150" show-overflow-tooltip />
              </el-table>
            </div>
            <div v-else class="empty-state">
              <el-icon><Document /></el-icon>
              <p>暂无风险处理记录</p>
            </div>
          </el-tab-pane>

          <el-tab-pane label="排练反馈汇总" name="feedbacks">
            <div v-if="currentItem.rehearsal_feedback_summary?.length" class="detail-section">
              <div v-for="fb in currentItem.rehearsal_feedback_summary" :key="fb.id" class="feedback-item">
                <div class="feedback-header">
                  <span class="feedback-date">{{ fb.rehearsal_date }}</span>
                  <span class="feedback-member">{{ fb.member_name }}</span>
                </div>
                <div v-if="fb.start_beat_issue" class="feedback-item-row">
                  <span class="label">起板问题：</span>
                  <span>{{ fb.start_beat_issue }}</span>
                </div>
                <div v-if="fb.forgotten_lines" class="feedback-item-row">
                  <span class="label">忘词片段：</span>
                  <span>{{ fb.forgotten_lines }}</span>
                </div>
                <div v-if="fb.teacher_comments" class="feedback-item-row">
                  <span class="label">老师点评：</span>
                  <span>{{ fb.teacher_comments }}</span>
                </div>
              </div>
            </div>
            <div v-else class="empty-state">
              <el-icon><Document /></el-icon>
              <p>暂无排练反馈记录</p>
            </div>
          </el-tab-pane>

          <el-tab-pane label="替补发生记录" name="understudy">
            <div v-if="currentItem.understudy_record_summary?.length" class="detail-section">
              <el-table :data="currentItem.understudy_record_summary" size="small" stripe>
                <el-table-column prop="date" label="日期" width="120" />
                <el-table-column label="调整" min-width="200">
                  <template #default="{ row }">
                    {{ row.original_member_name }} → {{ row.substitute_member_name }}
                  </template>
                </el-table-column>
                <el-table-column prop="reason" label="原因" min-width="200" show-overflow-tooltip />
                <el-table-column prop="status_display" label="状态" width="100">
                  <template #default="{ row }">
                    <el-tag size="small">{{ row.status_display }}</el-tag>
                  </template>
                </el-table-column>
              </el-table>
            </div>
            <div v-else class="empty-state">
              <el-icon><Document /></el-icon>
              <p>暂无替补调整记录</p>
            </div>
          </el-tab-pane>

          <el-tab-pane label="老师复盘结论" name="conclusion">
            <div v-if="currentItem.conclusions?.length" class="detail-section">
              <div v-for="c in currentItem.conclusions" :key="c.id" class="conclusion-card">
                <div class="conclusion-header">
                  <span class="conclusion-teacher">{{ c.teacher_name || '老师' }}</span>
                  <span class="conclusion-date">{{ formatDate(c.created_at) }}</span>
                </div>
                <div class="conclusion-grid">
                  <div class="conclusion-item">
                    <div class="detail-label">舞台表现</div>
                    <div class="detail-value">
                      <el-tag :type="stagePerfTagType(c.stage_performance)">{{ c.stage_performance_display }}</el-tag>
                    </div>
                  </div>
                  <div class="conclusion-item">
                    <div class="detail-label">节奏稳定性</div>
                    <div class="detail-value">
                      <el-tag :type="rhythmTagType(c.rhythm_stability)">{{ c.rhythm_stability_display }}</el-tag>
                    </div>
                  </div>
                </div>
                <div v-if="c.forgotten_lines" class="conclusion-row">
                  <div class="detail-label">忘词问题</div>
                  <div class="detail-value">{{ c.forgotten_lines }}</div>
                </div>
                <div v-if="c.beat_issues" class="conclusion-row">
                  <div class="detail-label">抢板/掉板问题</div>
                  <div class="detail-value">{{ c.beat_issues }}</div>
                </div>
                <div v-if="c.accompaniment_cohesion" class="conclusion-row">
                  <div class="detail-label">伴奏衔接问题</div>
                  <div class="detail-value">{{ c.accompaniment_cohesion }}</div>
                </div>
                <div v-if="c.overall_comment" class="conclusion-row">
                  <div class="detail-label">整体点评</div>
                  <div class="detail-value">{{ c.overall_comment }}</div>
                </div>
                <div v-if="c.improvement_suggestions" class="conclusion-row">
                  <div class="detail-label">改进建议</div>
                  <div class="detail-value highlight">{{ c.improvement_suggestions }}</div>
                </div>
              </div>
            </div>
            <div v-else class="empty-state">
              <el-icon><Edit /></el-icon>
              <p>暂无老师复盘结论</p>
              <el-button v-if="canAddConclusion" type="primary" size="small" @click="openConclusionDialog(currentItem)">
                添加点评
              </el-button>
            </div>
          </el-tab-pane>

          <el-tab-pane label="成员自评" name="selfReview">
            <div v-if="currentItem.self_reviews?.length" class="detail-section">
              <div v-for="sr in currentItem.self_reviews" :key="sr.id" class="self-review-card">
                <div class="self-review-header">
                  <span class="self-review-member">{{ sr.member_name }}</span>
                  <el-rate v-model="sr.self_rating" disabled size="small" />
                </div>
                <div v-if="sr.highlights" class="self-review-row">
                  <div class="detail-label">本场亮点</div>
                  <div class="detail-value">{{ sr.highlights }}</div>
                </div>
                <div v-if="sr.self_comment" class="self-review-row">
                  <div class="detail-label">自我评语</div>
                  <div class="detail-value">{{ sr.self_comment }}</div>
                </div>
                <div v-if="sr.improvement_goal" class="self-review-row">
                  <div class="detail-label">改进目标</div>
                  <div class="detail-value highlight">{{ sr.improvement_goal }}</div>
                </div>
              </div>
            </div>
            <div v-else class="empty-state">
              <el-icon><User /></el-icon>
              <p>暂无成员自评</p>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
    </el-dialog>

    <el-dialog v-model="conclusionDialogVisible" :title="conclusionDialogTitle" width="600px">
      <el-form :model="conclusionForm" label-width="120px" ref="conclusionFormRef">
        <el-form-item label="舞台表现" prop="stage_performance">
          <el-select v-model="conclusionForm.stage_performance" style="width: 100%">
            <el-option label="优秀" value="excellent" />
            <el-option label="良好" value="good" />
            <el-option label="一般" value="average" />
            <el-option label="需改进" value="needs_improvement" />
          </el-select>
        </el-form-item>
        <el-form-item label="节奏稳定性" prop="rhythm_stability">
          <el-select v-model="conclusionForm.rhythm_stability" style="width: 100%">
            <el-option label="稳定" value="stable" />
            <el-option label="基本稳定" value="mostly_stable" />
            <el-option label="不稳定" value="unstable" />
          </el-select>
        </el-form-item>
        <el-form-item label="忘词问题" prop="forgotten_lines">
          <el-input v-model="conclusionForm.forgotten_lines" type="textarea" :rows="2" placeholder="如有忘词问题请描述" />
        </el-form-item>
        <el-form-item label="抢板/掉板" prop="beat_issues">
          <el-input v-model="conclusionForm.beat_issues" type="textarea" :rows="2" placeholder="如有节奏问题请描述" />
        </el-form-item>
        <el-form-item label="伴奏衔接" prop="accompaniment_cohesion">
          <el-input v-model="conclusionForm.accompaniment_cohesion" type="textarea" :rows="2" placeholder="如有伴奏衔接问题请描述" />
        </el-form-item>
        <el-form-item label="整体点评" prop="overall_comment">
          <el-input v-model="conclusionForm.overall_comment" type="textarea" :rows="3" placeholder="整体表现点评" />
        </el-form-item>
        <el-form-item label="改进建议" prop="improvement_suggestions">
          <el-input v-model="conclusionForm.improvement_suggestions" type="textarea" :rows="3" placeholder="具体改进建议" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="conclusionDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitConclusion">保存</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="taskDialogVisible" :title="taskDialogTitle" width="600px">
      <el-form :model="taskForm" label-width="100px" ref="taskFormRef">
        <el-form-item label="任务标题" prop="task_title" :rules="[{ required: true }]">
          <el-input v-model="taskForm.task_title" />
        </el-form-item>
        <el-form-item label="任务描述" prop="task_description">
          <el-input v-model="taskForm.task_description" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item label="来源类型" prop="source_type">
          <el-select v-model="taskForm.source_type" style="width: 100%">
            <el-option label="未解决风险" value="risk" />
            <el-option label="演出中暴露问题" value="performance_issue" />
            <el-option label="老师改进建议" value="teacher_suggestion" />
            <el-option label="个人改进目标" value="self_goal" />
          </el-select>
        </el-form-item>
        <el-form-item label="优先级" prop="priority">
          <el-radio-group v-model="taskForm.priority">
            <el-radio value="high">高</el-radio>
            <el-radio value="medium">中</el-radio>
            <el-radio value="low">低</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="责任人" prop="assignee_id">
          <el-select v-model="taskForm.assignee_id" style="width: 100%" clearable>
            <el-option
              v-for="m in store.members"
              :key="m.id"
              :label="m.name"
              :value="m.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="截止时间" prop="deadline">
          <el-date-picker v-model="taskForm.deadline" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="taskDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitTask">保存</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="convertTaskDialogVisible" title="转为改进任务" width="600px">
      <el-form :model="convertTaskForm" label-width="100px" ref="convertTaskFormRef">
        <el-form-item label="任务标题" prop="task_title" :rules="[{ required: true }]">
          <el-input v-model="convertTaskForm.task_title" />
        </el-form-item>
        <el-form-item label="任务描述" prop="task_description">
          <el-input v-model="convertTaskForm.task_description" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item label="来源类型" prop="source_type">
          <el-select v-model="convertTaskForm.source_type" style="width: 100%">
            <el-option label="演出中暴露问题" value="performance_issue" />
            <el-option label="老师改进建议" value="teacher_suggestion" />
            <el-option label="未解决风险" value="risk" />
          </el-select>
        </el-form-item>
        <el-form-item label="来源描述" prop="source_description">
          <el-input v-model="convertTaskForm.source_description" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="优先级" prop="priority">
          <el-radio-group v-model="convertTaskForm.priority">
            <el-radio value="high">高</el-radio>
            <el-radio value="medium">中</el-radio>
            <el-radio value="low">低</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="责任人" prop="assignee_id">
          <el-select v-model="convertTaskForm.assignee_id" style="width: 100%" clearable>
            <el-option
              v-for="m in store.members"
              :key="m.id"
              :label="m.name"
              :value="m.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="截止时间" prop="deadline">
          <el-date-picker v-model="convertTaskForm.deadline" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="convertTaskDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitConvertTask">创建任务</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useOperaStore } from '@/stores/opera'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowLeft, Plus, Document, Edit, User } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const store = useOperaStore()

const activeTab = ref('items')
const itemDetailVisible = ref(false)
const itemDetailTab = ref('basic')
const currentItem = ref(null)
const conclusionDialogVisible = ref(false)
const conclusionFormRef = ref(null)
const taskDialogVisible = ref(false)
const taskFormRef = ref(null)
const convertTaskDialogVisible = ref(false)
const convertTaskFormRef = ref(null)
const editingTask = ref(null)

const review = computed(() => store.getPerformanceReviewById(route.params.id))
const canAddConclusion = computed(() => 
  review.value && ['teacher_reviewing', 'member_reviewing', 'completed'].includes(review.value.status)
)

const conclusionDialogTitle = computed(() => 
  editingConclusion.value ? '编辑复盘结论' : '添加复盘结论'
)
const taskDialogTitle = computed(() => 
  editingTask.value ? '编辑改进任务' : '新建改进任务'
)

const editingConclusion = ref(null)

const conclusionForm = reactive({
  review_item: null,
  stage_performance: 'good',
  rhythm_stability: 'mostly_stable',
  forgotten_lines: '',
  beat_issues: '',
  accompaniment_cohesion: '',
  overall_comment: '',
  improvement_suggestions: ''
})

const taskForm = reactive({
  review: null,
  review_item: null,
  task_title: '',
  task_description: '',
  source_type: 'performance_issue',
  source_description: '',
  priority: 'medium',
  assignee_id: null,
  deadline: ''
})

const convertTaskForm = reactive({
  review_item_id: null,
  task_title: '',
  task_description: '',
  source_type: 'performance_issue',
  source_description: '',
  priority: 'medium',
  assignee_id: null,
  deadline: ''
})

onMounted(async () => {
  await Promise.all([
    store.loadPrograms(),
    store.loadPerformanceReviews(),
    store.loadMembers()
  ])
  await loadReviewData()
})

async function loadReviewData() {
  const reviewId = parseInt(route.params.id)
  await Promise.all([
    store.loadReviewItems(reviewId),
    store.loadImprovementTasks(reviewId),
    store.loadReviewConclusions(reviewId),
    store.loadSelfReviews(reviewId)
  ])
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

function priorityTagType(priority) {
  const map = {
    'high': 'danger',
    'medium': 'warning',
    'low': 'info'
  }
  return map[priority] || 'info'
}

function taskStatusTagType(status) {
  const map = {
    'pending': 'info',
    'in_progress': 'warning',
    'completed': 'success',
    'cancelled': 'info'
  }
  return map[status] || 'info'
}

function riskTagType(level) {
  const map = {
    'none': 'success',
    'low': 'info',
    'medium': 'warning',
    'high': 'danger'
  }
  return map[level] || 'info'
}

function stagePerfTagType(perf) {
  const map = {
    'excellent': 'success',
    'good': 'primary',
    'average': 'warning',
    'needs_improvement': 'danger'
  }
  return map[perf] || 'info'
}

function rhythmTagType(rhythm) {
  const map = {
    'stable': 'success',
    'mostly_stable': 'primary',
    'unstable': 'danger'
  }
  return map[rhythm] || 'info'
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  return dateStr.substring(0, 16).replace('T', ' ')
}

function openItemDetail(item) {
  currentItem.value = item
  itemDetailVisible.value = true
  itemDetailTab.value = 'basic'
}

function openConclusionDialog(item) {
  const existing = item.conclusions?.[0]
  editingConclusion.value = existing
  Object.assign(conclusionForm, {
    review_item: item.id,
    stage_performance: existing?.stage_performance || 'good',
    rhythm_stability: existing?.rhythm_stability || 'mostly_stable',
    forgotten_lines: existing?.forgotten_lines || '',
    beat_issues: existing?.beat_issues || '',
    accompaniment_cohesion: existing?.accompaniment_cohesion || '',
    overall_comment: existing?.overall_comment || '',
    improvement_suggestions: existing?.improvement_suggestions || ''
  })
  conclusionDialogVisible.value = true
}

async function submitConclusion() {
  try {
    if (editingConclusion.value) {
      await store.editReviewConclusion(editingConclusion.value.id, conclusionForm)
      ElMessage.success('更新成功')
    } else {
      await store.addReviewConclusion(conclusionForm)
      ElMessage.success('添加成功')
    }
    conclusionDialogVisible.value = false
    await loadReviewData()
    if (currentItem.value) {
      const updated = store.reviewItems.find(i => i.id === currentItem.value.id)
      if (updated) currentItem.value = updated
    }
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

function openTaskDialog(task = null) {
  editingTask.value = task
  if (task) {
    Object.assign(taskForm, {
      review: task.review,
      review_item: task.review_item,
      task_title: task.task_title,
      task_description: task.task_description,
      source_type: task.source_type,
      source_description: task.source_description,
      priority: task.priority,
      assignee_id: task.assignee,
      deadline: task.deadline || ''
    })
  } else {
    Object.assign(taskForm, {
      review: parseInt(route.params.id),
      review_item: null,
      task_title: '',
      task_description: '',
      source_type: 'performance_issue',
      source_description: '',
      priority: 'medium',
      assignee_id: null,
      deadline: ''
    })
  }
  taskDialogVisible.value = true
}

async function submitTask() {
  try {
    if (editingTask.value) {
      await store.editImprovementTask(editingTask.value.id, taskForm)
      ElMessage.success('更新成功')
    } else {
      await store.addImprovementTask(taskForm)
      ElMessage.success('创建成功')
    }
    taskDialogVisible.value = false
    await loadReviewData()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

function openConvertTaskDialog(item) {
  convertTaskForm.review_item_id = item.id
  convertTaskForm.task_title = `${item.aria_name} - 改进任务`
  convertTaskForm.source_description = ''
  convertTaskForm.task_description = ''
  convertTaskForm.priority = 'medium'
  convertTaskForm.assignee_id = null
  convertTaskForm.deadline = ''
  convertTaskDialogVisible.value = true
}

async function submitConvertTask() {
  try {
    await store.convertToImprovementTask(convertTaskForm)
    ElMessage.success('任务创建成功')
    convertTaskDialogVisible.value = false
    await loadReviewData()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

async function handleStartTask(task) {
  try {
    await store.startImprovementTaskById(task.id)
    ElMessage.success('已开始')
    await loadReviewData()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

async function handleCompleteTask(task) {
  try {
    const { value: note } = await ElMessageBox.prompt('请输入完成备注', '完成任务', {
      confirmButtonText: '确认完成',
      cancelButtonText: '取消',
      inputType: 'textarea',
      inputPlaceholder: '请输入完成情况说明...'
    })
    await store.completeImprovementTaskById(task.id, note)
    ElMessage.success('已完成')
    await loadReviewData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('操作失败')
    }
  }
}

function deleteTask(task) {
  ElMessageBox.confirm(`确定要删除任务"${task.task_title}"吗？`, '删除确认', { type: 'warning' })
    .then(async () => {
      await store.removeImprovementTask(task.id)
      ElMessage.success('删除成功')
      await loadReviewData()
    }).catch(() => {})
}

async function handleStartTeacherReview() {
  try {
    await store.startTeacherReviewById(parseInt(route.params.id))
    ElMessage.success('已开始老师复盘')
    await store.loadPerformanceReviews()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

async function handleStartMemberReview() {
  try {
    await store.startMemberReviewById(parseInt(route.params.id))
    ElMessage.success('已开始成员自评')
    await store.loadPerformanceReviews()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

async function handleCompleteReview() {
  ElMessageBox.confirm('确定要完成本次复盘吗？完成后将无法修改。', '完成确认', { type: 'warning' })
    .then(async () => {
      try {
        await store.completeReviewById(parseInt(route.params.id))
        ElMessage.success('复盘已完成')
        await store.loadPerformanceReviews()
      } catch (error) {
        ElMessage.error('操作失败')
      }
    }).catch(() => {})
}
</script>

<style lang="scss" scoped>
.review-header {
  .review-info-row {
    display: flex;
    gap: 24px;
    margin-bottom: 20px;
    
    .info-item {
      flex: 1;
    }
  }
  
  .review-stats {
    display: flex;
    gap: 20px;
    padding: 16px;
    background: linear-gradient(135deg, rgba(196, 30, 58, 0.05), rgba(212, 175, 55, 0.05));
    border-radius: 10px;
    
    .stat-item {
      flex: 1;
      text-align: center;
      
      .stat-value {
        font-size: 28px;
        font-weight: bold;
        color: #C41E3A;
      }
      
      .stat-label {
        font-size: 13px;
        color: #666;
        margin-top: 4px;
      }
    }
  }
}

.performance-note {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px dashed #E8DCC8;
}

.review-tabs {
  :deep(.el-tabs__item.is-active) {
    color: #C41E3A !important;
  }
  
  :deep(.el-tabs__active-bar) {
    background-color: #D4AF37 !important;
  }
}

.tab-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.assignment-tags {
  display: flex;
  flex-wrap: wrap;
}

.item-detail-dialog {
  max-height: 600px;
  overflow-y: auto;
}

.detail-section {
  h4 {
    font-size: 16px;
    font-weight: 600;
    color: #C41E3A;
    margin-bottom: 12px;
    padding-left: 10px;
    border-left: 3px solid #D4AF37;
  }
}

.info-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  
  .info-item {
    flex: 1;
    min-width: 150px;
    
    &.full-width {
      flex: 1 1 100%;
    }
  }
}

.assignment-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  
  .assignment-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 12px;
    background: rgba(196, 30, 58, 0.05);
    border-radius: 6px;
    
    .role-name {
      color: #666;
      font-size: 13px;
    }
  }
}

.feedback-item {
  padding: 12px;
  background: rgba(212, 175, 55, 0.05);
  border-radius: 8px;
  margin-bottom: 12px;
  
  .feedback-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 8px;
    font-size: 13px;
    color: #666;
    
    .feedback-date {
      font-weight: 500;
      color: #C41E3A;
    }
  }
  
  .feedback-item-row {
    margin-top: 4px;
    font-size: 14px;
    
    .label {
      color: #666;
    }
  }
}

.conclusion-card {
  padding: 16px;
  background: linear-gradient(135deg, rgba(196, 30, 58, 0.03), rgba(212, 175, 55, 0.03));
  border-radius: 10px;
  border: 1px solid rgba(212, 175, 55, 0.2);
  margin-bottom: 12px;
  
  .conclusion-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px dashed #E8DCC8;
    
    .conclusion-teacher {
      font-weight: 600;
      color: #C41E3A;
    }
    
    .conclusion-date {
      color: #999;
      font-size: 13px;
    }
  }
  
  .conclusion-grid {
    display: flex;
    gap: 20px;
    margin-bottom: 12px;
    
    .conclusion-item {
      flex: 1;
    }
  }
  
  .conclusion-row {
    margin-bottom: 8px;
    
    .detail-value.highlight {
      color: #C41E3A;
      font-weight: 500;
    }
  }
}

.self-review-card {
  padding: 16px;
  background: rgba(46, 125, 50, 0.05);
  border-radius: 10px;
  margin-bottom: 12px;
  
  .self-review-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px dashed #E8DCC8;
    
    .self-review-member {
      font-weight: 600;
      color: #2E7D32;
    }
  }
  
  .self-review-row {
    margin-bottom: 8px;
    
    .detail-value.highlight {
      color: #2E7D32;
      font-weight: 500;
    }
  }
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #999;
  
  .el-icon {
    font-size: 48px;
    color: #D4AF37;
    margin-bottom: 12px;
    opacity: 0.5;
  }
  
  p {
    margin-bottom: 16px;
  }
}

.header-actions {
  display: flex;
  gap: 10px;
}
</style>
