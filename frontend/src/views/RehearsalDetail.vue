<template>
  <div class="page-container">
    <div class="page-header">
      <h2>
        <el-button link @click="router.back()">
          <el-icon><ArrowLeft /></el-icon>
        </el-button>
        排练详情
      </h2>
      <el-button type="primary" @click="openFeedbackDialog">
        <el-icon><Plus /></el-icon>
        添加反馈
      </el-button>
    </div>

    <div v-if="rehearsal" class="rehearsal-detail">
      <div class="opera-card">
        <div class="rehearsal-info">
          <div class="info-row">
            <div class="info-item">
              <div class="detail-label">节目</div>
              <div class="detail-value">{{ getProgramName(rehearsal.program) }}</div>
            </div>
            <div class="info-item">
              <div class="detail-label">日期</div>
              <div class="detail-value">{{ rehearsal.date }}</div>
            </div>
            <div class="info-item">
              <div class="detail-label">地点</div>
              <div class="detail-value">{{ rehearsal.location }}</div>
            </div>
            <div class="info-item">
              <div class="detail-label">反馈数</div>
              <div class="detail-value">
                <el-tag type="info">{{ rehearsalFeedbacks.length }}</el-tag>
              </div>
            </div>
          </div>
          <div class="info-row">
            <div class="info-item full-width">
              <div class="detail-label">备注</div>
              <div class="detail-value">{{ rehearsal.notes || '暂无备注' }}</div>
            </div>
          </div>
        </div>
      </div>

      <div class="opera-card">
        <h3 class="section-title">反馈列表</h3>
        <div v-if="rehearsalFeedbacks.length === 0" class="empty-state">
          <el-icon><ChatDotRound /></el-icon>
          <p>暂无反馈记录</p>
        </div>
        <div v-else class="feedback-list">
          <div v-for="feedback in rehearsalFeedbacks" :key="feedback.id" class="feedback-card">
            <div class="feedback-header">
              <div class="feedback-aria">
                <el-icon><VideoPlay /></el-icon>
                <span class="aria-name">{{ getAriaName(feedback.aria) }}</span>
              </div>
              <div class="feedback-member">
                <div class="member-avatar small">
                  {{ getMemberName(feedback.member).charAt(0) }}
                </div>
                <span>{{ getMemberName(feedback.member) }}</span>
              </div>
            </div>
            
            <div class="feedback-content">
              <div class="feedback-section">
                <div class="feedback-label">
                  <el-icon><Microphone /></el-icon>
                  录音
                </div>
                <div class="feedback-value audio-player">
                  <el-button size="small" :icon="VideoPlay" @click="playAudio(feedback.audio_url)">
                    播放录音
                  </el-button>
                </div>
              </div>
              
              <div class="feedback-section">
                <div class="feedback-label">
                  <el-icon><Warning /></el-icon>
                  起板问题
                </div>
                <div class="feedback-value">{{ feedback.start_beat_issue || '无' }}</div>
              </div>
              
              <div class="feedback-section">
                <div class="feedback-label">
                  <el-icon><Document /></el-icon>
                  忘词片段
                </div>
                <div class="feedback-value">{{ feedback.forgotten_lines || '无' }}</div>
              </div>
              
              <div class="feedback-section">
                <div class="feedback-label">
                  <el-icon><ChatDotRound /></el-icon>
                  老师点评
                </div>
                <div class="feedback-value comments">{{ feedback.teacher_comments || '暂无' }}</div>
              </div>
            </div>

            <div class="feedback-actions">
              <el-button type="primary" link size="small" @click="openEditFeedbackDialog(feedback)">编辑</el-button>
              <el-button type="danger" link size="small" @click="deleteFeedback(feedback)">删除</el-button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <el-dialog v-model="feedbackDialogVisible" :title="editingFeedback ? '编辑反馈' : '添加反馈'" width="600px">
      <el-form :model="feedbackForm" label-width="100px" ref="feedbackFormRef">
        <el-form-item label="唱段" prop="aria" :rules="[{ required: true }]">
          <el-select v-model="feedbackForm.aria" style="width: 100%">
            <el-option 
              v-for="a in programArias" 
              :key="a.id" 
              :label="a.name" 
              :value="a.id" 
            />
          </el-select>
        </el-form-item>
        <el-form-item label="成员" prop="member" :rules="[{ required: true }]">
          <el-select v-model="feedbackForm.member" style="width: 100%">
            <el-option 
              v-for="m in assignedMembers" 
              :key="m.id" 
              :label="m.name" 
              :value="m.id" 
            />
          </el-select>
        </el-form-item>
        <el-form-item label="录音文件" prop="audio_url">
          <el-upload
            action="#"
            :auto-upload="false"
            accept="audio/*"
            @change="handleAudioUpload"
          >
            <el-button :icon="Upload">选择录音</el-button>
            <template #tip>
              <div class="el-upload__tip">支持mp3、wav等音频格式</div>
            </template>
          </el-upload>
          <div v-if="feedbackForm.audio_url" class="file-name">{{ feedbackForm.audio_url }}</div>
        </el-form-item>
        <el-form-item label="起板问题" prop="start_beat_issue">
          <el-input 
            v-model="feedbackForm.start_beat_issue" 
            type="textarea" 
            :rows="2"
            placeholder="请描述起板问题" 
          />
        </el-form-item>
        <el-form-item label="忘词片段" prop="forgotten_lines">
          <el-input 
            v-model="feedbackForm.forgotten_lines" 
            type="textarea" 
            :rows="2"
            placeholder="请描述忘词的片段" 
          />
        </el-form-item>
        <el-form-item label="老师点评" prop="teacher_comments" :rules="[{ required: true }]">
          <el-input 
            v-model="feedbackForm.teacher_comments" 
            type="textarea" 
            :rows="4"
            placeholder="请输入老师的点评意见" 
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="feedbackDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitFeedback">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useOperaStore } from '@/stores/opera'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowLeft, Plus, VideoPlay, Microphone, Warning, Document, ChatDotRound, Upload } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const store = useOperaStore()

