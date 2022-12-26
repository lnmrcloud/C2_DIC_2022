from ..Clases_Abstractas import Operacion,NodoAST
from ...Interprete.Tabla_de_Simbolos import TIPO,Error
from ..Operaciones_de_Datos import Identificador,Arreglo

class TypeOf(Operacion):
    def __init__(self,Expresion, Fila, Columna):
        self.Expresion=Expresion
        self.Fila=Fila
        self.Columna=Columna
        self.Tipo=TIPO.CADENA
        
    def Interpretar(self, Arbol, TablaSimbolos):
        valor = self.Expresion.Interpretar(Arbol,TablaSimbolos)
        if isinstance(valor,Error): return valor
        if valor==None: return "NULL"
        if isinstance(self.Expresion,Identificador):
            if self.Expresion.Arreglo:
                if self.Expresion.Tipo == TIPO.ENTERO :
                    return "ARREGLO-INT"
                elif self.Expresion.Tipo == TIPO.DECIMAL :
                    return "ARREGLO-DOUBLE"
                elif self.Expresion.Tipo == TIPO.CADENA :
                    return "ARREGLO-STRING"
                elif self.Expresion.Tipo == TIPO.CARACTER :
                    return "ARREGLO-CHAR"
                elif self.Expresion.Tipo == TIPO.BOOLEANO :
                    return "ARREGLO-BOOLEAN"
        elif isinstance(valor,list):
            if self.Expresion.Tipo == TIPO.ENTERO :
                return "ARREGLO-INT"
            elif self.Expresion.Tipo == TIPO.DECIMAL :
                return "ARREGLO-DOUBLE"
            elif self.Expresion.Tipo == TIPO.CADENA :
                return "ARREGLO-STRING"
            elif self.Expresion.Tipo == TIPO.CARACTER :
                return "ARREGLO-CHAR"
            elif self.Expresion.Tipo == TIPO.BOOLEANO :
                return "ARREGLO-BOOLEAN"
        if self.Expresion.Tipo == TIPO.ENTERO :
            return "INT"
        elif self.Expresion.Tipo == TIPO.DECIMAL :
            return "DOUBLE"
        elif self.Expresion.Tipo == TIPO.CADENA :
            return "STRING"
        elif self.Expresion.Tipo == TIPO.CARACTER :
            return "CHAR"
        elif self.Expresion.Tipo == TIPO.BOOLEANO :
            return "BOOLEAN"
        elif self.Expresion.Tipo == TIPO.NULL : 
            return "NULL"
        
        
        return Error("Semantico","Tipo de dato no valido para typeof()",self.Fila,self.Columna)
        
    def getNodo(self):
        nodo=NodoAST("TYPEOF")
        nodo.agregarHijoNodo(self.Expresion.getNodo())
        return nodo