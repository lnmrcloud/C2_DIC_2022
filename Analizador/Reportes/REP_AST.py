import os
os.environ["PATH"] += os.pathsep + 'C:\\Program Files\\Graphviz\\bin\\'
from graphviz import Source
from ..AnalizadorSemantico.Clases_Abstractas import NodoAST
class RepoorteAST:
    def __init__(self,Ast):
        self.Ast = Ast
        super().__init__()
        
    def GenerarAST(self):
        init = NodoAST("RAIZ")
        instr = NodoAST("INSTRUCCIONES")
        for instruccion in self.Ast.getInstrucciones():
            instr.agregarHijoNodo(instruccion.getNodo())

        init.agregarHijoNodo(instr)
        grafo = self.Ast.getDot(init) #DEVUELVE EL CODIGO GRAPHVIZ DEL AST

       #? PARTE DONDE LE METEMOS EL STRING A UN DOT PARA GRAPHVIZ
        dots=Source(grafo)
        absFilePath = os.path.abspath(__file__)
        path, filename = os.path.split(absFilePath)       
        ruta=path+"\\AST"
        
        dots.render('AST.dot',directory=ruta,format='pdf') 