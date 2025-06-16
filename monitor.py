import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from datetime import datetime
from PIL import Image, ImageTk
import os
import subprocess
import sys
from estilos import PALETA, FUENTES
import sqlite3
import bcrypt

class MonitorApp:
    def  __init__(self, root, rol):
        self.root = root
        self.rol = rol
        self.root.title("Monitor de Temperatura y Presión")
        ancho_ventana = 1920
        alto_ventana = 1080
        pos_x = int((self.root.winfo_screenwidth()/2) - (ancho_ventana/2))
        pos_y = int((self.root.winfo_screenheight()/2) - (alto_ventana/2))
        self.root.geometry(f"{ancho_ventana}x{alto_ventana}+{pos_x}+{pos_y}")
        self.root.configure(bg = PALETA["fondo"])
        self.df= None
        self.stats_data = {}
        self.create_menu()
        self.setup_ui()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        
        #Menú Archivo
        file_menu = tk.Menu(menu_bar, tearoff = 0)
        file_menu.add_command(label = "Cargar Archivo", command = self.load_file)
        file_menu.add_command(label = "Exportar Resumen", command = self.export_summary)
        if self.rol == "admin":
            file_menu.add_command(label = "Crear Usuario", command = self.crear_usuario)
        file_menu.add_separator()
        file_menu.add_command(label = "Cerrar Sesión", command = self.logout)
        file_menu.add_command(label = "Salir", command = self.close)
        menu_bar.add_cascade(label = "Archivo", menu = file_menu)
        
        # Menú Vista
        view_menu = tk.Menu(menu_bar, tearoff = 0)
        view_menu.add_command(label = "Gráficas", command = self.show_both_graphs)
        view_menu.add_command(label = "Gráfica de Presión", command = self.show_pressure_graph)
        view_menu.add_command(label = "Gráfica de Temperatura", command = self.show_temperature_graph)
        menu_bar.add_cascade(label = "Vista", menu = view_menu)
        
        self.root.config(menu = menu_bar)
    
    def crear_usuario(self):
        def guardar_usuario(self):
            nuevo_usuario = user_entry.get().lower()
            nueva_contraseña = pass_entry.get()
            rol = rol_var.get()
            
            if not nuevo_usuario or not nueva_contraseña or rol not in ['admin', 'tecnico']:
                messagebox.showerror("Error", "Por favor, complete todos los campos correctamente")
                return
            
            try:
                conn = sqlite3.connect("usuarios.db")
                cursor = conn.cursor()
                hashed = bcrypt.hashpw(nueva_contraseña.encode(), bcrypt.gensalt())
                cursor.execute("INSERT INTO usuarios (usuario, password, rol) VALUES (?, ?, ?)", (nuevo_usuario, hashed, rol))
                conn.commit()
                conn.close()
                messagebox.showinfo("Éxito", f"Usuario '{nuevo_usuario}' creado exitosamente con rol '{rol}'")
                ventana_nueva.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", f"El usuario '{nuevo_usuario}' ya existe")
    
        ventana_nueva = tk.Toplevel()
        ventana_nueva.title("Crear Nuevo Usuario")
        ancho_ventana = 300
        alto_ventana = 250
        ancho_pantalla = ventana_nueva.winfo_screenwidth()
        alto_pantalla = ventana_nueva.winfo_screenheight()
        pos_x = int((ancho_pantalla/2) - (ancho_ventana/2))
        pos_y = int((alto_pantalla/2) - (alto_ventana/2))
        ventana_nueva.geometry(f"{ancho_ventana}x{alto_ventana}+{pos_x}+{pos_y}")
        ventana_nueva.configure(bg = PALETA["fondo"])
    
        tk.Label(ventana_nueva, text="Nuevo Usuario:", font=FUENTES["texto"], bg=PALETA["fondo"]).pack(pady=5)
        user_entry = tk.Entry(ventana_nueva, font=FUENTES["texto"])
        user_entry.pack()
        
        tk.Label(ventana_nueva, text="Nueva Contraseña:", font=FUENTES["texto"], bg=PALETA["fondo"]).pack(pady=5)
        pass_entry = tk.Entry(ventana_nueva, show="*", font=FUENTES["texto"])
        pass_entry.pack()
        
        tk.Label(ventana_nueva, text="Rol:", font=FUENTES["texto"], bg=PALETA["fondo"]).pack(pady=5)
        rol_var = tk.StringVar(value='tecnico')
        tk.OptionMenu(ventana_nueva, rol_var, 'admin', 'tecnico').pack()
        
        tk.Button(ventana_nueva, text="Guardar Usuario", command=guardar_usuario, background= PALETA["hover"],
                font=FUENTES["boton"], activebackground=PALETA["detalle"], cursor="hand2").pack(pady=10)
    
    def setup_ui(self):
        # --- Frame superior (logo, titulo) ---
        header_frame = tk.Frame(self.root, bg = PALETA["fondo"])
        header_frame.pack(fill = tk.X, pady = (10, 10))
        logo_title_frame = tk.Frame(header_frame, bg = PALETA["fondo"])
        logo_title_frame.pack(anchor="center")
        
        #Logo
        try:
            logo_path = os.path.join("img", "logo_empresa.png")
            logo = Image.open(logo_path).resize((300, 120))
            logo_img = ImageTk.PhotoImage(logo)
            logo_label = tk.Label(logo_title_frame, image = logo_img, bg = PALETA["fondo"])
            logo_label.image = logo_img
            logo_label.pack(pady = (10, 5))
        except Exception:
            tk.Label(logo_title_frame, text = "[Logo Empresa]", font = FUENTES["subtitulo"], 
                     bg = PALETA["fondo"], fg=PALETA["texto"]).pack()
        
        #Título
        tk.Label(logo_title_frame, text = "Monitoreo de Temperatura y presión", font = FUENTES["titulo"], 
                 bg = PALETA["fondo"], fg = PALETA["texto"]).pack(pady = (5, 10))

        # --- Frame principal ---
        main_frame = tk.Frame(self.root, bg = PALETA["fondo"])
        main_frame.pack(fill = tk.BOTH, expand = True)
        
        # --- Frame Izquierdo (tabla + info) ---
        left_frame = tk.Frame(main_frame, bg = PALETA["fondo"], width=400)
        left_frame.pack(side = tk.LEFT, fill = tk.BOTH, expand = True, padx = (20, 10))
        left_frame.pack_propagate(False)  # Evitar que el frame se ajuste al contenido

        #Tabla para mostrar los datos
        style = ttk.Style()
        style.configure("Treeview.Heading", font = FUENTES["texto"])
        style.configure("Treeview", font = FUENTES["texto"], rowheight = 25, background = PALETA["fondo2"], fieldbackground = PALETA["fondo2"], foreground = PALETA["texto"])
        
        self.tree = ttk.Treeview(left_frame, columns = ("Tiempo", "Temperatura", "Presión"), show = 'headings')
        for col in ("Tiempo", "Temperatura", "Presión"):
            self.tree.heading(col, text = col)
            self.tree.column(col, anchor = "center")
        self.tree.pack(pady = (0, 10), fill = tk.BOTH, expand = True)

        #Horas trabajadas
        self.total_label = tk.Label(left_frame, text = "Total de horas trabajadas: 0h",
                                    font = FUENTES["texto"], bg = PALETA["fondo"], fg = PALETA["texto"])
        self.total_label.pack(pady = (5, 10), anchor="w")
        
        #Resumen de estadisticas
        self.stats_label=tk.Label(left_frame, text="", font=FUENTES["texto"], background=PALETA["fondo"], justify="left")
        self.stats_label.pack(pady=(0, 10), anchor="w")
        
        #Fecha y Hora de carga
        self.file_info_label= tk.Label(left_frame, text="", font=FUENTES["texto"], bg=PALETA["fondo"],
                                       fg=PALETA["texto"])
        self.file_info_label.pack(pady=(0, 10), anchor="w")
        
        # --- Frame derecho (gráfica) ---
        right_frame = tk.Frame(main_frame, bg = PALETA["fondo"])
        right_frame.pack(side = tk.RIGHT, fill = tk.BOTH, expand = True, padx = (10, 20))
        
        #Frame para la gráfica
        self.figure = plt.figure(figsize = (5,3), dpi = 100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor(PALETA["fondo2"])
        self.figure.patch.set_facecolor(PALETA["fondo2"])
        self.canvas = FigureCanvasTkAgg(self.figure, right_frame)
        self.canvas.get_tk_widget().pack(fill = tk.BOTH, expand = True)

    def load_file(self):
        filepath = filedialog.askopenfilename(filetypes = [("CSV file", "*.csv")])
        if not filepath:
            return
    
        try:
            #cargar archivo en un data frame
            self.df = pd.read_csv(filepath, header = None, names = ["Tiempo", "Temperatura", "Presión"])

            #convertir la comlumna de tiempo a formato 24hrs (datetime.time)
            self.df["Tiempo"] = pd.to_datetime(self.df["Tiempo"], format = "%H:%M:%S").dt.time
            self.df["Tiempo_dt"] = pd.to_datetime(self.df["Tiempo"].astype(str), format = "%H:%M:%S")
            
            #limpiar tabla
            for row in self.tree.get_children():
                self.tree.delete(row)

            #Agregar datos a tabla
            for _, row in self.df.iterrows():
                self.tree.insert("", tk.END, values = (row["Tiempo"], row["Temperatura"], row["Presión"]))
            
            #Total de horas trabajas agregar
            inicio = self.df["Tiempo_dt"].iloc[0]
            fin = self.df["Tiempo_dt"].iloc[-1]
            diff = fin - inicio
            horas, minutos = divmod(diff.total_seconds() // 60, 60)
            self.total_label.config(text = f"Total de horas trabajadas: {int(horas)}h {int(minutos)}min")
            
            #Calcular estadísticas
            temp_max = self.df["Temperatura"].max()
            temp_max_time = self.df.loc[self.df["Temperatura"].idxmax(), "Tiempo"]
            pres_max = self.df["Presión"].max()
            pres_max_time = self.df.loc[self.df["Presión"].idxmax(), "Tiempo"]
            
            #Media de los datos
            temp_avg = self.df["Temperatura"].mean()
            pres_avg = self.df["Presión"].mean()
            
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
            
            self.show_both_graphs()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo: {e}")

    def export_summary(self):
        if not self.stats_data:
            messagebox.showwarning("Advertencia", "No hay datos para exportar.")
            return
        file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file:
            return
        
        try:
            pd.DataFrame.from_dict(self.stats_data, orient="index", columns=["Valor"]).to_csv(file, encoding="utf-8")
            messagebox.showinfo("Exportado", f"Resumen exportado exitosamente a:\n{file}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar el resumen: {e}")
            
    def logout(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro de que desea cerrar sesión?"):
            self.root.destroy()
            subprocess.Popen([sys.executable, "login.py"])
            
    def close(self):
        if messagebox.askyesno("Salir", "¿Está seguro de que desea salir?"):
            self.root.quit()
    
    def show_both_graphs(self):
        if self.df is None:
            messagebox.showwarning("Advertencia", "No hay datos para mostrar.")
            return
        
        #Limpiar la tabla
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        #Insertar datos en la tabla
        for _, row in self.df.iterrows():
            self.tree.insert("", tk.END, values = (row["Tiempo"], row["Temperatura"], row["Presión"]))
        
        #Stats de temperatura y presión
        #Calcular estadísticas
        temp_max = self.df["Temperatura"].max()
        temp_max_time = self.df.loc[self.df["Temperatura"].idxmax(), "Tiempo"]
        pres_max = self.df["Presión"].max()
        pres_max_time = self.df.loc[self.df["Presión"].idxmax(), "Tiempo"]
            
        #Media de los datos
        temp_avg = self.df["Temperatura"].mean()
        pres_avg = self.df["Presión"].mean()
            
        self.stats_label.config(
            text= f"Temperatura Máxima: {temp_max:.2f} °C a las {temp_max_time}\n"
                    f"Presión Máxima: {pres_max:.2f} PSI a las {pres_max_time}\n"
                    f"Temperatura Promedio: {temp_avg:.2f} °C\n"
                    f"Presión Promedio: {pres_avg:.2f} PSI"
        )
        
        self.ax.clear()
        self.ax.plot(self.df["Tiempo_dt"], self.df["Temperatura"], label = "Temperatura (°C)", color = 'red')
        self.ax.plot(self.df["Tiempo_dt"], self.df["Presión"], label = "Presión (PSI)", color = 'blue')
        self.ax.set_title("Gráfica de Temperatura y Presión")
        self.ax.set_xlabel("Hora")
        self.ax.set_ylabel("Valores")
        self.ax.legend()
        self.ax.grid(True)
            
        #Mejorar formato X
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        self.figure.autofmt_xdate()
        self.canvas.draw()
        
    def show_pressure_graph(self):
        if self.df is None:
            return
        
        #Limpiar la tabla
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        #Insertar datos de presión en la tabla
        for _, row in self.df.iterrows():
            self.tree.insert("", tk.END, values = (row["Tiempo"], "-", row["Presión"]))
            
        #Calculas estadisticas
        pres_max = self.df["Presión"].max()
        pres_max_time = self.df.loc[self.df["Presión"].idxmax(), "Tiempo"]
        pres_avg = self.df["Presión"].mean()
        self.stats_label.config(
            text= f"Presión Máxima: {pres_max:.2f} PSI a las {pres_max_time}\n"
                  f"Presión Promedio: {pres_avg:.2f} PSI"
        )
    
        #Actualizar gráficas
        self.ax.clear()
        self.ax.plot(self.df["Tiempo_dt"], self.df["Presión"], label = "Presión (PSI)", color = 'blue')
        self.ax.set_title("Gráfica de Presión")
        self.ax.set_xlabel("Hora") 
        self.ax.set_ylabel("Presión (PSI)")
        self.ax.grid(True)
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        self.figure.autofmt_xdate()
        self.canvas.draw()
        
    def show_temperature_graph(self):
        if self.df is None:
            return
        
        #Limpiar la tabla
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        #Insertar datos de presión en la tabla
        for _, row in self.df.iterrows():
            self.tree.insert("", tk.END, values = (row["Tiempo"],row["Temperatura"], "-"))
            
        #Calculas estadisticas
        temp_max = self.df["Temperatura"].max()
        temp_max_time = self.df.loc[self.df["Temperatura"].idxmax(), "Tiempo"]
        temp_avg = self.df["Temperatura"].mean()
        self.stats_label.config(
            text= f"Temperatura Máxima: {temp_max:.2f} °C a las {temp_max_time}\n"
                  f"Temperatura Promedio: {temp_avg:.2f} °C"
        )
        
        self.ax.clear()
        self.ax.plot(self.df["Tiempo_dt"], self.df["Temperatura"], label = "Temperatura (°C)", color = 'red')
        self.ax.set_title("Gráfica de Temperatura")
        self.ax.set_xlabel("Hora")
        self.ax.set_ylabel("Temperatura (°C)")
        self.ax.grid(True)
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        self.figure.autofmt_xdate()
        self.canvas.draw()

if __name__ == "__main__":
    rol = sys.argv[1] if len(sys.argv) > 1 else "tecnico"
    root = tk.Tk()
    app = MonitorApp(root, rol)
    root.mainloop()