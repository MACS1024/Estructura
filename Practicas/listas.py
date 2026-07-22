class Nodo:

    def __init__(self, dato):
        self.dato = dato # Dato que almacena el nodo
        self.siguiente = None #Apuntador que apunta al siguiente nodo de la lista


class ListaOrdenada:

    def __init__(self):
        self.inicio = None # Apuntador que apunta al primer nodo de la lista


    def insertar(self, dato):

        nuevo = Nodo(dato)# Creación de un nuevo nodo con el dato proporcionado

        # Si la lista está vacía, el nuevo nodo se convierte en el primer nodo
        if self.inicio is None:
            self.inicio = nuevo # El nuevo nodo se convierte en el primer nodo
            return
        
        # Si el dato del nuevo nodo es menor que el dato del primer nodo, se inserta al inicio de la lista
        if dato > self.inicio.dato:
            nuevo.siguiente = self.inicio
            self.inicio = nuevo
            return

        # Si el dato del nuevo nodo es mayor que el dato del primer nodo, se busca la posición correcta para insertarlo
        actual = self.inicio

        # Se recorre la lista hasta encontrar el nodo cuyo dato sea mayor que el dato del nuevo nodo
        while actual.siguiente and actual.siguiente.dato > dato:
            actual = actual.siguiente

        # Se inserta el nuevo nodo en la posición correcta
        nuevo.siguiente = actual.siguiente
        actual.siguiente = nuevo # El nuevo nodo se inserta en la posición correcta

    # Método para mostrar los elementos de la lista
    def mostrar(self):

        actual = self.inicio

        while actual:
            print(actual.dato,end=" -> ")
            actual = actual.siguiente

        print("None")


lista = ListaOrdenada()

for numero in [20,5,40,10,15]:
    lista.insertar(numero)

lista.mostrar()