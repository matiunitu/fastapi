import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.prioridades_model import Prioridades
from fastapi.encoders import jsonable_encoder

class PrioridadesController:
        
    def create_prioridades(self, user: Prioridades):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO prioridades (nombre_prioridad, nivel) VALUES (%s, %s)",
                (
                    user.nombre_prioridad,
                    user.nivel
                )
            )
            conn.commit()
            return {"resultado": "Prioridad creada"}
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
                "SELECT id_prioridad, nombre_prioridad, nivel FROM prioridades WHERE id_prioridad = %s",
                (user_id,)
            )
            result = cursor.fetchone()
            
            if result:
                content = {
                    'id_prioridad': result[0],
                    'nombre_prioridad': result[1],
                    'nivel': result[2]
                }
                json_data = jsonable_encoder(content)            
                return json_data
            else:
                raise HTTPException(status_code=404, detail="Prioridad not found")  
                
        except psycopg2.Error as err:
            print(err)
        finally:
            conn.close()
       
    def get_users(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id_prioridad, nombre_prioridad, nivel FROM prioridades"
            )
            result = cursor.fetchall()
            payload = []
            content = {} 

            for data in result:
                content = {
                    'id_prioridad': data[0],
                    'nombre_prioridad': data[1],
                    'nivel': data[2]
                }
                payload.append(content)
                content = {}

            json_data = jsonable_encoder(payload)        
            if result:
               return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="Prioridad not found")  
                
        except psycopg2.Error as err:
            print(err)
        finally:
            conn.close()