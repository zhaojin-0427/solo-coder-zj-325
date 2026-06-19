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

    <div class="stats-grid">
      <StatsCard 
        :icon="Warning" 
        label="风险总数" 
        :value="riskStats.total_risks" 
        bgColor="linear-gradient(135deg, #C41E3A, #8B0000)"
      />
      <StatsCard 
        :icon="Clock" 
        label="未解除风险" 
        :value="riskStats.unresolved_risks" 
        bgColor="linear-gradient(135deg, #FF9800, #F57C00)"
      />
      <StatsCard 
        :icon="CircleCheck" 
        label="风险解除率" 
        :value="riskStats.overall_resolution_rate + '%'" 
        bgColor="linear-gradient(135deg, #2E7D32, #1B5E20)"
      />
      <StatsCard 
        :icon="Timer" 
        label="平均处理时长" 
        :value="riskStats.avg_processing_hours !== null ? riskStats.avg_processing_hours + 'h' : '-'" 
        bgColor="linear-gradient(135deg, #1976D2, #0D47A1)"
      />
    </div>

    <div class="stats-grid">
      <StatsCard 
        :icon="DataAnalysis" 
        label="复盘批次总数" 
        :value="reviewStats.total_reviews" 
        bgColor="linear-gradient(135deg, #7B1FA2, #4A148C)"
      />
      <StatsCard 
        :icon="CircleCheck" 
        label="已完成复盘" 
        :value="reviewStats.completed_reviews" 
        bgColor="linear-gradient(135deg, #2E7D32, #1B5E20)"
      />
      <StatsCard 
        :icon="TrendCharts" 
        label="复盘完成率" 
        :value="reviewStats.overall_completion_rate + '%'" 
        bgColor="linear-gradient(135deg, #D4AF37, #B8860B)"
      />
      <StatsCard 
        :icon="List" 
        label="改进任务总数" 
        :value="reviewStats.total_improvement_tasks" 
        bgColor="linear-gradient(135deg, #009688, #004D40)"
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

    <el-row :gutter="20">
      <el-col :span="12">
        <div class="opera-card">
          <h3 class="section-title">各节目风险解除率</h3>
          <div class="chart-container">
            <v-chart class="chart" :option="resolutionRateChartOption" autoresize />
          </div>
        </div>
      </el-col>

      <el-col :span="12">
        <div class="opera-card">
          <h3 class="section-title">高频风险类型趋势（近30天）</h3>
          <div class="chart-container">
            <v-chart class="chart" :option="riskTypeTrendChartOption" autoresize />
          </div>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-col :span="24">
        <div class="opera-card">
          <h3 class="section-title">风险创建与解除趋势（近30天）</h3>
          <div class="chart-container">
            <v-chart class="chart" :option="dailyTrendChartOption" autoresize />
          </div>
        </div>
      </el-col>
    </el-row>

    <div class="opera-card">
      <h3 class="section-title">演出前风险统计</h3>
      <div class="risk-overview">
        <div class="risk-stat">
          <div class="risk-stat-value">{{ preRisk.open_check_count }}</div>
          <div class="risk-stat-label">进行中联排批次</div>
        </div>
        <div class="risk-stat">
          <div class="risk-stat-value">{{ preRisk.risk_aria_count }}</div>
          <div class="risk-stat-label">风险唱段数</div>
        </div>
        <div class="risk-stat">
          <div class="risk-stat-value">{{ preRisk.pending_risk_actions }}</div>
          <div class="risk-stat-label">待处理风险项</div>
        </div>
        <div class="risk-stat">
          <div class="risk-stat-value">{{ riskStats.unresolved_risks }}</div>
          <div class="risk-stat-label">未解除风险</div>
        </div>
        <div class="risk-stat-link" @click="goToRehearsalChecks">
          <el-icon><Right /></el-icon>
          <span>前往联排确认看板</span>
        </div>
      </div>

      <el-row :gutter="20" style="margin-top: 16px">
        <el-col :span="12">
          <h4 class="sub-title">风险标签分布</h4>
          <div class="chart-container">
            <v-chart class="chart small-chart" :option="riskFlagChartOption" autoresize />
          </div>
        </el-col>
        <el-col :span="12">
          <h4 class="sub-title">待处理项类型分布</h4>
          <div class="chart-container">
            <v-chart class="chart small-chart" :option="riskActionChartOption" autoresize />
          </div>
        </el-col>
      </el-row>

      <el-row :gutter="20" style="margin-top: 16px">
        <el-col :span="12">
          <h4 class="sub-title">解除来源分布</h4>
          <div class="chart-container">
            <v-chart class="chart small-chart" :option="resolutionSourceChartOption" autoresize />
          </div>
        </el-col>
        <el-col :span="12">
          <h4 class="sub-title">各节目平均处理时长</h4>
          <div class="chart-container">
            <v-chart class="chart small-chart" :option="avgProcessingTimeChartOption" autoresize />
          </div>
        </el-col>
      </el-row>

      <h4 class="sub-title" style="margin-top: 16px">各节目演出前风险</h4>
      <el-table :data="preRisk.program_risk" stripe size="small">
        <el-table-column prop="program_name" label="节目" min-width="160" />
        <el-table-column prop="open_check_count" label="进行中批次" width="120">
          <template #default="{ row }">
            <el-tag type="warning">{{ row.open_check_count }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="risk_aria_count" label="风险唱段数" width="120">
          <template #default="{ row }">
            <el-tag :type="row.risk_aria_count > 0 ? 'danger' : 'success'">{{ row.risk_aria_count }}</el-tag>
          </template>
        </el-table-column>
      </el-table>

      <h4 class="sub-title" style="margin-top: 24px">各节目风险处理统计</h4>
      <el-table :data="programRiskStats" stripe size="small">
        <el-table-column prop="program_name" label="节目" min-width="160" />
        <el-table-column prop="total_risks" label="风险总数" width="100">
          <template #default="{ row }">
            <el-tag type="info">{{ row.total_risks }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="resolved_risks" label="已解除" width="100">
          <template #default="{ row }">
            <el-tag type="success">{{ row.resolved_risks }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="unresolved_risks" label="未解除" width="100">
          <template #default="{ row }">
            <el-tag :type="row.unresolved_risks > 0 ? 'danger' : 'success'">{{ row.unresolved_risks }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="resolution_rate" label="解除率" width="120">
          <template #default="{ row }">
            <el-progress 
              :percentage="row.resolution_rate" 
              :stroke-width="12"
              :color="row.resolution_rate >= 80 ? '#2E7D32' : row.resolution_rate >= 50 ? '#FF9800' : '#C41E3A'"
            />
          </template>
        </el-table-column>
        <el-table-column prop="avg_processing_hours" label="平均处理时长" width="140">
          <template #default="{ row }">
            <span v-if="row.avg_processing_hours !== null">{{ row.avg_processing_hours }} 小时</span>
            <span v-else class="muted">-</span>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <div class="opera-card">
      <h3 class="section-title">演出复盘统计</h3>
      
      <el-row :gutter="20" style="margin-top: 16px">
        <el-col :span="12">
          <h4 class="sub-title">各节目复盘完成率</h4>
          <div class="chart-container">
            <v-chart class="chart small-chart" :option="reviewCompletionChartOption" autoresize />
          </div>
        </el-col>
        <el-col :span="12">
          <h4 class="sub-title">常见演出问题类型分布</h4>
          <div class="chart-container">
            <v-chart class="chart small-chart" :option="issueTypeChartOption" autoresize />
          </div>
        </el-col>
      </el-row>

      <el-row :gutter="20" style="margin-top: 16px">
        <el-col :span="12">
          <h4 class="sub-title">改进任务来源分布</h4>
          <div class="chart-container">
            <v-chart class="chart small-chart" :option="taskSourceChartOption" autoresize />
          </div>
        </el-col>
        <el-col :span="12">
          <h4 class="sub-title">成员改进任务完成率</h4>
          <div class="chart-container">
            <v-chart class="chart small-chart" :option="memberTaskChartOption" autoresize />
          </div>
        </el-col>
      </el-row>

      <el-row :gutter="20" style="margin-top: 16px">
        <el-col :span="12">
          <h4 class="sub-title">舞台表现分布</h4>
          <div class="chart-container">
            <v-chart class="chart small-chart" :option="stagePerformanceChartOption" autoresize />
          </div>
        </el-col>
        <el-col :span="12">
          <h4 class="sub-title">节奏稳定性分布</h4>
          <div class="chart-container">
            <v-chart class="chart small-chart" :option="rhythmStabilityChartOption" autoresize />
          </div>
        </el-col>
      </el-row>

      <h4 class="sub-title" style="margin-top: 24px">各节目演出复盘详情</h4>
      <el-table :data="programReviewStats" stripe size="small">
        <el-table-column prop="program_name" label="节目" min-width="160" />
        <el-table-column prop="total_reviews" label="复盘批次" width="100">
          <template #default="{ row }">
            <el-tag type="info">{{ row.total_reviews }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="completed_reviews" label="已完成" width="100">
          <template #default="{ row }">
            <el-tag type="success">{{ row.completed_reviews }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="completion_rate" label="复盘完成率" width="140">
          <template #default="{ row }">
            <el-progress 
              :percentage="row.completion_rate || 0" 
              :stroke-width="10"
              :color="(row.completion_rate || 0) >= 80 ? '#2E7D32' : (row.completion_rate || 0) >= 50 ? '#FF9800' : '#C41E3A'"
            />
          </template>
        </el-table-column>
        <el-table-column prop="total_tasks" label="改进任务数" width="120">
          <template #default="{ row }">
            <el-tag :type="row.total_tasks > 0 ? 'warning' : 'info'">{{ row.total_tasks }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="task_completion_rate" label="任务完成率" width="140">
          <template #default="{ row }">
            <el-progress 
              :percentage="row.task_completion_rate || 0" 
              :stroke-width="10"
              :color="(row.task_completion_rate || 0) >= 80 ? '#2E7D32' : (row.task_completion_rate || 0) >= 50 ? '#FF9800' : '#C41E3A'"
            />
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useOperaStore } from '@/stores/opera'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, PieChart, RadarChart, LineChart } from 'echarts/charts'
import {
  GridComponent, TooltipComponent, LegendComponent,
  TitleComponent, RadarComponent
} from 'echarts/components'
import StatsCard from '@/components/StatsCard.vue'
import { Grid, UserFilled, VideoPlay, Calendar, Refresh, Right, Warning, Clock, CircleCheck, Timer, DataAnalysis, TrendCharts, List } from '@element-plus/icons-vue'

use([
  CanvasRenderer,
  BarChart,
  PieChart,
  RadarChart,
  LineChart,
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent,
  RadarComponent
])

const store = useOperaStore()
const router = useRouter()
const selectedMember = ref('')

const preRisk = computed(() => store.statistics?.pre_performance_risk || {
  open_check_count: 0,
  risk_aria_count: 0,
  pending_risk_actions: 0,
  flag_breakdown: [],
  risk_action_breakdown: [],
  program_risk: []
})

const riskStats = computed(() => store.statistics?.risk_closure_stats || {
  total_risks: 0,
  unresolved_risks: 0,
  resolved_risks: 0,
  overall_resolution_rate: 0,
  avg_processing_hours: null,
  program_risk_stats: [],
  risk_type_trend: [],
  daily_risk_trend: [],
  resolution_source_breakdown: []
})

const programRiskStats = computed(() => riskStats.value.program_risk_stats || [])

const reviewStats = computed(() => store.statistics?.performance_review || {
  total_reviews: 0,
  completed_reviews: 0,
  overall_completion_rate: 0,
  total_improvement_tasks: 0,
  completed_tasks: 0,
  overall_task_completion_rate: 0,
  program_review_stats: [],
  issue_type_distribution: [],
  stage_performance_distribution: [],
  rhythm_stability_distribution: [],
  member_task_stats: [],
  task_source_breakdown: []
})

const programReviewStats = computed(() => reviewStats.value.program_review_stats || [])

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
        value: d.count,
        name: d.program_name,
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

const riskFlagChartOption = computed(() => {
  const data = preRisk.value.flag_breakdown
  const colors = {
    attendance: '#C41E3A',
    understudy: '#D4AF37',
    feedback: '#2E7D32',
    accompaniment: '#1976D2',
    teacher_risk: '#7B1FA2'
  }
  return {
    tooltip: { trigger: 'item', formatter: '{b}: {c}个' },
    legend: { bottom: 0, textStyle: { color: '#666' } },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      center: ['50%', '45%'],
      avoidLabelOverlap: false,
      itemStyle: { borderRadius: 8, borderColor: '#fff', borderWidth: 2 },
      label: { show: false, position: 'center' },
      labelLine: { show: false },
      data: data.map(d => ({
        value: d.count,
        name: d.label,
        itemStyle: { color: colors[d.action_type] || '#999' }
      }))
    }]
  }
})

const riskActionChartOption = computed(() => {
  const data = preRisk.value.risk_action_breakdown
  return {
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: {
      type: 'category',
      data: data.map(d => d.label),
      axisLabel: { color: '#666', interval: 0, rotate: 0 },
      axisLine: { lineStyle: { color: '#E8DCC8' } }
    },
    yAxis: {
      type: 'value',
      name: '数量',
      nameTextStyle: { color: '#666' },
      axisLabel: { color: '#666' },
      splitLine: { lineStyle: { color: '#E8DCC8', type: 'dashed' } }
    },
    series: [{
      name: '待处理项',
      type: 'bar',
      data: data.map(d => d.count),
      itemStyle: {
        color: {
          type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: '#FF9800' },
            { offset: 1, color: '#F57C00' }
          ]
        },
        borderRadius: [4, 4, 0, 0]
      },
      barWidth: '50%',
      label: { show: true, position: 'top', color: '#666' }
    }]
  }
})

const resolutionRateChartOption = computed(() => {
  const data = programRiskStats.value
  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      formatter: '{b}: {c}%'
    },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: {
      type: 'category',
      data: data.map(d => d.program_name),
      axisLabel: { color: '#666', interval: 0, rotate: 0 },
      axisLine: { lineStyle: { color: '#E8DCC8' } }
    },
    yAxis: {
      type: 'value',
      name: '解除率(%)',
      nameTextStyle: { color: '#666' },
      axisLabel: { color: '#666', formatter: '{value}%' },
      splitLine: { lineStyle: { color: '#E8DCC8', type: 'dashed' } },
      max: 100
    },
    series: [{
      name: '解除率',
      type: 'bar',
      data: data.map(d => ({
        value: d.resolution_rate,
        itemStyle: {
          color: d.resolution_rate >= 80 ? '#2E7D32' : d.resolution_rate >= 50 ? '#FF9800' : '#C41E3A',
          borderRadius: [4, 4, 0, 0]
        }
      })),
      barWidth: '50%',
      label: {
        show: true,
        position: 'top',
        color: '#666',
        formatter: '{c}%'
      }
    }]
  }
})

