/**
 * Web Component: <app-dashboard>
 * Shell principal: navbar + sidebar + main content area.
 * Se activa cuando el usuario está autenticado.
 */
import { apiCall, logout } from '../app.js';

// ── Configuración de roles y sus menús ────────────────────────────────────────
const ROLE_CONFIG = {
  admin: {
    label: 'Administrador',
    icon:  '👨‍💼',
    color: '#6c63ff',
    menu: [
      { id: 'dashboard',     label: 'Panel Principal',   icon: '📊' },
      { id: 'usuarios',      label: 'Usuarios',           icon: '👥' },
      { id: 'pqrs',          label: 'PQRS',               icon: '📋' },
      { id: 'roles',         label: 'Roles & Permisos',   icon: '🔑' },
      { id: 'reportes',      label: 'Reportes',           icon: '📈' },
      { id: 'powerbi',       label: 'Dashboard BI',       icon: '📊' },
    ],
  },
  docente: {
    label: 'Docente',
    icon:  '👨‍🏫',
    color: '#10b981',
    menu: [
      { id: 'dashboard',     label: 'Panel Principal',   icon: '📊' },
      { id: 'nueva-pqrs',    label: 'Nueva PQRS',         icon: '📝' },
      { id: 'mis-pqrs',      label: 'Mis PQRS',           icon: '📋' },
      { id: 'perfil',        label: 'Mi Perfil',          icon: '👤' },
    ],
  },
  estudiante: {
    label: 'Estudiante',
    icon:  '👨‍🎓',
    color: '#3b82f6',
    menu: [
      { id: 'dashboard',     label: 'Panel Principal',   icon: '📊' },
      { id: 'nueva-pqrs',    label: 'Nueva PQRS',         icon: '📝' },
      { id: 'mis-pqrs',      label: 'Mis PQRS',           icon: '📋' },
      { id: 'perfil',        label: 'Mi Perfil',          icon: '👤' },
    ],
  },
};

// ── Permisos por rol ───────────────────────────────────────────────────────────
const ROLE_PERMISSIONS = {
  admin: [
    'usuarios:read','usuarios:write','usuarios:delete',
    'pqrs:read','pqrs:write','pqrs:delete',
    'roles:read','roles:write',
    'reportes:read','configuracion:read','configuracion:write',
  ],
  docente: [
    'pqrs:read','pqrs:write',
    'respuestas:read','respuestas:write',
    'perfil:read','perfil:write',
  ],
  estudiante: [
    'pqrs:read','pqrs:write',
    'perfil:read','perfil:write',
  ],
};

class AppDashboard extends HTMLElement {
  connectedCallback() {
    this._user    = null;
    this._token   = null;
    this._section = 'dashboard';
    this._timer   = null;
  }

  /** Llamado desde app.js después del login */
  init(user, token, expiresAt) {
    this._user      = user;
    this._token     = token;
    this._expiresAt = expiresAt;
    this.render();
    this._startTimer();
    this._navigate('dashboard');
  }

  render() {
    const rol    = (this._user?.rol ?? 'estudiante').toLowerCase();
    const cfg    = ROLE_CONFIG[rol] ?? ROLE_CONFIG.estudiante;
    const initials = (this._user?.nombre ?? '?').slice(0,2).toUpperCase();

    const menuItems = cfg.menu.map(m => `
      <button class="nav-item" data-section="${m.id}" id="nav-${m.id}">
        <span class="icon">${m.icon}</span> ${m.label}
      </button>
    `).join('');

    this.innerHTML = `
      <div class="dashboard-layout">

        <!-- Navbar -->
        <nav class="app-navbar">
          <div class="navbar-brand">
            <span class="dot"></span>
            Sistema PQRS
          </div>
          <div class="navbar-user">
            <span class="token-timer" id="timerBadge">⏱ 60:00</span>
            <div class="user-avatar" title="${this._user?.nombre}">${initials}</div>
            <span style="font-size:0.85rem">
              ${this._user?.nombre}
              <span class="badge badge-accent" style="margin-left:6px">${cfg.label}</span>
            </span>
            <button class="btn btn-ghost btn-sm" id="logoutBtn">🚪 Salir</button>
          </div>
        </nav>

        <!-- Sidebar -->
        <aside class="app-sidebar">
          <div class="sidebar-label">Menú</div>
          <div id="sidebarMenu">${menuItems}</div>
        </aside>

        <!-- Content -->
        <main class="app-main" id="mainContent">
          <div class="animate-in" id="pageContent"></div>
        </main>
      </div>

      <!-- Toast global -->
      <toast-notification></toast-notification>
    `;

    // Events
    this.querySelector('#logoutBtn').onclick = () => logout();
    this.querySelectorAll('.nav-item').forEach(btn => {
      btn.onclick = () => this._navigate(btn.dataset.section);
    });
  }

