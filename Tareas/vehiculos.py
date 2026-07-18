class vehiculos:
    #Constructor de la clase vehiculos
    def __init__(self, marca, modelo, anio, velocidadInicial):
        self.__marca = marca
        self.__modelo = modelo
        self.__anio = anio
        self.__velocidadInicial = velocidadInicial

    #Metodo acelerar que aumenta la velocidad del vehiculo
    def acelerar(self, incremento):
        if incremento > 0:
            self.__velocidadInicial += incremento
            print(f"El vehículo ha acelerado {incremento} km/h. Velocidad actual: {self.__velocidadInicial} km/h")
        else:
            print("El incremento debe ser positivo.")
    
    #Metodo frenar que disminuye la velocidad del vehiculo
    def frenar(self, decremento):
        if decremento > 0:
            if decremento <= self.__velocidadInicial:
                self.__velocidadInicial -= decremento
                print(f"El vehículo ha frenado {decremento} km/h. Velocidad actual: {self.__velocidadInicial} km/h")
            else:
                print("El decremento no puede ser mayor que la velocidad actual.")
        else:
            print("El decremento debe ser positivo.")
    
    #Metodo para mostrar los datos del vehiculo
    def mostrar_datos(self):
        print("\n===== DATOS DEL VEHÍCULO =====")
        print(f"Marca: {self.__marca}")
        print(f"Modelo: {self.__modelo}")
        print(f"Año: {self.__anio}")
        print(f"Velocidad actual: {self.__velocidadInicial} km/h")
        print("==============================")

#Clase hija automovil que hereda de la clase vehiculos
class automovil(vehiculos):
    def __init__(self, marca, modelo, anio, velocidadInicial, numeroPuertas):
        super().__init__(marca, modelo, anio, velocidadInicial)
        self.__numeroPuertas = numeroPuertas

    def encenderaire(self):
        print("El aire acondicionado del automóvil está encendido.")

    def describir(self):
        print(f"Soy un automovil y tengo {self.__numeroPuertas} puertas.")

#Clase hija motocicleta que hereda de la clase vehiculos
class motocicleta(vehiculos):
    def __init__(self, marca, modelo, anio, velocidadInicial, cilindraje):
        super().__init__(marca, modelo, anio, velocidadInicial)
        self.__cilindraje = cilindraje

    def doCaballito(self):
        print("La motocicleta ha hecho un caballito")

    def describir(self):
        print(f"Soy una motocicleta y tengo un cilindraje de {self.__cilindraje} cc.")

#Clase hija camion que hereda de la clase vehiculos
class camion(vehiculos):
    def __init__(self, marca, modelo, anio, velocidadInicial, capacidadCarga):
        super().__init__(marca, modelo, anio, velocidadInicial)
        self.__capacidadCarga = capacidadCarga

    def cargarMercancia(self, peso):
        if peso <= self.__capacidadCarga:
            print(f"Se ha cargado {peso} kg de mercancía en el camión.")
        else:
            print(f"No se puede cargar {peso} kg. La capacidad máxima es {self.__capacidadCarga} kg.")

    def describir(self):
        print(f"Soy un camión y tengo una capacidad de carga de {self.__capacidadCarga} kg.")

# ==============================
# PROGRAMA PRINCIPAL
# ==============================

print("====================================")
print("   SISTEMA DE GESTIÓN DE VEHÍCULOS")
print("====================================")

# Creación de objetos
print("\n--- Creación de objetos ---")

auto1 = automovil("Toyota", "Corolla", 2024, 0, 4)
auto2 = automovil("Honda", "Civic", 2023, 10, 4)

moto1 = motocicleta("Yamaha", "R15", 2023, 0, 155)
moto2 = motocicleta("Kawasaki", "Ninja 400", 2024, 20, 400)

camion1 = camion("Volvo", "FH16", 2022, 0, 18000)

print("Se han creado dos automóviles.")
print("Se han creado dos motocicletas.")
print("Se ha creado un camión.")

# =====================================
# Llamada de métodos
# =====================================

print("\n===== AUTOMÓVIL 1 =====")
auto1.mostrar_datos()
auto1.acelerar(60)
auto1.encenderaire()
auto1.frenar(20)

print("\n===== AUTOMÓVIL 2 =====")
auto2.mostrar_datos()
auto2.acelerar(30)
auto2.encenderaire()

print("\n===== MOTOCICLETA 1 =====")
moto1.mostrar_datos()
moto1.acelerar(90)
moto1.doCaballito()

print("\n===== MOTOCICLETA 2 =====")
moto2.mostrar_datos()
moto2.frenar(10)
moto2.doCaballito()

print("\n===== CAMIÓN =====")
camion1.mostrar_datos()
camion1.acelerar(40)
camion1.cargarMercancia(15000)

# =====================================
# Herencia
# =====================================

print("\n====================================")
print(" DEMOSTRACIÓN DE HERENCIA ")
print("====================================")

print("Todos los vehículos utilizan los métodos heredados:")
print("- mostrar_datos()")
print("- acelerar()")
print("- frenar()")

auto1.acelerar(10)
moto1.acelerar(5)
camion1.acelerar(15)

# =====================================
# Polimorfismo
# =====================================

print("\n====================================")
print(" DEMOSTRACIÓN DE POLIMORFISMO ")
print("====================================")

vehiculos = [auto1, auto2, moto1, moto2, camion1]

for vehiculo in vehiculos:
    vehiculo.describir()

print("\n====================================")
print(" Fin del programa")
print("====================================")