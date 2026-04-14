from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from ..config.db_config import get_db_connection
from ..models.pqrs_model import Pqrs

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
            cur.execute("SELECT * FROM pqrs ORDER BY id_pqrs DESC")
            rows = cur.fetchall()
            return jsonable_encoder([dict(row) for row in rows])
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
            return jsonable_encoder(dict(r))
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def update_pqrs(self, id_pqrs: int, pqrs: Pqrs):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                """UPDATE pqrs
                   SET radicado=%s, descripcion=%s, fecha_limite=%s,
                       id_dependencia=%s, id_tipospqrs=%s, id_estado=%s,
                       id_prioridad=%s, updated_at=CURRENT_TIMESTAMP
                   WHERE id_pqrs=%s""",
                (
                    pqrs.radicado,
                    pqrs.descripcion,
                    pqrs.fecha_limite,
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

    def patch_estado(self, id_pqrs: int, data: dict):
        """Actualiza solo el id_estado y/o estado (activo) de un PQRS."""
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            sets, vals = [], []
            if "id_estado" in data:
                sets.append("id_estado=%s")
                vals.append(data["id_estado"])
            if "estado" in data:
                sets.append("estado=%s::boolean")
                vals.append(bool(data["estado"]))
            if not sets:
                raise HTTPException(status_code=400, detail="Ningún campo para actualizar")
            sets.append("updated_at=CURRENT_TIMESTAMP")
            vals.append(id_pqrs)
            cur.execute(f"UPDATE pqrs SET {', '.join(sets)} WHERE id_pqrs=%s", vals)
            if cur.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="PQRS no encontrado")
            conn.commit()
            return {"resultado": "Estado actualizado"}
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