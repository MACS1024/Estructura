"""
caja.py
-------
Representa una caja/ventanilla de atención.

Existen 5 cajas en el sistema:
    - Caja 1: exclusiva para clientes Diamante.
    - Cajas 2, 3, 4 y 5: atienden clientes Oro, Plata y No cliente.
"""


class Caja:
    def __init__(self, id_caja: int, tipo: str):
        """
        Args:
            id_caja: número identificador de la caja.
            tipo: "Diamante" (exclusiva) o "General" (Oro/Plata/No cliente).
        """
        self.id_caja = id_caja
        self.tipo = tipo
        self.estado = "Libre"          # Libre | Ocupada
        self.cliente_actual = None
        self.clientes_atendidos = []   # historial de tickets atendidos con éxito en esta caja

    def ocupar(self, ticket) -> None:
        self.estado = "Ocupada"
        self.cliente_actual = ticket

    def liberar(self) -> None:
        if self.cliente_actual is not None and self.cliente_actual.estado == "Atendido":
            self.clientes_atendidos.append(self.cliente_actual)
        self.cliente_actual = None
        self.estado = "Libre"

    def __str__(self):
        nombre = self.cliente_actual.nombre if self.cliente_actual else "-"
        return f"Caja {self.id_caja} [{self.tipo:<9}] · {self.estado:<8} · Atendiendo: {nombre}"
