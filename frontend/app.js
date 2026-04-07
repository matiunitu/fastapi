/**
 * app.js — Orquestador principal
 * Exporta: API_BASE_URL, apiCall(), logout()
 */

export const API_BASE_URL = 'http://localhost:8000';

// ─── API helper ────────────────────────────────────────────────────────────────
export async function apiCall(endpoint, method = 'GET', data = null) {
  const token = sessionStorage.getItem('jwt_token');
  const headers = { 'Content-Type': 'application/json', 'Accept': 'application/json' };
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const opts = { method, headers };
  if (data) opts.body = JSON.stringify(data);

  const res = await fetch(`${API_BASE_URL}${endpoint}`, opts);

  if (res.status === 401 || res.status === 403) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail ?? `HTTP ${res.status}`);
  }
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail ?? `Error ${res.status}`);
  }
  return res.json();
}

// ─── Logout ────────────────────────────────────────────────────────────────────
export function logout() {
  sessionStorage.removeItem('jwt_token');
  sessionStorage.removeItem('jwt_user');
  sessionStorage.removeItem('jwt_expires');

  const dashboard = document.getElementById('dashboardShell');
  const login     = document.getElementById('loginScreen');

  dashboard.hidden = true;
  login.hidden     = false;
  login.render?.();

  window.toast?.show('Sesión cerrada', 'info');
}

// ─── Bootstrap ────────────────────────────────────────────────────────────────
function bootstrap() {
  const loginEl  = document.getElementById('loginScreen');
  const dashEl   = document.getElementById('dashboardShell');

  // Escuchar evento de login exitoso
  document.addEventListener('auth-success', e => {
    const { token, user, expiresIn } = e.detail;
    loginEl.hidden  = true;
    dashEl.hidden   = false;

    dashEl.init(user, token, Date.now() + expiresIn * 1000);
  });

  // Restaurar sesión si el token aún no expiró
  const saved      = sessionStorage.getItem('jwt_token');
  const savedUser  = sessionStorage.getItem('jwt_user');
  const savedExp   = parseInt(sessionStorage.getItem('jwt_expires') ?? '0');

  if (saved && savedUser && savedExp > Date.now()) {
    loginEl.hidden  = true;
    dashEl.hidden   = false;
    dashEl.init(JSON.parse(savedUser), saved, savedExp);
  }
}

// Esperar a que los Web Components estén registrados
window.addEventListener('DOMContentLoaded', bootstrap);
