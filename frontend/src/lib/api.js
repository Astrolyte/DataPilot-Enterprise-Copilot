const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

async function parseResponse(response) {
  const text = await response.text()
  let data
  try { data = text ? JSON.parse(text) : {} } catch { data = { detail: text } }
  if (!response.ok) {
    const message = typeof data?.detail === 'string' ? data.detail : 'Something went wrong.'
    throw new Error(message)
  }
  return data
}

export async function login(username, password) {
  const body = new URLSearchParams({ username, password })
  const response = await fetch(`${API_BASE}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body,
  })
  return parseResponse(response)
}

export function googleLoginUrl() {
  return `${API_BASE}/auth/google/login`
}

export async function queryData(question, token) {
  const response = await fetch(`${API_BASE}/query`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ question }),
  })
  return parseResponse(response)
}

export async function healthCheck() {
  const response = await fetch(`${API_BASE}/health`)
  return response.ok
}

export { API_BASE }