  _navigate(section) {
    this._section = section;

    // Active states
    this.querySelectorAll('.nav-item').forEach(b => b.classList.remove('active'));
    this.querySelector(`#nav-${section}`)?.classList.add('active');

    // Render page
    const el = this.querySelector('#pageContent');
    if (el) {
      el.className = 'animate-in';
      el.innerHTML = '';
      this._renderSection(section, el);
    }
  }

  _renderSection(id, target) {
    switch(id) {
      case 'dashboard':   this._pageDashboard(target);  break;
      case 'usuarios':    this._pageUsuarios(target);   break;
      case 'pqrs':        this._pagePQRS(target);       break;
      case 'roles':       this._pageRoles(target);      break;
      case 'reportes':    this._pageReportes(target);   break;
      case 'powerbi':     this._pagePowerBI(target);    break;
      case 'nueva-pqrs':  this._pageNuevaPQRS(target);  break;
      case 'mis-pqrs':    this._pageMisPQRS(target);    break;
      case 'perfil':      this._pagePerfil(target);     break;
      default:            target.innerHTML = '<empty-state icon="🚧" title="Sección no encontrada" message="Esta sección aún no está disponible."></empty-state>';
    }
  }

  // ── DASHBOARD ──────────────────────────────────────────────────────────────
  async _pageDashboard(el) {
    const rol = (this._user?.rol ?? 'estudiante').toLowerCase();
    const cfg = ROLE_CONFIG[rol] ?? ROLE_CONFIG.estudiante;

    el.innerHTML = `
      <div class="page-header">
        <h2>${cfg.icon} Bienvenido, ${this._user?.nombre}</h2>
        <p>Rol: <strong>${cfg.label}</strong> — ${new Date().toLocaleDateString('es-CO', {weekday:'long',year:'numeric',month:'long',day:'numeric'})}</p>
      </div>
      <div class="stats-grid" id="statsGrid">
        <stat-card label="Cargando…" value="…" icon="🔄"></stat-card>
      </div>
      <div id="jwtInfo"></div>
    `;

    // Cargar stats reales
    try {
      const [usuarios, pqrs, roles] = await Promise.all([
        apiCall('/usuarios/').catch(() => []),
        apiCall('/pqrs/').catch(()  => []),
        apiCall('/roles/').catch(()  => []),
      ]);

      const statsGrid = el.querySelector('#statsGrid');
      statsGrid.innerHTML = `
        <stat-card label="Usuarios"      value="${usuarios.length}" icon="👥" trend="↑ activos"></stat-card>
        <stat-card label="PQRS totales"  value="${pqrs.length}"    icon="📋" trend="registradas"></stat-card>
        <stat-card label="Roles"         value="${roles.length}"   icon="🔑" trend="configurados"></stat-card>
        <stat-card label="Estado BD"     value="✅"              icon="🟢" trend="Neon PostgreSQL"></stat-card>
      `;

      // JWT info
      const jwtEl = el.querySelector('#jwtInfo');
      const payload = this._decodeToken();
      if (payload) {
        const exp = new Date(payload.exp * 1000).toLocaleTimeString('es-CO');
        jwtEl.innerHTML = `
          <div class="jwt-panel">
            <h3>🔐 Token JWT activo</h3>
            <p style="margin-top:6px;font-size:0.85rem">Expira a las <strong>${exp}</strong> — temporal (sesión)</p>
            <pre>${JSON.stringify({ sub: payload.sub, nombre: payload.nombre, rol: payload.rol, exp: new Date(payload.exp*1000).toISOString() }, null, 2)}</pre>
          </div>
        `;
      }
    } catch(e) {
      console.error(e);
    }
  }

