/**
 * Web Component: <empty-state>
 * Shows a friendly empty state placeholder with icon, title and message.
 *
 * Attrs:
 *   icon    — emoji or text icon (default 📭)
 *   title   — main heading   (default "Sin registros")
 *   message — subtitle text  (default "No hay datos disponibles")
 *   action  — label for optional CTA button
 *
 * Events:
 *   'empty-action' — dispatched when CTA button is clicked
 *
 * Usage:
 *   <empty-state icon="📋" title="Sin PQRS" message="Crea tu primera solicitud." action="Nueva PQRS"></empty-state>
 */
class EmptyState extends HTMLElement {
  static get observedAttributes() { return ['icon', 'title', 'message', 'action']; }

  connectedCallback()        { this.render(); }
  attributeChangedCallback() { this.render(); }

  render() {
    const icon    = this.getAttribute('icon')    ?? '📭';
    const title   = this.getAttribute('title')   ?? 'Sin registros';
    const message = this.getAttribute('message') ?? 'No hay datos disponibles.';
    const action  = this.getAttribute('action')  ?? '';

    this.innerHTML = `
      <div style="
        display:flex;flex-direction:column;align-items:center;justify-content:center;
        padding:48px 24px;text-align:center;color:var(--text-muted);
      ">
        <div style="font-size:3rem;margin-bottom:16px;opacity:0.7">${icon}</div>
        <h3 style="margin:0 0 8px;font-size:1.1rem;color:var(--text-secondary)">${title}</h3>
        <p style="margin:0 0 20px;font-size:0.875rem;max-width:300px">${message}</p>
        ${action
          ? `<button class="btn btn-primary btn-sm" id="emptyAction">${action}</button>`
          : ''}
      </div>
    `;

    if (action) {
      this.querySelector('#emptyAction')?.addEventListener('click', () => {
        this.dispatchEvent(new CustomEvent('empty-action', { bubbles: true }));
      });
    }
  }
}

customElements.define('empty-state', EmptyState);
