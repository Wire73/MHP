#Código fuente del programa
import os, sys, sqlite3, bcrypt
import pandas as pd
from datetime import datetime
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QApplication,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox 
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from estilos import paleta, fuente, login_style, menu_style

class MonitorWindow(QMainWindow):
    def __init__(self, usuario, rol):
        super().__init__()
        self.usuario = usuario
        self.rol = rol
        self.df = None
        self.stats_data = {}
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle(f"MHP Monitoreo - {self.usuario} ({self.rol})")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet(login_style)
        
        #widgets
        self.table = QTableWidget()
        self.total_lbl = QLabel("Total Horas: 0h")
        self.stats_lbl = QLabel("")
        self.file_lbl = QLabel("")
        
        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.ax = self.canvas.figure.add_subplot(111)
        self.ax.set_facecolor(paleta['fondo2'])
        self.canvas.figure.patch.set_facecolor(paleta['fondo2'])
        
        #Menu-Bar
        menubar = self.menuBar()
        menubar.setStyleSheet(menu_style)
        
        #Archivo Menú
        archivo_menu = menubar.addMenu("Archivo")
        
        #Acciones: Cargar, Exportar, Nuevo usuario
        load_action = archivo_menu.addAction("Cargar Archivo")
        load_action.triggered.connect(self.load_file)
        export_action = archivo_menu.addAction("Exportar Archivo")
        export_action.triggered.connect(self.export_summary)
        if self.rol == "admin":
            new_user = archivo_menu.addAction("Crear Nuevo Usuario")
            new_user.triggered.connect(self.create_user)
        archivo_menu.addSeparator() #Crear linea de separación
        logout_action = archivo_menu.addAction("Cerrar Sesión")
        logout_action.triggered.connect(self.logout)
        exit_action = archivo_menu.addAction("Salir")
        exit_action.triggered.connect(self.close)
        
        #Vista Menu
        vista_menu = menubar.addMenu("Vista")
        
        #Acciones: Mostrar gráficas y datos
        full_graph = vista_menu.addAction("Gráficas Completas")
        full_graph.triggered.connect(self.show_both_graphs)
        temp_graph = vista_menu.addAction("Gráfica de Temperatura")
        temp_graph.triggered.connect(self.show_temperature_graph)
        press_graph = vista_menu.addAction("Gráfica de Presión")
        press_graph.triggered.connect(self.show_pressure_graph)
        
        left_panel = QVBoxLayout()
        left_panel.addWidget(self.table)
        left_panel.addWidget(self.total_lbl)
        left_panel.addWidget(self.stats_lbl)
        left_panel.addWidget(self.file_lbl)
            
        right_panel = QVBoxLayout()
        right_panel.addWidget(self.canvas)
            
        main_area = QHBoxLayout()
        main_area.addLayout(left_panel, 3)
        main_area.addLayout(right_panel, 4)
            
        container = QWidget()
        layout = QVBoxLayout()
        layout.addLayout(main_area)
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        #Centrar ventana
        qr = self.frameGeometry()
        cp = QApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def load_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Abrir CSV", "", "CSV (*.csv)")
        if not path: return
            
        try:
            self.df = pd.read_csv(path, header=None, names=["Tiempo", "Temperatura", "Presión"])
            self.df["Tiempo_dt"] = pd.to_datetime(self.df["Tiempo"], format="%H:%M:%S")
            self.update_all()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
        
    def update_all(self):
        self.update_table(self.df)
        self.update_stats()
        self.show_both_graphs()
        
    def update_table(self, df):
        self.table.clear()
        columnas = [col for col in df.columns if col != "Tiempo_dt"]
        self.table.setRowCount(len(df))
        self.table.setColumnCount(len(columnas))
        self.table.setHorizontalHeaderLabels(columnas)
        for i, row in df.iterrows():
            for j, col in enumerate(columnas):
                val = row[col] if not pd.isna(row[col]) else "" 
                self.table.setItem(i, j, QTableWidgetItem(str(val)))
        
    def update_stats(self):
        df  = self.df
        t0, t1 = df["Tiempo_dt"].iloc[0], df["Tiempo_dt"].iloc[-1]
        diff = t1 - t0
        h, m = divmod(diff.total_seconds() // 60, 60)
        tmax, t0t = df["Temperatura"].max(), df.loc[df["Temperatura"].idxmax(), "Tiempo"]
        pmax, p0t = df["Presión"].max(), df.loc[df["Presión"].idxmax(), "Tiempo"]
        tav, pav = df["Temperatura"].mean(), df["Presión"].mean()
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            
        self.total_lbl.setText(f"Total Horas: {int(h)}h {int(m)}m")
        self.stats_lbl.setText(
            f"Temperatura Máxima: {tmax:.2f}°C a las {t0t}\nPresión Máxima: {pmax:.2f}PSI a las {p0t}\n"
            F"Temperatura Promedio: {tav:.2f}°C | Presión Promedio: {pav:.2f}PSI\n"
        )  
            
        self.file_lbl.setText(f"Archivo cargado el {now}")
        self.stats_data = {
            "Horas trabajadas": f"{int(h)}h {int(m)}m",
            "Temperatura máxima": f"{tmax:.2f}°C a las {t0t}",
            "Presión máxima": f"{pmax:.2f}PSI a las {p0t}",
            "Temperatura promedio": f"{tav:.2f}°C",
            "Presión promedio": f"{pav:.2f}PSI",
            "Fecha de carga": now
        }
        
    def export_summary(self):
        if not self.stats_data:
            QMessageBox.warning(self, "Advertencia", "No hay datos para exportar.")
            return
        path, _ = QFileDialog.getSaveFileName(self, "Exportar Resumen", "", "CSV (*.csv)")
        if not path: return
        pd.DataFrame.from_dict(self.stats_data, orient='index', columns=['Valor']).to_csv(path, encoding='utf-8')
        QMessageBox.information(self, "Éxito", f"Resumen exportado a {path}")
            
    def logout(self):
        QMessageBox.information(self, "Cerrar Sesión", "Se cerrará la sesión actual.")
        self.close()
        os.execl(sys.executable, sys.executable, *sys.argv)
        
    def create_user(self):
        from PyQt6.QtWidgets import QDialog, QLineEdit, QComboBox, QDialogButtonBox
        dlg = QDialog(self)
        dlg.setWindowTitle("Crear Nuevo Usuario")
        dlg.setFixedSize(300, 200)
            
        ue  = QLineEdit(); ue.setPlaceholderText("Usuario")
        pe  = QLineEdit(); pe.setPlaceholderText("Contraseña"); pe.setEchoMode(QLineEdit.EchoMode.Password)
        combo = QComboBox(); combo.addItems(["admin", "tecnico"])
            
        box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        box.accepted.connect(dlg.accept)
        box.rejected.connect(dlg.reject)
            
        lay = QVBoxLayout()
        lay.addWidget(ue); lay.addWidget(pe); lay.addWidget(combo); lay.addWidget(box)
        dlg.setLayout(lay)
            
        if dlg.exec():
            u, p, r = ue.text(), pe.text(), combo.currentText()
            if not u or not p:
                QMessageBox.warning(self, "Error", "Por favor, complete todos los campos.")
                return
            try:
                conn = sqlite3.connect("usuarios.db")
                c = conn.cursor()
                hashed = bcrypt.hashpw(p.encode('utf-8'), bcrypt.gensalt())
                c.execute("INSERT INTO usuarios (usuario, password, rol) VALUES (?, ?, ?)", (u, hashed, r))
                conn.commit(); conn.close()
                QMessageBox.information(self, "Éxito", f"Usuario '{u}' creado correctamente como {r}.")
            except sqlite3.IntegrityError:
                QMessageBox.warning(self, "Error", "Usuario '{u}' ya existe.")
        
    def show_graphs(self, tipo="ambos"):
        self.ax.clear()
        if tipo in ("ambos", "temp"):
            self.ax.plot(self.df["Tiempo_dt"], self.df["Temperatura"], label="Temperatura", color='red')
        if tipo in ("ambos", "press"):
            self.ax.plot(self.df["Tiempo_dt"], self.df["Presión"], label="Presión", color='blue')
        title = {
            "ambos": "Temperatura y Presión",
            "temp": "Temperatura",
            "press": "Presión"
        }[tipo]
        ylabel = {
            "ambos": "Temperatura (°C) / Presión (PSI)",
            "temp": "Temperatura (°C)",
            "press": "Presión (PSI)"
        }[tipo]
        self.ax.set_title(title)
        self.ax.set_xlabel("Hora")
        self.ax.set_ylabel(ylabel)
        self.ax.legend(); self.ax.grid(True)
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
        self.canvas.figure.autofmt_xdate()
        self.canvas.draw()
        
    def show_both_graphs(self):
        self.show_graphs("ambos")
        self.update_table(self.df)
        self.update_stats
        
    def show_temperature_graph(self):
        self.show_graphs("temp")
        temp_df = self.df[["Tiempo", "Temperatura", "Tiempo_dt"]].copy()
        self.update_table(temp_df)
        self.update_temperature_stats(temp_df)
        
    def show_pressure_graph(self):
        self.show_graphs("press")
        press_df = self.df[["Tiempo", "Presión", "Tiempo_dt"]].copy()
        self.update_table(press_df)
        self.update_pressure_stats(press_df)
    
    def update_temperature_stats(self, df):
        tmax = df["Temperatura"].max()
        t0t = df.loc[df["Temperatura"].idxmax(), "Tiempo"]
        tav = df["Temperatura"].mean()
        self.stats_lbl.setText(
            f"Temperatura Máxima: {tmax:.2f}°C a las {t0t}\n"
            f"Temperatura Promedio: {tav:.2f}°C"
        )
    
    def update_pressure_stats(self, df):
        pmax = df["Presión"].max()
        p0t = df.loc[df["Presión"].idxmax(), "Tiempo"]
        pav = df["Presión"].mean()
        self.stats_lbl.setText(
            f"Presión Máxima: {pmax:.2f}PSI a las {p0t}\n"
            f"Presión Promedio: {pav:.2f}PSI"
        )
            
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    rol = sys.argv[1] if len(sys.argv) > 1 else "tecnico"
    app = QApplication(sys.argv)
    window = MonitorWindow(rol)
    window.show()
    sys.exit(app.exec())