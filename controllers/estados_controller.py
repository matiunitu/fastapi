import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.estados_model import Estados
from fastapi.encoders import jsonable_encoder

class EstadosController:
        
    def create_estados(self, user: Estados):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO estados (nombre_estado) VALUES (%s)",
                (user.nombre_estado,)
            )
            conn.commit()
            return {"resultado": "Estado creado"}
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
                "SELECT id_estado, nombre_estado FROM estados WHERE id_estado = %s",
                (user_id,)
            )
            result = cursor.fetchone()
            
            if result:
                content = {
                    'id_estado': result[0],
                    'nombre_estado': result[1]
                }
                json_data = jsonable_encoder(content)            
                return json_data
            else:
                raise HTTPException(status_code=404, detail="Estado not found")  
                
        except psycopg2.Error as err:
            print(err)
        finally:
            conn.close()
       
    def get_users(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id_estado, nombre_estado FROM estados")
            result = cursor.fetchall()
            payload = []
            content = {} 

            for data in result:
                content = {
                    'id_estado': data[0],
                    'nombre_estado': data[1]
                }
                payload.append(content)
                content = {}

            json_data = jsonable_encoder(payload)        
            if result:
               return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="Estado not found")  
                
        except psycopg2.Error as err:
            print(err)
        finally:
            conn.close()