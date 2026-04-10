-- =====================================
-- ROLES
-- =====================================
CREATE TABLE IF NOT EXISTS roles (
    id_rol SERIAL PRIMARY KEY,
    nombre_rol VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT
);

INSERT INTO roles (nombre_rol) VALUES 
('ADMIN'),
('ESTUDIANTE'),
('DOCENTE')
ON CONFLICT (nombre_rol) DO NOTHING;

-- =====================================
-- PROGRAMAS
-- =====================================
CREATE TABLE IF NOT EXISTS programas (
    id_programa SERIAL PRIMARY KEY,
    nombre_programa VARCHAR(100) UNIQUE NOT NULL,
    descripcion TEXT
);

-- =====================================
-- DEPENDENCIAS
-- =====================================
CREATE TABLE IF NOT EXISTS dependencias (
    id_dependencia SERIAL PRIMARY KEY,
    nombre_dependencia VARCHAR(100) UNIQUE NOT NULL,
    descripcion TEXT
);

-- =====================================
-- TIPOS PQRS
-- =====================================
CREATE TABLE IF NOT EXISTS tipospqrs (
    id_tipospqrs SERIAL PRIMARY KEY,
    nombre_tipospqrs VARCHAR(100) UNIQUE NOT NULL,
    descripcion TEXT
);

-- =====================================
-- ESTADOS
-- =====================================
CREATE TABLE IF NOT EXISTS estados (
    id_estado SERIAL PRIMARY KEY,
    nombre_estado VARCHAR(100) UNIQUE NOT NULL
);

-- =====================================
-- PRIORIDADES
-- =====================================
CREATE TABLE IF NOT EXISTS prioridades (
    id_prioridad SERIAL PRIMARY KEY,
    nombre_prioridad VARCHAR(100) UNIQUE NOT NULL,
    nivel INTEGER NOT NULL
);

-- =====================================
-- USUARIOS
-- =====================================
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo_documento VARCHAR(10) NOT NULL,
    documento VARCHAR(50) UNIQUE NOT NULL,
    correo VARCHAR(100) UNIQUE,
    telefono VARCHAR(20),
    id_rol INTEGER REFERENCES roles(id_rol),
    id_programa INTEGER REFERENCES programas(id_programa),
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================
-- PQRS
-- =====================================
CREATE TABLE IF NOT EXISTS pqrs (
    id_pqrs SERIAL PRIMARY KEY,
    radicado VARCHAR(100) UNIQUE NOT NULL,
    descripcion TEXT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_limite TIMESTAMP,
    id_usuario INTEGER NOT NULL REFERENCES usuarios(id_usuario),
    id_dependencia INTEGER REFERENCES dependencias(id_dependencia),
    id_tipospqrs INTEGER REFERENCES tipospqrs(id_tipospqrs),
    id_estado INTEGER REFERENCES estados(id_estado),
    id_prioridad INTEGER REFERENCES prioridades(id_prioridad)
);

-- =====================================
-- RESPUESTAS (SIN USUARIO)
-- =====================================
CREATE TABLE IF NOT EXISTS respuestas (
    id_respuesta SERIAL PRIMARY KEY,
    mensaje TEXT NOT NULL,
    fecha_respuesta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_pqrs INTEGER NOT NULL REFERENCES pqrs(id_pqrs)
);

-- =====================================
-- SEGUIMIENTO PQRS
-- =====================================
CREATE TABLE IF NOT EXISTS seguimiento_pqrs (
    id_seguimiento SERIAL PRIMARY KEY,
    id_pqrs INTEGER NOT NULL REFERENCES pqrs(id_pqrs),
    comentario TEXT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_estado INTEGER REFERENCES estados(id_estado),
    id_usuario INTEGER REFERENCES usuarios(id_usuario)
);

