#Librerias a utilizar
import tkinter as tk
from tkinter import messagebox
import subprocess
from PIL import Image, ImageTk
import os
import sys
from dotenv import dotenv_values
import logging
from estilos import PALETA, FUENTES
import sqlite3
import bcrypt

#Configuración de logs
logging.basicConfig(
    filename = 'app.log',
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s' 
)

#validar login con base de datos
def validate_login(root, user_entry, pass_entry):
    usuario = user_entry.get().lower()
    password = pass_entry.get()
    
    if not usuario or not password:
        messagebox.showerror("Error", "Por favor, complete todos los campos")
        return
    
    try:
        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()
        cursor.execute("SELECT password, rol FROM usuarios WHERE usuario = ?", (usuario,))
        result = cursor.fetchone()
        conn.close()
        
        if result and bcrypt.checkpw(password.encode(), result[0]):
            rol =  result[1]
            logging.info(f"Inicio de sesión exitoso - Usuario: '{usuario}', ROl: '{rol}'")
            if not os.path.exists("monitor.py"):
                messagebox.showerror("Error", "El archivo 'monitor.py' no se encuentra en el directorio actual")
                return
            root.destroy()
            subprocess.Popen([sys.executable, "monitor.py", rol])
        else:
            logging.warning(f"Intento de inicio de sesión fallido - Usuario: '{usuario}'")
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
    except Exception as e:
        logging.error(f"Error al conectar a la base de datos: {e}")
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")

#Ventana
def start_login():
    root = tk.Tk()
    root.title("Inicio Sesion - MHP")
    ancho_ventana = 600
    alto_ventana = 650
    ancho_pantalla = root.winfo_screenwidth()
    alto_pantalla = root.winfo_screenheight()
    pos_x = int((ancho_pantalla/2) - (ancho_ventana/2))
    pos_y = int((alto_pantalla/2) - (alto_ventana/2))
    root.geometry(f"{ancho_ventana}x{alto_ventana}+{pos_x}+{pos_y}")
    root.configure(bg = PALETA["fondo"]) 
    
    #logo
    try:
        logo_path = os.path.join("img", "logo_empresa.png")
        logo = Image.open(logo_path)
        logo = logo.resize((350, 150))
        logo_img = ImageTk.PhotoImage(logo)
        tk.Label(root, image = logo_img, bg = PALETA["fondo"]).pack(pady=10)
    except Exception as e:
        logging.warning(f"Error al cargar el logo: {e}")
        tk.Label(root, text = "[LOGO]", font = FUENTES["texto"], bg = PALETA["fondo"]).pack(pady=10)
    
    #Nombre de la empresa
    tk.Label(root, text = "Martillos Hidráulicos de la Península", font = FUENTES["titulo"], bg = PALETA["fondo"]).pack()
    tk.Label(root, text = "Monitoreo temperatura y presión", font = FUENTES["subtitulo"], bg = PALETA["fondo"]).pack(pady = (0,20))
    
    #Usuario
    tk.Label(root, text = "Usuario:", font = FUENTES["texto"], bg = PALETA["fondo"]).pack()
    user_entry = tk.Entry(root, font = FUENTES["texto"])
    user_entry.pack(pady = 5)
    
    #Contraseña
    tk.Label(root, text = "Contraseña:", font = FUENTES["texto"], bg = PALETA["fondo"]).pack()
    pass_entry = tk.Entry(root, show = "*", font = FUENTES["texto"])
    pass_entry.pack(pady = 5)
    
    #Botón de mostrar/ocultar contraseña
    def toggle_password():
        if pass_entry.cget("show") == "":
            pass_entry.config(show="*")
            show_button.config(text="Mostrar Contraseña")
        else:
            pass_entry.config(show="")
            show_button.config(text="Ocultar Contraseña")
    
    #Botón para mostrar/ocultar contraseña
    show_button = tk.Button(root, text="Mostrar Contraseña", font=FUENTES["boton"],
                            command=toggle_password, bg=PALETA["hover"], cursor="hand2", activebackground=PALETA["detalle"])
    show_button.pack(pady=20)
    
    #botón
    tk.Button(root, text = "Iniciar Sesión", 
              font = FUENTES["boton"], bg = PALETA["hover"], 
              activebackground = PALETA["detalle"], cursor = "hand2", 
              command = lambda: validate_login(root, user_entry, pass_entry)).pack(pady = 20)
    
    #Tecla enter hace login
    root.bind('<Return>', lambda event: validate_login(root, user_entry, pass_entry))
    
    #Pie de página
    tk.Label(root, text = "Versión 1.0", bg = PALETA["fondo"]).pack(side = "bottom", pady = 10)
    tk.Label(root, text = "© 2025 MHP Industries", bg = PALETA["fondo"]).pack(side = "bottom")
    
    root.mainloop()
    
if __name__ == "__main__":
    start_login()