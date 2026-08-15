"""
ejecutivo.py
------------
Lógica del "ejecutivo" que opera cada caja. Su ciclo de trabajo es:

    1. Toma el siguiente ticket de la cola que le corresponde a su caja.
    2. Llama al cliente (registra hora de llamado).
    3. Verifica si el cliente se encuentra presente, respetando como
       margen el tiempo máximo de espera de su categoría
       (Diamante 2s / Oro 5s / Plata 10-15s / No cliente 30-60s).
    4. Si el cliente se presenta a tiempo -> lo atiende y registra
       inicio/fin de atención.
       Si NO se presenta dentro de su tiempo máximo -> lo marca como
       "No se presentó" y avanza automáticamente al siguiente turno.
"""

import random
import time
from datetime import datetime


TIEMPO_ATENCION_RANGO = (3, 8)   # segundos que tarda la atención una vez el cliente está en caja
PROBABILIDAD_PRESENCIA = 0.85    # probabilidad de que el cliente sí esté presente al ser llamado


def _hora_actual():
    ahora = datetime.now()
    return ahora.strftime("%d/%m/%Y"), ahora.strftime("%H:%M:%S")


def _simular_presencia_cliente() -> bool:
    """Simula si el cliente está o no en sala al momento de ser llamado."""
    return random.random() < PROBABILIDAD_PRESENCIA


def ejecutivo_atiende(caja, cola, estadisticas, lock, verbose=True,
                       stop_event=None, modo_continuo=False):
    """
    Bucle de trabajo de un ejecutivo asignado a una caja.

    Args:
        caja: instancia de Caja que este ejecutivo opera.
        cola: ColaPrioridad de la que este ejecutivo extrae turnos
              (cola exclusiva Diamante o cola general Oro/Plata/No cliente).
        estadisticas: instancia de Estadisticas compartida por todo el sistema.
        lock: threading.Lock que protege el acceso concurrente a la cola.
        verbose: si True, imprime en consola cada acción del ejecutivo.
        stop_event: threading.Event opcional para detener el ciclo (modo continuo).
        modo_continuo: si True, el ejecutivo sigue esperando nuevos turnos aunque
                       la cola esté momentáneamente vacía (usado en el menú interactivo).
                       Si False, el ejecutivo termina cuando la cola queda vacía
                       (usado en la simulación por lotes).
    """
    while True:
        if stop_event is not None and stop_event.is_set():
            break

        with lock:
            ticket = cola.pop()

        if ticket is None:
            if modo_continuo:
                time.sleep(0.3)
                continue
            break  # no quedan turnos para esta caja: el ejecutivo termina su turno

        # --- 1) Llamar al cliente ---
        caja.ocupar(ticket)
        ticket.caja_asignada = caja.id_caja
        _, hora_llamado = _hora_actual()
        ticket.hora_llamado = hora_llamado
        ticket.timestamp_llamado = time.time()
        ticket.estado = "Llamado"

        if verbose:
            print(f"[Ejecutivo caja {caja.id_caja}] Llamando turno #{ticket.numero_turno:03d} "
                  f"· {ticket.nombre} ({ticket.tipo_cliente.value}) "
                  f"· margen de espera: {ticket.tiempo_max_espera}s")

        # --- 2) Verificar si el cliente se encuentra presente ---
        presente = _simular_presencia_cliente()

        if presente:
            # El cliente responde en algún punto dentro de su tiempo máximo permitido.
            tiempo_respuesta = round(random.uniform(0, ticket.tiempo_max_espera), 2)
            time.sleep(tiempo_respuesta)
        else:
            # El ejecutivo espera el tiempo máximo permitido antes de dar por
            # ausente al cliente y avanzar al siguiente turno.
            time.sleep(ticket.tiempo_max_espera)

        if not presente:
            ticket.estado = "No se presentó"
            ticket.presente = False
            with lock:
                estadisticas.registrar_no_presentado(ticket)
            if verbose:
                print(f"[Ejecutivo caja {caja.id_caja}] Turno #{ticket.numero_turno:03d} "
                      f"NO se presentó dentro de {ticket.tiempo_max_espera}s. "
                      f"Se avanza al siguiente turno.")
            caja.liberar()
            continue

        # --- 3) Atender al cliente ---
        ticket.presente = True
        _, hora_inicio = _hora_actual()
        ticket.hora_inicio_atencion = hora_inicio
        ticket.timestamp_inicio_atencion = time.time()
        ticket.estado = "Atendido"

        tiempo_atencion = round(random.uniform(*TIEMPO_ATENCION_RANGO), 2)
        time.sleep(tiempo_atencion)

        _, hora_fin = _hora_actual()
        ticket.hora_fin_atencion = hora_fin
        ticket.timestamp_fin_atencion = time.time()

        with lock:
            estadisticas.registrar_atendido(ticket)

        if verbose:
            print(f"[Ejecutivo caja {caja.id_caja}] Turno #{ticket.numero_turno:03d} atendido. "
                  f"Espera real: {ticket.tiempo_espera_real()}s "
                  f"(máx. {ticket.tiempo_max_espera}s) · "
                  f"Duración atención: {ticket.tiempo_atencion()}s")

        caja.liberar()
