"""
Árbol Genealógico - Árbol Binario en Python
=============================================
Representa relaciones familiares mediante una estructura de árbol binario.

Parte 1: Clase NodoPersona
Parte 2: Clase ArbolGenealogico
Parte 3: Construcción de un árbol de ejemplo (12 personas, 3 niveles de profundidad)
Parte 4: Representación gráfica (ver generar_diagrama.py)
"""


# ---------------------------------------------------------------------------
# PARTE 1: CLASE NODO
# ---------------------------------------------------------------------------
class NodoPersona:
    """Representa a una persona dentro del árbol genealógico."""

    def __init__(self, nombre):
        self.nombre = nombre          # 1. Nombre de la persona
        self.izquierdo = None         # 2. Referencia al hijo izquierdo
        self.derecho = None           # 3. Referencia al hijo derecho

    def __repr__(self):
        return f"NodoPersona({self.nombre!r})"


# ---------------------------------------------------------------------------
# PARTE 2: CLASE ÁRBOL BINARIO
# ---------------------------------------------------------------------------
class ArbolGenealogico:
    """Árbol binario que organiza personas y sus descendientes."""

    def __init__(self):
        self.raiz = None

    # -- 1 y 2. Insertar personas / agregar nuevos miembros -----------------
    def insertar(self, nombre, nombre_padre=None, lado=None):
        """
        Inserta una nueva persona en el árbol.

        - Si el árbol está vacío, la persona se convierte en la raíz.
        - En caso contrario, se debe indicar el nombre del padre/madre
          (nombre_padre) y el lado ('izquierda' o 'derecha') que ocupará
          como descendiente, respetando la estructura binaria (máximo
          dos hijos por persona).
        """
        nuevo = NodoPersona(nombre)

        if self.raiz is None:
            self.raiz = nuevo
            return True

        if nombre_padre is None or lado not in ("izquierda", "derecha"):
            print(f"[Error] Debes indicar el padre/madre y el lado "
                  f"('izquierda'/'derecha') para insertar a '{nombre}'.")
            return False

        padre = self.buscar(nombre_padre)
        if padre is None:
            print(f"[Error] No se encontró a '{nombre_padre}' en el árbol.")
            return False

        if lado == "izquierda":
            if padre.izquierdo is not None:
                print(f"[Error] '{nombre_padre}' ya tiene hijo izquierdo.")
                return False
            padre.izquierdo = nuevo
        else:  # derecha
            if padre.derecho is not None:
                print(f"[Error] '{nombre_padre}' ya tiene hijo derecho.")
                return False
            padre.derecho = nuevo

        return True

    # -- 3 y 4. Buscar persona / localizar por nombre ------------------------
    def buscar(self, nombre, nodo="_raiz_"):
        """Busca una persona por nombre en todo el árbol (búsqueda recursiva)."""
        if nodo == "_raiz_":
            nodo = self.raiz

        if nodo is None:
            return None
        if nodo.nombre == nombre:
            return nodo

        encontrado = self.buscar(nombre, nodo.izquierdo)
        if encontrado is not None:
            return encontrado
        return self.buscar(nombre, nodo.derecho)

    # -- 5 y 6. Mostrar árbol / estructura jerárquica legible -----------------
    def mostrar_arbol(self, nodo="_raiz_", nivel=0, etiqueta="Raíz"):
        """Imprime el árbol de forma jerárquica e indentada."""
        if nodo == "_raiz_":
            nodo = self.raiz
            if nodo is None:
                print("(El árbol está vacío)")
                return

        print("    " * nivel + f"{etiqueta} → {nodo.nombre}")

        if nodo.izquierdo is not None:
            self.mostrar_arbol(nodo.izquierdo, nivel + 1, "Hijo Izq.")
        if nodo.derecho is not None:
            self.mostrar_arbol(nodo.derecho, nivel + 1, "Hijo Der.")

    # -- 7 y 8. Contar nodos / cuántas personas existen ------------------------
    def contar_nodos(self, nodo="_raiz_"):
        """Devuelve el número total de personas registradas en el árbol."""
        if nodo == "_raiz_":
            nodo = self.raiz
        if nodo is None:
            return 0
        return 1 + self.contar_nodos(nodo.izquierdo) + self.contar_nodos(nodo.derecho)

    # -- 9 y 10. Identificar hojas / nodos sin descendientes --------------------
    def identificar_hojas(self, nodo="_raiz_", hojas=None):
        """Devuelve una lista con los nombres de las personas sin descendientes."""
        if nodo == "_raiz_":
            nodo = self.raiz
            hojas = []
        if nodo is not None:
            if nodo.izquierdo is None and nodo.derecho is None:
                hojas.append(nodo.nombre)
            else:
                self.identificar_hojas(nodo.izquierdo, hojas)
                self.identificar_hojas(nodo.derecho, hojas)
        return hojas

    # -- Utilidad extra: profundidad del árbol --------------------------------
    def profundidad(self, nodo="_raiz_"):
        if nodo == "_raiz_":
            nodo = self.raiz
        if nodo is None:
            return -1  # árbol vacío = -1, raíz sola = 0
        return 1 + max(self.profundidad(nodo.izquierdo), self.profundidad(nodo.derecho))


