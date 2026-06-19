<template>
  <header class="opera-header">
    <div class="header-content">
      <div class="logo-section">
        <div class="logo">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" class="logo-icon">
            <circle cx="50" cy="50" r="45" fill="#C41E3A"/>
            <circle cx="50" cy="50" r="38" fill="none" stroke="#FFD700" stroke-width="2"/>
            <text x="50" y="62" text-anchor="middle" fill="#FFD700" font-size="36" font-family="serif" font-weight="bold">戏</text>
          </svg>
        </div>
        <div class="logo-text">
          <h1>社区戏曲票友平台</h1>
          <p>唱段分配 · 排练反馈 · 传承经典</p>
        </div>
      </div>
      <nav class="nav-menu">
        <router-link 
          v-for="item in menuItems" 
          :key="item.path" 
          :to="item.path"
          class="nav-item"
          :class="{ active: isActive(item.path) }"
        >
          <el-icon><component :is="item.icon" /></el-icon>
          <span>{{ item.label }}</span>
        </router-link>
      </nav>
    </div>
    <div class="header-decoration"></div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import {
  HomeFilled,
  Grid,
  User,
  Calendar,
  Switch,
  CircleCheck,
  DataAnalysis
} from '@element-plus/icons-vue'

const route = useRoute()

const menuItems = [
  { path: '/', label: '首页', icon: HomeFilled },
  { path: '/programs', label: '节目档案', icon: Grid },
  { path: '/assignments', label: '唱段分配', icon: User },
  { path: '/rehearsals', label: '排练记录', icon: Calendar },
  { path: '/understudy', label: '替补调整', icon: Switch },
  { path: '/rehearsal-checks', label: '联排确认', icon: CircleCheck },
  { path: '/statistics', label: '统计分析', icon: DataAnalysis }
]

function isActive(path) {
  if (path === '/') {
    return route.path === '/'
  }
  return route.path.startsWith(path)
}
</script>

<style lang="scss" scoped>
.opera-header {
  background: linear-gradient(135deg, #C41E3A 0%, #8B0000 100%);
  color: white;
  position: relative;
  box-shadow: 0 4px 20px rgba(196, 30, 58, 0.3);
  z-index: 100;
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 80px;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 16px;
}

.logo {
  width: 56px;
  height: 56px;
  animation: rotate 20s linear infinite;
  
  .logo-icon {
    width: 100%;
    height: 100%;
    filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
  }
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.logo-text {
  h1 {
    font-size: 22px;
    font-weight: bold;
    margin: 0;
    color: #FFD700;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    letter-spacing: 2px;
  }
  
  p {
    font-size: 12px;
    margin: 4px 0 0 0;
    color: rgba(255, 255, 255, 0.8);
    letter-spacing: 1px;
  }
}

.nav-menu {
  display: flex;
  gap: 8px;
  height: 100%;
  align-items: center;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  color: rgba(255, 255, 255, 0.85);
  text-decoration: none;
  border-radius: 6px;
  transition: all 0.3s ease;
  font-size: 14px;
  position: relative;
  
  &:hover {
    color: white;
    background: rgba(255, 255, 255, 0.1);
  }
  
  &.active {
    color: #FFD700;
    background: rgba(255, 215, 0, 0.15);
    
    &::after {
      content: '';
      position: absolute;
      bottom: -2px;
      left: 50%;
      transform: translateX(-50%);
      width: 30px;
      height: 3px;
      background: #FFD700;
      border-radius: 2px;
    }
  }
  
  .el-icon {
    font-size: 18px;
  }
}

.header-decoration {
  height: 4px;
  background: linear-gradient(to right, #FFD700, #D4AF37, #FFD700, #D4AF37, #FFD700);
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    height: auto;
    padding: 16px;
  }
  
  .logo-section {
    margin-bottom: 16px;
  }
  
  .nav-menu {
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .nav-item {
    padding: 6px 12px;
    font-size: 13px;
  }
}
</style>
