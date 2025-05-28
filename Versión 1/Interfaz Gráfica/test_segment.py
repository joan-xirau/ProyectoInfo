from node import *
from segment import *

n1 = node ('aaa', 0, 0)
n2 = node ('bbb', 3, 4)
n3 = node("ccc", 3,5 )

s1 = segment("s1" , n1, n2)
s2 = segment("s2" , n2, n3)

print("Segmento 1:",s1.name, "Nodo origen:", s1.origin.name, "Nodo Destino", s1.destination.name, "Coste", s1.cost)
print("Segmento 2:",s2.name, "Nodo origen:", s2.origin.name, "Nodo Destino", s2.destination.name, "Coste", s2.cost)