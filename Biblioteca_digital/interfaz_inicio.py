import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import os
from interfaz_busqueda import InterfazBusqueda
from interfaz_prestamo import InterfazPrestamo
from interfaz_admin import InterfazAdmin
from interfaz_usuarios import InterfazUsuarios

class InterfazInicio:
    def __init__(self, master):
        self.master = master
        self.master.title("Biblioteca Digital - Inicio")
        self.master.geometry("800x600")
        self.master.resizable(False, False)

        # Fondo principal
        self.fondo = ImageTk.PhotoImage(Image.open("assets/fondo_biblioteca.jpg"))
        self.label_fondo = tk.Label(master, image=self.fondo)
        self.label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

        # Título centrado
        self.label = tk.Label(master, text="Bienvenido a la Biblioteca Digital", font=("Georgia", 26, "bold"), bg="#ffffff", fg="#2c3e50")
        self.label.place(relx=0.5, y=50, anchor="center")

        # Botones
        self.btn_buscar = tk.Button(master, text="Buscar libros", command=self.abrir_busqueda, width=20, bg="#3498db", fg="white", font=("Arial", 14, "bold"), bd=3, relief="ridge")
        self.btn_buscar.place(relx=0.5, y=200, anchor="center")

        self.btn_prestamo = tk.Button(master, text="Realizar préstamo", command=self.abrir_prestamo, width=20, bg="#1abc9c", fg="white", font=("Arial", 14, "bold"), bd=3, relief="ridge")
        self.btn_prestamo.place(relx=0.5, y=280, anchor="center")

        self.btn_admin = tk.Button(master, text="Administrar catálogo", command=self.abrir_admin, width=20, bg="#9b59b6", fg="white", font=("Arial", 14, "bold"), bd=3, relief="ridge")
        self.btn_admin.place(relx=0.5, y=360, anchor="center")

        self.btn_usuarios = tk.Button(master, text="Gestionar Usuarios", command=self.abrir_usuarios, width=20, bg="#f39c12", fg="white", font=("Arial", 14, "bold"), bd=3, relief="ridge")
        self.btn_usuarios.place(relx=0.5, y=440, anchor="center")

    def abrir_busqueda(self):
        # Abrir ventana de búsqueda de libros
        new_window = tk.Toplevel(self.master)
        InterfazBusqueda(new_window)

    def abrir_prestamo(self):
        # Abrir ventana de préstamo de libros
        new_window = tk.Toplevel(self.master)
        InterfazPrestamo(new_window)

    def abrir_admin(self):
        # Abrir ventana de administración del catálogo
        new_window = tk.Toplevel(self.master)
        InterfazAdmin(new_window)

    def abrir_usuarios(self):
        # Abrir ventana de gestión de usuarios
        new_window = tk.Toplevel(self.master)
        InterfazUsuarios(new_window)
