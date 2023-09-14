# Proyecto 3: Editor Assember

Curso Arquitectura de Computadores 

2do Semestre de 2020

Desarrollo de un assembler de 8 bits

![](https://github.com/JavierIbarra/Curso-ARQ/blob/main/img/ej.png)

![](https://github.com/JavierIbarra/Curso-ARQ/blob/main/img/ej_errores.png)

## Run 

### Docker

1. Installar Xming

2. Crear imagen de docker 

        docker build -t gui_image .

3. Abrir la consola y ejecutar el archivo xming.exe

        xming.exe -ac

4. Ejecutar contenedor de la imagen y conectarla a Xming, para esto necesitas conocer tu direccion ip (192.168.X.X)

        docker run -it --rm -e DISPLAY={direccion ip}:0.0 --network="host" --name gui_container gui_image


### Local

1. **Requisitos:** 

    * python
    * tkinter (sudo apt-get install python3-tk)

2. **Ejecutar archivo:**

        python assembler


## Ayuda


**El programa se separa en tres archivos importantes:**

<ul>
    <li>assemply.py (logica grafica del programa)</li>
    <li>funciones.py (funciones para detectar errores)</li>
    <li>instrucciones.txt (instrucciones soportadas)</li>
</ul>

**El programa cuenta con tres textbox:**

<ul>
    <li>El de la derecha es donde se cargan los archivos con el codigo</li>
    <li>El de arriba a la izquierda muestra el codigo binario del programa</li>
    <li>El de abajo a la izquierda muestra el binario de la memoria inicial del codigo</li>
</ul>

**Significado de los colores**

| Color | Descripcion |
| --| --|
| red | Instruccion no existe |
| yellow | Literal fuera de rango |
| magenta | Variable no declarada en DATA  |
| cyan | Etiqueta no exisite |

## Opciones

| Operacion | Atajo | Descripcion|
| -- | --| --|
| "Archivos > Guardar como" | Ctrl+S | Genera tres archivo(*.ass,* data,*.out)| 
| "Archivos > Cargar" | Ctrl+O| Carga el archivo especificado|
| "Ejecutar > Recalcular Errores" | Ctrl+R | Muestra los errores del codigo|
| "Ejecutar > Assembler" | F5 | Crea los binarios del codigo y memoria (no guarda los archivos automaticamente) |
| "Editar > Deshacer" | Ctrl+Z | Elimina ultimo cambio realizado|
| "Editar > Rehacer" | Ctrl+Y | Recupera ultimo cambio deshecho|
| "Editar > Cortar" | Ctrl+X | Corta elemento seleccionado|
| "Editar > Copiar" | Ctrl+C | Copia elemento seleccionado|
| "Editar > Pegar" | Ctrl+V | Pega en el texto seleccionado|
| "Editar > Seleccionar Todo" | Ctrl+A | Selecciona todo los elemntos del texto seleccionado |
| "Ayuda > Ayuda" |  | Informacion de uso|
| "Ayuda > Acerca de" |  | Mustra informacion de versiones |
|| "Ctrl + UP" | Aumenta tamaño de la letra en los textbox|
|| "Ctrl + DOWN" | Disminuye tamaño de la letra en los textbox|


