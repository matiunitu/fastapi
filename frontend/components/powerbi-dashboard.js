/**
 * Web Component: <powerbi-dashboard>
 * Embeds the Power BI report via iframe.
 * Usage: <powerbi-dashboard></powerbi-dashboard>
 */
class PowerBiDashboard extends HTMLElement {
  connectedCallback() {
    this.render();
  }

  render() {
    this.innerHTML = `
      <div class="page-header">
        <h2>📊 Tablero de Analítica — Power BI</h2>
        <p>Dashboard interactivo conectado a la base de datos Neon PostgreSQL en tiempo real.</p>
      </div>
      <div class="card" style="padding:0;overflow:hidden;border-radius:var(--radius)">
        <div style="
          background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
          padding: 16px 20px;
          display: flex;
          align-items: center;
          gap: 10px;
          border-bottom: 1px solid var(--border);
        ">
          <span style="font-size:1.4rem">📈</span>
          <div>
            <div style="font-weight:600;color:#fff;font-size:0.95rem">Gráficas PQRS</div>
            <div style="color:#a5b4fc;font-size:0.78rem">Sistema de Gestión Universitaria — Power BI Service</div>
          </div>
          <span style="margin-left:auto;background:#10b981;color:#fff;font-size:0.7rem;padding:3px 8px;border-radius:99px;font-weight:600">● LIVE</span>
        </div>
        <div style="width:100%;background:#0f0f17;min-height:541px;display:flex;align-items:center;justify-content:center;">
          <iframe
            title="GraficasPqrs"
            width="100%"
            height="541"
            src="https://app.powerbi.com/reportEmbed?reportId=3cb8fa70-a950-4aa0-9d91-c9cbc16e91e1&autoAuth=true&ctid=740be6bd-fd36-470e-94d9-0f0c777fadb9"
            frameborder="0"
            allowFullScreen="true"
            style="display:block;width:100%;min-height:541px;border:none;"
          ></iframe>
        </div>
      </div>
    `;
  }
}

customElements.define('powerbi-dashboard', PowerBiDashboard);
