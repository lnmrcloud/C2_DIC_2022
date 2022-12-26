import os

#? ESTE INIT ES SOLO PARA OBTENER LA RUTA DE LOS ICONOS DE MANERA DINAMICA
absFilePath = os.path.abspath(__file__)
path, filename = os.path.split(absFilePath)
RUTAICONOS=path