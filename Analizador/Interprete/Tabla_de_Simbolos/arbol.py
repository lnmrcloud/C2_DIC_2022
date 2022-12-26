#Clase arbol

class Arbol:
    def __init__(self, instrucciones ):
        self.instrucciones       = instrucciones
        self.Errores             = []                       # LISTA DE ERRORES
        self.consola             = ""                       # ALMACENARA LO QUE SE MOSTRARA EN CONSOLA
        self.dot                 = ""
        self.TablaSimbolosGlobal = None         # TABLA DE SIMBOLOS BLOBAL

    def getInstrucciones(self):
        return self.instrucciones

    def setInstrucciones(self, instrucciones):
        self.instrucciones = instrucciones

    def getExcepciones(self):
        return self.Errores

    def setExcepciones(self, Errores):
        self.Errores = Errores

    def getConsola(self):
        return self.consola
    
    def setConsola(self, consola):
        self.consola = consola

    def updateConsola(self,cadena):
        self.consola += str(cadena) + '\n'

    def getTSGlobal(self):
        return self.TSglobal
    
    def setTSglobal(self, TSglobal):
        self.TSglobal = TSglobal
        
    def getDot(self, raiz): ## DEVUELVE EL STRING DE LA GRAFICA EN GRAPHVIZ
        self.dot = ""
        self.dot += "digraph {\n"
        self.dot+="bgcolor=\"cyan:red\" style=\"filled\"\n"
        self.dot+="node [shape=polygon sides=4 skew=.4 fillcolor=\"/rdylgn11/4:/rdylgn11/5\" style=\"rounded,filled\" gradientangle=180]\n"
        self.dot += "n0[label=\"" + raiz.getValor().replace("\"", "\\\"") + "\"];\n"
        self.contador = 1
        self.recorrerAST("n0", raiz)
        self.dot += "}"
        return self.dot

    def recorrerAST(self, idPadre, nodoPadre):
        for hijo in nodoPadre.getHijos():
            nombreHijo = "n" + str(self.contador)
            self.dot += nombreHijo + "[label=\"" + hijo.getValor().replace("\"", "\\\"") + "\"];\n"
            self.dot += idPadre + "->" + nombreHijo + ";\n"
            self.contador += 1
            self.recorrerAST(nombreHijo, hijo)