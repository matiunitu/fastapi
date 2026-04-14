"""
seed_usuarios.py
Siembra todos los datos necesarios para que la app funcione:
  - Roles, facultad, programa
  - Dependencias, tipos de PQRS, prioridades, estados
  - 3 usuarios demo: nelson (admin), maria (docente), juan (estudiante)

Ejecutar: python -X utf8 seed_usuarios.py
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.config.db_config import get_db_connection
from app.config.jwt_config import hash_password

# ────────────────────────────────────────────────────────────────
USUARIOS = [
    {"nombre": "nelson", "documento": "00000001", "tipo_documento": "CC",
     "correo": "nelson@admin.com",      "telefono": "3001111111",
     "password": "1234", "rol_nombre": "ADMIN"},
    {"nombre": "maria",  "documento": "00000002", "tipo_documento": "CC",
     "correo": "maria@docente.com",     "telefono": "3002222222",
     "password": "1234", "rol_nombre": "DOCENTE"},
    {"nombre": "juan",   "documento": "00000003", "tipo_documento": "CC",
     "correo": "juan@estudiante.com",   "telefono": "3003333333",
     "password": "1234", "rol_nombre": "ESTUDIANTE"},
]

ROLES = [
    ("ADMIN",      "Acceso total al sistema"),
    ("DOCENTE",    "Gestion de PQRS propias y respuestas"),
    ("ESTUDIANTE", "Crear y consultar sus propias PQRS"),
]

DEPENDENCIAS = [
    "Secretaria Academica",
    "Bienestar Universitario",
    "Registro y Control",
    "Recursos Humanos",
    "Sistemas e Informatica",
]

TIPOS_PQRS = [
    "Peticion",
    "Queja",
    "Reclamo",
    "Sugerencia",
]

ESTADOS = [
    "Pendiente",
    "En revision",
    "Resuelto",
    "Rechazado",
]

PRIORIDADES = [
    ("Baja",   1),
    ("Media",  2),
    ("Alta",   3),
]

# ────────────────────────────────────────────────────────────────
conn = get_db_connection()
cur  = conn.cursor()

def exists_by_col(table, col, val):
    cur.execute(f"SELECT 1 FROM {table} WHERE {col} = %s LIMIT 1", (val,))
    return cur.fetchone() is not None

def get_id(table, id_col, name_col, val):
    cur.execute(f"SELECT {id_col} FROM {table} WHERE {name_col} = %s LIMIT 1", (val,))
    r = cur.fetchone()
    return r[id_col] if r else None

# ── Roles ────────────────────────────────────────────────────────
print("Sembrando roles...")
for nombre, desc in ROLES:
    if not exists_by_col("roles", "nombre_rol", nombre):
        cur.execute("INSERT INTO roles (nombre_rol, descripcion) VALUES (%s, %s)", (nombre, desc))
        print(f"  [+] Rol: {nombre}")
conn.commit()

# ── Facultad ────────────────────────────────────────────────────
print("Sembrando facultad demo...")
if not exists_by_col("facultades", "nombre_facultad", "Facultad Demo"):
    cur.execute(
        "INSERT INTO facultades (nombre_facultad, descripcion) VALUES (%s, %s)",
        ("Facultad Demo", "Facultad de demostracion")
    )
    conn.commit()
id_facultad = get_id("facultades", "id_facultad", "nombre_facultad", "Facultad Demo")

# ── Programa ────────────────────────────────────────────────────
print("Sembrando programa demo...")
cur.execute("SELECT id_programa FROM programas WHERE nombre_programa = %s LIMIT 1", ("Programa Demo",))
prog_row = cur.fetchone()
if not prog_row:
    cur.execute(
        "INSERT INTO programas (nombre_programa, descripcion, id_facultad) VALUES (%s, %s, %s) RETURNING id_programa",
        ("Programa Demo", "Programa de demostracion", id_facultad)
    )
    prog_row = cur.fetchone()
    conn.commit()
id_programa = prog_row["id_programa"]


# ── Dependencias ─────────────────────────────────────────────────
print("Sembrando dependencias...")
for nombre in DEPENDENCIAS:
    if not exists_by_col("dependencias", "nombre_dependencia", nombre):
        cur.execute("INSERT INTO dependencias (nombre_dependencia) VALUES (%s)", (nombre,))
        print(f"  [+] Dependencia: {nombre}")
conn.commit()

# ── Tipos PQRS ──────────────────────────────────────────────────
print("Sembrando tipos PQRS...")
for nombre in TIPOS_PQRS:
    if not exists_by_col("tipospqrs", "nombre_tipospqrs", nombre):
        cur.execute("INSERT INTO tipospqrs (nombre_tipospqrs) VALUES (%s)", (nombre,))
        print(f"  [+] Tipo: {nombre}")
conn.commit()

# ── Estados ──────────────────────────────────────────────────────
print("Sembrando estados...")
for nombre in ESTADOS:
    if not exists_by_col("estados", "nombre_estado", nombre):
        cur.execute("INSERT INTO estados (nombre_estado) VALUES (%s)", (nombre,))
        print(f"  [+] Estado: {nombre}")
conn.commit()

# ── Prioridades ──────────────────────────────────────────────────
print("Sembrando prioridades...")
for nombre, nivel in PRIORIDADES:
    if not exists_by_col("prioridades", "nombre_prioridad", nombre):
        cur.execute("INSERT INTO prioridades (nombre_prioridad, nivel) VALUES (%s, %s)", (nombre, nivel))
        print(f"  [+] Prioridad: {nombre} (nivel {nivel})")
conn.commit()

# ── Usuarios ─────────────────────────────────────────────────────
print("Sembrando usuarios demo...")
for u in USUARIOS:
    id_rol = get_id("roles", "id_rol", "nombre_rol", u["rol_nombre"])
    if not id_rol:
        print(f"  [WARN] Rol '{u['rol_nombre']}' no encontrado — saltando usuario {u['nombre']}")
        continue

    hashed = hash_password(u["password"])

    cur.execute("SELECT id_usuario FROM usuarios WHERE LOWER(nombre) = LOWER(%s)", (u["nombre"],))
    existe = cur.fetchone()

    if existe:
        cur.execute(
            "UPDATE usuarios SET password_hash=%s, id_rol=%s, estado=1, activo=TRUE WHERE id_usuario=%s",
            (hashed, id_rol, existe["id_usuario"])
        )
        print(f"  [OK] '{u['nombre']}' actualizado -> rol {u['rol_nombre']}")
    else:
        cur.execute(
            """INSERT INTO usuarios
               (nombre, tipo_documento, documento, correo, telefono,
                id_rol, id_programa, password_hash, estado, activo)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,1,TRUE)""",
            (u["nombre"], u["tipo_documento"], u["documento"],
             u["correo"], u["telefono"], id_rol, id_programa, hashed)
        )
        print(f"  [NUEVO] '{u['nombre']}' creado -> rol {u['rol_nombre']}")

conn.commit()
conn.close()

print("\nListo! Credenciales demo:")
print("  nelson / 1234  ->  ADMIN")
print("  maria  / 1234  ->  DOCENTE")
print("  juan   / 1234  ->  ESTUDIANTE")
