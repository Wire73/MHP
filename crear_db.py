import sqlite3
import bcrypt

#Crear o conectar a la base de datos
conn = sqlite3.connect("usuarios.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    usuario TEXT PRIMARY KEY,
    password TEXT NOT NULL
)
''')

#Función para hashaer la contraseña
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

#Insertar usuarios de prueba
usuario = "admin"
password = "admin123"

try:
    hashed_password = hash_password(password)
    cursor.execute("INSERT INTO usuarios (usuario, password) VALUES (?, ?)",
                   (usuario, hashed_password))
    print("Usuario insertado correctamente.")
except sqlite3.IntegrityError:
    print("El usuario ya existe. No se insertó de nuevo.")
    
conn.commit()
conn.close()