import streamlit as sl
import sqlite3
import pandas as pan
import os
import re

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), 'db.sqlite3')

sl.set_page_config(page_title='DB Project - Gestión de Equipos y Jugadores', layout='wide')

@sl.cache_resource
def get_conn():
    conectar = sqlite3.connect(DB_PATH, check_same_thread=False)
    return conectar

conectar = get_conn()

sl.title('Proyecto DB - Gestión de Equipos y Jugadores')

# Función para ejecutar consultas SQL
def run_query(query, params=None):
    try:
        cursor = conectar.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        kind = query.strip().upper().split()[0]
        if kind in ('SELECT', 'WITH', 'PRAGMA', 'EXPLAIN'):
            try:
                rows = cursor.fetchall()
                cols = [desc[0] for desc in cursor.description] if cursor.description else []
                return rows, cols
            except Exception:
                return None, None
        else:
            conectar.commit()
            return None, None
    except Exception as e:
        sl.error(f"Error ejecutando consulta: {e}")
        return None, None

# Función para mostrar tabla
def show_table(table_name):
    query = f"SELECT * FROM {table_name}"
    data, columnas = run_query(query)
    if data:
        df = pan.DataFrame(data, columns=columnas)
        sl.dataframe(df)
    else:
        sl.info(f"No hay datos en la tabla {table_name}")

# Menú principal
menu = sl.sidebar.selectbox(
    "Seleccione una operación", ["Ver Equipos", "Ver Jugadores", "Ver Torneos", "Agregar Equipo", "Agregar Jugador", "Agregar Torneo", "SQL Runner"]
)

if menu == "Ver Equipos":
    sl.header("Equipos")
    show_table("core_equipo")

elif menu == "Ver Jugadores":
    sl.header("Jugadores")
    show_table("core_jugador")

elif menu == "Ver Torneos":
    sl.header("Torneos")
    show_table("core_torneo")

elif menu == "Agregar Equipo":
    sl.header("Agregar Nuevo Equipo")
    with sl.form("add_team"):
        nombre = sl.text_input("Nombre del equipo")
        logo = sl.text_input("Logo (URL)")
        fecha_creacion = sl.date_input("Fecha de creación")
        region = sl.selectbox("Región", ["LAS", "LAN", "EUW", "NA", "KR", "BR", "EUNE", "JP", "ME", "OCE", "RU", "SEA", "TR", "TW", "VN"])

        if sl.form_submit_button("Agregar Equipo"):
            query = """
            INSERT INTO core_equipo (nombre, logo, fecha_creacion, region)
            VALUES (?, ?, ?, ?)
            """
            run_query(query, (nombre, logo, str(fecha_creacion), region))
            sl.success("Equipo agregado exitosamente!")

elif menu == "Agregar Jugador":
    sl.header("Agregar Nuevo Jugador")
    with sl.form("add_player"):
        nickname = sl.text_input("Nickname")
        nombre_real = sl.text_input("Nombre real")
        rol = sl.selectbox("Rol", ["Top", "Jungle", "Mid", "ADC", "Support"])
        region = sl.selectbox("Región", ["LAS", "LAN", "EUW", "NA", "KR", "BR", "EUNE", "JP", "ME", "OCE", "RU", "SEA", "TR", "TW", "VN"])
        equipo_id = sl.number_input("ID del Equipo", min_value=1, step=1)

        if sl.form_submit_button("Agregar Jugador"):
            query = """
            INSERT INTO core_jugador (nickname, nombre_real, rol, region, equipo_id)
            VALUES (?, ?, ?, ?, ?)
            """
            run_query(query, (nickname, nombre_real, rol, region, equipo_id))
            sl.success("Jugador agregado exitosamente!")

elif menu == "Agregar Torneo":
    sl.header("Agregar Nuevo Torneo")
    with sl.form("add_tournament"):
        nombre = sl.text_input("Nombre del torneo")
        fecha_inicio = sl.date_input("Fecha de inicio")
        fecha_fin = sl.date_input("Fecha de fin")
        def get_formats_from_schema():
            cur = conectar.cursor()
            candidates = ('core_torneo', 'Torneo', 'torneo')
            for tbl in candidates:
                cur.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name=?;", (tbl,))
                fila = cur.fetchone()
                if fila and fila[0]:
                    sql = fila[0]
                    m = re.search(r"CHECK\s*\(\s*formato\s+IN\s*\(([^)]+)\)\)", sql, re.IGNORECASE)
                    if m:
                        vals = m.group(1)
                        items = [v.strip().strip("'\"") for v in vals.split(',')]
                        return items
            # fallback defaults
            return [
                "Round Robin",
                "Eliminación Simple",
                "Doble Eliminación",
                "Grupos",
            ]

        formatos = get_formats_from_schema()
        formato = sl.selectbox("Formato", formatos)

        if sl.form_submit_button("Agregar Torneo"):
            query = """
            INSERT INTO core_torneo (nombre, fecha_inicio, fecha_fin, formato)
            VALUES (?, ?, ?, ?)
            """
            run_query(query, (nombre, str(fecha_inicio), str(fecha_fin), formato))
            sl.success("Torneo agregado exitosamente!")

elif menu == "SQL Runner":
    sl.header("Ejecutar Consultas SQL")
    query = sl.text_area("Escribe tu consulta SQL aquí", height=150,
                        value="SELECT * FROM core_equipo LIMIT 5;")
    if sl.button("Ejecutar Consulta"):
        if query.strip():
            data, columnas = run_query(query)
            if data is not None and columnas:
                df = pan.DataFrame(data, columns=columnas)
                sl.dataframe(df)
            elif data is None:
                # No direct tabular output: try to detect affected table and show it
                sl.success("Consulta ejecutada exitosamente!")
                q_upper = query.strip().upper()
                import re
                tbl = None
                m = re.search(r"INSERT\s+INTO\s+([\w_]+)", q_upper)
                if not m:
                    m = re.search(r"UPDATE\s+([\w_]+)", q_upper)
                if not m:
                    m = re.search(r"DELETE\s+FROM\s+([\w_]+)", q_upper)
                if m:
                    tbl = m.group(1).lower()
                if tbl:
                    try:
                        sl.subheader(f"Contenido actual de `{tbl}`")
                        show_table(tbl)
                    except Exception as e:
                        sl.warning(f"No se pudo mostrar la tabla '{tbl}': {e}")
                else:
                    sl.info("No se encontro una tabla.")
        else:
            sl.warning("Por favor escribe una consulta SQL")
