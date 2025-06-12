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

#Configuración de logs
logging.basicConfig(
    filename = 'app.log',
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s' 
)

#cargar variables
env_path = os.path.join(os.getcwd(), 'users.env')
if not os.path.exists(env_path):
    logging.critical("No se encontró el archivo .env")
    sys.exit("El archivo .env no existe. No se puede continuar.")

usuarios = {k.lower(): v for k, v in dotenv_values(env_path).items()}
logging.info("Arhivo .env cargado correctamente")

def validate_login(root, user_entry, pass_entry):
    usuario = user_entry.get().lower()
    password = pass_entry.get().lower()
    
    if usuario in usuarios and usuarios[usuario] == password:
        logging.info(f"Inicio de sesión exitoso - Usuario: '{usuario}'")
        root.destroy()
        
        try: 
            subprocess.Popen([sys.executable, "monitor.py"])
        except Exception as e:
            logging.error(f"Error al ejecutar programa principal: {e}")
    else:
        logging.warning(f"Intento de inicio de sesión fallido - Usuario: '{usuario}'")
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

#Ventana
def start_login():
    root = tk.Tk()
    root.title("Inicio Sesion - MHP")
    ancho_ventana = 600
    alto_ventana = 500
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
    
    #botón
    tk.Button(root, text = "Iniciar Sesión", 
              font = FUENTES["boton"], bg = PALETA["hover"], 
              activebackground = PALETA["detalle"],
              borderwidth = 0, relief = "flat", cursor = "hand2", 
              command = lambda: validate_login(root, user_entry, pass_entry)).pack(pady = 20)
    
    #Pie de página
    tk.Label(root, text = "Versión 1.0", bg = PALETA["fondo"]).pack(side = "bottom", pady = 10)
    tk.Label(root, text = "© 2025 MHP Industries", bg = PALETA["fondo"]).pack(side = "bottom")
    
    root.mainloop()
    
if __name__ == "__main__":
    start_login()