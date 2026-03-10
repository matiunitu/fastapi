// Configuración de la API
const API_BASE_URL = 'http://localhost:8000';

// Estado de la aplicación
let currentUser = {
    username: '',
    role: '',
    id: null
};

// Función auxiliar para hacer llamadas a la API
async function apiCall(endpoint, method = 'GET', data = null) {
    try {
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        };
        
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        
        if (!response.ok) {
            throw new Error(`Error: ${response.status} ${response.statusText}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        showAlert(`Error de conexión: ${error.message}`, 'danger');
        throw error;
    }
}

// Función para mostrar alertas
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const contentArea = document.getElementById('contentArea');
    contentArea.insertBefore(alertDiv, contentArea.firstChild);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Configuración de roles y sus permisos
const roleConfig = {
    admin: {
        name: 'Administrador',
        icon: '👨‍💼',
        menu: [
            { id: 'dashboard', name: 'Panel Principal', icon: '📊' },
            { id: 'usuarios', name: 'Gestionar Usuarios', icon: '👥' },
            { id: 'pqrs', name: 'Gestionar PQRS', icon: '📋' },
            { id: 'reportes', name: 'Reportes', icon: '📈' },
            { id: 'configuracion', name: 'Configuración', icon: '⚙️' }
        ]
    },
    docente: {
        name: 'Docente',
        icon: '👨‍🏫',
        menu: [
            { id: 'dashboard', name: 'Panel Principal', icon: '📊' },
            { id: 'quejas', name: 'Poner Queja', icon: '📝' },
            { id: 'misQuejas', name: 'Mis Quejas', icon: '📋' },
            { id: 'perfil', name: 'Mi Perfil', icon: '👤' }
        ]
    },
    estudiante: {
        name: 'Estudiante',
        icon: '👨‍🎓',
        menu: [
            { id: 'dashboard', name: 'Panel Principal', icon: '📊' },
            { id: 'quejas', name: 'Poner Queja', icon: '📝' },
            { id: 'misQuejas', name: 'Mis Quejas', icon: '📋' },
            { id: 'perfil', name: 'Mi Perfil', icon: '👤' }
        ]
    }
};

// Evento de Submit del Login
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const role = document.getElementById('role').value;
    
    // Validación básica
    if (username === '' || password === '' || role === '') {
        alert('Por favor completa todos los campos');
        return;
    }
    
    // Simulación de autenticación (en producción conectar con backend)
    // Por ahora aceptamos cualquier usuario para desarrollo
    loginUser(username, role);
});

// Función para hacer login
function loginUser(username, role) {
    currentUser.username = username;
    currentUser.role = role;
    
    // Guardar en localStorage
    localStorage.setItem('currentUser', JSON.stringify(currentUser));
    
    // Cambiar a dashboard
    document.getElementById('loginPage').classList.add('d-none');
    document.getElementById('dashboardPage').classList.remove('d-none');
    
    // Establecer datos de usuario
    document.getElementById('userDisplay').textContent = username;
    document.getElementById('roleDisplay').textContent = roleConfig[role].name;
    
    // Generar menú
    generateMenu();
    
    // Mostrar dashboard
    showSection('dashboard');
}

// Generar menú dinámicamente
function generateMenu() {
    const role = currentUser.role;
    const menuConfig = roleConfig[role].menu;
    const menuSidebar = document.getElementById('menuSidebar');
    
    menuSidebar.innerHTML = '';
    
    menuConfig.forEach((item, index) => {
        const menuItem = document.createElement('button');
        menuItem.type = 'button';
        menuItem.classList.add('list-group-item', 'list-group-item-action', 'text-start');
        if (index === 0) menuItem.classList.add('active');
        menuItem.innerHTML = `${item.icon} ${item.name}`;
        
        menuItem.addEventListener('click', () => {
            // Remover active de todos
            document.querySelectorAll('.list-group-item').forEach(i => {
                i.classList.remove('active');
            });
            // Agregar active al clickeado
            menuItem.classList.add('active');
            // Mostrar sección
            showSection(item.id);
        });
        
        menuSidebar.appendChild(menuItem);
    });
}

// Mostrar sección específica
function showSection(sectionId) {
    const contentArea = document.getElementById('contentArea');
    const sectionTitle = document.getElementById('sectionTitle');
    const role = currentUser.role;
    
    contentArea.innerHTML = '';
    
    switch(sectionId) {
        case 'dashboard':
            showDashboard();
            sectionTitle.textContent = 'Panel Principal';
            break;
        case 'usuarios':
            showUsuarios();
            sectionTitle.textContent = 'Gestionar Usuarios';
            break;
        case 'pqrs':
            showPQRS();
            sectionTitle.textContent = 'Gestionar PQRS';
            break;
        case 'reportes':
            showReportes();
            sectionTitle.textContent = 'Reportes';
            break;
        case 'configuracion':
            showConfiguracion();
            sectionTitle.textContent = 'Configuración';
            break;
        case 'quejas':
            showQuejas();
            sectionTitle.textContent = 'Poner Queja';
            break;
        case 'misQuejas':
            showMisQuejas();
            sectionTitle.textContent = 'Mis Quejas';
            break;
        case 'perfil':
            showPerfil();
            sectionTitle.textContent = 'Mi Perfil';
            break;
    }
}

// Funciones de secciones
function showDashboard() {
    const role = currentUser.role;
    const roleInfo = roleConfig[role];
    
    let html = `
        <div class="welcome-card mb-4">
            <h2>${roleInfo.icon} ¡Bienvenido!</h2>
            <p>${roleInfo.name}</p>
        </div>
        
        <div class="row">
            <div class="col-md-6">
                <div class="stat-card">
                    <h5>Total de PQRS</h5>
                    <div class="stat-number">24</div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="stat-card">
                    <h5>Usuarios Activos</h5>
                    <div class="stat-number">156</div>
                </div>
            </div>
        </div>
        
        <div class="alert alert-success mt-4">
            <strong>✓ Sesión iniciada correctamente</strong>
            <p>Usuario: <strong>${currentUser.username}</strong> | Rol: <strong>${roleInfo.name}</strong></p>
        </div>
    `;
    
    document.getElementById('contentArea').innerHTML = html;
}

function showUsuarios() {
    const html = `
        <button class="btn btn-primary mb-3" id="newUserBtn">+ Crear Usuario</button>
        
        <table class="table table-hover" id="usuariosTable">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Nombre</th>
                    <th>Email</th>
                    <th>Teléfono</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody id="usuariosTableBody">
                <tr><td colspan="5" class="text-center">Cargando...</td></tr>
            </tbody>
        </table>
    `;
    
    document.getElementById('contentArea').innerHTML = html;
    
    // Evento para crear nuevo usuario
    document.getElementById('newUserBtn').addEventListener('click', () => {
        showForm('crear_usuario');
    });
    
    // Cargar usuarios
    loadUsuarios();
}

async function loadUsuarios() {
    try {
        const usuarios = await apiCall('/get_usuarios/');
        const tbody = document.getElementById('usuariosTableBody');
        if (!tbody) return;
        
        tbody.innerHTML = '';
        
        if (usuarios.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center">No hay usuarios registrados</td></tr>';
            return;
        }
        
        usuarios.forEach(usuario => {
            const row = `<tr>
                <td>${usuario.id_usuario || 'N/A'}</td>
                <td>${usuario.nombre || 'N/A'}</td>
                <td>${usuario.correo || 'N/A'}</td>
                <td>${usuario.telefono || 'N/A'}</td>
                <td>
                    <button class="btn btn-sm btn-warning" onclick="editUsuario(${usuario.id_usuario})">Editar</button>
                    <button class="btn btn-sm btn-danger" onclick="deleteUsuario(${usuario.id_usuario})">Eliminar</button>
                </td>
            </tr>`;
            tbody.innerHTML += row;
        });
    } catch (error) {
        console.error('Error al cargar usuarios:', error);
        const tbody = document.getElementById('usuariosTableBody');
        if (tbody) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center text-danger">Error al cargar usuarios</td></tr>';
        }
    }
}

function editUsuario(id) {
    showAlert('Editar usuario ' + id + ' - En desarrollo', 'info');
}

function deleteUsuario(id) {
    if (!confirm('¿Estás seguro de que deseas eliminar este usuario?')) return;
    
    apiCall(`/delete_usuario/${id}`, 'DELETE')
        .then(() => {
            showAlert('Usuario eliminado correctamente', 'success');
            loadUsuarios();
        })
        .catch((error) => {
            showAlert('Error al eliminar usuario: ' + error.message, 'danger');
        });
}

function showPQRS() {
    const html = `
        <button class="btn btn-primary mb-3" id="newPqrsBtn">+ Nueva PQRS</button>
        
        <table class="table table-hover" id="pqrsTable">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Radicado</th>
                    <th>Usuario</th>
                    <th>Tipo</th>
                    <th>Estado</th>
                    <th>Prioridad</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody id="pqrsTableBody">
                <tr><td colspan="7" class="text-center">Cargando...</td></tr>
            </tbody>
        </table>
    `;
    
    document.getElementById('contentArea').innerHTML = html;
    
    // Cargar PQRs de la API
    loadPQRS();
    
    // Evento para crear nueva PQRS
    document.getElementById('newPqrsBtn').addEventListener('click', () => {
        showForm('crear_pqrs');
    });
}

async function loadPQRS() {
    try {
        const pqrs = await apiCall('/pqrs/');
        const tbody = document.getElementById('pqrsTableBody');
        if (!tbody) return;
        
        tbody.innerHTML = '';
        
        if (pqrs.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" class="text-center">No hay PQRS registradas</td></tr>';
            return;
        }
        
        pqrs.forEach(p => {
            const row = `<tr>
                <td>${p.id_pqrs || 'N/A'}</td>
                <td>${p.radicado || 'N/A'}</td>
                <td>${p.id_usuario || 'N/A'}</td>
                <td><span class="badge bg-warning">${p.id_tipo_pqrs || 'N/A'}</span></td>
                <td><span class="badge bg-info" id="estado-${p.id_pqrs}">${p.id_estado || 'N/A'}</span></td>
                <td><span class="badge bg-danger">${p.id_prioridad || 'N/A'}</span></td>
                <td>
                    <button class="btn btn-sm btn-info" onclick="verPQRS(${p.id_pqrs})">Ver</button>
                    <button class="btn btn-sm btn-warning" onclick="cambiarEstadoPQRS(${p.id_pqrs})">Cambiar Estado</button>
                </td>
            </tr>`;
            tbody.innerHTML += row;
        });
    } catch (error) {
        console.error('Error al cargar PQRS:', error);
        const tbody = document.getElementById('pqrsTableBody');
        if (tbody) {
            tbody.innerHTML = '<tr><td colspan="7" class="text-center text-danger">Error al cargar PQRS</td></tr>';
        }
    }
}

function verPQRS(id) {
    showAlert(`Ver PQRS #${id} - Funcionalidad en desarrollo`, 'info');
}

async function cambiarEstadoPQRS(id) {
    const nuevoEstado = prompt('Ingresa el nuevo estado (1=Abierta, 2=En Proceso, 3=Resuelta, 4=Cerrada):', '1');
    if (!nuevoEstado) return;
    
    try {
        await apiCall(`/update_pqrs/${id}`, 'PUT', { id_estado: parseInt(nuevoEstado) });
        showAlert('Estado actualizado correctamente', 'success');
        loadPQRS();
    } catch (error) {
        showAlert('Error al actualizar estado: ' + error.message, 'danger');
    }
}

function showReportes() {
    const html = `
        <div class="row">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">PQRS por Tipo</h5>
                        <p>Quejas: 45</p>
                        <p>Peticiones: 23</p>
                        <p>Reclamos: 12</p>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Usuarios por Rol</h5>
                        <p>Estudiantes: 150</p>
                        <p>Docentes: 25</p>
                        <p>Administradores: 5</p>
                    </div>
                </div>
            </div>
        </div>
        
        <button class="btn btn-success mt-3">Descargar Reporte PDF</button>
    `;
    
    document.getElementById('contentArea').innerHTML = html;
}

function showConfiguracion() {
    const html = `
        <form>
            <div class="form-group">
                <label for="appName" class="form-label">Nombre de la Aplicación</label>
                <input type="text" class="form-control" id="appName" value="Sistema de Gestión PQRS">
            </div>
            
            <div class="form-group">
                <label for="siteEmail" class="form-label">Email del Sitio</label>
                <input type="email" class="form-control" id="siteEmail" value="info@example.com">
            </div>
            
            <div class="form-group">
                <label for="sitePhone" class="form-label">Teléfono</label>
                <input type="tel" class="form-control" id="sitePhone" value="+57 1 2345678">
            </div>
            
            <button type="submit" class="btn btn-primary">Guardar Cambios</button>
        </form>
    `;
    
    document.getElementById('contentArea').innerHTML = html;
}

function showQuejas() {
    const html = `
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">Crear Nueva PQRS</h5>
                
                <form id="pqrsForm">
                    <div class="form-group">
                        <label for="tipo_pqrs" class="form-label">Tipo de Solicitud</label>
                        <select class="form-select" id="tipo_pqrs" required>
                            <option value="">-- Selecciona --</option>
                            <option value="1">Queja</option>
                            <option value="2">Petición</option>
                            <option value="3">Reclamo</option>
                            <option value="4">Sugerencia</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="asunto" class="form-label">Asunto</label>
                        <input type="text" class="form-control" id="asunto" placeholder="Breve descripción del asunto" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="descripcion" class="form-label">Descripción Detallada</label>
                        <textarea class="form-control" id="descripcion" rows="5" placeholder="Describe tu queja o solicitud en detalle..." required></textarea>
                    </div>
                    
                    <div class="form-group">
                        <label for="id_prioridad" class="form-label">Prioridad</label>
                        <select class="form-select" id="id_prioridad" required>
                            <option value="1">Baja</option>
                            <option value="2" selected>Media</option>
                            <option value="3">Alta</option>
                        </select>
                    </div>
                    
                    <button type="submit" class="btn btn-primary">Enviar PQRS</button>
                    <button type="reset" class="btn btn-secondary">Limpiar</button>
                </form>
            </div>
        </div>
    `;
    
    document.getElementById('contentArea').innerHTML = html;
    
    // Agregar event listener al formulario
    document.getElementById('pqrsForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const pqrsData = {
            id_usuario: currentUser.id || 1,
            id_tipo_pqrs: parseInt(document.getElementById('tipo_pqrs').value),
            radicado: 'RAD-' + Date.now(),
            asunto: document.getElementById('asunto').value,
            descripcion: document.getElementById('descripcion').value,
            id_prioridad: parseInt(document.getElementById('id_prioridad').value),
            id_estado: 1
        };
        
        try {
            await apiCall('/create_pqrs', 'POST', pqrsData);
            showAlert('PQRS enviada exitosamente', 'success');
            document.getElementById('pqrsForm').reset();
        } catch (error) {
            showAlert('Error al enviar PQRS: ' + error.message, 'danger');
        }
    });
}

