from segment import *
from node import *
import matplotlib.pyplot as plt

class graph:
    #Declarar la clase, con la lista de nodos y segmetnos
    def __init__(self):
        self.nodes = []
        self.segments = []
    

def AddNode(g, n):
    #Solo sí el nodo no esta ya en el grafo, devuelve True y añade el nodo a la lista nodos del grafo
    if n in g.nodes:
        return False
    g.nodes.append(n)
    return True

def AddSegment(g, name, nameOriginNode, nameDestinationNode):
    # Encontrar los nodos pedidos, si alguno, no está , la función devuelve false
    node_1 = None
    node_2 = None

    for node in g.nodes:
        if node.name == nameOriginNode:
            node_1 = node
        elif node.name == nameDestinationNode:
            node_2 = node
    
    if not node_1 or not node_2:
        return False



    #Si ambos nodos estan, se crea un segmento que los une, y se añade dicho segmento al grafo, así como se añade el vecino al nodo
    #segment_0 = segment(nameOriginNode.name + nameDestinationNode.name, nameOriginNode , nameDestinationNode)   --> Si no diesen el nombre
    segment_0 = segment(name, node_1 , node_2)


    AddNeighbor(node_1, node_2)
    if segment_0 in g.segments:
        return False
    g.segments.append(segment_0)
    return True


def GetClosest(g,x,y):
    node = g.nodes[0]
    min_distance = sqrt((node.x - x)**2 + (node.y - y)**2 )
    for node in g.nodes:

        distance = sqrt((node.x - x)**2 + (node.y - y)**2 )

        if distance < min_distance:

            min_distance = distance
            min_node = node
    
    return min_node


def Plot(g):
    
    #Dibujar cada flecha en el grafo
    for segment in g.segments:
        #Mostrar los segmentos
        plt.arrow(
            x = segment.origin.x,
            y = segment.origin.y,
            dx = (segment.destination.x - segment.origin.x),
            dy = (segment.destination.y - segment.origin.y),
            color = "green",
            width  = 0.005 ,
            head_width = 0.35,
            length_includes_head = True,
        )

        #Mostras costes
        plt.text(
            x = (segment.destination.x + segment.origin.x)/2,
            y = (segment.destination.y + segment.origin.y )/2,
            s = Distance(segment.origin, segment.destination)

        )
    #Dibujar cada punto del nodo
    for node in g.nodes:

        plt.scatter(
            x = node.x,
            y =  node.y,
            s = 100,
            c = "blue",
            edgecolors="black",
            linewidths=1
        )
        #Mostrar El nombre

        plt.text(
            x = node.x + 0.5,
            y = node.y + 0.5,
            s = node.name

        )

    plt.title("Grafo")
    plt.xlabel("Coordenadas X")
    plt.ylabel("Coordenadas Y")
    plt.grid(True)
    plt.show()

def PlotNode(g, nameOrigin):
    #Encontramos el nodo , y dibujamos el resto ( si el nodo es el deseado, lo pintamos de otro color)
    node_0 = None
    for node in g.nodes:
        if node.name == nameOrigin:
            node_0 = node
            plt.scatter(
                x = node.x,
                y =  node.y,
                s = 100,
                c = "green",
                edgecolors="black",
                linewidths=1
            )
        else:
            plt.scatter(
            x = node.x,
            y =  node.y,
            s = 100,
            c = "blue",
            edgecolors="black",
            linewidths=1
        )

        plt.text(
            x = node.x + 0.5,
            y = node.y + 0.5,
            s = node.name

            )

    if not node_0:
        return False
    
    #Dibujamos un segmento a cada vecino
    for neighbor in node_0.neighbors:
        plt.arrow(
            x = node_0.x,
            y = node_0.y,
            dx = (neighbor.x - node_0.x),
            dy = (neighbor.y - node_0.y),
            color = "green",
            width  = 0.005 ,
            head_width = 0.35,
            length_includes_head = True,
        )

        #Mostras costes
        plt.text(
            x = (neighbor.x + node_0.x)/2,
            y = (neighbor.y + node_0.y )/2,
            s = Distance(node_0, neighbor)

        )        


    
    plt.title(f"Grafo a partir de {node_0.name}")
    plt.xlabel("Coordenadas X")
    plt.ylabel("Coordenadas Y")
    plt.grid(True)
    plt.show()


def ReadFile(filename):
    try:    
        with open(filename, 'r') as file:
            lines = file.readlines()
    except:
        return None

    g = graph()
    estado = None
    for line in lines:
        line = line.strip()  # Limpiar espacios y saltos de línea
        if not line:
            continue  # Saltar líneas vacías

        # Verificar secciones
        if line == "NODES":
            estado = "NODES"
            continue
        elif line == "SEGMENTS":
            estado = "SEGMENTS"
            continue

        # Procesar según la sección
        parts = line.split()  # Dividir por cualquier espacio
        if estado == "NODES":
            if len(parts) != 3:
                print(f"Línea de nodo inválida: {line}")
                continue
            name, x, y = parts[0], parts[1], parts[2]
            AddNode(g, node(name, float(x), float(y)))
        elif estado == "SEGMENTS":
            if len(parts) != 3:
                print(f"Línea de segmento inválida: {line}")
                continue
            seg_name, origin, dest = parts[0], parts[1], parts[2]
            AddSegment(g, seg_name, origin, dest)

    return g
