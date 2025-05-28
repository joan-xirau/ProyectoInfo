from graph import *
from path import *
import os

def CreateGraph_1 ():
 G = graph()
 AddNode(G, node("A",1,20))
 AddNode(G, node("B",8,17))
 AddNode(G, node("C",15,20))
 AddNode(G, node("D",18,15))
 AddNode(G, node("E",2,4))
 AddNode(G, node("F",6,5))
 AddNode(G, node("G",12,12))
 AddNode(G, node("H",10,3))
 AddNode(G, node("I",19,1))
 AddNode(G, node("J",13,5))
 AddNode(G, node("K",3,15))
 AddNode(G, node("L",4,10))
 AddSegment(G, "AB","A","B")
 AddSegment(G, "AE","A","E")
 AddSegment(G, "AK","A","K")
 AddSegment(G, "BA","B","A")
 AddSegment(G, "BC","B","C")
 AddSegment(G, "BF","B","F") 
 AddSegment(G, "BK","B","K")
 AddSegment(G, "BG","B","G")
 AddSegment(G, "CD","C","D")
 AddSegment(G, "CG","C","G")
 AddSegment(G, "DG","D","G")
 AddSegment(G, "DH","D","H")
 AddSegment(G, "DI","D","I")
 AddSegment(G, "EF","E","F")
 AddSegment(G, "FL","F","L")
 AddSegment(G, "GB","G","B")
 AddSegment(G, "GF","G","F")
 AddSegment(G, "GH","G","H")
 AddSegment(G, "ID","I","D")
 AddSegment(G, "IJ","I","J")
 AddSegment(G, "JI","J","I")
 AddSegment(G, "KA","K","A")
 AddSegment(G, "KL","K","L")
 AddSegment(G, "LK","L","K")
 AddSegment(G, "LF","L","F")
 return G

def CreateGraph_2 ():
    G = graph()
    AddNode(G, node("A", 2, 18))
    AddNode(G, node("B", 5, 16))
    AddNode(G, node("C", 9, 19))
    AddNode(G, node("D", 13, 17))
    AddNode(G, node("E", 16, 14))
    AddNode(G, node("F", 18, 10))
    AddNode(G, node("G", 14, 5))
    AddNode(G, node("H", 9, 3))
    AddNode(G, node("I", 5, 4))
    AddNode(G, node("J", 1, 9))
    AddNode(G, node("K", 6, 11))
    AddNode(G, node("L", 10, 13))

    AddSegment(G, "AB", "A", "B")
    AddSegment(G, "AC", "A", "C")
    AddSegment(G, "BC", "B", "C")
    AddSegment(G, "BD", "B", "D")
    AddSegment(G, "CD", "C", "D")
    AddSegment(G, "DE", "D", "E")
    AddSegment(G, "EF", "E", "F")
    AddSegment(G, "FG", "F", "G")
    AddSegment(G, "GH", "G", "H")
    AddSegment(G, "HI", "H", "I")
    AddSegment(G, "IJ", "I", "J")
    AddSegment(G, "JK", "J", "K")
    AddSegment(G, "KL", "K", "L")
    AddSegment(G, "LG", "L", "G")
    AddSegment(G, "LC", "L", "C")
    AddSegment(G, "FB", "F", "B")
    return G



#print ("Probando el grafo...")
#G = CreateGraph_1 ()
#Plot(G)
#PlotNode(G, "C")
#n = GetClosest(G,15,5)
#print (n.name) # La respuesta debe ser J
#n = GetClosest(G,8,19)
#print (n.name) # La respuesta debe ser B

#G = CreateGraph_2()
#Plot(G)

#G = ReadFile("grafo.txt")

#if G:
    #Plot(G)