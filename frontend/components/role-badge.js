/**
 * Web Component: <role-badge>
 * Displays a styled badge for a user role.
 *
 * Attrs: role  (admin | docente | estudiante)
 *
 * Usage:
 *   <role-badge role="admin"></role-badge>
 */
class RoleBadge extends HTMLElement {
  static get observedAttributes() { return ['role']; }

  connectedCallback()        { this.render(); }
  attributeChangedCallback() { this.render(); }

  render() {
    const role = (this.getAttribute('role') ?? '').toLowerCase();

    const cfg = {
      admin:      { label: '👨‍💼 Administrador', cls: 'badge-accent'   },
      docente:    { label: '👨‍🏫 Docente',        cls: 'badge-success'  },
      estudiante: { label: '👨‍🎓 Estudiante',      cls: 'badge-info'    },
    };

    const { label = `🔵 ${role}`, cls = 'badge-warning' } = cfg[role] ?? {};
    this.innerHTML = `<span class="badge ${cls}" style="font-size:0.8rem;padding:4px 10px">${label}</span>`;
  }
}

customElements.define('role-badge', RoleBadge);
