import sqlite3

# Conectar a la base de datos (crea el archivo si no existe)
conn = sqlite3.connect("../prueba.db")
cursor = conn.cursor()

# Crear una tabla
cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    edad INTEGER)''')

# Insertar datos
cursor.execute("INSERT INTO usuarios (nombre, edad) VALUES (?, ?)", ("Alan", 25))
conn.commit()  # Guardar cambios

# Consultar datos
cursor.execute("SELECT * FROM usuarios")
print(cursor.fetchall())  # Ver los resultados

conn.close()  # Cerrar conexión
