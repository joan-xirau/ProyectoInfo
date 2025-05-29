from segment import *
from node import *
from path import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backend_bases import MouseEvent
from airSpace import AirSpace

class graph:
    def __init__(self):
        self.nodes = []
        self.segments = []
        self.airspace = None
    
    def load_airspace(self, nav_file, seg_file, aer_file):
        self.airspace = AirSpace()
        self.airspace.load_from_files(nav_file, seg_file, aer_file)
        
        # Convert airspace to graph format
        self.nodes = []
        self.segments = []
        
        # Create nodes from navpoints
        for np in self.airspace.navpoints:
            # Convert lat/lon to x/y coordinates (simple projection)
            x = np.longitude
            y = np.latitude
            self.nodes.append(node(np.name, x, y))
        
        # Create segments
        for seg in self.airspace.navsegments:
            origin = self.find_node_by_name(self.airspace.find_navpoint_by_number(seg.origin_number).name)
            dest = self.find_node_by_name(self.airspace.find_navpoint_by_number(seg.destination_number).name)
            if origin and dest:
                self.segments.append(segment(f"{origin.name}-{dest.name}", origin, dest))
                AddNeighbor(origin, dest)
    
    def find_node_by_name(self, name):
        for node in self.nodes:
            if node.name == name:
                return node
        return None


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
    fig, ax = plt.subplots(figsize=(12, 8))  # Tamaño más grande para mejor visualización

    # Variable para saber si estamos en el modo de grafo completo o en el modo de un nodo específico
    current_node = None
    
    def draw_graph():
        # Limpiar el gráfico actual
        ax.clear()
        
        # Configuración de estilo para mejor visualización
        plt.style.use('classic')  # Estilo más limpio
        ax.grid(True, linestyle='--', alpha=0.6)  # Grid más suave
        
        # Dibujar cada flecha en el grafo con parámetros más pequeños
        for segment in g.segments:
            ax.annotate("",
                xy=(segment.destination.x, segment.destination.y),
                xytext=(segment.origin.x, segment.origin.y),
                arrowprops=dict(
                    arrowstyle="->",
                    color="green",
                    lw=0.5,  # Línea más fina
                    alpha=0.6,  # Transparencia
                    shrinkA=5,  # Espacio en origen
                    shrinkB=5,  # Espacio en destino
                ),
                annotation_clip=False
            )

            # Mostrar distancia solo si hay espacio suficiente
            dx = segment.destination.x - segment.origin.x
            dy = segment.destination.y - segment.origin.y
            dist = sqrt(dx**2 + dy**2)
            
            if dist > 1.0:  # Solo mostrar texto si los nodos están suficientemente separados
                ax.text(
                    x=(segment.destination.x + segment.origin.x) / 2,
                    y=(segment.destination.y + segment.origin.y) / 2,
                    s=f"{Distance(segment.origin, segment.destination):.1f}",
                    fontsize=6,  # Texto más pequeño
                    alpha=0.7
                )

        # Dibujar los nodos con tamaño reducido
        for node in g.nodes:
            if current_node is None or node != current_node:
                ax.scatter(
                    x=node.x,
                    y=node.y,
                    s=30,  # Tamaño reducido
                    c="blue",
                    edgecolors="black",
                    linewidths=0.5,
                    alpha=0.8
                )
            else:
                ax.scatter(
                    x=node.x,
                    y=node.y,
                    s=50,  # Tamaño un poco mayor para nodo seleccionado
                    c="green",
                    edgecolors="black",
                    linewidths=0.5,
                    alpha=1.0
                )

            # Mostrar nombre solo si hay espacio suficiente
            nearest_dist = min(
                sqrt((node.x - n.x)**2 + (node.y - n.y)**2)
                for n in g.nodes if n != node
            )
            
            if nearest_dist > 0.5:  # Solo mostrar texto si los nodos están suficientemente separados
                ax.text(
                    x=node.x + 0.05,
                    y=node.y + 0.05,
                    s=node.name,
                    fontsize=6,  # Texto más pequeño
                    alpha=0.8
                )

        ax.set_title("Grafo del Espacio Aéreo", pad=20)
        ax.set_xlabel("Longitud")
        ax.set_ylabel("Latitud")
        plt.tight_layout()  # Ajustar layout para evitar cortes

    def draw_node(node):
        ax.clear()
        plt.style.use('classic')
        ax.grid(True, linestyle='--', alpha=0.6)

        # Dibujar todos los nodos
        for n in g.nodes:
            color = "green" if n == node else "blue"
            size = 50 if n == node else 30
            alpha = 1.0 if n == node else 0.6
            
            ax.scatter(
                x=n.x,
                y=n.y,
                s=size,
                c=color,
                edgecolors="black",
                linewidths=0.5,
                alpha=alpha
            )
            
            # Mostrar nombre solo para nodos relevantes
            if n == node or n in node.neighbors:
                ax.text(
                    x=n.x + 0.05,
                    y=n.y + 0.05,
                    s=n.name,
                    fontsize=7,
                    alpha=0.9
                )

        visited = set()

        # Función auxiliar para dibujar caminos recursivamente
        def draw_paths(current_node):
            visited.add(current_node.name)
            for neighbor in current_node.neighbors:
                # Dibujar la arista entre current_node y neighbor
                ax.annotate("",
                    xy=(neighbor.x, neighbor.y),
                    xytext=(current_node.x, current_node.y),
                    arrowprops=dict(
                        arrowstyle="->",
                        color="green",
                        lw=0.8,
                        alpha=0.8,
                        shrinkA=5,
                        shrinkB=5,
                    ),
                    annotation_clip=False
                )
                
                # Mostrar distancia
                dx = neighbor.x - current_node.x
                dy = neighbor.y - current_node.y
                dist = sqrt(dx**2 + dy**2)
                
                if dist > 0.7:
                    ax.text(
                        x=(current_node.x + neighbor.x)/2,
                        y=(current_node.y + neighbor.y)/2,
                        s=f"{Distance(current_node, neighbor):.1f}",
                        fontsize=7,
                        alpha=0.8
                    )

                if neighbor.name not in visited:
                    draw_paths(neighbor)

        draw_paths(node)

        ax.set_title(f"Caminos desde {node.name}", pad=20)
        ax.set_xlabel("Longitud")
        ax.set_ylabel("Latitud")
        plt.tight_layout()

    # Resto del código permanece igual...
    def on_click(event: MouseEvent):
        nonlocal current_node
        if event.xdata is None or event.ydata is None:
            return
        
        clicked_node = None
        min_dist = float('inf')
        
        # Comprobar si se ha hecho clic en algún nodo con tolerancia más estricta
        for node in g.nodes:
            dist = sqrt((event.xdata - node.x)**2 + (event.ydata - node.y)**2)
            if dist < 0.2 and dist < min_dist:  # Radio de tolerancia más pequeño
                min_dist = dist
                clicked_node = node
        
        if clicked_node:
            if current_node == clicked_node:
                current_node = None
            else:
                current_node = clicked_node
        
        if current_node is None:
            draw_graph()
        else:
            draw_node(current_node)
        
        fig.canvas.draw_idle()  # Mejor rendimiento para actualización
    
    # Inicializar con el grafo completo
    draw_graph()
    fig.canvas.mpl_connect('button_press_event', on_click)
    plt.tight_layout()
    
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


