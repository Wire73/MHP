#Librerias a utilizar
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from datetime import datetime
from PIL import Image, ImageTk
import os

# --- VENTANA INICIAL ---
class MonitorApp:
    def  __init__(self, root):
        self.root = root
        self.root.title("Monitor de Temperatura y Presión")
        ancho_ventana = 1000
        alto_ventana = 800
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()
        pos_x = int((ancho_pantalla/2) - (ancho_ventana/2))
        pos_y = int((alto_pantalla/2) - (alto_ventana/2))
        self.root.geometry(f"{ancho_ventana}x{alto_ventana}+{pos_x}+{pos_y}")
        self.root.configure(bg = "#F8F6F0")
        self.setup_ui()

    def setup_ui(self):
        #Logo
        try:
            logo_path = os.path.join("img", "logo_empresa.png")
            logo = Image.open(logo_path)
            logo = logo.resize((300, 120))
            logo_img = ImageTk.PhotoImage(logo)
            logo_label = tk.Label(self.root, image = logo_img, bg = "#F8F6F0")
            logo_label.image = logo_img
            logo_label.pack(pady = (10, 5))
        except Exception:
            tk.Label(self.root, text = "[Logo Empresa]", font = ("Arial", 18), bg = "#F8F6F0", fg = "#333").pack()
        
        #Título
        tk.Label(self.root, text = "Monitoreo de Temperatura y presión", font = ("Arial", 20, "bold"), bg = "#F8F6F0", fg = "#2F4F4F").pack(pady = (5, 15))
        
        #Botón para poder cargar archivos
        self.load_button = tk.Button(self.root, text = "Cargar Archivo de Datos", font = ("Arial", 12, "bold"), bg = "#FFA500", fg = "white", activebackground = "#FFB84D", cursor = "hand2", command = self.load_file)
        self.load_button.pack(pady = 10)

        #Tabla para mostrar los datos
        style = ttk.Style()
        style.configure("Treeview.Heading", font = ("Arial", 11, "bold"), background = "#FFFFFF", foreground = "#2F4F4F")
        style.configure("Treeview", font = ("Arial", 10), rowheight = 25)
        
        self.tree = ttk.Treeview(self.root, columns = ("Tiempo", "Temperatura", "Presión"), show = 'headings')
        for col in ("Tiempo", "Temperatura", "Presión"):
            self.tree.heading(col, text = col)
            self.tree.column(col, anchor = "center")
        self.tree.pack(padx = 20, pady = 10, fill = tk.BOTH, expand = True)

        #Horas trabajadas
        self.total_label = tk.Label(self.root, text = "Total de horas trabajadas: 0h",
                                    font = ("Arial", 12, "bold"), bg = "#F8F6F0", fg = "#2F4F4F")
        self.total_label.pack(pady = (5, 10))
        
        #Frame para la gráfica
        self.figure = plt.figure(figsize = (5,3), dpi = 100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self.root)
        self.canvas.get_tk_widget().pack(fill = tk.BOTH, expand = True, padx = 20, pady = 10)

    def load_file(self):
        filepath = filedialog.askopenfilename(filetypes = [("Archivos de texto", "*.txt")])
        if not filepath:
            return
        
        try:
            #cargar archivo en un data frame
            df = pd.read_csv(filepath, header = None, names = ["Tiempo", "Temperatura", "Presión"])

            #convertir la comlumna de tiempo a formato 24hrs (datetime.time)
            df["Tiempo"] = pd.to_datetime(df["Tiempo"], format = "%H:%M:%S").dt.time
            df["Tiempo_dt"] = pd.to_datetime(df["Tiempo"].astype(str), format = "%H:%M:%S")
            
            #limpiar tabla
            for row in self.tree.get_children():
                self.tree.delete(row)

            #Agregar datos a tabla
            for _, row in df.iterrows():
                self.tree.insert("", tk.END, values = (row["Tiempo"], row["Temperatura"], row["Presión"]))
            
            #Total de horas trabajas agregar
            inicio = df["Tiempo_dt"].iloc[0]
            fin = df["Tiempo_dt"].iloc[-1]
            diferencia = fin - inicio
            total_segundos = diferencia.total_seconds()
            horas = int(total_segundos // 3600)
            minutos = int((total_segundos % 3600) // 60)
            self.total_label.config(text = f"Total de horas trabajadas: {horas} h {minutos} min")
            
            #Graficar los datos
            self.ax.clear()
            self.ax.plot(df["Tiempo_dt"], df["Temperatura"], label = "Temperatura (°C)", color = 'red')
            self.ax.plot(df["Tiempo_dt"], df["Presión"], label = "Presión (PSI)", color = 'blue')
            self.ax.set_xlabel("Hora")
            self.ax.set_ylabel("Valores")
            self.ax.set_title("Temperatura y Presión")
            self.ax.legend()
            self.ax.grid(True)
            
            #Mejorar formato X
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
            self.figure.autofmt_xdate()
            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MonitorApp(root)
    root.mainloop()