const feedbackDialogVisible = ref(false)
const editingFeedback = ref(null)
const feedbackFormRef = ref(null)

const rehearsal = computed(() => store.getRehearsalById(route.params.id))
const rehearsalFeedbacks = computed(() => store.feedbacks.filter(f => f.rehearsal === parseInt(route.params.id)))
const programArias = computed(() => {
  if (!rehearsal.value) return []
  return store.arias.filter(a => a.program === rehearsal.value.program)
})
const assignedMembers = computed(() => {
  if (!programArias.value.length) return store.members
  const ariaIds = programArias.value.map(a => a.id)
  const assignedMemberIds = [...new Set(store.assignments.filter(a => ariaIds.includes(a.aria)).map(a => a.member))]
  return store.members.filter(m => assignedMemberIds.includes(m.id))
})

const feedbackForm = reactive({
  aria: null,
  member: null,
  audio_url: '',
  start_beat_issue: '',
  forgotten_lines: '',
  teacher_comments: ''
})

onMounted(async () => {
  await Promise.all([
    store.loadPrograms(),
    store.loadRehearsals(),
    store.loadFeedbacks(),
    store.loadArias(),
    store.loadMembers(),
    store.loadAssignments()
  ])
})

function getProgramName(programId) {
  const program = store.programs.find(p => p.id === programId)
  return program ? program.name : '未知节目'
}

function getAriaName(ariaId) {
  const aria = store.arias.find(a => a.id === ariaId)
  return aria ? aria.name : '未知唱段'
}

function getMemberName(memberId) {
  const member = store.members.find(m => m.id === memberId)
  return member ? member.name : '未知成员'
}

function playAudio(url) {
  ElMessage.info('播放录音：' + url)
}

function openFeedbackDialog() {
  editingFeedback.value = null
  Object.assign(feedbackForm, {
    aria: null,
    member: null,
    audio_url: '',
    start_beat_issue: '',
    forgotten_lines: '',
    teacher_comments: ''
  })
  feedbackDialogVisible.value = true
}

function openEditFeedbackDialog(feedback) {
  editingFeedback.value = feedback
  Object.assign(feedbackForm, { ...feedback })
  feedbackDialogVisible.value = true
}

function handleAudioUpload(file) {
  feedbackForm.audio_url = '/mock/' + file.name
}

async function submitFeedback() {
  try {
    await feedbackFormRef.value.validate()
    const data = { ...feedbackForm, rehearsal: parseInt(route.params.id) }
    if (editingFeedback.value) {
      await store.editFeedback(editingFeedback.value.id, data)
      ElMessage.success('反馈更新成功')
    } else {
      await store.addFeedback(data)
      ElMessage.success('反馈添加成功')
    }
    feedbackDialogVisible.value = false
  } catch (error) {
    if (error !== false) {
      ElMessage.error('操作失败')
    }
  }
}

function deleteFeedback(feedback) {
  ElMessageBox.confirm(`确定要删除该反馈吗？`, '删除确认', { type: 'warning' })
    .then(async () => {
      await store.removeFeedback(feedback.id)
      ElMessage.success('删除成功')
    }).catch(() => {})
}
</script>

<style lang="scss" scoped>
.rehearsal-info {
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

.feedback-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.feedback-card {
  background: #FDF6E3;
  border-radius: 12px;
  padding: 20px;
  border: 1px solid #E8DCC8;
  position: relative;
}

.feedback-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #E8DCC8;
}

.feedback-aria {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #C41E3A;
  font-weight: 600;
  font-size: 16px;
}

.feedback-member {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #333;
}

.member-avatar {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #C41E3A, #8B0000);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 14px;
  
  &.small {
    width: 32px;
    height: 32px;
  }
}

.feedback-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.feedback-section {
  display: flex;
  gap: 12px;
  
  .feedback-label {
    display: flex;
    align-items: flex-start;
    gap: 6px;
    width: 100px;
    flex-shrink: 0;
    color: #666;
    font-size: 14px;
    
    .el-icon {
      color: #D4AF37;
      margin-top: 2px;
    }
  }
  
  .feedback-value {
    flex: 1;
    color: #333;
    font-size: 14px;
    
    &.comments {
      background: white;
      padding: 12px;
      border-radius: 6px;
      border-left: 3px solid #D4AF37;
    }
  }
}

.audio-player {
  .el-button {
    background: linear-gradient(135deg, #D4AF37, #B8860B);
    border: none;
    color: white;
    
    &:hover {
      opacity: 0.9;
    }
  }
}

.feedback-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 16px;
  padding-top: 12px;
  border-top: 1px solid #E8DCC8;
}

.file-name {
  margin-top: 8px;
  font-size: 13px;
  color: #666;
}
</style>
