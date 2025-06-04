#Librerias a utilizar
import tkinter as tk
from tkinter import messagebox
import subprocess
from PIL import Image, ImageTk
import os

#Diccionario de usuarios y contraseñas
usuarios = {
    "admin" : "1234",
    "zulmar" : "abcd",
    "andres" : "4321"
}

#Validación del login
def validate_login(root, user_entry, pass_entry):
    usuario = user_entry.get()
    password = pass_entry.get()
    
    if usuario in usuarios and usuarios[usuario] == password:
        root.destroy()
        subprocess.Popen(["python", "monitor.py"])
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

#Ventana
def start_login():
    root = tk.Tk()
    root.title("Inicio Sesion - MHP")
    root.geometry("400x500")
    root.configure(bg = "#FFA500") #Color naranja principal de la empresa
    
    #logo
    try:
        logo_path = os.path.join("img", "logo_empresa.png")
        logo = Image.open(logo_path)
        logo = logo.resize((150, 150))
        logo_img = ImageTk.PhotoImage(logo)
        tk.Label(root, image = logo_img, bg = "#FFA500").pack(pady=10)
    except Exception:
        tk.Label(root, text = "[LOGO]", font = ("Arial", 16), bg = "#FFA500").pack(pady=10)
    
    #Nombre de la empresa
    