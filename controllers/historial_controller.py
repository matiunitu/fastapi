import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.historial_model import Historial
from fastapi.encoders import jsonable_encoder

class HistorialController:
        
    def create_historial(self, user: Historial):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO historial 
                (fecha_cambio, id_pqrs, id_estado_anterior, id_estado_nuevo, cambiado_por) 
                VALUES (%s, %s, %s, %s, %s)""",
                (
                    user.fecha_cambio,
                    user.id_pqrs,
                    user.id_estado_anterior,
                    user.id_estado_nuevo,
                    user.cambiado_por
                )
            )
            conn.commit()
            return {"resultado": "Historial creado"}
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
                """SELECT id_historial, fecha_cambio, id_pqrs,
                          id_estado_anterior, id_estado_nuevo, cambiado_por
                   FROM historial WHERE id_historial = %s""",
                (user_id,)
            )
            result = cursor.fetchone()
            
            if result:
                content = {
                    'id_historial': result[0],
                    'fecha_cambio': result[1],
                    'id_pqrs': result[2],
                    'id_estado_anterior': result[3],
                    'id_estado_nuevo': result[4],
                    'cambiado_por': result[5]
                }
                json_data = jsonable_encoder(content)            
                return json_data
            else:
                raise HTTPException(status_code=404, detail="Historial not found")  
                
        except psycopg2.Error as err:
            print(err)
        finally:
            conn.close()
       
    def get_users(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id_historial, fecha_cambio, id_pqrs,
                          id_estado_anterior, id_estado_nuevo, cambiado_por
                   FROM historial"""
            )
            result = cursor.fetchall()
            payload = []
            content = {} 

            for data in result:
                content = {
                    'id_historial': data[0],
                    'fecha_cambio': data[1],
                    'id_pqrs': data[2],
                    'id_estado_anterior': data[3],
                    'id_estado_nuevo': data[4],
                    'cambiado_por': data[5]
                }
                payload.append(content)
                content = {}

            json_data = jsonable_encoder(payload)        
            if result:
               return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="Historial not found")  
                
        except psycopg2.Error as err:
            print(err)
        finally:
            conn.close()