  // ── USUARIOS ───────────────────────────────────────────────────────────────
  async _pageUsuarios(el) {
    el.innerHTML = `
      <div class="page-header">
        <h2>👥 Gestión de Usuarios</h2>
        <button class="btn btn-primary btn-sm" id="newUserBtn">+ Nuevo usuario</button>
      </div>
      <div class="card">
        <div id="usuariosTableWrap">
          <p style="color:var(--text-muted);text-align:center;padding:24px">Cargando…</p>
        </div>
      </div>
    `;

    el.querySelector('#newUserBtn').onclick = () => this._formUsuario(el);

    const wrap = el.querySelector('#usuariosTableWrap');
    try {
      const rows = await apiCall('/usuarios/');
      const table = document.createElement('data-table');
      table.columns = [
        { key: 'nombre',     label: 'Nombre' },
        { key: 'tipo_documento', label: 'Tipo Doc.' },
        { key: 'documento',  label: 'Documento' },
        { key: 'correo',     label: 'Correo' },
        { key: 'telefono',   label: 'Teléfono' },
        { key: 'rol',        label: 'Rol',
          render: v => `<role-badge role="${(v??'').toLowerCase()}"></role-badge>` },
        { key: 'activo',     label: 'Estado',
          render: v => `<status-badge active="${v===true||v==='true'||v==1?'true':'false'}"></status-badge>` },
        { key: 'created_at', label: 'Creado',
          render: v => v ? new Date(v).toLocaleDateString('es-CO') : '—' },
      ];
      table.actions = [
        { label: '✏️ Editar',   cls: 'btn-ghost', onClick: row => this._formUsuario(el, row) },
        { label: '🗑 Eliminar', cls: 'btn-danger', onClick: row => this._deleteUsuario(row.id_usuario, el) },
      ];
      table.rows     = rows;
      table.emptyMsg = 'Sin usuarios registrados';
      wrap.innerHTML = '';
      wrap.appendChild(table);
    } catch(e) {
      wrap.innerHTML = `<p style="color:var(--danger);text-align:center;padding:20px">${e.message}</p>`;
    }
  }

  _formUsuario(container, row = null) {
    const isEdit = !!row;
    const section = container.querySelector('#mainSection') ?? container;
    section.innerHTML = `
      <div class="page-header">
        <h2>${isEdit ? '✏️ Editar' : '➕ Nuevo'} Usuario</h2>
        <button class="btn btn-ghost btn-sm" id="backBtn">← Volver</button>
      </div>
      <div class="card" style="max-width:560px">
        <form id="userForm">
          <div class="form-group"><label>Nombre</label><input id="f-nombre" value="${row?.nombre??''}" required /></div>
          <div class="form-group"><label>Documento</label><input id="f-documento" value="${row?.documento??''}" required /></div>
          <div class="form-group"><label>Correo</label><input id="f-correo" type="email" value="${row?.correo??''}" required /></div>
          <div class="form-group"><label>Teléfono</label><input id="f-telefono" value="${row?.telefono??''}" required /></div>
          <div class="form-group"><label>Estado (1=activo, 0=inactivo)</label>
            <select id="f-estado">
              <option value="1" ${!isEdit||row?.estado==1?'selected':''}>1 — Activo</option>
              <option value="0" ${row?.estado==0?'selected':''}>0 — Inactivo</option>
            </select>
          </div>
          <div style="display:flex;gap:10px;margin-top:8px">
            <button type="submit" class="btn btn-primary">${isEdit?'Actualizar':'Crear'}</button>
            <button type="button" class="btn btn-ghost" id="cancelBtn">Cancelar</button>
          </div>
        </form>
      </div>
    `;

    const back = () => this._pageUsuarios(container);
    section.querySelector('#backBtn').onclick   = back;
    section.querySelector('#cancelBtn').onclick = back;

    section.querySelector('#userForm').addEventListener('submit', async e => {
      e.preventDefault();
      const data = {
        nombre:    section.querySelector('#f-nombre').value,
        documento: section.querySelector('#f-documento').value,
        correo:    section.querySelector('#f-correo').value,
        telefono:  section.querySelector('#f-telefono').value,
        estado:    parseInt(section.querySelector('#f-estado').value),
        id_rol:      row?.id_rol ?? 3,
        id_programa: row?.id_programa ?? 1,
      };
      try {
        if (isEdit) await apiCall(`/usuarios/${row.id_usuario}`, 'PUT', data);
        else        await apiCall('/usuarios/', 'POST', data);
        window.toast?.show(isEdit ? 'Usuario actualizado' : 'Usuario creado', 'success');
        this._pageUsuarios(container);
      } catch(err) { window.toast?.show(err.message, 'error'); }
    });
  }

