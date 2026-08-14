class Nodo:
    """Clase auxiliar para representar cada elemento (acción) en la pila."""
    def __init__(self, accion):
        self.accion = accion
        self.siguiente = None


class Pila:
    """Estructura de datos tipo Pila (LIFO) para el historial del editor."""
    def __init__(self):
        self.cima = None
        self._tamano = 0

    def push(self, accion):
        """Agrega una nueva acción a la cima de la pila."""
        nuevo_nodo = Nodo(accion)
        nuevo_nodo.siguiente = self.cima
        self.cima = nuevo_nodo
        self._tamano += 1
        print(f"-> Acción registrada: \"{accion}\"")

    def pop(self):
        """Elimina y retorna la última acción registrada (deshacer)."""
        if self.is_empty():
            print("⚠️ No hay acciones para deshacer.")
            return None
        
        accion_deshecha = self.cima.accion
        self.cima = self.cima.siguiente
        self._tamano -= 1
        return accion_deshecha

    def peek(self):
        """Muestra la última acción almacenada sin eliminarla."""
        if self.is_empty():
            print("⚠️ La pila está vacía.")
            return None
        return self.cima.accion

    def is_empty(self):
        """Indica si la pila está vacía."""
        return self.cima is None

    def size(self):
        """Devuelve la cantidad de elementos almacenados."""
        return self._tamano

    def mostrar_historial(self):
        """Muestra todas las acciones almacenadas (de la más reciente a la más antigua)."""
        if self.is_empty():
            print("\n📋 El historial está vacío.")
            return

        print("\n=== HISTORIAL DE ACCIONES (Más reciente primero) ===")
        actual = self.cima
        posicion = self._tamano
        while actual:
            print(f"[{posicion}] {actual.accion}")
            actual = actual.siguiente
            posicion -= 1
        print("===================================================\n")

def menu_editor():
    historial = Pila()

    while True:
        print("\n--- SIMULADOR DE EDITOR DE TEXTO ---")
        print("1. Agregar acción")
        print("2. Deshacer última acción (Pop)")
        print("3. Mostrar acción más reciente (Peek)")
        print("4. Mostrar historial completo")
        print("5. Mostrar cantidad de acciones (Size)")
        print("6. Salir")
        
        opcion = input("Seleccione una opción (1-6): ").strip()

        if opcion == '1':
            accion = input("Escriba la acción a realizar (ej. 'Escribir Hola'): ").strip()
            if accion:
                historial.push(accion)
            else:
                print("⚠️ La acción no puede estar vacía.")

        elif opcion == '2':
            deshecho = historial.pop()
            if deshecho:
                print(f"↺ Se deshizo la acción: \"{deshecho}\"")

        elif opcion == '3':
            reciente = historial.peek()
            if reciente:
                print(f"👁️ Acción más reciente: \"{reciente}\"")

        elif opcion == '4':
            historial.mostrar_historial()

        elif opcion == '5':
            print(f"📊 Cantidad de acciones almacenadas: {historial.size()}")

        elif opcion == '6':
            print("Saliendo del programa...")
            break
        else:
            print("⚠️ Opción no válida. Intente de nuevo.")

# Para ejecutar el menú en modo interactivo:
# menu_editor()

def ejecutar_pruebas():
    editor = Pila()

    print("\n--- PASO 1: Registrar 10 acciones distintas ---")
    acciones = [
        "Escribir 'Título principal'",
        "Agregar salto de línea",
        "Escribir 'Párrafo 1: Introducción'",
        "Aplicar negrita a 'Introducción'",
        "Eliminar palabra 'principal'",
        "Escribir 'Sección 2'",
        "Insertar imagen 'diagrama.png'",
        "Cambiar tamaño de fuente a 12pt",
        "Escribir 'Conclusión'",
        "Guardar borrador"
    ]

    for acc in acciones:
        editor.push(acc)

    print("\n--- PASO 2: Historial inicial (10 acciones) ---")
    editor.mostrar_historial()

    print("--- PASO 3: Deshacer 3 acciones ---")
    for _ in range(3):
        eliminado = editor.pop()
        print(f"↺ Acción deshecha: \"{eliminado}\"")

    print("\n--- PASO 4: Consultar la acción más reciente (Peek) ---")
    print(f"👁️ Acción más reciente en la cima: \"{editor.peek()}\"")

    print("\n--- PASO 5: Consultar tamaño actual (Size) ---")
    print(f"📊 Total de acciones guardadas: {editor.size()}")

    print("\n--- PASO 6: Historial después de deshacer ---")
    editor.mostrar_historial()

if __name__ == "__main__":
    ejecutar_pruebas()