const riskTypeTrendChartOption = computed(() => {
  const data = riskStats.value.risk_type_trend || []
  const colors = {
    attendance: '#C41E3A',
    understudy: '#D4AF37',
    feedback: '#2E7D32',
    accompaniment: '#1976D2',
    teacher_risk: '#7B1FA2'
  }
  return {
    tooltip: { trigger: 'item', formatter: '{b}: {c}个' },
    legend: { bottom: 0, textStyle: { color: '#666' } },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      center: ['50%', '45%'],
      avoidLabelOverlap: false,
      itemStyle: { borderRadius: 8, borderColor: '#fff', borderWidth: 2 },
      label: { show: false, position: 'center' },
      labelLine: { show: false },
      data: data.map(d => ({
        value: d.count,
        name: d.label,
        itemStyle: { color: colors[d.action_type] || '#999' }
      }))
    }]
  }
})

const dailyTrendChartOption = computed(() => {
  const data = riskStats.value.daily_risk_trend || []
  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'cross' }
    },
    legend: {
      data: ['新增风险', '解除风险'],
      textStyle: { color: '#666' }
    },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: {
      type: 'category',
      data: data.map(d => d.date),
      axisLabel: { 
        color: '#666', 
        interval: 4,
        rotate: 45
      },
      axisLine: { lineStyle: { color: '#E8DCC8' } }
    },
    yAxis: {
      type: 'value',
      name: '数量',
      nameTextStyle: { color: '#666' },
      axisLabel: { color: '#666' },
      splitLine: { lineStyle: { color: '#E8DCC8', type: 'dashed' } }
    },
    series: [
      {
        name: '新增风险',
        type: 'line',
        data: data.map(d => d.created),
        smooth: true,
        lineStyle: { color: '#C41E3A', width: 2 },
        itemStyle: { color: '#C41E3A' },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(196, 30, 58, 0.3)' },
              { offset: 1, color: 'rgba(196, 30, 58, 0.05)' }
            ]
          }
        }
      },
      {
        name: '解除风险',
        type: 'line',
        data: data.map(d => d.resolved),
        smooth: true,
        lineStyle: { color: '#2E7D32', width: 2 },
        itemStyle: { color: '#2E7D32' },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(46, 125, 50, 0.3)' },
              { offset: 1, color: 'rgba(46, 125, 50, 0.05)' }
            ]
          }
        }
      }
    ]
  }
})

