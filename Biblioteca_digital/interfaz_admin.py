import tkinter as tk
from tkinter import messagebox
import json
import os


class InterfazAdmin:
    def __init__(self, master):
        self.master = master
        self.master.title("Administrar Catálogo")
        self.master.geometry("600x500")

        # Agregar libro
        tk.Label(master, text="Agregar Nuevo Libro", font=("Helvetica", 14)).pack(pady=10)

        # Etiquetas fuera de los cuadros de texto
        tk.Label(master, text="Título del libro:").pack()
        self.entry_titulo = tk.Entry(master, width=40)
        self.entry_titulo.pack(pady=5)

        tk.Label(master, text="Autor del libro:").pack()
        self.entry_autor = tk.Entry(master, width=40)
        self.entry_autor.pack(pady=5)

        tk.Label(master, text="Género del libro:").pack()
        self.entry_genero = tk.Entry(master, width=40)
        self.entry_genero.pack(pady=5)

        self.btn_agregar = tk.Button(master, text="Agregar Libro", command=self.agregar_libro)
        self.btn_agregar.pack(pady=10)

        # Listado de libros
        self.lista_libros = tk.Listbox(master, width=50, height=10)
        self.lista_libros.pack(pady=10)

        self.btn_eliminar = tk.Button(master, text="Eliminar Libro", command=self.eliminar_libro)
        self.btn_eliminar.pack(pady=10)

        self.cargar_libros()

    def agregar_libro(self):
        titulo = self.entry_titulo.get()
        autor = self.entry_autor.get()
        genero = self.entry_genero.get()

        if not titulo or not autor or not genero:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        nuevo_libro = {
            "titulo": titulo,
            "autor": autor,
            "genero": genero,
            "estado": "disponible"
        }

        # Almacenar el libro en el archivo JSON
        if os.path.exists('datos/libros.json'):
            with open('datos/libros.json', 'r') as f:
                libros = json.load(f)
        else:
            libros = []

        libros.append(nuevo_libro)

        with open('datos/libros.json', 'w') as f:
            json.dump(libros, f, indent=4)

        messagebox.showinfo("Éxito", "Libro agregado exitosamente.")
        self.cargar_libros()

    def cargar_libros(self):
        self.lista_libros.delete(0, tk.END)
        if os.path.exists('datos/libros.json'):
            with open('datos/libros.json', 'r') as f:
                libros = json.load(f)

            for libro in libros:
                self.lista_libros.insert(tk.END, libro['titulo'])

    def eliminar_libro(self):
        seleccion = self.lista_libros.curselection()
        if seleccion:
            titulo_libro = self.lista_libros.get(seleccion[0])

            # Verificar si el libro está prestado
            if os.path.exists('datos/libros.json'):
                with open('datos/libros.json', 'r') as f:
                    libros = json.load(f)

                libro_a_eliminar = None
                for libro in libros:
                    if libro['titulo'] == titulo_libro:
                        libro_a_eliminar = libro
                        break

                if libro_a_eliminar:
                    if libro_a_eliminar.get('estado') == 'prestado':
                        messagebox.showerror("Error", "No puedes eliminar un libro que está prestado.")
                        return

                    libros = [libro for libro in libros if libro['titulo'] != titulo_libro]

                    with open('datos/libros.json', 'w') as f:
                        json.dump(libros, f, indent=4)

                    messagebox.showinfo("Éxito", "Libro eliminado exitosamente.")
                    self.cargar_libros()
                else:
                    messagebox.showerror("Error", "El libro no existe.")
        else:
            messagebox.showerror("Error", "Debes seleccionar un libro.")
