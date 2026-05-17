const API_URL = 'http://127.0.0.1:8000/api';

function getToken() {
  return localStorage.getItem('access');
}

function getRefresh() {
  return localStorage.getItem('refresh');
}

function setTokens(access, refresh) {
  localStorage.setItem('access', access);
  localStorage.setItem('refresh', refresh);
}

function clearTokens() {
  localStorage.removeItem('access');
  localStorage.removeItem('refresh');
}

async function refreshToken() {
  const refresh = getRefresh();
  if (!refresh) {
    redirectToLogin();
    return null;
  }

  const response = await fetch(`${API_URL}/token/refresh/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh })
  });

  if (response.ok) {
    const data = await response.json();
    localStorage.setItem('access', data.access);
    return data.access;
  } else {
    clearTokens();
    redirectToLogin();
    return null;
  }
}

async function apiFetch(endpoint, options = {}) {
  let token = getToken();

  const defaultHeaders = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  };

  let response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: { ...defaultHeaders, ...options.headers }
  });

  // Token expirado — tenta renovar
  if (response.status === 401) {
    token = await refreshToken();
    if (!token) return null;

    response = await fetch(`${API_URL}${endpoint}`, {
      ...options,
      headers: { ...defaultHeaders, Authorization: `Bearer ${token}` }
    });
  }

  return response;
}

function redirectToLogin() {
  window.location.href = 'index.html';
}

function checkAuth() {
  if (!getToken()) {
    redirectToLogin();
  }
}