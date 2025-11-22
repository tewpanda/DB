PRAGMA foreign_keys = ON;

-- 1. Tabla Equipo
CREATE TABLE IF NOT EXISTS Equipo (
    id_equipo INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    logo TEXT,
    fecha_creacion DATE NOT NULL,
    region TEXT NOT NULL CHECK (region IN ('LAS', 'LAN', 'EUW', 'NA', 'KR', 'BR', 'EUNE', 'JP', 'ME', 'OCE', 'RU', 'SEA', 'TR', 'TW', 'VN'))
);

-- 2. Tabla Torneo
CREATE TABLE IF NOT EXISTS Torneo (
    id_torneo INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    formato TEXT NOT NULL CHECK (formato IN ('Round Robin', 'Eliminación Simple', 'Doble Eliminación', 'Grupos')),
    num_equipos INTEGER NOT NULL CHECK (num_equipos > 1)
);

-- 3. Tabla Jugador
CREATE TABLE IF NOT EXISTS Jugador (
    id_jugador INTEGER PRIMARY KEY AUTOINCREMENT,
    nickname TEXT NOT NULL UNIQUE,
    nombre_real TEXT NOT NULL,
    rol TEXT NOT NULL CHECK (rol IN ('Top', 'Jungle', 'Mid', 'ADC', 'Support', 'Sustituto')),
    region TEXT NOT NULL,
    id_equipo INTEGER,
    FOREIGN KEY (id_equipo) REFERENCES Equipo(id_equipo) ON DELETE SET NULL
);

-- 4. Tabla Inscripcion
CREATE TABLE IF NOT EXISTS Inscripcion (
    id_inscripcion INTEGER PRIMARY KEY AUTOINCREMENT,
    id_equipo INTEGER NOT NULL,
    id_torneo INTEGER NOT NULL,
    fecha_inscripcion DATETIME DEFAULT (CURRENT_TIMESTAMP),
    estado TEXT NOT NULL CHECK (estado IN ('Pendiente', 'Aceptada', 'Rechazada', 'Retirada')),
    UNIQUE (id_equipo, id_torneo),
    FOREIGN KEY (id_equipo) REFERENCES Equipo(id_equipo) ON DELETE CASCADE,
    FOREIGN KEY (id_torneo) REFERENCES Torneo(id_torneo) ON DELETE CASCADE
);

-- 5. Tabla Partida
CREATE TABLE IF NOT EXISTS Partida (
    id_partida INTEGER PRIMARY KEY AUTOINCREMENT,
    id_torneo INTEGER NOT NULL,
    fase TEXT NOT NULL,
    fecha_hora DATETIME NOT NULL,
    equipo_local_id INTEGER NOT NULL,
    equipo_visitante_id INTEGER NOT NULL,
    CHECK (equipo_local_id <> equipo_visitante_id),
    FOREIGN KEY (id_torneo) REFERENCES Torneo(id_torneo) ON DELETE CASCADE,
    FOREIGN KEY (equipo_local_id) REFERENCES Equipo(id_equipo) ON DELETE RESTRICT,
    FOREIGN KEY (equipo_visitante_id) REFERENCES Equipo(id_equipo) ON DELETE RESTRICT
);

-- 6. Tabla Resultado
CREATE TABLE IF NOT EXISTS Resultado (
    id_resultado INTEGER PRIMARY KEY AUTOINCREMENT,
    id_partida INTEGER NOT NULL UNIQUE,
    equipo_ganador_id INTEGER NOT NULL,
    score_ganador INTEGER NOT NULL,
    score_perdedor INTEGER NOT NULL,
    duracion_minutos INTEGER,
    FOREIGN KEY (id_partida) REFERENCES Partida(id_partida) ON DELETE CASCADE,
    FOREIGN KEY (equipo_ganador_id) REFERENCES Equipo(id_equipo)
);

-- 7. Tabla Estadistica_Jugador
CREATE TABLE IF NOT EXISTS Estadistica_Jugador (
    id_estadistica INTEGER PRIMARY KEY AUTOINCREMENT,
    id_partida INTEGER NOT NULL,
    id_jugador INTEGER NOT NULL,
    kills INTEGER NOT NULL DEFAULT 0,
    deaths INTEGER NOT NULL DEFAULT 0,
    assists INTEGER NOT NULL DEFAULT 0,
    oro INTEGER NOT NULL DEFAULT 0,
    dano INTEGER NOT NULL DEFAULT 0,
    campeon_usado TEXT NOT NULL,
    UNIQUE (id_partida, id_jugador),
    FOREIGN KEY (id_partida) REFERENCES Partida(id_partida) ON DELETE CASCADE,
    FOREIGN KEY (id_jugador) REFERENCES Jugador(id_jugador) ON DELETE CASCADE
);

-- 8. Tabla Usuario
CREATE TABLE IF NOT EXISTS Usuario (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    rol_usuario TEXT NOT NULL CHECK (rol_usuario IN ('Administrador', 'Árbitro', 'Capitán', 'Jugador', 'Espectador')),
    fecha_registro DATETIME DEFAULT (CURRENT_TIMESTAMP)
);

-- Índices
CREATE INDEX IF NOT EXISTS idx_jugador_nickname ON Jugador (nickname);
CREATE INDEX IF NOT EXISTS idx_estadistica_jugador ON Estadistica_Jugador (id_jugador);
CREATE INDEX IF NOT EXISTS idx_partida_torneo ON Partida (id_torneo);

-- Vistas
CREATE VIEW IF NOT EXISTS jugadores_equipos AS
SELECT
    j.id_jugador,
    j.nickname,
    j.nombre_real,
    j.rol,
    j.region AS region_jugador,
    e.nombre AS nombre_equipo,
    e.region AS region_equipo
FROM
    Jugador j
LEFT JOIN 
    Equipo e ON j.id_equipo = e.id_equipo;

CREATE VIEW IF NOT EXISTS inscripciones_torneo AS
SELECT
    i.id_inscripcion,
    t.nombre AS nombre_torneo,
    e.nombre AS nombre_equipo,
    i.estado AS estado_inscripcion,
    i.fecha_inscripcion
FROM
    Inscripcion i
JOIN
    Torneo t ON i.id_torneo = t.id_torneo
JOIN
    Equipo e ON i.id_equipo = e.id_equipo;

CREATE VIEW IF NOT EXISTS estadisticas_jugadores AS
SELECT
    j.id_jugador,
    j.nickname,
    COUNT(ej.id_partida) AS partidas_jugadas,
    COALESCE(SUM(ej.kills),0) AS total_kills,
    COALESCE(SUM(ej.deaths),0) AS total_deaths,
    COALESCE(SUM(ej.assists),0) AS total_assists,
    ( (COALESCE(SUM(ej.kills),0) + COALESCE(SUM(ej.assists),0)) * 1.0 ) / 
    CASE WHEN COALESCE(SUM(ej.deaths),0) = 0 THEN 1 ELSE COALESCE(SUM(ej.deaths),0) END AS KDA_aproximado
FROM
    Jugador j
LEFT JOIN
    Estadistica_Jugador ej ON j.id_jugador = ej.id_jugador
GROUP BY
    j.id_jugador, j.nickname
ORDER BY
    partidas_jugadas DESC, KDA_aproximado DESC;
