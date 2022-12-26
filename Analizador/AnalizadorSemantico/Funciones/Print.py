from ..Clases_Abstractas import Operacion,NodoAST
from ...Interprete.Tabla_de_Simbolos import Error,TIPO

class Print(Operacion):
    def __init__(self, Expresion, Fila, Columna):
        self.Expresion = Expresion
        self.Fila      = Fila
        self.Columna   = Columna

    def Interpretar(self, Arbol, TablaSimbolos):
        value = self.Expresion.Interpretar(Arbol, TablaSimbolos)  # RETORNA CUALQUIER VALOR

        if isinstance(value, Error) : return value

        if self.Expresion.Tipo == TIPO.ARREGLO:
            return Error("Semantico", "No se puede imprimir un arreglo completo", self.Fila, self.Columna)
        
        Arbol.updateConsola(value)
        
        return None
    
    def getNodo(self):
        nodo=NodoAST("PRINT")
        nodo.agregarHijoNodo(self.Expresion.getNodo())
        return nodo