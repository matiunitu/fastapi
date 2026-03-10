import psycopg2
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.db_config import get_db_connection
from models.usuario_model import Usuario


class UsuariosController:
    def create_usuario(self, usuario: Usuario):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Insertar solo los campos requeridos por tabla SERIAL / DEFAULT
            cursor.execute(
                """INSERT INTO usuarios
                (nombre, documento, correo, telefono, id_rol, id_programa)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id_usuario""",
                (
                    usuario.nombre,
                    usuario.documento,
                    usuario.correo,
                    usuario.telefono,
                    usuario.id_rol,
                    usuario.id_programa,
                ),
            )
            id_usuario = cursor.fetchone()[0]
            conn.commit()
            return {"id_usuario": id_usuario, "resultado": "Usuario creado"}
        except psycopg2.IntegrityError as err:
            conn.rollback()
            raise HTTPException(status_code=400, detail=f"Integrity error: {str(err)}")
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_usuario(self, id_usuario: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id_usuario, nombre, documento, correo, telefono,
                id_rol, id_programa, activo, created_at
                FROM usuarios
                WHERE id_usuario = %s""",
                (id_usuario,),
            )
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            payload = {
                "id_usuario": result[0],
                "nombre": result[1],
                "documento": result[2],
                "correo": result[3],
                "telefono": result[4],
                "id_rol": result[5],
                "id_programa": result[6],
                "activo": result[7],
                "created_at": result[8],
            }
            return jsonable_encoder(payload)
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_usuarios(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id_usuario, nombre, documento, correo, telefono, id_rol, id_programa, activo, created_at FROM usuarios"
            )
            results = cursor.fetchall()
            payload = []
            for r in results:
                payload.append(
                    {
                        "id_usuario": r[0],
                        "nombre": r[1],
                        "documento": r[2],
                        "correo": r[3],
                        "telefono": r[4],
                        "id_rol": r[5],
                        "id_programa": r[6],
                        "activo": r[7],
                        "created_at": r[8],
                    }
                )
            return jsonable_encoder(payload)
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def update_usuario(self, id_usuario: int, usuario: Usuario):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE usuarios SET nombre=%s, documento=%s, correo=%s, telefono=%s,
                id_rol=%s, id_programa=%s, activo=%s
                WHERE id_usuario=%s""",
                (
                    usuario.nombre,
                    usuario.documento,
                    usuario.correo,
                    usuario.telefono,
                    usuario.id_rol,
                    usuario.id_programa,
                    usuario.activo,
                    id_usuario,
                ),
            )
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            conn.commit()
            return {"resultado": "Usuario actualizado"}
        except psycopg2.IntegrityError as err:
            conn.rollback()
            raise HTTPException(status_code=400, detail=f"Integrity error: {str(err)}")
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def delete_usuario(self, id_usuario: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id_usuario=%s", (id_usuario,))
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            conn.commit()
            return {"resultado": "Usuario eliminado"}
        except psycopg2.IntegrityError as err:
            conn.rollback()
            raise HTTPException(status_code=400, detail=f"Integrity error: {str(err)}")
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()
