import tkinter as tk
from tkinter import messagebox
import json
import os

class InterfazBusqueda:
    def __init__(self, master):
        self.master = master
        self.master.title("Buscar Libros")
        self.master.geometry("600x500")

        tk.Label(master, text="Buscar libros", font=("Helvetica", 14)).pack(pady=10)

        tk.Label(master, text="Filtrar por Autor:").pack(pady=5)
        self.entry_autor = tk.Entry(master, width=40)
        self.entry_autor.pack(pady=5)

        tk.Label(master, text="Filtrar por Género:").pack(pady=5)
        self.entry_genero = tk.Entry(master, width=40)
        self.entry_genero.pack(pady=5)

        self.btn_buscar = tk.Button(master, text="Buscar", command=self.buscar)
        self.btn_buscar.pack(pady=10)

        self.resultados = tk.Listbox(master, width=70, height=15)
        self.resultados.pack(pady=10)

        # Detectar doble clic en un libro
        self.resultados.bind("<Double-1>", self.mostrar_detalles)

    def buscar(self):
        autor = self.entry_autor.get().lower()
        genero = self.entry_genero.get().lower()
        self.resultados.delete(0, tk.END)

        if os.path.exists('datos/libros.json'):
            with open('datos/libros.json', 'r') as f:
                libros = json.load(f)

            for libro in libros:
                # Verificar si el libro coincide con los filtros de autor o género
                if (autor in libro['autor'].lower() or not autor) and (genero in libro['genero'].lower() or not genero):
                    estado = libro.get('estado', 'desconocido')
                    prestado_a = libro.get('prestado_a', '')

                    if estado == 'apartado' and prestado_a:
                        info_extra = f" - {estado.upper()} por {prestado_a}"
                    else:
                        info_extra = f" - {estado.upper()}"

                    self.resultados.insert(
                        tk.END, 
                        f"{libro['titulo']} - {libro['autor']} ({libro['genero']}){info_extra}"
                    )

    def mostrar_detalles(self, event):
        seleccion = self.resultados.curselection()
        if seleccion:
            indice = seleccion[0]
            texto_libro = self.resultados.get(indice)

            # Extraer el título
            titulo = texto_libro.split(" - ")[0]

            if os.path.exists('datos/libros.json'):
                with open('datos/libros.json', 'r') as f:
                    libros = json.load(f)

                for i, libro in enumerate(libros):
                    if libro['titulo'].lower() == titulo.lower():
                        # Crear nueva ventana
                        detalle_ventana = tk.Toplevel(self.master)
                        detalle_ventana.title(f"Detalles de '{libro['titulo']}'")
                        detalle_ventana.geometry("400x300")

                        detalles_texto = f"""
Título: {libro['titulo']}
Autor: {libro['autor']}
Género: {libro['genero']}
Estado: {libro.get('estado', 'desconocido').capitalize()}
Prestado a: {libro.get('prestado_a', 'Nadie')}
"""
                        tk.Label(detalle_ventana, text=detalles_texto, justify="left", font=("Helvetica", 12)).pack(pady=20)

                        # Si el libro está apartado, mostrar botón para devolver
                        if libro.get('estado') == 'apartado':
                            btn_devolver = tk.Button(
                                detalle_ventana, 
                                text="Marcar como Disponible",
                                command=lambda: self.marcar_disponible(i, detalle_ventana)
                            )
                            btn_devolver.pack(pady=10)

                        break

    def marcar_disponible(self, indice_libro, ventana):
        # Cargar libros
        if os.path.exists('datos/libros.json'):
            with open('datos/libros.json', 'r') as f:
                libros = json.load(f)

            # Cambiar estado
            libros[indice_libro]['estado'] = 'disponible'
            libros[indice_libro]['prestado_a'] = ''

            # Guardar cambios
            with open('datos/libros.json', 'w') as f:
                json.dump(libros, f, indent=4)

            ventana.destroy()  # Cerrar la ventana de detalles
            self.buscar()       # Refrescar lista de búsqueda
