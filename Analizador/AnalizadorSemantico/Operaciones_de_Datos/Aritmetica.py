from ..Clases_Abstractas import Operacion,NodoAST
from ...Interprete.Tabla_de_Simbolos import Error,TIPO,OperadorAritmetico

class Aritmetica(Operacion):
    """
        CLASE QUE REALIZARA LAS OPERACIONES ARITMETICAS QUE SE REALICEN
    """
    def __init__(self, Operador, OperacionIzq, OperacionDer, Fila, Columna):
        self.Operador     = Operador        #+,-,*,/
        self.OperacionIzq = OperacionIzq    # VALOR PRIMITIVO o UN OBJETO ARITMETICA
        self.OperacionDer = OperacionDer    # VALOR PRIMITIVO o UN OBJETO ARITMETICA
        self.Fila         = Fila
        self.Columna      = Columna
        self.Tipo         = None            # EL TIPO ES NULO HASTA REALIZAR LA OPERACION ENTRE PRIMITIVOS

    
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
        if self.Operador == OperadorAritmetico.MAS: 
            # IZQUIERDA ES ENTERO
            if self.OperacionIzq.Tipo == TIPO.ENTERO and self.OperacionDer.Tipo == TIPO.ENTERO:
                self.Tipo = TIPO.ENTERO
                return self.ObtenerVal(self.OperacionIzq.Tipo, izq) + self.ObtenerVal(self.OperacionDer.Tipo, der)
            elif self.OperacionIzq.Tipo == TIPO.ENTERO and self.OperacionDer.Tipo == TIPO.DECIMAL:
                self.Tipo = TIPO.DECIMAL
                return self.ObtenerVal(self.OperacionIzq.Tipo, izq) + self.ObtenerVal(self.OperacionDer.Tipo, der)
            elif self.OperacionIzq.Tipo == TIPO.ENTERO and self.OperacionDer.Tipo == TIPO.BOOLEANO:
                self.Tipo = TIPO.ENTERO
                return self.ObtenerVal(self.OperacionIzq.Tipo, izq) + self.ObtenerVal(self.OperacionDer.Tipo, der)
            elif self.OperacionIzq.Tipo == TIPO.ENTERO and self.OperacionDer.Tipo == TIPO.CADENA:
                self.Tipo = TIPO.CADENA
                return str(self.ObtenerVal(self.OperacionIzq.Tipo, izq)) + self.ObtenerVal(self.OperacionDer.Tipo, der)
            # IZQUIERDA ES DECIMAL
            elif self.OperacionIzq.Tipo == TIPO.DECIMAL and self.OperacionDer.Tipo == TIPO.ENTERO:
                self.Tipo = TIPO.DECIMAL
                return self.ObtenerVal(self.OperacionIzq.Tipo, izq) + self.ObtenerVal(self.OperacionDer.Tipo, der)
            elif self.OperacionIzq.Tipo == TIPO.DECIMAL and self.OperacionDer.Tipo == TIPO.DECIMAL:
                self.Tipo = TIPO.DECIMAL
                return self.ObtenerVal(self.OperacionIzq.Tipo, izq) + self.ObtenerVal(self.OperacionDer.Tipo, der)
            elif self.OperacionIzq.Tipo == TIPO.DECIMAL and self.OperacionDer.Tipo == TIPO.BOOLEANO:
                self.Tipo = TIPO.DECIMAL
                return self.ObtenerVal(self.OperacionIzq.Tipo, izq) + self.ObtenerVal(self.OperacionDer.Tipo, der)
            elif self.OperacionIzq.Tipo == TIPO.DECIMAL and self.OperacionDer.Tipo == TIPO.CADENA:
                self.Tipo = TIPO.CADENA
                return str(self.ObtenerVal(self.OperacionIzq.Tipo, izq)) + self.ObtenerVal(self.OperacionDer.Tipo, der)
            # IZQUIERDA ES BOOLEANO
            elif self.OperacionIzq.Tipo == TIPO.BOOLEANO and self.OperacionDer.Tipo == TIPO.ENTERO:
                self.Tipo = TIPO.ENTERO
                return self.ObtenerVal(self.OperacionIzq.Tipo, izq) + self.ObtenerVal(self.OperacionDer.Tipo, der)
            elif self.OperacionIzq.Tipo == TIPO.BOOLEANO and self.OperacionDer.Tipo == TIPO.DECIMAL:
                self.Tipo = TIPO.DECIMAL
                return self.ObtenerVal(self.OperacionIzq.Tipo, izq) + self.ObtenerVal(self.OperacionDer.Tipo, der)
            elif self.OperacionIzq.Tipo == TIPO.BOOLEANO and self.OperacionDer.Tipo == TIPO.BOOLEANO:
                self.Tipo = TIPO.ENTERO
                return self.ObtenerVal(self.OperacionIzq.Tipo, izq) + self.ObtenerVal(self.OperacionDer.Tipo, der)
            elif self.OperacionIzq.Tipo == TIPO.BOOLEANO and self.OperacionDer.Tipo == TIPO.CADENA:
                self.Tipo = TIPO.CADENA
                return str(self.ObtenerVal(self.OperacionIzq.Tipo, izq)) + self.ObtenerVal(self.OperacionDer.Tipo, der)
            # IZQUIERDA ES CARACTER
            elif self.OperacionIzq.Tipo == TIPO.CARACTER and self.OperacionDer.Tipo == TIPO.CARACTER:
                self.Tipo = TIPO.CADENA
                return self.ObtenerVal(self.OperacionIzq.Tipo, izq) + self.ObtenerVal(self.OperacionDer.Tipo, der)
            elif self.OperacionIzq.Tipo == TIPO.CARACTER and self.OperacionDer.Tipo == TIPO.CADENA:
                self.Tipo = TIPO.CADENA
                return self.ObtenerVal(self.OperacionIzq.Tipo, izq) + self.ObtenerVal(self.OperacionDer.Tipo, der)
            # IZQUIERDA ES CADENA
            elif self.OperacionIzq.Tipo == TIPO.CADENA and self.OperacionDer.Tipo == TIPO.ENTERO:
                self.Tipo = TIPO.CADENA
                return self.ObtenerVal(self.OperacionIzq.Tipo, izq) + str(self.ObtenerVal(self.OperacionDer.Tipo, der))
            elif self.OperacionIzq.Tipo == TIPO.CADENA and self.OperacionDer.Tipo == TIPO.DECIMAL:
                self.Tipo = TIPO.CADENA
                return self.ObtenerVal(self.OperacionIzq.Tipo, izq) + str(self.ObtenerVal(self.OperacionDer.Tipo, der))
            elif self.OperacionIzq.Tipo == TIPO.CADENA and self.OperacionDer.Tipo == TIPO.BOOLEANO:
                self.Tipo = TIPO.CADENA
                return self.ObtenerVal(self.OperacionIzq.Tipo, izq) + str(self.ObtenerVal(self.OperacionDer.Tipo, der))
            elif self.OperacionIzq.Tipo == TIPO.CADENA and self.OperacionDer.Tipo == TIPO.CARACTER:
                self.Tipo = TIPO.CADENA
                return self.ObtenerVal(self.OperacionIzq.Tipo, izq) + self.ObtenerVal(self.OperacionDer.Tipo, der)
            elif self.OperacionIzq.Tipo == TIPO.CADENA and self.OperacionDer.Tipo == TIPO.CADENA:
                self.Tipo = TIPO.CADENA
                return self.ObtenerVal(self.OperacionIzq.Tipo, izq) + self.ObtenerVal(self.OperacionDer.Tipo, der)
            # SI NO ESTA DENTRO DE LAS POSIBLE COMBINACIONES ES UN ERROR SEMANTICO
            
            return Error("Semantico", "Tipo Erroneo de operacion para +.", self.Fila, self.Columna)
        
        #    RESTA
        
        elif self.Operador == OperadorAritmetico.MENOS: 
            # IZQUIERDA ES ENTERO
            if self.OperacionIzq.Tipo == TIPO.ENTERO and self.OperacionDer.Tipo == TIPO.ENTERO:
                self.Tipo = TIPO.ENTERO
                return self.ObtenerVal(self.OperacionIzq.Tipo, izq) - self.ObtenerVal(self.OperacionDer.Tipo, der)
            if self.OperacionIzq.Tipo == TIPO.ENTERO and self.OperacionDer.Tipo == TIPO.DECIMAL:
                self.Tipo = TIPO.DECIMAL
                return self.ObtenerVal(self.OperacionIzq.Tipo, izq) - self.ObtenerVal(self.OperacionDer.Tipo, der)
            if self.OperacionIzq.Tipo == TIPO.ENTERO and self.OperacionDer.Tipo == TIPO.BOOLEANO:
                self.Tipo = TIPO.ENTERO
                return self.ObtenerVal(self.OperacionIzq.Tipo, izq) - self.ObtenerVal(self.OperacionDer.Tipo, der)
            # IZQUIEDA ES DECIMAL
            if self.OperacionIzq.Tipo == TIPO.DECIMAL and self.OperacionDer.Tipo == TIPO.ENTERO:
                self.Tipo = TIPO.DECIMAL
                return self.ObtenerVal(self.OperacionIzq.Tipo, izq) - self.ObtenerVal(self.OperacionDer.Tipo, der)
            if self.OperacionIzq.Tipo == TIPO.DECIMAL and self.OperacionDer.Tipo == TIPO.DECIMAL:
                self.Tipo = TIPO.DECIMAL
                return self.ObtenerVal(self.OperacionIzq.Tipo, izq) - self.ObtenerVal(self.OperacionDer.Tipo, der)
            if self.OperacionIzq.Tipo == TIPO.DECIMAL and self.OperacionDer.Tipo == TIPO.BOOLEANO:
                self.Tipo = TIPO.DECIMAL
                return self.ObtenerVal(self.OperacionIzq.Tipo, izq) - self.ObtenerVal(self.OperacionDer.Tipo, der)
            # IZQUIEDA ES BOOLEANO
            if self.OperacionIzq.Tipo == TIPO.BOOLEANO and self.OperacionDer.Tipo == TIPO.ENTERO:
                self.Tipo = TIPO.ENTERO
                return self.ObtenerVal(self.OperacionIzq.Tipo, izq) - self.ObtenerVal(self.OperacionDer.Tipo, der)
            if self.OperacionIzq.Tipo == TIPO.BOOLEANO and self.OperacionDer.Tipo == TIPO.DECIMAL:
                self.Tipo = TIPO.DECIMAL
                return self.ObtenerVal(self.OperacionIzq.Tipo, izq) - self.ObtenerVal(self.OperacionDer.Tipo, der)
            # SI NO ESTA DENTRO DE LAS POSIBLE COMBINACIONES ES UN ERROR SEMANTICO
            return Error("Semantico", "Tipo Erroneo de operacion para -.", self.Fila, self.Columna)
        # MULTIPLICACION
        elif self.Operador == OperadorAritmetico.ASTERISCO: 
            # IZQUIEDA ES ENTERO
            if self.OperacionIzq.Tipo == TIPO.ENTERO and self.OperacionDer.Tipo == TIPO.ENTERO:
                self.Tipo = TIPO.ENTERO
                return self.ObtenerVal(self.OperacionIzq.Tipo, izq) * self.ObtenerVal(self.OperacionDer.Tipo, der)
            if self.OperacionIzq.Tipo == TIPO.ENTERO and self.OperacionDer.Tipo == TIPO.DECIMAL:
                self.Tipo = TIPO.DECIMAL
                return self.ObtenerVal(self.OperacionIzq.Tipo, izq) * self.ObtenerVal(self.OperacionDer.Tipo, der)
            # IZQUIEDA ES DECIMAL
            if self.OperacionIzq.Tipo == TIPO.DECIMAL and self.OperacionDer.Tipo == TIPO.ENTERO:
                self.Tipo = TIPO.DECIMAL
                return self.ObtenerVal(self.OperacionIzq.Tipo, izq) * self.ObtenerVal(self.OperacionDer.Tipo, der)
            if self.OperacionIzq.Tipo == TIPO.DECIMAL and self.OperacionDer.Tipo == TIPO.DECIMAL:
                self.Tipo = TIPO.DECIMAL
                return self.ObtenerVal(self.OperacionIzq.Tipo, izq) * self.ObtenerVal(self.OperacionDer.Tipo, der)
            
            return Error("Semantico", "Tipo Erroneo de operacion para *.", self.Fila, self.Columna)
        # DIVISION
        elif self.Operador == OperadorAritmetico.DIAGONAL: 
            if self.ObtenerVal(self.OperacionDer.Tipo, der)==0:
                return Error("Semantico", "Resultado indefinido por division entre 0, Operacion invalida", self.Fila, self.Columna)
            # IZQUIEDA ES ENTERO
            if self.OperacionIzq.Tipo == TIPO.ENTERO and self.OperacionDer.Tipo == TIPO.ENTERO:
                self.Tipo = TIPO.DECIMAL
                return self.ObtenerVal(self.OperacionIzq.Tipo, izq) / self.ObtenerVal(self.OperacionDer.Tipo, der)
            if self.OperacionIzq.Tipo == TIPO.ENTERO and self.OperacionDer.Tipo == TIPO.DECIMAL:
                self.Tipo = TIPO.DECIMAL
                return self.ObtenerVal(self.OperacionIzq.Tipo, izq) / self.ObtenerVal(self.OperacionDer.Tipo, der)
            # IZQUIEDA ES DECIMAL
            if self.OperacionIzq.Tipo == TIPO.DECIMAL and self.OperacionDer.Tipo == TIPO.ENTERO:
                self.Tipo = TIPO.DECIMAL
                return self.ObtenerVal(self.OperacionIzq.Tipo, izq) / self.ObtenerVal(self.OperacionDer.Tipo, der)
            if self.OperacionIzq.Tipo == TIPO.DECIMAL and self.OperacionDer.Tipo == TIPO.DECIMAL:
                self.Tipo = TIPO.DECIMAL
                return self.ObtenerVal(self.OperacionIzq.Tipo, izq) / self.ObtenerVal(self.OperacionDer.Tipo, der)
            
            return Error("Semantico", "Tipo Erroneo de operacion para /.", self.Fila, self.Columna)
        # POTENCIA
        elif self.Operador == OperadorAritmetico.POTENCIA:
            # IZQUIEDA ES ENTERO
            if self.OperacionIzq.Tipo == TIPO.ENTERO and self.OperacionDer.Tipo == TIPO.ENTERO:
                self.Tipo = TIPO.ENTERO
                return self.ObtenerVal(self.OperacionIzq.Tipo, izq) ** self.ObtenerVal(self.OperacionDer.Tipo, der)
            if self.OperacionIzq.Tipo == TIPO.ENTERO and self.OperacionDer.Tipo == TIPO.DECIMAL:
                self.Tipo = TIPO.DECIMAL
                return self.ObtenerVal(self.OperacionIzq.Tipo, izq) ** self.ObtenerVal(self.OperacionDer.Tipo, der)
            # IZQUIEDA ES DECIMAL
            if self.OperacionIzq.Tipo == TIPO.DECIMAL and self.OperacionDer.Tipo == TIPO.ENTERO:
                self.Tipo = TIPO.DECIMAL
                return self.ObtenerVal(self.OperacionIzq.Tipo, izq) ** self.ObtenerVal(self.OperacionDer.Tipo, der)
            if self.OperacionIzq.Tipo == TIPO.DECIMAL and self.OperacionDer.Tipo == TIPO.DECIMAL:
                self.Tipo = TIPO.DECIMAL
                return self.ObtenerVal(self.OperacionIzq.Tipo, izq) ** self.ObtenerVal(self.OperacionDer.Tipo, der)
            
            return Error("Semantico", "Tipo Erroneo de operacion para **.", self.Fila, self.Columna)
        # MODULO
        elif self.Operador == OperadorAritmetico.MODULO:
            if self.ObtenerVal(self.OperacionDer.Tipo, der)==0:
                return Error("Semantico", "Resultado indefinido por n%0, Operacion invalida", self.Fila, self.Columna)
            # IZQUIEDA ES ENTERO
            if self.OperacionIzq.Tipo == TIPO.ENTERO and self.OperacionDer.Tipo == TIPO.ENTERO:
                self.Tipo = TIPO.DECIMAL
                return self.ObtenerVal(self.OperacionIzq.Tipo, izq) % self.ObtenerVal(self.OperacionDer.Tipo, der)
            if self.OperacionIzq.Tipo == TIPO.ENTERO and self.OperacionDer.Tipo == TIPO.DECIMAL:
                self.Tipo = TIPO.DECIMAL
                return self.ObtenerVal(self.OperacionIzq.Tipo, izq) % self.ObtenerVal(self.OperacionDer.Tipo, der)
            # IZQUIEDA ES DECIMAL
            if self.OperacionIzq.Tipo == TIPO.DECIMAL and self.OperacionDer.Tipo == TIPO.ENTERO:
                self.Tipo = TIPO.DECIMAL
                return self.ObtenerVal(self.OperacionIzq.Tipo, izq) % self.ObtenerVal(self.OperacionDer.Tipo, der)
            if self.OperacionIzq.Tipo == TIPO.DECIMAL and self.OperacionDer.Tipo == TIPO.DECIMAL:
                self.Tipo = TIPO.DECIMAL
                return self.ObtenerVal(self.OperacionIzq.Tipo, izq) % self.ObtenerVal(self.OperacionDer.Tipo, der)
            
            return Error("Semantico", "Tipo Erroneo de operacion para %.", self.Fila, self.Columna)
        #   NEGACION UNIARIA
        elif self.Operador == OperadorAritmetico.UMENOS: 
            # LA NEGACION UNARIA SOLO PUEDE NEGAR NUMERO ENTEROS Y DECIMALES
            if self.OperacionIzq.Tipo == TIPO.ENTERO:
                self.Tipo = TIPO.ENTERO
                return - self.ObtenerVal(self.OperacionIzq.Tipo, izq)
            elif self.OperacionIzq.Tipo == TIPO.DECIMAL:
                self.Tipo = TIPO.DECIMAL
                return - self.ObtenerVal(self.OperacionIzq.Tipo, izq)
                # SI NO ESTA DENTRO DE LAS POSIBLE COMBINACIONES ES UN ERROR SEMANTICO
            return Error("Semantico", "Tipo Erroneo de operacion para - unario.", self.Fila, self.Columna)
        # SI EL SIMBOLO OPERADOR NO ES NINGUNO DE LOS ANTERIORES ES UN ERROR SEMANTICO
        return Error("Semantico", "Tipo de Operacion no Especificado.", self.Fila, self.Columna)

    def ObtenerVal(self, tipo, val):
        if tipo == TIPO.ENTERO:
            return int(val)
        elif tipo == TIPO.DECIMAL:
            return float(val)
        elif tipo == TIPO.BOOLEANO:
            
            return bool(val)
        return str(val) #? SI ES CADENA O CARACTER
    
    def getNodo(self):
        nodo = NodoAST("ARITMETICA")
        if self.OperacionDer != None:
            nodo.agregarHijoNodo(self.OperacionIzq.getNodo())
            if self.Operador==OperadorAritmetico.MAS:
                nodo.agregarHijo("+")
            elif self.Operador==OperadorAritmetico.MENOS:
                nodo.agregarHijo("-")
            elif self.Operador==OperadorAritmetico.ASTERISCO:
                nodo.agregarHijo("*")
            elif self.Operador==OperadorAritmetico.DIAGONAL:
                nodo.agregarHijo("/")
            elif self.Operador==OperadorAritmetico.POTENCIA:
                nodo.agregarHijo("**")
            elif self.Operador==OperadorAritmetico.MODULO:
                nodo.agregarHijo("%")
            nodo.agregarHijoNodo(self.OperacionDer.getNodo())
        else:
            nodo.agregarHijo("-")
            nodo.agregarHijoNodo(self.OperacionIzq.getNodo())
        
        return nodo