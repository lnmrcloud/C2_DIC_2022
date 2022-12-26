import os
os.environ["PATH"] += os.pathsep + 'C:\\Program Files\\Graphviz\\bin\\'
from graphviz import Source

class ReporteErrores:
    def __init__(self,Errores):
        self.Errores = Errores
        super().__init__()

    def Generar_Reporte(self):
        
        dot=""
        dot+="digraph G {\n"
        dot+="bgcolor=\"blue:green\" style=\"filled\"\n"
        dot+="node [shape=record fillcolor=\"blue:brown\" style=\"filled\" gradientangle=180]\n"
        dot+="a0 [label=<\n"
        dot+="<TABLE border=\"10\" cellspacing=\"10\" cellpadding=\"10\" style=\"rounded\" bgcolor=\"/rdylgn11/1:/rdylgn11/11\" gradientangle=\"315\">\n"
        dot+="<TR>\n"
        dot+="<TD border=\"3\" colspan=\"5\" bgcolor=\"/rdylgn11/4:/rdylgn11/5\">Reporte de errores</TD>\n"
        dot+="</TR>\n"
        dot+="<TR>\n"
        dot+="<TD border=\"3\"  bgcolor=\"/rdylgn11/4:/rdylgn11/5\">No.</TD>\n"
        dot+="<TD border=\"3\"  bgcolor=\"/rdylgn11/4:/rdylgn11/5\">Tipo</TD>\n"
        dot+="<TD border=\"3\"  bgcolor=\"/rdylgn11/4:/rdylgn11/5\">Descripcion</TD>\n"
        dot+="<TD border=\"3\"  bgcolor=\"/rdylgn11/4:/rdylgn11/5\">Fila</TD>\n"
        dot+="<TD border=\"3\"  bgcolor=\"/rdylgn11/4:/rdylgn11/5\">Columna</TD>\n"
        dot+="</TR>\n"
        numero=1
        for Error in self.Errores:
            dot+="<TR>\n"
            dot+="<TD border=\"3\"  bgcolor=\"/rdylgn11/4:/rdylgn11/5\">"+str(numero)+"</TD>\n"
            dot+="<TD border=\"3\"  bgcolor=\"/rdylgn11/4:/rdylgn11/5\">"+str(Error.Tipo)+"</TD>\n"
            dot+="<TD border=\"3\"  bgcolor=\"/rdylgn11/4:/rdylgn11/5\">"+str(Error.Descripcion)+"</TD>\n"
            dot+="<TD border=\"3\"  bgcolor=\"/rdylgn11/4:/rdylgn11/5\">"+str(Error.Fila)+"</TD>\n"
            dot+="<TD border=\"3\"  bgcolor=\"/rdylgn11/4:/rdylgn11/5\">"+str(Error.Columna)+"</TD>\n"
            dot+="</TR>\n"
            numero+=1
        dot+="</TABLE>>];\n"
        dot+="}"
        
        #? PARTE DONDE LE METEMOS EL STRING A UN DOT PARA GRAPHVIZ
        dots=Source(dot)
        absFilePath = os.path.abspath(__file__)
        path, filename = os.path.split(absFilePath)       
        ruta=path+"\\Errores"
        
        dots.render('Errores.dot',directory=ruta,format='pdf') 
        