<template>
  <div class="page-container">
    <div class="page-header">
      <h2>统计分析</h2>
      <el-button type="primary" @click="refreshData">
        <el-icon><Refresh /></el-icon>
        刷新数据
      </el-button>
    </div>

    <div class="stats-grid">
      <StatsCard 
        :icon="Grid" 
        label="节目总数" 
        :value="store.programs.length" 
        bgColor="linear-gradient(135deg, #C41E3A, #8B0000)"
      />
      <StatsCard 
        :icon="VideoPlay" 
        label="唱段总数" 
        :value="store.arias.length" 
        bgColor="linear-gradient(135deg, #D4AF37, #B8860B)"
      />
      <StatsCard 
        :icon="UserFilled" 
        label="成员总数" 
        :value="store.members.length" 
        bgColor="linear-gradient(135deg, #2E7D32, #1B5E20)"
      />
      <StatsCard 
        :icon="Calendar" 
        label="排练总次数" 
        :value="store.rehearsals.length" 
        bgColor="linear-gradient(135deg, #FF9800, #F57C00)"
      />
    </div>

    <el-row :gutter="20">
      <el-col :span="12">
        <div class="opera-card">
          <h3 class="section-title">各节目排练次数</h3>
          <div class="chart-container">
            <v-chart class="chart" :option="rehearsalChartOption" autoresize />
          </div>
        </div>
      </el-col>

      <el-col :span="12">
        <div class="opera-card">
          <h3 class="section-title">替补发生频率</h3>
          <div class="chart-container">
            <v-chart class="chart" :option="understudyChartOption" autoresize />
          </div>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-col :span="12">
        <div class="opera-card">
          <h3 class="section-title">高频失误片段排行</h3>
          <div class="chart-container">
            <v-chart class="chart" :option="mistakeChartOption" autoresize />
          </div>
        </div>
      </el-col>

      <el-col :span="12">
        <div class="opera-card">
          <h3 class="section-title">成员参与活跃度</h3>
          <div class="chart-container">
            <div class="member-select">
              <el-select v-model="selectedMember" placeholder="选择成员" style="width: 200px" @change="updateRadarChart">
                <el-option 
                  v-for="m in memberOptions" 
                  :key="m.name" 
                  :label="m.name" 
                  :value="m.name" 
                />
              </el-select>
            </div>
            <v-chart class="chart" :option="activityChartOption" autoresize />
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useOperaStore } from '@/stores/opera'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, PieChart, RadarChart } from 'echarts/charts'
import { 
  GridComponent, TooltipComponent, LegendComponent, 
  TitleComponent, RadarComponent 
} from 'echarts/components'
import StatsCard from '@/components/StatsCard.vue'
import { Grid, UserFilled, VideoPlay, Calendar, Refresh } from '@element-plus/icons-vue'

use([
  CanvasRenderer,
  BarChart,
  PieChart,
  RadarChart,
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent,
  RadarComponent
])

const store = useOperaStore()
const selectedMember = ref('')

const memberOptions = computed(() => {
  if (!store.statistics) return []
  return store.statistics.member_activity.map(m => ({ name: m.name }))
})

const rehearsalChartOption = computed(() => {
  if (!store.statistics) return {}
  const data = store.statistics.program_rehearsal_counts
  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: data.map(d => d.program_name),
      axisLabel: {
        color: '#666',
        interval: 0,
        rotate: 0
      },
      axisLine: {
        lineStyle: { color: '#E8DCC8' }
      }
    },
    yAxis: {
      type: 'value',
      name: '次数',
      nameTextStyle: { color: '#666' },
      axisLabel: { color: '#666' },
      splitLine: {
        lineStyle: { color: '#E8DCC8', type: 'dashed' }
      }
    },
    series: [{
      name: '排练次数',
      type: 'bar',
      data: data.map(d => d.count),
      itemStyle: {
        color: {
          type: 'linear',
          x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: '#C41E3A' },
            { offset: 1, color: '#8B0000' }
          ]
        },
        borderRadius: [4, 4, 0, 0]
      },
      barWidth: '50%'
    }]
  }
})

