from ...Clases_Abstractas import Operacion,NodoAST
from ..De_Transferencia import Break,Continue,Return
from ....Interprete.Tabla_de_Simbolos import Error,TablaSimbolos

class Case(Operacion):
    def __init__(self, Variable, Instrucciones, File, Columna):
        self.Variable      = Variable
        self.Instrucciones = Instrucciones
        self.File          = File
        self.Columna       = Columna

    def Interpretar(self, Arbol, TablaSimbolo):
        
        nuevaTabla = TablaSimbolos(TablaSimbolo, "SWITCH-CASE")       #NUEVO ENTORNO
        TablaSimbolo.AgregarHijo(nuevaTabla)
        for instruccion in self.Instrucciones:
            result = instruccion.Interpretar(Arbol, nuevaTabla) #EJECUTA INSTRUCCION ADENTRO DEL IF
            if isinstance(result, Error) :
                Arbol.getExcepciones().append(result)
                Arbol.updateConsola(result.toString())
            if isinstance(result, Break): return result
            if isinstance(result, Return): return result
            if isinstance(result, Continue): return result
            
    def getNodo(self):
        nodo=NodoAST("CASE")
        nodo.agregarHijoNodo(self.Variable.getNodo())
        instrucciones=NodoAST("INSTRUCCIONES")
        for instruccion in self.Instrucciones:
            instrucciones.agregarHijoNodo(instruccion.getNodo())
        nodo.agregarHijoNodo(instrucciones)
        return nodo
                
        