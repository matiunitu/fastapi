import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.tipospqrs_model import Tipospqrs
from fastapi.encoders import jsonable_encoder

class TipospqrsController:
    
    def create_tipospqrs(self, data: Tipospqrs):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO tipospqrs
                   (nombre_tipospqrs, descripcion)
                   VALUES (%s, %s)""",
                (data.nombre_tipospqrs, data.descripcion)
            )
            conn.commit()
            return {"resultado": "Tipo PQRS creado"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_tipospqrs(self, id_tipospqrs: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id_tipospqrs, nombre_tipospqrs, descripcion
                   FROM tipospqrs
                   WHERE id_tipospqrs = %s""",
                (id_tipospqrs,)
            )
            result = cursor.fetchone()

            if result:
                content = {
                    "id_tipospqrs": result[0],
                    "nombre_tipospqrs": result[1],
                    "descripcion": result[2]
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Tipo PQRS no encontrado")

        finally:
            conn.close()

    def get_tipospqrs_all(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id_tipospqrs, nombre_tipospqrs, descripcion
                   FROM tipospqrs"""
            )
            result = cursor.fetchall()

            payload = []
            for data in result:
                payload.append({
                    "id_tipospqrs": data[0],
                    "nombre_tipospqrs": data[1],
                    "descripcion": data[2]
                })

            return jsonable_encoder(payload)

        finally:
            conn.close()