const resolutionSourceChartOption = computed(() => {
  const data = riskStats.value.resolution_source_breakdown || []
  const colors = ['#C41E3A', '#D4AF37', '#2E7D32', '#FF9800', '#1976D2', '#7B1FA2', '#009688', '#E91E63']
  return {
    tooltip: { trigger: 'item', formatter: '{b}: {c}个' },
    legend: { 
      orient: 'vertical',
      left: 'left',
      textStyle: { color: '#666' } 
    },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      center: ['65%', '50%'],
      avoidLabelOverlap: false,
      itemStyle: { borderRadius: 8, borderColor: '#fff', borderWidth: 2 },
      label: { show: false, position: 'center' },
      labelLine: { show: false },
      data: data.map((d, i) => ({
        value: d.count,
        name: d.label,
        itemStyle: { color: colors[i % colors.length] }
      }))
    }]
  }
})

const avgProcessingTimeChartOption = computed(() => {
  const data = programRiskStats.value.filter(d => d.avg_processing_hours !== null)
  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      formatter: '{b}: {c} 小时'
    },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: {
      type: 'category',
      data: data.map(d => d.program_name),
      axisLabel: { color: '#666', interval: 0, rotate: 0 },
      axisLine: { lineStyle: { color: '#E8DCC8' } }
    },
    yAxis: {
      type: 'value',
      name: '小时',
      nameTextStyle: { color: '#666' },
      axisLabel: { color: '#666' },
      splitLine: { lineStyle: { color: '#E8DCC8', type: 'dashed' } }
    },
    series: [{
      name: '平均处理时长',
      type: 'bar',
      data: data.map(d => d.avg_processing_hours),
      itemStyle: {
        color: {
          type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: '#1976D2' },
            { offset: 1, color: '#0D47A1' }
          ]
        },
        borderRadius: [4, 4, 0, 0]
      },
      barWidth: '50%',
      label: {
        show: true,
        position: 'top',
        color: '#666',
        formatter: '{c}h'
      }
    }]
  }
})

