"""
PARTE 4: Representación gráfica del árbol genealógico
=======================================================
Dibuja el árbol usando matplotlib, distinguiendo:
- Nodo raíz (color distinto)
- Nodos intermedios (con hijos)
- Nodos hoja (sin descendientes)
- Líneas que muestran la relación padre-hijo
"""

import matplotlib.pyplot as plt
from arbol_genealogico import construir_arbol_ejemplo


def calcular_posiciones(nodo, profundidad=0, contador=[0], posiciones=None):
    """
    Recorrido in-order: asigna coordenadas x (según orden de visita)
    y coordenadas y (según el nivel/profundidad) para que el árbol
    se dibuje sin que los nodos se encimen.
    """
    if posiciones is None:
        posiciones = {}
    if nodo is None:
        return posiciones

    calcular_posiciones(nodo.izquierdo, profundidad + 1, contador, posiciones)

    x = contador[0]
    y = -profundidad
    posiciones[nodo.nombre] = (x, y)
    contador[0] += 1

    calcular_posiciones(nodo.derecho, profundidad + 1, contador, posiciones)

    return posiciones


def dibujar_arbol(arbol, archivo_salida="arbol_genealogico.png"):
    posiciones = calcular_posiciones(arbol.raiz)
    hojas = set(arbol.identificar_hojas())
    raiz_nombre = arbol.raiz.nombre

    fig, ax = plt.subplots(figsize=(14, 8))

    # --- Dibujar las conexiones (relación padre-hijo) primero ---
    def dibujar_conexiones(nodo):
        if nodo is None:
            return
        x0, y0 = posiciones[nodo.nombre]
        if nodo.izquierdo is not None:
            x1, y1 = posiciones[nodo.izquierdo.nombre]
            ax.plot([x0, x1], [y0, y1], color="#8a8a8a", linewidth=1.8, zorder=1)
            dibujar_conexiones(nodo.izquierdo)
        if nodo.derecho is not None:
            x1, y1 = posiciones[nodo.derecho.nombre]
            ax.plot([x0, x1], [y0, y1], color="#8a8a8a", linewidth=1.8, zorder=1)
            dibujar_conexiones(nodo.derecho)

    dibujar_conexiones(arbol.raiz)

    # --- Dibujar los nodos ---
    for nombre, (x, y) in posiciones.items():
        if nombre == raiz_nombre:
            color = "#e07a3f"   # raíz
            tam = 2600
        elif nombre in hojas:
            color = "#4f9d69"   # hoja
            tam = 2000
        else:
            color = "#4a7ba6"   # intermedio
            tam = 2200

        ax.scatter(x, y, s=tam, color=color, edgecolors="white",
                   linewidths=1.5, zorder=2)
        ax.text(x, y - 0.28, nombre, ha="center", va="top",
                fontsize=9, fontweight="bold", color="#222222")

    # --- Leyenda ---
    from matplotlib.lines import Line2D
    leyenda = [
        Line2D([0], [0], marker='o', color='w', label='Nodo raíz',
               markerfacecolor='#e07a3f', markersize=14),
        Line2D([0], [0], marker='o', color='w', label='Nodo intermedio',
               markerfacecolor='#4a7ba6', markersize=14),
        Line2D([0], [0], marker='o', color='w', label='Nodo hoja',
               markerfacecolor='#4f9d69', markersize=14),
    ]
    ax.legend(handles=leyenda, loc="upper center", ncol=3,
              bbox_to_anchor=(0.5, 1.08), frameon=False, fontsize=11)

    ax.set_title("Árbol Genealógico Binario", fontsize=15, fontweight="bold", pad=40)
    ax.axis("off")
    plt.tight_layout()
    plt.savefig(archivo_salida, dpi=180, bbox_inches="tight")
    print(f"Diagrama guardado en: {archivo_salida}")


if __name__ == "__main__":
    arbol = construir_arbol_ejemplo()
    dibujar_arbol(arbol, "arbol_genealogico.png")
