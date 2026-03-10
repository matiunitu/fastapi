import psycopg2
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.db_config import get_db_connection
from models.pqrs_model import Pqrs


class PqrsController:
    def create_pqrs(self, pqrs: Pqrs):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                """INSERT INTO pqrs (radicado, descripcion, fecha_creacion, fecha_limite,
                   id_usuario, id_dependencia, id_tipospqrs, id_estado, id_prioridad)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id_pqrs""",
                (
                    pqrs.radicado,
                    pqrs.descripcion,
                    pqrs.fecha_creacion,
                    pqrs.fecha_limite,
                    pqrs.id_usuario,
                    pqrs.id_dependencia,
                    pqrs.id_tipospqrs,
                    pqrs.id_estado,
                    pqrs.id_prioridad,
                ),
            )
            id_pqrs = cur.fetchone()[0]
            conn.commit()
            return {"id_pqrs": id_pqrs, "resultado": "PQRS creado"}
        except psycopg2.IntegrityError as err:
            conn.rollback()
            raise HTTPException(status_code=400, detail=f"Integrity error: {str(err)}")
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_pqrs(self, id_pqrs: int):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT id_pqrs, radicado, descripcion, fecha_creacion, fecha_limite, id_usuario, id_dependencia, id_tipospqrs, id_estado, id_prioridad FROM pqrs WHERE id_pqrs=%s", (id_pqrs,))
            r = cur.fetchone()
            if not r:
                raise HTTPException(status_code=404, detail="PQRS no encontrado")
            return jsonable_encoder({
                "id_pqrs": r[0],
                "radicado": r[1],
                "descripcion": r[2],
                "fecha_creacion": r[3],
                "fecha_limite": r[4],
                "id_usuario": r[5],
                "id_dependencia": r[6],
                "id_tipospqrs": r[7],
                "id_estado": r[8],
                "id_prioridad": r[9],
            })
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_pqrs_all(self):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT id_pqrs, radicado, descripcion, fecha_creacion, fecha_limite, id_usuario, id_dependencia, id_tipospqrs, id_estado, id_prioridad FROM pqrs")
            rows = cur.fetchall()
            return jsonable_encoder([
                {
                    "id_pqrs": r[0],
                    "radicado": r[1],
                    "descripcion": r[2],
                    "fecha_creacion": r[3],
                    "fecha_limite": r[4],
                    "id_usuario": r[5],
                    "id_dependencia": r[6],
                    "id_tipospqrs": r[7],
                    "id_estado": r[8],
                    "id_prioridad": r[9],
                }
                for r in rows
            ])
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def update_pqrs(self, id_pqrs: int, pqrs: Pqrs):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "UPDATE pqrs SET radicado=%s, descripcion=%s, fecha_creacion=%s, fecha_limite=%s, id_usuario=%s, id_dependencia=%s, id_tipospqrs=%s, id_estado=%s, id_prioridad=%s WHERE id_pqrs=%s",
                (
                    pqrs.radicado,
                    pqrs.descripcion,
                    pqrs.fecha_creacion,
                    pqrs.fecha_limite,
                    pqrs.id_usuario,
                    pqrs.id_dependencia,
                    pqrs.id_tipospqrs,
                    pqrs.id_estado,
                    pqrs.id_prioridad,
                    id_pqrs,
                ),
            )
            if cur.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="PQRS no encontrado")
            conn.commit()
            return {"resultado": "PQRS actualizado"}
        except psycopg2.IntegrityError as err:
            conn.rollback()
            raise HTTPException(status_code=400, detail=f"Integrity error: {str(err)}")
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def delete_pqrs(self, id_pqrs: int):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM pqrs WHERE id_pqrs=%s", (id_pqrs,))
            if cur.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="PQRS no encontrado")
            conn.commit()
            return {"resultado": "PQRS eliminado"}
        except psycopg2.IntegrityError as err:
            conn.rollback()
            raise HTTPException(status_code=400, detail=f"Integrity error: {str(err)}")
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()
