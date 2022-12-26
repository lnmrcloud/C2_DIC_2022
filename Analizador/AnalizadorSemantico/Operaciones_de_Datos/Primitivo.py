from ..Clases_Abstractas import Operacion,NodoAST

class Primitivos(Operacion):
    """
        CLASE QUE ALMACENARA EL VALOR ENCONTRADO Y QUE TIPO DE DATO PRIMITIVO ES    
    """
    def __init__(self, Tipo, Valor, Fila, Columna):
        self.Tipo    = Tipo
        self.Valor   = Valor
        self.Fila    = Fila
        self.Columna = Columna

    def Interpretar(self, Arbol, TablaSimbolos):
        return self.Valor
    
    def getNodo(self):
        nodo=NodoAST("PRIMITIVO")
        nodo.agregarHijo(str(self.Valor))
        return nodo