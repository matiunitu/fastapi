/**
 * Web Component: <toast-notification>
 * Uso global: window.toast.show('mensaje', 'success'|'error'|'warning'|'info')
 */
class ToastNotification extends HTMLElement {
  connectedCallback() {
    this.className = 'toast-container';
    window.toast = this;
  }

  show(message, type = 'info', duration = 4000) {
    const icons = { success: '✅', error: '❌', warning: '⚠️', info: 'ℹ️' };

    const el = document.createElement('div');
    el.className = `toast ${type}`;
    el.innerHTML = `
      <span class="toast-icon">${icons[type] ?? '🔔'}</span>
      <span class="toast-msg">${message}</span>
      <button class="toast-close" title="Cerrar">✕</button>
    `;
    el.querySelector('.toast-close').onclick = () => el.remove();
    this.appendChild(el);

    setTimeout(() => el.remove(), duration);
  }
}

customElements.define('toast-notification', ToastNotification);
