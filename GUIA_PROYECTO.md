# 📁 Guía del Proyecto — Sistema PQRS Universitario

> Sistema de gestión de Peticiones, Quejas, Reclamos y Sugerencias (PQRS) para una institución universitaria.
> Stack: **FastAPI + PostgreSQL (Neon) + Web Components nativos**.

---

## 🗂️ Estructura General del Proyecto

```
fastapi/                          ← Raíz del proyecto
├── app/                          ← Backend (API REST con FastAPI)
│   ├── config/
│   │   └── db_config.py          ← Conexión a la base de datos
│   ├── controllers/              ← Lógica de negocio (clases)
│   ├── models/                   ← Esquemas de datos (Pydantic)
│   ├── routes/                   ← Definición de endpoints REST
│   ├── sql/
│   │   └── create_tables.sql     ← Script SQL completo de la BD
│   └── main.py                   ← Punto de entrada de la API
│
├── frontend/                     ← Frontend (HTML + JS puro)
│   ├── components/               ← Web Components reutilizables
│   ├── index.html                ← Única página HTML
│   ├── app.js                    ← Orquestador y cliente HTTP
│   └── styles.css                ← Estilos globales
│
├── requirements.txt              ← Dependencias Python
├── alter_db_audit.py             ← Script para migrar BD (audit fields)
└── API_DOCUMENTATION.md          ← Docs completa de la API
```

---

## 🔧 Backend — Carpeta `app/`

### `app/main.py` — Punto de entrada
- Crea la instancia de FastAPI.
- Registra todos los routers (rutas de la API).
- Configura CORS para permitir peticiones desde el frontend.

```python
# Ejemplo de lo que hace:
app = FastAPI(title="PQRS API")
app.include_router(pqrs_router)
app.include_router(usuarios_router)
# ... etc
```

---

### `app/config/db_config.py` — Conexión a la BD

Contiene la función `get_db_connection()` que retorna una conexión a PostgreSQL usando `psycopg2`.

- **Base de datos:** Neon (PostgreSQL en la nube)
- **Host:** `ep-fragrant-glitter-aig2qu6i-pooler.c-4.us-east-1.aws.neon.tech`
- **BD:** `pqrsdb`
- Usa `DictCursor` para retornar filas como diccionarios.

> ⚠️ En producción se debe mover la contraseña a una variable de entorno `.env`.

---

### `app/models/` — Modelos de datos (Pydantic)

Cada archivo define la **forma de los datos** que la API acepta y devuelve (validación automática).

| Archivo | Modelo | Descripción |
|---|---|---|
| `auth_model.py` | `LoginRequest`, `TokenResponse` | Login y respuesta JWT |
| `usuario_model.py` | `Usuario` | Datos de un usuario |
| `pqrs_model.py` | `Pqrs` | Campos de una solicitud PQRS |
| `respuesta_model.py` | `Respuesta` | Respuesta a un PQRS |
| `historial_estados_model.py` | `HistorialEstado` | Cambio de estado de un PQRS |
| `rol_model.py` | `Rol` | Rol del sistema |
| `estado_model.py` | `Estado` | Estado posible de PQRS |
| `prioridad_model.py` | `Prioridad` | Nivel de urgencia |
| `dependencia_model.py` | `Dependencia` | Área a la que se dirige el PQRS |
| `programa_model.py` | `Programa` | Programa académico |
| `facultad_model.py` | `Facultad` | Facultad académica |
| `tipospqrs_model.py` | `TiposPqrs` | Petición / Queja / Reclamo / Sugerencia |

---

### `app/controllers/` — Lógica de negocio (Clases)

Cada controlador es una **clase Python** con métodos CRUD:
- `create_X()` → INSERT
- `get_X_all()` → SELECT *
- `get_X(id)` → SELECT WHERE id
- `update_X(id, data)` → UPDATE
- `delete_X(id)` → DELETE

```python
class PqrsController:
    def create_pqrs(self, pqrs: Pqrs):    # POST /pqrs/
    def get_pqrs_all(self):               # GET  /pqrs/
    def get_pqrs(self, id_pqrs):          # GET  /pqrs/{id}
    def update_pqrs(self, id, pqrs):      # PUT  /pqrs/{id}
    def delete_pqrs(self, id):            # DELETE /pqrs/{id}
```

