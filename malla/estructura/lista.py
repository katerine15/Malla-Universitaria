class Nodo:
    def __init__(self, dato):
        self.dato = dato  #Valor almacenado
        self.anterior = None
        self.siguiente = None # Referencia al siguiente nodo

    
class listaDobleEnlace:
    def __init__(self):
        self.inicio = None
        self.final = None
        self.size = 0

    def insertar_inicio(self, dato):
        nuevo_nodo = Nodo(dato)
        if self.inicio is None:
            self.inicio = nuevo_nodo
            self.final = nuevo_nodo
        else:
            nuevo_nodo.siguiente = self.inicio
            self.inicio.anterior = nuevo_nodo
            self.inicio = nuevo_nodo
        self.size += 1

    def insertar_final(self, dato):
        nuevo_nodo = Nodo(dato)
        if self.inicio is None:
            self.final = nuevo_nodo
            self.inicio = nuevo_nodo

        else:
            nuevo_nodo.anterior = self.final
            self.final.siguiente = nuevo_nodo
            self.final = nuevo_nodo
        self.size += 1
    
    def recorrerAdelante(self):
        # recorre desde el inicio a final
        elementos = []
        actual = self.inicio
        while actual:
            elementos.append(str(actual.dato))
            actual = actual.siguiente
        return " <-> ".join(elementos)
    
    def recorrerAtras(self):
        # recorre desde el final al inicio
        elementos = []
        actual = self.final
        while actual:
            elementos.append(str(actual.dato))
            actual = actual.anterior
        return " <-> ".join(elementos)
