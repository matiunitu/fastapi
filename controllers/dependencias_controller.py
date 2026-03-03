import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.dependencias_model import Dependencias
from fastapi.encoders import jsonable_encoder

class DependenciasController:

    def create_dependencia(self, dependencia: Dependencias):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO dependencias (nombre_dependencia, descripcion) VALUES (%s, %s)",
                (dependencia.nombre_dependencia, dependencia.descripcion)
            )

            conn.commit()
            cursor.close()
            conn.close()

            return {"resultado": "Dependencia creada"}

        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))


    def get_dependencia(self, id_dependencia: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM dependencias WHERE id_dependencia = %s",
                (id_dependencia,)
            )

            result = cursor.fetchone()

            if result:
                content = {
                    'id_dependencia': result[0],
                    'nombre_dependencia': result[1],
                    'descripcion': result[2],
                }

                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="Dependencia not found")

        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))


    def get_dependencias(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM dependencias")
            result = cursor.fetchall()

            payload = []

            for data in result:
                payload.append({
                    'id_dependencia': data[0],
                    'nombre_dependencia': data[1],
                    'descripcion': data[2],
                })

            return jsonable_encoder(payload)

        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))