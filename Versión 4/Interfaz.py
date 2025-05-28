import tkinter as tk


from graph import *
from path import *
from test_graph import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import simpledialog, messagebox
from os import *
from tkinter import ttk
import time
import random

def plot_example_1():
    global current_graph
    global canvas_widget

    
    try:
        current_graph = CreateGraph_1()
        
        if canvas_widget:
            canvas_widget.destroy()
        canvas = FigureCanvasTkAgg(Plot(current_graph), master=left_frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        
    except Exception as e:
        messagebox.showerror("ERROR", f"No se pudo cargar el archivo: {str(e)}")

def plot_example_2():
    global current_graph
    global canvas_widget

    
    try:
        current_graph = CreateGraph_2()
        
        if canvas_widget:
            canvas_widget.destroy()
        canvas = FigureCanvasTkAgg(Plot(current_graph), master=left_frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        
    except Exception as e:
        messagebox.showerror("ERROR", f"No se pudo cargar el archivo: {str(e)}")

def Instrucciones():
    # Crear ventana emergente
    instrucciones_window = tk.Toplevel()
    instrucciones_window.title("Instrucciones de Uso")
    instrucciones_window.geometry("800x600")
    
    # Crear un widget Text con scrollbar
    text_frame = tk.Frame(instrucciones_window)
    text_frame.pack(fill=tk.BOTH, expand=True)
    
    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    text_widget = tk.Text(text_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
    text_widget.pack(fill=tk.BOTH, expand=True)
    
    scrollbar.config(command=text_widget.yview)
    
    # Contenido de las instrucciones
    instrucciones = """
    INTERFAZ GRÁFICA DE GRAFOS - MANUAL DE USO

    1. CARGA DE GRAFOS
    -----------------
    - Ejemplo 1/2: Carga grafos de ejemplo predefinidos
    - Grafo en Blanco: Crea un grafo vacío para construir manualmente
    - Subir Archivo: Carga un grafo desde 3 archivos (_nav.txt, _seg.txt, _aer.txt)
    - Cargar Cataluña/España/Europa: Carga grafos predefinidos de estas regiones

    2. EDICIÓN DEL GRAFO
    -------------------
    - Añadir Nodo: Introduce "nombre x y" en el campo de texto y pulsa el botón
    - Eliminar Nodo: Introduce el nombre del nodo y pulsa el botón
    - Añadir Segmento: Introduce "nombre origen destino" y pulsa el botón
    - Eliminar Segmento: Introduce el nombre del segmento y pulsa el botón
    - Guardar Archivo: Guarda el grafo actual en un archivo de texto

    3. OPERACIONES CON CAMINOS
    -------------------------
    - Mejor Camino: Introduce "origen destino" para encontrar el camino más corto
    - Añadir a Camino: Añade nodos a un camino personalizado
    - Contiene Nodo: Comprueba si un nodo está en el camino actual
    - Coste a Nodo: Muestra el coste acumulado hasta un nodo en el camino

    4. VISUALIZACIÓN KML
    -------------------
    - Guardar KML: Exporta el grafo a un archivo KML para Google Earth
    - Ejecutar KML: Abre directamente el archivo KML generado

    5. ALGORITMOS DISPONIBLES
    ------------------------
    - Dijkstra: Algoritmo clásico de caminos mínimos
    - A*: Algoritmo heurístico para caminos mínimos
    - Original: Algoritmo básico de búsqueda de caminos

    INSTRUCCIONES DETALLADAS:
    ------------------------
    1. Para crear un grafo manualmente:
       - Pulsa "Grafo en Blanco"
       - Crea los dor primero nodos
       - Añade nodos con sus coordenadas (ej: "A 10 20")
       - Conecta nodos con segmentos (ej: "S1 A B")

    2. Para encontrar caminos:
       - Carga un grafo existente
       - Introduce dos nodos separados por espacio (ej: "A B")
       - Pulsa "Mejor Camino" para visualizar la ruta óptima

    3. Para crear un grafo al azar:
       - Introducir en la primera ventana el número de nodos y segmentos
       - En la segunda ventana, la x_min y la x_max
       - Y en la tercera ventana, la y_min y la y_maz

    4. Para exportar a Google Earth:
       - Carga o crea un grafo
       - Pulsa "Guardar KML" e introduce un nombre
       - Usa "Ejecutar KML" para visualizarlo en Google Earth


    


    CONSEJOS:
    - Los nombres de nodos deben ser únicos
    - Las coordenadas son valores numéricos
    - Para grafos grandes, las operaciones pueden tardar unos segundos
    - Puedes combinar grafos predefinidos con nodos manuales
    """
    
    # Insertar texto y configurar para solo lectura
    text_widget.insert(tk.END, instrucciones)
    text_widget.config(state=tk.DISABLED)
    
    # Botón de cierre
    close_button = tk.Button(instrucciones_window, text="Cerrar", 
                           command=instrucciones_window.destroy)
    close_button.pack(pady=10)


def load_Cat():
    global current_graph
    global canvas_widget

def load_file_3_files():
    global current_graph
    global canvas_widget


    
    # Ask for base filename (without extension)
    base_name = simpledialog.askstring("Cargar Archivo", "Nombre base del archivo (sin extensión)")
    
    if not base_name:
        return
    
    start_time = time.time()

    
    nav_file = f"{base_name}_nav.txt"
    seg_file = f"{base_name}_seg.txt"
    aer_file = f"{base_name}_aer.txt"
    
    try:
        current_graph = graph()
        current_graph.load_airspace(nav_file, seg_file, aer_file)   

        
        if canvas_widget:
            canvas_widget.destroy()
        canvas = FigureCanvasTkAgg(Plot(current_graph), master=left_frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        messagebox.showinfo("Cargado con Éxito", f"Se ha cargado el archivo en {round(elapsed_time,5)} segundos")

    except Exception as e:
        messagebox.showerror("ERROR", f"No se pudo cargar el archivo: {str(e)}")

def load_Cat():
    global current_graph
    global canvas_widget


    
    # Ask for base filename (without extension)
    base_name = "Cat"
    start_time = time.time()

    
    nav_file = f"{base_name}_nav.txt"
    seg_file = f"{base_name}_seg.txt"
    aer_file = f"{base_name}_aer.txt"
    
    try:
        current_graph = graph()
        current_graph.load_airspace(nav_file, seg_file, aer_file)   

        
        if canvas_widget:
            canvas_widget.destroy()
        canvas = FigureCanvasTkAgg(Plot(current_graph), master=left_frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        messagebox.showinfo("Cargado con Éxito", f"Se ha cargado el archivo en {round(elapsed_time,5)} segundos")

    except Exception as e:
        messagebox.showerror("ERROR", f"No se pudo cargar el archivo: {str(e)}")


def load_Spain():
    global current_graph
    global canvas_widget


    
    # Ask for base filename (without extension)
    base_name = "Spain"
    start_time = time.time()

    
    nav_file = f"{base_name}_nav.txt"
    seg_file = f"{base_name}_seg.txt"
    aer_file = f"{base_name}_aer.txt"
    
    try:
        current_graph = graph()
        current_graph.load_airspace(nav_file, seg_file, aer_file)   

        
        if canvas_widget:
            canvas_widget.destroy()
        canvas = FigureCanvasTkAgg(Plot(current_graph), master=left_frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        messagebox.showinfo("Cargado con Éxito", f"Se ha cargado el archivo en {round(elapsed_time,5)} segundos")

    except Exception as e:
        messagebox.showerror("ERROR", f"No se pudo cargar el archivo: {str(e)}")


def load_Europe():
    global current_graph
    global canvas_widget


    
    # Ask for base filename (without extension)
    base_name = "ECAC"
    start_time = time.time()

    
    nav_file = f"{base_name}_nav.txt"
    seg_file = f"{base_name}_seg.txt"
    aer_file = f"{base_name}_aer.txt"
    
    try:
        current_graph = graph()
        current_graph.load_airspace(nav_file, seg_file, aer_file)   

        
        if canvas_widget:
            canvas_widget.destroy()
        canvas = FigureCanvasTkAgg(Plot(current_graph), master=left_frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        messagebox.showinfo("Cargado con Éxito", f"Se ha cargado el archivo en {round(elapsed_time,5)} segundos")

    except Exception as e:
        messagebox.showerror("ERROR", f"No se pudo cargar el archivo: {str(e)}")




def save_file():
    global current_graph
    
    file_name = simpledialog.askstring("Cargar Archivo", "Nombre del Archivo")
    archivo = open(file_name, "w", encoding="utf-8")
    archivo.write(f"NODES \n\n")
    for node_in_graph in current_graph.nodes:
        archivo.write(f"{node_in_graph.name} {node_in_graph.x} {node_in_graph.y} \n")
    archivo.write(f"SEGMENTS \n\n")
    for segment_in_graph in current_graph.segments:
        archivo.write(f"{segment_in_graph.name} {segment_in_graph.origin.name} {segment_in_graph.destination.name} \n")    

    archivo.close() 


def add_node_button():
    global current_graph
    global canvas_widget
    global entry

    if current_graph:
        repeated = False
        information = list(entry.get().split(" "))
        for node_in_graph in current_graph.nodes:
            if node_in_graph.name == information[0]:
                    repeated = True
                    break
        if repeated:
            messagebox.showwarning("ERROR", "Ya existe un nodo con ese nombre")
        else:
                info_node = node(information[0], information[1], information[2])           
                AddNode(current_graph, info_node)
                if canvas_widget:
                    canvas_widget.destroy()
                canvas = FigureCanvasTkAgg(Plot(current_graph), master = left_frame)
                canvas.draw()
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.pack(fill=tk.BOTH, expand=True)
    else:
        current_graph = graph()
        repeated = False
        information = list(entry.get().split(" "))
        for node_in_graph in current_graph.nodes:
            if node_in_graph.name == information[0]:
                    repeated = True
                    break
        if repeated:
            messagebox.showwarning("ERROR", "Ya existe un nodo con ese nombre")
        else:
                info_node = node(information[0], information[1], information[2])           
                AddNode(current_graph, info_node)
                if canvas_widget:
                    canvas_widget.destroy()
                canvas = FigureCanvasTkAgg(Plot(current_graph), master = left_frame)
                canvas.draw()
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.pack(fill=tk.BOTH, expand=True)




def del_node_button():
    global current_graph
    global canvas_widget
    global entry


    if current_graph:
        
        information = entry.get()
        delete_segments = []
        found = False
        try:
            for node_in_graph in current_graph.nodes:
                if node_in_graph.name == information:
                    for segment_in_graph in current_graph.segments:
                        if segment_in_graph.destination == node_in_graph or segment_in_graph.origin == node_in_graph:
                             delete_segments.append(segment_in_graph.name)

                    for to_delete in delete_segments:
                        DelSegment(current_graph, to_delete)


                    DelNode(current_graph, node_in_graph)
                    if canvas_widget:
                        canvas_widget.destroy()
                    canvas = FigureCanvasTkAgg(Plot(current_graph), master = left_frame)
                    canvas.draw()
                    canvas_widget = canvas.get_tk_widget()
                    canvas_widget.pack(fill=tk.BOTH, expand=True)
                    Found = True
                    break

        except:
             messagebox.showwarning("ERROR", "No se ha podido eliminar el nodo")
    else:
        messagebox.showwarning("ERROR", "No existe ningún grafo")



def add_segment_button():
    global current_graph
    global canvas_widget
    global entry

    if current_graph:
        repeated = False
        information = list(entry.get().split(" "))
        for segment_in_graph in current_graph.segments:
            if segment_in_graph.name == information[0]:
                    repeated = True
                    break
        if repeated:
            messagebox.showwarning("ERROR", "Ya existe un segmento con ese nombre")
        else:
            try:
                founded_node1 = None
                founded_node2 = None
                for node_in_graph in current_graph.nodes:
                    if node_in_graph.name == information[1]:
                        founded_node1 = node_in_graph
                    elif node_in_graph.name == information[2]:
                         founded_node2 = node_in_graph
                
                if founded_node1 and founded_node2:
                    info_segment = segment(information[0], founded_node1, founded_node2)           
                    AddSegment(current_graph, information[0], founded_node1.name, founded_node2.name)
                    if canvas_widget:
                        canvas_widget.destroy()
                    canvas = FigureCanvasTkAgg(Plot(current_graph), master = left_frame)
                    canvas.draw()
                    canvas_widget = canvas.get_tk_widget()
                    canvas_widget.pack(fill=tk.BOTH, expand=True)
                else:
                    messagebox.showwarning("ERROR", "No se ha encontrado uno de los nodos")
            except:
                messagebox.showwarning("ERROR", "No se ha podido crear el segmento")
    else:
        messagebox.showwarning("ERROR", "No existe ningún grafo")
     




def del_segment_button():
    global current_graph
    global canvas_widget
    global entry
    found = False

    if current_graph:
        information = entry.get()
        for segment_in_graph in current_graph.segments:
            if segment_in_graph.name == information:
                found = True   

        if found:
            DelSegment(current_graph, information )
            if canvas_widget:
                canvas_widget.destroy()
            canvas = FigureCanvasTkAgg(Plot(current_graph), master = left_frame)
            canvas.draw()
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(fill=tk.BOTH, expand=True)



        else:
            messagebox.showwarning("ERROR", "No existe ningún segmento con ese nombre")
    else:
        messagebox.showwarning("ERROR", "No existe ningún grafo")


def plot_shortest_path():
    global current_graph
    global canvas_widget
    global entry
    global current_path

    # Verificar que hay un grafo cargado
    if not current_graph or not current_graph.nodes:
        messagebox.showwarning("ERROR", "No hay grafo cargado")
        return

    # Obtener y validar los nodos de entrada
    information = entry.get().strip().split()
    if len(information) != 2:
        messagebox.showwarning("ERROR", "Debe ingresar exactamente dos nodos (origen y destino) separados por espacio")
        return

    start_node, end_node = information[0], information[1]

    # Verificar que los nodos existen en el grafo
    node_names = [node.name for node in current_graph.nodes]
    if start_node not in node_names:
        messagebox.showwarning("ERROR", f"El nodo {start_node} no existe en el grafo")
        return
    if end_node not in node_names:
        messagebox.showwarning("ERROR", f"El nodo {end_node} no existe en el grafo")
        return

    # Encontrar el camino más corto
    try:
        camino, tiempo = shortest_path(current_graph, start_node, end_node)
        
        if not camino:
            messagebox.showwarning("ERROR", f"No existe camino entre {start_node} y {end_node}")
            return

        # Crear y mostrar el camino
        path_obj = Path(f"De {start_node} a {end_node}", camino)
        
        # Actualizar el camino actual
        global current_path
        current_path = path_obj
        
        if canvas_widget:
            canvas_widget.destroy()
        
        # Usar el nuevo estilo de visualización
        canvas = FigureCanvasTkAgg(path_obj.plot(current_graph), master=left_frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        
        # Mostrar información del camino
        total_cost = sum(
            Distance(
                next(n for n in current_graph.nodes if n.name == camino[i]),
                next(n for n in current_graph.nodes if n.name == camino[i+1])
            )
            for i in range(len(camino)-1)
        )
        messagebox.showinfo("Camino encontrado", 
            f"Camino más corto: {' -> '.join(camino)}\n"
            f"Coste total: {total_cost:.2f} km\n"
            f"Tiempo: {round(tiempo,7)} segundos")

        
    except Exception as e:
        messagebox.showerror("ERROR", f"Error al calcular el camino: {str(e)}")


def plot_blank_graph():
    global current_graph
    global canvas_widget

    current_graph = graph()

    node_1 = simpledialog.askstring("Nodo 1", "Información del Nodo 1").split()
    messagebox.showinfo("INFOR", "Nodo guardado con éxito")
    AddNode(current_graph, node(node_1[0],  int(node_1[1]),int(node_1[2])))

    node_2 = simpledialog.askstring("Nodo 1", "Información del Nodo 2").split()
    messagebox.showinfo("INFOR", "Nodo guardado con éxito")
    AddNode(current_graph, node(node_2[0],  int(node_2[1]),int(node_2[2])))


    if canvas_widget:
        canvas_widget.destroy()
    canvas = FigureCanvasTkAgg(Plot(current_graph), master=left_frame)
    canvas.draw()
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)

         
def add_node_to_path():
    global current_graph
    global canvas_widget
    global entry
    global current_path  # Necesitamos una variable global para mantener el camino actual

    if not current_graph:
        messagebox.showwarning("ERROR", "No hay grafo cargado")
        return

    node_name = entry.get().strip()
    if not node_name:
        messagebox.showwarning("ERROR", "Debe ingresar un nombre de nodo")
        return

    # Buscar el nodo en el grafo
    node_found = next((n for n in current_graph.nodes if n.name == node_name), None)
    if not node_found:
        messagebox.showwarning("ERROR", f"El nodo {node_name} no existe en el grafo")
        return

    # Inicializar el camino si no existe
    if 'current_path' not in globals():
        global current_path
        current_path = Path("Camino personalizado")
    
    # Añadir el nodo al camino
    current_path.add_node(node_found)
    messagebox.showinfo("Éxito", f"Nodo {node_name} añadido al camino")

    # Mostrar el camino actual
    if canvas_widget:
        canvas_widget.destroy()
    
    canvas = FigureCanvasTkAgg(current_path.plot(current_graph), master=left_frame)
    canvas.draw()
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)

def check_contains_node():
    global current_graph
    global entry
    global current_path

    if not current_graph:
        messagebox.showwarning("ERROR", "No hay grafo cargado")
        return

    node_name = entry.get().strip()
    if not node_name:
        messagebox.showwarning("ERROR", "Debe ingresar un nombre de nodo")
        return

    # Buscar el nodo en el grafo
    node_found = next((n for n in current_graph.nodes if n.name == node_name), None)
    if not node_found:
        messagebox.showwarning("ERROR", f"El nodo {node_name} no existe en el grafo")
        return

    # Verificar si tenemos un camino
    if 'current_path' not in globals() or not current_path.nodes:
        messagebox.showinfo("Resultado", f"No hay camino creado o está vacío")
        return

    # Verificar si el nodo está en el camino
    if current_path.contains_node(node_found):
        messagebox.showinfo("Resultado", f"El nodo {node_name} SÍ está en el camino")
    else:
        messagebox.showinfo("Resultado", f"El nodo {node_name} NO está en el camino")

def show_cost_to_node():
    global current_graph
    global entry
    global current_path

    if not current_graph:
        messagebox.showwarning("ERROR", "No hay grafo cargado")
        return

    node_name = entry.get().strip()
    if not node_name:
        messagebox.showwarning("ERROR", "Debe ingresar un nombre de nodo")
        return

    # Buscar el nodo en el grafo
    node_found = next((n for n in current_graph.nodes if n.name == node_name), None)
    if not node_found:
        messagebox.showwarning("ERROR", f"El nodo {node_name} no existe en el grafo")
        return

    # Verificar si tenemos un camino
    if 'current_path' not in globals() or not current_path.nodes:
        messagebox.showinfo("Resultado", f"No hay camino creado o está vacío")
        return

    # Calcular el coste hasta el nodo
    cost = current_path.cost_to_node(node_found, current_graph)
    if cost == -1:
        messagebox.showinfo("Resultado", f"El nodo {node_name} no está en el camino")
    else:
        messagebox.showinfo("Resultado", f"Coste hasta el nodo {node_name}: {cost:.2f}")

def plot_random_graph():
    global current_graph
    global canvas_widget
    global entry
    global current_path




    current_graph = graph()
    n,m  = list(map(int,simpledialog.askstring("Inserte Información", "Número de nodos y segmentos").split()))
    messagebox.showinfo("INFO", "Información guardada con éxito")
    x_min,x_max  = list(map(int,simpledialog.askstring("Inserte Información", "X_min y X_max").split()))
    messagebox.showinfo("INFO", "Información guardada con éxito")
    y_min,y_max  = list(map(int,simpledialog.askstring("Inserte Información", "Y_min y Y_max").split()))
    messagebox.showinfo("INFO", "Información guardada con éxito")

    nombres = []
    i = 0
    while len(nombres) < n:
        etiqueta = ""
        temp = i
        while True:
            etiqueta = chr(65 + (temp % 26)) + etiqueta
            temp = temp // 26 - 1
            if temp < 0:
                break
        nombres.append(etiqueta)
        i += 1


    # Crear nodos
    for i in range(n):
        nombre = nombres[i]
        x = random.uniform(x_min, x_max)
        y = random.uniform(y_min, y_max)
        AddNode(current_graph, node(nombre, x, y))

    for i in range(m):
        n1, n2 = random.sample(current_graph.nodes, 2)
        AddSegment(current_graph, f"{n1.name} + {n2.name}", n1.name, n2.name)

            
    if canvas_widget:
        canvas_widget.destroy()
    canvas = FigureCanvasTkAgg(Plot(current_graph), master=left_frame)
    canvas.draw()
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)



def create_kml():
    global current_graph
    global canvas_widget
    
    # Ask for base filename (without extension)
    base_name = simpledialog.askstring("Guardar Archivo", "Nombre base del archivo")
    if not base_name:
        return
    
    try:
  
        # Generar archivo KML
        kml_file = current_graph.airspace.generate_kml(f"{base_name}_airspace.kml")
        messagebox.showinfo("Éxito", f"Archivo KML generado: {kml_file}")

        
    except Exception as e:
        messagebox.showerror("ERROR", f"No se pudo generar el archivo: {str(e)}")

def execute_kml():

    
    # Ask for base filename (without extension)
    base_name = simpledialog.askstring("Ejecutar Archivo", "Nombre base del archivo (sin la extensión)")
    if not base_name:
        return
    
    try:
  
        # Generar archivo KML
        kml_file = f"{base_name}_airspace.kml"
        os.startfile(kml_file)
        messagebox.showinfo("Éxito", f"Archivo KML ejecutado")

        
    except Exception as e:
        messagebox.showerror("ERROR", f"No se pudo ejecutar el archivo: {str(e)}")



#Interfaz Gráfica
ventana = tk.Tk()
ventana.title("Interfaz Gráfica")
ventana.geometry("900x600")

ventana.columnconfigure(0 , weight= 4)
ventana.columnconfigure(1,weight = 1)
ventana.rowconfigure(0, weight = 1)

canvas_widget = None
current_graph = None

#Frame Izquierdo

left_frame = tk.LabelFrame(master = ventana, bg = "lightgreen", relief = "groove" , bd = 10 , text = "Grafo" , font=("Arial", 12))
left_frame.grid(column = 0, row = 0, padx= 0, pady=0,
                sticky = "nsew")
left_frame.grid_propagate(False)

#Frame Derecho

right_frame = tk.Frame(master = ventana, bg = "lightblue", relief = "groove" , bd = 10)
right_frame.grid(column = 1, row = 0, padx= 0, pady=0,
                sticky = "nsew")

right_frame.columnconfigure(0, weight = 1)
right_frame.rowconfigure(0, weight = 2)
right_frame.rowconfigure(1, weight = 2)
right_frame.rowconfigure(2, weight = 4)
right_frame.rowconfigure(3, weight = 1)

#Frame Archivos
files_frame = tk.LabelFrame(master = right_frame, bg = "#d8e6ad", relief = "groove" , bd = 10 , text = "Formato 3 Arhcivos" , font=("Arial", 12))
files_frame.grid(column = 0, row = 0, padx= 5, pady=5,
                sticky = "nsew")

files_frame.columnconfigure(0, weight = 1)
files_frame.columnconfigure(1, weight = 1)
files_frame.rowconfigure(0, weight =  1)    
files_frame.rowconfigure(1, weight = 1)


# Botones que llenan completamente el frame
example_1_button = tk.Button(master=files_frame, text="Ejemplo 1", command= plot_example_1)
example_1_button.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")
    
example_2_button = tk.Button(master=files_frame, text="Ejemplo 2", command= plot_example_2)
example_2_button.grid(column=1, row=0, padx=5, pady=5, sticky="nsew")

Instrucciones_button = tk.Button(master=files_frame, text="Instrucciones", command= Instrucciones)
Instrucciones_button.grid(column=0, row=1, padx=5, pady=5, sticky="nsew")

save_button = tk.Button(master=files_frame, text="Guardar Archivo", command= save_file)
save_button.grid(column=1, row=1, padx=5, pady=5, sticky="nsew")




#Frame 3 Archivos
files_frame = tk.LabelFrame(master = right_frame, bg = "#e6add8", relief = "groove" , bd = 10 , text = "Formato 3 Arhcivos" , font=("Arial", 12))
files_frame.grid(column = 0, row = 1, padx= 5, pady=5,
                sticky = "nsew")

files_frame.columnconfigure(0, weight = 1)
files_frame.columnconfigure(1, weight = 1)
files_frame.rowconfigure(0, weight =  1)    
files_frame.rowconfigure(1, weight = 1)


# Botones que llenan completamente el frame
upload_button = tk.Button(master=files_frame, text="Subir Archivo", command= load_file_3_files)
upload_button.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")
    
cat_button = tk.Button(master=files_frame, text="Cargar Cataluña", command= load_Cat)
cat_button.grid(column=1, row=0, padx=5, pady=5, sticky="nsew")

spain_button = tk.Button(master=files_frame, text="Cargar España", command= load_Spain)
spain_button.grid(column=0, row=1, padx=5, pady=5, sticky="nsew")

europe_button = tk.Button(master=files_frame, text="Cargar Europa", command= load_Europe)
europe_button.grid(column=1, row=1, padx=5, pady=5, sticky="nsew")


#Frame Editar
edit_frame = tk.LabelFrame(master = right_frame, bg = "#d8e6ad", relief = "groove" , bd = 10 , text = "Editar Grafo" , font=("Arial", 12))
edit_frame.grid(column = 0, row = 2, padx= 5, pady=5,
                sticky = "nsew")

edit_frame.columnconfigure(0, weight=1)
edit_frame.columnconfigure(1, weight=1)

edit_frame.rowconfigure(0, weight=1)
edit_frame.rowconfigure(1, weight=1)
edit_frame.rowconfigure(2, weight=1)
edit_frame.rowconfigure(3, weight=2)

#Cambiar entre Algoritmos
algorithm_frame = tk.LabelFrame(master=edit_frame, bg="#add8e6", relief="groove", bd=5, text="Algoritmo", font=("Arial", 10))
algorithm_frame.grid(column=0, row=6, padx=5, pady=5, sticky="nsew", columnspan=2)

# Variables para los radio buttons
algorithm_var = tk.StringVar(value="dijkstra")

# Radio buttons
tk.Radiobutton(algorithm_frame, text="Dijkstra", variable=algorithm_var, value="dijkstra", 
               command=lambda: set_algorithm("dijkstra")).pack(anchor=tk.W)
tk.Radiobutton(algorithm_frame, text="A*", variable=algorithm_var, value="astar", 
               command=lambda: set_algorithm("astar")).pack(anchor=tk.W)
tk.Radiobutton(algorithm_frame, text="Original", variable=algorithm_var, value="original", 
               command=lambda: set_algorithm("original")).pack(anchor=tk.W)


#Funciones de nodo
addnode_button = tk.Button(master=edit_frame, text="Añadir Nodo", command=add_node_button)
addnode_button.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

delnode_button = tk.Button(master=edit_frame, text="Eliminar Nodo", command=del_node_button)
delnode_button.grid(column=0, row=1, padx=5, pady=5, sticky="nsew")

#Funciones de segmento
addsegment_button = tk.Button(master=edit_frame, text="Añadir Segmento", command= add_segment_button)
addsegment_button.grid(column=1, row=0, padx=5, pady=5, sticky="nsew")

delsegment_button = tk.Button(master=edit_frame, text="Eliminar Segmento", command= del_segment_button)
delsegment_button.grid(column=1, row=1, padx=5, pady=5, sticky="nsew")


#Función mejor camino
delsegment_button = tk.Button(master=edit_frame, text="Mejor Camino", command= plot_shortest_path)
delsegment_button.grid(column=0, row=2, padx=5, pady=5, sticky="nsew")

#Función Grafo En Blanco
delsegment_button = tk.Button(master=edit_frame, text="Grafo en Blanco", command= plot_blank_graph)
delsegment_button.grid(column=1, row=2, padx=5, pady=5, sticky="nsew")


# Botones para operaciones con caminos
add_to_path_button = tk.Button(master=edit_frame, text="Añadir a Camino", command=add_node_to_path)
add_to_path_button.grid(column=0, row=4, padx=5, pady=5, sticky="nsew")

contains_node_button = tk.Button(master=edit_frame, text="Contiene Nodo", command=check_contains_node)
contains_node_button.grid(column=1, row=4, padx=5, pady=5, sticky="nsew")

cost_to_node_button = tk.Button(master=edit_frame, text="Coste a Nodo", command=show_cost_to_node)
cost_to_node_button.grid(column=0, row=5, padx=5, pady=5, sticky="nsew", columnspan=1)

#Función Grafo Random
delsegment_button = tk.Button(master=edit_frame, text="Grafo Aleatorio", command= plot_random_graph)
delsegment_button.grid(column=1, row=5, padx=5, pady=5, sticky="nsew")

#Entrada

entry = tk.Entry(master=edit_frame, font=("Arial", 25))
entry.grid(column=0, row=3, padx=5, pady=5, sticky="nsew", columnspan=2)


#Frame KML
kml_frame = tk.LabelFrame(master = right_frame, bg = "#e6add8", relief = "groove" , bd = 10 , text = "KML" , font=("Arial", 12))
kml_frame.grid(column = 0, row = 3, padx= 5, pady=5,
                sticky = "nsew")

kml_frame.columnconfigure(0, weight = 1)
kml_frame.columnconfigure(1, weight = 1)
kml_frame.rowconfigure(0, weight =  1)    

# Botones que llenan completamente el frame
save_kml = tk.Button(master=kml_frame, text="Guardar KML", command= create_kml)
save_kml.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

execute_kml_button = tk.Button(master=kml_frame, text="Ejecutar KML", command= execute_kml)
execute_kml_button.grid(column=1, row=0, padx=5, pady=5, sticky="nsew")



ventana.mainloop()


