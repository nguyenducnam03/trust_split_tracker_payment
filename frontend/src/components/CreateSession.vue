<template>
  <div class="create-session">
    <h2>Create Payment Session</h2>

    <!-- Session info -->
    <div class="session-info">
      <div class="field">
        <label>Session name</label>
        <input v-model="sessionName" type="text" placeholder="e.g. Badminton 19/04" />
      </div>
      <div class="field">
        <label>Number of people</label>
        <input v-model.number="numberOfPeople" type="number" min="1" max="50" placeholder="e.g. 8" @keydown.enter.prevent="focusFirstName" />
      </div>
    </div>

    <!-- Cost items -->
    <div class="cost-section">
      <div class="cost-header">
        <span class="section-label">Cost items</span>
        <button class="btn-add-cost" @click="addCostItem">+ Add item</button>
      </div>
      <div class="cost-list" v-if="costItems.length > 0">
        <div v-for="(item, i) in costItems" :key="i" class="cost-item">
          <input v-model="item.name" type="text" placeholder="e.g. Court" class="cost-name" />
          <div class="cost-amount-wrap">
            <input v-model.number="item.total" type="number" min="0" placeholder="0" class="cost-amount" />
            <span class="cost-unit">k</span>
          </div>
          <button class="btn-remove" @click="removeCostItem(i)">✕</button>
        </div>
      </div>
      <p v-else class="hint">No cost items → enter amount manually below</p>
    </div>

    <!-- Grid -->
    <div class="grid-wrap" v-if="members.length > 0">
      <div class="grid-scroll">
        <table class="grid">
          <thead>
            <tr>
              <th class="col-no">#</th>
              <th class="col-name">Name</th>
              <th v-for="(item, i) in costItems" :key="i" class="col-check">
                <div class="cost-th">
                  <span>{{ item.name || `Khoản ${i + 1}` }}</span>
                  <span class="cost-th-amount">{{ item.total || 0 }}k</span>
                  <button class="btn-toggle-all" @click="toggleAll(i)">
                    {{ isAllSelected(i) ? 'Uncheck all' : 'Check all' }}
                  </button>
                </div>
              </th>
              <th class="col-amount">Amount</th>
              <th class="col-action"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(member, idx) in members" :key="idx">
              <td class="col-no">{{ idx + 1 }}</td>
              <td class="col-name">
                <input v-model="member.name" type="text" placeholder="Name" :data-name-idx="idx" @keydown.enter.prevent="focusNext('name', idx)" />
              </td>
              <td v-for="(item, i) in costItems" :key="i" class="col-check">
                <label class="check-cell">
                  <input type="checkbox" v-model="member.selected[i]" />
                  <span class="check-amount" :class="{ dimmed: !member.selected[i] }">
                    {{ formatCheckAmount(item, i) }}
                  </span>
                </label>
              </td>
              <td class="col-amount">
                <span v-if="costItems.length > 0" class="amount-auto">
                  {{ formatMoney(calcAmount(idx)) }}
                </span>
                <input
                  v-else
                  v-model.number="member.manualAmount"
                  type="number"
                  min="0"
                  placeholder="0"
                  :data-amount-idx="idx"
                  @keydown.enter.prevent="focusNext('amount', idx)"
                />
                <span v-if="costItems.length === 0" class="cost-unit">k</span>
              </td>
              <td class="col-action">
                <button class="btn-remove" @click="removeMember(idx)">✕</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <button class="btn-add-row" @click="addMember">+ Add person</button>
    </div>

    <!-- Summary -->
    <div class="summary" v-if="members.length > 0">
      <span>Total: <strong>{{ formatMoney(totalAmount) }}</strong></span>
      <span>{{ members.length }} people</span>
    </div>

    <!-- Submit -->
    <button class="btn-submit" :disabled="!canSubmit || loading" @click="onSubmit">
      {{ loading ? 'Creating...' : 'Create Session' }}
    </button>
    <p v-if="validationError && showValidation" class="error">{{ validationError }}</p>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { createSession } from '../services/api'

