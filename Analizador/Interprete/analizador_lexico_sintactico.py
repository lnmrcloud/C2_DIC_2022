import re
from tkinter.constants import END, FALSE, TRUE
from ..ply import lex,yacc

#? TABLA DE SIMBOLOS

from .Tabla_de_Simbolos import Error, TIPO, OperadorAritmetico, OperadorRelacional ,OperadorLogico,Arbol, TablaSimbolos

#? MANEJO DE DATOS

from ..AnalizadorSemantico.Operaciones_de_Datos import Aritmetica,Asignacion,Declaracion,Identificador,IncrementoDecremento,Logica,Primitivos,Relacional,Casteo,DeclaracionArregloTipo1,Arreglo,DeclaracionArregloTipo2,AsignacionArreglo,ObtenerValorArreglo

#? FUNCIONES
from ..AnalizadorSemantico.Funciones import Print,Main,Funcion,Llamada,Parametro,ToUpper,ToLower,Read

#? FUNCIONES NATIVAS
from ..AnalizadorSemantico.Funciones_Nativas import Length,Round,Truncate,TypeOf

#* SENTENCIAS
#?   CICLICAS
from ..AnalizadorSemantico.Sentencias.Ciclicas import While,For

#?   DE CONTROL
from ..AnalizadorSemantico.Sentencias.De_Control import If,Switch,Case

#?   DE TRANSFERENCIA
from ..AnalizadorSemantico.Sentencias.De_Transferencia import Break,Continue,Return

#? De Reportes
from ..Reportes import RepoorteAST,ReporteErrores,RepoorteTablaSimbolos


