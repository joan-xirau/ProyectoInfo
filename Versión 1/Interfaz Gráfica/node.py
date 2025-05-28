from math import *

class node:
    #Definir la clase, con nombre , coordenadas y vecinos (al inicio una lista vacía)
    def __init__(self,name, x = 0,y = 0):
        self.name = name
        self.x = float(x)
        self.y = float(y)
        self.neighbors = []


def AddNeighbor (n1, n2):
    #Definir la función de añadir vecino (que solo devuelve True si lo  hace)
    if n2 in n1.neighbors:
        return False
    n1.neighbors.append(n2)
    return True

def DelNeighbor(n1,n2):
    #Definir la función de añadir vecino (que solo devuelve True si lo  hace)
    if n2 in n1.neighbors:
        n1.neighbors.remove(n2)
        return True
    return False

def Distance (n1,n2):
    #Calculo de la distancia entre dos nodos
    return round(sqrt((n1.x - n2.x)**2 + (n1.y - n2.y)**2 ), 2)