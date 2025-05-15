import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime, timedelta

class InterfazPrestamo:
    def __init__(self, master):
        self.master = master
        self.master.title("Realizar Préstamo")
        self.master.geometry("600x500")

        tk.Label(master, text="Seleccionar Usuario", font=("Helvetica", 14)).pack(pady=10)

        self.lista_usuarios = tk.Listbox(master, width=50, height=10)
        self.lista_usuarios.pack(pady=10)

        self.btn_historial = tk.Button(master, text="Ver Historial de Préstamos", command=self.mostrar_historial)
        self.btn_historial.pack(pady=10)

        self.btn_prestar = tk.Button(master, text="Realizar Préstamo", command=self.realizar_prestamo)
        self.btn_prestar.pack(pady=10)

        self.btn_devolver = tk.Button(master, text="Devolver Libro", command=self.devolver_libro)
        self.btn_devolver.pack(pady=10)

        # Cargar usuarios
        self.cargar_usuarios()

    def cargar_usuarios(self):
        self.lista_usuarios.delete(0, tk.END)

        if os.path.exists('datos/usuarios.json'):
            try:
                with open('datos/usuarios.json', 'r', encoding='utf-8') as f:
                    usuarios = json.load(f)
                    if isinstance(usuarios, list):
                        for usuario in usuarios:
                            if "nombre" in usuario:
                                self.lista_usuarios.insert(tk.END, usuario["nombre"])
                            else:
                                print("Usuario mal formado:", usuario)
                    else:
                        messagebox.showerror("Error", "El archivo usuarios.json no contiene una lista.")
            except json.JSONDecodeError:
                messagebox.showerror("Error", "El archivo usuarios.json está dañado o vacío.")
        else:
            messagebox.showerror("Error", "No existe el archivo usuarios.json.")

    def mostrar_historial(self):
        seleccion = self.lista_usuarios.curselection()
        if seleccion:
            nombre_usuario = self.lista_usuarios.get(seleccion[0])

            if os.path.exists('datos/usuarios.json'):
                with open('datos/usuarios.json', 'r', encoding='utf-8') as f:
                    usuarios = json.load(f)
                    for usuario in usuarios:
                        if usuario['nombre'] == nombre_usuario:
                            libros = usuario.get('libros_prestados', [])
                            if not libros:
                                messagebox.showinfo("Historial", "No hay libros prestados actualmente.")
                            else:
                                historial = "\n".join([
                                    f"{l['titulo']} (Prestado: {l['fecha_prestamo']}, Devuelve: {l['fecha_devolucion']})"
                                    for l in libros
                                ])
                                messagebox.showinfo("Historial de Préstamos", historial)
                            return
        else:
            messagebox.showerror("Error", "Selecciona un usuario primero.")

    def realizar_prestamo(self):
        seleccion = self.lista_usuarios.curselection()
        if not seleccion:
            messagebox.showerror("Error", "Selecciona un usuario para realizar préstamo.")
            return

        nombre_usuario = self.lista_usuarios.get(seleccion[0])

        # Mostrar libros disponibles
        top = tk.Toplevel(self.master)
        top.title("Seleccionar Libro")
        top.geometry("400x400")

        tk.Label(top, text="Libros disponibles", font=("Helvetica", 12)).pack(pady=10)

        lista_libros = tk.Listbox(top, width=40, height=10)
        lista_libros.pack(pady=10)

        libros_disponibles = []
        if os.path.exists('datos/libros.json'):
            with open('datos/libros.json', 'r', encoding='utf-8') as f:
                libros = json.load(f)
                for libro in libros:
                    if libro['estado'] == 'disponible':
                        lista_libros.insert(tk.END, libro['titulo'])
                        libros_disponibles.append(libro['titulo'])

        def confirmar_prestamo():
            seleccion_libro = lista_libros.curselection()
            if seleccion_libro:
                libro_titulo = lista_libros.get(seleccion_libro[0])
                self.registrar_prestamo(libro_titulo, nombre_usuario)
                top.destroy()
            else:
                messagebox.showerror("Error", "Selecciona un libro.")

        tk.Button(top, text="Confirmar Préstamo", command=confirmar_prestamo).pack(pady=10)

    def registrar_prestamo(self, titulo_libro, nombre_usuario):
        fecha_prestamo = datetime.now()
        fecha_devolucion = fecha_prestamo + timedelta(days=7)

        # Actualizar libros
        if os.path.exists('datos/libros.json'):
            with open('datos/libros.json', 'r', encoding='utf-8') as f:
                libros = json.load(f)

            for libro in libros:
                if libro['titulo'] == titulo_libro:
                    libro['estado'] = 'apartado'
                    libro['prestado_a'] = nombre_usuario
                    break

            with open('datos/libros.json', 'w', encoding='utf-8') as f:
                json.dump(libros, f, indent=4)

        # Actualizar usuarios
        if os.path.exists('datos/usuarios.json'):
            with open('datos/usuarios.json', 'r', encoding='utf-8') as f:
                usuarios = json.load(f)

            for usuario in usuarios:
                if usuario['nombre'] == nombre_usuario:
                    usuario.setdefault('libros_prestados', []).append({
                        "titulo": titulo_libro,
                        "fecha_prestamo": fecha_prestamo.strftime("%Y-%m-%d"),
                        "fecha_devolucion": fecha_devolucion.strftime("%Y-%m-%d")
                    })
                    break

            with open('datos/usuarios.json', 'w', encoding='utf-8') as f:
                json.dump(usuarios, f, indent=4)

        messagebox.showinfo("Éxito", f"Préstamo registrado.\nFecha de devolución: {fecha_devolucion.strftime('%Y-%m-%d')}")

    def devolver_libro(self):
        seleccion = self.lista_usuarios.curselection()
        if not seleccion:
            messagebox.showerror("Error", "Selecciona un usuario para devolver libro.")
            return

        nombre_usuario = self.lista_usuarios.get(seleccion[0])

        if os.path.exists('datos/usuarios.json'):
            with open('datos/usuarios.json', 'r', encoding='utf-8') as f:
                usuarios = json.load(f)

            usuario_obj = next((u for u in usuarios if u['nombre'] == nombre_usuario), None)

            if usuario_obj and usuario_obj['libros_prestados']:
                top = tk.Toplevel(self.master)
                top.title("Devolver Libro")
                top.geometry("400x400")

                tk.Label(top, text="Selecciona libro a devolver", font=("Helvetica", 12)).pack(pady=10)

                lista_libros = tk.Listbox(top, width=40, height=10)
                lista_libros.pack(pady=10)

                for libro in usuario_obj['libros_prestados']:
                    lista_libros.insert(tk.END, libro['titulo'])

                def confirmar_devolucion():
                    seleccion_libro = lista_libros.curselection()
                    if seleccion_libro:
                        libro_titulo = lista_libros.get(seleccion_libro[0])
                        self.registrar_devolucion(nombre_usuario, libro_titulo)
                        top.destroy()
                    else:
                        messagebox.showerror("Error", "Selecciona un libro.")

                tk.Button(top, text="Confirmar Devolución", command=confirmar_devolucion).pack(pady=10)

            else:
                messagebox.showinfo("Información", "Este usuario no tiene libros prestados.")

    def registrar_devolucion(self, nombre_usuario, titulo_libro):
        # Actualizar libros
        if os.path.exists('datos/libros.json'):
            with open('datos/libros.json', 'r', encoding='utf-8') as f:
                libros = json.load(f)

            for libro in libros:
                if libro['titulo'] == titulo_libro:
                    libro['estado'] = 'disponible'
                    libro['prestado_a'] = ""
                    break

            with open('datos/libros.json', 'w', encoding='utf-8') as f:
                json.dump(libros, f, indent=4)

        # Actualizar usuarios
        if os.path.exists('datos/usuarios.json'):
            with open('datos/usuarios.json', 'r', encoding='utf-8') as f:
                usuarios = json.load(f)

            for usuario in usuarios:
                if usuario['nombre'] == nombre_usuario:
                    usuario['libros_prestados'] = [l for l in usuario['libros_prestados'] if l['titulo'] != titulo_libro]
                    break

            with open('datos/usuarios.json', 'w', encoding='utf-8') as f:
                json.dump(usuarios, f, indent=4)

        messagebox.showinfo("Éxito", "Devolución registrada exitosamente.")
