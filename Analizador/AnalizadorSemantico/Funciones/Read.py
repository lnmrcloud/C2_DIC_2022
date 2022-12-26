from tkinter.messagebox import OK
from ..Clases_Abstractas import Operacion,NodoAST
from ...Interprete.Tabla_de_Simbolos import TIPO,Error
from ... import VentanaPrincipal
from tkinter import  simpledialog
from tkinter import *


class Read(Operacion):
    def __init__(self, Fila, Columna):
        self.Fila = Fila
        self.Columna = Columna
        self.Tipo = TIPO.CADENA

    def Interpretar(self, Arbol, TablaSimbolos):
        
        # INSERTAMOS EL NUEVO MENSAJE EN LA CONSOLA
        VentanaPrincipal.TextArea2.insert(END, Arbol.getConsola())
        #! MOVEMOS EL CURSOR AL FINAL DE LA CONSOLA
        VentanaPrincipal.TextArea2.mark_set(INSERT, END)
        VentanaPrincipal.TextArea2.see(INSERT)
        
        #? LIMPIAMOS LA CONSOLA LUEGO DE IMPRIMIRLA
        Arbol.setConsola("")
        
        return self.popup() # OBTENERME EL VALOR INGRESADO
        
    
    def popup(self):
        cadena = simpledialog.askstring("Read()","Ingrese el texto deseado.", initialvalue="")
        if cadena == None:
            return Error("Semantico","Valor no ingresado en Read()",self.Fila,self.Columna)
        return cadena
    
    def getNodo(self):
        nodo = NodoAST("READ()")
        return nodo