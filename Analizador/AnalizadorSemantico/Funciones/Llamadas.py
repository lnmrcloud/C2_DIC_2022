from ..Sentencias.De_Transferencia import Return
from ..Clases_Abstractas import Operacion,NodoAST
from ...Interprete.Tabla_de_Simbolos import Error

class Llamada(Operacion):
    def __init__(self, Identificador , Parametros , Fila, Columna):
        self.Identificador = Identificador
        self.Parametros    = Parametros
        self.Fila          = Fila
        self.Columna       = Columna
        self.Tipo          = None

    def Interpretar(self, Arbol, TablaSimbolos):
        funcion = TablaSimbolos.GetFuncion(self.Identificador.lower())
        if isinstance(funcion,Error): return funcion
        if funcion == None:
            return Error("Semantico", "Funcion " + self.Identificador + " no encontrada.", self.Fila, self.Columna)
        if len(self.Parametros)!= len(funcion.Parametros):
            return Error("Semantico", "Cantidad de parametros diferente ",self.Fila,self.Columna)
        funcion.ParametrosRecibidos = self.Parametros
        valor=funcion.Interpretar(Arbol,TablaSimbolos)
        if isinstance(valor,Error): return valor
        if isinstance(valor,Return):
            self.Tipo = valor.Tipo
            return valor.Result
        
        
        
        return valor
    
    def getNodo(self):
        nodo=NodoAST("LLAMADA")
        nodo.agregarHijo(str(self.Identificador))
        parametros=NodoAST("PARAMETROS")
        for parametro in self.Parametros:
            parametros.agregarHijoNodo(parametro.getNodo())
        nodo.agregarHijoNodo(parametros)    
        
        return nodo