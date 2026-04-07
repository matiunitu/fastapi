/**
 * Web Component: <login-screen>
 * Renderiza el formulario de login y emite el evento 'auth-success'
 * con { token, user } cuando el JWT es obtenido correctamente.
 */
import { API_BASE_URL } from '../app.js';

class LoginScreen extends HTMLElement {
  connectedCallback() {
    this.render();
    this.querySelector('#loginForm').addEventListener('submit', e => this._onSubmit(e));
  }

  render() {
    this.innerHTML = `
      <div class="login-bg">
        <div class="login-card">
          <div class="login-logo">
            <svg width="52" height="52" viewBox="0 0 52 52" fill="none">
              <rect width="52" height="52" rx="14" fill="rgba(108,99,255,0.15)"/>
              <rect x="10" y="10" width="32" height="32" rx="8" fill="rgba(108,99,255,0.25)" stroke="rgba(108,99,255,0.6)" stroke-width="1.5"/>
              <path d="M20 26l5 5 10-10" stroke="#8b85ff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <h1>Sistema PQRS</h1>
            <p>Gestión Universitaria — v2.0</p>
          </div>

          <form id="loginForm" autocomplete="off">
            <div class="form-group">
              <label for="lg-username">Usuario</label>
              <input id="lg-username" type="text" placeholder="ej: nelson" required />
            </div>
            <div class="form-group">
              <label for="lg-password">Contraseña</label>
              <input id="lg-password" type="password" placeholder="••••••••" required />
            </div>

            <button class="btn btn-primary" style="width:100%;justify-content:center;margin-top:8px" id="loginBtn" type="submit">
              Iniciar sesión
            </button>
          </form>

          <div class="demo-hint">
            <strong>🔑 Credenciales demo</strong>
            <span>Usuario: <b>nelson</b> &nbsp;|&nbsp; Contraseña: <b>1234</b></span>
            <span style="color:var(--text-muted);font-size:0.75rem">Rol: admin — Token válido 60 min</span>
          </div>
        </div>
      </div>
    `;
  }

  async _onSubmit(e) {
    e.preventDefault();
    const btn = this.querySelector('#loginBtn');
    const username = this.querySelector('#lg-username').value.trim();
    const password = this.querySelector('#lg-password').value;

    btn.disabled = true;
    btn.textContent = 'Entrando…';

    try {
      const res = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || `Error ${res.status}`);
      }

      const data = await res.json();

      // Guardar en sessionStorage (temporal — se borra al cerrar pestaña)
      sessionStorage.setItem('jwt_token',  data.access_token);
      sessionStorage.setItem('jwt_user',   JSON.stringify(data.user));
      sessionStorage.setItem('jwt_expires', Date.now() + data.expires_in * 1000);

      this.dispatchEvent(new CustomEvent('auth-success', {
        bubbles: true,
        detail: { token: data.access_token, user: data.user, expiresIn: data.expires_in },
      }));
    } catch (err) {
      window.toast?.show(err.message, 'error');
    } finally {
      btn.disabled = false;
      btn.textContent = 'Iniciar sesión';
    }
  }
}

customElements.define('login-screen', LoginScreen);