const reviewCompletionChartOption = computed(() => {
  const data = programReviewStats.value
  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      formatter: '{b}: {c}%'
    },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: {
      type: 'category',
      data: data.map(d => d.program_name),
      axisLabel: { color: '#666', interval: 0, rotate: 0 },
      axisLine: { lineStyle: { color: '#E8DCC8' } }
    },
    yAxis: {
      type: 'value',
      name: '完成率(%)',
      nameTextStyle: { color: '#666' },
      axisLabel: { color: '#666', formatter: '{value}%' },
      splitLine: { lineStyle: { color: '#E8DCC8', type: 'dashed' } },
      max: 100
    },
    series: [{
      name: '复盘完成率',
      type: 'bar',
      data: data.map(d => ({
        value: d.completion_rate || 0,
        itemStyle: {
          color: (d.completion_rate || 0) >= 80 ? '#2E7D32' : (d.completion_rate || 0) >= 50 ? '#FF9800' : '#C41E3A',
          borderRadius: [4, 4, 0, 0]
        }
      })),
      barWidth: '50%',
      label: {
        show: true,
        position: 'top',
        color: '#666',
        formatter: '{c}%'
      }
    }]
  }
})

const issueTypeChartOption = computed(() => {
  const data = reviewStats.value.issue_type_distribution || []
  const colors = ['#C41E3A', '#D4AF37', '#2E7D32', '#FF9800', '#1976D2', '#7B1FA2']
  return {
    tooltip: { trigger: 'item', formatter: '{b}: {c}个 ({d}%)' },
    legend: { orient: 'vertical', left: 'left', textStyle: { color: '#666' } },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      center: ['65%', '50%'],
      avoidLabelOverlap: false,
      itemStyle: { borderRadius: 8, borderColor: '#fff', borderWidth: 2 },
      label: { show: false, position: 'center' },
      emphasis: {
        label: { show: true, fontSize: 16, fontWeight: 'bold', color: '#C41E3A' }
      },
      labelLine: { show: false },
      data: data.map((d, i) => ({
        value: d.count,
        name: d.label,
        itemStyle: { color: colors[i % colors.length] }
      }))
    }]
  }
})