# ---------------------------------------------------------------------------
# PARTE 3: CONSTRUCCIÓN DEL ÁRBOL (12 personas, 3 niveles de profundidad,
#           5 nodos hoja)
# ---------------------------------------------------------------------------
def construir_arbol_ejemplo():
    arbol = ArbolGenealogico()

    # Nivel 0 - Raíz (patriarca)
    arbol.insertar("Roberto García")

    # Nivel 1 - Hijos de Roberto
    arbol.insertar("María López", "Roberto García", "izquierda")
    arbol.insertar("Carlos García", "Roberto García", "derecha")

    # Nivel 2 - Nietos
    arbol.insertar("Ana López", "María López", "izquierda")
    arbol.insertar("Pedro López", "María López", "derecha")
    arbol.insertar("Sofía García", "Carlos García", "izquierda")
    arbol.insertar("Luis García", "Carlos García", "derecha")

    # Nivel 3 - Bisnietos (hojas)
    arbol.insertar("Diego Ramírez", "Ana López", "izquierda")
    arbol.insertar("Elena Ramírez", "Ana López", "derecha")
    arbol.insertar("Fernando López", "Pedro López", "izquierda")
    arbol.insertar("Camila García", "Sofía García", "derecha")
    arbol.insertar("Jorge García", "Luis García", "izquierda")

    #nivel 4 - Bisnietos (hojas)
    arbol.insertar("Juan Pérez", "Camila García", "izquierda")
    arbol.insertar("Lucía Pérez", "Camila García", "derecha")

    return arbol


# ---------------------------------------------------------------------------
# PROGRAMA PRINCIPAL / DEMOSTRACIÓN
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    arbol = construir_arbol_ejemplo()

    print("=" * 60)
    print("ESTRUCTURA JERÁRQUICA DEL ÁRBOL GENEALÓGICO")
    print("=" * 60)
    arbol.mostrar_arbol()

    print("\n" + "=" * 60)
    print("BÚSQUEDA DE PERSONAS")
    print("=" * 60)
    for nombre in ["Sofía García", "Diego Ramírez", "Juan Pérez"]:
        resultado = arbol.buscar(nombre)
        estado = "Encontrado" if resultado else "No encontrado"
        print(f"Buscar '{nombre}': {estado}")

    print("\n" + "=" * 60)
    print("CONTEO DE NODOS")
    print("=" * 60)
    print(f"Total de personas en el árbol: {arbol.contar_nodos()}")
    print(f"Profundidad del árbol (niveles por debajo de la raíz): {arbol.profundidad()}")

    print("\n" + "=" * 60)
    print("NODOS HOJA (personas sin descendientes)")
    print("=" * 60)
    hojas = arbol.identificar_hojas()
    print(f"Total de hojas: {len(hojas)}")
    for h in hojas:
        print(f" - {h}")
