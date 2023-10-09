import tkinter as tk
from tkinter import messagebox
from urllib.request import urlopen
from urllib.error import URLError
import json
import re

# Función para comprobar si una URL es válida
def is_valid_url(url):
    # Utiliza una expresión regular para verificar el formato de la URL
    url_pattern = re.compile(r'^(https?://)?(www\.)?[A-Za-z0-9\.-]+(\.[A-Za-z]{2,})+')
    return bool(url_pattern.match(url))

# Función para comprobar la conectividad
def check_connectivity():
    # Obtiene la URL ingresada por el usuario
    url = url_entry.get()
    if not is_valid_url(url):
        # Muestra un mensaje de error si la URL no es válida
        messagebox.showerror("Error de URL", "La URL ingresada no es válida. Asegúrate de que tenga el formato correcto (por ejemplo, https://www.ejemplo.com).")
        return

    try:
        # Intenta conectarse a la URL
        response = urlopen(url)
        if response.getcode() == 200:
            # Si la respuesta tiene un código 200, muestra que el sitio está en línea y funcionando
            result_label.config(text="El sitio está en línea y funcionando.")
        else:
            # Si el código no es 200, muestra un mensaje con el código de estado
            result_label.config(text="El sitio está en línea, pero ha devuelto un código de estado " + str(response.getcode()) + ".")
    except URLError as e:
        # Si se produce un error al conectar, muestra un mensaje de error
        error_message = f"Error al conectar: {str(e)}"
        result_label.config(text=error_message)
        messagebox.showerror("Error de Conexión", "No se pudo conectar al sitio web. Verifica la URL e inténtalo de nuevo.")

# Función para agregar un sitio a la lista de favoritos
def add_to_favorites():
    # Obtiene la URL ingresada por el usuario
    url = url_entry.get()
    if not is_valid_url(url):
        # Muestra un mensaje de error si la URL no es válida
        messagebox.showerror("Error de URL", "La URL ingresada no es válida.")
        return

    # Agrega la URL a la lista de favoritos y guarda la lista
    favorites_listbox.insert(tk.END, url)
    save_favorites()

# Función para eliminar un sitio de la lista de favoritos
def remove_from_favorites():
    # Obtiene el índice del elemento seleccionado en la lista de favoritos
    selected_index = favorites_listbox.curselection()
    if selected_index:
        # Elimina el elemento seleccionado de la lista de favoritos y guarda la lista actualizada
        favorites_listbox.delete(selected_index)
        save_favorites()

# Función para guardar la lista de favoritos en un archivo JSON
def save_favorites():
    # Obtiene los elementos de la lista de favoritos
    favorites = favorites_listbox.get(0, tk.END)
    # Guarda la lista en un archivo JSON llamado "favorites.json"
    with open("favorites.json", "w") as file:
        json.dump(favorites, file)

# Función para cargar la lista de favoritos desde un archivo JSON
def load_favorites():
    try:
        with open("favorites.json", "r") as file:
            # Carga la lista de favoritos desde el archivo
            favorites = json.load(file)
            for url in favorites:
                # Agrega los elementos a la lista de favoritos
                favorites_listbox.insert(tk.END, url)
    except FileNotFoundError:
        # Maneja la excepción si el archivo no se encuentra
        pass

# Creación de la ventana de la aplicación y elementos de la GUI
app = tk.Tk()
app.title("Comprobador de Conectividad de Sitios Web")

url_label = tk.Label(app, text="Ingresa la URL del sitio web:")
url_label.pack(pady=10)
url_entry = tk.Entry(app, width=40)
url_entry.pack()

check_button = tk.Button(app, text="Comprobar Conectividad", command=check_connectivity)
check_button.pack(pady=10)

result_label = tk.Label(app, text="")
result_label.pack()

favorites_label = tk.Label(app, text="Sitios Favoritos:")
favorites_label.pack()
favorites_listbox = tk.Listbox(app, selectmode=tk.SINGLE, width=40)
favorites_listbox.pack()
load_favorites()

add_to_favorites_button = tk.Button(app, text="Agregar a Favoritos", command=add_to_favorites)
add_to_favorites_button.pack()

remove_from_favorites_button = tk.Button(app, text="Eliminar de Favoritos", command=remove_from_favorites)
remove_from_favorites_button.pack()

# Inicia el bucle principal de la GUI
app.mainloop()
