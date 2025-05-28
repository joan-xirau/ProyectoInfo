from path import *
from test_graph import CreateGraph_1
import matplotlib.pyplot as plt

def test_path_class():
    # Crear un grafo de prueba
    G = CreateGraph_1()
    
    # Crear un camino
    camino = Path("Camino de prueba")
    
    # Añadir nodos al camino
    node_a = next(n for n in G.nodes if n.name == "A")
    node_b = next(n for n in G.nodes if n.name == "B")
    node_c = next(n for n in G.nodes if n.name == "C")
    node_d = next(n for n in G.nodes if n.name == "D")
    
    camino.add_node(node_a)
    camino.add_node(node_b)
    camino.add_node(node_c)
    
    print("\n--- Probando la clase Path ---")
    print(camino)
    
    # Probar contains_node
    print(f"\n¿El camino contiene el nodo B? {camino.contains_node(node_b)}")
    print(f"¿El camino contiene el nodo D? {camino.contains_node(node_d)}")
    
    # Probar cost_to_node
    print(f"\nCoste hasta el nodo B: {camino.cost_to_node(node_b, G)}")
    print(f"Coste hasta el nodo C: {camino.cost_to_node(node_c, G)}")
    print(f"Coste hasta el nodo D: {camino.cost_to_node(node_d, G)}")
    
    # Probar plot
    print("\nMostrando visualización del camino...")
    fig = camino.plot(G)
    plt.show()  # Usamos plt.show() en lugar de fig.show()

def test_shortest_path():
    G = CreateGraph_1()
    
    # Probar shortest_path (función original)
    print("\n--- Probando shortest_path ---")
    path_nodes = shortest_path(G, "A", "I")
    print(f"Camino más corto de A a I: {path_nodes}")
    
    if path_nodes:
        # Crear un objeto Path a partir del resultado
        camino_corto = Path("Camino más corto A-I", path_nodes)
        print(camino_corto)
        
        # Mostrar el camino
        fig = camino_corto.plot(G)
        plt.show()  # Usamos plt.show() en lugar de fig.show()
    else:
        print("No hay camino entre A e I")

if __name__ == "__main__":
    test_path_class()
    test_shortest_path()