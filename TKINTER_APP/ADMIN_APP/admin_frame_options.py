import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tkinter as tk 
from tkinter import messagebox, font
from tkcalendar import Calendar
from datetime import date
from PIL import Image, ImageTk
from customtkinter import CTkComboBox, CTkButton, CTkEntry, set_appearance_mode, set_default_color_theme

"""Funcion para Realizar Consultas"""
def queries_option():
    global current_frame, selected_option, entries
    connection = c.make_connection()
    if not connection:
        return
    cursor = connection.cursor()
    try:
        if current_frame == add_frame:
            action = "add"
        elif current_frame == delete_frame:
            action = "delete"
        elif current_frame == update_frame:
            action = "update"
        else:
            messagebox.showerror("Error", "Operación no válida o Frame desconocido.")
            return
        
        if action == "add":
            if "Agregar Bus" in selected_option:
                chofer_id = int(entries[0].get())
                ruta_id = int(entries[1].get())
                fecha_sal=(entries[2].get())
                fecha_ret=(entries[3].get())
                f.add_bus(chofer_id,ruta_id,fecha_sal,fecha_ret)
                messagebox.showinfo("Éxito", "Bus agregado correctamente.")
            elif "Agregar Chofer" in selected_option:
                nombre = entries[4].get()
                edad = int(entries[5].get())
                carnet = int(entries[6].get())
                f.add_driver(nombre, edad, carnet)
                messagebox.showinfo("Éxito", "Chofer agregado correctamente")
            elif "Agregar Ruta" in selected_option:
                dep_inicio = entries[7].get()
                dep_final = entries[8].get()
                costo = float(entries[9].get())
                costo_vip = float(entries[10].get())
                f.add_route(dep_inicio, dep_final, costo, costo_vip)
                messagebox.showinfo("Éxito", "Ruta agregada correctamente")
        
        
        elif action == "delete":
            if "Eliminar Bus" in selected_option:
                bus_id = int(entries[0].get())
                f.del_bus(bus_id)
                messagebox.showinfo("Éxito", "Bus eliminado correctamente")
            elif "Eliminar Chofer" in selected_option:
                chofer_id = int(entries[1].get())
                f.del_driver(chofer_id)
                messagebox.showinfo("Éxito", "Chofer eliminado correctamente")
            elif "Eliminar Ruta" in selected_option:
                ruta_id = int(entries[2].get())
                f.del_route(ruta_id)
                messagebox.showinfo("Éxito", "Ruta eliminada correctamente")
        
        
        elif action == "update":
            if "Actualizar Bus" in selected_option:
                bus_id = int(entries[0].get())
                chofer_id = int(entries[1].get())
                ruta_id = int(entries[2].get())
                fecha_sal=(entries[3].get())
                fecha_ret=(entries[4].get())
                f.update_bus(bus_id,  chofer_id, ruta_id,fecha_sal,fecha_ret)
                messagebox.showinfo("Éxito", "Bus actualizado correctamente")
            elif "Actualizar Chofer" in selected_option:
                nombre = entries[5].get()
                chofer_id = int(entries[6].get())
                edad = int(entries[7].get())
                carnet = int(entries[8].get())
                f.update_driver(chofer_id, nombre, edad, carnet)
                messagebox.showinfo("Éxito", "Chofer actualizado correctamente")
            elif "Actualizar Ruta" in selected_option:
                ruta_id = int(entries[9].get())
                dep_inicio = entries[10].get()
                dep_final = entries[11].get()
                costo = int(entries[12].get())
                costo_vip = int(entries[13].get())
                f.update_route(ruta_id,dep_inicio,dep_final,costo,costo_vip)
                messagebox.showinfo("Éxito", "Chofer actualizado correctamente")
    except Exception as e:
        messagebox.showerror("Error",e)