function showMisQuejas() {
    const html = `
        <table class="table table-hover" id="misQuejasTable">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Radicado</th>
                    <th>Tipo</th>
                    <th>Estado</th>
                    <th>Prioridad</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody id="misQuejasTableBody">
                <tr><td colspan="6" class="text-center">Cargando...</td></tr>
            </tbody>
        </table>
    `;
    
    document.getElementById('contentArea').innerHTML = html;
    loadMisQuejas();
}

async function loadMisQuejas() {
    try {
        const pqrs = await apiCall('/pqrs/');
        const tbody = document.getElementById('misQuejasTableBody');
        if (!tbody) return;
        
        // Filtrar solo las del usuario actual
        const misPqrs = pqrs.filter(p => p.id_usuario == (currentUser.id || 1));
        
        tbody.innerHTML = '';
        
        if (misPqrs.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" class="text-center">No tienes PQRS registradas</td></tr>';
            return;
        }
        
        misPqrs.forEach(p => {
            const row = `<tr>
                <td>${p.id_pqrs || 'N/A'}</td>
                <td>${p.radicado || 'N/A'}</td>
                <td><span class="badge bg-warning">${p.id_tipo_pqrs || 'N/A'}</span></td>
                <td><span class="badge bg-info">${p.id_estado || 'N/A'}</span></td>
                <td><span class="badge bg-danger">${p.id_prioridad || 'N/A'}</span></td>
                <td><button class="btn btn-sm btn-info" onclick="verPQRS(${p.id_pqrs})">Ver</button></td>
            </tr>`;
            tbody.innerHTML += row;
        });
    } catch (error) {
        console.error('Error al cargar PQRS:', error);
        const tbody = document.getElementById('misQuejasTableBody');
        if (tbody) {
            tbody.innerHTML = '<tr><td colspan="6" class="text-center text-danger">Error al cargar PQRS</td></tr>';
        }
    }
}

