from ..Clases_Abstractas import Operacion,NodoAST
from ...Interprete.Tabla_de_Simbolos import TIPO,Error

class ToLower(Operacion):
    def __init__(self, Expresion , Fila, Columna):
        self.Expresion = Expresion
        self.Fila      = Fila
        self.Columna   = Columna
        self.Tipo     = None
        
    def Interpretar(self, Arbol, TablaSimbolos):
        valor = self.Expresion.Interpretar(Arbol,TablaSimbolos)
        if isinstance(valor,Error): return valor
        
        if self.Expresion.Tipo!=TIPO.CADENA:
            return Error("Semantico","Tipo de dato no valido  para Funcion toLower",self.Fila,self.Columna)
        self.Tipo=TIPO.CADENA
        return valor.lower()
    
    def getNodo(self):
        nodo=NodoAST("TOLOWER")
        nodo.agregarHijoNodo(self.Expresion.getNodo())
        
        return nodo