  async _deleteUsuario(id, el) {
    if (!confirm('¿Eliminar este usuario?')) return;
    try {
      await apiCall(`/usuarios/${id}`, 'DELETE');
      window.toast?.show('Usuario eliminado', 'success');
      this._pageUsuarios(el);
    } catch(e) { window.toast?.show(e.message, 'error'); }
  }

  // ── PQRS (Admin) ────────────────────────────────────────────────────────────
  async _pagePQRS(el) {
    el.innerHTML = `
      <div class="page-header">
        <h2>📋 Gestión de PQRS</h2>
        <p>Administra, cambia estado y activa/inactiva cualquier solicitud.</p>
      </div>
      <div class="card">
        <div id="pqrsWrap"><p style="text-align:center;padding:24px;color:var(--text-muted)">Cargando…</p></div>
      </div>
      <modal-dialog id="pqrsModal"></modal-dialog>
    `;
    await this._loadPqrsTable(el);
  }

  async _loadPqrsTable(el) {
    const wrap = el.querySelector('#pqrsWrap');
    try {
      const [rows, estados] = await Promise.all([
        apiCall('/pqrs/'),
        apiCall('/estados/').catch(() => []),
      ]);

      // Build estado map id→nombre and deduplicate
      const estadoMap = {};
      const uniqueEstados = [];
      const seenEstados = new Set();
      (estados || []).forEach(e => { 
        estadoMap[e.id_estado] = e.nombre_estado; 
        if (!seenEstados.has(e.nombre_estado) && e.nombre_estado) {
          uniqueEstados.push(e);
          seenEstados.add(e.nombre_estado);
        }
      });
      // Save uniqueEstados on el for modal usage
      el._uniqueEstados = uniqueEstados;

      const table = document.createElement('data-table');
      table.columns = [
        { key: 'radicado',      label: 'Radicado' },
        { key: 'descripcion',   label: 'Descripción',
          render: v => `<span title="${v??''}">${(v??'').slice(0,45)}${(v??'').length>45?'…':''}</span>` },
        { key: 'id_estado',     label: 'Estado PQRS',
          render: v => {
            const nombre = estadoMap[v] ?? (v ? `ID ${v}` : 'Sin estado');
            return `<status-badge status="${nombre}"></status-badge>`;
          }},
        { key: 'estado',        label: 'Activo',
          render: v => `<status-badge active="${v==1||v===true?'true':'false'}"></status-badge>` },
        { key: 'fecha_creacion',label: 'Fecha',
          render: v => v ? new Date(v).toLocaleDateString('es-CO') : '—' },
        { key: 'updated_at',    label: 'Actualizado',
          render: v => v ? new Date(v).toLocaleString('es-CO') : '—' },
      ];
      table.actions = [
        { 
          label: '⚙️ Gestionar',  
          cls: 'btn-primary btn-sm',  
          onClick: row => this._modalEditPqrs(el, row, el._uniqueEstados) 
        }
      ];
      table.rows     = rows;
      table.emptyMsg = 'Sin PQRS registradas';
      wrap.innerHTML = '';
      wrap.appendChild(table);
    } catch(e) {
      wrap.innerHTML = `<p style="color:var(--danger);padding:20px">${e.message}</p>`;
    }
  }

