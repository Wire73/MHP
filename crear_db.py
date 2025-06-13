import sqlite3
import bcrypt   

#Crear o conectar a la base de datos
conn = sqlite3.connect("usuarios.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    usuario TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    rol TEXT NOT NULL CHECK(rol IN ('admin', 'tecnico'))
)
''')

#Función para hashaer la contraseña
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

#Insertar usuarios de prueba
usuarios = [
    ("admin", "admin123", "admin"),
    ("tecnico1", "tecnico123", "tecnico"),
    ("tecnico2", "tecnico456", "tecnico")
]

for usuario, password, rol in usuarios:
    try:
        hashed_password = hash_password(password)
        cursor.execute("INSERT INTO usuarios (usuario, password, rol) VALUES (?, ?, ?)", 
                       (usuario, hashed_password, rol))
        print(f"Usuario '{usuario}' insertado correctamente.")
    except sqlite3.IntegrityError:
        print(f"El usuario '{usuario}' ya existe. No se insertó.")
conn.commit()
conn.close()