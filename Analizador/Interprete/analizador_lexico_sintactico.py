import re
from tkinter.constants import END, FALSE, TRUE
from ..ply import lex,yacc

#? TABLA DE SIMBOLOS

from .Tabla_de_Simbolos import Error, Tipo, OperadorAritmetico,OperadorRelacional,OperadorLogico,arbol,tabla_simbolos

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
        "True" : "TRUE",
        "False" : "FALSE",
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
        "MODULO",
        "POTENCIA",
        "MENOR_QUE",
        "MAYOR_QUE",
        "MENOR_IGUAL_QUE",
        "MAYOR_IGUAL_QUE",
        "IGUAL_QUE",
        "DIFERENTE_QUE"
    ] + list(reservadas.values())

    #tokens

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

    def t_ID(self,t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        # Check for reserved words
        t.type=self.reservadas.get(t.value.lower(),'ID')
        return t

    def t_CADENA(self,t):
        r'\".*?\"'
        # Se quitan comillas - 1
        t.value = t.value[1:-1] 
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

    def t_newline(self,t):
        r'\n'
        t.lexer.lineno += t.value.count("\n")

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
        ('left', 'POR', 'DIVISON', 'MODULO'),
        ('left', 'POTENCIA'),
        ('right', 'UMENOS')
    )

    # Definicion de la gramatica
    
    #    ? VISTA GENERAL:
    #    inicio :  instrucciones 

    def p_init(t):
        '''init            : instrucciones'''
       # t[0] = t[1]


    #    ? VISTA GENERAL:
    #    instrucciones :  instrucciones instruccion
    #                   | instruccion


    def p_instrucciones_lista(t):
        '''instrucciones    : instrucciones instruccion
                            | instruccion'''
       # if (len(t) != 2):
       #     t[1].append(t[2])
       #     t[0] = t[1]
       # else:
       #     t[0] = [t[1]]



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
        t[0] = t[1]



    def p_expression(t):
        '''expression       : MENOS expression %prec UMENOS
                            | NOT expression %prec UMENOS
                            | expression MAS expression
                            | expression MENOS expression
                            | expression POR expression
                            | expression DIVIDIDO expression
                            | expression POTENCIA expression
                            | expression MODULO expression
                            | expression MAYQUE expression
                            | expression MENQUE expression
                            | expression MENIGUALQUE expression
                            | expression MAYIGUALQUE expression
                            | expression IGUALQUE expression
                            | expression NIGUALQUE expression
                            | expression OR expression
                            | expression AND expression
                            | final_expression'''
        if(len(t)==2):
            t[0] = t[1]
        elif (len(t)==3):
            if(t[1] == '-'):
                t[0] = Arithmetic(Literal(0,Type.INT, t.lineno(1), t.lexpos(0)),t[2],ArithmeticOption.MINUS,t.lineno(1), t.lexpos(0))
            else:
                t[0] = Logical(t[2],Literal(True, Type.BOOL, t.lineno(1), t.lexpos(0)),LogicOption.NOT, t.lineno(1), t.lexpos(0))
        else:
            if t[2] == "+":
                t[0] = Arithmetic(t[1], t[3], ArithmeticOption.PLUS,
                                t.lineno(1), t.lexpos(0))
            elif t[2] == "-":
                t[0] = Arithmetic(
                    t[1], t[3], ArithmeticOption.MINUS, t.lineno(1), t.lexpos(0))
            elif t[2] == "*":
                t[0] = Arithmetic(
                    t[1], t[3], ArithmeticOption.TIMES, t.lineno(1), t.lexpos(0))
            elif t[2] == "/":
                t[0] = Arithmetic(t[1], t[3], ArithmeticOption.DIV,
                                t.lineno(1), t.lexpos(0))
            elif t[2] == "^":
                t[0] = Arithmetic(t[1], t[3], ArithmeticOption.RAISED,
                                t.lineno(1), t.lexpos(0))
            elif t[2] == "%":
                t[0] = Arithmetic(
                    t[1], t[3], ArithmeticOption.MODULE, t.lineno(1), t.lexpos(0))
            elif t[2] == "or":
                t[0] = Logical(t[1], t[3], LogicOption.OR,
                            t.lineno(1), t.lexpos(0))
            elif t[2] == "and":
                t[0] = Logical(t[1], t[3], LogicOption.AND,
                            t.lineno(1), t.lexpos(0))
            elif t[2] == "<":
                t[0] = Relational(t[1], t[3], RelationalOption.LESS,
                                t.lineno(1), t.lexpos(0))
            elif t[2] == ">":
                t[0] = Relational(
                    t[1], t[3], RelationalOption.GREATER, t.lineno(1), t.lexpos(0))
            elif t[2] == "<=":
                t[0] = Relational(
                    t[1], t[3], RelationalOption.LESSEQUAL, t.lineno(1), t.lexpos(0))
            elif t[2] == ">=":
                t[0] = Relational(
                    t[1], t[3], RelationalOption.GREATEREQUAL, t.lineno(1), t.lexpos(0))
            elif t[2] == "==":
                t[0] = Relational(t[1], t[3], RelationalOption.EQUAL,
                                t.lineno(1), t.lexpos(0))
            elif t[2] == "!=":
                t[0] = Relational(
                    t[1], t[3], RelationalOption.DISTINCT, t.lineno(1), t.lexpos(0))


    def p_final_expression(t):
        '''final_expression     : PARIZQ expression PARDER
                                | CORCHETEIZQ exp_list CORCHETEDER
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
                t[0] = Literal(t[1], Type.INT, t.lineno(1), t.lexpos(0))
            if t.slice[1].type == "DECIMAL":
                t[0] = Literal(t[1], Type.FLOAT, t.lineno(1), t.lexpos(0))
            elif t.slice[1].type == "FALSE":
                t[0] = Literal(False, Type.BOOL, t.lineno(1), t.lexpos(0))
            elif t.slice[1].type == "TRUE":
                t[0] = Literal(True, Type.BOOL, t.lineno(1), t.lexpos(0))
            elif t.slice[1].type == "CADENA":
                t[0] = Literal(str(t[1]), Type.STRING, t.lineno(1), t.lexpos(0))
            elif t.slice[1].type == 'ID':
                t[0] = Access(t[1], t.lineno(1), t.lexpos(0))
            elif t.slice[1].type == 'nativas':
                t[0] = t[1]
            elif t.slice[1].type == 'call_function':
                t[0] = t[1]
        else:
            if t.slice[1].type == "PARIZQ":
                t[0] = t[2]
            else:
                t[0] = Literal(t[2], Type.LIST, t.lineno(1), t.lexpos(0))

    def p_nativas(t):
        '''nativas          : UPPER PARIZQ expression PARDER
                            | LOWER PARIZQ expression PARDER
                            | STR PARIZQ expression PARDER
                            | FLOAT PARIZQ expression PARDER
                            | LEN PARIZQ expression PARDER
                            '''
        if(t.slice[1].type == "UPPER"):
            t[0] = Upper(t[3], t.lineno(1), t.lexpos(0))        
        elif(t.slice[1].type == 'LOWER'):
            t[0] = Lower(t[3], t.lineno(1), t.lexpos(0))
        elif(t.slice[1].type == 'LEN'):
            t[0] = Len(t.lineno(1), t.lexpos(0), t[3])

    def p_print_instr(t):
        'print_instr    : PRINT PARIZQ exp_list PARDER'
        t[0] = Print(t[3], t.lineno(1), t.lexpos(0), False)

    def p_println_instr(t):
        'println_instr  : PRINTLN PARIZQ exp_list PARDER'
        t[0] = Print(t[3], t.lineno(1), t.lexpos(0), True)

    def p_tipo(t):
        '''tipo     : INT
                    | FLOAT
                    | BOOL
                    | STR
                    | NONE
        '''

    def p_asignacion_instr(t):
        '''asignacion_instr     : ID IGUAL expression'''
        t[0] = Declaration(t[1], t[3], t.lineno(1), t.lexpos(0))

    def p_definicion_asignacion_instr(t):
        '''definicion_asignacion_instr  : ID  DOSP tipo IGUAL expression'''
        t[0] = Declaration(t[1], t[5], t.lineno(1), t.lexpos(0))

    def p_asignacion_arreglo_instr(t):
        '''asignacion_arreglo_instr     : ID index_list IGUAL expression'''

    def p_call_function_instr(t):
        '''call_function    : ID PARIZQ PARDER
                            | ID PARIZQ exp_list PARDER'''
        if len(t) == 4:
            t[0] = CallFunc(t[1], [], t.lineno(1), t.lexpos(0))
        else:
            t[0] = CallFunc(t[1], t[3], t.lineno(1), t.lexpos(0))

    def p_exp_list_instr(t):
        '''exp_list         : exp_list COMA expression
                            | expression'''
        if len(t) == 2:
            t[0] = [t[1]]
        else:
            t[1].append(t[3])
            t[0] = t[1]
        
    def p_index_list_instr(t):
        '''index_list       : index_list CORCHETEIZQ expression CORCHETEDER
                            | CORCHETEIZQ expression CORCHETEDER'''

    def p_statement(t):
        '''statement        : instrucciones'''
        t[0] = Statement(t[1], t.lineno(1), t.lexpos(0))

    def p_declare_function(t):
        '''declare_function     : DEF ID PARIZQ dec_params PARDER DOSP statement END
                                | DEF ID PARIZQ PARDER DOSP statement END'''
        if len(t) == 8:
            t[0] = Function(t[2], [], Type.NULL, t[6], t.lineno(1), t.lexpos(0))
        else:
            t[0] = Function(t[2], t[4], Type.NULL, t[7], t.lineno(1), t.lexpos(0))

    def p_dec_params(t):
        '''dec_params :   dec_params COMA ID DOSP tipo
                        | dec_params COMA ID
                        | ID DOSP tipo
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

    def p_if_state(t):
        '''if_state     : IF expression DOSP statement END
                        | IF expression DOSP statement ELSE DOSP statement END
                        | IF expression DOSP statement else_if_list END'''
        

    def p_else_if_list(t):
        '''else_if_list     : ELIF expression DOSP statement
                            | ELIF expression DOSP statement ELSE statement
                            | ELIF expression DOSP statement else_if_list'''

    def p_while_state(t):
        '''while_state      : WHILE expression DOSP statement END'''
        t[0] = While(t[2], t[4], t.lineno(1), t.lexpos(0))

    def p_for_state(t):
        '''for_state        : FOR ID IN expression DOSP expression DOSP statement END
                            | FOR ID IN expression DOSP statement END'''
                        
    def p_break(t):
        '''break_state      : BREAK'''
        t[0] = Break(t.lineno(1), t.lexpos(0))

    def p_continue(t):
        '''continue_state      : CONTINUE'''
        t[0] = Continue(t.lineno(1), t.lexpos(0))

    def p_return(t):
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
        
        ast = arbol(instrucciones)
        TSGlobal = tabla_simbolos(None,"Global")
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
