from ..Clases_Abstractas import Operacion,NodoAST
from ...Interprete.Tabla_de_Simbolos import TIPO,Error

class Round(Operacion):
    def __init__(self,Expresion, Fila, Columna):
        self.Expresion=Expresion
        self.Fila=Fila
        self.Columna=Columna
        self.Tipo=TIPO.ENTERO
        
    def Interpretar(self, Arbol, TablaSimbolos):
        valor = self.Expresion.Interpretar(Arbol,TablaSimbolos)
        if isinstance(valor,Error): return valor
        if isinstance(valor,list): return Error("Semantico","Tipo de dato no valido para Round()",self.Fila,self.Columna)
        if self.Expresion.Tipo != TIPO.ENTERO and self.Expresion.Tipo != TIPO.DECIMAL:
            return Error("Semantico","Tipo de dato no valido para Round()",self.Fila,self.Columna)
        if self.Expresion.Tipo == TIPO.DECIMAL:
            num=str(valor).split(".")
            numero=int(num[0])      #? PARTE ENTERA
            decimal=int(num[1][0])  #? PRIMER CARACTER DE LA PARTE DECIMAL
            if(decimal>=5):
                if numero<0:
                    numero-=1
                else:
                    numero+=1
            return numero
        return round(valor)
        
    def getNodo(self):
        nodo=NodoAST("ROUND")
        nodo.agregarHijoNodo(self.Expresion.getNodo())
        return nodo