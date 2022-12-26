# Clase simbolo:

class Simbolo:
    def __init__(self, identificador, tipo, arreglo, Fila, Columna, valor ):
        self.id      = identificador
        self.tipo    = tipo             #? ES EL TIPO DE DATO QUE ES EL SIMBOLO
        self.Fila    = Fila
        self.Columna = Columna
        self.valor   = valor            #? ES EL VALOR QUE ALMACENARA EL SIMBOLO
        self.arreglo = arreglo          #? True es arreglo, False no lo es

    def getID(self):
        return self.id

    def setID(self, id):
        self.id = id

    def getTipo(self):
        return self.tipo

    def setTipo(self, tipo):
        self.tipo = tipo  

    def getValor(self):
        return self.valor

    def setValor(self, valor):
        self.valor = valor

    def getFila(self):
        return self.Fila
    
    def getColumna(self):
        return self.Columna
    
    def isArreglo(self):
        return self.arreglo