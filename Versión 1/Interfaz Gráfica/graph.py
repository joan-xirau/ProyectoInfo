from segment import *
from node import *
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseEvent



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

def DelNode(g,n):
    #Solo sí el nodo esta ya en el grafo, devuelve True y elimina el nodo de la lista nodos del grafo
    if n in g.nodes:
        g.nodes.remove(n)
        return True
    return False

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

def DelSegment(g, name):
    found = False
    for segment_in_graph in g.segments:
        if segment_in_graph.name == name:
            found = True
            break
    if found:
        DelNeighbor(segment_in_graph.origin, segment_in_graph.destination)
        g.segments.remove(segment_in_graph)
        return True
    else:
        return False
        

    



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
    fig, ax = plt.subplots()

    # Variable para saber si estamos en el modo de grafo completo o en el modo de un nodo específico
    current_node = None
    
    def draw_graph():
        # Limpiar el gráfico actual
        ax.clear()
        
        # Dibujar cada flecha en el grafo
        for segment in g.segments:
            ax.arrow(
                x = segment.origin.x,
                y = segment.origin.y,
                dx = (segment.destination.x - segment.origin.x),
                dy = (segment.destination.y - segment.origin.y),
                color = "green",
                width  = 0.005,
                head_width = 0.35,
                length_includes_head = True,
            )

            ax.text(
                x = (segment.destination.x + segment.origin.x) / 2,
                y = (segment.destination.y + segment.origin.y) / 2,
                s = Distance(segment.origin, segment.destination)
            )

        # Dibujar los nodos
        for node in g.nodes:
            if current_node is None or node != current_node:
                ax.scatter(
                    x = node.x,
                    y = node.y,
                    s = 100,
                    c = "blue",
                    edgecolors="black",
                    linewidths=1
                )
            else:
                ax.scatter(
                    x = node.x,
                    y = node.y,
                    s = 100,
                    c = "green",  # Nodo seleccionado en verde
                    edgecolors="black",
                    linewidths=1
                )

            ax.text(
                x = node.x + 0.5,
                y = node.y + 0.5,
                s = node.name
            )

        ax.set_title("Grafo")
        ax.set_xlabel("Coordenadas X")
        ax.set_ylabel("Coordenadas Y")
        ax.grid(True)

    def draw_node(node):
        # Limpiar el gráfico
        ax.clear()

        # Dibujar solo los nodos
        for n in g.nodes:
            if n == node:
                ax.scatter(
                    x = n.x,
                    y = n.y,
                    s = 100,
                    c = "green",
                    edgecolors="black",
                    linewidths=1
                )
            else:
                ax.scatter(
                    x = n.x,
                    y = n.y,
                    s = 100,
                    c = "blue",  # Nodo no seleccionado en azul
                    edgecolors="black",
                    linewidths=1
                )

            ax.text(
                x = n.x + 0.5,
                y = n.y + 0.5,
                s = n.name
            )

        # Dibujar los segmentos hacia los vecinos del nodo seleccionado
        for neighbor in node.neighbors:
            ax.arrow(
                x = node.x,
                y = node.y,
                dx = (neighbor.x - node.x),
                dy = (neighbor.y - node.y),
                color = "green",
                width  = 0.005,
                head_width = 0.35,
                length_includes_head = True,
            )
            ax.text(
                x = (neighbor.x + node.x) / 2,
                y = (neighbor.y + node.y) / 2,
                s = Distance(node, neighbor)
            )

        ax.set_title(f"Grafo a partir de {node.name}")
        ax.set_xlabel("Coordenadas X")
        ax.set_ylabel("Coordenadas Y")
        ax.grid(True)

    def on_click(event: MouseEvent):
        nonlocal current_node
        clicked_node = None
        
        # Comprobar si se ha hecho clic en algún nodo
        for node in g.nodes:
            if (event.xdata - node.x)**2 + (event.ydata - node.y)**2 < 0.5:  # 0.5 es el radio de tolerancia
                clicked_node = node
                break
        
        if clicked_node:
            if current_node == clicked_node:
                # Si ya está seleccionado, volver al grafo completo
                current_node = None
            else:
                # Si no está seleccionado, mostrar el nodo seleccionado
                current_node = clicked_node
        
        # Redibujar el gráfico con el nuevo estado
        if current_node is None:
            draw_graph()
        else:
            draw_node(current_node)
        
        # Refresca el gráfico y devuelve el fig
        plt.draw()  # Refresca el gráfico
        return fig  # Devolver la figura actualizada

    # Inicializar con el grafo completo
    draw_graph()

    # Conectar el evento de clic con la función on_click
    fig.canvas.mpl_connect('button_press_event', on_click)

    # Devuelve el objeto fig
    return fig


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


