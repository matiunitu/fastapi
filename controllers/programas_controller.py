import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.programas_model import Programas
from fastapi.encoders import jsonable_encoder

class ProgramasController:
        
    def create_programas(self, programas: Programas):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (nombre,apellido,cedula,edad,usuario,contrasena) VALUES (%s, %s, %s, %s, %s ,%s)", (programas.nombre, programas.apellido, programas.cedula, programas.edad, programas.usuario, programas.contrasena))
            conn.commit()
            conn.close()
            return {"resultado": "Programa creado"}
        except psycopg2.Error as err:
            print(err)
            # Si falla el INSERT, los datos no quedan guardados parcialmente en la base de datos
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            conn.rollback()
        finally:
            conn.close()
        

    def get_programas(self, programas_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM programas WHERE id = %s", (programas_id,))
            result = cursor.fetchone()
            payload = []
            content = {} 
            
            content={
                'id_programa': result[0],
                'nombre_programa': result[1],
                'nivel': result[2]
            }
            payload.append(content)
            
            json_data = jsonable_encoder(content)            
            if result:
               return  json_data
            else:
                ##Esto interrumpe la ejecución y responde al cliente con un código 404
                ## comunica al cliente de la API qué pasó (error HTTP).
                ##código 404,comportamiento correcto según las reglas HTTP
                raise HTTPException(status_code=404, detail="Programas not found")  
                
        except psycopg2.Error as err:
            print(err)
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            ##Maneja el estado de la transacción en la base de datos.Si un INSERT, UPDATE o DELETE falla dentro de una transacción, rollback() revierte esos cambios.
            conn.rollback()
        finally:
            conn.close()
       
    def get_programass(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM programas")
            result = cursor.fetchall()
            payload = []
            content = {} 
            for data in result:
                content={
                    'id_programa':data[0],
                    'nombre_programa':data[1],
                    'descripcion':data[2],
                }
                payload.append(content)
                content = {}
            json_data = jsonable_encoder(payload)        
            if result:
               return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="Programas not found")  
                
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()
    
    
       

##programas_controller = ProgramasController()