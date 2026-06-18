<template>
  <div class="main-layout">
    <OperaHeader />
    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    <footer class="main-footer">
      <div class="footer-content">
        <p>© 2024 社区戏曲票友平台 · 传承国粹 · 弘扬经典</p>
        <div class="footer-decoration">
          <span class="pattern">♪</span>
          <span class="pattern">♫</span>
          <span class="pattern">♬</span>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import OperaHeader from '@/components/OperaHeader.vue'
</script>

<style lang="scss" scoped>
.main-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  padding: 0;
}

.main-footer {
  background: linear-gradient(135deg, #8B0000 0%, #C41E3A 100%);
  color: rgba(255, 255, 255, 0.9);
  padding: 20px 24px;
  text-align: center;
  margin-top: 40px;
  
  .footer-content {
    max-width: 1400px;
    margin: 0 auto;
  }
  
  p {
    margin: 0;
    font-size: 14px;
    letter-spacing: 1px;
  }
  
  .footer-decoration {
    margin-top: 8px;
    
    .pattern {
      color: #FFD700;
      font-size: 16px;
      margin: 0 8px;
      opacity: 0.7;
    }
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
