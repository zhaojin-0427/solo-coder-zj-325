<template>
  <div class="home-page">
    <div class="hero-section chinese-pattern">
      <div class="hero-content">
        <div class="hero-text">
          <h2 class="hero-title">
            <span class="title-line">传承戏曲艺术</span>
            <span class="title-line">弘扬民族文化</span>
          </h2>
          <p class="hero-subtitle">社区戏曲票友唱段分配与排练反馈平台</p>
          <div class="hero-buttons">
            <router-link to="/programs" class="btn-primary hero-btn">
              <el-icon><VideoPlay /></el-icon>
              浏览节目
            </router-link>
            <router-link to="/assignments" class="btn-secondary hero-btn">
              <el-icon><UserFilled /></el-icon>
              查看分配
            </router-link>
          </div>
        </div>
        <div class="hero-decoration">
          <div class="opera-mask">
            <svg viewBox="0 0 200 300" class="mask-svg">
              <ellipse cx="100" cy="150" rx="80" ry="120" fill="#C41E3A" opacity="0.1"/>
              <ellipse cx="100" cy="150" rx="70" ry="110" fill="none" stroke="#D4AF37" stroke-width="2" opacity="0.3"/>
              <path d="M60 120 Q70 110 80 120" stroke="#C41E3A" stroke-width="3" fill="none"/>
              <path d="M120 120 Q130 110 140 120" stroke="#C41E3A" stroke-width="3" fill="none"/>
              <path d="M80 170 Q100 190 120 170" stroke="#C41E3A" stroke-width="3" fill="none"/>
              <text x="100" y="260" text-anchor="middle" fill="#D4AF37" font-size="24" font-family="serif">韵</text>
            </svg>
          </div>
        </div>
      </div>
    </div>

    <div class="page-container">
      <div class="stats-grid">
        <StatsCard 
          :icon="Grid" 
          label="节目总数" 
          :value="store.programs.length" 
          bgColor="linear-gradient(135deg, #C41E3A, #8B0000)"
        />
        <StatsCard 
          :icon="UserFilled" 
          label="成员总数" 
          :value="store.members.length" 
          bgColor="linear-gradient(135deg, #D4AF37, #B8860B)"
        />
        <StatsCard 
          :icon="VideoPlay" 
          label="唱段总数" 
          :value="store.arias.length" 
          bgColor="linear-gradient(135deg, #2E7D32, #1B5E20)"
        />
        <StatsCard 
          :icon="Calendar" 
          label="排练次数" 
          :value="store.rehearsals.length" 
          bgColor="linear-gradient(135deg, #FF9800, #F57C00)"
        />
      </div>

      <div class="content-grid">
        <div class="opera-card">
          <h3 class="section-title">热门节目</h3>
          <div class="program-list">
            <router-link 
              v-for="program in store.activePrograms.slice(0, 4)" 
              :key="program.id"
              :to="`/programs/${program.id}`"
              class="program-item"
            >
              <div class="program-icon">
                <el-icon :size="24"><Film /></el-icon>
              </div>
              <div class="program-info">
                <div class="program-name">{{ program.name }}</div>
                <div class="program-meta">
                  <span class="tag active">{{ program.type_display || program.type }}</span>
                  <span class="duration">{{ program.duration }}分钟</span>
                </div>
              </div>
              <el-icon class="arrow-icon"><ArrowRight /></el-icon>
            </router-link>
          </div>
        </div>

        <div class="opera-card">
          <h3 class="section-title">近期排练</h3>
          <div class="rehearsal-list">
            <div v-if="store.rehearsals.length === 0" class="empty-state">
              <el-icon><Calendar /></el-icon>
              <p>暂无排练记录</p>
            </div>
            <router-link 
              v-for="rehearsal in recentRehearsals" 
              :key="rehearsal.id"
              :to="`/rehearsals/${rehearsal.id}`"
              class="rehearsal-item"
            >
              <div class="rehearsal-date">
                <div class="date-day">{{ getDay(rehearsal.date) }}</div>
                <div class="date-month">{{ getMonth(rehearsal.date) }}</div>
              </div>
              <div class="rehearsal-info">
                <div class="rehearsal-program">{{ getProgramName(rehearsal.program) }}</div>
                <div class="rehearsal-location">
                  <el-icon :size="14"><Location /></el-icon>
                  {{ rehearsal.location }}
                </div>
              </div>
            </router-link>
          </div>
        </div>
      </div>

      <div class="opera-card">
        <h3 class="section-title">待处理替补申请</h3>
        <div v-if="store.pendingUnderstudy.length === 0" class="empty-state">
          <el-icon><CircleCheck /></el-icon>
          <p>暂无待处理的替补申请</p>
        </div>
        <div v-else class="understudy-list">
          <div 
            v-for="item in store.pendingUnderstudy" 
            :key="item.id"
            class="understudy-item"
          >
            <div class="understudy-info">
              <el-icon class="warning-icon" :size="20"><Warning /></el-icon>
              <div>
                <p class="understudy-text">
                  <strong>{{ getMemberName(item.substitute_member) }}</strong> 申请替代 
                  <strong>{{ getOriginalMember(item.original_assignment) }}</strong>
                </p>
                <p class="understudy-reason">原因：{{ item.reason }}</p>
              </div>
            </div>
            <div class="understudy-actions">
              <span class="tag pending">待处理</span>
              <router-link to="/understudy" class="action-link">去处理</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import { useOperaStore } from '@/stores/opera'
