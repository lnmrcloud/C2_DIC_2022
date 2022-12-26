from ...Clases_Abstractas import Operacion,NodoAST

class Continue(Operacion):
    def __init__(self, Fila, Columna):
        self.Fila    = Fila
        self.Columna = Columna

    def Interpretar(self, Arbol, TablaSimbolos):
        return self
    
    def getNodo(self):
        nodo=NodoAST("CONTINUE")
        return nodo