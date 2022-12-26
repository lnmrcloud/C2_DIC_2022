from ...Interprete.Tabla_de_Simbolos import TIPO,Error,Simbolo
from ..Clases_Abstractas import Operacion,NodoAST
from .Arreglo import Arreglo
import copy


class DeclaracionArregloTipo1(Operacion):
    def __init__(self, Tipo1, Dimensiones, Identificador, Tipo2, Expresiones, Fila, Columna):
        self.Identificador = Identificador
        self.Tipo = Tipo1
        self.Tipo2 = Tipo2
        self.Dimensiones = Dimensiones
        self.Expresiones = Expresiones
        self.Fila = Fila
        self.Columna = Columna
        self.Arreglo = True


    def Interpretar(self, Arbol, TablaSimbolo):
        if self.Tipo != self.Tipo2:                     #VERIFICACION DE TipoS
            return Error("Semantico", "Tipo de dato diferente en Arreglo.", self.Fila, self.Columna)
        if self.Dimensiones != len(self.Expresiones):   #VERIFICACION DE Dimensiones
            return Error("Semantico", "Dimensiones diferentes en Arreglo.", self.Fila, self.Columna)

        # CREACION DEL Arreglo
        value = self.crearDimensiones(Arbol, TablaSimbolo, copy.copy(self.Expresiones))     #RETORNA EL Arreglo DE Dimensiones
        if isinstance(value, Error): return value
        simbolo = Simbolo(str(self.Identificador), self.Tipo, self.Arreglo, self.Fila, self.Columna, value)
        result = TablaSimbolo.SetVariable(simbolo)
        if isinstance(result, Error): return result
        return None
        
    def crearDimensiones(self, Arbol, TablaSimbolo, Expresiones):
        arr = []
        if len(Expresiones) == 0:
            return None
        dimension = Expresiones.pop(0)
        num = dimension.Interpretar(Arbol, TablaSimbolo)
        if isinstance(num, Error): return num
        if dimension.Tipo != TIPO.ENTERO:
            return Error("Semantico", "Expresion diferente a ENTERO en Arreglo.", self.Fila, self.Columna)
        
        #!? VERIFICAMOS QUE LOS NUMEROS DE LAS DIMENSIONES NO SEAN NEGATIVOS
        if num<=0: return Error("Semantico","Dimension negativa o igual a cero",self.Fila,self.Columna)
        
        contador = 0
        while contador < num:
            arr.append(self.crearDimensiones(Arbol, TablaSimbolo, copy.copy(Expresiones)))
            contador += 1
        return arr

    def getNodo(self):
        nodo = NodoAST("DECLARACION ARREGLO")
        if self.Tipo == TIPO.ENTERO:
            nodo.agregarHijo(str("INT"))
        elif self.Tipo == TIPO.DECIMAL:
            nodo.agregarHijo(str("DOUBLE"))
        elif self.Tipo == TIPO.CADENA:
            nodo.agregarHijo(str("STRING"))
        elif self.Tipo == TIPO.CARACTER:
            nodo.agregarHijo(str("CHAR"))
        elif self.Tipo == TIPO.BOOLEANO:
            nodo.agregarHijo(str("BOOLEAN"))
        dimensiones=NodoAST("DIMENSIONES")
        i=0
        while i<self.Dimensiones:
            dimensiones.agregarHijo("[]")
            i+=1
        nodo.agregarHijoNodo(dimensiones)
        nodo.agregarHijo(str(self.Identificador))
        nodo.agregarHijo("=")
        
        if self.Tipo2 == TIPO.ENTERO:
            nodo.agregarHijo(str("INT"))
        elif self.Tipo2 == TIPO.DECIMAL:
            nodo.agregarHijo(str("DOUBLE"))
        elif self.Tipo2 == TIPO.CADENA:
            nodo.agregarHijo(str("STRING"))
        elif self.Tipo2 == TIPO.CARACTER:
            nodo.agregarHijo(str("CHAR"))
        elif self.Tipo2 == TIPO.BOOLEANO:
            nodo.agregarHijo(str("BOOLEAN"))
        exp = NodoAST("DIMENSIONES")
        for expresion in self.Expresiones:
            exp.agregarHijoNodo(expresion.getNodo())
        nodo.agregarHijoNodo(exp)
        return nodo

