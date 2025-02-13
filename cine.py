class Persona:

    lista=[]
    
    def __init__(self,nombre,correo):
        self.nombre=nombre
        self.correo=correo

    def registrar(self):
        Persona.lista.append(self)
        print(f"La persona {self.nombre} ha sido registrada con el correo {self.correo}")

    def actualizar_datos(self,nombre,correo):
        self.nombre=nombre
        self.correo=correo
        print(f"Los datos han sido actualizados")

    @classmethod
    def personas_registradas(cls):
        print("Personas registradas")
        for Persona in cls.lista:
            print(f"-{Persona.nombre} - {Persona.correo}")

class Usuario(Persona):
    def __init__(self, nombre, correo):
        super().__init__(nombre, correo)
        self.historial_reservas = []

    def reservar(self, funcion, asientos):
        if asientos <= funcion.asientos_disponibles:
            funcion.asientos_disponibles -= asientos
            self.historial_reservas.append({"funcion": funcion, "asientos": asientos})
            print(f"Reserva realizada para '{funcion.pelicula.titulo}' en la sala {funcion.sala.identificador}.")
        else:
            print("No hay suficientes asientos disponibles.")

    def cancelar_reserva(self, funcion):
        reserva = next((r for r in self.historial_reservas if r["funcion"] == funcion), None)
        if reserva:
            funcion.asientos_disponibles += reserva["asientos"]
            self.historial_reservas.remove(reserva)
            print(f"Reserva cancelada para '{funcion.pelicula.titulo}'.")
        else:
            print("No tienes una reserva para esta función.")

class Empleado(Persona):
    def __init__(self, nombre, correo, rol):
        super().__init__(nombre, correo)
        self.rol = rol

    def agregar_funcion(self, funcion):
        print(f"Función agregada: {funcion.pelicula.titulo} a las {funcion.hora} en la sala {funcion.sala.identificador}.")

    def modificar_promocion(self, promocion, nuevo_descuento, nuevas_condiciones):
        promocion.descuento = nuevo_descuento
        promocion.condiciones = nuevas_condiciones
        print(f"Promoción modificada: {nuevo_descuento}% de descuento. {nuevas_condiciones}.")

class Espacio:
    def __init__(self,capacidad,identificador):
        self.capacidad=capacidad
        self.identificador=identificador
    
    def descripcion(self):
        print(f"El edificio tiene tamaño {self.capacidad} y tiene id {self.identificador}")

class Sala(Espacio):
    def __init__(self,capacidad,identificador,tipo):
        super().__init__(capacidad,identificador)
        self.tipo=tipo
        self.disponibilidad=True

    def Consultardisponibilidad(self):
        if self.disponibilidad:
            print("La sala esta disponible")
        else:
            print("La sala esta ocupada")

class Pelicula:
    def __init__(self, titulo, genero, duracion):
        self.titulo = titulo
        self.genero = genero
        self.duracion = duracion

class Funcion:
    def __init__(self, pelicula, sala, hora, asientos_disponibles=None):
        self.pelicula = pelicula
        self.sala = sala
        self.hora = hora
        self.asientos_disponibles = asientos_disponibles or sala.capacidad

class Promocion:
    def __init__(self, descuento, condiciones):
        self.descuento = descuento
        self.condiciones = condiciones

    def mostrar(self):
        print(f"Promoción: {self.descuento}% de descuento. Condiciones: {self.condiciones}")



pelicula1 = Pelicula("Matrix", "Ciencia Ficción", 136)
pelicula2 = Pelicula("Titanic", "Drama/Romance", 195)

sala1 = Sala(100,"Sala 1","3DX")
sala2 = Sala(50,"Sala 2","Tradicional")

funcion1 = Funcion(pelicula1, sala1, "18:00")
funcion2 = Funcion(pelicula2, sala2, "20:00")

usuario1 = Usuario("Ana Pérez", "ana.perez@email.com")
empleado1 = Empleado("Luis Martínez", "luis.martinez@email.com", "Gerente")

usuario1.registrar()
empleado1.registrar()

usuario1.reservar(funcion1, 3)

usuario1.cancelar_reserva(funcion1)

promocion1 = Promocion(20, "Válido de lunes a jueves.")
promocion1.mostrar()
empleado1.modificar_promocion(promocion1, 30, "Válido todos los días antes de las 5 PM.")

Persona.personas_registradas()