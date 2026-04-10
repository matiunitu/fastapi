#!/usr/bin/env python3
"""Verificar y crear usuario nelson si no existe"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "app"))

from config.db_config import get_db_connection
from config.jwt_config import hash_password

conn = get_db_connection()
cur = conn.cursor()

# Verificar usuario nelson
cur.execute("SELECT id_usuario, nombre, password_hash, estado FROM usuarios WHERE LOWER(nombre) = 'nelson'")
user = cur.fetchone()

if user:
    print(f"✓ Usuario encontrado: {user['nombre']} (id={user['id_usuario']}, estado={user['estado']})")
    print(f"  - Password hash: {'SET' if user['password_hash'] else 'NOT SET'}")
else:
    print("✗ Usuario nelson NO existe. Creando...")
    
    # Obtener rol admin
    cur.execute("SELECT id_rol FROM roles WHERE LOWER(nombre_rol) = 'admin'")
    admin_role = cur.fetchone()
    if not admin_role:
        print("ERROR: Rol admin no existe")
        conn.close()
        sys.exit(1)
    
    admin_rol_id = admin_role['id_rol']
    print(f"  - Rol admin id: {admin_rol_id}")
    
    # Obtener o crear programa
    cur.execute("SELECT id_programa FROM programas LIMIT 1")
    prog = cur.fetchone()
    if not prog:
        print("  - Creando programa demo...")
        cur.execute("INSERT INTO facultades(nombre_facultad, descripcion, estado) VALUES ('Demo', 'Demo', 1) RETURNING id_facultad")
        fac = cur.fetchone()
        cur.execute("INSERT INTO programas(nombre_programa, descripcion, id_facultad, estado) VALUES ('Ing. Demo', 'Demo', %s, 1) RETURNING id_programa", (fac['id_facultad'],))
        prog = cur.fetchone()
        conn.commit()
    
    prog_id = prog['id_programa']
    hashed = hash_password("1234")
    
    cur.execute("""
        INSERT INTO usuarios (nombre, documento, correo, telefono, id_rol, id_programa, password_hash, estado, activo)
        VALUES (%s, %s, %s, %s, %s, %s, %s, 1, TRUE)
    """, ("nelson", "00000001", "nelson@admin.com", "000-0000", admin_rol_id, prog_id, hashed))
    conn.commit()
    print("✓ Usuario nelson creado exitosamente")
    print("  - Usuario: nelson")
    print("  - Contraseña: 1234")
    print("  - Rol: admin")

conn.close()
print("\n✓ Verificación completada")
