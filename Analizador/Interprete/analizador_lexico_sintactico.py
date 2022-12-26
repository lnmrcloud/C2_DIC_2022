import re
from tkinter.constants import END, FALSE, TRUE
from ..ply import lex,yacc

#? TABLA DE SIMBOLOS

from .Tabla_de_Simbolos import Error, Tipo, OperadorAritmetico,OperadorRelacional,OperadorLogico,arbol,tabla_simbolos

#? MANEJO DE DATOS

from ..AnalizadorSemantico.Operaciones_de_Datos import Aritmetica,Asignacion,Declaracion,Identificador,IncrementoDecremento,Logica,Primitivos,Relacional,Casteo,DeclaracionArregloTipo1,Arreglo,DeclaracionArregloTipo2,AsignacionArreglo,ObtenerValorArreglo