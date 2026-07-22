class Nodo:

    def __init__(self,dato):
        self.dato=dato
        self.siguiente=None


class ListaCircular:

    def __init__(self):
        self.inicio=None


    def insertar(self,dato):

        nuevo=Nodo(dato)

        if self.inicio is None:

            self.inicio=nuevo
            nuevo.siguiente=nuevo
            return

        actual=self.inicio

        while actual.siguiente!=self.inicio:
            actual=actual.siguiente

        actual.siguiente=nuevo
        nuevo.siguiente=self.inicio


    def mostrar(self):

        if self.inicio is None:
            return

        actual=self.inicio

        while True:

            print(actual.dato,end=" -> ")

            actual=actual.siguiente

            if actual==self.inicio:
                break

        print("(regresa al inicio)")


lista=ListaCircular()

for x in [10,20,30,40]:
    lista.insertar(x)

lista.mostrar()