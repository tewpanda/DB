# DB Project

Proyecto de base de datos - estructura y artefactos iniciales.

Descripción
---------
Este repositorio contiene los archivos iniciales para un proyecto de base de datos (esquemas, scripts, documentación y configuración).

Contenido
--------
- README con información del proyecto
- .gitignore para ignorar archivos locales

Cómo usar
--------
Este repositorio contiene una pequeña aplicación Streamlit que gestiona equipos, jugadores y torneos
con una base SQLite de ejemplo. Está pensado para uso local y demostraciones.

Contenido principal
------------------
- `streamlit_app.py` - aplicación Streamlit.
- `schema.sql` / `seeds.sql` - esquema y datos de ejemplo para la base SQLite.
- `init_db.py` - script que aplica `schema.sql` y `seeds.sql` sobre `db.sqlite3`.
- `db.sqlite3` - archivo de base de datos (no recomendable subir al repo).
- `test_db.py` - pruebas básicas que verifican la existencia de tablas.

Instalación y uso (Windows / PowerShell)
---------------------------------------
1. Clona el repositorio:

   git clone <url-del-repo>
   cd DB

2. Crear y activar un entorno virtual (recomendado):

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

3. Inicializar la base de datos (crea `db.sqlite3` con el esquema y datos de `seeds.sql`):

```powershell
python init_db.py
```

4. Ejecutar tests rápidos:

```powershell
python test_db.py
```

5. Iniciar la aplicación Streamlit:

```powershell
python -m streamlit run streamlit_app.py
```

Notas
-----
- Se recomienda NO subir `db.sqlite3` al repositorio; está incluido localmente solo para pruebas.
- Si prefieres subir una copia limpia, borra `db.sqlite3` antes de commitear y deja `schema.sql`/`seeds.sql`.
- Para desplegar en producción, reemplaza SQLite por una base de datos gestionada y configura credenciales seguras.

Contacto
-------
Si necesitas ayuda para subir este repo a GitHub o para crear el remoto, responde y puedo hacerlo
usando tu `gh` CLI autenticado (crearé el repositorio `tewpanda/DB` por defecto si lo autorizas).

Licencia
--------
Añade aquí la licencia que quieras usar (por ejemplo MIT, Apache-2.0, etc.).

Estado
-----
Inicial: archivos base creados y listos para versionado.
