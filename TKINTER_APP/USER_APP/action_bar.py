import tkinter as tk
from PIL import Image, ImageTk
from USER_APP import user_show_frames as shf

all_frames = []

"""Frame de la Barra de Accion"""
def make_action_bar(window):
    # Creación del frame de la barra de acción
    action_bar = tk.Frame(window, bg="#F1F2F6", width=380, height=40)
    action_bar.name = "action_bar"
    action_bar.pack(side="top", fill="x")
    # Agregar logo al centro
    try:
        pasa_logo = "../ASSETS/logo.png"
        logo_image = Image.open(pasa_logo).resize((56, 20), Image.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_image)
        logo_label = tk.Label(action_bar, image=logo_photo, bg="#F1F2F6")
        logo_label.image = logo_photo
        logo_label.place(relx=0.5, rely=0.5, anchor="center")
    except Exception as e:
        print(f"Error al cargar el Logo: {e}")
    # Crear Boton para Regresar pero inicialmente ocultarlo
    try:
        back_image_path = "../ASSETS/back_button.png"
        back_image = Image.open(back_image_path).resize((12, 15), Image.LANCZOS)
        back_photo = ImageTk.PhotoImage(back_image)
        global back_button
        def on_back_button():
            global current_frame, results_frame, login_frame, register_frame, content_frame, start_frame, terms_frame
            # Verificar desde qué frame se está presionando el Boton de Regreso
            if current_frame == results_frame:
                results_frame.pack_forget()
                hide_back_button()
                show_frame(content_frame, all_frames)
            elif current_frame == login_frame:
                login_frame.pack_forget()
                hide_back_button()
                show_frame(start_frame, all_frames)
            elif current_frame == register_frame:
                register_frame.pack_forget()
                hide_back_button()
                show_frame(start_frame, all_frames)
            elif current_frame == terms_frame:
                terms_frame.pack_forget()
                hide_back_button()
                show_frame(start_frame, all_frames)
        back_button = tk.Button(
            action_bar,
            image=back_photo,
            bg="#F1F2F6",
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
        log_out_image_path = "../ASSETS/log_out_button.png"
        log_out_image = Image.open(log_out_image_path).resize((18, 18), Image.LANCZOS)
        log_out_photo = ImageTk.PhotoImage(log_out_image)
        global log_out_button
        def log_out_button():
            global current_frame, results_frame, content_frame
            # Verificar desde qué frame se está presionando el Boton de Cerrar Sesion
            if current_frame == results_frame:
                results_frame.pack_forget()
                hide_log_out_button()
                show_frame(start_frame, all_frames)
            elif current_frame == content_frame:
                content_frame.pack_forget()
                hide_log_out_button()
                show_frame(start_frame, all_frames)
        log_out_button = tk.Button(
            action_bar,
            image=log_out_photo,
            bg="#F1F2F6",
            borderwidth=0,
            command=on_log_out_button
        )
        log_out_button.image = log_out_photo
        log_out_button.place(x=340, y=12)  
        log_out_button.place_forget()  
    except Exception as e:
        print(f"Error al cargar el Boton de Cerrar Sesion: {e}")
    return action_bar

"""Funcion para Mostrar el Boton para Regresar"""
def show_back_button(target_frame=None, back_button=None):
    if back_button:
        back_button.place(x=25, y=12)  

"""Funcion para ocultar el Boton para Regresar"""
def hide_back_button(back_button=None):
    if back_button:
        on_back_button()
        back_button.place_forget()

"""Funcion para limpiar datos al  presionar el Boton de Regresar"""
def on_back_button():
    # Borrar datos al presionar el boton de regreso
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
def show_log_out_button(target_frame=None, log_out_button=None):
    if log_out_button:
        log_out_button.place(x=340, y=12)

"""Funcion para ocultar el Boton para Cerrar Sesion"""
def hide_log_out_button(log_out_button=None):
    if log_out_button:
        log_out_button.place_forget()

"""Funcion para limpiar datos al presionar el Boton Cerrar Sesion"""
def on_log_out_button():
    # Borrar datos al cerrar sesión
    if current_frame == content_frame or current_frame == results_frame:
        point_origin_input.set("Seleccionar")  
        point_destination_input.set("Seleccionar")
        departure_date_button.configure(text="Seleccionar") 
        return_date_button.configure(text="Seleccionar")
        passengers_entry.delete(0, tk.END) 
        passenger_class_input.set("Seleccionar")  
    # Ocultar frame actual
    if current_frame == results_frame:
        results_frame.pack_forget()
    elif current_frame == content_frame:
        content_frame.pack_forget()
    hide_log_out_button()
    show_frame(start_frame, all_frames)