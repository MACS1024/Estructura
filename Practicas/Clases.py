#Definiendo la clase
class Galleta:
    pass

#Instanciando el objeto
galleta_chocolate = Galleta()
galleta_vainilla = Galleta()

class Perro:
    #Constructor
    def __init__(self, nombre, raza):
        self.nombre = nombre
        self.raza = raza
        print(f"{self.nombre} ha nacido!")

    #def nombre_metodo(argumentos/parametros)
    #Funciones miembro / Metodos 
    def ladrar(self):
        return print(f"{self.nombre} dice Guau!!")
    
    #Destructor
    def __del__(self):
        print(f"{self.nombre} ha sido elimindo de la memoria!")

mi_perro = Perro("Solovino", "Malix")
mi_perro.ladrar()
del mi_perro