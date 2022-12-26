from ...Clases_Abstractas import Operacion,NodoAST
from ..De_Transferencia import Break,Continue,Return
from ....Interprete.Tabla_de_Simbolos import Error,TablaSimbolos,TIPO
from ...Operaciones_de_Datos.Asignacion import Asignacion

class For(Operacion):
    def __init__(self,Variable, Condicion,Asignacion, Instrucciones, Fila, Columna):
        self.Variable      = Variable
        self.Condicion     = Condicion
        self.Asignacion    = Asignacion
        self.Instrucciones = Instrucciones
        self.Fila          = Fila
        self.Columna       = Columna

    def Interpretar(self, Arbol, TablaSimbolo):
        # VERIFICAMOS SI ES ASIGNACION
        if isinstance(self.Variable,Asignacion):
            valor =self.Variable.Interpretar(Arbol,TablaSimbolo)
            if isinstance(valor,Error): return valor
        # SI NO ES ASIGNACION ENTONCES ES UNA DECLARACION EN UN NUEVO ENTORNO
        nuevaTabla = TablaSimbolos(TablaSimbolo,"FOR")       #NUEVO ENTORNO        
        TablaSimbolo.AgregarHijo(nuevaTabla)
        valor=self.Variable.Interpretar(Arbol,nuevaTabla)
        if isinstance(valor,Error): return valor

        while True:
            
            Condicion = self.Condicion.Interpretar(Arbol, nuevaTabla)
            if isinstance(Condicion, Error): return Condicion

            if self.Condicion.Tipo == TIPO.BOOLEANO:
                if bool(Condicion) == True:   # VERIFICA SI ES VERDADERA LA Condicion
                    nuevaTabla2 = TablaSimbolos(nuevaTabla,"FOR") # SE CREA UN NUEVO ENTRNO CADA VEZ QUE HAGA UNA ITERACION DENTRO DEL FOR
                    nuevaTabla.AgregarHijo(nuevaTabla2)
                    for instruccion in self.Instrucciones:
                        result = instruccion.Interpretar(Arbol, nuevaTabla2) #EJECUTA INSTRUCCION ADENTRO DEL IF
                        if isinstance(result, Error) :
                            Arbol.getExcepciones().append(result)
                            Arbol.updateConsola(result.toString())
                        if isinstance(result, Break): return None
                        if isinstance(result, Return): return result
                        if isinstance(result, Continue): break
                    # REALIZAMOS LA ASIGNACION
                    asignacion =self.Asignacion.Interpretar(Arbol,nuevaTabla)
                    if isinstance(asignacion,Error): return asignacion
                else:
                    break
            else:
                return Error("Semantico", "Tipo de dato no booleano en IF.", self.Fila, self.Columna)
    
    def getNodo(self):
        nodo=NodoAST("FOR")
        nodo.agregarHijo("For")
        nodo.agregarHijoNodo(self.Variable.getNodo())
        nodo.agregarHijoNodo(self.Condicion.getNodo())
        nodo.agregarHijoNodo(self.Asignacion.getNodo())
        instrucciones=NodoAST("INSTRUCCIONES")
        for instruccion in self.Instrucciones:
            instrucciones.agregarHijoNodo(instruccion.getNodo())
        nodo.agregarHijoNodo(instrucciones)
        return nodo