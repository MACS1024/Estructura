"""
simulacion.py
--------------
Simulación completa del sistema de turnos con prioridad:
    - Registra clientes de las 4 categorías (Diamante, Oro, Plata, No cliente).
    - Cada uno recibe su ticket con fecha y hora de creación.
    - Se activan las 5 cajas (1 exclusiva Diamante + 4 generales).
    - Cada ejecutivo llama, verifica presencia y atiende o avanza según
      el tiempo máximo de espera de la categoría del cliente.
    - Al finalizar, se imprimen las estadísticas: clientes ingresados,
      tiempos de espera y atención, y el detalle de fecha/hora de cada uno.

Ejecutar con:  python3 simulacion.py
"""

import time

from modelo import TipoCliente
from sistema_turnos import SistemaTurnos

# Clientes de prueba: (nombre, categoría)
clientes_prueba = [
    ("Ana García",        TipoCliente.DIAMANTE),
    ("Luis Pérez",        TipoCliente.ORO),
    ("María Torres",      TipoCliente.PLATA),
    ("Carlos Ruiz",       TipoCliente.NO_CLIENTE),
    ("Sofía Hernández",   TipoCliente.ORO),
    ("Jorge Martínez",    TipoCliente.DIAMANTE),
    ("Valeria López",     TipoCliente.PLATA),
    ("Diego Ramírez",     TipoCliente.NO_CLIENTE),
    ("Camila Flores",     TipoCliente.ORO),
    ("Andrés Castillo",   TipoCliente.PLATA),
    ("Fernanda Ortiz",    TipoCliente.DIAMANTE),
    ("Ricardo Mendoza",   TipoCliente.NO_CLIENTE),
    ("Paola Jiménez",     TipoCliente.ORO),
    ("Sebastián Rojas",   TipoCliente.PLATA),
    ("Daniela Vargas",    TipoCliente.NO_CLIENTE),
    ("Emilio Navarro",    TipoCliente.ORO),
    ("Renata Salas",      TipoCliente.DIAMANTE),
    ("Iván Cordero",      TipoCliente.PLATA),
]


def separador(titulo):
    print("\n" + "#" * 96)
    print(f"# {titulo}")
    print("#" * 96)


def main():
    sistema = SistemaTurnos()

    # ------------------------------------------------------------------
    # 1) Registrar clientes de las 4 categorías (se emite su ticket)
    # ------------------------------------------------------------------
    separador("REGISTRO DE CLIENTES (emisión de tickets)")
    for nombre, tipo in clientes_prueba:
        ticket = sistema.registrar_cliente(nombre, tipo)
        print(f"Turno #{ticket.numero_turno:03d} | {nombre:<18} | {tipo.value:<10} | "
              f"Creado: {ticket.fecha_creacion} {ticket.hora_creacion} | "
              f"Espera máx.: {ticket.tiempo_max_espera}s")

    print(f"\nTotal de clientes ingresados: {sistema.estadisticas.total_ingresados}")
    print(sistema.estado_colas())

    # ------------------------------------------------------------------
    # 2) Ejemplo de ticket individual (formato tipo comprobante)
    # ------------------------------------------------------------------
    separador("EJEMPLO DE TICKET GENERADO")
    sistema.cola_diamante.peek().imprimir_ticket()

    # ------------------------------------------------------------------
    # 3) Activar las 5 cajas (ejecutivos) y procesar toda la fila
    # ------------------------------------------------------------------
    separador("ATENCIÓN EN CAJAS (1 exclusiva Diamante + 4 generales)")
    inicio = time.time()
    sistema.iniciar_cajas(verbose=True, modo_continuo=False)
    sistema.esperar_finalizacion()
    duracion_total = round(time.time() - inicio, 2)

    # ------------------------------------------------------------------
    # 4) Estadísticas finales
    # ------------------------------------------------------------------
    separador(f"SIMULACIÓN FINALIZADA EN {duracion_total} SEGUNDOS")
    sistema.estadisticas.imprimir_resumen()
    sistema.estadisticas.imprimir_detalle_clientes()


if __name__ == "__main__":
    main()
