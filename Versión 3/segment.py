from node import *

class segment:
    #Definir la clase, con nombre , origen, final, y el coste entre ambos nodos 
    def __init__(self, name, origin,destination): #Esta función recive dos NODOS
        self.name = name
        self.origin = origin
        self.destination = destination
        self.cost = Distance(origin, destination)