| Controlador | Gestiona |
|---|---|
| `auth_controller.py` | Login, generación y verificación de JWT |
| `usuarios_controller.py` | Usuarios del sistema |
| `pqrs_controller.py` | Solicitudes PQRS |
| `respuestas_controller.py` | Respuestas a PQRS |
| `historial_estados_controller.py` | Cambios de estado |
| `historial_controller.py` | Seguimiento PQRS |
| `roles_controller.py` | Roles del sistema |
| `estados_controller.py` | Estados de PQRS |
| `prioridades_controller.py` | Prioridades |
| `dependencias_controller.py` | Dependencias |
| `facultades_controller.py` | Facultades |
| `programas_controller.py` | Programas académicos |
| `tipospqrs_controller.py` | Tipos de solicitud |

---

### `app/routes/` — Endpoints REST

Conectan las URLs con los métodos del controlador. Cada archivo define un `APIRouter`.

```python
router = APIRouter(prefix="/pqrs", tags=["PQRS"])

@router.get("/")        → pqrs_ctrl.get_pqrs_all()
@router.post("/")       → pqrs_ctrl.create_pqrs()
@router.get("/{id}")    → pqrs_ctrl.get_pqrs(id)
@router.put("/{id}")    → pqrs_ctrl.update_pqrs()
@router.delete("/{id}") → pqrs_ctrl.delete_pqrs()
```

---

### `app/sql/create_tables.sql` — Esquema de la BD

Script SQL completo con:
- Todas las tablas con relaciones (FK)
- Campos de auditoría en cada tabla: `created_at`, `updated_at`, `estado`
- Índices de rendimiento
- **Vistas** listas para Power BI:
  - `vista_pqrs` — PQRS con nombres legibles (sin IDs)
  - `vista_usuarios` — Usuarios con rol y programa
  - `vista_seguimiento` — Historial de seguimiento
  - `vista_historial` — Auditoría de cambios de estado

---

## 🎨 Frontend — Carpeta `frontend/`

### `frontend/index.html` — La única página

Solo contiene el esqueleto. Todo el contenido es generado dinámicamente por los Web Components.

```html
<login-screen id="loginScreen"></login-screen>
<app-dashboard id="dashboardShell" hidden></app-dashboard>
<!-- 10 <script> tags para cargar los 10 componentes -->
```

---

### `frontend/app.js` — Orquestador principal

| Función / Variable | Descripción |
|---|---|
| `API_BASE_URL` | URL base de la API (`http://localhost:8000`) |
| `apiCall(endpoint, method, data)` | Hace fetch con JWT automático en el header |
| `logout()` | Limpia sessionStorage y vuelve al login |
| `bootstrap()` | Arranca la app; escucha `auth-success` y restaura sesión |

**Flujo de autenticación:**
```
Usuario llena formulario
    → login-screen llama POST /auth/login
    → API responde { access_token, user, expires_in }
    → Token guardado en sessionStorage (temporal, se borra al cerrar pestaña)
    → Evento 'auth-success' dispara bootstrap
    → app-dashboard se inicializa con usuario y token
```

---

### `frontend/styles.css` — Sistema de diseño

Define variables CSS globales que todos los componentes heredan:
- Paleta de colores dark mode (`--bg-base`, `--accent`, `--text-primary`...)
- Tipografía Inter (Google Fonts)
- Clases utilitarias: `.btn`, `.card`, `.badge`, `.form-group`, `.data-table`
- Animaciones: `fadeSlideIn`, `animate-in`

---

### `frontend/components/` — Los 10 Web Components

Son **elementos HTML personalizados** (`customElements.define`). Reutilizables, sin dependencia de frameworks.

| # | Componente | Tag HTML | Para qué sirve |
|---|---|---|---|
| 1 | `app-dashboard.js` | `<app-dashboard>` | Shell completo: navbar + sidebar + contenido. Controla la navegación y los menús por rol |
| 2 | `login-screen.js` | `<login-screen>` | Pantalla de login JWT. Emite evento `auth-success` al autenticarse |
| 3 | `data-table.js` | `<data-table>` | Tabla dinámica con columnas configurables y botones de acción por fila |
| 4 | `stat-card.js` | `<stat-card>` | Tarjeta KPI (número grande + label + tendencia) para el panel |
| 5 | `toast-notification.js` | `<toast-notification>` | Notificaciones flotantes globales. Uso: `window.toast.show('msg', 'tipo')` |
| 6 | `powerbi-dashboard.js` | `<powerbi-dashboard>` | Embebe el tablero de Power BI vía `<iframe>` en la sección Dashboard BI |
| 7 | `modal-dialog.js` | `<modal-dialog>` | Modal reutilizable. API: `modal.setTitle()`, `modal.setContent()`, `modal.open()` |
| 8 | `role-badge.js` | `<role-badge>` | Chip coloreado de rol (admin / docente / estudiante) |
| 9 | `status-badge.js` | `<status-badge>` | Chip de estado PQRS o activo/inactivo de usuario |
| 10 | `empty-state.js` | `<empty-state>` | Placeholder amigable para tablas o secciones vacías |

