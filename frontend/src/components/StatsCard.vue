<template>
  <div class="stats-card">
    <div class="icon-wrapper" :style="{ background: bgColor }">
      <el-icon :size="28"><component :is="icon" /></el-icon>
    </div>
    <div class="stats-content">
      <div class="stats-value">{{ value }}</div>
      <div class="stats-label">{{ label }}</div>
    </div>
    <div class="decoration-corner top-left"></div>
    <div class="decoration-corner top-right"></div>
    <div class="decoration-corner bottom-left"></div>
    <div class="decoration-corner bottom-right"></div>
  </div>
</template>

<script setup>
defineProps({
  icon: {
    type: Object,
    required: true
  },
  label: {
    type: String,
    required: true
  },
  value: {
    type: [String, Number],
    required: true
  },
  bgColor: {
    type: String,
    default: 'linear-gradient(135deg, #C41E3A, #8B0000)'
  }
})
</script>

<style lang="scss" scoped>
.stats-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 20px;
  box-shadow: 0 4px 12px rgba(196, 30, 58, 0.08);
  border: 1px solid #E8DCC8;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(196, 30, 58, 0.15);
  }
}

.icon-wrapper {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  flex-shrink: 0;
}

.stats-content {
  flex: 1;
}

.stats-value {
  font-size: 32px;
  font-weight: bold;
  color: #C41E3A;
  line-height: 1.2;
}

.stats-label {
  font-size: 14px;
  color: #666;
  margin-top: 4px;
}

.decoration-corner {
  position: absolute;
  width: 16px;
  height: 16px;
  border: 2px solid #D4AF37;
  
  &.top-left {
    top: 8px;
    left: 8px;
    border-right: none;
    border-bottom: none;
    border-radius: 4px 0 0 0;
  }
  
  &.top-right {
    top: 8px;
    right: 8px;
    border-left: none;
    border-bottom: none;
    border-radius: 0 4px 0 0;
  }
  
  &.bottom-left {
    bottom: 8px;
    left: 8px;
    border-right: none;
    border-top: none;
    border-radius: 0 0 0 4px;
  }
  
  &.bottom-right {
    bottom: 8px;
    right: 8px;
    border-left: none;
    border-top: none;
    border-radius: 0 0 4px 0;
  }
}
</style>
