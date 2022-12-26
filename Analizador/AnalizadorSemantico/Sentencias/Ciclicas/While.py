from ...Clases_Abstractas import Operacion,NodoAST
from ..De_Transferencia import Break,Continue,Return
from ....Interprete.Tabla_de_Simbolos import Error,TablaSimbolos,TIPO

class While(Operacion):
    def __init__(self, Condicion, Instrucciones, Fila, Columna):
        self.Condicion     = Condicion
        self.Instrucciones = Instrucciones
        self.Fila          = Fila
        self.Columna       = Columna

    def Interpretar(self, Arbol, TablaSimbolo):
        while True:
            Condicion = self.Condicion.Interpretar(Arbol, TablaSimbolo)
            if isinstance(Condicion, Error): return Condicion

            if self.Condicion.Tipo == TIPO.BOOLEANO:
                if bool(Condicion) == True:   # VERIFICA SI ES VERDADERA LA Condicion
                    nuevaTabla = TablaSimbolos(TablaSimbolo,"WHILE")       #NUEVO ENTORNO
                    TablaSimbolo.AgregarHijo(nuevaTabla)
                    for instruccion in self.Instrucciones:
                        result = instruccion.Interpretar(Arbol, nuevaTabla) #EJECUTA INSTRUCCION ADENTRO DEL IF
                        if isinstance(result, Error) :
                            Arbol.getExcepciones().append(result)
                            Arbol.updateConsola(result.toString())
                        if isinstance(result, Break): return None
                        if isinstance(result, Return): return result
                        if isinstance(result, Continue): break
                else:
                    break
            else:
                return Error("Semantico", "Tipo de dato no booleano en IF.", self.Fila, self.Columna)
            
    def getNodo(self):
        nodo=NodoAST("While")
        nodo.agregarHijo("While")
        nodo.agregarHijoNodo(self.Condicion.getNodo())
        instrucciones=NodoAST("INSTRUCCIONES")
        for instruccion in self.Instrucciones:
            instrucciones.agregarHijoNodo(instruccion.getNodo())
        nodo.agregarHijoNodo(instrucciones)
        return nodo