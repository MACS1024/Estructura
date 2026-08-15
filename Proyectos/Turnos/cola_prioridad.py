"""
cola_prioridad.py
------------------
Cola de prioridad para tickets. Ordena primero por categoría del cliente
(Diamante > Oro > Plata > No cliente) y, dentro de la misma categoría,
respeta el orden de llegada (FIFO), gracias a un contador de desempate.

Implementada con heapq para que push/pop sean O(log n).
"""

import heapq
import itertools

from modelo import PRIORIDAD


class ColaPrioridad:
    def __init__(self):
        self._heap = []
        self._contador = itertools.count()   # desempate estable (FIFO dentro de la misma categoría)

    def push(self, ticket) -> None:
        """Agrega un ticket a la cola respetando su prioridad de categoría."""
        prioridad = PRIORIDAD[ticket.tipo_cliente]
        heapq.heappush(self._heap, (prioridad, next(self._contador), ticket))

    def pop(self):
        """Retira y retorna el ticket con mayor prioridad (o None si está vacía)."""
        if not self._heap:
            return None
        return heapq.heappop(self._heap)[2]

    def peek(self):
        """Consulta el siguiente ticket a atender sin retirarlo."""
        return self._heap[0][2] if self._heap else None

    def is_empty(self) -> bool:
        return len(self._heap) == 0

    def size(self) -> int:
        return len(self._heap)

    def listar(self):
        """Retorna los tickets pendientes ordenados por prioridad."""
        return [t for _, _, t in sorted(self._heap)]
