#Librerias a utilizar
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from datetime import datetime

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
        self.setup_ui()

    def setup_ui(self):
        #Botón para poder cargar archivos
        self.load_button = tk.Button(self.root, text = "Cargar Archivo de Datos", command = self.load_file)
        self.load_button.pack(pady = 10)

        #Tabla para mostrar los datos
        self.tree = ttk.Treeview(self.root, columns = ("Tiempo", "Temperatura", "Presión"), show = 'headings')
        self.tree.heading("Tiempo", text = "Tiempo")
        self.tree.heading("Temperatura", text = "Temperatura (°C)")
        self.tree.heading("Presión", text = "Presión (PSI)")
        self.tree.pack(pady = 10, fill = tk.BOTH, expand = True)

        #Frame para la gráfica
        self.figure = plt.figure(figsize = (5,3), dpi = 100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self.root)
        self.canvas.get_tk_widget().pack(fill = tk.BOTH, expand = True)

    def load_file(self):
        filepath = filedialog.askopenfilename(filetypes = [("Archivos de texto", "*.txt")])
        if not filepath:
            return
        
        try:
            #cargar archivo en un data frame
            df = pd.read_csv(filepath, header = None, names = ["Tiempo", "Temperatura", "Presión"])

            #convertir la comlumna de tiempo a formato 24hrs (datetime.time)
            df["Tiempo"] = pd.to_datetime(df["Tiempo"], format = "%H:%M:%S").dt.time
            
            #limpiar tabla
            for row in self.tree.get_children():
                self.tree.delete(row)

            #Agregar datos a tabla
            for _, row in df.iterrows():
                self.tree.insert("", tk.END, values = (row["Tiempo"], row["Temperatura"], row["Presión"]))
            
            #Graficar correctamente el tiempo (convertir time a datetime)
            df["Tiempo_dt"] = pd.to_datetime(df["Tiempo"].astype(str), format = "%H:%M:%S")
            
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