from abc import ABC, abstractmethod

class Operacion(ABC):
    """
    !    UNA CLASE ABSTACTA QUE NOS SERVIRA PARA LLAMARLA SIEMPRE QUE QUERRAMOS QUE SE REALICE UNA OPERACION
    """
    def __init__(self,Fila,Columna):
        # CADA OPERACION SIEMPRE TENDRA UNA FILA Y COLUMNA
        self.Fila    = Fila
        self.Columna = Columna
        super().__init__()

    @abstractmethod
    def Interpretar(self,Arbol,TablaSimbolos):
        pass
    
    @abstractmethod
    def getNodo(self):
        pass