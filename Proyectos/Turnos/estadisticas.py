"""
estadisticas.py
----------------
Recolecta y reporta las estadísticas del sistema de turnos:
    - Cuántos clientes entraron (por categoría y en total).
    - En cuánto tiempo salieron (tiempo de atención) los clientes.
    - Registro de fecha/hora de creación, llamado e inicio/fin de atención,
      para poder calcular el tiempo de espera real de cada cliente.
    - Cumplimiento del SLA (tiempo máximo de espera) por categoría.
"""

import threading
from collections import defaultdict

from modelo import TipoCliente


class Estadisticas:
    def __init__(self):
        self._lock = threading.Lock()
        self.total_ingresados = 0
        self.ingresados_por_tipo = defaultdict(int)
        self.atendidos = []          # tickets atendidos con éxito
        self.no_presentados = []     # tickets que no se presentaron a tiempo

    # ------------------------------------------------------------------
    def registrar_ingreso(self, tipo_cliente: TipoCliente) -> None:
        with self._lock:
            self.total_ingresados += 1
            self.ingresados_por_tipo[tipo_cliente] += 1

    def registrar_atendido(self, ticket) -> None:
        with self._lock:
            self.atendidos.append(ticket)

    def registrar_no_presentado(self, ticket) -> None:
        with self._lock:
            self.no_presentados.append(ticket)

    # ------------------------------------------------------------------
    def _promedio(self, valores):
        valores = [v for v in valores if v is not None]
        return round(sum(valores) / len(valores), 2) if valores else 0.0

    def resumen_por_tipo(self):
        """Retorna un diccionario con métricas agregadas por categoría de cliente."""
        resumen = {}
        for tipo in TipoCliente:
            atendidos_tipo = [t for t in self.atendidos if t.tipo_cliente == tipo]
            no_pres_tipo = [t for t in self.no_presentados if t.tipo_cliente == tipo]
            esperas = [t.tiempo_espera_real() for t in atendidos_tipo]
            atenciones = [t.tiempo_atencion() for t in atendidos_tipo]
            cumplidos = [t for t in atendidos_tipo if t.cumplio_sla()]

            resumen[tipo] = {
                "ingresados": self.ingresados_por_tipo.get(tipo, 0),
                "atendidos": len(atendidos_tipo),
                "no_presentados": len(no_pres_tipo),
                "espera_promedio": self._promedio(esperas),
                "atencion_promedio": self._promedio(atenciones),
                "cumplimiento_sla": (
                    round(100 * len(cumplidos) / len(atendidos_tipo), 1)
                    if atendidos_tipo else 0.0
                ),
            }
        return resumen

    # ------------------------------------------------------------------
    def imprimir_resumen(self) -> None:
        print("\n" + "=" * 96)
        print(f"{'ESTADÍSTICAS DEL SISTEMA DE TURNOS':^96}")
        print("=" * 96)
        print(f"Total de clientes ingresados : {self.total_ingresados}")
        print(f"Total atendidos con éxito    : {len(self.atendidos)}")
        print(f"Total no presentados         : {len(self.no_presentados)}")

        resumen = self.resumen_por_tipo()
        print("\n" + "-" * 96)
        print(f"{'Categoría':<12}{'Ingresados':>12}{'Atendidos':>12}{'No present.':>14}"
              f"{'Espera prom.(s)':>18}{'Atención prom.(s)':>18}{'Cumpl. SLA':>12}")
        print("-" * 96)
        for tipo in TipoCliente:
            d = resumen[tipo]
            print(f"{tipo.value:<12}{d['ingresados']:>12}{d['atendidos']:>12}{d['no_presentados']:>14}"
                  f"{d['espera_promedio']:>18}{d['atencion_promedio']:>18}{str(d['cumplimiento_sla'])+'%':>12}")
        print("-" * 96)

    def imprimir_detalle_clientes(self) -> None:
        """Imprime el detalle de cada cliente atendido: fecha/hora y tiempos de espera."""
        print("\n" + "=" * 118)
        print(f"{'DETALLE DE CLIENTES ATENDIDOS (fecha, hora y tiempos)':^118}")
        print("=" * 118)
        print(f"{'Turno':<7}{'Cliente':<18}{'Tipo':<11}{'Caja':<6}{'Fecha':<12}{'Hora creación':<15}"
              f"{'Hora llamado':<14}{'Espera(s)':<11}{'Atención(s)':<13}{'SLA'}")
        print("-" * 118)
        for t in sorted(self.atendidos, key=lambda x: x.numero_turno):
            print(f"{'#'+format(t.numero_turno,'03d'):<7}{t.nombre:<18}{t.tipo_cliente.value:<11}"
                  f"{t.caja_asignada:<6}{t.fecha_creacion:<12}{t.hora_creacion:<15}"
                  f"{(t.hora_llamado or '-'):<14}{str(t.tiempo_espera_real()):<11}"
                  f"{str(t.tiempo_atencion()):<13}{'Cumplido' if t.cumplio_sla() else 'Excedido'}")
        print("=" * 118)

        if self.no_presentados:
            print("\nClientes que NO se presentaron a tiempo:")
            for t in sorted(self.no_presentados, key=lambda x: x.numero_turno):
                print(f"  #{t.numero_turno:03d} {t.nombre} ({t.tipo_cliente.value}) - "
                      f"creado {t.fecha_creacion} {t.hora_creacion}, límite {t.tiempo_max_espera}s")
