"""
menu_turnos.py
---------------
Menú interactivo del sistema de turnos con prioridad. Las 5 cajas (1
exclusiva Diamante + 4 generales) se activan en segundo plano apenas
inicia el programa, cada una operada por su ejecutivo, y van atendiendo
a los clientes conforme se registran.

Ejecutar con:  python3 menu_turnos.py
"""

import time

from modelo import TipoCliente
from sistema_turnos import SistemaTurnos

TIPOS_MENU = {
    "1": TipoCliente.DIAMANTE,
    "2": TipoCliente.ORO,
    "3": TipoCliente.PLATA,
    "4": TipoCliente.NO_CLIENTE,
}


def mostrar_menu():
    print("\n" + "=" * 55)
    print("   SISTEMA DE TURNOS CON PRIORIDAD - BANCO MERIDIANO")
    print("=" * 55)
    print("1. Registrar cliente Diamante  (máx. 2s de espera)")
    print("2. Registrar cliente Oro       (máx. 5s de espera)")
    print("3. Registrar cliente Plata     (10-15s de espera)")
    print("4. Registrar cliente No cliente(30-60s de espera)")
    print("5. Ver estado de las cajas")
    print("6. Ver estado de las colas")
    print("7. Ver estadísticas actuales")
    print("8. Salir")
    print("=" * 55)


def registrar(sistema, tipo_cliente):
    nombre = input("Nombre del cliente: ").strip()
    if not nombre:
        print("✘ El nombre no puede estar vacío.")
        return
    ticket = sistema.registrar_cliente(nombre, tipo_cliente)
    print(f"\n✔ Ticket generado -> Turno #{ticket.numero_turno:03d}")
    ticket.imprimir_ticket()


def main():
    sistema = SistemaTurnos()
    # Las cajas quedan activas en segundo plano desde el inicio (modo continuo):
    # cada ejecutivo espera nuevos turnos aunque la cola esté momentáneamente vacía.
    sistema.iniciar_cajas(verbose=True, modo_continuo=True)

    try:
        while True:
            mostrar_menu()
            opcion = input("Seleccione una opción (1-8): ").strip()

            if opcion in TIPOS_MENU:
                registrar(sistema, TIPOS_MENU[opcion])
            elif opcion == "5":
                print("\n--- Estado de las cajas ---")
                print(sistema.estado_cajas())
            elif opcion == "6":
                print("\n--- Estado de las colas ---")
                print(sistema.estado_colas())
            elif opcion == "7":
                sistema.estadisticas.imprimir_resumen()
            elif opcion == "8":
                print("\nCerrando cajas y finalizando el sistema...")
                sistema.detener()
                sistema.estadisticas.imprimir_resumen()
                sistema.estadisticas.imprimir_detalle_clientes()
                print("\n¡Hasta luego!\n")
                break
            else:
                print("✘ Opción no válida.")

            time.sleep(0.2)
    except KeyboardInterrupt:
        print("\n\nInterrumpido por el usuario. Cerrando cajas...")
        sistema.detener()
        sistema.estadisticas.imprimir_resumen()


if __name__ == "__main__":
    main()
