class cuentaBancaria:
    def __init__(self, titular, saldo_inicial):
        self.titular = titular
        self.__saldo = saldo_inicial
        print(f"Cuanta creada para {self.titular}")

    def obtener_saldo(self):
        return self.__saldo
    
    def depositar(self, monto):
        if monto > 0:
            self.__saldo += monto
            print(f"Se han depositado {monto} a la cuenta de {self.titular}. Saldo actual: {self.__saldo}")
        else:
            print("La cantidad a depositar debe ser mayor que cero.")

cuenta1 = cuentaBancaria("Manuel", 1000)
cuenta1.depositar(1500)
cuenta1.depositar(-500)  # Intento de depósito inválido
# cuenta1.__saldo = 2000  # Intento de acceder al atributo privado
print(f"Saldo de {cuenta1.titular}: {cuenta1.obtener_saldo()}")