import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime

class InterfazUsuarios:
    def __init__(self, master):
        self.master = master
        self.master.title("Gestionar Usuarios")
        self.master.geometry("600x500")

        tk.Label(master, text="Crear Nuevo Usuario", font=("Helvetica", 14)).pack(pady=10)

        # Etiquetas fuera de los cuadros de texto
        tk.Label(master, text="Nombre del usuario:").pack()
        self.entry_nombre = tk.Entry(master, width=40)
        self.entry_nombre.pack(pady=5)

        tk.Label(master, text="Correo del usuario:").pack()
        self.entry_email = tk.Entry(master, width=40)
        self.entry_email.pack(pady=5)

        tk.Label(master, text="Teléfono del usuario:").pack()
        self.entry_telefono = tk.Entry(master, width=40)
        self.entry_telefono.pack(pady=5)

        self.btn_crear = tk.Button(master, text="Crear Usuario", command=self.crear_usuario)
        self.btn_crear.pack(pady=10)

        # Listado de usuarios
        self.lista_usuarios = tk.Listbox(master, width=50, height=10)
        self.lista_usuarios.pack(pady=10)

        self.btn_eliminar = tk.Button(master, text="Eliminar Usuario", command=self.eliminar_usuario)
        self.btn_eliminar.pack(pady=10)

        self.cargar_usuarios()

    def crear_usuario(self):
        nombre = self.entry_nombre.get()
        email = self.entry_email.get()
        telefono = self.entry_telefono.get()

        if not nombre or not email or not telefono:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        nuevo_usuario = {
            "nombre": nombre,
            "email": email,
            "telefono": telefono,
            "libros_prestados": []
        }

        if os.path.exists('datos/usuarios.json'):
            with open('datos/usuarios.json', 'r') as f:
                usuarios = json.load(f)
        else:
            usuarios = []

        usuarios.append(nuevo_usuario)

        with open('datos/usuarios.json', 'w') as f:
            json.dump(usuarios, f, indent=4)

        messagebox.showinfo("Éxito", "Usuario creado exitosamente.")
        self.cargar_usuarios()

    def cargar_usuarios(self):
        self.lista_usuarios.delete(0, tk.END)
        if os.path.exists('datos/usuarios.json'):
            with open('datos/usuarios.json', 'r') as f:
                usuarios = json.load(f)

            for usuario in usuarios:
                self.lista_usuarios.insert(tk.END, usuario['nombre'])

    def eliminar_usuario(self):
        seleccion = self.lista_usuarios.curselection()
        if seleccion:
            nombre_usuario = self.lista_usuarios.get(seleccion[0])

            # Verificar si el usuario tiene libros prestados
            if os.path.exists('datos/libros.json'):
                with open('datos/libros.json', 'r') as f:
                    libros = json.load(f)

                libros_prestados = any(libro.get('prestado_a') == nombre_usuario and libro.get('estado') == 'prestado' for libro in libros)

                if libros_prestados:
                    messagebox.showerror("Error", "No puedes eliminar un usuario con libros prestados.")
                    return

            if os.path.exists('datos/usuarios.json'):
                with open('datos/usuarios.json', 'r') as f:
                    usuarios = json.load(f)

                usuarios = [usuario for usuario in usuarios if usuario['nombre'] != nombre_usuario]

                with open('datos/usuarios.json', 'w') as f:
                    json.dump(usuarios, f, indent=4)

                messagebox.showinfo("Éxito", "Usuario eliminado exitosamente.")
                self.cargar_usuarios()
        else:
            messagebox.showerror("Error", "Debes seleccionar un usuario.")