  async _modalEditPqrs(el, row, estados = []) {
    const modal = el.querySelector('#pqrsModal');
    if (!modal) return;

    const estadoOpts = estados.map(e =>
      `<option value="${e.id_estado}" ${e.id_estado == row.id_estado ? 'selected' : ''}>${e.nombre_estado}</option>`
    ).join('');

    modal.setTitle(`✏️ Editar PQRS — ${row.radicado}`);
    modal.setContent(`
      <div class="form-group">
        <label>Radicado</label>
        <input id="m-radicado" value="${row.radicado ?? ''}" />
      </div>
      <div class="form-group">
        <label>Descripción</label>
        <textarea id="m-desc" rows="3">${row.descripcion ?? ''}</textarea>
      </div>
      <div class="form-group">
        <label>Estado del PQRS</label>
        <select id="m-estado">
          ${estadoOpts || '<option value="">Sin estados</option>'}
        </select>
      </div>
      <div class="form-group">
        <label>Activo en el sistema</label>
        <select id="m-activo">
          <option value="1" ${row.estado==1||row.estado===true?'selected':''}>Sí — Activo</option>
          <option value="0" ${row.estado==0||row.estado===false?'selected':''}>No — Inactivo</option>
        </select>
      </div>
    `);
    modal.setActions([
      { label: 'Guardar cambios', cls: 'btn-primary', onClick: async () => {
        const cont    = modal.querySelector('#modalContent') ?? modal;
        const radicado  = cont.querySelector('#m-radicado').value;
        const desc      = cont.querySelector('#m-desc').value;
        const id_estado = parseInt(cont.querySelector('#m-estado').value) || row.id_estado;
        const activo    = parseInt(cont.querySelector('#m-activo').value);

        try {
          await apiCall(`/pqrs/${row.id_pqrs}`, 'PUT', {
            radicado,
            descripcion: desc,
            id_estado,
            id_dependencia: row.id_dependencia,
            id_tipospqrs:   row.id_tipospqrs,
            id_prioridad:   row.id_prioridad,
          });
          // Patch estado activo separately
          await apiCall(`/pqrs/${row.id_pqrs}/estado`, 'PATCH', { estado: activo });
          modal.close();
          window.toast?.show('PQRS actualizado correctamente', 'success');
          await this._loadPqrsTable(el);
        } catch(err) { window.toast?.show(err.message, 'error'); }
      }},
      { label: 'Cancelar', cls: 'btn-ghost', onClick: () => modal.close() },
    ]);
    modal.open();
  }

  async _toggleActivoPqrs(row, el) {
    const nuevoEstado = (row.estado==1||row.estado===true) ? 0 : 1;
    const msg = nuevoEstado === 1 ? 'activar' : 'desactivar';
    if (!confirm(`¿Deseas ${msg} este PQRS?`)) return;
    try {
      await apiCall(`/pqrs/${row.id_pqrs}/estado`, 'PATCH', { estado: nuevoEstado });
      window.toast?.show(`PQRS ${nuevoEstado===1?'activado':'desactivado'}`, 'success');
      await this._loadPqrsTable(el);
    } catch(e) { window.toast?.show(e.message, 'error'); }
  }


  // ── ROLES & PERMISOS ────────────────────────────────────────────────────────
  _pageRoles(el) {
    const rolesData = [
      { nombre: 'admin',      label: 'Administrador', icon: '👨‍💼', color: '#6c63ff',
        desc: 'Control total del sistema: usuarios, PQRS, configuración y reportes.' },
      { nombre: 'docente',    label: 'Docente',        icon: '👨‍🏫', color: '#10b981',
        desc: 'Puede crear y gestionar PQRS propias y responder solicitudes.' },
      { nombre: 'estudiante', label: 'Estudiante',     icon: '👨‍🎓', color: '#3b82f6',
        desc: 'Puede consultar y crear sus propias PQRS únicamente.' },
    ];

    const cards = rolesData.map(r => {
      const perms = ROLE_PERMISSIONS[r.nombre] ?? [];
      const permChips = perms.map(p => `<li>${p}</li>`).join('');
      return `
        <div class="role-card">
          <div class="role-name">${r.icon} ${r.label} <span class="badge badge-accent">${r.nombre}</span></div>
          <div class="role-desc">${r.desc}</div>
          <ul class="perm-list">${permChips}</ul>
        </div>
      `;
    }).join('');

    el.innerHTML = `
      <div class="page-header">
        <h2>🔑 Roles y Permisos</h2>
        <p>El sistema tiene 3 roles base — controlados con JWT. El token incluye el campo <code>rol</code>.</p>
      </div>
      <div class="role-grid">${cards}</div>
      <div class="jwt-panel" style="margin-top:24px">
        <h3>📐 Fundamentos de Roles</h3>
        <p style="margin-top:8px;font-size:0.875rem">
          Cada endpoint protegido usa el decorador <code>require_role()</code> o <code>require_permission()</code>
          del módulo <code>auth_deps.py</code>. El rol viaja <strong>dentro del JWT</strong> — sin consultar la BD
          en cada request.
        </p>
        <pre>{
  "sub":        "1",
  "nombre":     "nelson",
  "rol":        "admin",
  "id_usuario": 1,
  "exp":        1712345678   ← expira en 60 min
}</pre>
      </div>
    `;
  }

