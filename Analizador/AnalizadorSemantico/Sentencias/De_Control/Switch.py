from ...Clases_Abstractas import Operacion,NodoAST
from ..De_Transferencia import Break,Continue,Return
from ....Interprete.Tabla_de_Simbolos import Error,TablaSimbolos

class Switch(Operacion):
    def __init__(self, Variable, CasesList, CaseDefault, File, Columna):
        self.Variable    = Variable
        self.CasesList   = CasesList
        self.CaseDefault = CaseDefault
        self.File        = File
        self.Columna     = Columna

    def Interpretar(self, Arbol, TablaSimbolo):
        Condicion = self.Variable.Interpretar(Arbol, TablaSimbolo)
        if isinstance(Condicion, Error): return Condicion
        if len(self.CasesList)==0 and len(self.CaseDefault)==0:
            return Error("Semantico","Switch sin Cases o default case",self.File,self.Columna)
        for Case in self.CasesList:
            
            valor=Case.Variable.Interpretar(Arbol,TablaSimbolo)
            if isinstance(valor,Error): 
                Arbol.getExcepciones().append(valor)
                Arbol.updateConsola(valor.toString())
            else:
                if Condicion==valor:
                    ejecutarCase=Case.Interpretar(Arbol,TablaSimbolo)
                    if isinstance(ejecutarCase, Error): return ejecutarCase
                    if isinstance(ejecutarCase, Break): return None
                    if isinstance(ejecutarCase, Return): return ejecutarCase
                    if isinstance(ejecutarCase, Continue): return ejecutarCase
                
        if len(self.CaseDefault)!=0:
            nuevaTabla = TablaSimbolos(TablaSimbolo,"SWITCH-DEFAULT")  #Nuevo entorno para el default
            TablaSimbolo.AgregarHijo(nuevaTabla)
            for instruccion in self.CaseDefault:
                result = instruccion.Interpretar(Arbol, nuevaTabla) #EJECUTA INSTRUCCION ADENTRO DEL IF
                if isinstance(result, Error) :
                    Arbol.getExcepciones().append(result)
                    Arbol.updateConsola(result.toString())
                if isinstance(result, Break): return None
                if isinstance(result, Return): return result 
                if isinstance(result, Continue): return result
    
    def getNodo(self):
        nodo=NodoAST("SWITCH")
        nodo.agregarHijo("SWITCH")
        nodo.agregarHijoNodo(self.Variable.getNodo())
        if len(self.CasesList)!=0:
            cases=NodoAST("CASES")
            for case in self.CasesList:
                cases.agregarHijoNodo(case.getNodo())
            nodo.agregarHijoNodo(cases)
        if len(self.CaseDefault)!=0:
            casedefault=NodoAST("DEFAULT")
            instrucciones =NodoAST("INSTRUCCIONES")
            for instruccion in self.CaseDefault:
                instrucciones.agregarHijoNodo(instruccion.getNodo())
            casedefault.agregarHijoNodo(instrucciones)
            nodo.agregarHijoNodo(casedefault)
        
        return nodo