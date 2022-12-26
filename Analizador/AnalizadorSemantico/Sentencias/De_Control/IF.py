from ...Clases_Abstractas import Operacion,NodoAST
from ..De_Transferencia import Break,Continue,Return
from ....Interprete.Tabla_de_Simbolos import Error,TablaSimbolos,TIPO

class If(Operacion):
    def __init__(self, Condicion, InstruccionesIf, InstruccionesElse, File, Columna):
        self.Condicion         = Condicion
        self.InstruccionesIf   = InstruccionesIf
        self.InstruccionesElse = InstruccionesElse
        self.File              = File
        self.Columna           = Columna

    def Interpretar(self, Arbol, TablaSimbolo):
        Condicion = self.Condicion.Interpretar(Arbol, TablaSimbolo)
        if isinstance(Condicion, Error): return Condicion

        if self.Condicion.Tipo == TIPO.BOOLEANO:
            if bool(Condicion) == True:   # VERIFICA SI ES VERDADERA LA Condicion
                nuevaTabla = TablaSimbolos(TablaSimbolo,"IF")       #NUEVO ENTORNO
                TablaSimbolo.AgregarHijo(nuevaTabla)
                for instruccion in self.InstruccionesIf:
                    result = instruccion.Interpretar(Arbol, nuevaTabla) #EJECUTA INSTRUCCION ADENTRO DEL IF
                    if isinstance(result, Error) :
                        Arbol.getExcepciones().append(result)
                        Arbol.updateConsola(result.toString())
                    if isinstance(result, Break): return result
                    if isinstance(result, Return): return result
                    if isinstance(result, Continue): return result
            else:               #ELSE
                
                if self.InstruccionesElse != None:
                    if isinstance(self.InstruccionesElse,If):
                        result = self.InstruccionesElse.Interpretar(Arbol, TablaSimbolo)
                        if isinstance(result, Error): return result
                        if isinstance(result, Break): return result
                        if isinstance(result, Return): return result
                        if isinstance(result, Continue): return result
                    else:
                        nuevaTabla = TablaSimbolos(TablaSimbolo," ELSE ")       #NUEVO ENTORNO
                        TablaSimbolo.AgregarHijo(nuevaTabla)
                        for instruccion in self.InstruccionesElse:
                            result = instruccion.Interpretar(Arbol, nuevaTabla) #EJECUTA INSTRUCCION ADENTRO DEL IF
                            if isinstance(result, Error) :
                                Arbol.getExcepciones().append(result)
                                Arbol.updateConsola(result.toString()) 
                            if isinstance(result, Break): return result
                            if isinstance(result, Return): return result
                            if isinstance(result, Continue): return result    
        else:
            return Error("Semantico", "Tipo de dato no booleano en IF.", self.File, self.Columna)
    
    def getNodo(self):
        nodo=NodoAST("IF")
        nodo.agregarHijoNodo(self.Condicion.getNodo())
        Instrucciones=NodoAST("INSTRUCCIONES")
        for instruccion in self.InstruccionesIf:
            Instrucciones.agregarHijoNodo(instruccion.getNodo())
        nodo.agregarHijoNodo(Instrucciones)
        if self.InstruccionesElse!=None:
            if isinstance(self.InstruccionesElse,If):
                ifnodo=NodoAST("ELSE IF")
                ifnodo.agregarHijoNodo(self.InstruccionesElse.getNodo())
                nodo.agregarHijoNodo(ifnodo)
            else:
                elsenodo=NodoAST("ELSE")
                for instruccion in self.InstruccionesElse:
                    elsenodo.agregarHijoNodo(instruccion.getNodo())
                nodo.agregarHijoNodo(elsenodo)
                
        return nodo