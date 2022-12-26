from ..Clases_Abstractas import Operacion,NodoAST
from ...Interprete.Tabla_de_Simbolos import Error

class Identificador(Operacion):
    def __init__(self, Identificador, Fila, Columna):
        self.Identificador = Identificador
        self.Fila          = Fila
        self.Columna       = Columna
        self.Tipo          = None
        self.Arreglo       = False 

    def Interpretar(self, Arbol, TablaSimbolos):
        simbolo = TablaSimbolos.GetVariable(self.Identificador.lower())

        if simbolo == None:
            return Error("Semantico", "Variable " + self.Identificador + " no encontrada.", self.Fila, self.Columna)

        self.Tipo = simbolo.getTipo()
        self.Arreglo= simbolo.isArreglo()
        return simbolo.getValor()
    
    def getNodo(self):
        nodo=NodoAST("IDENTIFICADOR")
        nodo.agregarHijo(str(self.Identificador))
        return nodo