def create_input_field(parent, label_text, placeholder, identifier_button):
    global entries
    frame = tk.Frame(parent, bg="#09090A")
    frame.pack(side="top", pady=10, fill="x", padx=10)
    if identifier_button == 1:
        label = tk.Label(frame, text=label_text, bg="#09090A", fg="#C8BCF6")
        label.pack(side="left", padx=10)
        entry = CTkEntry(
            frame,
            placeholder_text=placeholder,
            border_color="#C8BCF6",
            corner_radius=32,
        )
        entry.pack(side="left", padx=10, fill="x", expand=True)
        if entry is not None:
            entries.append(entry)  # Agregar la entrada a la lista
    
    
    elif identifier_button == 2:
        frame = tk.Frame(parent, bg="#09090A")
        frame.pack(side="top", pady=20, fill="x", padx=10)
        def on_button_click():
            global selected_option
            selected_option = label_text

            queries_option()  # Llama a la función queries_option cuando se presione el botón
        available = CTkButton(
            frame,
            text=label_text,
            corner_radius=32,
            fg_color="#7732FF",
            hover_color="#5A23CC",
            command=on_button_click,
        )
        available.pack(pady=10, fill="x")

"""Frame para Crear Botones Predeterminados"""
def make_option_frame(parent, title_name):
    option_frame = ttk.Frame(parent)
    global option, entries 
    option = ttk.Entry(option_frame)
    entries = []  # Reiniciar la lista de entradas cada vez que se crea un nuevo conjunto
    option.pack(padx=10, pady=10)

    # Scrollbar
    canvas = tk.Canvas(option_frame, bg="#09090A", highlightthickness=0, width=350, height=1300)
    scrollbar = tk.Scrollbar(option_frame, orient="vertical", command=canvas.yview,width=18)

    # Crear un marco interno dentro del canvas
    scrollable_frame = tk.Frame(canvas, bg="#09090A")
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # Vincular el marco interno con el canvas
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=350, height=1300)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Titulo de Bus
    title_font = font.Font(family="Canva Sans", size=15, weight="bold")
    title_label = tk.Label(
        scrollable_frame,
        text=f"{title_name} un Bus",  
        font=title_font,
        bg="#09090A",
        fg="#7732FF",
        wraplength=350,
        justify="center",
    )
    title_label.pack(pady=20)
    #bus
    if title_name == "Agregar":
        create_input_field(scrollable_frame, "Chofer ID:", "Ingresar", 1)
        create_input_field(scrollable_frame, "Ruta ID:", "Ingresar", 1)
        create_input_field(scrollable_frame, "fecha_salida:", "Ingresar", 1)
        create_input_field(scrollable_frame, "fecha_retorno","Ingresar", 1)
        create_input_field(scrollable_frame, f"{title_name} Bus", "Ingresar", 2)
    elif title_name == "Eliminar":
        create_input_field(scrollable_frame, "Bus ID:", "Ingresar", 1)
        create_input_field(scrollable_frame, f"{title_name} Bus", "Ingresar", 2)
    elif title_name == "Actualizar":
        create_input_field(scrollable_frame, "Bus ID:", "Ingresar", 1)
        create_input_field(scrollable_frame, "Chofer ID:", "Ingresar", 1)
        create_input_field(scrollable_frame, "Ruta ID:", "Ingresar", 1)
        create_input_field(scrollable_frame, "fecha_salida:", "Ingresar", 1)
        create_input_field(scrollable_frame, "fecha_retorno","Ingresar", 1)
        create_input_field(scrollable_frame, f"{title_name} Bus", "Ingresar", 2)
    # Titulo de Chofer
    title_font = font.Font(family="Canva Sans", size=15, weight="bold")
    title_label = tk.Label(
        scrollable_frame,
        text=f"{title_name} un Chofer",  
        font=title_font,
        bg="#09090A",
        fg="#7732FF",
        wraplength=350,
        justify="center",
    )
    title_label.pack(pady=20)
    #chofer
    if title_name == "Agregar":
        create_input_field(scrollable_frame, "Nombre del Chofer:", "Ingresar", 1)
        create_input_field(scrollable_frame, "Edad:", "Ingresar", 1)
        create_input_field(scrollable_frame, "Carnet:", "Ingresar", 1)
        create_input_field(scrollable_frame, f"{title_name} Chofer", "Ingresar", 2)
    elif title_name == "Eliminar":
        create_input_field(scrollable_frame, "Chofer ID:", "Ingresar", 1)
        create_input_field(scrollable_frame, f"{title_name} Chofer", "Ingresar", 2)
    elif title_name == "Actualizar":
        create_input_field(scrollable_frame, "Nombre del Chofer:", "Ingresar", 1)
        create_input_field(scrollable_frame, "Chofer ID:", "Ingresar", 1)
        create_input_field(scrollable_frame, "Edad:", "Ingresar", 1)
        create_input_field(scrollable_frame, "Carnet:", "Ingresar", 1)
        create_input_field(scrollable_frame, f"{title_name} Chofer", "Ingresar", 2)
    # Titulo de RUTA
    title_font = font.Font(family="Canva Sans", size=15, weight="bold")
    title_label = tk.Label(
        scrollable_frame,
        text=f"{title_name} una Ruta",  
        font=title_font,
        bg="#09090A",
        fg="#7732FF",
        wraplength=350,
        justify="center",
    )
    title_label.pack(pady=20)    
    #ruta
    if title_name == "Agregar":
        create_input_field(scrollable_frame, "Dep_inicio:", "Ingresar", 1)
        create_input_field(scrollable_frame, "Dep_final:", "Ingresar", 1)        
        create_input_field(scrollable_frame, "Costo:", "Ingresar", 1)
        create_input_field(scrollable_frame, "Costo VIP:", "Ingresar", 1)
        create_input_field(scrollable_frame, f"{title_name} Ruta", "Ingresar", 2)
    elif title_name == "Eliminar":
        create_input_field(scrollable_frame, "Ruta ID", "Ingresar", 1)
        create_input_field(scrollable_frame, f"{title_name} Ruta", "Ingresar", 2)  
    elif title_name == "Actualizar":
        create_input_field(scrollable_frame, "Ruta ID", "Ingresar", 1)
        create_input_field(scrollable_frame, "Dep_inicio", "Ingresar", 1)
        create_input_field(scrollable_frame, "Dep_final", "Ingresar", 1)        
        create_input_field(scrollable_frame, "Costo:", "Ingresar", 1)
        create_input_field(scrollable_frame, "Costo VIP:", "Ingresar", 1)
        create_input_field(scrollable_frame, f"{title_name} Ruta", "Ingresar", 2)
    return option_frame

