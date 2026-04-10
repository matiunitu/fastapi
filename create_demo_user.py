#!/usr/bin/env python3
"""Create demo user nelson with correct role"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "app"))

from config.db_config import get_db_connection
from config.jwt_config import hash_password

try:
    conn = get_db_connection()
    cur = conn.cursor()

    # Obtener rol Administrador
    cur.execute("SELECT id_rol FROM roles WHERE LOWER(nombre_rol) = 'administrador'")
    admin_role = cur.fetchone()
    if not admin_role:
        print('ERROR: No existe rol Administrador')
        conn.close()
        sys.exit(1)

    admin_rol_id = admin_role['id_rol']
    print(f'✓ Rol Administrador encontrado: id={admin_rol_id}')

    # Obtener o crear programa
    cur.execute('SELECT id_programa FROM programas LIMIT 1')
    prog = cur.fetchone()
    if not prog:
        cur.execute('INSERT INTO facultades(nombre_facultad, descripcion, estado) VALUES (%s, %s, 1) RETURNING id_facultad', ('Demo', 'Demo'))
        fac = cur.fetchone()
        cur.execute('INSERT INTO programas(nombre_programa, descripcion, id_facultad, estado) VALUES (%s, %s, %s, 1) RETURNING id_programa', ('Ing. Demo', 'Demo', fac['id_facultad']))
        prog = cur.fetchone()
        conn.commit()
        print(f'✓ Programa creado: id={prog["id_programa"]}')
    else:
        print(f'✓ Programa encontrado: id={prog["id_programa"]}')

    prog_id = prog['id_programa']

    # Eliminar usuario anterior (si existe)
    cur.execute('DELETE FROM usuarios WHERE LOWER(nombre) = %s', ('nelson',))
    conn.commit()

    # Crear usuario nelson
    hashed = hash_password('1234')
    cur.execute('''
        INSERT INTO usuarios (nombre, documento, correo, telefono, id_rol, id_programa, password_hash, estado, activo)
        VALUES (%s, %s, %s, %s, %s, %s, %s, 1, TRUE)
    ''', ('nelson', '00000001', 'nelson@admin.com', '000-0000', admin_rol_id, prog_id, hashed))
    conn.commit()
    print('✓ Usuario nelson creado exitosamente')
    print('  - Usuario: nelson')
    print('  - Contraseña: 1234')
    print('  - Rol: Administrador')

    conn.close()
    print('\n✅ Demo user ready!')
except Exception as e:
    print(f'ERROR: {e}')
    sys.exit(1)
