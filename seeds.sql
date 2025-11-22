-- Seeds: datos ficticios pequeños para probar la aplicación

-- Equipos
INSERT INTO Equipo (nombre, logo, fecha_creacion, region) VALUES
('Dragones Rojos', '', '2018-04-01','LAS'),
('Tiburones Azules', '', '2019-07-15','LAN'),
('Halcones Verdes', '', '2020-01-20','EUW');

-- Jugadores
INSERT INTO Jugador (nickname, nombre_real, rol, region, id_equipo) VALUES
('FireKing','Juan Pérez','Top','LAS',1),
('SeaWolf','María García','Jungle','LAN',2),
('GreenArrow','Carlos López','Mid','EUW',3),
('Shadow','Ana Ruiz','ADC','LAS',1),
('Wave','Luis Soto','Support','LAN',2),
('Leaf','Sofia Castro','Sustituto','EUW',3);

-- Torneo
INSERT INTO Torneo (nombre, fecha_inicio, fecha_fin, formato, num_equipos) VALUES
('Copa Interregional','2025-11-01','2025-11-10','Round Robin',3);

-- Inscripciones
INSERT INTO Inscripcion (id_equipo, id_torneo, estado) VALUES
(1,1,'Aceptada'),
(2,1,'Aceptada'),
(3,1,'Aceptada');

-- Partidas (dos partidas de ejemplo)
INSERT INTO Partida (id_torneo, fase, fecha_hora, equipo_local_id, equipo_visitante_id) VALUES
(1,'Fase de Grupos','2025-11-02 18:00:00',1,2),
(1,'Fase de Grupos','2025-11-03 20:00:00',3,1);

-- Resultados
INSERT INTO Resultado (id_partida, equipo_ganador_id, score_ganador, score_perdedor, duracion_minutos) VALUES
(1,1,2,0,35),
(2,3,2,1,42);

-- Estadísticas
INSERT INTO Estadistica_Jugador (id_partida, id_jugador, kills, deaths, assists, oro, dano, campeon_usado) VALUES
(1,1,5,2,3,12000,15000,'Aatrox'),
(1,4,7,1,4,13500,18000,'Jinx'),
(1,2,3,5,2,9000,8000,'Lee Sin'),
(2,3,10,2,5,16000,20000,'Zed'),
(2,6,1,7,0,7000,4000,'Leona');

-- Usuario de prueba
-- Usuarios de prueba (passwords hashed with SHA256 for demo: 'adminpass' and 'playerpass')
INSERT INTO Usuario (username, email, password_hash, rol_usuario) VALUES
('admin','admin@example.com','713bfda78870bf9d1b261f565286f85e97ee614efe5f0faf7c34e7ca4f65baca','Administrador'),
('player1','player1@example.com','ea4aab402774b7584d4ff359cb8f240ea67d74476964601844eb2674e25039be','Jugador');
