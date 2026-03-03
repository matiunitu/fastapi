import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.roles_model import Roles
from fastapi.encoders import jsonable_encoder

class RolesController:
        
    def create_roles(self, user: Roles):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO roles (nombre_rol, descripcion) VALUES (%s, %s)",
                (
                    user.nombre_rol,
                    user.descripcion
                )
            )
            conn.commit()
            return {"resultado": "Rol creado"}
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
                "SELECT id_rol, nombre_rol, descripcion FROM roles WHERE id_rol = %s",
                (user_id,)
            )
            result = cursor.fetchone()
            
            if result:
                content = {
                    'id_rol': result[0],
                    'nombre_rol': result[1],
                    'descripcion': result[2]
                }
                json_data = jsonable_encoder(content)            
                return json_data
            else:
                raise HTTPException(status_code=404, detail="Rol not found")  
                
        except psycopg2.Error as err:
            print(err)
        finally:
            conn.close()
       
    def get_users(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id_rol, nombre_rol, descripcion FROM roles"
            )
            result = cursor.fetchall()
            payload = []
            content = {} 

            for data in result:
                content = {
                    'id_rol': data[0],
                    'nombre_rol': data[1],
                    'descripcion': data[2]
                }
                payload.append(content)
                content = {}

            json_data = jsonable_encoder(payload)        
            if result:
               return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="Rol not found")  
                
        except psycopg2.Error as err:
            print(err)
        finally:
            conn.close()