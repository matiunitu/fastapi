import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.pqrs_model import Pqrs
from fastapi.encoders import jsonable_encoder

class PqrsController:
        
    def create_pqrs(self, user: Pqrs):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO pqrs 
                (radicado, descripcion, fecha_creacion, fecha_limite,
                 id_usuario, id_dependencia, id_tiposqrs, id_estado, id_prioridad)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    user.radicado,
                    user.descripcion,
                    user.fecha_creacion,
                    user.fecha_limite,
                    user.id_usuario,
                    user.id_dependencia,
                    user.id_tiposqrs,
                    user.id_estado,
                    user.id_prioridad
                )
            )
            conn.commit()
            return {"resultado": "PQRS creado"}
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
                """SELECT id_pqrs, radicado, descripcion, fecha_creacion, fecha_limite,
                          id_usuario, id_dependencia, id_tiposqrs, id_estado, id_prioridad
                   FROM pqrs WHERE id_pqrs = %s""",
                (user_id,)
            )
            result = cursor.fetchone()
            
            if result:
                content = {
                    'id_pqrs': result[0],
                    'radicado': result[1],
                    'descripcion': result[2],
                    'fecha_creacion': result[3],
                    'fecha_limite': result[4],
                    'id_usuario': result[5],
                    'id_dependencia': result[6],
                    'id_tiposqrs': result[7],
                    'id_estado': result[8],
                    'id_prioridad': result[9]
                }
                json_data = jsonable_encoder(content)            
                return json_data
            else:
                raise HTTPException(status_code=404, detail="PQRS not found")  
                
        except psycopg2.Error as err:
            print(err)
        finally:
            conn.close()
       
    def get_users(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id_pqrs, radicado, descripcion, fecha_creacion, fecha_limite,
                          id_usuario, id_dependencia, id_tiposqrs, id_estado, id_prioridad
                   FROM pqrs"""
            )
            result = cursor.fetchall()
            payload = []
            content = {} 

            for data in result:
                content = {
                    'id_pqrs': data[0],
                    'radicado': data[1],
                    'descripcion': data[2],
                    'fecha_creacion': data[3],
                    'fecha_limite': data[4],
                    'id_usuario': data[5],
                    'id_dependencia': data[6],
                    'id_tiposqrs': data[7],
                    'id_estado': data[8],
                    'id_prioridad': data[9]
                }
                payload.append(content)
                content = {}

            json_data = jsonable_encoder(payload)        
            if result:
               return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="PQRS not found")  
                
        except psycopg2.Error as err:
            print(err)
        finally:
            conn.close()