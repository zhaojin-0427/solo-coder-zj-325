import { apiRequest } from '@/utils/request'

function extractResults(response) {
  if (response && response.results !== undefined) {
    return response.results
  }
  return response
}

export function fetchPrograms() {
  return apiRequest('GET', '/programs/').then(extractResults)
}

export function createProgram(data) {
  return apiRequest('POST', '/programs/', data)
}

export function updateProgram(id, data) {
  return apiRequest('PUT', `/programs/${id}/`, data)
}

export function deleteProgram(id) {
  return apiRequest('DELETE', `/programs/${id}/`)
}

export function fetchArias(programId = null) {
  const params = programId ? { program: programId } : null
  return apiRequest('GET', '/arias/', null, params).then(extractResults)
}

export function createAria(data) {
  return apiRequest('POST', '/arias/', data)
}

export function updateAria(id, data) {
  return apiRequest('PUT', `/arias/${id}/`, data)
}

export function deleteAria(id) {
  return apiRequest('DELETE', `/arias/${id}/`)
}

export function fetchRoles(programId = null) {
  const params = programId ? { program: programId } : null
  return apiRequest('GET', '/roles/', null, params).then(extractResults)
}

export function createRole(data) {
  return apiRequest('POST', '/roles/', data)
}

export function updateRole(id, data) {
  return apiRequest('PUT', `/roles/${id}/`, data)
}

export function deleteRole(id) {
  return apiRequest('DELETE', `/roles/${id}/`)
}

export function fetchMembers() {
  return apiRequest('GET', '/members/').then(extractResults)
}

export function createMember(data) {
  return apiRequest('POST', '/members/', data)
}

export function updateMember(id, data) {
  return apiRequest('PUT', `/members/${id}/`, data)
}

export function deleteMember(id) {
  return apiRequest('DELETE', `/members/${id}/`)
}

export function fetchAssignments(programId = null) {
  const params = programId ? { program: programId } : null
  return apiRequest('GET', '/aria-assignments/', null, params).then(extractResults)
}

export function createAssignment(data) {
  return apiRequest('POST', '/aria-assignments/', data)
}

export function updateAssignment(id, data) {
  return apiRequest('PUT', `/aria-assignments/${id}/`, data)
}

export function deleteAssignment(id) {
  return apiRequest('DELETE', `/aria-assignments/${id}/`)
}

export function autoAssign(programId) {
  return apiRequest('POST', '/auto-assign/', { program_id: programId })
}

export function applyAutoAssign(assignments) {
  return apiRequest('POST', '/apply-auto-assign/', { assignments })
}

export function fetchRehearsals(programId = null) {
  const params = programId ? { program: programId } : null
  return apiRequest('GET', '/rehearsals/', null, params).then(extractResults)
}

export function createRehearsal(data) {
  return apiRequest('POST', '/rehearsals/', data)
}

export function updateRehearsal(id, data) {
  return apiRequest('PUT', `/rehearsals/${id}/`, data)
}

export function deleteRehearsal(id) {
  return apiRequest('DELETE', `/rehearsals/${id}/`)
}

export function fetchFeedbacks(rehearsalId = null) {
  const params = rehearsalId ? { rehearsal: rehearsalId } : null
  return apiRequest('GET', '/rehearsal-feedbacks/', null, params).then(extractResults)
}

export function createFeedback(data) {
  return apiRequest('POST', '/rehearsal-feedbacks/', data)
}

export function updateFeedback(id, data) {
  return apiRequest('PUT', `/rehearsal-feedbacks/${id}/`, data)
}

export function deleteFeedback(id) {
  return apiRequest('DELETE', `/rehearsal-feedbacks/${id}/`)
}

export function fetchUnderstudyChanges() {
  return apiRequest('GET', '/understudy-changes/').then(extractResults)
}

export function createUnderstudyChange(data) {
  return apiRequest('POST', '/understudy-changes/', data)
}

export function updateUnderstudyChange(id, data) {
  return apiRequest('PUT', `/understudy-changes/${id}/`, data)
}

export function fetchArchives() {
  return apiRequest('GET', '/archives/').then(extractResults)
}

export function createArchive(data) {
  return apiRequest('POST', '/archives/', data)
}

export function fetchStatistics() {
  return apiRequest('GET', '/statistics/')
}

export function fetchRehearsalChecks(programId = null) {
  const params = programId ? { program_id: programId } : null
  return apiRequest('GET', '/rehearsal-checks/', null, params).then(extractResults)
}

export function createRehearsalCheck(data) {
  return apiRequest('POST', '/rehearsal-checks/', data)
}

export function updateRehearsalCheck(id, data) {
  return apiRequest('PUT', `/rehearsal-checks/${id}/`, data)
}

export function deleteRehearsalCheck(id) {
  return apiRequest('DELETE', `/rehearsal-checks/${id}/`)
}

export function fetchRehearsalCheckItems(checkId) {
  return apiRequest('GET', `/rehearsal-checks/${checkId}/items/`)
}

export function fetchRiskDashboard(checkId) {
  return apiRequest('GET', `/rehearsal-checks/${checkId}/risk_dashboard/`)
}

export function generateRiskActions(checkId) {
  return apiRequest('POST', `/rehearsal-checks/${checkId}/generate_actions/`)
}

export function confirmAccompaniment(itemId, memberId = null) {
  return apiRequest('POST', `/rehearsal-check-items/${itemId}/confirm_accompaniment/`, memberId ? { member_id: memberId } : {})
}

export function setRehearsalCheckItemRisk(itemId, data) {
  return apiRequest('POST', `/rehearsal-check-items/${itemId}/set_risk/`, data)
}

export function updateRehearsalCheckConfirmation(id, data) {
  return apiRequest('PUT', `/rehearsal-check-confirmations/${id}/`, data)
}