-- =====================================
-- HISTORIAL DE ESTADOS
-- =====================================
CREATE TABLE IF NOT EXISTS historial_estados (
    id_historial SERIAL PRIMARY KEY,
    id_pqrs INTEGER NOT NULL REFERENCES pqrs(id_pqrs),
    id_estado_anterior INTEGER REFERENCES estados(id_estado),
    id_estado_nuevo INTEGER REFERENCES estados(id_estado),
    cambiado_por INTEGER REFERENCES usuarios(id_usuario),
    fecha_cambio TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================
-- ÍNDICES (RENDIMIENTO)
-- =====================================
CREATE INDEX IF NOT EXISTS idx_pqrs_usuario ON pqrs(id_usuario);
CREATE INDEX IF NOT EXISTS idx_pqrs_estado ON pqrs(id_estado);
CREATE INDEX IF NOT EXISTS idx_seguimiento_pqrs ON seguimiento_pqrs(id_pqrs);

-- =====================================
-- VISTA USUARIOS (SIN IDs)
-- =====================================
CREATE OR REPLACE VIEW vista_usuarios AS
SELECT 
    u.id_usuario,
    u.nombre,
    u.tipo_documento,
    u.documento,
    u.correo,
    u.telefono,
    r.nombre_rol AS rol,
    p.nombre_programa AS programa,
    CASE 
        WHEN r.nombre_rol = 'ADMIN' THEN 'Administrador'
        WHEN r.nombre_rol = 'ESTUDIANTE' THEN 'Estudiante'
        WHEN r.nombre_rol = 'DOCENTE' THEN 'Docente'
        ELSE 'Usuario'
    END AS tipo_usuario,
    u.activo,
    u.created_at
FROM usuarios u
LEFT JOIN roles r ON u.id_rol = r.id_rol
LEFT JOIN programas p ON u.id_programa = p.id_programa;

-- =====================================
-- VISTA PQRS COMPLETA
-- =====================================
CREATE OR REPLACE VIEW vista_pqrs AS
SELECT 
    pq.id_pqrs,
    pq.radicado,
    pq.descripcion,
    pq.fecha_creacion,
    pq.fecha_limite,
    u.nombre AS usuario,
    r.nombre_rol AS rol_usuario,
    CASE 
        WHEN r.nombre_rol = 'ADMIN' THEN 'Administrador'
        WHEN r.nombre_rol = 'ESTUDIANTE' THEN 'Estudiante'
        WHEN r.nombre_rol = 'DOCENTE' THEN 'Docente'
        ELSE 'Usuario'
    END AS tipo_usuario,
    d.nombre_dependencia AS dependencia,
    t.nombre_tipospqrs AS tipo_pqrs,
    e.nombre_estado AS estado,
    pr.nombre_prioridad AS prioridad
FROM pqrs pq
LEFT JOIN usuarios u ON pq.id_usuario = u.id_usuario
LEFT JOIN roles r ON u.id_rol = r.id_rol
LEFT JOIN dependencias d ON pq.id_dependencia = d.id_dependencia
LEFT JOIN tipospqrs t ON pq.id_tipospqrs = t.id_tipospqrs
LEFT JOIN estados e ON pq.id_estado = e.id_estado
LEFT JOIN prioridades pr ON pq.id_prioridad = pr.id_prioridad;

-- =====================================
-- VISTA SEGUIMIENTO
-- =====================================
CREATE OR REPLACE VIEW vista_seguimiento AS
SELECT 
    s.id_seguimiento,
    pq.radicado,
    s.comentario,
    s.fecha,
    e.nombre_estado AS estado,
    u.nombre AS usuario,
    r.nombre_rol AS rol_usuario
FROM seguimiento_pqrs s
LEFT JOIN pqrs pq ON s.id_pqrs = pq.id_pqrs
LEFT JOIN estados e ON s.id_estado = e.id_estado
LEFT JOIN usuarios u ON s.id_usuario = u.id_usuario
LEFT JOIN roles r ON u.id_rol = r.id_rol;

-- =====================================
-- VISTA HISTORIAL
-- =====================================
CREATE OR REPLACE VIEW vista_historial AS
SELECT 
    h.id_historial,
    pq.radicado,
    e1.nombre_estado AS estado_anterior,
    e2.nombre_estado AS estado_nuevo,
    u.nombre AS cambiado_por,
    r.nombre_rol AS rol_usuario,
    h.fecha_cambio
FROM historial_estados h
LEFT JOIN pqrs pq ON h.id_pqrs = pq.id_pqrs
LEFT JOIN estados e1 ON h.id_estado_anterior = e1.id_estado
LEFT JOIN estados e2 ON h.id_estado_nuevo = e2.id_estado
LEFT JOIN usuarios u ON h.cambiado_por = u.id_usuario
LEFT JOIN roles r ON u.id_rol = r.id_rol;