#Modulo del login
import os, sys, sqlite3, bcrypt
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, 
    QMessageBox, QApplication, QSpacerItem, QSizePolicy
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from estilos import paleta, fuente, login_style

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inicio de Sesión - MHP")
        self.setFixedSize(600, 650)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        #Se aplican los estilos
        self.setStyleSheet(login_style)
        
        #logo
        logo_lbl = QLabel()
        logo_path = os.path.join("img", "logo_empresa.png")
        if os.path.exists(logo_path):
            pix = QPixmap(logo_path).scaledToWidth(350, Qt.TransformationMode.SmoothTransformation)
            logo_lbl.setPixmap(pix)
        logo_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_lbl)
        
        #titulos
        t1 = QLabel("Martillos Hidráulicos de la Península")
        t1.setFont(fuente(20, negrita=True))
        t1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(t1)
        
        t2 = QLabel("Sistema de Gestión de Monitoreo")
        t2.setFont(fuente(14, italic=True))
        t2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(t2)
        
        #Formulario de login
        self.user_in = QLineEdit()
        self.user_in.setPlaceholderText("Usuario")
        self.user_in.setFont(fuente())
        
        self.pwd_in = QLineEdit()
        self.pwd_in.setPlaceholderText("Contraseña")
        self.pwd_in.setEchoMode(QLineEdit.EchoMode.Password)
        self.pwd_in.setFont(fuente())
        
        layout.addWidget(self.user_in)
        layout.addWidget(self.pwd_in)
        
        #Mostrar/ocultar contraseña
        self.btn_toggle = QPushButton("Mostrar/Ocultar contraseña")
        self.btn_toggle.setFont(fuente())
        self.btn_toggle.clicked.connect(self.toggle_password)
        layout.addWidget(self.btn_toggle)
        
        #Botón de login
        btn_login = QPushButton("Iniciar Sesión")
        btn_login.setFont(fuente(12, negrita=True))
        btn_login.clicked.connect(self.handle_login)
        layout.addWidget(btn_login)
        
        #Pie de página
        footer_layout = QVBoxLayout()
        footer = QLabel("© 2025 Martillos Hidráulicos de la Península - Todos los derechos reservados")
        footer.setFont(fuente(9, italic=True))
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setObjectName("footer")
        
        footer2 = QLabel("Version 2.0")
        footer2.setFont(fuente(9, italic=True))
        footer2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer2.setObjectName("footer")
        
        footer_layout.addWidget(footer)
        footer_layout.addWidget(footer2)
        
        layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        layout.addLayout(footer_layout)
        
        self.setLayout(layout)
        qr = self.frameGeometry()
        cp = QApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def toggle_password(self):
        if self.pwd_in.echoMode() == QLineEdit.EchoMode.Normal:
            self.pwd_in.setEchoMode(QLineEdit.EchoMode.Password)
            self.btn_toggle.setText("Mostrar contraseña")
        else:
            self.pwd_in.setEchoMode(QLineEdit.EchoMode.Normal)
            self.btn_toggle.setText("Ocultar contraseña")
    
    def handle_login(self):
        usuario = self.user_in.text().lower()
        password = self.pwd_in.text()
        
        if not usuario or not password:
            QMessageBox.warning(self, "Error", "Por favor, complete todos los campos.")
            return
        
        try:
            conn = sqlite3.connect("usuarios.db")
            c = conn.cursor()
            c.execute("SELECT password, rol FROM usuarios WHERE usuario = ?", (usuario,))
            row = c.fetchone()
            conn.close()
            
            if row and bcrypt.checkpw(password.encode(), row[0]):
                rol = row[1]
                QMessageBox.information(self, "Éxito", f"Bienvenido, {usuario} ({rol})!")
                from monitor import MonitorWindow
                self.hide()
                self.monitor = MonitorWindow(usuario, rol)
                self.monitor.show()
            else:
                QMessageBox.critical(self, "Error", "Usuario o contraseña incorrectos.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al conectar a la base de datos: {str(e)}")

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())