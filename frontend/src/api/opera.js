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