const router = useRouter()
const loading = ref(false)
const error = ref('')
const showValidation = ref(false)

const sessionName = ref('')
const numberOfPeople = ref(null)
const costItems = ref([])
const members = ref([])

watch(numberOfPeople, (n) => {
  if (!n || n < 1) { members.value = []; return }
  const current = members.value.length
  if (n > current) {
    for (let i = current; i < n; i++) {
      members.value.push(newMember())
    }
  } else {
    members.value = members.value.slice(0, n)
  }
})

watch(costItems, (items) => {
  members.value.forEach((m) => {
    while (m.selected.length < items.length) m.selected.push(true)
    m.selected = m.selected.slice(0, items.length)
  })
}, { deep: true })

function newMember() {
  return { name: '', manualAmount: null, selected: costItems.value.map(() => true) }
}

function addMember() {
  members.value.push(newMember())
  numberOfPeople.value = members.value.length
}

function removeMember(idx) {
  members.value.splice(idx, 1)
  numberOfPeople.value = members.value.length
}

function isAllSelected(i) {
  return members.value.every((m) => m.selected[i])
}

function toggleAll(i) {
  const allSelected = isAllSelected(i)
  members.value.forEach((m) => (m.selected[i] = !allSelected))
}

function addCostItem() {
  costItems.value.push({ name: '', total: null })
  members.value.forEach((m) => m.selected.push(true))
}

function removeCostItem(i) {
  costItems.value.splice(i, 1)
  members.value.forEach((m) => m.selected.splice(i, 1))
}

function calcAmount(memberIdx) {
  return costItems.value.reduce((sum, item, i) => {
    if (!item.total) return sum
    const participants = members.value.filter((m) => m.selected[i]).length
    if (participants === 0) return sum
    return members.value[memberIdx].selected[i]
      ? sum + (item.total * 1000) / participants
      : sum
  }, 0)
}

const totalAmount = computed(() => {
  if (costItems.value.length > 0) {
    return members.value.reduce((sum, _, idx) => sum + calcAmount(idx), 0)
  }
  return members.value.reduce((sum, m) => sum + (m.manualAmount || 0) * 1000, 0)
})

const validationError = computed(() => {
  if (!sessionName.value.trim()) return 'Session name is required'
  if (members.value.length === 0) return 'Add at least one person'
  const missingName = members.value.some(m => !m.name.trim())
  if (missingName) return 'All members must have a name'
  if (costItems.value.length === 0) {
    const missingAmount = members.value.some(m => !m.manualAmount || m.manualAmount <= 0)
    if (missingAmount) return 'All members must have an amount > 0'
  }
  return ''
})

const canSubmit = computed(() => !validationError.value)

function focusFirstName() {
  const first = document.querySelector('[data-name-idx="0"]')
  if (first) first.focus()
}

function focusNext(type, idx) {
  const next = document.querySelector(`[data-${type}-idx="${idx + 1}"]`)
  if (next) next.focus()
}

function formatCheckAmount(item, i) {
  if (!item.total) return ''
  const participants = members.value.filter((m) => m.selected[i]).length
  if (participants === 0) return ''
  return Math.round((item.total * 1000) / participants).toLocaleString('vi-VN') + 'đ'
}

function formatMoney(n) {
  return Math.round(n || 0).toLocaleString('vi-VN') + 'đ'
}

async function onSubmit() {
  showValidation.value = true
  if (validationError.value) return
  loading.value = true
  error.value = ''
  try {
    const payload = {
      name: sessionName.value,
      cost_items: costItems.value.filter(c => c.name && c.total),
      members: members.value.map((m, idx) => ({
        name: m.name,
        amount: costItems.value.length > 0 ? calcAmount(idx) : (m.manualAmount || 0) * 1000,
      })),
    }
    const session = await createSession(payload)
    router.push(`/sessions/${session.id}`)
  } catch (err) {
    error.value = err.response?.data?.detail || 'Something went wrong'
  } finally {
    loading.value = false
  }
}
</script>
