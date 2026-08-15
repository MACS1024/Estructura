"""
modelo.py
---------
Modelo de datos del sistema de turnos con prioridad:
    - TipoCliente: categorías de cliente (Diamante, Oro, Plata, No cliente).
    - Tiempos de espera máximos permitidos por categoría (SLA).
    - Ticket: representa el turno de un cliente, con fecha/hora de creación
      y todos los tiempos relevantes de su ciclo de vida (creado -> llamado
      -> atendido / no se presentó).
"""

import random
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class TipoCliente(Enum):
    DIAMANTE = "Diamante"
    ORO = "Oro"
    PLATA = "Plata"
    NO_CLIENTE = "No cliente"


# Tiempo máximo de espera permitido por categoría, en segundos.
# Diamante y Oro tienen un tope fijo; Plata y No cliente son un rango
# del cual se sortea un valor concreto al emitir el ticket.
RANGOS_TIEMPO_ESPERA = {
    TipoCliente.DIAMANTE:   (2, 2),     # no más de 2 segundos
    TipoCliente.ORO:        (5, 5),     # no más de 5 segundos
    TipoCliente.PLATA:      (10, 15),   # entre 10 y 15 segundos
    TipoCliente.NO_CLIENTE: (30, 60),   # entre 30 y 60 segundos
}

# Prioridad numérica para la cola (menor número = mayor prioridad).
PRIORIDAD = {
    TipoCliente.DIAMANTE: 1,
    TipoCliente.ORO: 2,
    TipoCliente.PLATA: 3,
    TipoCliente.NO_CLIENTE: 4,
}


def calcular_tiempo_max_espera(tipo: TipoCliente) -> float:
    """Calcula el tiempo máximo de espera (SLA) para un ticket según su categoría."""
    minimo, maximo = RANGOS_TIEMPO_ESPERA[tipo]
    if minimo == maximo:
        return float(minimo)
    return round(random.uniform(minimo, maximo), 2)


@dataclass
class Ticket:
    """Representa el turno de un cliente desde su creación hasta su cierre."""
    numero_turno: int
    nombre: str
    tipo_cliente: TipoCliente
    tiempo_max_espera: float                 # SLA en segundos, según categoría

    # Momento de creación del ticket
    fecha_creacion: str = field(default_factory=lambda: datetime.now().strftime("%d/%m/%Y"))
    hora_creacion: str = field(default_factory=lambda: datetime.now().strftime("%H:%M:%S"))
    timestamp_creacion: float = field(default_factory=time.time)

    # Se completan durante el ciclo de vida del ticket
    caja_asignada: int = None
    hora_llamado: str = None
    timestamp_llamado: float = None
    presente: bool = None                    # True si el cliente respondió al llamado
    hora_inicio_atencion: str = None
    timestamp_inicio_atencion: float = None
    hora_fin_atencion: str = None
    timestamp_fin_atencion: float = None
    estado: str = "En espera"                # En espera | Llamado | Atendido | No se presentó

    # ------------------------------------------------------------------
    def tiempo_espera_real(self):
        """Segundos transcurridos entre la creación del ticket y su llamado."""
        if self.timestamp_llamado is None:
            return None
        return round(self.timestamp_llamado - self.timestamp_creacion, 2)

    def tiempo_atencion(self):
        """Duración real de la atención en caja, en segundos."""
        if self.timestamp_inicio_atencion and self.timestamp_fin_atencion:
            return round(self.timestamp_fin_atencion - self.timestamp_inicio_atencion, 2)
        return None

    def tiempo_total_en_sistema(self):
        """Desde que se emitió el ticket hasta que terminó su atención (o se marcó ausente)."""
        fin = self.timestamp_fin_atencion or self.timestamp_llamado
        if fin is None:
            return None
        return round(fin - self.timestamp_creacion, 2)

    def cumplio_sla(self):
        """Indica si el cliente fue llamado dentro de su tiempo máximo de espera."""
        espera = self.tiempo_espera_real()
        if espera is None:
            return None
        return espera <= self.tiempo_max_espera

    def imprimir_ticket(self):
        """Representación tipo 'ticket físico' con fecha y hora de creación."""
        linea = "-" * 38
        print(linea)
        print(f"{'BANCO MERIDIANO':^38}")
        print(linea)
        print(f" Turno:        #{self.numero_turno:03d}")
        print(f" Cliente:      {self.nombre}")
        print(f" Categoría:    {self.tipo_cliente.value}")
        print(f" Fecha:        {self.fecha_creacion}")
        print(f" Hora:         {self.hora_creacion}")
        print(f" Espera máx.:  {self.tiempo_max_espera} seg")
        print(linea)

    def __str__(self):
        return (f"#{self.numero_turno:03d} | {self.nombre:<20} | {self.tipo_cliente.value:<10} | "
                f"{self.estado:<15} | Creado: {self.fecha_creacion} {self.hora_creacion}")