const understudyChartOption = computed(() => {
  if (!store.statistics) return {}
  const data = store.statistics.understudy_frequency
  const colors = ['#C41E3A', '#D4AF37', '#2E7D32', '#FF9800', '#1976D2']
  return {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c}次 ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      textStyle: { color: '#666' }
    },
    series: [{
      name: '替补原因',
      type: 'pie',
      radius: ['40%', '70%'],
      center: ['60%', '50%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 8,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: false,
        position: 'center'
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 18,
          fontWeight: 'bold',
          color: '#C41E3A'
        }
      },
      labelLine: {
        show: false
      },
      data: data.map((d, i) => ({
        value: d.value,
        name: d.name,
        itemStyle: { color: colors[i % colors.length] }
      }))
    }]
  }
})

const mistakeChartOption = computed(() => {
  if (!store.statistics) return {}
  const data = [...store.statistics.frequent_error_arias].sort((a, b) => a.total - b.total)
  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      name: '失误次数',
      nameTextStyle: { color: '#666' },
      axisLabel: { color: '#666' },
      splitLine: {
        lineStyle: { color: '#E8DCC8', type: 'dashed' }
      }
    },
    yAxis: {
      type: 'category',
      data: data.map(d => d.aria_name),
      axisLabel: {
        color: '#666',
        fontSize: 12
      },
      axisLine: {
        lineStyle: { color: '#E8DCC8' }
      }
    },
    series: [{
      name: '失误次数',
      type: 'bar',
      data: data.map(d => d.total),
      itemStyle: {
        color: {
          type: 'linear',
          x: 0, y: 0, x2: 1, y2: 0,
          colorStops: [
            { offset: 0, color: '#D4AF37' },
            { offset: 1, color: '#C41E3A' }
          ]
        },
        borderRadius: [0, 4, 4, 0]
      },
      barWidth: '60%',
      label: {
        show: true,
        position: 'right',
        color: '#666'
      }
    }]
  }
})

const activityChartOption = computed(() => {
  if (!store.statistics) return {}
  const memberData = selectedMember.value 
    ? store.statistics.member_activity.find(m => m.name === selectedMember.value)
    : store.statistics.member_activity[0]
  
  if (!memberData) return {}
  
  const indicator = [
    { name: '排练次数', max: 10 },
    { name: '分配唱段', max: 5 },
    { name: '反馈数量', max: 5 },
    { name: '准时率', max: 100 },
    { name: '表现评分', max: 100 }
  ]
  
  const values = [
    memberData.feedback_count || 0,
    memberData.assignment_count || 0,
    memberData.feedback_count || 0,
    Math.min(100, (memberData.assignment_count || 0) * 20 + 50),
    Math.min(100, (memberData.feedback_count || 0) * 15 + 60)
  ]
  
  return {
    tooltip: {
      trigger: 'item'
    },
    radar: {
      indicator: indicator,
      center: ['50%', '55%'],
      radius: '65%',
      splitNumber: 4,
      axisName: {
        color: '#666',
        fontSize: 12
      },
      splitLine: {
        lineStyle: { color: '#E8DCC8' }
      },
      splitArea: {
        areaStyle: {
          color: ['rgba(212, 175, 55, 0.05)', 'rgba(196, 30, 58, 0.05)']
        }
      },
      axisLine: {
        lineStyle: { color: '#E8DCC8' }
      }
    },
    series: [{
      type: 'radar',
      data: [{
        value: values,
        name: memberData.name,
        symbol: 'circle',
        symbolSize: 8,
        lineStyle: {
          color: '#C41E3A',
          width: 2
        },
        areaStyle: {
          color: 'rgba(196, 30, 58, 0.2)'
        },
        itemStyle: {
          color: '#C41E3A',
          borderColor: '#fff',
          borderWidth: 2
        }
      }]
    }]
  }
})

function updateRadarChart() {
}

async function refreshData() {
  await store.loadStatistics()
}

onMounted(async () => {
  await Promise.all([
    store.loadPrograms(),
    store.loadArias(),
    store.loadMembers(),
    store.loadRehearsals(),
    store.loadStatistics()
  ])
  if (store.statistics && store.statistics.member_activity.length > 0) {
    selectedMember.value = store.statistics.member_activity[0].name
  }
})
</script>

<style lang="scss" scoped>
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.chart-container {
  position: relative;
}

.chart {
  height: 350px;
  width: 100%;
}

.member-select {
  position: absolute;
  top: 0;
  right: 0;
  z-index: 10;
}
</style>
