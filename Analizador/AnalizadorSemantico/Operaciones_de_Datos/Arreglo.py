from ..Clases_Abstractas import Operacion,NodoAST
from ...Interprete.Tabla_de_Simbolos import Error,TablaSimbolos,TIPO
import copy

class Arreglo(Operacion):
    def __init__(self, Instrucciones, Fila, Columna):
        self.Tipo          = None
        self.Instrucciones = Instrucciones
        
        self.Fila          = Fila
        self.Columna       = Columna

    def Interpretar(self, Arbol, TablaSimbolo):
        self.Valor         = []
        for instruccion in self.Instrucciones:
            valor=instruccion.Interpretar(Arbol,TablaSimbolo)
            if isinstance(valor,Error): return valor
            if self.Tipo==None:
                self.Tipo=instruccion.Tipo
            elif self.Tipo != instruccion.Tipo:
                return Error("Semantico","Tipo diferente de dato dentro de arreglo",instruccion.Fila,instruccion.Columna)
            self.Valor.append(valor)
        return copy.deepcopy(self.Valor)
    
    def getNodo(self):
        nodo=NodoAST("ARREGLO")
        instrucciones2=NodoAST("Instrucciones")
        for instruccion in self.Instrucciones:
            instrucciones2.agregarHijoNodo(instruccion.getNodo())
        nodo.agregarHijoNodo(instrucciones2)
        return nodo

class ObtenerValorArreglo(Operacion):
    def __init__(self, Identificador, Expresiones, Fila, Columna):
        self.Identificador = Identificador
        self.Expresiones   = Expresiones
        self.Valor         = []
        self.Fila          = Fila
        self.Columna       = Columna
        self.Tipo          = None

    def Interpretar(self, Arbol, TablaSimbolo):
        simbolo = TablaSimbolo.GetVariable(self.Identificador.lower())

        if simbolo == None:
            return Error("Semantico", "Arreglo " + self.Identificador + " no encontrada.", self.Fila, self.Columna)
        self.Tipo=simbolo.getTipo()
        if not simbolo.isArreglo(): 
            return Error("Semantico", "Arreglo " + self.Identificador + " no es un arreglo.", self.Fila, self.Columna)
        value = self.buscarDimensiones(Arbol, TablaSimbolo, copy.copy(self.Expresiones), simbolo.getValor())     #RETORNA EL VALOR SOLICITADO
        if isinstance(value, Error): return value
        if isinstance(value, list):
            return Error("Semantico", "Acceso a Arreglo incompleto.", self.Fila, self.Columna)

        return copy.deepcopy(value)
        
    def buscarDimensiones(self, Arbol, TablaSimbolo, expresiones, arreglo):
        value = None
        if len(expresiones) == 0:
            return arreglo
        if not isinstance(arreglo, list):
            return Error("Semantico", "Accesos de más en un Arreglo.", self.Fila, self.Columna)
        dimension = expresiones.pop(0)
        num = dimension.Interpretar(Arbol, TablaSimbolo)
        if isinstance(num, Error): return num
        if dimension.Tipo != TIPO.ENTERO:
            return Error("Semantico", "Expresion diferente a ENTERO en Arreglo.", self.Fila, self.Columna)
        try:
            value = self.buscarDimensiones(Arbol, TablaSimbolo, copy.copy(expresiones), arreglo[num])
                
            return value
        except:
            return Error("Semantico", "Indice fuera de rango", self.Fila, self.Columna)
    
    def getNodo(self):
        nodo = NodoAST("ACCESO ARREGLO")
        nodo.agregarHijo(str(self.Identificador))
        exp = NodoAST("DIMENSIONES")
        for expresion in self.Expresiones:
            exp.agregarHijoNodo(expresion.getNodo())
        nodo.agregarHijoNodo(exp)
        return nodo
    