from ..Clases_Abstractas import Operacion,NodoAST
from ...Interprete.Tabla_de_Simbolos import Error,TIPO,Simbolo

class Declaracion(Operacion):
    def __init__(self, Identificador, Fila, Columna, Expresion):
        self.Identificador = Identificador
        self.Expresion     = Expresion
        self.Fila          = Fila
        self.Columna       = Columna

    def Interpretar(self, Arbol, TablaSimbolos):
        simbolo = Simbolo(str(self.Identificador), TIPO.NULL,False, self.Fila, self.Columna, "NULL")
        result  = TablaSimbolos.SetVariable(simbolo)

        if isinstance(result, Error): return result
        #verifica si viene expresion
        if self.Expresion !=None:
            
            value = self.Expresion.Interpretar(Arbol, TablaSimbolos) # Valor a asignar a la variable
            if isinstance(value, Error): return value
            if self.Expresion.Tipo==None: return Error("Semantico","Asignacion de funcion sin valor",self.Fila,self.Columna)
            if value==None: return Error("Semantico","Operacion no valida, asignacion sin valor",self.Fila,self.Columna)
            if isinstance(value,list): return Error("Semantico","Asignacion incorrecta de arreglo",self.Fila,self.Columna)
            simbolo = Simbolo(str(self.Identificador), self.Expresion.Tipo,False, self.Fila, self.Columna, value)

            result = TablaSimbolos.ActualizarVariable(simbolo)

            if isinstance(result, Error): return result
        
            
        return None

    def getNodo(self):
        nodo=NodoAST("DECLARACION")
        id=NodoAST("IDENTIFICADOR")
        id.agregarHijo(str(self.Identificador))
        nodo.agregarHijoNodo(id)
        
        if self.Expresion!=None:
            nodo.agregarHijo("=")
            nodo.agregarHijoNodo(self.Expresion.getNodo())
        return nodo