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

    def seed_demo_user(self):
        """Crea el usuario demo nelson/admin/1234 si no existe."""
        conn = get_db_connection()
        try:
            cur = conn.cursor()

            # Verificar que existan roles base
            cur.execute("SELECT id_rol FROM roles WHERE nombre_rol = 'admin' LIMIT 1")
            rol = cur.fetchone()
            if not rol:
                # Insertar roles si no existen
                cur.execute("""
                    INSERT INTO roles (nombre_rol, descripcion, estado) VALUES
                    ('admin',      'Acceso total al sistema',                    1),
                    ('docente',    'Gestión de PQRS propias y respuestas',       1),
                    ('estudiante', 'Crear y consultar sus propias PQRS',         1)
                    ON CONFLICT DO NOTHING
                """)
                conn.commit()
                cur.execute("SELECT id_rol FROM roles WHERE nombre_rol = 'admin' LIMIT 1")
                rol = cur.fetchone()

            # Verificar programa demo
            cur.execute("SELECT id_programa FROM programas LIMIT 1")
            prog = cur.fetchone()
            id_programa = prog["id_programa"] if prog else None

            if not id_programa:
                # Crear facultad y programa demo
                cur.execute("""
                    INSERT INTO facultades (nombre_facultad, descripcion, estado)
                    VALUES ('Facultad Demo', 'Facultad de demostración', 1)
                    RETURNING id_facultad
                """)
                fac = cur.fetchone()
                cur.execute("""
                    INSERT INTO programas (nombre_programa, descripcion, id_facultad, estado)
                    VALUES ('Programa Demo', 'Programa de demostración', %s, 1)
                    RETURNING id_programa
                """, (fac["id_facultad"],))
                prog = cur.fetchone()
                id_programa = prog["id_programa"]
                conn.commit()

            # Verificar si nelson ya existe
            cur.execute("SELECT id_usuario FROM usuarios WHERE LOWER(nombre) = 'nelson' LIMIT 1")
            existing = cur.fetchone()

            if not existing:
                hashed = hash_password("1234")
                cur.execute("""
                    INSERT INTO usuarios
                        (nombre, documento, correo, telefono, id_rol, id_programa,
                         password_hash, estado, activo)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, 1, TRUE)
                """, (
                    "nelson",
                    "00000001",
                    "nelson@admin.com",
                    "000-0000",
                    rol["id_rol"],
                    id_programa,
                    hashed,
                ))
                conn.commit()
                return {"message": "Usuario demo 'nelson' creado exitosamente"}
            else:
                # Asegurar que tiene password
                hashed = hash_password("1234")
                cur.execute("""
                    UPDATE usuarios
                    SET password_hash = %s, estado = 1, id_rol = %s
                    WHERE LOWER(nombre) = 'nelson'
                """, (hashed, rol["id_rol"]))
                conn.commit()
                return {"message": "Usuario demo 'nelson' ya existe, password actualizado"}
        finally:
            conn.close()
