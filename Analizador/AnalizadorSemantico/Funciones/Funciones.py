from ..Clases_Abstractas import Operacion,NodoAST
from ..Sentencias.De_Transferencia import Continue,Break,Return
from ...Interprete.Tabla_de_Simbolos import Error,TablaSimbolos
from ..Operaciones_de_Datos import Declaracion,Primitivos,DeclaracionArregloTipo2
import sys
sys.setrecursionlimit(2000)
class Funcion(Operacion):
    
    def __init__(self, Identificador, Parametros , Instrucciones, Fila, Columna):
        self.Identificador       = Identificador
        self.Parametros          = Parametros       # Parametros
        self.Instrucciones       = Instrucciones
        self.ParametrosRecibidos = []               # primitivos, aritmeticas, llamadas, logicas, Relacional
        self.Fila                = Fila
        self.Columna             = Columna

    def Interpretar(self, Arbol, TablaSimbolo):
        # LIMPIAMOS LA VARIABLE TIPO Y VALOR
        
        
        nuevaTabla = TablaSimbolos(TablaSimbolo,"Funcion "+str(self.Identificador))       #NUEVO ENTORNO
        #!? SECCION PARA NO GUARDAR TABLAS EN RECURSIVIDAD
        aux=TablaSimbolo
        seguardaHijo=True
        while aux.EntornoAnterior!=None:
            if aux.NombreEntorno != nuevaTabla.NombreEntorno:
                aux=aux.EntornoAnterior
            else:
                seguardaHijo=False
                break

        if seguardaHijo:
            TablaSimbolo.AgregarHijo(nuevaTabla)
        #!? FIN DE SECCION
        i=0
        while i<len(self.Parametros) :
            valor=self.ParametrosRecibidos[i].Interpretar(Arbol,TablaSimbolo)
            if isinstance(valor,Error): return valor
            
            param=self.Parametros[i].Interpretar(Arbol,TablaSimbolo)
            if isinstance(param,Error): return param
            
            if self.Parametros[i].Tipo != self.ParametrosRecibidos[i].Tipo:
                return Error("Semantico", "Parametro "+valor+" enviado de diferente tipo",self.ParametrosRecibidos[i].Fila,self.ParametrosRecibidos[i].Columna)
            
            if self.Parametros[i].Arreglo:
                if not isinstance(valor,list): return Error("Semantico", "Parametro "+valor+" enviado de no es un arreglo",self.ParametrosRecibidos[i].Fila,self.ParametrosRecibidos[i].Columna)
                declarar=DeclaracionArregloTipo2(self.Parametros[i].Tipo,self.Parametros[i].Dimensiones,self.Parametros[i].Id,self.ParametrosRecibidos[i],self.ParametrosRecibidos[i].Fila,self.ParametrosRecibidos[i].Columna)
                decla=declarar.Interpretar(Arbol,nuevaTabla)
                if isinstance(decla,Error): return decla
            else:
                primitivovalor=Primitivos(self.ParametrosRecibidos[i].Tipo,valor,self.Fila,self.Columna)
                
                declarar= Declaracion(self.Parametros[i].Id,self.Parametros[i].Fila,self.Parametros[i].Columna,primitivovalor)
                decla=declarar.Interpretar(Arbol,nuevaTabla)
                if isinstance(decla,Error): return decla
            i+=1
        for instruccion in self.Instrucciones:
            result = instruccion.Interpretar(Arbol, nuevaTabla) #EJECUTA INSTRUCCION ADENTRO DEL IF
            if isinstance(result, Error) :
                Arbol.getExcepciones().append(result)
                Arbol.updateConsola(result.toString())
            if isinstance(result, Return): return result
            
            if isinstance(result, Break): 
                BreakError=Error("Semantico", "Break fuera de ciclo",self.Fila,self.Columna)
                Arbol.getExcepciones().append(BreakError)
                Arbol.updateConsola(BreakError.toString())
            if isinstance(result, Continue): 
                CotinueError=Error("Semantico", "Continue fuera de ciclo",self.Fila,self.Columna)
                Arbol.getExcepciones().append(CotinueError)
                Arbol.updateConsola(CotinueError.toString())
        # LIMPIAMOS LA VARIABLE DE PARAMETROS RECIBIDOS
        
        return None
                
    def getNodo(self):
        nodo=NodoAST("FUNCION")
        nodo.agregarHijo(str(self.Identificador))
        if len(self.Parametros)!=0:
            parametros=NodoAST("PARAMETROS")
            for parametro in self.Parametros:
                parametros.agregarHijoNodo(parametro.getNodo())
            nodo.agregarHijoNodo(parametros)
        instrucciones=NodoAST("INSTRUCCIONES")
        for instruccion in self.Instrucciones:
            instrucciones.agregarHijoNodo(instruccion.getNodo())
        nodo.agregarHijoNodo(instrucciones)
        return nodo