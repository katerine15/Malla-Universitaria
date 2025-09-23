from .lista import Nodo, listaDobleEnlace
from django.db.models import QuerySet

class NodoDjango(Nodo):
    """
    Nodo especializado para trabajar con modelos de Django
    """
    def __init__(self, modelo_django):
        super().__init__(modelo_django)
        self.modelo = modelo_django  # Referencia directa al modelo Django
    
    def __str__(self):
        return str(self.modelo)

class ListaDjangoDobleEnlace(listaDobleEnlace):
    """
    Lista doblemente enlazada especializada para trabajar con modelos de Django
    """
    
    def __init__(self):
        super().__init__()
    
    def from_queryset(self, queryset):
        """
        Convierte un QuerySet de Django a lista doblemente enlazada
        """
        for modelo in queryset:
            self.insertar_final(modelo)
        return self
    
    def from_list(self, lista_modelos):
        """
        Convierte una lista de modelos Django a lista doblemente enlazada
        """
        for modelo in lista_modelos:
            self.insertar_final(modelo)
        return self
    
    def insertar_inicio(self, modelo_django):
        """
        Inserta un modelo Django al inicio de la lista
        """
        nuevo_nodo = NodoDjango(modelo_django)
        if self.inicio is None:
            self.inicio = nuevo_nodo
            self.final = nuevo_nodo
        else:
            nuevo_nodo.siguiente = self.inicio
            self.inicio.anterior = nuevo_nodo
            self.inicio = nuevo_nodo
        self.size += 1
    
    def insertar_final(self, modelo_django):
        """
        Inserta un modelo Django al final de la lista
        """
        nuevo_nodo = NodoDjango(modelo_django)
        if self.inicio is None:
            self.final = nuevo_nodo
            self.inicio = nuevo_nodo
        else:
            nuevo_nodo.anterior = self.final
            self.final.siguiente = nuevo_nodo
            self.final = nuevo_nodo
        self.size += 1
    
    def buscar(self, **kwargs):
        """
        Busca modelos en la lista basado en atributos
        Ejemplo: lista.buscar(id=1) o lista.buscar(name="Matemáticas")
        """
        resultados = ListaDjangoDobleEnlace()
        actual = self.inicio
        while actual:
            modelo = actual.modelo
            coincide = True
            for attr, valor in kwargs.items():
                if not hasattr(modelo, attr) or getattr(modelo, attr) != valor:
                    coincide = False
                    break
            if coincide:
                resultados.insertar_final(modelo)
            actual = actual.siguiente
        return resultados
    
    def filtrar(self, funcion_filtro):
        """
        Filtra modelos usando una función personalizada
        Ejemplo: lista.filtrar(lambda x: x.completed == True)
        """
        resultados = ListaDjangoDobleEnlace()
        actual = self.inicio
        while actual:
            if funcion_filtro(actual.modelo):
                resultados.insertar_final(actual.modelo)
            actual = actual.siguiente
        return resultados
    
    def ordenar_por(self, campo, reverso=False):
        """
        Ordena la lista por un campo específico del modelo
        """
        # Convertir a lista Python, ordenar, y reconstruir
        modelos = self.to_list()
        modelos.sort(key=lambda x: getattr(x, campo), reverse=reverso)
        
        # Limpiar lista actual
        self.inicio = None
        self.final = None
        self.size = 0
        
        # Reconstruir con orden correcto
        for modelo in modelos:
            self.insertar_final(modelo)
        
        return self
    
    def to_list(self):
        """
        Convierte la lista doblemente enlazada a una lista Python estándar
        """
        modelos = []
        actual = self.inicio
        while actual:
            modelos.append(actual.modelo)
            actual = actual.siguiente
        return modelos
    
    def to_queryset(self, model_class):
        """
        Convierte la lista a un QuerySet (usando los IDs de los modelos)
        """
        ids = [modelo.id for modelo in self.to_list()]
        return model_class.objects.filter(id__in=ids)
    
    def __iter__(self):
        """
        Permite iterar sobre la lista como si fuera una lista normal
        """
        actual = self.inicio
        while actual:
            yield actual.modelo
            actual = actual.siguiente
    
    def __len__(self):
        """
        Devuelve el tamaño de la lista
        """
        return self.size
    
    def __getitem__(self, index):
        """
        Permite acceso por índice como lista[0]
        """
        if index < 0 or index >= self.size:
            raise IndexError("Índice fuera de rango")
        
        actual = self.inicio
        for i in range(index):
            actual = actual.siguiente
        return actual.modelo
    
    def primero(self):
        """
        Devuelve el primer modelo de la lista
        """
        return self.inicio.modelo if self.inicio else None
    
    def ultimo(self):
        """
        Devuelve el último modelo de la lista
        """
        return self.final.modelo if self.final else None
    
    def esta_vacia(self):
        """
        Verifica si la lista está vacía
        """
        return self.size == 0
    
    def eliminar_por_id(self, modelo_id):
        """
        Elimina un modelo de la lista por su ID
        """
        actual = self.inicio
        while actual:
            if actual.modelo.id == modelo_id:
                # Eliminar nodo actual
                if actual.anterior:
                    actual.anterior.siguiente = actual.siguiente
                else:
                    self.inicio = actual.siguiente
                
                if actual.siguiente:
                    actual.siguiente.anterior = actual.anterior
                else:
                    self.final = actual.anterior
                
                self.size -= 1
                return True
            actual = actual.siguiente
        return False
    
    def recorrerAdelante(self):
        """
        Recorre la lista de adelante hacia atrás y devuelve string representativo
        """
        elementos = []
        actual = self.inicio
        while actual:
            elementos.append(str(actual.modelo))
            actual = actual.siguiente
        return " <-> ".join(elementos)
    
    def recorrerAtras(self):
        """
        Recorre la lista de atrás hacia adelante y devuelve string representativo
        """
        elementos = []
        actual = self.final
        while actual:
            elementos.append(str(actual.modelo))
            actual = actual.anterior
        return " <-> ".join(elementos)
