import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tkinter as tk 
from tkinter import messagebox, font
from tkcalendar import Calendar
from datetime import date
from PIL import Image, ImageTk
from customtkinter import CTkComboBox, CTkButton, CTkEntry, set_appearance_mode, set_default_color_theme

"""Frame de la Barra de Accion"""
def make_action_bar():
    # Creación del frame de la barra de acción
    action_bar = tk.Frame(window, bg="#09090A", width=380, height=40)
    action_bar.name = "action_bar"
    action_bar.pack(side="top", fill="x")
    # Agregar logo al centro
    try:
        pasa_logo = "../../ASSETS/logo_admin.png"
        logo_image = Image.open(pasa_logo).resize((56, 20), Image.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_image)
        logo_label = tk.Label(action_bar, image=logo_photo, bg="#09090A")
        logo_label.image = logo_photo
        logo_label.place(relx=0.5, rely=0.5, anchor="center")
    except Exception as e:
        print(f"Error al cargar el Logo: {e}")
    # Crear Boton para Regresar pero inicialmente ocultarlo
    try:
        back_image_path = "../../ASSETS/back_button_admin.png"
        back_image = Image.open(back_image_path).resize((12, 15), Image.LANCZOS)
        back_photo = ImageTk.PhotoImage(back_image)
        global back_button
        def on_back_button():
            global current_frame, login_frame, register_frame, start_frame, terms_frame
            # Verificar desde qué frame se está presionando el Boton de Regreso
            if current_frame == login_frame:
                login_frame.pack_forget()
                hide_back_button()
                show_frame(start_frame)
            elif current_frame == register_frame:
                register_frame.pack_forget()
                hide_back_button()
                show_frame(start_frame)
            elif current_frame == terms_frame:
                terms_frame.pack_forget()
                hide_back_button()
                show_frame(start_frame)
        back_button = tk.Button(
            action_bar,
            image=back_photo,
            bg="#09090A",
            borderwidth=0,
            command=on_back_button
        )
        back_button.image = back_photo
        back_button.place(x=25, y=12) 
        back_button.place_forget()
    except Exception as e:
        print(f"Error al cargar el Boton Regresar: {e}")
    # Boton para Cerrar Sesion
    try:
        log_out_image_path = "../../ASSETS/log_out_button_admin.png"
        log_out_image = Image.open(log_out_image_path).resize((18, 18), Image.LANCZOS)
        log_out_photo = ImageTk.PhotoImage(log_out_image)
        global log_out_button
        def log_out_button():
            global current_frame, add_frame, fetch_frame, update_frame, delete_frame
            # Verificar desde qué frame se está presionando el Boton de Cerrar Sesion
            if current_frame == add_frame:
                add_frame.pack_forget()
                hide_log_out_button()
                show_frame(start_frame)
                hide_option()
            elif current_frame == fetch_frame:
                fetch_frame.pack_forget()
                hide_log_out_button()
                show_frame(start_frame)
                hide_option()
            elif current_frame == update_frame:
                update_frame.pack_forget()
                hide_log_out_button()
                hide_option()
                show_frame(start_frame)
                hide_option()
            elif current_frame == delete_frame:
                delete_frame.pack_forget()
                hide_log_out_button()
                hide_option()
                show_frame(start_frame)
        log_out_button = tk.Button(
            action_bar,
            image=log_out_photo,
            bg="#09090A",
            borderwidth=0,
            command=on_log_out_button
        )
        log_out_button.image = log_out_photo
        log_out_button.place(x=340, y=12)  
        log_out_button.place_forget()  
    except Exception as e:
        print(f"Error al cargar el Boton de Cerrar Sesion: {e}")
    return action_bar

"""Frame de la Barra de Navegacion"""
def make_navigation_bar(window, add_frame, delete_frame, fetch_frame, update_frame):
    # Crear Frame
    navigation_bar = tk.Frame(window, bg="#09090A", height=60, width=380)
    navigation_bar.pack(side="bottom", fill="x")
    navigation_bar.pack_propagate(False)
    # Cargar Icono
    def load_icon(path, size=(24, 24)):
        try:
            image = Image.open(path)
            image = image.resize(size, Image.LANCZOS)
            return ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Error al cargar el Icono {path}: {e}")
            return None
    # Iconos de Botones de Navegacion
    try:
        search_icon = load_icon("../../ASSETS/search_icon.png")
        add_icon = load_icon("../../ASSETS/add_icon.png")
        delete_icon = load_icon("../../ASSETS/delete_icon.png")
        update_icon = load_icon("../../ASSETS/update_icon.png")
    except Exception as e:
        print(f"Error al cargar los Iconos de la Barra de Navegacion {e}")
        add_icon = delete_icon = search_icon = update_icon = None
    # Estilo de Botones de Navegacion
    button_style = {
        'width': 80, 
        'height': 60, 
        'fg_color': "#09090A", 
        'hover_color': "#F0F0F0", 
        'text_color': "#7732FF"
    }
    # Botones de Navegacion
    fetch_button = ctk.CTkButton(
        navigation_bar, 
        text="Buscar", 
        image=search_icon, 
        command=lambda: show_frame(make_fetch_frame()),
        **button_style
    )
    fetch_button.pack(side="left", expand=True)
    add_button = ctk.CTkButton(
        navigation_bar, 
        text="Agregar", 
        image=add_icon, 
        command=lambda: show_frame(make_add_frame()),
        **button_style
    )
    add_button.pack(side="left", expand=True)
    delete_button = ctk.CTkButton(
        navigation_bar, 
        text="Eliminar", 
        image=delete_icon, 
        command=lambda: show_frame(make_delete_frame()),
        **button_style
    )
    delete_button.pack(side="left", expand=True)
    update_button = ctk.CTkButton(
        navigation_bar, 
        text="Modificar", 
        image=update_icon, 
        command=lambda: show_frame(make_update_frame()),
        **button_style
    )
    update_button.pack(side="left", expand=True)
    return navigation_bar

"""Funcion para Mostrar el Boton para Regresar"""
def show_back_button(target_frame=None):
    if back_button:
        back_button.place(x=25, y=12)  

"""Funcion para ocultar el Boton para Regresar"""
def hide_back_button():
    if back_button:
        on_back_button()
        back_button.place_forget()

"""Funcion para limpiar datos al  presionar el Boton de Regresar"""
def on_back_button():
    global current_frame, login_frame, register_frame, start_frame
    # Borar datos al presionar el boton de regreso
    if current_frame == login_frame:
        login_id_card_entry.delete(0, tk.END)
        login_password_entry.delete(0, tk.END)
    elif current_frame == register_frame:
        name_entry.delete(0, tk.END)
        last_name_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)
        id_card_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)

"""Funcion para mostrar el Boton para Cerrar Sesion"""
def show_log_out_button(target_frame=None):
    if log_out_button:
        log_out_button.place(x=340, y=12)

"""Funcion para ocultar el Boton para Cerrar Sesion"""
def hide_log_out_button():
    if log_out_button:
        log_out_button.place_forget()

"""Funcion para limpiar datos al presionar el Boton Cerrar Sesion"""
def on_log_out_button():
    global current_frame, start_frame
    hide_log_out_button()
    show_frame(start_frame)

"""Función para Mostrar Option"""
def show_option(target_frame=None):
    global option
    if option and target_frame:
        option.place(relx=0.5, rely=0.5, anchor='center')

"""Función para Ocultar Option"""
def hide_option():
    if option:
        option.place_forget()