---

## 🔑 Sistema de Roles

| Rol | Menú disponible | Acceso |
|---|---|---|
| `admin` | Dashboard, Usuarios, PQRS, Roles, Reportes, Dashboard BI | Control total |
| `docente` | Dashboard, Nueva PQRS, Mis PQRS, Perfil | Solo sus PQRS |
| `estudiante` | Dashboard, Nueva PQRS, Mis PQRS, Perfil | Solo sus PQRS |

El rol viaja **dentro del JWT** (no consulta la BD en cada request):
```json
{
  "sub": "1",
  "nombre": "nelson",
  "rol": "admin",
  "id_usuario": 1,
  "exp": 1712345678
}
```

---

## 🗄️ Tablas de la Base de Datos

```
roles               → Tipos de rol
facultades          → Facultades universitarias
programas           → Programas académicos (→ facultad)
dependencias        → Áreas que reciben PQRS
tipospqrs           → Petición / Queja / Reclamo / Sugerencia
estados             → Pendiente / En revisión / Resuelto...
prioridades         → Baja / Media / Alta
usuarios            → Usuarios (→ rol, → programa)
pqrs                → Solicitudes (→ usuario, tipo, estado, prioridad, dependencia)
respuestas          → Respuestas a PQRS
seguimiento_pqrs    → Notas de seguimiento
historial_estados   → Auditoría de cambios de estado
```

Todas las tablas tienen los campos de auditoría:
```sql
created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
estado      BOOLEAN   DEFAULT TRUE
```

---

## 🚀 Cómo correr el proyecto localmente

### 1. Backend (API)

```powershell
# Activar entorno virtual
.\myvenv\Scripts\Activate.ps1

# Instalar dependencias (solo la primera vez)
pip install -r requirements.txt

# Correr servidor
uvicorn app.main:app --reload --port 8000
```

- API: http://localhost:8000
- Swagger UI (docs): http://localhost:8000/docs

### 2. Frontend

```powershell
cd frontend
npx serve .
```

- Frontend: http://localhost:3000

> ⚠️ No abrir el `.html` directo — necesita servirse desde HTTP por los módulos ES.

### 3. Credenciales demo

| Usuario | Contraseña | Rol |
|---|---|---|
| `nelson` | `1234` | admin |

---

## 📝 Scripts de utilidad en la raíz

| Archivo | Para qué sirve |
|---|---|
| `alter_db_audit.py` | Agrega `created_at`, `updated_at`, `estado` a todas las tablas |
| `alter_db.py` | Migración antigua (deduplicar roles, agregar tablas) |
| `update_db.py` | Actualización de esquema |
| `fix_seq.py` | Repara secuencias SERIAL si se dessincronizan |
| `test_seed.py` | Prueba de inserción de datos de prueba |
| `test_dict.py` | Prueba del DictCursor de psycopg2 |
| `test_encoder.py` | Prueba del encoder JSON para fechas |

---

## 🌐 Despliegue en la nube

| Capa | Plataforma | Estado |
|---|---|---|
| Base de datos | **Neon** (PostgreSQL) | ✅ Ya en la nube |
| Backend (API) | **Render.com** | 🔄 Pendiente |
| Frontend | **Vercel / GitHub Pages** | 🔄 Pendiente |

**Para Render (API):**
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Cambiar `API_BASE_URL` en `frontend/app.js` a la URL de Render

---

## 📊 Power BI

- **Tablero:** Sección "Dashboard BI" en el menú del Admin
- **Componente:** `<powerbi-dashboard>` (archivo `powerbi-dashboard.js`)
- **Fuente:** iframe de Power BI Service (publicado en la web)
- **Datos:** Conectado a Neon PostgreSQL usando las vistas de la BD
