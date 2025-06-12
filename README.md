# MHP UI

## Virtual Environment

### Create a new virtual environment (Windows)

```bash
Comando python -m venv "Nombre del entorno"
Ejecutar python -m venv myenv
```

### Activate Virtual Environment (Windows)

```bash
Para activar el entorno
Ejecutar myenv/Scripts/activate

Para desactivar el entorno
Ejecutar myenv/Scripts/deactivate
```

### Create Virtual Environment (Linux(Ubuntu))

Lo primero que debemos hacer es instalar el paquete **python3-venv** Este paquete
es necesario para poder crear y gestionar entornos virtuales de Python en nuestro
sistema. Para instalarlo se debe ejecutar el siguiente comando en la terminal:

```bash
sudo apt install python3-venv
```

Ahora ya con el paquete instalado podemos proceder a la creación del entorno
ejecutando el siguiente comando:

```bash
python3 -m venv nombre_de_tu_entorno
```

En mi caso el nombre de mi entorno es "mientorno" entonces ejecuto

```bash
python3 -m venv mientorno
```

### Activate Virtual Environment (Linux(Ubuntu))

Para activar el entorno virtual basta con ejecutar el siguiente comando en la terminal

```bash
source nombre_de_tu_entorno/bin/activate
```

Para desactivar el entorno virtual sólo necesitamos escribir lo siguiente en la terminal

```bash
deactivate
```