const taskSourceChartOption = computed(() => {
  const data = reviewStats.value.task_source_breakdown || []
  const colors = ['#7B1FA2', '#C41E3A', '#D4AF37', '#2E7D32', '#FF9800', '#1976D2']
  return {
    tooltip: { trigger: 'item', formatter: '{b}: {c}个 ({d}%)' },
    legend: { orient: 'vertical', left: 'left', textStyle: { color: '#666' } },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      center: ['65%', '50%'],
      avoidLabelOverlap: false,
      itemStyle: { borderRadius: 8, borderColor: '#fff', borderWidth: 2 },
      label: { show: false, position: 'center' },
      emphasis: {
        label: { show: true, fontSize: 16, fontWeight: 'bold', color: '#7B1FA2' }
      },
      labelLine: { show: false },
      data: data.map((d, i) => ({
        value: d.count,
        name: d.label,
        itemStyle: { color: colors[i % colors.length] }
      }))
    }]
  }
})

const memberTaskChartOption = computed(() => {
  const data = [...(reviewStats.value.member_task_stats || [])].sort((a, b) => a.completion_rate - b.completion_rate)
  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      formatter: '{b}: {c}%'
    },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: {
      type: 'value',
      name: '完成率(%)',
      nameTextStyle: { color: '#666' },
      axisLabel: { color: '#666', formatter: '{value}%' },
      splitLine: { lineStyle: { color: '#E8DCC8', type: 'dashed' } },
      max: 100
    },
    yAxis: {
      type: 'category',
      data: data.map(d => d.member_name),
      axisLabel: { color: '#666', fontSize: 12 },
      axisLine: { lineStyle: { color: '#E8DCC8' } }
    },
    series: [{
      name: '任务完成率',
      type: 'bar',
      data: data.map(d => ({
        value: d.completion_rate,
        itemStyle: {
          color: d.completion_rate >= 80 ? '#2E7D32' : d.completion_rate >= 50 ? '#FF9800' : '#C41E3A',
          borderRadius: [0, 4, 4, 0]
        }
      })),
      barWidth: '60%',
      label: {
        show: true,
        position: 'right',
        color: '#666',
        formatter: '{c}%'
      }
    }]
  }
})

