from ..Clases_Abstractas import Operacion,NodoAST
from ..Sentencias.De_Transferencia import Continue,Break,Return
from ...Interprete.Tabla_de_Simbolos import Error,TablaSimbolos

class Main(Operacion):
    def __init__(self, Instrucciones, Fila, Columna):
        self.Instrucciones = Instrucciones
        self.Fila          = Fila
        self.Columna       = Columna

    def Interpretar(self, Arbol, TablaSimbolo):
        
        nuevaTabla = TablaSimbolos(TablaSimbolo,"Main()")       #NUEVO ENTORNO
        TablaSimbolo.AgregarHijo(nuevaTabla)
        for instruccion in self.Instrucciones:
            result = instruccion.Interpretar(Arbol, nuevaTabla) #EJECUTA INSTRUCCION ADENTRO DEL IF
            if isinstance(result, Error) :
                Arbol.getExcepciones().append(result)
                Arbol.updateConsola(result.toString())
            if isinstance(result, Break): return result
            if isinstance(result, Return): return result
            if isinstance(result, Continue): 
                CotinueError=Error("Semantico", "Continue fuera de ciclo")
                Arbol.getExcepciones().append(CotinueError)
                Arbol.updateConsola(CotinueError.toString())
                
    def getNodo(self):
        nodo=NodoAST("MAIN")
        instrucciones=NodoAST("INSTRUCCIONES")
        for instruccion in self.Instrucciones:
            instrucciones.agregarHijoNodo(instruccion.getNodo())
        nodo.agregarHijoNodo(instrucciones)
        return nodo