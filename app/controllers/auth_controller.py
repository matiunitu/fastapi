from ..config.db_config import get_db_connection
from ..config.jwt_config import verify_password, hash_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from ..models.auth_model import LoginRequest, TokenResponse
from fastapi import HTTPException, status


class AuthController:

    def login(self, data: LoginRequest) -> TokenResponse:
        """Valida credenciales y retorna JWT temporal (60 min)."""
        conn = get_db_connection()
        try:
            cur = conn.cursor()
            # Buscar usuario por nombre + JOIN con rol
            cur.execute("""
                SELECT u.id_usuario, u.nombre, u.password_hash, u.estado,
                       r.nombre_rol
                FROM   usuarios u
                JOIN   roles r ON u.id_rol = r.id_rol
                WHERE  LOWER(u.nombre) = LOWER(%s)
                LIMIT  1
            """, (data.username,))
            row = cur.fetchone()

            if not row:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Usuario no encontrado"
                )

            if row["estado"] == 0:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Usuario inactivo"
                )

            if not row["password_hash"] or not verify_password(data.password, row["password_hash"]):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Contraseña incorrecta"
                )

            payload = {
                "sub":        str(row["id_usuario"]),
                "nombre":     row["nombre"],
                "rol":        row["nombre_rol"],
                "id_usuario": row["id_usuario"],
            }
            token = create_access_token(payload)

            return TokenResponse(
                access_token=token,
                token_type="bearer",
                expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                user={
                    "id_usuario": row["id_usuario"],
                    "nombre":     row["nombre"],
                    "rol":        row["nombre_rol"],
                }
            )
        finally:
            conn.close()

    # ── Datos catálogo para seed ────────────────────────────────────
    DEPENDENCIAS = [
        "Secretaria Academica",
        "Bienestar Universitario",
        "Registro y Control",
        "Recursos Humanos",
        "Sistemas e Informatica",
    ]

    TIPOS_PQRS = ["Peticion", "Queja", "Reclamo", "Sugerencia"]

    ESTADOS = ["Pendiente", "En revision", "Resuelto", "Rechazado"]

    PRIORIDADES = [("Baja", 1), ("Media", 2), ("Alta", 3)]

    ROLES = [
        ("ADMIN",      "Acceso total al sistema"),
        ("DOCENTE",    "Gestion de PQRS propias y respuestas"),
        ("ESTUDIANTE", "Crear y consultar sus propias PQRS"),
    ]

    USUARIOS = [
        {"nombre": "nelson", "documento": "00000001", "tipo_documento": "CC",
         "correo": "nelson@admin.com",    "telefono": "3001111111",
         "password": "1234", "rol_nombre": "ADMIN"},
        {"nombre": "maria",  "documento": "00000002", "tipo_documento": "CC",
         "correo": "maria@docente.com",   "telefono": "3002222222",
         "password": "1234", "rol_nombre": "DOCENTE"},
        {"nombre": "juan",   "documento": "00000003", "tipo_documento": "CC",
         "correo": "juan@estudiante.com", "telefono": "3003333333",
         "password": "1234", "rol_nombre": "ESTUDIANTE"},
    ]

    # ── helpers internos ─────────────────────────────────────────
    @staticmethod
    def _exists(cur, table, col, val):
        cur.execute(f"SELECT 1 FROM {table} WHERE {col} = %s LIMIT 1", (val,))
        return cur.fetchone() is not None

    @staticmethod
    def _get_id(cur, table, id_col, name_col, val):
        cur.execute(f"SELECT {id_col} FROM {table} WHERE {name_col} = %s LIMIT 1", (val,))
        r = cur.fetchone()
        return r[id_col] if r else None

    # ── seed completo ────────────────────────────────────────────
    def seed_demo_user(self):
        """
        Siembra todos los catálogos (roles, dependencias, tipos PQRS,
        prioridades, estados) + facultad/programa demo + 3 usuarios demo.
        """
        conn = get_db_connection()
        resumen = []
        try:
            cur = conn.cursor()

            # ── Roles ────────────────────────────────────────────
            for nombre, desc in self.ROLES:
                if not self._exists(cur, "roles", "nombre_rol", nombre):
                    cur.execute(
                        "INSERT INTO roles (nombre_rol, descripcion) VALUES (%s, %s)",
                        (nombre, desc),
                    )
                    resumen.append(f"Rol: {nombre}")
            conn.commit()

            # ── Facultad demo ────────────────────────────────────
            if not self._exists(cur, "facultades", "nombre_facultad", "Facultad Demo"):
                cur.execute(
                    "INSERT INTO facultades (nombre_facultad, descripcion) VALUES (%s, %s)",
                    ("Facultad Demo", "Facultad de demostracion"),
                )
                conn.commit()
                resumen.append("Facultad Demo")
            id_facultad = self._get_id(cur, "facultades", "id_facultad", "nombre_facultad", "Facultad Demo")

            # ── Programa demo ────────────────────────────────────
            cur.execute("SELECT id_programa FROM programas WHERE nombre_programa = %s LIMIT 1", ("Programa Demo",))
            prog_row = cur.fetchone()
            if not prog_row:
                cur.execute(
                    "INSERT INTO programas (nombre_programa, descripcion, id_facultad) VALUES (%s, %s, %s) RETURNING id_programa",
                    ("Programa Demo", "Programa de demostracion", id_facultad),
                )
                prog_row = cur.fetchone()
                conn.commit()
                resumen.append("Programa Demo")
            id_programa = prog_row["id_programa"]

            # ── Dependencias ─────────────────────────────────────
            for nombre in self.DEPENDENCIAS:
                if not self._exists(cur, "dependencias", "nombre_dependencia", nombre):
                    cur.execute("INSERT INTO dependencias (nombre_dependencia) VALUES (%s)", (nombre,))
                    resumen.append(f"Dependencia: {nombre}")
            conn.commit()

            # ── Tipos PQRS ───────────────────────────────────────
            for nombre in self.TIPOS_PQRS:
                if not self._exists(cur, "tipospqrs", "nombre_tipospqrs", nombre):
                    cur.execute("INSERT INTO tipospqrs (nombre_tipospqrs) VALUES (%s)", (nombre,))
                    resumen.append(f"Tipo: {nombre}")
            conn.commit()

            # ── Estados ──────────────────────────────────────────
            for nombre in self.ESTADOS:
                if not self._exists(cur, "estados", "nombre_estado", nombre):
                    cur.execute("INSERT INTO estados (nombre_estado) VALUES (%s)", (nombre,))
                    resumen.append(f"Estado: {nombre}")
            conn.commit()

            # ── Prioridades ──────────────────────────────────────
            for nombre, nivel in self.PRIORIDADES:
                if not self._exists(cur, "prioridades", "nombre_prioridad", nombre):
                    cur.execute("INSERT INTO prioridades (nombre_prioridad, nivel) VALUES (%s, %s)", (nombre, nivel))
                    resumen.append(f"Prioridad: {nombre} (nivel {nivel})")
            conn.commit()

            # ── Usuarios demo ────────────────────────────────────
            for u in self.USUARIOS:
                id_rol = self._get_id(cur, "roles", "id_rol", "nombre_rol", u["rol_nombre"])
                if not id_rol:
                    resumen.append(f"WARN: Rol '{u['rol_nombre']}' no encontrado, saltando {u['nombre']}")
                    continue

                hashed = hash_password(u["password"])

                cur.execute("SELECT id_usuario FROM usuarios WHERE LOWER(nombre) = LOWER(%s)", (u["nombre"],))
                existe = cur.fetchone()

                if existe:
                    cur.execute(
                        "UPDATE usuarios SET password_hash=%s, id_rol=%s, estado=1, activo=TRUE WHERE id_usuario=%s",
                        (hashed, id_rol, existe["id_usuario"]),
                    )
                    resumen.append(f"Usuario '{u['nombre']}' actualizado -> {u['rol_nombre']}")
                else:
                    cur.execute(
                        """INSERT INTO usuarios
                           (nombre, tipo_documento, documento, correo, telefono,
                            id_rol, id_programa, password_hash, estado, activo)
                           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,1,TRUE)""",
                        (u["nombre"], u["tipo_documento"], u["documento"],
                         u["correo"], u["telefono"], id_rol, id_programa, hashed),
                    )
                    resumen.append(f"Usuario '{u['nombre']}' creado -> {u['rol_nombre']}")

            conn.commit()

            return {
                "message": "Seed completo",
                "creados": resumen,
                "credenciales": [
                    "nelson / 1234  ->  ADMIN",
                    "maria  / 1234  ->  DOCENTE",
                    "juan   / 1234  ->  ESTUDIANTE",
                ],
            }
        finally:
            conn.close()