import StatsCard from '@/components/StatsCard.vue'
import { 
  Grid, UserFilled, VideoPlay, Calendar, Film, 
  ArrowRight, Location, Warning, CircleCheck 
} from '@element-plus/icons-vue'

const store = useOperaStore()

const recentRehearsals = computed(() => {
  return [...store.rehearsals]
    .sort((a, b) => new Date(b.date) - new Date(a.date))
    .slice(0, 4)
})

onMounted(async () => {
  await Promise.all([
    store.loadPrograms(),
    store.loadMembers(),
    store.loadArias(),
    store.loadRehearsals(),
    store.loadUnderstudyChanges()
  ])
})

function getProgramName(programId) {
  const program = store.programs.find(p => p.id === programId)
  return program ? program.name : '未知节目'
}

function getMemberName(memberId) {
  const member = store.members.find(m => m.id === memberId)
  return member ? member.name : '未知成员'
}

function getOriginalMember(assignmentId) {
  const assignment = store.assignments.find(a => a.id === assignmentId)
  if (assignment) {
    return getMemberName(assignment.member)
  }
  return '未知成员'
}

function getDay(dateStr) {
  return new Date(dateStr).getDate()
}

function getMonth(dateStr) {
  const months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
  return months[new Date(dateStr).getMonth()]
}
</script>

<style lang="scss" scoped>
.home-page {
  min-height: calc(100vh - 80px);
}

.hero-section {
  background: linear-gradient(135deg, #C41E3A 0%, #8B0000 50%, #C41E3A 100%);
  padding: 60px 24px;
  color: white;
  position: relative;
  overflow: hidden;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ccircle cx='50' cy='50' r='40' fill='none' stroke='%23FFD700' stroke-width='0.5' opacity='0.1'/%3E%3C/svg%3E") repeat;
    background-size: 200px 200px;
  }
}

.hero-content {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  z-index: 1;
}

.hero-text {
  flex: 1;
}

.hero-title {
  font-size: 48px;
  font-weight: bold;
  margin: 0 0 16px 0;
  line-height: 1.3;
  
  .title-line {
    display: block;
    text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.3);
  }
  
  .title-line:first-child {
    color: #FFD700;
  }
}

.hero-subtitle {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.9);
  margin: 0 0 32px 0;
  letter-spacing: 2px;
}

.hero-buttons {
  display: flex;
  gap: 16px;
}

.hero-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 14px 32px;
  font-size: 16px;
  text-decoration: none;
}

.hero-decoration {
  flex-shrink: 0;
  margin-left: 40px;
}

.opera-mask {
  width: 250px;
  height: 350px;
  animation: float 3s ease-in-out infinite;
  
  .mask-svg {
    width: 100%;
    height: 100%;
    filter: drop-shadow(0 10px 30px rgba(0, 0, 0, 0.3));
  }
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
  margin-top: -40px;
  position: relative;
  z-index: 10;
}

.content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.program-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.program-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: #FDF6E3;
  border-radius: 8px;
  text-decoration: none;
  color: inherit;
  transition: all 0.3s ease;
  border: 1px solid transparent;
  
  &:hover {
    background: #F5E6D3;
    border-color: #D4AF37;
    transform: translateX(4px);
  }
}

.program-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #C41E3A, #8B0000);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.program-info {
  flex: 1;
}

.program-name {
  font-weight: 600;
  color: #C41E3A;
  font-size: 16px;
  margin-bottom: 4px;
}

.program-meta {
  display: flex;
  align-items: center;
  gap: 12px;
}

.duration {
  font-size: 13px;
  color: #666;
}

.arrow-icon {
  color: #D4AF37;
  font-size: 20px;
}

.rehearsal-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.rehearsal-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: #FDF6E3;
  border-radius: 8px;
  text-decoration: none;
  color: inherit;
  transition: all 0.3s ease;
  border: 1px solid transparent;
  
  &:hover {
    background: #F5E6D3;
    border-color: #D4AF37;
    transform: translateX(4px);
  }
}

.rehearsal-date {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #D4AF37, #B8860B);
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
  
  .date-day {
    font-size: 24px;
    font-weight: bold;
    line-height: 1;
  }
  
  .date-month {
    font-size: 12px;
  }
}

.rehearsal-info {
  flex: 1;
}

.rehearsal-program {
  font-weight: 600;
  color: #C41E3A;
  font-size: 16px;
  margin-bottom: 4px;
}

.rehearsal-location {
  font-size: 13px;
  color: #666;
  display: flex;
  align-items: center;
  gap: 4px;
}

.understudy-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.understudy-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  background: linear-gradient(to right, rgba(255, 152, 0, 0.05), transparent);
  border-radius: 8px;
  border-left: 4px solid #FF9800;
}

.understudy-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.warning-icon {
  color: #FF9800;
}

.understudy-text {
  margin: 0 0 4px 0;
  color: #333;
  
  strong {
    color: #C41E3A;
  }
}

.understudy-reason {
  margin: 0;
  font-size: 13px;
  color: #666;
}

.understudy-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.action-link {
  color: #C41E3A;
  text-decoration: none;
  font-size: 14px;
  
  &:hover {
    text-decoration: underline;
  }
}

@media (max-width: 768px) {
  .hero-content {
    flex-direction: column;
    text-align: center;
  }
  
  .hero-title {
    font-size: 32px;
  }
  
  .hero-decoration {
    margin: 30px 0 0 0;
  }
  
  .opera-mask {
    width: 180px;
    height: 250px;
  }
  
  .content-grid {
    grid-template-columns: 1fr;
  }
  
  .hero-buttons {
    justify-content: center;
  }
}
</style>
