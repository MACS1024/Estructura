class cuentaBancaria:
    #contructor
    def __init__(self, numCuenta, titular, saldoInicial):
        self.__numCuenta = numCuenta
        self.__titular = titular
        self.__saldo = saldoInicial
        print(f"Cuenta creada: {self.__numCuenta}, Titular: {self.__titular}, Saldo inicial: {self.__saldo}")

    #metodo para depositar
    def depositar(self, cantidad):
        if cantidad > 0:
            self.__saldo += cantidad
            print(f"Depósito realizado: {cantidad}. Nuevo saldo: {self.__saldo}")
        else:
            print("Cantidad a depositar debe ser positiva.")

    #metodo para retirar
    def retirar(self, cantidad):
        if cantidad <= 0:
            print("La cantidad a retirar debe ser positiva")
        elif cantidad > self.__saldo:
            print("Saldo insuficiente")
        else:
            self.__saldo -= cantidad
            print(f"Retiro realizado: {cantidad}, nuevo saldo: {self.__saldo}")
    
    #metodo para consultar saldo
    def consultar_saldo(self):
        print(f"Saldo disponible: ", {self.__saldo})

    #metodo para mostrar datos de la cuenta
    def mostrar_datos(self):
        print("\n===== DATOS DE LA CUENTA =====")
        print(f"Titular: ", self.__titular)
        print(f"Numero de cuenta: ", self.__numCuenta)
        print(f"Saldo: ", self.__saldo)
        print("==============================")

    #Destructor
    def __del__(self):
        print(f"La cuenta con numero: {self.__numCuenta} ha sido eliminada.")

# ==========================
# Programa Principal
# ==========================

#Dos objetos de tipo cuentaBancaria
cuenta1 = cuentaBancaria("1001", "Manuel Chuc", 5000)
cuenta2 = cuentaBancaria("1002", "Norma Huchin", 3000)

print("\n--- Operaciones en Cuenta 1 ---")
cuenta1.depositar(1000)
cuenta1.depositar(-200)      # Depósito inválido
cuenta1.retirar(1500)
cuenta1.retirar(6000)        # Retiro inválido
cuenta1.consultar_saldo()

print("\n--- Operaciones en Cuenta 2 ---")
cuenta2.depositar(500)
cuenta2.depositar(700)
cuenta2.retirar(1000)
cuenta2.retirar(5000)        # Retiro inválido
cuenta2.consultar_saldo()

print("\n--- Información de las cuentas ---")
cuenta1.mostrar_datos()
cuenta2.mostrar_datos()

print("\n--- Eliminando una cuenta ---")
del cuenta1

