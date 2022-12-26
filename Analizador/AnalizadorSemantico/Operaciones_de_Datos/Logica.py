from ..Clases_Abstractas import Operacion,NodoAST
from ...Interprete.Tabla_de_Simbolos import Error,TIPO,OperadorLogico

class Logica(Operacion):
    """
    !    CLASE DONDE SE OPERAN LOS OPERADORES LOGICOS AND, OR Y NOT
    """
    def __init__(self, Operador, OperacionIzq, OperacionDer, Fila, Columna):
        self.Operador     = Operador            # &&, ||, !
        self.OperacionIzq = OperacionIzq    # OPERACION DE DATOS, DEBE SER RESULTADO BOOLEANO
        self.OperacionDer = OperacionDer    # OPERACION DE DATOS, DEBE SER RESULTADO BOOLEANO
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
        # OPERADOR LOGICO AND
        if self.Operador == OperadorLogico.AND:
            if self.OperacionIzq.Tipo == TIPO.BOOLEANO and self.OperacionDer.Tipo == TIPO.BOOLEANO:
                return self.obtenerVal(self.OperacionIzq.Tipo, izq) and self.obtenerVal(self.OperacionDer.Tipo, der)
            return Error("Semantico", "Tipo Erroneo de operacion para &&.", self.Fila, self.Columna)
        # OPERADOR LOGICO OR
        elif self.Operador == OperadorLogico.OR:
            if self.OperacionIzq.Tipo == TIPO.BOOLEANO and self.OperacionDer.Tipo == TIPO.BOOLEANO:
                return self.obtenerVal(self.OperacionIzq.Tipo, izq) or self.obtenerVal(self.OperacionDer.Tipo, der)
            return Error("Semantico", "Tipo Erroneo de operacion para ||.", self.Fila, self.Columna)
        # OPERADOR LOGICO NOT
        elif self.Operador == OperadorLogico.NOT:
            if self.OperacionIzq.Tipo == TIPO.BOOLEANO:
                return not self.obtenerVal(self.OperacionIzq.Tipo, izq)
            return Error("Semantico", "Tipo Erroneo de operacion para !.", self.Fila, self.Columna)
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
        nodo = NodoAST("LOGICA")
        if self.OperacionDer != None:
            nodo.agregarHijoNodo(self.OperacionIzq.getNodo())
            if self.Operador==OperadorLogico.AND:
                nodo.agregarHijo("&&")
            elif self.Operador==OperadorLogico.OR:
                nodo.agregarHijo("||")
            
            nodo.agregarHijoNodo(self.OperacionDer.getNodo())
        else:
            nodo.agregarHijo("!")
            nodo.agregarHijoNodo(self.OperacionIzq.getNodo())
        
        return nodo
