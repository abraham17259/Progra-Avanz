class Persona:
    lista_personas = []
    
    def __init__(self, nombre, contacto):
        self.nombre = nombre
        self.contacto = contacto
    
    def registrar(self):
        Persona.lista_personas.append(self)
        print(f"{self.nombre} ha sido registrado correctamente.")
    
    @classmethod
    def personas_registradas(cls):
        print("Personas registradas:")
        for persona in cls.lista_personas:
            print(f"- {persona.nombre} ({persona.contacto})")

class Cliente(Persona):
    def __init__(self, nombre, contacto):
        super().__init__(nombre, contacto)
        self.historial_pedidos = []
    
    def realizar_pedido(self, pedido):
        if pedido.validar_pedido():
            self.historial_pedidos.append(pedido)
            pedido.confirmar_pedido()
        else:
            print("Pedido rechazado por falta de stock.")
    
    def consultar_historial(self):
        print(f"Historial de pedidos de {self.nombre}:")
        for pedido in self.historial_pedidos:
            print(f"- Pedido: {pedido.productos}, Estado: {pedido.estado}, Total: {pedido.total}")

class Empleado(Persona):
    def __init__(self, nombre, contacto, rol):
        super().__init__(nombre, contacto)
        self.rol = rol
    
    def actualizar_inventario(self, inventario, ingrediente, cantidad):
        inventario.actualizar_stock(ingrediente, cantidad)
    
class ProductoBase:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio
    
class Bebida(ProductoBase):
    def __init__(self, nombre, precio, tamano, tipo, opciones=None):
        super().__init__(nombre, precio)
        self.tamano = tamano
        self.tipo = tipo
        self.opciones = opciones if opciones else []
    
class Postre(ProductoBase):
    def __init__(self, nombre, precio, vegano=False, sin_gluten=False):
        super().__init__(nombre, precio)
        self.vegano = vegano
        self.sin_gluten = sin_gluten
    
class Inventario:
    def __init__(self):
        self.ingredientes = {}
    
    def actualizar_stock(self, ingrediente, cantidad):
        self.ingredientes[ingrediente] = self.ingredientes.get(ingrediente, 0) + cantidad
        print(f"Inventario actualizado: {ingrediente} -> {self.ingredientes[ingrediente]}")
    
    def verificar_stock(self, ingredientes_necesarios):
        return all(self.ingredientes.get(ing, 0) >= cant for ing, cant in ingredientes_necesarios.items())
    
    def consumir_ingredientes(self, ingredientes_necesarios):
        if self.verificar_stock(ingredientes_necesarios):
            for ing, cant in ingredientes_necesarios.items():
                self.ingredientes[ing] -= cant
            return True
        return False
    
class Pedido:
    def __init__(self, cliente, productos, inventario):
        self.cliente = cliente
        self.productos = productos
        self.estado = "Pendiente"
        self.total = sum(prod.precio for prod in productos)
        self.inventario = inventario
    
    def validar_pedido(self):
        ingredientes_necesarios = {}
        return self.inventario.verificar_stock(ingredientes_necesarios)
    
    def confirmar_pedido(self):
        if self.inventario.consumir_ingredientes({}):
            self.estado = "En preparación"
            print(f"Pedido confirmado para {self.cliente.nombre}. Total: ${self.total}")
        else:
            print("No se pudo procesar el pedido por falta de ingredientes.")
    
class Promocion:
    def __init__(self, descripcion, descuento):
        self.descripcion = descripcion
        self.descuento = descuento
    
    def aplicar_descuento(self, pedido):
        pedido.total *= (1 - self.descuento / 100)
        print(f"Promoción aplicada: {self.descripcion}. Nuevo total: ${pedido.total}")

# Ejemplo de uso
inventario = Inventario()
inventario.actualizar_stock("Café", 10)
inventario.actualizar_stock("Leche", 5)

cliente1 = Cliente("Ana Pérez", "ana@email.com")
cliente1.registrar()

empleado1 = Empleado("Luis Martínez", "luis@email.com", "Barista")
empleado1.registrar()

bebida1 = Bebida("Café Latte", 4.5, "Grande", "Caliente", ["Leche de almendra"])
postre1 = Postre("Brownie", 3.0, sin_gluten=True)

pedido1 = Pedido(cliente1, [bebida1, postre1], inventario)
cliente1.realizar_pedido(pedido1)

promocion1 = Promocion("Descuento del 10% para clientes frecuentes", 10)
promocion1.aplicar_descuento(pedido1)

cliente1.consultar_historial()
Persona.personas_registradas()