const stagePerformanceChartOption = computed(() => {
  const data = reviewStats.value.stage_performance_distribution || []
  const colors = ['#2E7D32', '#4CAF50', '#FF9800', '#F44336', '#9E9E9E']
  return {
    tooltip: { trigger: 'item', formatter: '{b}: {c}个 ({d}%)' },
    legend: { bottom: 0, textStyle: { color: '#666' } },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      center: ['50%', '45%'],
      avoidLabelOverlap: false,
      itemStyle: { borderRadius: 8, borderColor: '#fff', borderWidth: 2 },
      label: { show: false, position: 'center' },
      emphasis: {
        label: { show: true, fontSize: 16, fontWeight: 'bold', color: '#2E7D32' }
      },
      labelLine: { show: false },
      data: data.map((d, i) => ({
        value: d.value,
        name: d.name,
        itemStyle: { color: colors[i % colors.length] }
      }))
    }]
  }
})

const rhythmStabilityChartOption = computed(() => {
  const data = reviewStats.value.rhythm_stability_distribution || []
  const colors = ['#2E7D32', '#4CAF50', '#FF9800', '#F44336', '#9E9E9E']
  return {
    tooltip: { trigger: 'item', formatter: '{b}: {c}个 ({d}%)' },
    legend: { bottom: 0, textStyle: { color: '#666' } },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      center: ['50%', '45%'],
      avoidLabelOverlap: false,
      itemStyle: { borderRadius: 8, borderColor: '#fff', borderWidth: 2 },
      label: { show: false, position: 'center' },
      emphasis: {
        label: { show: true, fontSize: 16, fontWeight: 'bold', color: '#2E7D32' }
      },
      labelLine: { show: false },
      data: data.map((d, i) => ({
        value: d.value,
        name: d.name,
        itemStyle: { color: colors[i % colors.length] }
      }))
    }]
  }
})

function goToRehearsalChecks() {
  router.push('/rehearsal-checks')
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

.risk-overview {
  display: flex;
  gap: 24px;
  align-items: center;
  flex-wrap: wrap;

  .risk-stat {
    flex: 1;
    min-width: 140px;
    text-align: center;
    padding: 16px;
    background: linear-gradient(135deg, rgba(196, 30, 58, 0.06), rgba(212, 175, 55, 0.06));
    border-radius: 10px;

    .risk-stat-value {
      font-size: 30px;
      font-weight: bold;
      color: #C41E3A;
    }

    .risk-stat-label {
      font-size: 13px;
      color: #666;
      margin-top: 4px;
    }
  }

  .risk-stat-link {
    display: flex;
    align-items: center;
    gap: 6px;
    color: #C41E3A;
    cursor: pointer;
    font-weight: 600;

    &:hover {
      color: #8B0000;
    }
  }
}

.sub-title {
  font-size: 15px;
  font-weight: 600;
  color: #C41E3A;
  margin-bottom: 12px;
}

.small-chart {
  height: 280px;
}

.muted {
  color: #999;
  font-size: 12px;
}
</style>
