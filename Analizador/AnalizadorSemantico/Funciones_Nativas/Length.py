from ..Clases_Abstractas import Operacion,NodoAST
from ...Interprete.Tabla_de_Simbolos import TIPO,Error
from ..Operaciones_de_Datos import Identificador

class Length(Operacion):
    def __init__(self,Expresion, Fila, Columna):
        self.Expresion = Expresion
        self.Fila      = Fila
        self.Columna   = Columna
        self.Tipo      = TIPO.ENTERO
        
    def Interpretar(self, Arbol, TablaSimbolos):
        valor = self.Expresion.Interpretar(Arbol,TablaSimbolos)
        if isinstance(valor,Error):return Error
        
        if isinstance(valor,list): 
            return len(valor)    
        elif self.Expresion.Tipo == TIPO.CADENA:
            return len(valor)
        elif self.Expresion.Tipo == TIPO.ARREGLO:
            return len(valor)
        else:
            return Error("Semantico", "Tipo de dato no valido para length()",self.Fila,self.Columna)
    
    def getNodo(self):
        nodo = NodoAST("LENGTH")
        nodo.agregarHijoNodo(self.Expresion.getNodo())
        return nodo