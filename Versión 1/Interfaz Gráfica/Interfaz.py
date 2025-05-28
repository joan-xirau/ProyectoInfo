import tkinter as tk


from graph import *
from test_graph import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import simpledialog, messagebox




#Grafos Ejemplos



def show_example_1():
    global canvas_widget
    global currrent_graph

    currrent_graph = CreateGraph_1 ()


    if canvas_widget:
            canvas_widget.destroy()
    canvas = FigureCanvasTkAgg(Plot(currrent_graph), master = left_frame)
    canvas.draw()
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)



    return None


def show_example_2():
    global canvas_widget
    global currrent_graph

    currrent_graph = CreateGraph_2 ()

    if canvas_widget:
            canvas_widget.destroy()
    canvas = FigureCanvasTkAgg(Plot(currrent_graph), master = left_frame)
    canvas.draw()
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)

    return None

def load_file():
    global currrent_graph
    global canvas_widget

    file_name = simpledialog.askstring("Cargar Archivo", "Nombre del Archivo")
    currrent_graph = ReadFile(file_name)
    if graph:
        if canvas_widget:
                canvas_widget.destroy()
        canvas = FigureCanvasTkAgg(Plot(currrent_graph), master = left_frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
    else:
        messagebox.showwarning("ERROR", "Archivo no encontrado")

    return None



def save_file():
    global currrent_graph
    
    file_name = simpledialog.askstring("Cargar Archivo", "Nombre del Archivo")
    archivo = open(file_name, "w", encoding="utf-8")
    archivo.write(f"NODES \n\n")
    for node_in_graph in currrent_graph.nodes:
        archivo.write(f"{node_in_graph.name} {node_in_graph.x} {node_in_graph.y} \n")
    archivo.write(f"SEGMENTS \n\n")
    for segment_in_graph in currrent_graph.segments:
        archivo.write(f"{segment_in_graph.name} {segment_in_graph.origin.name} {segment_in_graph.destination.name} \n")    

    archivo.close() 


def add_node_button():
    global currrent_graph
    global canvas_widget
    global entry

    if currrent_graph:
        repeated = False
        information = list(entry.get().split(" "))
        for node_in_graph in currrent_graph.nodes:
            if node_in_graph.name == information[0]:
                    repeated = True
                    break
        if repeated:
            messagebox.showwarning("ERROR", "Ya existe un nodo con ese nombre")
        else:
                info_node = node(information[0], information[1], information[2])           
                AddNode(currrent_graph, info_node)
                if canvas_widget:
                    canvas_widget.destroy()
                canvas = FigureCanvasTkAgg(Plot(currrent_graph), master = left_frame)
                canvas.draw()
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.pack(fill=tk.BOTH, expand=True)
    else:
        currrent_graph = graph()
        repeated = False
        information = list(entry.get().split(" "))
        for node_in_graph in currrent_graph.nodes:
            if node_in_graph.name == information[0]:
                    repeated = True
                    break
        if repeated:
            messagebox.showwarning("ERROR", "Ya existe un nodo con ese nombre")
        else:
                info_node = node(information[0], information[1], information[2])           
                AddNode(currrent_graph, info_node)
                if canvas_widget:
                    canvas_widget.destroy()
                canvas = FigureCanvasTkAgg(Plot(currrent_graph), master = left_frame)
                canvas.draw()
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.pack(fill=tk.BOTH, expand=True)




def del_node_button():
    global currrent_graph
    global canvas_widget
    global entry


    if currrent_graph:
        
        information = entry.get()
        delete_segments = []
        found = False
        try:
            for node_in_graph in currrent_graph.nodes:
                if node_in_graph.name == information:
                    for segment_in_graph in currrent_graph.segments:
                        if segment_in_graph.destination == node_in_graph or segment_in_graph.origin == node_in_graph:
                             delete_segments.append(segment_in_graph.name)

                    for to_delete in delete_segments:
                        DelSegment(currrent_graph, to_delete)


                    DelNode(currrent_graph, node_in_graph)
                    if canvas_widget:
                        canvas_widget.destroy()
                    canvas = FigureCanvasTkAgg(Plot(currrent_graph), master = left_frame)
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
    global currrent_graph
    global canvas_widget
    global entry

    if currrent_graph:
        repeated = False
        information = list(entry.get().split(" "))
        for segment_in_graph in currrent_graph.segments:
            if segment_in_graph.name == information[0]:
                    repeated = True
                    break
        if repeated:
            messagebox.showwarning("ERROR", "Ya existe un segmento con ese nombre")
        else:
            try:
                founded_node1 = None
                founded_node2 = None
                for node_in_graph in currrent_graph.nodes:
                    if node_in_graph.name == information[1]:
                        founded_node1 = node_in_graph
                    elif node_in_graph.name == information[2]:
                         founded_node2 = node_in_graph
                
                if founded_node1 and founded_node2:
                    info_segment = segment(information[0], founded_node1, founded_node2)           
                    AddSegment(currrent_graph, information[0], founded_node1.name, founded_node2.name)
                    if canvas_widget:
                        canvas_widget.destroy()
                    canvas = FigureCanvasTkAgg(Plot(currrent_graph), master = left_frame)
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
    global currrent_graph
    global canvas_widget
    global entry
    found = False

    if currrent_graph:
        information = entry.get()
        for segment_in_graph in currrent_graph.segments:
            if segment_in_graph.name == information:
                found = True   

        if found:
            DelSegment(currrent_graph, information )
            if canvas_widget:
                canvas_widget.destroy()
            canvas = FigureCanvasTkAgg(Plot(currrent_graph), master = left_frame)
            canvas.draw()
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(fill=tk.BOTH, expand=True)



        else:
            messagebox.showwarning("ERROR", "No existe ningún segmento con ese nombre")
    else:
        messagebox.showwarning("ERROR", "No existe ningún grafo")





#Interfaz Gráfica
ventana = tk.Tk()
ventana.title("Interfaz Gráfica")
ventana.geometry("900x600")

ventana.columnconfigure(0 , weight= 4)
ventana.columnconfigure(1,weight = 1)
ventana.rowconfigure(0, weight = 1)

canvas_widget = None
currrent_graph = None

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
edit_frame.rowconfigure(2, weight=2)

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

#Entrada

entry = tk.Entry(master=edit_frame, font=("Arial", 25))
entry.grid(column=0, row=2, padx=5, pady=5, sticky="nsew", columnspan=2)





ventana.mainloop()


