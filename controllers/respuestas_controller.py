import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.respuestas_model import Respuestas
from fastapi.encoders import jsonable_encoder

class RespuestasController:
        
    def create_respuestas(self, user: Respuestas):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO respuestas 
                (mensaje, fecha_respuesta, id_pqrs, id_usuario) 
                VALUES (%s, %s, %s, %s)""",
                (
                    user.mensaje,
                    user.fecha_respuesta,
                    user.id_pqrs,
                    user.id_usuario
                )
            )
            conn.commit()
            return {"resultado": "Respuesta creada"}
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
                """SELECT id_respuesta, mensaje, fecha_respuesta, id_pqrs, id_usuario
                   FROM respuestas WHERE id_respuesta = %s""",
                (user_id,)
            )
            result = cursor.fetchone()
            
            if result:
                content = {
                    'id_respuesta': result[0],
                    'mensaje': result[1],
                    'fecha_respuesta': result[2],
                    'id_pqrs': result[3],
                    'id_usuario': result[4]
                }
                json_data = jsonable_encoder(content)            
                return json_data
            else:
                raise HTTPException(status_code=404, detail="Respuesta not found")  
                
        except psycopg2.Error as err:
            print(err)
        finally:
            conn.close()
       
    def get_users(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id_respuesta, mensaje, fecha_respuesta, id_pqrs, id_usuario
                   FROM respuestas"""
            )
            result = cursor.fetchall()
            payload = []
            content = {} 

            for data in result:
                content = {
                    'id_respuesta': data[0],
                    'mensaje': data[1],
                    'fecha_respuesta': data[2],
                    'id_pqrs': data[3],
                    'id_usuario': data[4]
                }
                payload.append(content)
                content = {}

            json_data = jsonable_encoder(payload)        
            if result:
               return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="Respuesta not found")  
                
        except psycopg2.Error as err:
            print(err)
        finally:
            conn.close()