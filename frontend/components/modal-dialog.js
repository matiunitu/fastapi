/**
 * Web Component: <modal-dialog>
 * Reusable modal with open/close API.
 *
 * Usage:
 *   const modal = document.createElement('modal-dialog');
 *   modal.setTitle('Crear usuario');
 *   modal.setContent('<p>HTML aquí</p>');
 *   modal.setActions([{ label: 'Guardar', cls: 'btn-primary', onClick: () => {} }]);
 *   document.body.appendChild(modal);
 *   modal.open();
 *
 * Events:
 *   'modal-closed' — dispatched when modal is closed
 */
class ModalDialog extends HTMLElement {
  connectedCallback() {
    this._title   = '';
    this._content = '';
    this._actions = [];
    this._build();
  }

  _build() {
    this.innerHTML = `
      <div class="modal-overlay" id="modalOverlay" style="
        display:none;position:fixed;inset:0;z-index:9999;
        background:rgba(0,0,0,0.6);backdrop-filter:blur(4px);
        align-items:center;justify-content:center;
      ">
        <div class="modal-box" style="
          background:var(--bg-card);
          border:1px solid var(--border);
          border-radius:var(--radius);
          box-shadow:0 20px 60px rgba(0,0,0,0.5);
          width:90%;max-width:520px;
          max-height:90vh;overflow-y:auto;
          display:flex;flex-direction:column;
          animation:fadeSlideIn 0.2s ease;
        ">
          <div style="
            display:flex;align-items:center;justify-content:space-between;
            padding:18px 22px;border-bottom:1px solid var(--border);
          ">
            <h3 id="modalTitle" style="margin:0;font-size:1rem;color:var(--text-primary)"></h3>
            <button id="modalClose" class="btn btn-ghost btn-sm" style="padding:4px 10px;font-size:1.1rem" title="Cerrar">&times;</button>
          </div>
          <div id="modalContent" style="padding:22px;flex:1"></div>
          <div id="modalFooter" style="
            padding:14px 22px;border-top:1px solid var(--border);
            display:flex;gap:10px;justify-content:flex-end;flex-wrap:wrap;
          "></div>
        </div>
      </div>
    `;

    this.querySelector('#modalClose').onclick = () => this.close();
    this.querySelector('#modalOverlay').addEventListener('click', e => {
      if (e.target.id === 'modalOverlay') this.close();
    });
  }

  setTitle(t)   { this._title = t;   if (this.querySelector('#modalTitle'))   this.querySelector('#modalTitle').textContent = t; }
  setContent(c) { this._content = c; if (this.querySelector('#modalContent')) this.querySelector('#modalContent').innerHTML = c; }

  setActions(actions = []) {
    this._actions = actions;
    const footer = this.querySelector('#modalFooter');
    if (!footer) return;
    footer.innerHTML = '';
    actions.forEach(a => {
      const btn = document.createElement('button');
      btn.className = `btn ${a.cls ?? 'btn-ghost'}`;
      btn.textContent = a.label;
      btn.onclick = () => a.onClick?.();
      footer.appendChild(btn);
    });
  }

  open() {
    const overlay = this.querySelector('#modalOverlay');
    if (overlay) { overlay.style.display = 'flex'; }
  }

  close() {
    const overlay = this.querySelector('#modalOverlay');
    if (overlay) { overlay.style.display = 'none'; }
    this.dispatchEvent(new CustomEvent('modal-closed', { bubbles: true }));
  }
}

customElements.define('modal-dialog', ModalDialog);
