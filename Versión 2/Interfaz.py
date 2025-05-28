import tkinter as tk


from graph import *
from path import *
from test_graph import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import simpledialog, messagebox




def show_example_1():
    global canvas_widget
    global current_graph

    current_graph = CreateGraph_1 ()


    if canvas_widget:
            canvas_widget.destroy()
    canvas = FigureCanvasTkAgg(Plot(current_graph), master = left_frame)
    canvas.draw()
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)



    return None


def show_example_2():
    global canvas_widget
    global current_graph

    current_graph = CreateGraph_2 ()

    if canvas_widget:
            canvas_widget.destroy()
    canvas = FigureCanvasTkAgg(Plot(current_graph), master = left_frame)
    canvas.draw()
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)

    return None

def load_file():
    global current_graph
    global canvas_widget

    file_name = simpledialog.askstring("Cargar Archivo", "Nombre del Archivo")
    current_graph = ReadFile(file_name)
    if graph:
        if canvas_widget:
                canvas_widget.destroy()
        canvas = FigureCanvasTkAgg(Plot(current_graph), master = left_frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
    else:
        messagebox.showwarning("ERROR", "Archivo no encontrado")

    return None



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
        camino = shortest_path(current_graph, start_node, end_node)
        
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
        
        canvas = FigureCanvasTkAgg(path_obj.plot(current_graph), master=left_frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        
        # Mostrar información del camino
        messagebox.showinfo("Camino encontrado", f"Camino más corto: {' -> '.join(camino)}\nCoste total: {path_obj.cost_to_node(next(n for n in current_graph.nodes if n.name == end_node), current_graph):.2f}")
        
    except Exception as e:
        messagebox.showerror("ERROR", f"Error al calcular el camino: {str(e)}")


         
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
right_frame.rowconfigure(0, weight =  1)
right_frame.rowconfigure(1, weight = 1)
right_frame.rowconfigure(2, weight = 2)

#Frame Ejemplos
examples_frame = tk.LabelFrame(master = right_frame, bg = "#e6b98f", relief = "groove" , bd = 10 , text = "Ejemplos" , font=("Arial", 12))
examples_frame.grid(column = 0, row = 0, padx= 5, pady=5,
                sticky = "nsew")

examples_frame.columnconfigure(0, weight = 1)
examples_frame.rowconfigure(0, weight =  1)    
examples_frame.rowconfigure(1, weight = 1)

# Botones que llenan completamente el frame
example1_button = tk.Button(master=examples_frame, text="Ejemplo 1", command=lambda:show_example_1())
example1_button.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

example2_button = tk.Button(master=examples_frame, text="Ejemplo 2", command=lambda: show_example_2())
example2_button.grid(column=0, row=1, padx=5, pady=5, sticky="nsew")

#Frame Archivos
files_frame = tk.LabelFrame(master = right_frame, bg = "#e6add8", relief = "groove" , bd = 10 , text = "Archivo" , font=("Arial", 12))
files_frame.grid(column = 0, row = 1, padx= 5, pady=5,
                sticky = "nsew")

files_frame.columnconfigure(0, weight = 1)
files_frame.rowconfigure(0, weight =  1)    
files_frame.rowconfigure(1, weight = 1)

# Botones que llenan completamente el frame
upload_button = tk.Button(master=files_frame, text="Subir Archivo", command= load_file)
upload_button.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

save_button = tk.Button(master=files_frame, text="Guardar Archivo", command= save_file)
save_button.grid(column=0, row=1, padx=5, pady=5, sticky="nsew")
    

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
delsegment_button.grid(column=0, row=2, padx=5, pady=5, sticky="nsew", columnspan=2)

# Botones para operaciones con caminos
add_to_path_button = tk.Button(master=edit_frame, text="Añadir a Camino", command=add_node_to_path)
add_to_path_button.grid(column=0, row=4, padx=5, pady=5, sticky="nsew")

contains_node_button = tk.Button(master=edit_frame, text="Contiene Nodo", command=check_contains_node)
contains_node_button.grid(column=1, row=4, padx=5, pady=5, sticky="nsew")

cost_to_node_button = tk.Button(master=edit_frame, text="Coste a Nodo", command=show_cost_to_node)
cost_to_node_button.grid(column=0, row=5, padx=5, pady=5, sticky="nsew", columnspan=2)

#Entrada

entry = tk.Entry(master=edit_frame, font=("Arial", 25))
entry.grid(column=0, row=3, padx=5, pady=5, sticky="nsew", columnspan=2)





ventana.mainloop()


