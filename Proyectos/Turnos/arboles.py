# Clase Nodo
class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.izquierda = None
        self.derecha = None


# Clase Arbol
class Arbol:
    def __init__(self):
        self.raiz = None

    # Insertar un elemento en el árbol
    def insertar(self, dato):
        nuevo = Nodo(dato)

        if self.raiz is None:
            self.raiz = nuevo
        else:
            self._insertar(self.raiz, nuevo)

    def _insertar(self, actual, nuevo):
        if nuevo.dato < actual.dato:
            if actual.izquierda is None:
                actual.izquierda = nuevo
            else:
                self._insertar(actual.izquierda, nuevo)

        else:
            if actual.derecha is None:
                actual.derecha = nuevo
            else:
                self._insertar(actual.derecha, nuevo)

    # Recorrido Preorden
    def preorden(self, nodo):
        if nodo is not None:
            print(nodo.dato, end=" ")
            self.preorden(nodo.izquierda)
            self.preorden(nodo.derecha)

    # Recorrido Inorden
    def inorden(self, nodo):
        if nodo is not None:
            self.inorden(nodo.izquierda)
            print(nodo.dato, end=" ")
            self.inorden(nodo.derecha)

    # Recorrido Postorden
    def postorden(self, nodo):
        if nodo is not None:
            self.postorden(nodo.izquierda)
            self.postorden(nodo.derecha)
            print(nodo.dato, end=" ")


# Programa principal
arbol = Arbol()

print("=== RECORRIDO DE UN ÁRBOL BINARIO ===")

cantidad = int(input("¿Cuántos elementos deseas insertar? "))

for i in range(cantidad):
    dato = int(input(f"Ingresa el elemento {i + 1}: "))
    arbol.insertar(dato)

print("\n--- RECORRIDOS ---")

print("Preorden:")
arbol.preorden(arbol.raiz)

print("\n\nInorden:")
arbol.inorden(arbol.raiz)

print("\n\nPostorden:")
arbol.postorden(arbol.raiz)

print()