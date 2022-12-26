from ..Clases_Abstractas import Operacion,NodoAST
from ...Interprete.Tabla_de_Simbolos import TIPO,Error

class Truncate(Operacion):
    def __init__(self,Expresion, Fila, Columna):
        self.Expresion=Expresion
        self.Fila=Fila
        self.Columna=Columna
        self.Tipo=TIPO.ENTERO
        
    def Interpretar(self, Arbol, TablaSimbolos):
        valor = self.Expresion.Interpretar(Arbol,TablaSimbolos)
        if isinstance(valor,Error): return valor
        if isinstance(valor,list): return Error("Semantico","Tipo de dato no valido para truncate()",self.Fila,self.Columna)
        if self.Expresion.Tipo != TIPO.ENTERO and self.Expresion.Tipo != TIPO.DECIMAL:
            return Error("Semantico","Tipo de dato no valido para truncate()",self.Fila,self.Columna)

        return int(valor)
        
    def getNodo(self):
        nodo=NodoAST("TRUNCATE")
        nodo.agregarHijoNodo(self.Expresion.getNodo())
        return nodo