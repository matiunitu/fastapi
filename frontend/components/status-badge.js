/**
 * Web Component: <status-badge>
 * Displays a styled status chip (estado) for PQRS or users.
 *
 * Attrs:
 *   status  — text key, e.g. "Pendiente", "Resuelto", "En revisión"
 *   active  — "true" | "false" (optional boolean override for user active state)
 *
 * Usage:
 *   <status-badge status="Pendiente"></status-badge>
 *   <status-badge active="true"></status-badge>
 */
class StatusBadge extends HTMLElement {
  static get observedAttributes() { return ['status', 'active']; }

  connectedCallback()        { this.render(); }
  attributeChangedCallback() { this.render(); }

  render() {
    const active = this.getAttribute('active');
    const status = this.getAttribute('status') ?? '';

    let label, cls;

    // Boolean active/inactive mode
    if (active !== null) {
      const isActive = active === 'true' || active === '1';
      label = isActive ? '✅ Activo' : '❌ Inactivo';
      cls   = isActive ? 'badge-success' : 'badge-danger';
    } else {
      // PQRS status text mode
      const lower = status.toLowerCase();
      if (lower.includes('pend'))    { cls = 'badge-warning'; label = `🟡 ${status}`; }
      else if (lower.includes('res')) { cls = 'badge-success'; label = `✅ ${status}`; }
      else if (lower.includes('rech')){ cls = 'badge-danger';  label = `❌ ${status}`; }
      else if (lower.includes('rev')) { cls = 'badge-info';    label = `🔵 ${status}`; }
      else                            { cls = 'badge-accent';  label = `🔸 ${status || '—'}`; }
    }

    this.innerHTML = `<span class="badge ${cls}" style="font-size:0.78rem;white-space:nowrap">${label}</span>`;
  }
}

customElements.define('status-badge', StatusBadge);
