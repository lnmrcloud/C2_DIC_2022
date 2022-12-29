from . import TIPO,Error
import sys

sys.setrecursionlimit(3000)
class TablaSimbolos:
    """
    *    HAY UNA TABLA DE SIMBOLOS POR ENTORNO
    """
    def __init__(self, EntornoAnterior=None, NombreEntorno=""):
        self.Tabla_Variables = {}               #? TABLA DE VARIABLES DEL ENTORNO
        self.EntornoAnterior = EntornoAnterior  #? PUNTERO QUE ALMACENA EL ENTORNO ANTERIOR O ENTORNO PADRE
        self.Tabla_Funciones = {}               #? TABLA DE FUNCIONES DENTRO DEL ENTRONO, SOLO TENDRA VALORES EN EL ENTRONO GROBAL
        self.NombreEntorno   = NombreEntorno
        self.Hijos           = None
    
    def SetVariable(self, simbolo):
        """
        *    AGREGA UNA VARIABLE A LA TABLA DEL ENTRONOACTUAL      
        """
        if simbolo.id.lower() in self.Tabla_Variables :
            #!? SI LA VARIABLE YA ESTA DECLARADA EN EL ENTORNO ESTA SERA UN ERROR SEMANTICO
            #! RETORNAREMOS EL STRING DEL ERROR
            return Error("Semantico", "Variable " + simbolo.id + " ya existe", simbolo.Fila, simbolo.Columna)
        else:
            #! SI NO, ESTA SE AGREGARA CON SU ID A LA TABLA DEL ENTORNO ACTUAL
            self.Tabla_Variables[simbolo.id.lower()] = simbolo
            return None

    def GetVariable(self, id):            
        """
        *    RETORNA EL SIMBOLO DE LA VARIABLE CON ID ENVIADO
        """
        EntornoActual = self
        #? RECORREMOS DEL ENTORNO ACTUAL HASTA LLEGAR AL ENTORNO GLOBAL
        while EntornoActual!= None:
            if id in EntornoActual.Tabla_Variables :
                # RETORNA EL SIMBOLO SI ENCUENTRA LA VARIABLE EN LA TABLA 
                return EntornoActual.Tabla_Variables[id]           
            else:
                EntornoActual = EntornoActual.EntornoAnterior
        # SI NO EXISTE RETORNA NADA
        return None

    def SetFuncion(self, Funcion):
        """
        *    AGREGA UNA VARIABLE A LA TABLA DEL ENTRONOACTUAL      
        """
        if Funcion.Identificador.lower() in self.Tabla_Funciones :
            # SI LA VARIABLE YA ESTA DECLARADA EN EL ENTORNO ESTA SERA UN ERROR SEMANTICO
            # RETORNAREMOS EL STRING DEL ERROR
            return Error("Semantico", "Variable " + Funcion.Identificador + " ya existe", Funcion.Fila, Funcion.Columna)
        else:
            # SI NO, ESTA SE AGREGARA CON SU ID A LA TABLA DEL ENTORNO ACTUAL
            self.Tabla_Funciones[Funcion.Identificador.lower()] = Funcion
            return None

    def GetFuncion(self, id):            
        """
        *    RETORNA EL SIMBOLO DE LA VARIABLE CON ID ENVIADO
        """
        EntornoActual = self
        #! RECORREMOS DEL ENTORNO ACTUAL HASTA LLEGAR AL ENTORNO GLOBAL
        while EntornoActual!= None:
            if id in EntornoActual.Tabla_Funciones :
                # RETORNA EL SIMBOLO SI ENCUENTRA LA VARIABLE EN LA TABLA 
                return EntornoActual.Tabla_Funciones[id]           
            else:
                EntornoActual = EntornoActual.EntornoAnterior
        # SI NO EXISTE RETORNA NADA
        return None

    def ActualizarVariable(self, simbolo):
        """
            ACTUALIZA LOS ATRIBUTOS DEL SIMBOLO ALMACENADO
        """
        EntronoActual = self
        # RECORREMOS DEL ENTORNO ACTUAL HASTA LLEGAR AL ENTORNO GLOBAL
        while EntronoActual != None:
            if simbolo.id in EntronoActual.Tabla_Variables :
                # SI LA VARIABLE ESTA EN EL ENTORNO ACTUAL VERIFICAMOS QUE LA NUEVA ASIGNACION SEA DEL MISMO TIPO 
                if EntronoActual.Tabla_Variables[simbolo.id].getTipo()==TIPO.NULL:
                    EntronoActual.Tabla_Variables[simbolo.id].setValor(simbolo.getValor())
                    EntronoActual.Tabla_Variables[simbolo.id].setTipo(simbolo.getTipo())
                    return None 
                elif EntronoActual.Tabla_Variables[simbolo.id].getTipo()!=TIPO.NULL and simbolo.getTipo()==TIPO.NULL:
                    EntronoActual.Tabla_Variables[simbolo.id].setValor(simbolo.getValor())
                    EntronoActual.Tabla_Variables[simbolo.id].setTipo(simbolo.getTipo())
                    return None 
                elif EntronoActual.Tabla_Variables[simbolo.id].getTipo() == simbolo.getTipo():
                    # SI SON DEL MISMO TIPO SE ACTUALIZA LOS ATRIBUTOS DE LA VARIABLE
                    EntronoActual.Tabla_Variables[simbolo.id].setValor(simbolo.getValor())
                    EntronoActual.Tabla_Variables[simbolo.id].setTipo(simbolo.getTipo())
                    return None 
                # SI EL TIPO DE LA NUEVA ASIGNACION NO ES IGUAL, RETORNARA UN ERROR SEMANTICO
                return Error("Semantico", "Tipo de dato Diferente en Asignacion", simbolo.getFila(), simbolo.getColumna())
            else:
                EntronoActual = EntronoActual.EntornoAnterior
        # SI NO EXISTE LA VARIABLE QUE SE DESEA ACTUALIZAR, RETORNARA UN ERROR SEMANTICO
        return Error("Semantico", "Variable No encontrada en Asignacion", simbolo.getFila(), simbolo.getColumna())
    
    def AgregarHijo(self,Entorno):
        if self.Hijos==None:
            self.Hijos=[]
        self.Hijos.append(Entorno)
        
    def GetDot(self):
        dot=""
        for variable in self.Tabla_Variables:
            dot+="<TR>\n"
            dot+="<TD border=\"3\"  bgcolor=\"/rdylgn11/4:/rdylgn11/5\">\""+str(self.Tabla_Variables[variable].getID())+"\"</TD>\n"
            dot+="<TD border=\"3\"  bgcolor=\"/rdylgn11/4:/rdylgn11/5\">\"Variable\"</TD>\n"
            dot+="<TD border=\"3\"  bgcolor=\"/rdylgn11/4:/rdylgn11/5\">\""+str(self.Tabla_Variables[variable].getTipo())+"\"</TD>\n"
            dot+="<TD border=\"3\"  bgcolor=\"/rdylgn11/4:/rdylgn11/5\">\""+self.NombreEntorno+"\"</TD>\n"
            dot+="<TD border=\"3\"  bgcolor=\"/rdylgn11/4:/rdylgn11/5\">\""+str(self.Tabla_Variables[variable].getValor())+"\"</TD>\n"
            dot+="<TD border=\"3\"  bgcolor=\"/rdylgn11/4:/rdylgn11/5\">\""+str(self.Tabla_Variables[variable].getFila())+"\"</TD>\n"
            dot+="<TD border=\"3\"  bgcolor=\"/rdylgn11/4:/rdylgn11/5\">\""+str(self.Tabla_Variables[variable].getColumna())+"\"</TD>\n"
            dot+="</TR>\n"
        
        for funcion in self.Tabla_Funciones:
            dot+="<TR>\n"
            dot+="<TD border=\"3\"  bgcolor=\"/rdylgn11/4:/rdylgn11/5\">\""+str(self.Tabla_Funciones[funcion].Identificador)+"\"</TD>\n"
            dot+="<TD border=\"3\"  bgcolor=\"/rdylgn11/4:/rdylgn11/5\">\"Funcion\"</TD>\n"
            dot+="<TD border=\"3\"  bgcolor=\"/rdylgn11/4:/rdylgn11/5\">\"--\"</TD>\n"
            dot+="<TD border=\"3\"  bgcolor=\"/rdylgn11/4:/rdylgn11/5\">\""+self.NombreEntorno+"\"</TD>\n"
            dot+="<TD border=\"3\"  bgcolor=\"/rdylgn11/4:/rdylgn11/5\">\"--\"</TD>\n"
            dot+="<TD border=\"3\"  bgcolor=\"/rdylgn11/4:/rdylgn11/5\">\""+str(self.Tabla_Funciones[funcion].Fila)+"\"</TD>\n"
            dot+="<TD border=\"3\"  bgcolor=\"/rdylgn11/4:/rdylgn11/5\">\""+str(self.Tabla_Funciones[funcion].Columna)+"\"</TD>\n"
            dot+="</TR>\n"
        
        return dot
            
