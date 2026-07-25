def torres_hanoi(n, origen, destino, auxiliar):
    # Caso base: Si solo queda un disco, se mueve directamente
    if n == 1:
        print(f"Mover disco 1 de torre {origen} a torre {destino}")
        return

    # Paso 1: Mover n-1 discos del origen al auxiliar usando el destino
    torres_hanoi(n - 1, origen, auxiliar, destino)

    # Paso 2: Mover el disco restante (el más grande) del origen al destino
    print(f"Mover disco {n} de torre {origen} a torre {destino}")

    # Paso 3: Mover los n-1 discos del auxiliar al destino usando el origen
    torres_hanoi(n - 1, auxiliar, destino, origen)


# --- Bloque de ejecución ---
if __name__ == "__main__":
    # Definimos el número de discos
    numero_discos = 5

    print(f"Resolviendo Torres de Hanoi para {numero_discos} discos:\n")
    # Llamada a la función pasándole las etiquetas de las torres (A, C, B)
    torres_hanoi(numero_discos, origen="A", destino="C", auxiliar="B")