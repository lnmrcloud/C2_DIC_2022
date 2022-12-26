from ...Interprete.Tabla_de_Simbolos import TIPO,Error,Simbolo
from ..Clases_Abstractas import Operacion,NodoAST
import copy



class AsignacionArreglo(Operacion):
    def __init__(self, Identificador, Dimensiones, Expresion, Fila, Columna):
        self.Identificador = Identificador
        self.Dimensiones = Dimensiones
        self.Expresion = Expresion
        self.Fila = Fila
        self.Columna = Columna


    def Interpretar(self, Arbol, TablaSimbolo):
        value = self.Expresion.Interpretar(Arbol, TablaSimbolo) # Expresion a asignar a la variable
        if isinstance(value, Error): return value

        simbolo = TablaSimbolo.GetVariable(self.Identificador.lower())

        if simbolo == None:
            return Error("Semantico", "Arreglo " + self.Identificador + " no encontrada.", self.Fila, self.Columna)
        
        if not simbolo.isArreglo(): 
            return Error("Semantico", "Arreglo " + self.Identificador + " no es un arreglo.", self.Fila, self.Columna)

        if simbolo.getTipo() != self.Expresion.Tipo:
            return Error("Semantico", "Tipos de dato diferente en Modificacion de arreglo.", self.Fila, self.Columna)

        # BUSQUEDA DEL ARREGLO
        value = self.modificarDimensiones(Arbol, TablaSimbolo, copy.copy(self.Dimensiones), simbolo.getValor(), value)     #RETORNA EL Expresion SOLICITADO
        if isinstance(value, Error): return value

        return value

    def modificarDimensiones(self, Arbol, TablaSimbolo, Dimensiones, arreglo, Expresion):
        if len(Dimensiones) == 0:
            if isinstance(arreglo, list):
                return Error("Semantico", "Modificacion a Arreglo incompleto.", self.Fila, self.Columna)
            return Expresion
        if not isinstance(arreglo, list):
            return Error("Semantico", "Accesos de más en un Arreglo.", self.Fila, self.Columna)
        dimension = Dimensiones.pop(0)
        num = dimension.Interpretar(Arbol, TablaSimbolo)
        if isinstance(num, Error): return num
        if dimension.Tipo != TIPO.ENTERO:
            return Error("Semantico", "Expresion diferente a ENTERO en Arreglo.", self.Fila, self.Columna)
        if num<0: return Error("Semantico","Dimension negativa",self.Fila,self.Columna)
        try:
            value = self.modificarDimensiones(Arbol, TablaSimbolo, copy.copy(Dimensiones), arreglo[num], Expresion)
            if isinstance(value, Error): return value
            if value != None:
                arreglo[num] = value
        except:
            return Error("Semantico", "Indice fuera de rango", self.Fila, self.Columna)
        return None

    def getNodo(self):
        nodo = NodoAST("ASIGNACION ARREGLO")
        nodo.agregarHijo(str(self.Identificador))
        exp = NodoAST("DIMENSIONES")
        for expresion in self.Dimensiones:
            exp.agregarHijoNodo(expresion.getNodo())
        nodo.agregarHijoNodo(exp)
        nodo.agregarHijo("=")
        nodo.agregarHijoNodo(self.Expresion.getNodo())
        return nodo

            
