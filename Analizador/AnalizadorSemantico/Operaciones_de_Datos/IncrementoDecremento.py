from ..Clases_Abstractas import Operacion,NodoAST
from ...Interprete.Tabla_de_Simbolos import Error,TIPO,Simbolo

class IncrementoDecremento(Operacion):
    
    #!    CLASE ENCARGADA DE EJECUTAR EL INCREMENTO Y DECREMENTO DE UNA VARIABLE, Y DEVOLVER EL VALOR DE ESTA
    
    def __init__(self, Identificador, Fila, Comlumna,Solo,INCDEC):
        self.Identificador = Identificador  #*RECIBE UN OBJETO IDENTIFICADOR
        self.Fila          = Fila
        self.Comlumna      = Comlumna
        self.Solo          = Solo          #* SI SOLO ES TRUE ES ANTES DEL IGUAL, FALSE DESPUES DEL IGUAL
        self.INCDEC        = INCDEC      #* TRUE=INCREMENTO, FALSE=DECREMENTO
        self.Tipo          = None

    def Interpretar(self, Arbol, TablaSimbolos):
            ID=self.Identificador.Interpretar(Arbol,TablaSimbolos)
            if isinstance(ID,Error):return ID
            if ID==None: return Error("Semantico","Operacion no valida, asignacion sin valor",self.Fila,self.Columna)
            if isinstance(ID,list): return Error("Semantico","Operacion invalida para arreglo",self.Fila,self.Columna)
            if self.Identificador.Tipo== TIPO.ENTERO or self.Identificador.Tipo==TIPO.DECIMAL:
                if self.INCDEC:
                    ID=ID+1
                else:
                    ID=ID-1
                simbolo = Simbolo(self.Identificador.Identificador, self.Identificador.Tipo,False, self.Fila, self.Comlumna,ID)
                self.Tipo=self.Identificador.Tipo
                result = TablaSimbolos.ActualizarVariable(simbolo)
                if isinstance(result, Error): return result
                if self.Solo:
                    return None
                else:
                    return ID
            return Error("Semantico","Identificador "+self.Identificador.Identificador+" no es INT O DOUBLE",self.Fila,self.Comlumna)
        


    def getNodo(self):
        if self.INCDEC==True:
            nodo=NodoAST("INCREMENTO")
            nodo.agregarHijoNodo(self.Identificador.getNodo())
            nodo.agregarHijo("++")
            return nodo
        else:
            nodo=NodoAST("DECREMENTO")
            nodo.agregarHijo(self.Identificador.getNodo())
            nodo.agregarHijo("--")
            return nodo
        