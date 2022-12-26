#Clase error

class Error:
    """
        LA CLASE ERROR SERA UN NODO, DONDE SE ALMACENARA LOS DIFERENTES ERRORES QUE SURJAN DURANTE EL ANALISIS
        
    """
    def __init__(self, Tipo, Descripcion, Fila, Columna):
        self.Tipo        = Tipo             # TIPO DE ERROR: SEMANTICO,SINTACTICO
        self.Descripcion = Descripcion      # DESCRIPCION DEL ERROR
        self.Fila        = Fila             # FILA ACTUAL DEL ERROR
        self.Columna     = Columna          # COLUMNA ACTUAL DEL ERROR

    def toString(self):
        # RETORNA UN STRING PARA PODER IMPRIMIRLO LUEGO
        return self.Tipo + " - \'" + self.Descripcion + "\'  en [" + str(self.Fila) + "," + str(self.Columna) + "]"