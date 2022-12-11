import ply.lex as lex
import ply.yacc as yacc
import sys

#Palabras reservadas

palabras_reservadas={
    "bool":"BOOL",
    "str":"STRING",
    "int": "INT",
    "float": "FLOAT",
    "True": "TRUE",
    "False": "FALSE",
    "if": "IF",
    "elif": "ELSEIF",
    "else": "ELSE",
    "or" : "OR",
    "and" : "AND",
    "not" : "NOT",
    "while": "WHILE",
    "for": "FOR",
    "in": "IN",
    "continue": "CONTINUE",
    "return": "RETURN",
    "break": "BREAK",
    "end": "END",
    "None": "NONE",
    "println" : "PRINTLN",
    "print": "PRINT",
    "upper": "UPPER",
    "lower": "LOWER",
    "len": "LEN",
    "def": "DEF",
}

#Simbolos tokens

simbolos_tokens = {
    "ID",
    "CADENA",
    "ENTERO",
    "DECIMAL",
    "PUNTO",
    "COMA",
    "DOSPUNTOS",
    "NUEVALINEA",
    "PARENTESIS_IZQ",
    "PARENTESIS_DER",
    "CORCHETE_IZQ",
    "CORCHETE_DER",
    "LLAVE_IZQ",
    "LLAVE_DER",
    "MAS",
    "MENOS",
    "POR",
    "DIVISION",
    "IGUAL",
    "MODULO"
    "POTENCIA",
    "MENOR_QUE",
    "MAYOR_QUE",
    "MENOR_IGUAL_QUE",
    "MAYOR_IGUAL_QUE",
    "IGUAL_QUE",
    "DIFERENTE_QUE"
} + list(palabras_reservadas.values())

t_PUNTO = r'\.'
t_COMA = r','
t_DOSPUNTOS = r':'
t_NUEVALINEA = r'\n'
t_PARENTESIS_IZQ = r'\('
t_PARENTESIS_DER = r'\)'
t_CORCHETE_IZQ = r'\['
t_CORCHETE_DER = r']'
t_LLAVE_IZQ = r'{'
t_LLAVE_DER = r'}'
t_MAS = r'\+'
t_MENOS = r'-'
t_POR = r'\*'
t_DIVISION = r'/'
t_IGUAL = r'='
t_MODULO = r'%'
t_POTENCIA = r'\^'
t_MENOR_QUE = r'<'
t_MAYOR_QUE = r'>'
t_MENOR_IGUAL_QUE = r'<='
t_MAYOR_IGUAL_QUE = r'>='
t_IGUAL_QUE= r'=='
t_DIFERENTE_QUE = r'!='

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    # Check for reserved words
    t.type = palabras_reservadas.get(t.value, 'ID')
    return t

def t_CADENA(t):
    r'\".*?\"'
    # Se quitan comillas - 1
    t.value = t.value[1:-1] 
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

# Comentario de múltiples líneas #= .. =#

def t_COMENTARIO_MULTILINEA(t):
    r'\#=(.|\n)*?=\#'
    t.lexer.lineno += t.value.count('\n')

# Comentario simple # ...

def t_COMENTARIO_SIMPLE(t):
    r'\#.*\n'
    t.lexer.lineno += 1

# Caracteres ignorados
t_ignore = " \t"

def t_error(t):
    print("Error Léxico:")
    t.lexer.skip(1)


lexer = lex.lex()

# Precedencia

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'IGUAL_QUE', 'DIFERENTE_QUE'),
    ('left', 'MAYOR_QUE', 'MENOR_QUE', 'MAYOR_IGUAL_QUE', 'MENOR_IGUAL_QUE'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVISON', 'MODULO'),
    ('left', 'POTENCIA'),
    ('right', 'UMENOS')
)

def p_inicial(t):
    '''inicial            : instrucciones'''
    # t[0] = t[1]

def p_instrucciones_lista(t):
    '''instrucciones    : instrucciones instruccion
                        | instruccion'''
    #if (len(t) != 2):
    #    t[1].append(t[2])
    #    t[0] = t[1]
    #else:
    #    t[0] = [t[1]]
    
def p_instruccion(t):
    '''instruccion      : print_instr LINEANUEVA
                        | println_instr LINEANUEVA
                        | asignacion_instr LINEANUEVA
                        | asignacion_arreglo_instr LINEANUEVA
                        | definicion_asignacion_instr LINEANUEVA
                        | call_function LINEANUEVA
                        | declare_function LINEANUEVA
                        | return_state LINEANUEVA
                        | break_state LINEANUEVA
                        | continue_state LINEANUEVA
                        | if_state LINEANUEVA
                        | while_state LINEANUEVA
                        | for_state LINEANUEVA
                        | nativas LINEANUEVA
                        | expression LINEANUEVA'''
    #t[0] = t[1]