#!/usr/bin/env python3
"""Init DB script

Este script aplica `schema.sql` y `seeds.sql` (si existen) sobre
`django_db.sqlite3` en el mismo directorio del repositorio.

Uso:
    py -3 init_db.py    # en Windows
    python init_db.py
"""
from pathlib import Path
import sqlite3
import sys

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / 'db.sqlite3'
SCHEMA = ROOT / 'schema.sql'
SEEDS = ROOT / 'seeds.sql'

def apply_sql_file(conn: sqlite3.Connection, path: Path) -> None:
    print(f"Aplicando {path.name}...")
    sql = path.read_text(encoding='utf-8')
    conn.executescript(sql)
    conn.commit()

def main():
    # Ensure DB file exists (sqlite will create it when connecting)
    print(f"Usando base de datos: {DB_PATH}")
    conn = sqlite3.connect(str(DB_PATH))

    applied = False
    if SCHEMA.exists():
        apply_sql_file(conn, SCHEMA)
        applied = True
    else:
        print("No se encontró `schema.sql`. Saltando esquema.")

    if SEEDS.exists():
        apply_sql_file(conn, SEEDS)
        applied = True
    else:
        print("No se encontró `seeds.sql`. Saltando seeds.")

    if applied:
        print("Inicialización de la base de datos completada.")
    else:
        print("No se aplicó ningún SQL. Asegúrate de que `schema.sql` o `seeds.sql` existan.")

    conn.close()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Error al inicializar la BD: {e}")
        sys.exit(1)
