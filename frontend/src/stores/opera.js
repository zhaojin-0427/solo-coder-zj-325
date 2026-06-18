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
  fetchStatistics, fetchArchives, createArchive
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
  const loading = ref(false)

  const activePrograms = computed(() => programs.value.filter(p => ['planning', 'rehearsing', 'performing'].includes(p.status)))
  const activeAssignments = computed(() => assignments.value.filter(a => a.status === 'confirmed'))
  const pendingUnderstudy = computed(() => understudyChanges.value.filter(u => u.status === 'pending'))

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
    return result
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
    activePrograms, activeAssignments, pendingUnderstudy,
    loadPrograms, loadArias, loadRoles, loadMembers, loadAssignments, loadRehearsals, loadFeedbacks, loadUnderstudyChanges, loadStatistics, loadArchives,
    addProgram, editProgram, removeProgram,
    addAria, editAria, removeAria,
    addRole, editRole, removeRole,
    addMember, editMember, removeMember,
    addAssignment, editAssignment, removeAssignment, runAutoAssign,
    addRehearsal, editRehearsal, removeRehearsal,
    addFeedback, editFeedback, removeFeedback,
    addUnderstudyChange, editUnderstudyChange,
    addArchive,
    getProgramById, getRehearsalById
  }
})
