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
            id_pqrs = cur.fetchone()['id_pqrs']
            conn.commit()
            return {"id_pqrs": id_pqrs, "resultado": "PQRS creado"}
        except Exception as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_pqrs_all(self):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM pqrs")
            rows = cur.fetchall()
            return rows
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_pqrs(self, id_pqrs: int):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM pqrs WHERE id_pqrs=%s", (id_pqrs,))
            r = cur.fetchone()
            if not r:
                raise HTTPException(status_code=404, detail="PQRS no encontrado")
            return r
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def update_pqrs(self, id_pqrs: int, pqrs: Pqrs):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                """UPDATE pqrs SET radicado=%s, descripcion=%s, fecha_creacion=%s, fecha_limite=%s,
                   id_usuario=%s, id_dependencia=%s, id_tipospqrs=%s, id_estado=%s, id_prioridad=%s
                   WHERE id_pqrs=%s""",
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
                    id_pqrs
                )
            )
            if cur.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="PQRS no encontrado")
            conn.commit()
            return {"resultado": "PQRS actualizado"}
        except Exception as err:
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
        except Exception as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()