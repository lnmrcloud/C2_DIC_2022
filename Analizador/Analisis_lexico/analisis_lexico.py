from ..ply import lex
class MyLex(object):
    #Palabras reservadas
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

    def t_error(self,t): #LEXICOS
        print('caracter no reconocido: ' + str(t.value[0]))
        # almacenamiento de errores lexicos
        t.lexer.skip(1)


    # Construyendo el analizador lexico
    
    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)


    # Test it output    
    def Lista_de_Tokens(self,data):
        
        self.build()
        self.lexer.input(data)
        lista=[]
        i=0
        while True:
            tok=self.lexer.token()
            if not tok:
                 break
            
            l = []
            l.append(str(tok.type))
            l.append(str(tok.value))
            lista.append(l)
            i+=1
        
        return lista
