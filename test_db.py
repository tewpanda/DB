import os
import sqlite3

def test_database_exists():
    """Test that the django_db.sqlite3 database exists"""
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    db_path = os.path.join(repo_root, 'db.sqlite3')
    assert os.path.exists(db_path), 'django_db.sqlite3 should exist'

def test_tables_exist():
    """Test that the required tables exist in the database"""
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    db_path = os.path.join(repo_root, 'db.sqlite3')

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Check that core_equipo table exists
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='core_equipo';")
    rows = cur.fetchall()
    assert rows, 'core_equipo table should exist'

    # Check that core_jugador table exists
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='core_jugador';")
    rows = cur.fetchall()
    assert rows, 'core_jugador table should exist'

    # Check that core_torneo table exists
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='core_torneo';")
    rows = cur.fetchall()
    assert rows, 'core_torneo table should exist'

    conn.close()

def test_basic_queries():
    """Test basic SELECT queries on the tables"""
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    db_path = os.path.join(repo_root, 'db.sqlite3')

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Test SELECT from core_equipo
    cur.execute("SELECT COUNT(*) FROM core_equipo;")
    count = cur.fetchone()[0]
    assert isinstance(count, int), 'Should return an integer count'

    # Test SELECT from core_jugador
    cur.execute("SELECT COUNT(*) FROM core_jugador;")
    count = cur.fetchone()[0]
    assert isinstance(count, int), 'Should return an integer count'

    # Test SELECT from core_torneo
    cur.execute("SELECT COUNT(*) FROM core_torneo;")
    count = cur.fetchone()[0]
    assert isinstance(count, int), 'Should return an integer count'

    conn.close()
