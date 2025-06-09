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
from estilos import PALETA, FUENTES

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
        
        #Resumen de estadisticas
        self.stats_label=tk.Label(self.root, text="", font=FUENTES["texto"], bg="#F8F6F0",
                                  justify="left", fg="#2F4F4F")
        self.stats_label.pack(pady=(0, 10))
        
        #Fecha y Hora de carga
        self.file_info_label= tk.Label(self.root, text="", font=FUENTES["texto"], bg="#F8F6F0",
                                       fg="#6E6E6E")
        self.file_info_label.pack(pady=(0, 10))
        
        #botón para exportar resultados
        self.export_button=tk.Button(self.root, text="Exportar resumen", font=FUENTES["boton"],
                                     bg="#4682B4", fg="white", activebackground="#5A9BD4",
                                     command=self.export_summary)
        self.export_button.pack(pady=(0, 10))
        
        #Frame para la gráfica
        self.figure = plt.figure(figsize = (5,3), dpi = 100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self.root)
        self.canvas.get_tk_widget().pack(fill = tk.BOTH, expand = True, padx = 20, pady = 10)

    def load_file(self):
        filepath = filedialog.askopenfilename(filetypes = [("Archivos de texto", "*.csv")])
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
            
            #Calcular estadísticas
            temp_max = df["Temperatura"].max()
            temp_max_time = df.loc[df["Temperatura"].idxmax(), "Tiempo"]
            pres_max = df["Presión"].max()
            pres_max_time = df.loc[df["Presión"].idxmax(), "Tiempo"]
            
            #Media de los datos
            temp_avg = df["Temperatura"].mean()
            pres_avg = df["Presión"].mean()
            
            self.stats_label.config(
                text= f"Temperatura Máxima: {temp_max:.2f} °C a las {temp_max_time}\n"
                      f"Presión Máxima: {pres_max:.2f} PSI a las {pres_max_time}\n"
                      f"Temperatura Promedio: {temp_avg:.2f} °C\n"
                      f"Presión Promedio: {pres_avg:.2f} PSI"
            )
            
            now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            self.file_info_label.config(text=f"Archivo cargado el {now}")
            
            #Datos a exportar
            self.stats_data = {
                "Horas trabajadas":f"{horas} h {minutos} min",
                "Temperatura máxima":f"{temp_max:.2f} °C a las {temp_max_time}",
                "Presión máxima":f"{pres_max:.2f} PSI a las {pres_max_time}",
                "Temperatura promedio":f"{temp_avg:.2f} °C",
                "Presión promedio":f"{pres_avg:.2f} PSI",
                "Fecha de carga": now
            }
            
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

    def export_summary(self):
        if not hasattr(self, "stats_data"):
            messagebox.showwarning("Advertencia", "No hay datos para exportar.")
            return
        file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file:
            return
        
        try:
            df_summary = pd.DataFrame.from_dict(self.stats_data, orient="index", columns=["Valor"])
            df_summary.to_csv(file, encoding="utf-8")
            messagebox.showinfo("Exportado", f"Resumen exportado exitosamente a:\n{file}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar el resumen: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MonitorApp(root)
    root.mainloop()