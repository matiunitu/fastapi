/**
 * Web Component: <stat-card>
 * Attrs: label, value, trend, icon
 */
class StatCard extends HTMLElement {
  static get observedAttributes() { return ['label','value','trend','icon']; }

  connectedCallback()              { this.render(); }
  attributeChangedCallback()       { this.render(); }

  render() {
    const label = this.getAttribute('label') ?? '—';
    const value = this.getAttribute('value') ?? '0';
    const trend = this.getAttribute('trend') ?? '';
    const icon  = this.getAttribute('icon')  ?? '📊';

    this.className = 'stat-box';
    this.innerHTML = `
      <div class="label">${icon} ${label}</div>
      <div class="value">${value}</div>
      ${trend ? `<div class="trend">${trend}</div>` : ''}
    `;
  }
}

customElements.define('stat-card', StatCard);
