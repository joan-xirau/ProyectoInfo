
from node import *
import matplotlib.pyplot as plt

class Path:
    def __init__(self, name="", nodes=None):
        self.name = name
        self.nodes = nodes if nodes is not None else []
    
    def add_node(self, node):
        """Añade un nodo al final del camino"""
        self.nodes.append(node.name)
        return self
    
    def contains_node(self, node):
        """Comprueba si el nodo está en el camino"""
        return node.name in self.nodes
    
    def cost_to_node(self, node, graph):
        """
        Calcula el coste total desde el origen del camino hasta el nodo especificado.
        Devuelve -1 si el nodo no está en el camino.
        """
        if not self.contains_node(node):
            return -1
        
        total_cost = 0
        for i in range(len(self.nodes)-1):
            current_name = self.nodes[i]
            next_name = self.nodes[i+1]
            
            current_node = next(n for n in graph.nodes if n.name == current_name)
            next_node = next(n for n in graph.nodes if n.name == next_name)
            
            total_cost += Distance(current_node, next_node)
            
            if next_name == node.name:
                return total_cost
        
        return total_cost
    
    def plot(self, graph):
        """Genera la visualización del camino en el grafo con el nuevo estilo"""
        fig, ax = plt.subplots(figsize=(12, 8))
        plt.style.use('seaborn')
        ax.grid(True, linestyle='--', alpha=0.6)

        # Dibujar todos los nodos
        for node in graph.nodes:
            # Nodos normales en azul claro
            ax.scatter(
                x=node.x,
                y=node.y,
                s=30,
                c="lightblue",
                edgecolors="black",
                linewidths=0.5,
                alpha=0.6
            )
            # Mostrar nombre solo si hay espacio
            nearest_dist = min(
                sqrt((node.x - n.x)**2 + (node.y - n.y)**2)
                for n in graph.nodes if n != node
            )
            if nearest_dist > 0.5:
                ax.text(
                    x=node.x + 0.05,
                    y=node.y + 0.05,
                    s=node.name,
                    fontsize=6,
                    alpha=0.7
                )

        # Dibujar todos los segmentos (en gris claro)
        for segment in graph.segments:
            ax.annotate("",
                xy=(segment.destination.x, segment.destination.y),
                xytext=(segment.origin.x, segment.origin.y),
                arrowprops=dict(
                    arrowstyle="-",  # Sin punta de flecha
                    color="lightgray",
                    lw=0.3,
                    alpha=0.4,
                    shrinkA=5,
                    shrinkB=5,
                ),
                annotation_clip=False
            )

        # Dibujar el camino (en rojo)
        for i in range(len(self.nodes)-1):
            current_name = self.nodes[i]
            next_name = self.nodes[i+1]
            
            current_node = next(n for n in graph.nodes if n.name == current_name)
            next_node = next(n for n in graph.nodes if n.name == next_name)
            
            # Flecha del camino
            ax.annotate("",
                xy=(next_node.x, next_node.y),
                xytext=(current_node.x, current_node.y),
                arrowprops=dict(
                    arrowstyle="->",
                    color="red",
                    lw=1.2,
                    alpha=0.9,
                    shrinkA=5,
                    shrinkB=5,
                ),
                annotation_clip=False
            )
            
            # Texto con la distancia
            dx = next_node.x - current_node.x
            dy = next_node.y - current_node.y
            dist = sqrt(dx**2 + dy**2)
            if dist > 0.7:
                ax.text(
                    x=(current_node.x + next_node.x)/2,
                    y=(current_node.y + next_node.y)/2,
                    s=f"{dist:.1f}",
                    fontsize=7,
                    color="red",
                    alpha=0.9,
                    bbox=dict(
                        facecolor='white',
                        edgecolor='none',
                        alpha=0.7,
                        boxstyle='round,pad=0.2'
                    )
                )

        # Resaltar nodos del camino
        for node_name in self.nodes:
            node = next(n for n in graph.nodes if n.name == node_name)
            ax.scatter(
                x=node.x,
                y=node.y,
                s=50,
                c="red",
                edgecolors="black",
                linewidths=0.7,
                alpha=1.0
            )
            ax.text(
                x=node.x + 0.07,
                y=node.y + 0.07,
                s=node.name,
                fontsize=7,
                color="red",
                alpha=1.0,
                weight='bold'
            )

        ax.set_title(f"Camino {self.name}" if self.name else "Mejor Camino", pad=20)
        ax.set_xlabel("Longitud")
        ax.set_ylabel("Latitud")
        plt.tight_layout()
        
        return fig
    
def reachable_nodes(g, node_name, reached=None):
    if reached is None:
        reached = set()

    # Buscar el nodo de inicio
    start_node = None
    for node_in_graph in g.nodes:
        if node_in_graph.name == node_name:
            start_node = node_in_graph
            break

    if start_node is None:
        return reached  # Nodo no encontrado en el grafo

    if start_node.name in reached:
        return reached  # Ya fue visitado

    reached.add(start_node.name)

    for neighbor in start_node.neighbors:
        reachable_nodes(g, neighbor.name, reached)

    return reached

def shortest_path(g, start_name, end_name):
    # Inicializar distancias y nodos previos
    distances = {node.name: float('inf') for node in g.nodes}
    previous = {node.name: None for node in g.nodes}
    unvisited = set(node.name for node in g.nodes)

    distances[start_name] = 0

    while unvisited:
        # Buscar el nodo no visitado con menor distancia
        current_name = min(unvisited, key=lambda name: distances[name])
        current_distance = distances[current_name]

        if current_name == end_name or current_distance == float('inf'):
            break

        # Buscar el objeto nodo en el grafo
        current_node = next(n for n in g.nodes if n.name == current_name)

        for neighbor in current_node.neighbors:
            if neighbor.name in unvisited:
                weight = Distance(current_node, neighbor)
                new_distance = current_distance + weight
                if new_distance < distances[neighbor.name]:
                    distances[neighbor.name] = new_distance
                    previous[neighbor.name] = current_name

        unvisited.remove(current_name)

    # Reconstruir el camino más corto
    path = []
    current = end_name
    while current is not None:
        path.insert(0, current)
        current = previous[current]

    if distances[end_name] == float('inf'):
        return None  # No hay camino

    return path
