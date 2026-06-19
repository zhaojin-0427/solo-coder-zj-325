import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import {
  fetchPrograms, createProgram, updateProgram, deleteProgram,
  fetchArias, createAria, updateAria, deleteAria,
  fetchRoles, createRole, updateRole, deleteRole,
  fetchMembers, createMember, updateMember, deleteMember,
  fetchAssignments, createAssignment, updateAssignment, deleteAssignment, autoAssign, applyAutoAssign,
  fetchRehearsals, createRehearsal, updateRehearsal, deleteRehearsal,
  fetchFeedbacks, createFeedback, updateFeedback, deleteFeedback,
  fetchUnderstudyChanges, createUnderstudyChange, updateUnderstudyChange,
  fetchStatistics, fetchArchives, createArchive,
  fetchRehearsalChecks, createRehearsalCheck, updateRehearsalCheck, deleteRehearsalCheck,
  fetchRehearsalCheckItems, fetchRiskDashboard, generateRiskActions,
  confirmAccompaniment, setRehearsalCheckItemRisk, updateRehearsalCheckConfirmation,
  fetchRiskActions, resolveRiskAction, confirmCloseRiskAction, rejectAutoResolve,
  updateRiskActionHandler, fetchActiveRisks, fetchHistoryRisks, reviewItemRisks,
  fetchPerformanceReviews, createPerformanceReview, updatePerformanceReview, deletePerformanceReview,
  fetchReviewSummary, fetchReviewItems, startTeacherReview, startMemberReview, completeReview,
  fetchReviewConclusions, createReviewConclusion, updateReviewConclusion, deleteReviewConclusion,
  fetchMemberSelfReviews, createMemberSelfReview, updateMemberSelfReview, deleteMemberSelfReview,
  fetchImprovementTasks, createImprovementTask, updateImprovementTask, deleteImprovementTask,
  completeImprovementTask, startImprovementTask, convertToTask
} from '@/api/opera'