function showPerfil() {
    const html = `
        <div class="row">
            <div class="col-md-4">
                <div class="card">
                    <div class="card-body text-center">
                        <div style="font-size: 64px; margin-bottom: 10px;">👤</div>
                        <h5 class="card-title">${currentUser.username}</h5>
                        <p class="text-muted">${roleConfig[currentUser.role].name}</p>
                    </div>
                </div>
            </div>
            
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header">
                        <h5 class="mb-0">Información Personal</h5>
                    </div>
                    <div class="card-body">
                        <form>
                            <div class="form-group">
                                <label for="fullName" class="form-label">Nombre Completo</label>
                                <input type="text" class="form-control" id="fullName" value="${currentUser.username} García">
                            </div>
                            
                            <div class="form-group">
                                <label for="email" class="form-label">Email</label>
                                <input type="email" class="form-control" id="email" value="${currentUser.username}@example.com">
                            </div>
                            
                            <div class="form-group">
                                <label for="phone" class="form-label">Teléfono</label>
                                <input type="tel" class="form-control" id="phone" value="+57 300 123 4567">
                            </div>
                            
                            <div class="form-group">
                                <label for="document" class="form-label">Documento</label>
                                <input type="text" class="form-control" id="document" value="1023456789" disabled>
                            </div>
                            
                            <button type="submit" class="btn btn-primary">Guardar Cambios</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.getElementById('contentArea').innerHTML = html;
}

// Mostrar formularios dinámicamente
function showForm(formType) {
    const contentArea = document.getElementById('contentArea');
    
    if (formType === 'crear_usuario') {
        const html = `
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Crear Nuevo Usuario</h5>
                    
                    <form id="createUserForm">
                        <div class="form-group">
                            <label for="nombre" class="form-label">Nombre</label>
                            <input type="text" class="form-control" id="nombre" required>
                        </div>
                        
                        <div class="form-group">
                            <label for="apellido" class="form-label">Apellido</label>
                            <input type="text" class="form-control" id="apellido" required>
                        </div>
                        
                        <div class="form-group">
                            <label for="correo" class="form-label">Correo</label>
                            <input type="email" class="form-control" id="correo" required>
                        </div>
                        
                        <div class="form-group">
                            <label for="telefono" class="form-label">Teléfono</label>
                            <input type="tel" class="form-control" id="telefono" required>
                        </div>
                        
                        <div class="form-group">
                            <label for="numero_documento" class="form-label">Documento</label>
                            <input type="text" class="form-control" id="numero_documento" required>
                        </div>
                        
                        <div class="form-group">
                            <label for="id_rol" class="form-label">Rol</label>
                            <select class="form-select" id="id_rol" required>
                                <option value="1">Estudiante</option>
                                <option value="2">Docente</option>
                                <option value="3">Administrador</option>
                            </select>
                        </div>
                        
                        <button type="submit" class="btn btn-primary">Crear</button>
                        <button type="button" class="btn btn-secondary" onclick="showSection('usuarios')">Cancelar</button>
                    </form>
                </div>
            </div>
        `;
        contentArea.innerHTML = html;
        
        document.getElementById('createUserForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const userData = {
                nombre: document.getElementById('nombre').value,
                apellido: document.getElementById('apellido').value,
                correo: document.getElementById('correo').value,
                telefono: document.getElementById('telefono').value,
                numero_documento: document.getElementById('numero_documento').value,
                id_rol: parseInt(document.getElementById('id_rol').value)
            };
            
            try {
                await apiCall('/create_usuario', 'POST', userData);
                showAlert('Usuario creado exitosamente', 'success');
                showSection('usuarios');
            } catch (error) {
                showAlert('Error al crear usuario: ' + error.message, 'danger');
            }
        });
    }
    
    else if (formType === 'crear_pqrs') {
        const html = `
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Crear Nueva PQRS</h5>
                    
                    <form id="createPqrsForm">
                        <div class="form-group">
                            <label for="id_tipo_pqrs" class="form-label">Tipo de Solicitud</label>
                            <select class="form-select" id="id_tipo_pqrs" required>
                                <option value="">-- Selecciona --</option>
                                <option value="1">Queja</option>
                                <option value="2">Petición</option>
                                <option value="3">Reclamo</option>
                                <option value="4">Sugerencia</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label for="asunto" class="form-label">Asunto</label>
                            <input type="text" class="form-control" id="asunto" required>
                        </div>
                        
                        <div class="form-group">
                            <label for="descripcion" class="form-label">Descripción Detallada</label>
                            <textarea class="form-control" id="descripcion" rows="5" required></textarea>
                        </div>
                        
                        <div class="form-group">
                            <label for="id_prioridad" class="form-label">Prioridad</label>
                            <select class="form-select" id="id_prioridad" required>
                                <option value="1">Baja</option>
                                <option value="2" selected>Media</option>
                                <option value="3">Alta</option>
                            </select>
                        </div>
                        
                        <button type="submit" class="btn btn-primary">Enviar</button>
                        <button type="button" class="btn btn-secondary" onclick="showSection('quejas')">Cancelar</button>
                    </form>
                </div>
            </div>
        `;
        contentArea.innerHTML = html;
        
        document.getElementById('createPqrsForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const pqrsData = {
                id_usuario: currentUser.id || 1,
                id_tipo_pqrs: parseInt(document.getElementById('id_tipo_pqrs').value),
                radicado: 'RAD-' + Date.now(),
                asunto: document.getElementById('asunto').value,
                descripcion: document.getElementById('descripcion').value,
                id_prioridad: parseInt(document.getElementById('id_prioridad').value),
                id_estado: 1
            };
            
            try {
                await apiCall('/create_pqrs', 'POST', pqrsData);
                showAlert('PQRS enviada exitosamente', 'success');
                showSection('quejas');
            } catch (error) {
                showAlert('Error al enviar PQRS: ' + error.message, 'danger');
            }
        });
    }
}

// Evento de Logout
document.getElementById('logoutBtn').addEventListener('click', () => {
    if (confirm('¿Estás seguro de que deseas cerrar sesión?')) {
        logout();
    }
});

function logout() {
    // Limpiar datos
    currentUser = { username: '', role: '' };
    localStorage.removeItem('currentUser');
    
    // Volver a login
    document.getElementById('dashboardPage').classList.add('d-none');
    document.getElementById('loginPage').classList.remove('d-none');
    
    // Limpiar formulario
    document.getElementById('loginForm').reset();
}

// Verificar si hay sesión guardada al cargar
window.addEventListener('DOMContentLoaded', () => {
    const savedUser = localStorage.getItem('currentUser');
    if (savedUser) {
        currentUser = JSON.parse(savedUser);
        loginUser(currentUser.username, currentUser.role);
    }
});
