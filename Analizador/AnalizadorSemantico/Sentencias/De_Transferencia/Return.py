from ...Clases_Abstractas import Operacion,NodoAST
from ....Interprete.Tabla_de_Simbolos import Error

class Return(Operacion):
    def __init__(self, Expresion, Fila, Columna):
        self.Expresion = Expresion
        self.Fila      = Fila
        self.Columna   = Columna
        self.Tipo      = None
        self.Result    = None

    def Interpretar(self, Arbol, table):
        if self.Expresion!=None:
            Result = self.Expresion.Interpretar(Arbol, table)
            if isinstance(Result, Error): return Result

            self.Tipo = self.Expresion.Tipo #Tipo DEL Result
            self.Result = Result            #VALOR DEL Result

        return self
    
    def getNodo(self):
        nodo=NodoAST("RETURN")
        nodo.agregarHijoNodo(self.Expresion.getNodo())
        return nodo