export const useOperaStore = defineStore('opera', () => {
  const programs = ref([])
  const arias = ref([])
  const roles = ref([])
  const members = ref([])
  const assignments = ref([])
  const rehearsals = ref([])
  const feedbacks = ref([])
  const understudyChanges = ref([])
  const archives = ref([])
  const statistics = ref(null)
  const rehearsalChecks = ref([])
  const riskActions = ref([])
  const performanceReviews = ref([])
  const reviewItems = ref([])
  const reviewConclusions = ref([])
  const selfReviews = ref([])
  const improvementTasks = ref([])
  const loading = ref(false)

  const activePrograms = computed(() => programs.value.filter(p => ['planning', 'rehearsing', 'performing'].includes(p.status)))
  const activeAssignments = computed(() => assignments.value.filter(a => a.status === 'confirmed'))
  const pendingUnderstudy = computed(() => understudyChanges.value.filter(u => u.status === 'pending'))
  const openRehearsalChecks = computed(() => rehearsalChecks.value.filter(c => c.status === 'open'))

  async function loadPrograms() {
    loading.value = true
    try {
      programs.value = await fetchPrograms()
    } finally {
      loading.value = false
    }
  }

  async function loadArias(programId = null) {
    loading.value = true
    try {
      arias.value = await fetchArias(programId)
    } finally {
      loading.value = false
    }
  }

  async function loadRoles(programId = null) {
    loading.value = true
    try {
      roles.value = await fetchRoles(programId)
    } finally {
      loading.value = false
    }
  }

  async function loadMembers() {
    loading.value = true
    try {
      members.value = await fetchMembers()
    } finally {
      loading.value = false
    }
  }

  async function loadAssignments(programId = null) {
    loading.value = true
    try {
      assignments.value = await fetchAssignments(programId)
    } finally {
      loading.value = false
    }
  }

  async function loadRehearsals(programId = null) {
    loading.value = true
    try {
      rehearsals.value = await fetchRehearsals(programId)
    } finally {
      loading.value = false
    }
  }

  async function loadFeedbacks(rehearsalId = null) {
    loading.value = true
    try {
      feedbacks.value = await fetchFeedbacks(rehearsalId)
    } finally {
      loading.value = false
    }
  }

  async function loadUnderstudyChanges() {
    loading.value = true
    try {
      understudyChanges.value = await fetchUnderstudyChanges()
    } finally {
      loading.value = false
    }
  }

  async function loadStatistics() {
    loading.value = true
    try {
      statistics.value = await fetchStatistics()
    } finally {
      loading.value = false
    }
  }

  async function loadArchives() {
    loading.value = true
    try {
      archives.value = await fetchArchives()
    } finally {
      loading.value = false
    }
  }

  async function addArchive(data) {
    const result = await createArchive(data)
    archives.value.push(result)
    return result
  }

  async function loadRehearsalChecks(programId = null) {
    loading.value = true
    try {
      rehearsalChecks.value = await fetchRehearsalChecks(programId)
    } finally {
      loading.value = false
    }
  }

  async function addRehearsalCheck(data) {
    const result = await createRehearsalCheck(data)
    rehearsalChecks.value.unshift(result)
    return result
  }

  async function editRehearsalCheck(id, data) {
    const result = await updateRehearsalCheck(id, data)
    const index = rehearsalChecks.value.findIndex(c => c.id === id)
    if (index !== -1) rehearsalChecks.value[index] = result
    return result
  }

  async function removeRehearsalCheck(id) {
    await deleteRehearsalCheck(id)
    rehearsalChecks.value = rehearsalChecks.value.filter(c => c.id !== id)
  }

  function getRehearsalCheckById(id) {
    return rehearsalChecks.value.find(c => c.id === parseInt(id))
  }

  async function loadPerformanceReviews(programId = null) {
    loading.value = true
    try {
      performanceReviews.value = await fetchPerformanceReviews(programId)
    } finally {
      loading.value = false
    }
  }

  async function addPerformanceReview(data) {
    const result = await createPerformanceReview(data)
    if (result.review) {
      performanceReviews.value.unshift(result.review)
      return result.review
    }
    return result
  }

  async function editPerformanceReview(id, data) {
    const result = await updatePerformanceReview(id, data)
    const index = performanceReviews.value.findIndex(r => r.id === id)
    if (index !== -1) performanceReviews.value[index] = result
    return result
  }

  async function removePerformanceReview(id) {
    await deletePerformanceReview(id)
    performanceReviews.value = performanceReviews.value.filter(r => r.id !== id)
  }

  function getPerformanceReviewById(id) {
    return performanceReviews.value.find(r => r.id === parseInt(id))
  }

  async function getReviewSummary(reviewId) {
    return await fetchReviewSummary(reviewId)
  }

  async function loadReviewItems(reviewId) {
    loading.value = true
    try {
      reviewItems.value = await fetchReviewItems(reviewId)
    } finally {
      loading.value = false
    }
  }

  async function startTeacherReviewById(reviewId) {
    const result = await startTeacherReview(reviewId)
    const index = performanceReviews.value.findIndex(r => r.id === reviewId)
    if (index !== -1) performanceReviews.value[index] = result
    return result
  }

  async function startMemberReviewById(reviewId) {
    const result = await startMemberReview(reviewId)
    const index = performanceReviews.value.findIndex(r => r.id === reviewId)
    if (index !== -1) performanceReviews.value[index] = result
    return result
  }

  async function completeReviewById(reviewId) {
    const result = await completeReview(reviewId)
    const index = performanceReviews.value.findIndex(r => r.id === reviewId)
    if (index !== -1) performanceReviews.value[index] = result
    return result
  }

  async function loadReviewConclusions(reviewId = null, reviewItemId = null) {
    loading.value = true
    try {
      reviewConclusions.value = await fetchReviewConclusions(reviewId, reviewItemId)
    } finally {
      loading.value = false
    }
  }

  async function addReviewConclusion(data) {
    const result = await createReviewConclusion(data)
    reviewConclusions.value.unshift(result)
    return result
  }

  async function editReviewConclusion(id, data) {
    const result = await updateReviewConclusion(id, data)
    const index = reviewConclusions.value.findIndex(c => c.id === id)
    if (index !== -1) reviewConclusions.value[index] = result
    return result
  }

  async function removeReviewConclusion(id) {
    await deleteReviewConclusion(id)
    reviewConclusions.value = reviewConclusions.value.filter(c => c.id !== id)
  }

  async function loadSelfReviews(reviewId = null, reviewItemId = null, memberId = null) {
    loading.value = true
    try {
      selfReviews.value = await fetchMemberSelfReviews(reviewId, reviewItemId, memberId)
    } finally {
      loading.value = false
    }
  }

  async function addSelfReview(data) {
    const result = await createMemberSelfReview(data)
    selfReviews.value.push(result)
    return result
  }

  async function editSelfReview(id, data) {
    const result = await updateMemberSelfReview(id, data)
    const index = selfReviews.value.findIndex(r => r.id === id)
    if (index !== -1) selfReviews.value[index] = result
    return result
  }

  async function removeSelfReview(id) {
    await deleteMemberSelfReview(id)
    selfReviews.value = selfReviews.value.filter(r => r.id !== id)
  }

  async function loadImprovementTasks(reviewId = null, status = null, assigneeId = null) {
    loading.value = true
    try {
      improvementTasks.value = await fetchImprovementTasks(reviewId, status, assigneeId)
    } finally {
      loading.value = false
    }
  }

  async function addImprovementTask(data) {
    const result = await createImprovementTask(data)
    improvementTasks.value.unshift(result)
    return result
  }

  async function editImprovementTask(id, data) {
    const result = await updateImprovementTask(id, data)
    const index = improvementTasks.value.findIndex(t => t.id === id)
    if (index !== -1) improvementTasks.value[index] = result
    return result
  }

  async function removeImprovementTask(id) {
    await deleteImprovementTask(id)
    improvementTasks.value = improvementTasks.value.filter(t => t.id !== id)
  }

  async function completeImprovementTaskById(id, completionNote = '') {
    const result = await completeImprovementTask(id, completionNote)
    const index = improvementTasks.value.findIndex(t => t.id === id)
    if (index !== -1) improvementTasks.value[index] = result
    return result
  }

  async function startImprovementTaskById(id) {
    const result = await startImprovementTask(id)
    const index = improvementTasks.value.findIndex(t => t.id === id)
    if (index !== -1) improvementTasks.value[index] = result
    return result
  }

  async function convertToImprovementTask(data) {
    const result = await convertToTask(data)
    improvementTasks.value.unshift(result)
    return result
  }

  async function getRehearsalCheckItems(checkId) {
    return await fetchRehearsalCheckItems(checkId)
  }

  async function getRiskDashboard(checkId) {
    return await fetchRiskDashboard(checkId)
  }

  async function runGenerateRiskActions(checkId) {
    const result = await generateRiskActions(checkId)
    await loadRiskActions(checkId)
    return result
  }

  async function loadRiskActions(checkId = null) {
    loading.value = true
    try {
      riskActions.value = await fetchRiskActions(checkId)
    } finally {
      loading.value = false
    }
  }

  async function resolveRiskActionById(id, handlerId = null, handlerNote = '') {
    const result = await resolveRiskAction(id, handlerId, handlerNote)
    const index = riskActions.value.findIndex(a => a.id === id)
    if (index !== -1) riskActions.value[index] = result
    return result
  }

  async function confirmCloseRiskActionById(id, handlerId = null, handlerNote = '') {
    const result = await confirmCloseRiskAction(id, handlerId, handlerNote)
    const index = riskActions.value.findIndex(a => a.id === id)
    if (index !== -1) riskActions.value[index] = result
    return result
  }

  async function rejectAutoResolveById(id, handlerNote = '') {
    const result = await rejectAutoResolve(id, handlerNote)
    const index = riskActions.value.findIndex(a => a.id === id)
    if (index !== -1) riskActions.value[index] = result
    return result
  }

  async function updateRiskActionHandlerById(id, handlerId = null, handlerNote = '') {
    const result = await updateRiskActionHandler(id, handlerId, handlerNote)
    const index = riskActions.value.findIndex(a => a.id === id)
    if (index !== -1) riskActions.value[index] = result
    return result
  }

  async function loadActiveRisks(checkId = null) {
    loading.value = true
    try {
      riskActions.value = await fetchActiveRisks(checkId)
    } finally {
      loading.value = false
    }
  }

  async function loadHistoryRisks(checkId = null) {
    loading.value = true
    try {
      const history = await fetchHistoryRisks(checkId)
      return history
    } finally {
      loading.value = false
    }
  }

  async function reviewRisksForItem(itemId) {
    return await reviewItemRisks(itemId)
  }

  async function confirmAccompanimentForItem(itemId, memberId = null) {
    return await confirmAccompaniment(itemId, memberId)
  }

  async function setItemRisk(itemId, data) {
    return await setRehearsalCheckItemRisk(itemId, data)
  }

  async function updateConfirmation(confirmationId, data) {
    return await updateRehearsalCheckConfirmation(confirmationId, data)
  }

  async function addProgram(data) {
    const result = await createProgram(data)
    programs.value.push(result)
    return result
  }

  async function editProgram(id, data) {
    const result = await updateProgram(id, data)
    const index = programs.value.findIndex(p => p.id === id)
    if (index !== -1) programs.value[index] = result
    return result
  }

  async function removeProgram(id) {
    await deleteProgram(id)
    programs.value = programs.value.filter(p => p.id !== id)
  }

  async function addAria(data) {
    const result = await createAria(data)
    arias.value.push(result)
    return result
  }

  async function editAria(id, data) {
    const result = await updateAria(id, data)
    const index = arias.value.findIndex(a => a.id === id)
    if (index !== -1) arias.value[index] = result
    return result
  }

  async function removeAria(id) {
    await deleteAria(id)
    arias.value = arias.value.filter(a => a.id !== id)
  }

  async function addRole(data) {
    const result = await createRole(data)
    roles.value.push(result)
    return result
  }

  async function editRole(id, data) {
    const result = await updateRole(id, data)
    const index = roles.value.findIndex(r => r.id === id)
    if (index !== -1) roles.value[index] = result
    return result
  }

  async function removeRole(id) {
    await deleteRole(id)
    roles.value = roles.value.filter(r => r.id !== id)
  }

  async function addMember(data) {
    const result = await createMember(data)
    members.value.push(result)
    return result
  }

  async function editMember(id, data) {
    const result = await updateMember(id, data)
    const index = members.value.findIndex(m => m.id === id)
    if (index !== -1) members.value[index] = result
    return result
  }

  async function removeMember(id) {
    await deleteMember(id)
    members.value = members.value.filter(m => m.id !== id)
  }

  async function addAssignment(data) {
    const result = await createAssignment(data)
    assignments.value.push(result)
    return result
  }

  async function editAssignment(id, data) {
    const result = await updateAssignment(id, data)
    const index = assignments.value.findIndex(a => a.id === id)
    if (index !== -1) assignments.value[index] = result
    return result
  }

  async function removeAssignment(id) {
    await deleteAssignment(id)
    assignments.value = assignments.value.filter(a => a.id !== id)
  }

  async function runAutoAssign(programId) {
    const result = await autoAssign(programId)
    await loadAssignments(programId)
    return { ...result, count: result.total_suggestions || 0 }
  }

  async function addRehearsal(data) {
    const result = await createRehearsal(data)
    rehearsals.value.push(result)
    return result
  }

  async function editRehearsal(id, data) {
    const result = await updateRehearsal(id, data)
    const index = rehearsals.value.findIndex(r => r.id === id)
    if (index !== -1) rehearsals.value[index] = result
    return result
  }

  async function removeRehearsal(id) {
    await deleteRehearsal(id)
    rehearsals.value = rehearsals.value.filter(r => r.id !== id)
  }

  async function addFeedback(data) {
    const result = await createFeedback(data)
    feedbacks.value.push(result)
    return result
  }

  async function editFeedback(id, data) {
    const result = await updateFeedback(id, data)
    const index = feedbacks.value.findIndex(f => f.id === id)
    if (index !== -1) feedbacks.value[index] = result
    return result
  }

  async function removeFeedback(id) {
    await deleteFeedback(id)
    feedbacks.value = feedbacks.value.filter(f => f.id !== id)
  }

  async function addUnderstudyChange(data) {
    const result = await createUnderstudyChange(data)
    understudyChanges.value.push(result)
    return result
  }

  async function editUnderstudyChange(id, data) {
    const result = await updateUnderstudyChange(id, data)
    const index = understudyChanges.value.findIndex(u => u.id === id)
    if (index !== -1) understudyChanges.value[index] = result
    return result
  }

  function getProgramById(id) {
    return programs.value.find(p => p.id === parseInt(id))
  }

  function getRehearsalById(id) {
    return rehearsals.value.find(r => r.id === parseInt(id))
  }

  return {
    programs, arias, roles, members, assignments, rehearsals, feedbacks, understudyChanges, archives, statistics, loading,
    rehearsalChecks, riskActions,
    performanceReviews, reviewItems, reviewConclusions, selfReviews, improvementTasks,
    activePrograms, activeAssignments, pendingUnderstudy, openRehearsalChecks,
    loadPrograms, loadArias, loadRoles, loadMembers, loadAssignments, loadRehearsals, loadFeedbacks, loadUnderstudyChanges, loadStatistics, loadArchives,
    loadRehearsalChecks, addRehearsalCheck, editRehearsalCheck, removeRehearsalCheck,
    getRehearsalCheckItems, getRiskDashboard, runGenerateRiskActions, loadRiskActions,
    resolveRiskActionById, confirmCloseRiskActionById, rejectAutoResolveById, updateRiskActionHandlerById,
    loadActiveRisks, loadHistoryRisks, reviewRisksForItem,
    confirmAccompanimentForItem, setItemRisk, updateConfirmation,
    addProgram, editProgram, removeProgram,
    addAria, editAria, removeAria,
    addRole, editRole, removeRole,
    addMember, editMember, removeMember,
    addAssignment, editAssignment, removeAssignment, runAutoAssign,
    addRehearsal, editRehearsal, removeRehearsal,
    addFeedback, editFeedback, removeFeedback,
    addUnderstudyChange, editUnderstudyChange,
    addArchive,
    getProgramById, getRehearsalById, getRehearsalCheckById,
    loadPerformanceReviews, addPerformanceReview, editPerformanceReview, removePerformanceReview,
    getPerformanceReviewById, getReviewSummary, loadReviewItems,
    startTeacherReviewById, startMemberReviewById, completeReviewById,
    loadReviewConclusions, addReviewConclusion, editReviewConclusion, removeReviewConclusion,
    loadSelfReviews, addSelfReview, editSelfReview, removeSelfReview,
    loadImprovementTasks, addImprovementTask, editImprovementTask, removeImprovementTask,
    completeImprovementTaskById, startImprovementTaskById, convertToImprovementTask
  }
})
