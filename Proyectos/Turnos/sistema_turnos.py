"""
sistema_turnos.py
-------------------
Orquesta el sistema completo:
    - 1 cola exclusiva para clientes Diamante -> Caja 1 (exclusiva).
    - 1 cola general para Oro / Plata / No cliente -> Cajas 2, 3, 4 y 5.
    - Cada caja es operada por un ejecutivo (hilo) que llama, verifica
      presencia y atiende o avanza según corresponda.
    - Estadísticas centralizadas y compartidas entre todos los ejecutivos.
"""

import threading
import time

from caja import Caja
from cola_prioridad import ColaPrioridad
from ejecutivo import ejecutivo_atiende
from estadisticas import Estadisticas
from modelo import Ticket, TipoCliente, calcular_tiempo_max_espera


class SistemaTurnos:
    def __init__(self):
        self.cola_diamante = ColaPrioridad()          # exclusiva Caja 1
        self.cola_general = ColaPrioridad()            # Oro / Plata / No cliente -> Cajas 2-5
        self.lock_diamante = threading.Lock()
        self.lock_general = threading.Lock()

        self.estadisticas = Estadisticas()

        self.cajas = [
            Caja(1, "Diamante"),
            Caja(2, "General"),
            Caja(3, "General"),
            Caja(4, "General"),
            Caja(5, "General"),
        ]

        self._contador_turno = 1
        self._lock_contador = threading.Lock()
        self._hilos = []
        self.stop_event = threading.Event()

    # ------------------------------------------------------------------
    def _siguiente_numero_turno(self) -> int:
        with self._lock_contador:
            n = self._contador_turno
            self._contador_turno += 1
            return n

    def registrar_cliente(self, nombre: str, tipo_cliente: TipoCliente) -> Ticket:
        """
        Registra un nuevo cliente: crea su ticket (con fecha y hora de creación)
        y lo coloca en la cola correspondiente a su categoría.
        """
        ticket = Ticket(
            numero_turno=self._siguiente_numero_turno(),
            nombre=nombre,
            tipo_cliente=tipo_cliente,
            tiempo_max_espera=calcular_tiempo_max_espera(tipo_cliente),
        )
        self.estadisticas.registrar_ingreso(tipo_cliente)

        if tipo_cliente == TipoCliente.DIAMANTE:
            with self.lock_diamante:
                self.cola_diamante.push(ticket)
        else:
            with self.lock_general:
                self.cola_general.push(ticket)

        return ticket

    # ------------------------------------------------------------------
    def iniciar_cajas(self, verbose=True, modo_continuo=False) -> None:
        """Lanza un hilo (ejecutivo) por cada una de las 5 cajas."""
        for caja in self.cajas:
            if caja.tipo == "Diamante":
                cola, lock = self.cola_diamante, self.lock_diamante
            else:
                cola, lock = self.cola_general, self.lock_general

            hilo = threading.Thread(
                target=ejecutivo_atiende,
                args=(caja, cola, self.estadisticas, lock, verbose, self.stop_event, modo_continuo),
                daemon=True,
                name=f"Ejecutivo-Caja{caja.id_caja}",
            )
            hilo.start()
            self._hilos.append(hilo)

    def esperar_finalizacion(self) -> None:
        """Bloquea hasta que todos los ejecutivos terminen (modo por lotes)."""
        for hilo in self._hilos:
            hilo.join()

    def detener(self) -> None:
        """Señaliza a todos los ejecutivos que deben detenerse (modo continuo)."""
        self.stop_event.set()
        for hilo in self._hilos:
            hilo.join(timeout=2)

    # ------------------------------------------------------------------
    def estado_cajas(self) -> str:
        return "\n".join(str(c) for c in self.cajas)

    def estado_colas(self) -> str:
        with self.lock_diamante:
            diamante = self.cola_diamante.size()
        with self.lock_general:
            general = self.cola_general.size()
        return f"En espera Diamante: {diamante}  |  En espera Oro/Plata/No cliente: {general}"
