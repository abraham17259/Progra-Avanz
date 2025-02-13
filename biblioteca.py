from datetime import datetime, timedelta

class Material:
    def __init__(self, titulo, estado='disponible'):
        self.titulo = titulo
        self.estado = estado

    def prestar(self):
        if self.estado == 'disponible':
            self.estado = 'prestado'
            return True
        return False

    def devolver(self):
        self.estado = 'disponible'

class Libro(Material):
    def __init__(self, titulo, autor, genero):
        super().__init__(titulo)
        self.autor = autor
        self.genero = genero

class Revista(Material):
    def __init__(self, titulo, edicion, periodicidad):
        super().__init__(titulo)
        self.edicion = edicion
        self.periodicidad = periodicidad

class MaterialDigital(Material):
    def __init__(self, titulo, tipo_archivo, enlace):
        super().__init__(titulo, estado='disponible')
        self.tipo_archivo = tipo_archivo
        self.enlace = enlace

class Persona:
    def __init__(self, nombre, correo):
        self.nombre = nombre
        self.correo = correo

class Usuario(Persona):
    def __init__(self, nombre, correo):
        super().__init__(nombre, correo)
        self.materiales_prestados = []
        self.penalizaciones = 0

    def consultar_catalogo(self, catalogo):
        catalogo.mostrar_materiales()

    def solicitar_prestamo(self, material, bibliotecario):
        bibliotecario.procesar_prestamo(self, material)

    def devolver_material(self, material, bibliotecario):
        bibliotecario.procesar_devolucion(self, material)

class Bibliotecario(Persona):
    def __init__(self, nombre, correo, sucursal):
        super().__init__(nombre, correo)
        self.sucursal = sucursal

    def agregar_material(self, material):
        self.sucursal.agregar_material(material)

    def procesar_prestamo(self, usuario, material):
        if material.prestar():
            usuario.materiales_prestados.append(material)
            print(f"{usuario.nombre} ha tomado prestado '{material.titulo}'.")
        else:
            print("Material no disponible.")

    def procesar_devolucion(self, usuario, material):
        if material in usuario.materiales_prestados:
            usuario.materiales_prestados.remove(material)
            material.devolver()
            print(f"{usuario.nombre} ha devuelto '{material.titulo}'.")
        else:
            print("Este usuario no tiene este material en préstamo.")

class Sucursal:
    def __init__(self, nombre):
        self.nombre = nombre
        self.catalogo = []

    def agregar_material(self, material):
        self.catalogo.append(material)

    def transferir_material(self, material, otra_sucursal):
        if material in self.catalogo:
            self.catalogo.remove(material)
            otra_sucursal.agregar_material(material)
            print(f"'{material.titulo}' ha sido transferido a {otra_sucursal.nombre}.")

class Prestamo:
    def __init__(self, usuario, material, fecha_prestamo, dias_prestamo=7):
        self.usuario = usuario
        self.material = material
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = fecha_prestamo + timedelta(days=dias_prestamo)

class Penalizacion:
    def __init__(self, usuario, dias_retraso):
        self.usuario = usuario
        self.dias_retraso = dias_retraso
        self.multa = dias_retraso * 5 
        usuario.penalizaciones += self.multa

    def mostrar_penalizacion(self):
        print(f"{self.usuario.nombre} tiene una multa de ${self.multa} pesos por {self.dias_retraso} días de retraso.")

class Catalogo:
    def __init__(self):
        self.materiales = []

    def agregar_material(self, material):
        self.materiales.append(material)

    def buscar_por_titulo(self, titulo):
        return [m for m in self.materiales if titulo.lower() in m.titulo.lower()]
    
    def mostrar_materiales(self):
        for material in self.materiales:
            print(f"{material.titulo} - Estado: {material.estado}")


# Ejemplo de uso
sucursal1 = Sucursal("Biblioteca Facultad de Ingeniería")
sucursal2 = Sucursal("Biblioteca Facultad de Medicina")

bibliotecario = Bibliotecario("Ana Torres", "ana.torres@universidad.edu", sucursal1)
usuario = Usuario("Luis Gómez", "luis.gomez@alumnos.edu")

libro1 = Libro("Cálculo Integral", "James Stewart", "Matemáticas")
revista1 = Revista("Revista de Ciencia y Tecnología", "Marzo 2024", "Trimestral")

digital1 = MaterialDigital("Introducción a la IA", "PDF", "https://universidad.edu/ia-introduccion.pdf")
digital2 = MaterialDigital("Guía de Anatomía Humana", "EPUB", "https://universidad.edu/anatomia.epub")

bibliotecario.agregar_material(libro1)
bibliotecario.agregar_material(revista1)

usuario.solicitar_prestamo(libro1, bibliotecario)
usuario.devolver_material(libro1, bibliotecario)

sucursal1.transferir_material(libro1, sucursal2)

penalizacion = Penalizacion(usuario, 5)
penalizacion.mostrar_penalizacion()
