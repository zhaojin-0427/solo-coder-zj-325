import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    component: () => import('@/layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        name: 'Home',
        component: () => import('@/views/Home.vue'),
        meta: { title: '首页' }
      },
      {
        path: 'programs',
        name: 'Programs',
        component: () => import('@/views/Programs.vue'),
        meta: { title: '节目档案' }
      },
      {
        path: 'programs/:id',
        name: 'ProgramDetail',
        component: () => import('@/views/ProgramDetail.vue'),
        meta: { title: '节目详情' }
      },
      {
        path: 'assignments',
        name: 'Assignments',
        component: () => import('@/views/Assignments.vue'),
        meta: { title: '唱段分配' }
      },
      {
        path: 'rehearsals',
        name: 'Rehearsals',
        component: () => import('@/views/Rehearsals.vue'),
        meta: { title: '排练记录' }
      },
      {
        path: 'rehearsals/:id',
        name: 'RehearsalDetail',
        component: () => import('@/views/RehearsalDetail.vue'),
        meta: { title: '排练详情' }
      },
      {
        path: 'understudy',
        name: 'Understudy',
        component: () => import('@/views/Understudy.vue'),
        meta: { title: '替补调整' }
      },
      {
        path: 'rehearsal-checks',
        name: 'RehearsalChecks',
        component: () => import('@/views/RehearsalCheck.vue'),
        meta: { title: '联排确认' }
      },
      {
        path: 'rehearsal-checks/:id',
        name: 'RehearsalCheckDetail',
        component: () => import('@/views/RehearsalCheckDetail.vue'),
        meta: { title: '联排确认详情' }
      },
      {
        path: 'statistics',
        name: 'Statistics',
        component: () => import('@/views/Statistics.vue'),
        meta: { title: '统计分析' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  document.title = to.meta.title ? `${to.meta.title} - 戏曲票友平台` : '戏曲票友平台'
  next()
})

export default router