class DeclaracionArregloTipo2(Operacion):
    def __init__(self, Tipo1, Dimensiones, Identificador, Expresiones, Fila, Columna):
        self.Identificador = Identificador
        self.Tipo = Tipo1
        self.Dimensiones = Dimensiones
        self.Expresiones = Expresiones
        self.Fila = Fila
        self.Columna = Columna
        self.Arreglo = True


    def Interpretar(self, Arbol, TablaSimbolo):
        
        valores=self.Expresiones.Interpretar(Arbol,TablaSimbolo)
        if isinstance(valores,Error): return valores
        if not isinstance(valores,list): return Error("Semantico","Tipo de dato no valido en asignacion de arreglo"+self.Identificador,self.Fila,self.Columna)
        if self.Tipo != self.Expresiones.Tipo:                     #VERIFICACION DE TipoS
             return Error("Semantico", "Tipo de dato diferente en Arreglo.", self.Fila, self.Columna)
        

        dim=[1]
        value = self.verificarDimensiones(Arbol, TablaSimbolo, copy.deepcopy(valores),1,dim)     #RETORNA EL Arreglo DE Dimensiones
        if isinstance(value, Error): return value
        if value[0] != self.Dimensiones: return Error("Semantico", "Dimensiones diferentes en Arreglo.", self.Fila, self.Columna) 
        
        simbolo = Simbolo(str(self.Identificador), self.Tipo, self.Arreglo, self.Fila, self.Columna, valores)
        result = TablaSimbolo.SetVariable(simbolo)
        if isinstance(result, Error): return result
        return None
        
    def verificarDimensiones(self, Arbol, TablaSimbolo, valores, dimension,num):
        
        numerodimension=0
        for valor in valores:
            if isinstance(valor,list):
                if numerodimension==0:
                    numerodimension=len(valor)
                if numerodimension!=len(valor): return Error("Semantico","Diferentes cantidad de dimensiones dentro de una misma dimension",self.Fila,self.Columna)
                val=self.verificarDimensiones(Arbol,TablaSimbolo,valor,dimension+1,num)
                if isinstance(val,Error):return val
                
            else:
                if numerodimension==0:
                    numerodimension=1
                if numerodimension!=1: return Error("Semantico","Diferentes cantidad de dimensiones dentro de una misma dimension",self.Fila,self.Columna)
        if num[0]<dimension:
            num[0]=dimension   
        return num
            
            
            

    def getNodo(self):
        nodo = NodoAST("DECLARACION ARREGLO")
        if self.Tipo == TIPO.ENTERO:
            nodo.agregarHijo(str("INT"))
        elif self.Tipo == TIPO.DECIMAL:
            nodo.agregarHijo(str("DOUBLE"))
        elif self.Tipo == TIPO.CADENA:
            nodo.agregarHijo(str("STRING"))
        elif self.Tipo == TIPO.CARACTER:
            nodo.agregarHijo(str("CHAR"))
        elif self.Tipo == TIPO.BOOLEANO:
            nodo.agregarHijo(str("BOOLEAN"))
        dimensiones=NodoAST("DIMENSIONES")
        i=0
        while i<self.Dimensiones:
            dimensiones.agregarHijo("[]")
            i+=1
        nodo.agregarHijoNodo(dimensiones)
        
        nodo.agregarHijo(str(self.Identificador))
        nodo.agregarHijo("=")
        nodo.agregarHijoNodo(self.Expresiones.getNodo())
        
        return nodo
            

