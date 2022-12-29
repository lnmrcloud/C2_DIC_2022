from enum import Enum

class TIPO(Enum):
    ENTERO   = 1
    FLOAT  = 2
    BOOLEANO = 3
    CARACTER = 4
    CADENA   = 5
    NULL     = 6
    ARREGLO  = 7

class OperadorAritmetico(Enum):
    MAS       = 1
    MENOS     = 2
    ASTERISCO = 3
    DIAGONAL  = 4
    POTENCIA  = 5
    MODULO    = 6
    UMENOS    = 7

class OperadorRelacional(Enum):
    MENORQUE       = 1
    MAYORQUE       = 2
    MENORIGUAL     = 3
    MAYORIGUAL     = 4
    IGUALACION     = 5
    DIFERENCIACION = 6

class OperadorLogico(Enum):
    NOT = 1
    AND = 2
    OR  = 3