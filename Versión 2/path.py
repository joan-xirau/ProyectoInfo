
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
        """Genera la visualización del camino en el grafo"""
        fig, ax = plt.subplots()
        
        # Dibujar todos los nodos
        for node in graph.nodes:
            ax.scatter(
                x=node.x,
                y=node.y,
                s=100,
                c="blue",
                edgecolors="black",
                linewidths=1
            )
            ax.text(
                x=node.x + 0.5,
                y=node.y + 0.5,
                s=node.name
            )
        
        # Dibujar todos los segmentos (en gris claro)
        for segment in graph.segments:
            ax.arrow(
                x=segment.origin.x,
                y=segment.origin.y,
                dx=(segment.destination.x - segment.origin.x),
                dy=(segment.destination.y - segment.origin.y),
                color="lightgray",
                width=0.005,
                head_width=0.35,
                length_includes_head=True,
            )
        
        # Dibujar el camino (en rojo)
        for i in range(len(self.nodes)-1):
            current_name = self.nodes[i]
            next_name = self.nodes[i+1]
            
            current_node = next(n for n in graph.nodes if n.name == current_name)
            next_node = next(n for n in graph.nodes if n.name == next_name)
            
            ax.arrow(
                x=current_node.x,
                y=current_node.y,
                dx=(next_node.x - current_node.x),
                dy=(next_node.y - current_node.y),
                color="red",
                width=0.01,
                head_width=0.5,
                length_includes_head=True,
            )
        
        ax.set_title(f"Camino {self.name}" if self.name else "Visualización del Camino")
        ax.set_xlabel("Coordenada X")
        ax.set_ylabel("Coordenada Y")
        ax.grid(True)
        
        return fig

    def __str__(self):
        return f"Path '{self.name}': {' -> '.join(self.nodes)}"
    
    
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
