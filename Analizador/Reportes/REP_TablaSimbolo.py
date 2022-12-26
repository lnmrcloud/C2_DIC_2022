import os
os.environ["PATH"] += os.pathsep + 'C:\\Program Files\\Graphviz\\bin\\'
from graphviz import Source

class RepoorteTablaSimbolos:
    def __init__(self,Ast):
        self.Ast = Ast
        super().__init__()
        
    def GenerarReporte(self):
        dot=""
        dot+="digraph G {\n"
        dot+="bgcolor=\"blue:green\" style=\"filled\"\n"
        dot+="node [shape=record fillcolor=\"blue:brown\" style=\"filled\" gradientangle=180]\n"
        dot+="a0 [label=<\n"
        dot+="<TABLE border=\"10\" cellspacing=\"10\" cellpadding=\"10\" style=\"rounded\" bgcolor=\"/rdylgn11/1:/rdylgn11/11\" gradientangle=\"315\">\n"
        dot+="<TR>\n"
        dot+="<TD border=\"3\" colspan=\"7\" bgcolor=\"/rdylgn11/4:/rdylgn11/5\">Reporte de Tabla de simbolos</TD>\n"
        dot+="</TR>\n"
        dot+="<TR>\n"
        dot+="<TD border=\"3\"  bgcolor=\"/rdylgn11/4:/rdylgn11/5\">Identificador</TD>\n"
        dot+="<TD border=\"3\"  bgcolor=\"/rdylgn11/4:/rdylgn11/5\">Tipo</TD>\n"
        dot+="<TD border=\"3\"  bgcolor=\"/rdylgn11/4:/rdylgn11/5\">Tipo dato</TD>\n"
        dot+="<TD border=\"3\"  bgcolor=\"/rdylgn11/4:/rdylgn11/5\">Entorno</TD>\n"
        dot+="<TD border=\"3\"  bgcolor=\"/rdylgn11/4:/rdylgn11/5\">Valor</TD>\n"
        dot+="<TD border=\"3\"  bgcolor=\"/rdylgn11/4:/rdylgn11/5\">Fila</TD>\n"
        dot+="<TD border=\"3\"  bgcolor=\"/rdylgn11/4:/rdylgn11/5\">Columna</TD>\n"
        dot+="</TR>\n"
        dot+=self.Ast.getTSGlobal().GetDot()
        if self.Ast.getTSGlobal().Hijos != None:
            dot+=self.obtenerdothijos(self.Ast.getTSGlobal())
        dot+="</TABLE>>];\n"
        dot+="}"
       #? PARTE DONDE LE METEMOS EL STRING A UN DOT PARA GRAPHVIZ
        dots=Source(dot)
        absFilePath = os.path.abspath(__file__)
        path, filename = os.path.split(absFilePath)       
        ruta=path+"\\Tabla_Simbolos"
        
        dots.render('Tabla_Simbolos.dot',directory=ruta,format='pdf') 
    
    def obtenerdothijos(self,Entorno):
        dot=""
        dothijo=""
        for hijo in Entorno.Hijos:
            dot+=hijo.GetDot()
            if hijo.Hijos!=None:
                dothijo+=self.obtenerdothijos(hijo)
        dot+=dothijo
        return dot