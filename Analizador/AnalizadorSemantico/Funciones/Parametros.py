from ..Clases_Abstractas import Operacion,NodoAST
from ...Interprete.Tabla_de_Simbolos import TIPO

class Parametro(Operacion):
    def __init__(self,Id,Dimensiones,Tipo, Fila, Columna):
        self.Id          = Id
        self.Dimensiones = Dimensiones  #? recibe un numero entero si es 0 no es un arreglo
        self.Tipo        = Tipo     # STRING, CHAR, BOOLEAN,INT,DOUBLE
        self.Fila        = Fila
        self.Columna     = Columna
        self.Arreglo     = False
        
    def Interpretar(self, Arbol, TablaSimbolos):
        if self.Dimensiones>0: self.Arreglo=True
        return self
    
    def getNodo(self):
        nodo=NodoAST("PARAMETRO")
        if self.Tipo==TIPO.CADENA:
            nodo.agregarHijo("STRING")
        elif self.Tipo==TIPO.CARACTER:
            nodo.agregarHijo("CHAR")
        elif self.Tipo==TIPO.ENTERO:
            nodo.agregarHijo("INT")
        elif self.Tipo==TIPO.DECIMAL:
            nodo.agregarHijo("DOUBLE")
        elif self.Tipo==TIPO.BOOLEANO:
            nodo.agregarHijo("BOOLEAN")
        nodo.agregarHijo(str(self.Id))
        return nodo