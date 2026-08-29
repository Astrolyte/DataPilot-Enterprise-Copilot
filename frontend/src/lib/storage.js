const KEY = 'datapilot_session'

export function getSession() {
  try { return JSON.parse(localStorage.getItem(KEY) || 'null') } catch { return null }
}

export function saveSession(session) {
  localStorage.setItem(KEY, JSON.stringify(session))
}

export function clearSession() {
  localStorage.removeItem(KEY)
}

const HISTORY_KEY = 'datapilot_history'
export function getHistory() {
  try { return JSON.parse(localStorage.getItem(HISTORY_KEY) || '[]') } catch { return [] }
}
export function saveHistory(item) {
  const history = [item, ...getHistory()].slice(0, 50)
  localStorage.setItem(HISTORY_KEY, JSON.stringify(history))
  return history
}
export function clearHistory() { localStorage.removeItem(HISTORY_KEY) }