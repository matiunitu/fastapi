#!/usr/bin/env python3
"""Update demo user nelson"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "app"))

from config.db_config import get_db_connection
import hashlib

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

    # Simple hash para contraseña (para testing)
    password_hash = hashlib.sha256("1234".encode()).hexdigest()
    print(f'✓ Hash generado: {password_hash[:16]}...')

    # Actualizar usuario nelson si existe, o crearlo
    cur.execute('SELECT id_usuario FROM usuarios WHERE LOWER(nombre) = %s', ('nelson',))
    existing = cur.fetchone()
    
    if existing:
        cur.execute('''
            UPDATE usuarios 
            SET password_hash = %s, id_rol = %s, estado = 1
            WHERE LOWER(nombre) = %s
        ''', (password_hash, admin_rol_id, 'nelson'))
        conn.commit()
        print(f'✓ Usuario nelson actualizado (id={existing["id_usuario"]})')
    else:
        # Obtener programa
        cur.execute('SELECT id_programa FROM programas LIMIT 1')
        prog = cur.fetchone()
        if not prog:
            print('ERROR: No existe programa')
            conn.close()
            sys.exit(1)
        
        prog_id = prog['id_programa']
        cur.execute('''
            INSERT INTO usuarios (nombre, documento, correo, telefono, id_rol, id_programa, password_hash, estado, activo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 1, TRUE)
        ''', ('nelson', '00000001', 'nelson@admin.com', '000-0000', admin_rol_id, prog_id, password_hash))
        conn.commit()
        print('✓ Usuario nelson creado')

    print('  - Usuario: nelson')
    print('  - Contraseña: 1234')
    print('  - Rol: Administrador')

    conn.close()
    print('\n✅ Demo user ready!')
except Exception as e:
    print(f'ERROR: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