class LexicoSintactico(object):

    #Palabras reservadas
    errores = []
    input   = ''
    reservadas = {
        "bool" :"BOOL",
        "str" :"STRING",
        "int" : "INT",
        "float" : "FLOAT",
        "true" : "TRUE",
        "false" : "FALSE",
        "if" : "IF",
        "elif" : "ELSEIF",
        "else" : "ELSE",
        "or" : "OR",
        "and" : "AND",
        "not" : "NOT",
        "while" : "WHILE",
        "for" : "FOR",
        "in" : "IN",
        "continue" : "CONTINUE",
        "return" : "RETURN",
        "break" : "BREAK",
        "end" : "END",
        "None" : "NONE",
        "println" : "PRINTLN",
        "print" : "PRINT",
        "upper" : "UPPER",
        "lower" : "LOWER",
        "len" : "LEN",
        "def" : "DEF"
    }

    #Simbolos tokens

    tokens = [
        "ID",
        "LINEANUEVA",
        "CADENA",
        "ENTERO",
        "DECIMAL",
        "PUNTO",
        "COMA",
        "DOSPUNTOS",
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
        "MODULO",
        "POTENCIA",
        "MENOR_QUE",
        "MAYOR_QUE",
        "MENOR_IGUAL_QUE",
        "MAYOR_IGUAL_QUE",
        "IGUAL_QUE",
        "DIFERENTE_QUE",
        "COMILLAS"
    ] + list(reservadas.values())

    #tokens

    t_PUNTO = r'\.'
    t_COMA = r','
    t_DOSPUNTOS = r':'
    t_LINEANUEVA = r'\n'
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
    t_COMILLAS = r'\"'

    def t_ID(self,t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        # Check for reserved words
        t.type=self.reservadas.get(t.value.lower(),'ID')
        return t

    def t_CADENA(self,t):
        #r'\".*?\"'
        r'\"(\\[nN]|\\\\|\\\*|\\[tT]|\\\'|\\\"|[^\\\"\'])*?\"'
        # Se quitan comillas - 1
        t.value = t.value[1:-1]
        #t.value = t.value 
        return t

    def t_ENTERO(self,t):
        r'\d+'
        try:
            t.value = int(t.value)
        except ValueError:
            print("Integer value too large %d", t.value)
            t.value = 0
        return t

    def t_DECIMAL(self,t):
        r'\d+\.\d+'
        try:
            t.value = float(t.value)
        except ValueError:
            print("Float value too large %d", t.value)
            t.value = 0
        return t

    # Comentario de múltiples líneas #= .. =#

    def t_COMENTARIO_MULTILINEA(self,t):
        r'\#=(.|\n)*?=\#'
        t.lexer.lineno += t.value.count('\n')

    # Comentario simple # ...

    def t_COMENTARIO_SIMPLE(self,t):
        r'\#.*\n'
        t.lexer.lineno += 1

    # Caracteres ignorados
    t_ignore = " \t"

    def t_error(self,t): #LEXICOS
        self.errores.append(Error("Lexico","Error lexico en "+t.value[0],t.lexer.lineno,self.find_column(self.input,t)))
        
        t.lexer.skip(1)    
    
    # Precedencia

    precedence = (
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'IGUAL_QUE', 'DIFERENTE_QUE'),
        ('left', 'MAYOR_QUE', 'MENOR_QUE', 'MAYOR_IGUAL_QUE', 'MENOR_IGUAL_QUE'),
        ('left', 'MAS', 'MENOS'),
        ('left', 'POR', 'DIVISION', 'MODULO'),
        ('left', 'POTENCIA'),
        ('right', 'UMENOS')
    )

    # Definicion de la gramatica

    def p_init(self,t):
        '''init            : instrucciones'''
        t[0]=t[1]

    def p_instrucciones_lista(self,t):
        '''instrucciones    : instrucciones instruccion
                            | instruccion'''
        if (len(t) != 2):
            t[1].append(t[2])
            t[0] = t[1]
        else:
            t[0] = [t[1]]

    def p_instruccion(self,t):
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
        t[0] = t[1]

    def p_expression(self,t):
        '''expression       : MENOS expression %prec UMENOS
                            | NOT expression %prec UMENOS
                            | expression MAS expression
                            | expression MENOS expression
                            | expression POR expression
                            | expression DIVISION expression
                            | expression POTENCIA expression
                            | expression MODULO expression
                            | expression MAYOR_QUE expression
                            | expression MENOR_QUE expression
                            | expression MENOR_IGUAL_QUE expression
                            | expression MAYOR_IGUAL_QUE expression
                            | expression IGUAL_QUE expression
                            | expression DIFERENTE_QUE expression
                            | expression OR expression
                            | expression AND expression
                            | final_expression'''
        if(len(t)==2):
            t[0] = t[1]
        elif (len(t)==3):
            if(t[1] == '-'):
                #t[0] = Arithmetic(Literal(0,Type.INT, t.lineno(1), t.lexpos(0)),t[2],ArithmeticOption.MINUS,t.lineno(1), t.lexpos(0))
                t[0] = Aritmetica(OperadorAritmetico.UMENOS, t[2],None, t.lineno(1), self.find_column(self.input, t.slice[1]))
            else:
                #t[0] = Logical(t[2],Literal(True, Type.BOOL, t.lineno(1), t.lexpos(0)),LogicOption.NOT, t.lineno(1), t.lexpos(0))
                t[0] = Logica(OperadorLogico.NOT, t[2],None, t.lineno(1), self.find_column(self.input, t.slice[1]))
        else:
            if t[2] == "+":
                #t[0] = Arithmetic(t[1], t[3], ArithmeticOption.PLUS,t.lineno(1), t.lexpos(0))
                t[0] = Aritmetica(OperadorAritmetico.MAS, t[1],t[3], t.lineno(2), self.find_column(self.input, t.slice[2]))
            elif t[2] == "-":
                #t[0] = Arithmetic(t[1], t[3], ArithmeticOption.MINUS, t.lineno(1), t.lexpos(0))
                t[0] = Aritmetica(OperadorAritmetico.MENOS, t[1],t[3], t.lineno(2), self.find_column(self.input, t.slice[2]))
            elif t[2] == "*":
                #t[0] = Arithmetic(t[1], t[3], ArithmeticOption.TIMES, t.lineno(1), t.lexpos(0))
                t[0] = Aritmetica(OperadorAritmetico.ASTERISCO, t[1],t[3], t.lineno(2), self.find_column(self.input, t.slice[2]))
            elif t[2] == "/":
                #t[0] = Arithmetic(t[1], t[3], ArithmeticOption.DIV,t.lineno(1), t.lexpos(0))
                t[0] = Aritmetica(OperadorAritmetico.DIAGONAL, t[1],t[3], t.lineno(2), self.find_column(self.input, t.slice[2]))
            elif t[2] == "^":
                #t[0] = Arithmetic(t[1], t[3], ArithmeticOption.RAISED,t.lineno(1), t.lexpos(0))
                t[0] = Aritmetica(OperadorAritmetico.POTENCIA, t[1],t[3], t.lineno(2), self.find_column(self.input, t.slice[2]))
            elif t[2] == "%":
                #t[0] = Arithmetic(t[1], t[3], ArithmeticOption.MODULE, t.lineno(1), t.lexpos(0))
                t[0] = Aritmetica(OperadorAritmetico.MODULO, t[1],t[3], t.lineno(2), self.find_column(self.input, t.slice[2]))
            elif t[2] == "or":
                #t[0] = Logical(t[1], t[3], LogicOption.OR,t.lineno(1), t.lexpos(0))
                t[0] = Logica(OperadorLogico.OR, t[1],t[3], t.lineno(2), self.find_column(self.input, t.slice[2]))
            elif t[2] == "and":
                #t[0] = Logical(t[1], t[3], LogicOption.AND,t.lineno(1), t.lexpos(0))
                t[0] = Logica(OperadorLogico.AND, t[1],t[3], t.lineno(2), self.find_column(self.input, t.slice[2]))
            elif t[2] == "<":
                #t[0] = Relational(t[1], t[3], RelationalOption.LESS,t.lineno(1), t.lexpos(0))
                t[0] = Relacional(OperadorRelacional.MENORQUE, t[1],t[3], t.lineno(2), self.find_column(self.input, t.slice[2]))
            elif t[2] == ">":
                #t[0] = Relational(t[1], t[3], RelationalOption.GREATER, t.lineno(1), t.lexpos(0))
                t[0] = Relacional(OperadorRelacional.MAYORQUE, t[1],t[3], t.lineno(2), self.find_column(self.input, t.slice[2]))
            elif t[2] == "<=":
                #t[0] = Relational(t[1], t[3], RelationalOption.LESSEQUAL, t.lineno(1), t.lexpos(0))
                t[0] = Relacional(OperadorRelacional.MENORIGUAL, t[1],t[3], t.lineno(2), self.find_column(self.input, t.slice[2]))
            elif t[2] == ">=":
                #t[0] = Relational(t[1], t[3], RelationalOption.GREATEREQUAL, t.lineno(1), t.lexpos(0))
                t[0] = Relacional(OperadorRelacional.MAYORIGUAL, t[1],t[3], t.lineno(2), self.find_column(self.input, t.slice[2]))
            elif t[2] == "==":
                #t[0] = Relational(t[1], t[3], RelationalOption.EQUAL,t.lineno(1), t.lexpos(0))
                t[0] = Relacional(OperadorRelacional.IGUALACION, t[1],t[3], t.lineno(2), self.find_column(self.input, t.slice[2]))
            elif t[2] == "!=":
                #t[0] = Relational(t[1], t[3], RelationalOption.DISTINCT, t.lineno(1), t.lexpos(0))
                t[0] = Relacional(OperadorRelacional.DIFERENCIACION, t[1],t[3], t.lineno(2), self.find_column(self.input, t.slice[2]))


    def p_final_expression(self,t):
        '''final_expression     : PARENTESIS_IZQ expression PARENTESIS_DER
                                | CORCHETE_IZQ exp_list CORCHETE_DER
                                | DECIMAL
                                | ENTERO
                                | CADENA
                                | ID
                                | ID index_list  
                                | TRUE
                                | FALSE
                                | call_function
                                | nativas'''
        if len(t) == 2:
            if t.slice[1].type == "ENTERO":
                #t[0] = Literal(t[1], Type.INT, t.lineno(1), t.lexpos(0))
                t[0] = Primitivos(TIPO.ENTERO, t[1], t.lineno(1), self.find_column(self.input, t.slice[1]))
            if t.slice[1].type == "DECIMAL":
                #t[0] = Literal(t[1], Type.FLOAT, t.lineno(1), t.lexpos(0))
                t[0] = Primitivos(TIPO.FLOAT, t[1], t.lineno(1), self.find_column(self.input, t.slice[1]))
            elif t.slice[1].type == "FALSE":
                #t[0] = Literal(False, Type.BOOL, t.lineno(1), t.lexpos(0))
                t[0] = Primitivos(TIPO.BOOLEANO, False, t.lineno(1), self.find_column(self.input, t.slice[1]))
            elif t.slice[1].type == "TRUE":
                #t[0] = Literal(True, Type.BOOL, t.lineno(1), t.lexpos(0))
                t[0] = Primitivos(TIPO.BOOLEANO, True, t.lineno(1), self.find_column(self.input, t.slice[1]))
            elif t.slice[1].type == "CADENA":
                #t[0] = Literal(str(t[1]), Type.STRING, t.lineno(1), t.lexpos(0))
                cadena=str(t[1])
                cadena=cadena.replace('\\\\','\\')
                cadena=cadena.replace('\\\'','\'')
                cadena=cadena.replace('\\n','\n')
                cadena=cadena.replace('\\N','\n')
                cadena=cadena.replace('\\t','\t')
                cadena=cadena.replace('\\T','\t')
                cadena=cadena.replace('\\\"','\"')
                t[0] = Primitivos(TIPO.CADENA,cadena, t.lineno(1), self.find_column(self.input, t.slice[1]))
            elif t.slice[1].type == 'ID':
                #t[0] = Access(t[1], t.lineno(1), t.lexpos(0))
                t[0] = Identificador(t[1].lower(), t.lineno(1), self.find_column(input, t.slice[1]))
            elif t.slice[1].type == 'nativas':
                t[0] = t[1]
            elif t.slice[1].type == 'call_function':
                t[0] = t[1]
        else:
            if t.slice[1].type == "PARENTESIS_IZQ":
                t[0] = t[2]
            else:
                t[0] = Literal(t[2], Type.LIST, t.lineno(1), t.lexpos(0))
                #Lista de variables

    def p_nativas(self,t):
        '''nativas          : UPPER PARENTESIS_IZQ expression PARENTESIS_DER
                            | LOWER PARENTESIS_IZQ expression PARENTESIS_DER
                            | STRING PARENTESIS_IZQ expression PARENTESIS_DER
                            | FLOAT PARENTESIS_IZQ expression PARENTESIS_DER
                            | LEN PARENTESIS_IZQ expression PARENTESIS_DER
                            '''
        if(t.slice[1].type == "UPPER"):
            t[0]=ToUpper(t[3],t.lineno(1),self.find_column(self.input,t.slice[1]))       
        elif(t.slice[1].type == 'LOWER'):
            t[0]=ToLower(t[3],t.lineno(1),self.find_column(self.input,t.slice[1]))
        elif(t.slice[1].type == 'LEN'):
            t[0]=Length(t[3],t.lineno(1),self.find_column(self.input,t.slice[1]))

    def p_print_instr(self,t):
        #'print_instr    : PRINT PARENTESIS_IZQ exp_list PARENTESIS_DER'
        'print_instr    : PRINT PARENTESIS_IZQ expression PARENTESIS_DER'
        t[0] = Print(t[3], t.lineno(3), self.find_column(self.input, t.slice[1]))

    def p_println_instr(self,t):
        #'println_instr  : PRINTLN PARENTESIS_IZQ exp_list PARENTESIS_DER'
        'println_instr  : PRINTLN PARENTESIS_IZQ expression PARENTESIS_DER'
        t[0] = Print(t[3], t.lineno(3), self.find_column(self.input, t.slice[1]))

    def p_tipo(self,t):
        '''tipo     : INT
                    | FLOAT
                    | BOOL
                    | STRING
                    | NONE
        '''
        tipo=None
        if t[1]=="string":
            tipo=TIPO.CADENA
        elif t[1]=="char":
            tipo=TIPO.CARACTER
        elif t[1]=="boolean":
            tipo=TIPO.BOOLEANO
        elif t[1]=="int":
            tipo=TIPO.ENTERO
        elif t[1]=="float":
            tipo=TIPO.FLOAT
        t[0]=tipo

    def p_asignacion_instr(self,t):
        '''asignacion_instr     : ID IGUAL expression'''
        #t[0] = Declaration(t[1], t[3], t.lineno(1), t.lexpos(0))
        t[0]=Declaracion(t[1].lower(),t.lineno(1),self.find_column(self.input,t.slice[2]),t[3])

    def p_definicion_asignacion_instr(self,t):
        '''definicion_asignacion_instr  : ID  DOSPUNTOS tipo IGUAL expression'''
        t[0] = Declaration(t[1], t[5], t.lineno(1), t.lexpos(0))

    def p_asignacion_arreglo_instr(self,t):
        '''asignacion_arreglo_instr     : ID index_list IGUAL expression'''

    def p_call_function_instr(self,t):
        '''call_function    : ID PARENTESIS_IZQ PARENTESIS_DER
                            | ID PARENTESIS_IZQ exp_list PARENTESIS_DER'''
        if len(t) == 4:
            t[0] = CallFunc(t[1], [], t.lineno(1), t.lexpos(0))
        else:
            t[0] = CallFunc(t[1], t[3], t.lineno(1), t.lexpos(0))

    def p_exp_list_instr(self,t):
        '''exp_list         : exp_list COMA expression
                            | expression'''
        if len(t) == 2:
            t[0] = [t[1]]
        else:
            t[1].append(t[3])
            t[0] = t[1]
        
    def p_index_list_instr(self,t):
        '''index_list       : index_list CORCHETE_IZQ expression CORCHETE_DER
                            | CORCHETE_IZQ expression CORCHETE_DER'''

    def p_statement(self,t):
        '''statement        : instrucciones'''
        t[0] = Statement(t[1], t.lineno(1), t.lexpos(0))

    def p_declare_function(self,t):
        '''declare_function     : DEF ID PARENTESIS_IZQ dec_params PARENTESIS_DER DOSPUNTOS statement END
                                | DEF ID PARENTESIS_IZQ PARENTESIS_DER DOSPUNTOS statement END'''
        if len(t) == 8:
            t[0] = Function(t[2], [], Type.NULL, t[6], t.lineno(1), t.lexpos(0))
        else:
            t[0] = Function(t[2], t[4], Type.NULL, t[7], t.lineno(1), t.lexpos(0))

    def p_dec_params(self,t):
        '''dec_params :   dec_params COMA ID DOSPUNTOS tipo
                        | dec_params COMA ID
                        | ID DOSPUNTOS tipo
                        | ID'''
        if len(t) == 2:
            t[0] = [Param(t[1],Type.STRING,t.lineno(1), t.lexpos(0))]
        elif len(t) == 4:
            if(t.slice[1].type == 'ID'):
                t[0] = [Param(t[1],t[3],t.lineno(1), t.lexpos(0))]
            else:
                t[0] = t[1].append(Param(t[3],Type.STRING,t.lineno(1), t.lexpos(0)))
        else:
            t[0] = t[1].append(Param(t[3],t[5],t.lineno(1), t.lexpos(0)))

    def p_if_state(self,t):
        '''if_state     : IF expression DOSPUNTOS statement END
                        | IF expression DOSPUNTOS statement ELSE DOSPUNTOS statement END
                        | IF expression DOSPUNTOS statement else_if_list END'''
        

    def p_else_if_list(self,t):
        '''else_if_list     : ELSEIF expression DOSPUNTOS statement
                            | ELSEIF expression DOSPUNTOS statement ELSE statement
                            | ELSEIF expression DOSPUNTOS statement else_if_list'''

    def p_while_state(self,t):
        '''while_state      : WHILE expression DOSPUNTOS statement END'''
        t[0] = While(t[2], t[4], t.lineno(1), t.lexpos(0))

    def p_for_state(self,t):
        '''for_state        : FOR ID IN expression DOSPUNTOS expression DOSPUNTOS statement END
                            | FOR ID IN expression DOSPUNTOS statement END'''
                        
    def p_break(self,t):
        '''break_state      : BREAK'''
        t[0] = Break(t.lineno(1), t.lexpos(0))

    def p_continue(self,t):
        '''continue_state      : CONTINUE'''
        t[0] = Continue(t.lineno(1), t.lexpos(0))

    def p_return(self,t):
        '''return_state     : RETURN
                            | RETURN expression'''
        if(len(t) == 2):
            t[0] = ReturnSt(None, t.lineno(1), t.lexpos(0))
        else:
            t[0] = ReturnSt(t[2], t.lineno(1), t.lexpos(0))


    # Funciones analizador sintactico -------------------------------------------------------------------------------------------------------------

    def p_error(self,t):
            #! ALMACENAMIENTO DE ERRORES SINTACTICOS
        if t==None:
            self.errores.append(Error("Sintactico","Error sintactico por llegar al final del documento",0,0))
                
        else:
            self.errores.append(Error("Sintactico","Error sintactico en "+t.value,t.lineno,self.find_column(self.input,t)))

    def find_column(self, inp, token):
        inp=str(inp)
        line_start = 1 + inp.rfind('\n', 0, token.lexpos) 
        return (token.lexpos - line_start) + 1
    
    def build(self,**kwargs):
             
        self.errores = []
        self.lexer = lex.lex(module=self,**kwargs)
        self.parser = yacc.yacc(module=self)
        return 

    def Analizar(self,data):
        
        self.build()
        self.input=data
        instrucciones = self.parser.parse(data) #? ARBOL AST
        
        ast = Arbol(instrucciones)
        TSGlobal = TablaSimbolos(None,"Global")
        ast.setTSglobal(TSGlobal)
        
        
        for error in self.errores:    #? CAPTURA DE ERRORES LEXICOS Y SINTACTICOS
            ast.Errores.append(error)
            ast.updateConsola(error.toString())

        instrucciones=ast.getInstrucciones()
        if instrucciones==None:
            instrucciones=[]
            ast.setInstrucciones([])
        for instruccion in instrucciones:
            if isinstance(instruccion,Declaracion) or isinstance(instruccion,Asignacion) or isinstance(instruccion,Print) or isinstance(instruccion,IncrementoDecremento) or isinstance(instruccion,DeclaracionArregloTipo1) or isinstance(instruccion,DeclaracionArregloTipo2) or isinstance(instruccion,AsignacionArreglo):
                value=instruccion.Interpretar(ast,TSGlobal)
                if isinstance(value,Error):
                    ast.getExcepciones().append(value)
                    ast.updateConsola(value.toString())
            elif isinstance(instruccion,Funcion):
                result=TSGlobal.SetFuncion(instruccion)
                if isinstance(result,Error):
                    ast.getExcepciones().append(result)
                    ast.updateConsola(result.toString())
        contador=0
        for instruccion in instrucciones:
            
            if isinstance(instruccion,Main):
                contador+=1
                
                if contador==2:
                    err = Error("Semantico", "Existen mas de una funcion Main", instruccion.Fila, instruccion.Columna)
                    ast.getExcepciones().append(err)
                    ast.updateConsola(err.toString())
                    
                    break
                value=instruccion.Interpretar(ast,TSGlobal)
                if isinstance(value,Error):
                    ast.getExcepciones().append(value)
                    ast.updateConsola(value.toString())        
                if isinstance(value, Break): 
                    err = Error("Semantico", "Sentencia BREAK fuera de ciclo", instruccion.Fila, instruccion.Columna)
                    ast.getExcepciones().append(err)
                    ast.updateConsola(err.toString())
                if isinstance(value, Return): 
                    err = Error("Semantico", "Sentencia RETURN fuera de ciclo", instruccion.Fila, instruccion.Columna)
                    ast.getExcepciones().append(err)
                    ast.updateConsola(err.toString())
        
        #? GENERAMOS LOS REPORTES NECESARIOS
        #* REPORTE DE ERRORES, RECIBE UNA LISTA DE LOS ERRORES GENERADOS
        
        try:
            ReporteErrores(ast.getExcepciones()).Generar_Reporte()
        except:
            error=Error("Funcionalidad","No se pudo generar reporte de errores")
            ast.Errores.append(error)
            ast.updateConsola(error.toString())
        #* REPORTE DE AST, RECIBE UN OBJETO DE TIPO ARBOL
        
        try:
            RepoorteAST(ast).GenerarAST()
        except:
            error=Error("Funcionalidad","No se pudo generar reporte de AST")
            ast.Errores.append(error)
            ast.updateConsola(error.toString())
        #*REPORTE DE TABLA DE SIMBOLOS
        try:
            RepoorteTablaSimbolos(ast).GenerarReporte()
        except:
            error=Error("Funcionalidad","No se pudo generar reporte de tabla de simbolos")
            ast.Errores.append(error)
            ast.updateConsola(error.toString())
        return ast
