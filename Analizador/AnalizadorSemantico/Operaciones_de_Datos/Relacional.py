from ..Clases_Abstractas import Operacion,NodoAST
from ...Interprete.Tabla_de_Simbolos import Error,TIPO,OperadorRelacional

class Relacional(Operacion):
    def __init__(self, Operador, OperacionIzq, OperacionDer, Fila, Columna):
        self.Operador     = Operador
        self.OperacionIzq = OperacionIzq
        self.OperacionDer = OperacionDer
        self.Fila         = Fila
        self.Columna      = Columna
        self.Tipo         = TIPO.BOOLEANO

    
    def Interpretar(self, Arbol, TablaSimbolos):
        izq = self.OperacionIzq.Interpretar(Arbol, TablaSimbolos)
        if isinstance(izq, Error): return izq
        if izq == None: return Error("Semantico","Operacion sin valor",self.Fila,self.Columna)
        if isinstance(izq,list): return Error("Semantico","Operacion con arreglo no valida",self.Fila,self.Columna)
        if self.OperacionDer!=None:
            der = self.OperacionDer.Interpretar(Arbol, TablaSimbolos)
            if isinstance(der, Error): return der
            if der == None: return Error("Semantico","Operacion sin valor",self.Fila,self.Columna)
            if isinstance(der,list): return Error("Semantico","Operacion con arreglo no valida",self.Fila,self.Columna)
            if self.OperacionDer.Tipo == None :
                return Error("Semantico","Operacion de funcion "+self.OperacionDer.Identificador+"() sin valor",self.OperacionDer.Fila,self.OperacionDer.Columna)
        if self.OperacionIzq.Tipo == None:
            return Error("Semantico","Operacion de funcion "+self.OperacionIzq.Identificador+"() sin valor",self.OperacionIzq.Fila,self.OperacionIzq.Columna)
        #   SUMA
        # OPERADOR RELACIONAL ==
        if self.Operador == OperadorRelacional.IGUALACION:
            # IZQUIERDA ES ENTERO
            if self.OperacionIzq.Tipo == TIPO.ENTERO and self.OperacionDer.Tipo == TIPO.ENTERO:
                return self.obtenerVal(self.OperacionIzq.Tipo, izq) == self.obtenerVal(self.OperacionDer.Tipo, der)
            elif self.OperacionIzq.Tipo == TIPO.ENTERO and self.OperacionDer.Tipo == TIPO.DECIMAL:
                return self.obtenerVal(self.OperacionIzq.Tipo, izq) == self.obtenerVal(self.OperacionDer.Tipo, der)
            elif self.OperacionIzq.Tipo == TIPO.ENTERO and self.OperacionDer.Tipo == TIPO.CADENA:
                return str(self.obtenerVal(self.OperacionIzq.Tipo, izq)) == self.obtenerVal(self.OperacionDer.Tipo, der)
            # IZQUIERDA ES DECIMAL
            elif self.OperacionIzq.Tipo == TIPO.DECIMAL and self.OperacionDer.Tipo == TIPO.ENTERO:
                return self.obtenerVal(self.OperacionIzq.Tipo, izq) == self.obtenerVal(self.OperacionDer.Tipo, der)
            elif self.OperacionIzq.Tipo == TIPO.DECIMAL and self.OperacionDer.Tipo == TIPO.DECIMAL:
                return self.obtenerVal(self.OperacionIzq.Tipo, izq) == self.obtenerVal(self.OperacionDer.Tipo, der)
            elif self.OperacionIzq.Tipo == TIPO.DECIMAL and self.OperacionDer.Tipo == TIPO.CADENA:
                return str(self.obtenerVal(self.OperacionIzq.Tipo, izq)) == self.obtenerVal(self.OperacionDer.Tipo, der)
            # IZQUIERDA ES BOOLEANO
            elif self.OperacionIzq.Tipo == TIPO.BOOLEANO and self.OperacionDer.Tipo == TIPO.BOOLEANO:
                return self.obtenerVal(self.OperacionIzq.Tipo, izq) == self.obtenerVal(self.OperacionDer.Tipo, der)
            elif self.OperacionIzq.Tipo == TIPO.BOOLEANO and self.OperacionDer.Tipo == TIPO.CADENA:
                return self.obtenerVal(self.OperacionIzq.Tipo, izq) == bool(self.obtenerVal(self.OperacionDer.Tipo, der))
            # IZQUIERDA ES CARACTER
            elif self.OperacionIzq.Tipo == TIPO.CARACTER and self.OperacionDer.Tipo == TIPO.CARACTER:
                return self.obtenerVal(self.OperacionIzq.Tipo, izq) == self.obtenerVal(self.OperacionDer.Tipo, der)
            # IZQUIERDA ES CADENA
            elif self.OperacionIzq.Tipo == TIPO.CADENA and self.OperacionDer.Tipo == TIPO.ENTERO:
                return self.obtenerVal(self.OperacionIzq.Tipo, izq) == str(self.obtenerVal(self.OperacionDer.Tipo, der))
            elif self.OperacionIzq.Tipo == TIPO.CADENA and self.OperacionDer.Tipo == TIPO.DECIMAL:
                return self.obtenerVal(self.OperacionIzq.Tipo, izq) == str(self.obtenerVal(self.OperacionDer.Tipo, der))
            elif self.OperacionIzq.Tipo == TIPO.CADENA and self.OperacionDer.Tipo == TIPO.BOOLEANO:
                return bool(self.obtenerVal(self.OperacionIzq.Tipo, izq)) == self.obtenerVal(self.OperacionDer.Tipo, der)
            elif self.OperacionIzq.Tipo == TIPO.CADENA and self.OperacionDer.Tipo == TIPO.CADENA:
                return self.obtenerVal(self.OperacionIzq.Tipo, izq) == self.obtenerVal(self.OperacionDer.Tipo, der)
            return Error("Semantico", "Tipo Erroneo de operacion para ==.", self.Fila, self.Columna)
        # OPERADOR RELACIONAL =!
        if self.Operador == OperadorRelacional.DIFERENCIACION:
            # IZQUIERDA ES ENTERO
            if self.OperacionIzq.Tipo == TIPO.ENTERO and self.OperacionDer.Tipo == TIPO.ENTERO:
                return self.obtenerVal(self.OperacionIzq.Tipo, izq) != self.obtenerVal(self.OperacionDer.Tipo, der)
            elif self.OperacionIzq.Tipo == TIPO.ENTERO and self.OperacionDer.Tipo == TIPO.DECIMAL:
                return self.obtenerVal(self.OperacionIzq.Tipo, izq) != self.obtenerVal(self.OperacionDer.Tipo, der)
            elif self.OperacionIzq.Tipo == TIPO.ENTERO and self.OperacionDer.Tipo == TIPO.CADENA:
                return str(self.obtenerVal(self.OperacionIzq.Tipo, izq)) != self.obtenerVal(self.OperacionDer.Tipo, der)
            # IZQUIERDA ES DECIMAL
            elif self.OperacionIzq.Tipo == TIPO.DECIMAL and self.OperacionDer.Tipo == TIPO.ENTERO:
                return self.obtenerVal(self.OperacionIzq.Tipo, izq) != self.obtenerVal(self.OperacionDer.Tipo, der)
            elif self.OperacionIzq.Tipo == TIPO.DECIMAL and self.OperacionDer.Tipo == TIPO.DECIMAL:
                return self.obtenerVal(self.OperacionIzq.Tipo, izq) != self.obtenerVal(self.OperacionDer.Tipo, der)
            elif self.OperacionIzq.Tipo == TIPO.DECIMAL and self.OperacionDer.Tipo == TIPO.CADENA:
                return str(self.obtenerVal(self.OperacionIzq.Tipo, izq)) != self.obtenerVal(self.OperacionDer.Tipo, der)
            # IZQUIERDA ES BOOLEANO
            elif self.OperacionIzq.Tipo == TIPO.BOOLEANO and self.OperacionDer.Tipo == TIPO.BOOLEANO:
                return self.obtenerVal(self.OperacionIzq.Tipo, izq) != self.obtenerVal(self.OperacionDer.Tipo, der)
            elif self.OperacionIzq.Tipo == TIPO.BOOLEANO and self.OperacionDer.Tipo == TIPO.CADENA:
                return self.obtenerVal(self.OperacionIzq.Tipo, izq) != bool(self.obtenerVal(self.OperacionDer.Tipo, der))
            # IZQUIERDA ES CARACTER
            elif self.OperacionIzq.Tipo == TIPO.CARACTER and self.OperacionDer.Tipo == TIPO.CARACTER:
                return self.obtenerVal(self.OperacionIzq.Tipo, izq) != self.obtenerVal(self.OperacionDer.Tipo, der)
            # IZQUIERDA ES CADENA
            elif self.OperacionIzq.Tipo == TIPO.CADENA and self.OperacionDer.Tipo == TIPO.ENTERO:
                return self.obtenerVal(self.OperacionIzq.Tipo, izq) != str(self.obtenerVal(self.OperacionDer.Tipo, der))
            elif self.OperacionIzq.Tipo == TIPO.CADENA and self.OperacionDer.Tipo == TIPO.DECIMAL:
                return self.obtenerVal(self.OperacionIzq.Tipo, izq) != str(self.obtenerVal(self.OperacionDer.Tipo, der))
            elif self.OperacionIzq.Tipo == TIPO.CADENA and self.OperacionDer.Tipo == TIPO.BOOLEANO:
                return bool(self.obtenerVal(self.OperacionIzq.Tipo, izq)) != self.obtenerVal(self.OperacionDer.Tipo, der)
            elif self.OperacionIzq.Tipo == TIPO.CADENA and self.OperacionDer.Tipo == TIPO.CADENA:
                return self.obtenerVal(self.OperacionIzq.Tipo, izq) != self.obtenerVal(self.OperacionDer.Tipo, der)
            return Error("Semantico", "Tipo Erroneo de operacion para ==.", self.Fila, self.Columna)
        # OPERADOR RELACIONAL <
        elif self.Operador == OperadorRelacional.MENORQUE:
            # IZQUIERDA ES ENTERO
            if self.OperacionIzq.Tipo == TIPO.ENTERO and self.OperacionDer.Tipo == TIPO.ENTERO:
                return self.obtenerVal(self.OperacionIzq.Tipo, izq) < self.obtenerVal(self.OperacionDer.Tipo, der)
            elif self.OperacionIzq.Tipo == TIPO.ENTERO and self.OperacionDer.Tipo == TIPO.DECIMAL:
                return self.obtenerVal(self.OperacionIzq.Tipo, izq) < self.obtenerVal(self.OperacionDer.Tipo, der)
            # IZQUIERDA ES DECIMAL
            elif self.OperacionIzq.Tipo == TIPO.DECIMAL and self.OperacionDer.Tipo == TIPO.ENTERO:
                return self.obtenerVal(self.OperacionIzq.Tipo, izq) < self.obtenerVal(self.OperacionDer.Tipo, der)
            elif self.OperacionIzq.Tipo == TIPO.DECIMAL and self.OperacionDer.Tipo == TIPO.DECIMAL:
                return self.obtenerVal(self.OperacionIzq.Tipo, izq) < self.obtenerVal(self.OperacionDer.Tipo, der)
            # IZQUIERDA ES BOOLEANO
            elif self.OperacionIzq.Tipo == TIPO.BOOLEANO and self.OperacionDer.Tipo == TIPO.BOOLEANO:
                return self.obtenerVal(self.OperacionIzq.Tipo, izq) < self.obtenerVal(self.OperacionDer.Tipo, der)
            return Error("Semantico", "Tipo Erroneo de operacion para <.", self.Fila, self.Columna)
        # OPERADOR RELACIONAL >
        elif self.Operador == OperadorRelacional.MAYORQUE:
            # IZQUIERDA ES ENTERO
            if self.OperacionIzq.Tipo == TIPO.ENTERO and self.OperacionDer.Tipo == TIPO.ENTERO:
                return self.obtenerVal(self.OperacionIzq.Tipo, izq) > self.obtenerVal(self.OperacionDer.Tipo, der)
            elif self.OperacionIzq.Tipo == TIPO.ENTERO and self.OperacionDer.Tipo == TIPO.DECIMAL:
                return self.obtenerVal(self.OperacionIzq.Tipo, izq) > self.obtenerVal(self.OperacionDer.Tipo, der)
            # IZQUIERDA ES DECIMAL
            elif self.OperacionIzq.Tipo == TIPO.DECIMAL and self.OperacionDer.Tipo == TIPO.ENTERO:
                return self.obtenerVal(self.OperacionIzq.Tipo, izq) > self.obtenerVal(self.OperacionDer.Tipo, der)
            elif self.OperacionIzq.Tipo == TIPO.DECIMAL and self.OperacionDer.Tipo == TIPO.DECIMAL:
                return self.obtenerVal(self.OperacionIzq.Tipo, izq) > self.obtenerVal(self.OperacionDer.Tipo, der)
            # IZQUIERDA ES BOOLEANO
            elif self.OperacionIzq.Tipo == TIPO.BOOLEANO and self.OperacionDer.Tipo == TIPO.BOOLEANO:
                return self.obtenerVal(self.OperacionIzq.Tipo, izq) > self.obtenerVal(self.OperacionDer.Tipo, der)
            return Error("Semantico", "Tipo Erroneo de operacion para >.", self.Fila, self.Columna)
        
        # OPERADOR RELACIONAL <=
        elif self.Operador == OperadorRelacional.MENORIGUAL:
            # IZQUIERDA ES ENTERO
            if self.OperacionIzq.Tipo == TIPO.ENTERO and self.OperacionDer.Tipo == TIPO.ENTERO:
                return self.obtenerVal(self.OperacionIzq.Tipo, izq) <= self.obtenerVal(self.OperacionDer.Tipo, der)
            elif self.OperacionIzq.Tipo == TIPO.ENTERO and self.OperacionDer.Tipo == TIPO.DECIMAL:
                return self.obtenerVal(self.OperacionIzq.Tipo, izq) <= self.obtenerVal(self.OperacionDer.Tipo, der)
            # IZQUIERDA ES DECIMAL
            elif self.OperacionIzq.Tipo == TIPO.DECIMAL and self.OperacionDer.Tipo == TIPO.ENTERO:
                return self.obtenerVal(self.OperacionIzq.Tipo, izq) <= self.obtenerVal(self.OperacionDer.Tipo, der)
            elif self.OperacionIzq.Tipo == TIPO.DECIMAL and self.OperacionDer.Tipo == TIPO.DECIMAL:
                return self.obtenerVal(self.OperacionIzq.Tipo, izq) <= self.obtenerVal(self.OperacionDer.Tipo, der)
            # IZQUIERDA ES BOOLEANO
            elif self.OperacionIzq.Tipo == TIPO.BOOLEANO and self.OperacionDer.Tipo == TIPO.BOOLEANO:
                return self.obtenerVal(self.OperacionIzq.Tipo, izq) <= self.obtenerVal(self.OperacionDer.Tipo, der)
            return Error("Semantico", "Tipo Erroneo de operacion para <.", self.Fila, self.Columna)
        # OPERADOR RELACIONAL >=
        elif self.Operador == OperadorRelacional.MAYORIGUAL:
            # IZQUIERDA ES ENTERO
            if self.OperacionIzq.Tipo == TIPO.ENTERO and self.OperacionDer.Tipo == TIPO.ENTERO:
                return self.obtenerVal(self.OperacionIzq.Tipo, izq) >= self.obtenerVal(self.OperacionDer.Tipo, der)
            elif self.OperacionIzq.Tipo == TIPO.ENTERO and self.OperacionDer.Tipo == TIPO.DECIMAL:
                return self.obtenerVal(self.OperacionIzq.Tipo, izq) >= self.obtenerVal(self.OperacionDer.Tipo, der)
            # IZQUIERDA ES DECIMAL
            elif self.OperacionIzq.Tipo == TIPO.DECIMAL and self.OperacionDer.Tipo == TIPO.ENTERO:
                return self.obtenerVal(self.OperacionIzq.Tipo, izq) >= self.obtenerVal(self.OperacionDer.Tipo, der)
            elif self.OperacionIzq.Tipo == TIPO.DECIMAL and self.OperacionDer.Tipo == TIPO.DECIMAL:
                return self.obtenerVal(self.OperacionIzq.Tipo, izq) >= self.obtenerVal(self.OperacionDer.Tipo, der)
            # IZQUIERDA ES BOOLEANO
            elif self.OperacionIzq.Tipo == TIPO.BOOLEANO and self.OperacionDer.Tipo == TIPO.BOOLEANO:
                return self.obtenerVal(self.OperacionIzq.Tipo, izq) >= self.obtenerVal(self.OperacionDer.Tipo, der)
            return Error("Semantico", "Tipo Erroneo de operacion para >.", self.Fila, self.Columna)

        
        return Error("Semantico", "Tipo de Operacion no Especificado.", self.Fila, self.Columna)

    def obtenerVal(self, tipo, val):
        if tipo == TIPO.ENTERO:
            return int(val)
        elif tipo == TIPO.DECIMAL:
            return float(val)
        elif tipo == TIPO.BOOLEANO:
            return bool(val)
        return str(val)
    
    def getNodo(self):
        nodo = NodoAST("RELACIONAL")
        nodo.agregarHijoNodo(self.OperacionIzq.getNodo())
        if self.Operador==OperadorRelacional.IGUALACION:
            nodo.agregarHijo("==")
        elif self.Operador==OperadorRelacional.DIFERENCIACION:
            nodo.agregarHijo("=!")
        elif self.Operador==OperadorRelacional.MAYORQUE:
            nodo.agregarHijo(">")
        elif self.Operador==OperadorRelacional.MENORQUE:
            nodo.agregarHijo("<")
        elif self.Operador==OperadorRelacional.MAYORIGUAL:
            nodo.agregarHijo(">=")
        elif self.Operador==OperadorRelacional.MENORIGUAL:
            nodo.agregarHijo("<=")
        nodo.agregarHijoNodo(self.OperacionDer.getNodo())
        
        
        return nodo
        