  // ── REPORTES ────────────────────────────────────────────────────────────────
  _pageReportes(el) {
    el.innerHTML = `
      <div class="page-header">
        <h2>📈 Reportes</h2>
        <p>Datos exportables y conexión a Power BI</p>
      </div>
      <div class="card" style="margin-bottom:20px">
        <div class="card-header"><h3>🔗 Cadena de conexión PostgreSQL</h3></div>
        <p style="margin-bottom:12px;font-size:0.875rem">Usa estos datos en Power BI Desktop → Obtener datos → PostgreSQL:</p>
        <pre style="font-size:0.78rem;background:var(--bg-base);padding:14px;border-radius:6px;border:1px solid var(--border);color:#a5f3fc">Servidor: ep-fragrant-glitter-aig2qu6i-pooler.c-4.us-east-1.aws.neon.tech
Puerto:   5432
BD:       pqrsdb
Usuario:  neondb_owner
SSL:      require

Vistas recomendadas:
  - vista_pqrs
  - vista_usuarios
  - vista_seguimiento
  - vista_historial</pre>
        <p style="margin-top:12px;font-size:0.8rem;color:var(--text-muted)">👆 Para ver el tablero interactivo ve a <strong>Dashboard BI</strong> en el menú.</p>
      </div>
    `;
  }

  // ── POWER BI DASHBOARD ──────────────────────────────────────────────────────
  _pagePowerBI(el) {
    el.innerHTML = '';
    const pbi = document.createElement('powerbi-dashboard');
    el.appendChild(pbi);
  }

  // ── NUEVA PQRS ──────────────────────────────────────────────────────────────
  _pageNuevaPQRS(el) {
    el.innerHTML = `
      <div class="page-header"><h2>📝 Nueva PQRS</h2></div>
      <div class="card" style="max-width:600px">
        <form id="pqrsForm">
          <div class="form-group">
            <label>Tipo de solicitud</label>
            <select id="f-tipo" required>
              <option value="">— Selecciona —</option>
              <option value="1">Queja</option>
              <option value="2">Petición</option>
              <option value="3">Reclamo</option>
              <option value="4">Sugerencia</option>
            </select>
          </div>
          <div class="form-group"><label>Asunto</label><input id="f-asunto" required /></div>
          <div class="form-group"><label>Descripción detallada</label><textarea id="f-desc" required></textarea></div>
          <div class="form-group">
            <label>Prioridad</label>
            <select id="f-prior">
              <option value="1">🟢 Baja</option>
              <option value="2" selected>🟡 Media</option>
              <option value="3">🔴 Alta</option>
            </select>
          </div>
          <div style="display:flex;gap:10px">
            <button type="submit" class="btn btn-primary">Enviar PQRS</button>
            <button type="reset" class="btn btn-ghost">Limpiar</button>
          </div>
        </form>
      </div>
    `;

    el.querySelector('#pqrsForm').addEventListener('submit', async e => {
      e.preventDefault();
      const data = {
        id_usuario:    this._user?.id_usuario ?? 1,
        id_tipospqrs:  parseInt(el.querySelector('#f-tipo').value),
        radicado:      'RAD-' + Date.now(),
        descripcion:   el.querySelector('#f-desc').value,
        id_prioridad:  parseInt(el.querySelector('#f-prior').value),
        id_estado:     1,
        id_dependencia: 1,
      };
      try {
        await apiCall('/pqrs/', 'POST', data);
        window.toast?.show('PQRS enviada exitosamente', 'success');
        el.querySelector('#pqrsForm').reset();
      } catch(err) { window.toast?.show(err.message, 'error'); }
    });
  }

