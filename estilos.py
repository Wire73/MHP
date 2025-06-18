#Estilos, colores, fuentes que se usaron durante este proyecto
from PyQt6.QtGui import QFont, QColor

#paleta de colores
paleta = {
    "fondo":"#fefae0",
    "acento":"#f4a261",
    "texto":"#264653",
    "boton_hover":"#ffb480",
    "detalle":"#e76f51",
    "error":"#e63946",
    "boton_press" :"#E2DEC4",
    "fondo_entry":"#F9F7F3",
    "footer": "#888888",
    "fondo2":"#E2DEC4"
}

#Fuentes
def fuente(tamaño=12, negrita=False, italic=False):
    font = QFont("Helvetica", tamaño)
    font.setBold(negrita)
    font.setItalic(italic)
    return font

#Estilos CSS
login_style = f"""

/* FONDO */
QWidget {{
    background-color: {paleta['fondo']};
    color: {paleta['texto']}
}}

/*Campos de texto */
QLineEdit {{
    background-color: {paleta['fondo_entry']};
    color: {paleta['texto']};
    padding: 5px;
    border-radius: 5px;
    border: 1px solid {paleta['detalle']};
}}

/* Botón individual "login" */
QPushButton {{
    background-color: {paleta['acento']};
    color: {paleta['texto']};
    border: 1px solid {paleta['detalle']};
    padding: 10px;
    border-radius: 5px;
}}

QPushButton:hover {{
    background-color: {paleta['boton_hover']};
}}

QPushButton:pressed {{
    background-color: {paleta['boton_press']};
}}

QLabel#footer {{
    color: {paleta['footer']};
}}

"""

menu_style = f"""

    QMebuBar {{
        background-color: {paleta['fondo']};
        color: {paleta['texto']};
    }}
    
    QMenuBar::item {{
        background-color: {paleta['fondo2']};
        padding: 6px 15px;
    }}
    
    QMenuBar::item:selected {{
        background-color: {paleta['fondo2']};
    }}
    
    QMenu {{
        background-color: {paleta['fondo2']};
        color: {paleta['texto']};
        border: 1px solid {paleta['detalle']};
    }}
    
    QMenu::item {{
        padding: 5px 25px;
    }}
    
    QMenu::item:selected {{
        background-color: {paleta['acento']}
        color: black;
    }}
    
"""

#Aplicar estilos a objeto especifico con .setObjectName("nombre")
#APlicar estilos a ese objeto con #nombre