"""Frame para Agregar Datos"""
def make_add_frame():
    global current_frame, add_frame, option_frame
    if add_frame is None:
        add_frame = tk.Frame(window, bg="#09090A")
        add_frame.name = "add"
    if option_frame is None or option_frame.master != add_frame:
        if option_frame:
            option_frame.pack_forget() 
        option_frame = make_option_frame(add_frame, "Agregar")
        option_frame.pack(fill="both", expand=True)
    if current_frame:
        current_frame.pack_forget()
    current_frame = add_frame
    current_frame.pack(fill="both", expand=True)
    show_option(target_frame=add_frame)
    return add_frame

"""Frame para Modificar Datos"""
def make_update_frame():
    global current_frame, update_frame, option_frame
    if update_frame is None:
        update_frame = tk.Frame(window, bg="#09090A")
        update_frame.name = "update"
    if option_frame is None or option_frame.master != update_frame:
        if option_frame:
            option_frame.pack_forget()  
        option_frame = make_option_frame(update_frame, "Actualizar")
        option_frame.pack(fill="both", expand=True)
    if current_frame:
        current_frame.pack_forget()
    current_frame = update_frame
    current_frame.pack(fill="both", expand=True)
    show_option(target_frame=update_frame)
    return update_frame

"""Frame para Eliminar Datos"""
def make_delete_frame():
    global current_frame, delete_frame, option_frame
    if delete_frame is None:
        delete_frame = tk.Frame(window, bg="#09090A")
        delete_frame.name = "delete"
    if option_frame is None or option_frame.master != delete_frame:
        if option_frame:
            option_frame.pack_forget()  
        option_frame = make_option_frame(delete_frame, "Eliminar")
        option_frame.pack(fill="both", expand=True)
    if current_frame:
        current_frame.pack_forget()
    current_frame = delete_frame
    current_frame.pack(fill="both", expand=True)
    show_option(target_frame=delete_frame)
    return delete_frame