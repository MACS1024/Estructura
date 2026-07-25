class nodoCancion:
    def __init__(self, nomCancion, artista):
        self.nomCancion = nomCancion
        self.artista = artista
        self.siguiente = None
        self.anterior = None

class listaReproduccion: 
    def __init__(self):
        self.inicio = None

    def insertar_final(self, nomCancion, artista):

        nuevoNodo = nodoCancion(nomCancion, artista)

        if self.inicio is None:
            self.inicio = nuevoNodo
            nuevoNodo.siguiente = nuevoNodo
            nuevoNodo.anterior = nuevoNodo
            return

        nodoactual = self.inicio

        while nodoactual.siguiente != self.inicio:
            nodoactual = nodoactual.siguiente

        nodoactual.siguiente = nuevoNodo
        nuevoNodo.anterior = nodoactual
        nuevoNodo.siguiente = self.inicio
        self.inicio.anterior = nuevoNodo

    def eliminar_cancion(self, nomCancion):
        if self.inicio is None:
            return

        nodoactual = self.inicio
        while True:
            if nodoactual.nomCancion == nomCancion:
                if nodoactual.siguiente == nodoactual:  # Solo hay un nodo
                    self.inicio = None
                else:
                    nodoactual.anterior.siguiente = nodoactual.siguiente
                    nodoactual.siguiente.anterior = nodoactual.anterior
                    if nodoactual == self.inicio:
                        self.inicio = nodoactual.siguiente
                return
            nodoactual = nodoactual.siguiente
            if nodoactual == self.inicio:
                break  # Hemos recorrido toda la lista sin encontrar la canción

    def mostrar_lista(self):
        if self.inicio is None:
            print("La lista de reproducción está vacía.")
            return

        nodoactual = self.inicio
        while True:
            print(f"Canción: {nodoactual.nomCancion}, Artista: {nodoactual.artista}")
            nodoactual = nodoactual.siguiente
            if nodoactual == self.inicio:
                break  # Hemos recorrido toda la lista
    