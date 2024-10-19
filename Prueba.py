import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk 
import os
import random

# Configurar la ventana principal
root = tk.Tk()
root.title("Descubre la Imagen")
root.geometry("700x470")  # Expandir la ventana para las imágenes

# Ruta a la carpeta de imágenes
carpeta_imagenes = 'C:/Users/Edwin/Downloads/Lab6 - ADA/Puzzle'

# Buscar imágenes que sean .png o .jpg en la carpeta
imagenes = [os.path.join(carpeta_imagenes, img) for img in os.listdir(carpeta_imagenes) if img.endswith(('.png', '.jpg'))]

# Duplicar las imágenes para que haya pares, pero mantener las rutas originales
imagenes_duplicadas = imagenes + imagenes

# Mezclar las imágenes
random.shuffle(imagenes_duplicadas)

# Crear una lista de widgets de botones para el grid 6x6
botones = []
imagenes_tk = {}
grid_size = 6

# Imagen de reverso (tapada)
imagen_reverso = Image.open("C:/Users/Edwin/Downloads/Lab6 - ADA/Reverso.jpg")  # Imagen para tapar las imágenes
imagen_reverso = imagen_reverso.resize((100, 100), Image.Resampling.LANCZOS)
imagen_reverso_tk = ImageTk.PhotoImage(imagen_reverso)

# Variables para el manejo del estado del juego
seleccionados = []
pares_encontrados = 0

# Función para "tapar" nuevamente las imágenes si no son iguales
def tapar_imagenes():
    global seleccionados
    # Volvemos a tapar solo las imágenes que no eran iguales
    for bn, _ in seleccionados:
        bn.config(image=imagen_reverso_tk, state=tk.NORMAL, bg="SystemButtonFace")  # Restaurar el color y la imagen
    seleccionados = []

# Función que se ejecuta al hacer clic en un botón
def seleccionar_imagen(bn, img_ruta):
    global seleccionados, pares_encontrados

    # Revelar la imagen seleccionada
    bn.config(image=imagenes_tk[img_ruta], state=tk.DISABLED)
    root.update_idletasks()  # Forzar actualización de la interfaz para evitar problemas de redibujo
    seleccionados.append((bn, img_ruta))
    
    # Verificar si se han seleccionado dos imágenes
    if len(seleccionados) == 2:
        bn1, img_ruta1 = seleccionados[0]
        bn2, img_ruta2 = seleccionados[1]
        
        if img_ruta1 == img_ruta2:
            # Las imágenes son iguales, cambiar el color de fondo a verde y no taparlas
            bn1.config(bg="green")
            bn2.config(bg="green")
            pares_encontrados += 1
            seleccionados = []  # Vaciamos la lista porque son iguales y ya no se pueden volver a seleccionar
            messagebox.showinfo("¡Felicidades!", "¡Wow! las imágenes son pares iguales.")
            if pares_encontrados == len(imagenes_duplicadas) // 2:
                messagebox.showinfo("¡Felicidades!", "¡Has encontrado todos los pares!")
        else:
            # Las imágenes son diferentes, cambiar el color de fondo a rojo
            bn1.config(bg="red")
            bn2.config(bg="red")
            # Las imágenes se vuelven a tapar después de 1 segundo
            root.after(1000, tapar_imagenes)
            messagebox.showinfo("Lo sentimos", "¡Upss! las imágenes son diferentes.")

# Crear el grid de botones
indice_imagen = 0
for i in range(grid_size):
    fila = []
    for j in range(grid_size):
        if indice_imagen < len(imagenes_duplicadas):
            img_ruta = imagenes_duplicadas[indice_imagen]
            indice_imagen += 1
            
            # Cargar la imagen con Pillow y redimensionarla
            imagen_pil = Image.open(img_ruta)         
            imagen_pil = imagen_pil.resize((100, 100), Image.Resampling.LANCZOS)
            imagen_tk = ImageTk.PhotoImage(imagen_pil)
            
            # Guardar la imagen en un diccionario con la ruta como clave
            imagenes_tk[img_ruta] = imagen_tk
            
            # Crear el botón con la imagen tapada
            bn = tk.Button(root, image=imagen_reverso_tk)  # Establecer un fondo blanco
            
            # Usar img_ruta para la configuración del comando
            bn.config(command=lambda b=bn, im=img_ruta: seleccionar_imagen(b, im))
            bn.grid(row=i, column=j, padx=5, pady=5)
            
            fila.append(bn)
    botones.append(fila)

# Iniciar el loop de la interfaz
root.mainloop()