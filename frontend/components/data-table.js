/**
 * Web Component: <data-table>
 *
 * Propiedades JS (no atributos para evitar serializar arrays):
 *   table.columns = [{ key, label, render? }]
 *   table.rows    = [ ...objects ]
 *   table.actions = [{ label, cls, onClick(row) }]
 *   table.emptyMsg = 'Sin datos'
 */
class DataTable extends HTMLElement {
  constructor() {
    super();
    this._columns  = [];
    this._rows     = [];
    this._actions  = [];
    this._emptyMsg = 'Sin registros';
  }

  set columns(v)  { this._columns = v;  this.render(); }
  set rows(v)     { this._rows = v;     this.render(); }
  set actions(v)  { this._actions = v;  this.render(); }
  set emptyMsg(v) { this._emptyMsg = v; this.render(); }

  connectedCallback() { this.render(); }

  render() {
    const hasActions = this._actions.length > 0;

    const headers = this._columns.map(c =>
      `<th>${c.label}</th>`
    ).join('') + (hasActions ? '<th>Acciones</th>' : '');

    const rows = this._rows.length === 0
      ? `<tr><td colspan="${this._columns.length + (hasActions ? 1 : 0)}" style="text-align:center;padding:32px;color:var(--text-muted)">${this._emptyMsg}</td></tr>`
      : this._rows.map(row => {
          const cells = this._columns.map(col => {
            const raw = row[col.key] ?? '—';
            const val = col.render ? col.render(raw, row) : raw;
            return `<td>${val}</td>`;
          }).join('');

          const actBtns = this._actions.map((act, i) => {
            const label = typeof act.label === 'function' ? act.label(row) : act.label;
            const cls   = typeof act.cls   === 'function' ? act.cls(row)   : (act.cls ?? 'btn-ghost');
            const rowIdx = this._rows.indexOf(row);
            return `<button class="btn btn-sm ${cls}" data-idx="${rowIdx}" data-act="${i}">${label}</button>`;
          }).join('');

          return `<tr>${cells}${hasActions ? `<td><div class="actions">${actBtns}</div></td>` : ''}</tr>`;
        }).join('');

    this.innerHTML = `
      <div style="overflow-x:auto">
        <table class="data-table">
          <thead><tr>${headers}</tr></thead>
          <tbody>${rows}</tbody>
        </table>
      </div>
    `;

    // Bind action buttons
    this.querySelectorAll('[data-act]').forEach(btn => {
      btn.addEventListener('click', () => {
        const actIdx = parseInt(btn.dataset.act);
        const rowIdx = parseInt(btn.dataset.idx);
        const row = this._rows[rowIdx];
        if (row) {
          this._actions[actIdx]?.onClick(row);
        }
      });
    });
  }
}

customElements.define('data-table', DataTable);
