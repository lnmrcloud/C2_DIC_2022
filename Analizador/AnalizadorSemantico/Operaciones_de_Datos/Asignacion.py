from ..Clases_Abstractas import Operacion,NodoAST
from ...Interprete.Tabla_de_Simbolos import Error,Simbolo

class Asignacion(Operacion):
    """
    !    CLASE DE ASIGNACION, ASIGNA UN VALOR A UNA VARIABLE
    """
    def __init__(self, Identificador, Expresion, Fila, Comlumna):
        self.Identificador = Identificador
        self.Expresion     = Expresion
        self.Fila          = Fila
        self.Comlumna      = Comlumna
        self.Tipo          = None

    def Interpretar(self, Arbol, TablaSimbolos):
        
        value = self.Expresion.Interpretar(Arbol, TablaSimbolos) # Valor a asignar a la variable
        if isinstance(value, Error): return value
        if self.Expresion.Tipo==None: return Error("Semantico","Asignacion de funcion sin valor",self.Fila,self.Columna)
        if value==None: return Error("Semantico","Operacion no valida, asignacion sin valor",self.Fila,self.Columna)
        if isinstance(value,list): return Error("Semantico","Asignacion incorrecta de arreglo",self.Fila,self.Columna)
        simbolo = Simbolo(self.Identificador, self.Expresion.Tipo,False,self.Fila, self.Comlumna, value)
        self.Tipo=self.Expresion.Tipo
        result = TablaSimbolos.ActualizarVariable(simbolo)

        if isinstance(result, Error): return result
        return None

    def getNodo(self):
        nodo=NodoAST("ASIGNACION")
        id=NodoAST("IDENTIFICADOR")
        id.agregarHijo(str(self.Identificador))
        nodo.agregarHijoNodo(id)
        nodo.agregarHijo("=")
        nodo.agregarHijoNodo(self.Expresion.getNodo())
        return nodo