  // ── MIS PQRS ────────────────────────────────────────────────────────────────
  async _pageMisPQRS(el) {
    el.innerHTML = `
      <div class="page-header"><h2>📋 Mis PQRS</h2></div>
      <div class="card">
        <div id="misPqrsWrap"><p style="text-align:center;padding:24px;color:var(--text-muted)">Cargando…</p></div>
      </div>
    `;
    const wrap = el.querySelector('#misPqrsWrap');
    try {
      const all  = await apiCall('/pqrs/');
      const rows = all.filter(p => p.id_usuario === this._user?.id_usuario);
      const table = document.createElement('data-table');
      table.columns = [
        { key: 'radicado',       label: 'Radicado' },
        { key: 'descripcion',    label: 'Descripción',
          render: v => `<span title="${v}">${(v??'').slice(0,45)}${(v??'').length>45?'…':''}</span>` },
        { key: 'estado',         label: 'Estado',
          render: (v, row) => `<status-badge status="${row.nombre_estado??v??'—'}"></status-badge>` },
        { key: 'id_prioridad',   label: 'Prioridad',
          render: v => v==3?'<span class="badge badge-danger">🔴 Alta</span>':v==2?'<span class="badge badge-warning">🟡 Media</span>':'<span class="badge badge-success">🟢 Baja</span>' },
        { key: 'fecha_creacion', label: 'Fecha',
          render: v => v ? new Date(v).toLocaleDateString('es-CO') : '—' },
        { key: 'updated_at',     label: 'Actualizado',
          render: v => v ? new Date(v).toLocaleString('es-CO') : '—' },
      ];
      table.rows     = rows;
      table.emptyMsg = 'No tienes PQRS registradas';
      wrap.innerHTML = '';
      wrap.appendChild(table);
    } catch(e) {
      wrap.innerHTML = `<p style="color:var(--danger);padding:20px">${e.message}</p>`;
    }
  }

  // ── PERFIL ──────────────────────────────────────────────────────────────────
  _pagePerfil(el) {
    const rol = (this._user?.rol ?? 'estudiante').toLowerCase();
    const cfg = ROLE_CONFIG[rol] ?? ROLE_CONFIG.estudiante;
    const payload = this._decodeToken();

    el.innerHTML = `
      <div class="page-header"><h2>👤 Mi Perfil</h2></div>
      <div style="display:grid;grid-template-columns:200px 1fr;gap:20px;align-items:start">
        <div class="card" style="text-align:center">
          <div style="width:72px;height:72px;border-radius:50%;background:var(--accent-dim);border:2px solid var(--border-accent);display:flex;align-items:center;justify-content:center;font-size:1.8rem;font-weight:700;color:var(--accent-light);margin:0 auto 12px">
            ${(this._user?.nombre??'?').slice(0,2).toUpperCase()}
          </div>
          <h3>${this._user?.nombre}</h3>
          <p style="margin-top:4px"><span class="badge badge-accent">${cfg.label}</span></p>
        </div>
        <div class="card">
          <div class="card-header"><h3>Información del Token JWT</h3></div>
          <pre style="background:var(--bg-base);border:1px solid var(--border);border-radius:var(--radius-sm);padding:14px;font-size:0.8rem;color:#a5f3fc;overflow-x:auto">${JSON.stringify(payload, null, 2)}</pre>
          <p style="margin-top:12px;font-size:0.8rem;color:var(--text-muted)">
            🔐 El token es almacenado en <code>sessionStorage</code> — se elimina al cerrar la pestaña (temporal).
          </p>
        </div>
      </div>
    `;
  }

  // ── Timer JWT ────────────────────────────────────────────────────────────────
  _startTimer() {
    clearInterval(this._timer);
    this._timer = setInterval(() => {
      const remaining = Math.floor((this._expiresAt - Date.now()) / 1000);
      const badge = this.querySelector('#timerBadge');
      if (!badge) return;

      if (remaining <= 0) {
        clearInterval(this._timer);
        window.toast?.show('Tu sesión ha expirado. Por favor inicia sesión nuevamente.', 'warning');
        setTimeout(() => logout(), 1500);
        return;
      }

      const m = String(Math.floor(remaining / 60)).padStart(2,'0');
      const s = String(remaining % 60).padStart(2,'0');
      badge.textContent = `⏱ ${m}:${s}`;
      badge.className = 'token-timer' + (remaining < 300 ? ' danger' : remaining < 600 ? ' warning' : '');
    }, 1000);
  }

  _decodeToken() {
    try {
      const parts = (this._token ?? '').split('.');
      return JSON.parse(atob(parts[1]));
    } catch { return null; }
  }

  disconnectedCallback() {
    clearInterval(this._timer);
  }
}

customElements.define('app-dashboard', AppDashboard);
