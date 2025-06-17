#Estilos, colores, fuentes que se usaron durante este proyecto
from PyQt6.QtGui import QFont, QColor

#Paleta de colores
PALETA = {
    "fondo":"#fefae0",
    "acento":"#f4a261",
    "texto":"#264653",
    "hover":"#ffb480",
    "detalle":"#e76f51",
    "error":"#e63946",
    "fondo2" :"#E2DEC4"
}

#Fuentes
def fuente(tamaño=12, negrita=False, italic=False):
    font = QFont("Helvetica", tamaño)
    font.setBold(negrita)
    font.setItalic(italic)
    return font