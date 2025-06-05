#Librerias a utilizar
import tkinter as tk
from tkinter import messagebox
import subprocess
from PIL import Image, ImageTk
import os
import sys
from dotenv import load_dotenv

#cargar variables
load_dotenv(dotenv_path = "users.env")

#Función para cargar usuarios
def cargar_usuarios():
    usuarios = {}
    for clave, valor in os.environ.items():
        if clave.isalpha():
            usuarios[clave.lower()] = valor
    return usuarios

#Validación del login
def validate_login(root, user_entry, pass_entry):
    usuarios = cargar_usuarios()
    
    if not usuarios:
        messagebox.showerror("Error", "No se encontro el archivo de usuarios")
        return

    usuario = user_entry.get().lower()
    password = pass_entry.get()
    
    if usuario in usuarios and usuarios[usuario] == password:
        root.destroy()
        subprocess.Popen([sys.executable, "monitor.py"])
    else:
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
    root.configure(bg = "#FFA500") #Color naranja principal de la empresa
    
    #logo
    try:
        logo_path = os.path.join("img", "logo_empresa.png")
        logo = Image.open(logo_path)
        logo = logo.resize((350, 150))
        logo_img = ImageTk.PhotoImage(logo)
        tk.Label(root, image = logo_img, bg = "#FFA500").pack(pady=10)
    except Exception:
        tk.Label(root, text = "[LOGO]", font = ("Arial", 16), bg = "#FFA500").pack(pady=10)
    
    #Nombre de la empresa
    tk.Label(root, text = "Martillos Hidráulicos de la Península", font = ("Arial", 18, "bold"), bg = "#FFA500", fg = "white").pack()
    tk.Label(root, text = "Monitoreo temperatura y presión", font = ("Arial", 10), bg = "#FFA500", fg = "white").pack(pady = (0,20))
    
    #Usuario
    tk.Label(root, text = "Usuario:", font = ("Arial", 12), bg = "#FFA500", fg = "white").pack()
    user_entry = tk.Entry(root, font = ("Arial", 12))
    user_entry.pack(pady = 5)
    
    #Contraseña
    tk.Label(root, text = "Contraseña:", font = ("Arial", 12), bg = "#FFA500", fg = "white").pack()
    pass_entry = tk.Entry(root, show = "*", font = ("Arial", 12))
    pass_entry.pack(pady = 5)
    
    #botón
    tk.Button(root, text = "Iniciar Sesión", font = ("Arial", 12), bg = "white", fg = "#FFA500", command = lambda: validate_login(root, user_entry, pass_entry)).pack(pady = 20)
    
    #Pie de página
    tk.Label(root, text = "Versión 1.0", bg = "#FFA500", fg = "white").pack(side = "bottom", pady = 10)
    tk.Label(root, text = "© 2025 MHP Industries", bg = "#FFA500", fg = "white").pack(side = "bottom")
    
    root.mainloop()
    
if __name__ == "__main__":
    start_login()