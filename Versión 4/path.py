
from node import *
import matplotlib.pyplot as plt
from heapq import heappop, heappush
import time
from math import sqrt



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
        plt.style.use('classic')
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

import time  # Asegúrate de importar time si no lo has hecho

def shortest_path_original(g, start_name, end_name):
    start_time = time.time()

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

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Algoritmo original ejecutado en {elapsed_time:.4f} segundos")

    if distances[end_name] == float('inf'):
        return None, elapsed_time  # No hay camino
    return path, elapsed_time




def dijkstra_shortest_path(g, start_name, end_name):
    """Implementación optimizada de Dijkstra usando heap"""
    start_time = time.time()
    
    # Inicialización
    distances = {node.name: float('inf') for node in g.nodes}
    previous = {node.name: None for node in g.nodes}
    distances[start_name] = 0
    
    heap = [(0, start_name)]
    
    while heap:
        current_distance, current_name = heappop(heap)
        
        if current_distance > distances[current_name]:
            continue
        
        if current_name == end_name:
            break
        
        current_node = next(n for n in g.nodes if n.name == current_name)
        
        for neighbor in current_node.neighbors:
            distance = current_distance + Distance(current_node, neighbor)
            
            if distance < distances[neighbor.name]:
                distances[neighbor.name] = distance
                previous[neighbor.name] = current_name
                heappush(heap, (distance, neighbor.name))
    
    # Reconstruir el camino
    path = []
    current = end_name
    while current is not None:
        path.insert(0, current)
        current = previous[current]
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Dijkstra ejecutado en {elapsed_time:.4f} segundos")
    
    if distances[end_name] == float('inf'):
        return None, elapsed_time
    return path, elapsed_time


def a_star_shortest_path(g, start_name, end_name):
    """Implementación de A* para potencialmente mejor rendimiento"""
    start_time = time.time()

    def heuristic(node_name):
        node = next(n for n in g.nodes if n.name == node_name)
        end_node = next(n for n in g.nodes if n.name == end_name)
        return Distance(node, end_node)
    
    open_set = set([start_name])
    came_from = {}

    g_score = {node.name: float('inf') for node in g.nodes}
    g_score[start_name] = 0

    f_score = {node.name: float('inf') for node in g.nodes}
    f_score[start_name] = heuristic(start_name)

    open_heap = [(f_score[start_name], start_name)]

    while open_heap:
        _, current_name = heappop(open_heap)

        if current_name == end_name:
            path = []
            while current_name in came_from:
                path.insert(0, current_name)
                current_name = came_from[current_name]
            path.insert(0, start_name)

            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"A* ejecutado en {elapsed_time:.4f} segundos")
            return path, elapsed_time
        
        open_set.remove(current_name)
        current_node = next(n for n in g.nodes if n.name == current_name)

        for neighbor in current_node.neighbors:
            tentative_g_score = g_score[current_name] + Distance(current_node, neighbor)

            if tentative_g_score < g_score[neighbor.name]:
                came_from[neighbor.name] = current_name
                g_score[neighbor.name] = tentative_g_score
                f_score[neighbor.name] = g_score[neighbor.name] + heuristic(neighbor.name)

                if neighbor.name not in open_set:
                    open_set.add(neighbor.name)
                    heappush(open_heap, (f_score[neighbor.name], neighbor.name))
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"A* ejecutado en {elapsed_time:.4f} segundos")
    return None, elapsed_time



CURRENT_ALGORITHM = "dijkstra"  

def set_algorithm(algorithm):
    global CURRENT_ALGORITHM
    CURRENT_ALGORITHM = algorithm

def shortest_path(g, start_name, end_name):
    if CURRENT_ALGORITHM == "dijkstra":
        return dijkstra_shortest_path(g, start_name, end_name)
    elif CURRENT_ALGORITHM == "astar":
        return a_star_shortest_path(g, start_name, end_name)
    else:
        return shortest_path_original(g, start_name, end_name)
