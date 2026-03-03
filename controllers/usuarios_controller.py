import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.usuarios_model import Usuarios
from fastapi.encoders import jsonable_encoder

class UsuariosController:
        
    def create_usuarios(self, user: Usuarios):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO usuarios 
                (nombre, documento, correo, telefono, id_rol, id_programa, activo, created_at) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    user.nombre,
                    user.documento,
                    user.correo,
                    user.telefono,
                    user.id_rol,
                    user.id_programa,
                    user.activo,
                    user.created_at
                )
            )
            conn.commit()
            return {"resultado": "Usuario creado"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()
        

    def get_user(self, user_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id_usuario, nombre, documento, correo, telefono,
                          id_rol, id_programa, activo, created_at
                   FROM usuarios WHERE id_usuario = %s""",
                (user_id,)
            )
            result = cursor.fetchone()
            
            if result:
                content = {
                    'id_usuario': result[0],
                    'nombre': result[1],
                    'documento': result[2],
                    'correo': result[3],
                    'telefono': result[4],
                    'id_rol': result[5],
                    'id_programa': result[6],
                    'activo': result[7],
                    'created_at': result[8]
                }
                json_data = jsonable_encoder(content)            
                return json_data
            else:
                raise HTTPException(status_code=404, detail="Usuario not found")  
                
        except psycopg2.Error as err:
            print(err)
        finally:
            conn.close()
       
    def get_users(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id_usuario, nombre, documento, correo, telefono,
                          id_rol, id_programa, activo, created_at
                   FROM usuarios"""
            )
            result = cursor.fetchall()
            payload = []
            content = {} 

            for data in result:
                content = {
                    'id_usuario': data[0],
                    'nombre': data[1],
                    'documento': data[2],
                    'correo': data[3],
                    'telefono': data[4],
                    'id_rol': data[5],
                    'id_programa': data[6],
                    'activo': data[7],
                    'created_at': data[8]
                }
                payload.append(content)
                content = {}

            json_data = jsonable_encoder(payload)        
            if result:
               return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="Usuario not found")  
                
        except psycopg2.Error as err:
            print(err)
        finally:
            conn.close()