export function fetchRiskActions(checkId = null, isActive = null) {
  const params = {}
  if (checkId) params.rehearsal_check = checkId
  if (isActive !== null) params.is_active = isActive
  return apiRequest('GET', '/risk-action-items/', null, Object.keys(params).length ? params : null).then(extractResults)
}

export function resolveRiskAction(id, handlerId = null, handlerNote = '') {
  const data = {}
  if (handlerId) data.handler_id = handlerId
  if (handlerNote) data.handler_note = handlerNote
  return apiRequest('POST', `/risk-action-items/${id}/resolve/`, data)
}

export function confirmCloseRiskAction(id, handlerId = null, handlerNote = '') {
  const data = {}
  if (handlerId) data.handler_id = handlerId
  if (handlerNote) data.handler_note = handlerNote
  return apiRequest('POST', `/risk-action-items/${id}/confirm_close/`, data)
}

export function rejectAutoResolve(id, handlerNote = '') {
  return apiRequest('POST', `/risk-action-items/${id}/reject_auto_resolve/`, { handler_note: handlerNote })
}

export function updateRiskActionHandler(id, handlerId = null, handlerNote = '') {
  const data = {}
  if (handlerId) data.handler_id = handlerId
  if (handlerNote) data.handler_note = handlerNote
  return apiRequest('POST', `/risk-action-items/${id}/update_handler/`, data)
}

export function fetchActiveRisks(checkId = null) {
  const params = checkId ? { rehearsal_check: checkId } : null
  return apiRequest('GET', '/risk-action-items/active_risks/', null, params).then(extractResults)
}

export function fetchHistoryRisks(checkId = null) {
  const params = checkId ? { rehearsal_check: checkId } : null
  return apiRequest('GET', '/risk-action-items/history_risks/', null, params).then(extractResults)
}

export function reviewItemRisks(itemId) {
  return apiRequest('POST', `/rehearsal-check-items/${itemId}/review_risks/`)
}

export function fetchPerformanceReviews(programId = null) {
  const params = programId ? { program_id: programId } : null
  return apiRequest('GET', '/performance-reviews/', null, params).then(extractResults)
}

export function createPerformanceReview(data) {
  return apiRequest('POST', '/create-performance-review/', data)
}

export function updatePerformanceReview(id, data) {
  return apiRequest('PUT', `/performance-reviews/${id}/`, data)
}

export function deletePerformanceReview(id) {
  return apiRequest('DELETE', `/performance-reviews/${id}/`)
}

export function fetchReviewSummary(reviewId) {
  return apiRequest('GET', `/performance-reviews/${reviewId}/summary/`)
}

export function fetchReviewItems(reviewId) {
  return apiRequest('GET', `/performance-reviews/${reviewId}/items/`)
}

export function startTeacherReview(reviewId) {
  return apiRequest('POST', `/performance-reviews/${reviewId}/start_teacher_review/`)
}

export function startMemberReview(reviewId) {
  return apiRequest('POST', `/performance-reviews/${reviewId}/start_member_review/`)
}

export function completeReview(reviewId) {
  return apiRequest('POST', `/performance-reviews/${reviewId}/complete_review/`)
}

export function fetchReviewConclusions(reviewId = null, reviewItemId = null) {
  const params = {}
  if (reviewId) params.review = reviewId
  if (reviewItemId) params.review_item = reviewItemId
  return apiRequest('GET', '/performance-review-conclusions/', null, Object.keys(params).length ? params : null).then(extractResults)
}

export function createReviewConclusion(data) {
  return apiRequest('POST', '/performance-review-conclusions/', data)
}

export function updateReviewConclusion(id, data) {
  return apiRequest('PUT', `/performance-review-conclusions/${id}/`, data)
}

export function deleteReviewConclusion(id) {
  return apiRequest('DELETE', `/performance-review-conclusions/${id}/`)
}

export function fetchMemberSelfReviews(reviewId = null, reviewItemId = null, memberId = null) {
  const params = {}
  if (reviewId) params.review = reviewId
  if (reviewItemId) params.review_item = reviewItemId
  if (memberId) params.member_id = memberId
  return apiRequest('GET', '/member-self-reviews/', null, Object.keys(params).length ? params : null).then(extractResults)
}

export function createMemberSelfReview(data) {
  return apiRequest('POST', '/member-self-reviews/', data)
}

export function updateMemberSelfReview(id, data) {
  return apiRequest('PUT', `/member-self-reviews/${id}/`, data)
}

export function deleteMemberSelfReview(id) {
  return apiRequest('DELETE', `/member-self-reviews/${id}/`)
}

export function fetchImprovementTasks(reviewId = null, status = null, assigneeId = null) {
  const params = {}
  if (reviewId) params.review = reviewId
  if (status) params.status = status
  if (assigneeId) params.assignee_id = assigneeId
  return apiRequest('GET', '/improvement-tasks/', null, Object.keys(params).length ? params : null).then(extractResults)
}

export function createImprovementTask(data) {
  return apiRequest('POST', '/improvement-tasks/', data)
}

export function updateImprovementTask(id, data) {
  return apiRequest('PUT', `/improvement-tasks/${id}/`, data)
}

export function deleteImprovementTask(id) {
  return apiRequest('DELETE', `/improvement-tasks/${id}/`)
}

export function completeImprovementTask(id, completionNote = '') {
  return apiRequest('POST', `/improvement-tasks/${id}/complete/`, { completion_note: completionNote })
}

export function startImprovementTask(id) {
  return apiRequest('POST', `/improvement-tasks/${id}/start/`)
}

export function convertToTask(data) {
  return apiRequest('POST', '/convert-to-task/', data)
}
