from ..Clases_Abstractas import Operacion,NodoAST
from ...Interprete.Tabla_de_Simbolos import TIPO,Error
class Casteo(Operacion):
    def __init__(self,Tipo,Expresion, Fila, Columna):
        self.Tipo    = Tipo
        self.Expresion   = Expresion
        self.Fila    = Fila
        self.Columna = Columna
        
    def Interpretar(self, Arbol, TablaSimbolos):
        valor=self.Expresion.Interpretar(Arbol,TablaSimbolos)
        if isinstance(valor,Error): return valor
        if valor == None: return Error("Semantico","Operacion sin valor",self.Fila,self.Columna)
        if isinstance(valor,list): return Error("Semantico","Operacion con arreglo no valida",self.Fila,self.Columna)
         
        

        #? (DOUBLE) VALOR
        if self.Tipo == TIPO.DECIMAL:
            if self.Expresion.Tipo == TIPO.ENTERO:
                try:
                    return float(self.obtenervalor(self.Expresion.Tipo, valor))
                except:
                    return Error("Semantico", "No se puede castear "+str(valor)+" para Double.", self.Fila, self.Columna)
            elif self.Expresion.Tipo == TIPO.CADENA:
                try:
                    return float(self.obtenervalor(self.Expresion.Tipo, valor))
                except:
                    return Error("Semantico", "No se puede castear \""+str(valor)+"\" para Double.", self.Fila, self.Columna)
            elif self.Expresion.Tipo == TIPO.CARACTER:
                try:
                    return ord(self.obtenervalor(self.Expresion.Tipo, valor))
                except:
                    return Error("Semantico", "No se puede castear \'"+str(valor)+"\' para Double.", self.Fila, self.Columna)
            return Error("Semantico", "Tipo Erroneo de casteo para Double.", self.Fila, self.Columna)
        #? (INT) VALOR
        elif self.Tipo == TIPO.ENTERO:
            if self.Expresion.Tipo == TIPO.DECIMAL:
                try:
                    return int(self.obtenervalor(self.Expresion.Tipo, valor))
                except:
                    return Error("Semantico", "No se puede castear "+str(valor)+" para Int.", self.Fila, self.Columna)
            elif self.Expresion.Tipo == TIPO.CADENA:
                try:
                    return int(self.obtenervalor(self.Expresion.Tipo, valor))
                except:
                    return Error("Semantico", "No se puede castear \""+str(valor)+"\" para Int.", self.Fila, self.Columna)
            elif self.Expresion.Tipo == TIPO.CARACTER:
                try:
                    return ord(self.obtenervalor(self.Expresion.Tipo, valor))
                except:
                    return Error("Semantico", "No se puede castear \'"+str(valor)+"\' para Int.", self.Fila, self.Columna)
            return Error("Semantico", "Tipo Erroneo de casteo para Int.", self.Fila, self.Columna)
        #? (CHAR) VALOR
        elif self.Tipo == TIPO.CARACTER:
            if self.Expresion.Tipo == TIPO.ENTERO:
                try:
                    return str(chr(self.obtenervalor(self.Expresion.Tipo, valor)))
                except:
                    return Error("Semantico", "No se puede castear "+str(valor)+" para Char.", self.Fila, self.Columna)
            return Error("Semantico", "Tipo Erroneo de casteo para Char.", self.Fila, self.Columna)
        #? (STRING) VALOR
        elif self.Tipo == TIPO.CADENA:
            if self.Expresion.Tipo == TIPO.ENTERO:
                try:
                    return str(self.obtenervalor(self.Expresion.Tipo, valor))
                except:
                    return Error("Semantico", "No se puede castear "+str(valor)+" para Int.", self.Fila, self.Columna)
            elif self.Expresion.Tipo == TIPO.DECIMAL:
                try:
                    return str(self.obtenervalor(self.Expresion.Tipo, valor))
                except:
                    return Error("Semantico", "No se puede castear "+str(valor)+" para Int.", self.Fila, self.Columna)
            return Error("Semantico", "Tipo Erroneo de casteo para String.", self.Fila, self.Columna)
        #? (BOOLEAN) VALOR
        elif self.Tipo == TIPO.BOOLEANO:
            if self.Expresion.Tipo == TIPO.CADENA:
                try:
                    if(str(valor).lower()=="false"):
                        return False
                    return bool(self.obtenervalor(self.Expresion.Tipo, valor))
                except:
                    return Error("Semantico", "No se puede castear \""+str(valor)+"\" para Boolean.", self.Fila, self.Columna)
            return Error("Semantico", "Tipo Erroneo de casteo para Int.", self.Fila, self.Columna)
        
    def obtenervalor(self, tipo, valor):
        if tipo == TIPO.ENTERO:
            return int(valor)
        elif tipo == TIPO.DECIMAL:
            return float(valor)
        elif tipo == TIPO.BOOLEANO:
            return bool(valor)
        return str(valor)
    
    def getNodo(self):
        nodo=NodoAST("CASTEO")
        nodo.agregarHijo("(")
        if self.Tipo==TIPO.CADENA:
            nodo.agregarHijo("STRING")
        elif self.Tipo==TIPO.CARACTER:
            nodo.agregarHijo("CHAR")
        elif self.Tipo==TIPO.ENTERO:
            nodo.agregarHijo("INT")
        elif self.Tipo==TIPO.DECIMAL:
            nodo.agregarHijo("DOUBLE")
        elif self.Tipo==TIPO.BOOLEANO:
            nodo.agregarHijo("BOOLEAN")
        nodo.agregarHijo(")")
        nodo.agregarHijoNodo(self.Expresion.getNodo())
        return nodo