import tkinter as tk
import os
from tkinter import messagebox, font
from tkcalendar import Calendar
from datetime import date
from PIL import Image, ImageTk
from customtkinter import CTkComboBox, CTkButton, CTkEntry, set_appearance_mode, set_default_color_theme

# ------------------------------------------------------------------------------------------------------------------------------------------------------------

"""Configuración de la Ventana"""
set_appearance_mode("light")
set_default_color_theme("blue")

window = tk.Tk()
window.title("Pasa")
window.geometry("380x750+120+10")
window.resizable(False, False)
window.configure(bg="#F1F2F6")
try:
    window.iconbitmap("../IMAGES/icon.ico")
except Exception:
    print(f"Error al cargar el icono: {Exception}")

# -------------------------------------------------------------------------------------------------------------------------------------------------------------

"""Pantalla de Carga"""
def loading_screen():
    try:
        pasa_iso = os.path.join(os.path.dirname(__file__), "../IMAGES/iso.png")
        image = Image.open(pasa_iso)
        image = image.resize((200, 200), Image.Resampling.LANCZOS) 
        photo = ImageTk.PhotoImage(image)
        iso_label = tk.Label(loading_frame, image=photo, bg="#7732FF")
        iso_label.image = photo  
        iso_label.pack(expand=True)
    except FileNotFoundError:
        print(f"Archivo no encontrado: {pasa_iso}")
    except Exception:
        print(f"Error al cargar el isotipo: {Exception}")

    window.after(1500, lambda: show_frame(start_frame))

loading_frame = tk.Frame(window, bg="#7732FF")
loading_frame.pack(fill="both", expand=True)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------

"""Barra de Acción"""
action_bar = tk.Frame(window, bg="#F1F2F6", width=380, height=40)
action_bar.pack(side="top", fill="x")

# Logo
try:
    pasa_logo = "../IMAGES/logo.png"
    image = Image.open(pasa_logo)
    image_resized = image.resize((56, 20), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image_resized)
    logo_label = tk.Label(action_bar, image=photo, bg="#F1F2F6")
    logo_label.image = photo
    logo_label.place(relx=0.5, rely=0.5, anchor="center")
except Exception:
    print(f"Error al cargar el logo: {Exception}")

# ------------------------------------------------------------------------------------------------------------------------------------------------------------

"""Funcion para Mostrar un Frame"""
def show_frame(frame_to_show):
    for frame in all_frames:
        frame.pack_forget()
    frame_to_show.pack(pady=20, padx=20, expand=True)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------

"""Crear una Cuenta"""
def create_account():
    name = name_entry.get().strip()
    last_name = last_name_entry.get().strip()
    age = age_entry.get().strip()
    id_card = id_card_entry.get().strip()
    password = password_entry.get().strip()

    if not all([name, last_name, age, id_card, password]):
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return
    try:
        age = int(age)
        if age < 18:
            messagebox.showerror("Error", "No puedes crear una cuenta si eres menor de edad")
            return
    except ValueError:
        messagebox.showerror("Error", "La edad debe ser un numero")
        return
    
    name_entry.delete(0, tk.END)
    last_name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    id_card_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    show_frame(content_frame)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------

"""Inicio de Sesion"""
def login():
    id_card = login_id_card_entry.get().strip()
    password = login_password_entry.get().strip()
    
    if not all([id_card, password]):
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return
    
    login_id_card_entry.delete(0, tk.END)
    login_password_entry.delete(0, tk.END)
    show_frame(content_frame)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------

"""Primer Frame"""
start_frame = tk.Frame(window, bg="#F1F2F6")
title_font = font.Font(family="Canva Sans", size=15, weight="bold")
title_label = tk.Label(
    start_frame,
    text="¡Viajar nunca fue mas sencillo!",
    font=title_font,
    bg="#F1F2F6",
    fg="black",
    wraplength=350,
    justify="center",
)
title_label.pack(pady=50)

login_button = CTkButton(
    start_frame,
    text="Iniciar Sesion",
    corner_radius=32,
    fg_color="#7732FF",
    text_color="white",
    hover_color="#5A23CC",
    command=lambda: show_frame(login_frame),
)
login_button.pack(pady=10)

signup_button = CTkButton(
    start_frame,
    text="Crear cuenta",
    corner_radius=32,
    fg_color="#7732FF",
    text_color="white",
    hover_color="#5A23CC",
    command=lambda: show_frame(register_frame),
)
signup_button.pack(pady=10)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------

"""Frame para Crear una Cuenta"""
register_frame = tk.Frame(window, bg="#F1F2F6")

# Nombre
name_frame = tk.Frame(register_frame, bg="#F1F2F6")
name_frame.pack(side="top", pady=10, fill="x", padx=10)
name_label = tk.Label(name_frame, text="Nombre:", bg="#F1F2F6")
name_label.pack(side="left", padx=10)
name_entry = CTkEntry(
    name_frame,
    placeholder_text="Ingresa",
    border_color="#7732FF",
    corner_radius=32
)
name_entry.pack(side="left", padx=10, fill="x", expand=True)

# Apellidos
last_name_frame = tk.Frame(register_frame, bg="#F1F2F6")
last_name_frame.pack(side="top", pady=10, fill="x", padx=10)
last_name_label = tk.Label(last_name_frame, text="Apellidos:", bg="#F1F2F6")
last_name_label.pack(side="left", padx=10)
last_name_entry = CTkEntry(
    last_name_frame,
    placeholder_text="Ingresa",
    border_color="#7732FF",
    corner_radius=32
)
last_name_entry.pack(side="left", padx=10, fill="x", expand=True)

# Edad
age_frame = tk.Frame(register_frame, bg="#F1F2F6")
age_frame.pack(side="top", pady=10, fill="x", padx=10)
age_label = tk.Label(age_frame, text="Edad:", bg="#F1F2F6")
age_label.pack(side="left", padx=10)
age_entry = CTkEntry(
    age_frame,
    placeholder_text="Ingresa",
    border_color="#7732FF",
    corner_radius=32
)
age_entry.pack(side="left", padx=10, fill="x", expand=True)

# Carnet
id_card_frame = tk.Frame(register_frame, bg="#F1F2F6")
id_card_frame.pack(side="top", pady=10, fill="x", padx=10)
id_card_label = tk.Label(id_card_frame, text="Carnet:", bg="#F1F2F6")
id_card_label.pack(side="left", padx=10)
id_card_entry = CTkEntry(
    id_card_frame,
    placeholder_text="Ingresa",
    border_color="#7732FF",
    corner_radius=32
)
id_card_entry.pack(side="left", padx=10, fill="x", expand=True)

# Contraseña
password_frame = tk.Frame(register_frame, bg="#F1F2F6")
password_frame.pack(side="top", pady=10, fill="x", padx=10)
password_label = tk.Label(password_frame, text="Contraseña:", bg="#F1F2F6")
password_label.pack(side="left", padx=10)
password_entry = CTkEntry(
    password_frame,
    placeholder_text="Ingresa",
    show="*",
    border_color="#7732FF",
    corner_radius=32
)
password_entry.pack(side="left", padx=10, fill="x", expand=True)

# Crear cuenta
create_account_button = CTkButton(
    register_frame,
    text="Crear cuenta",
    corner_radius=32,
    fg_color="#7732FF",
    text_color="white",
    hover_color="#5A23CC",
    command=create_account
)
create_account_button.pack(pady=10) 

# ------------------------------------------------------------------------------------------------------------------------------------------------------------

"""Frame para Iniciar Sesion"""
login_frame = tk.Frame(window, bg="#F1F2F6")

# Carnet
login_id_card_frame = tk.Frame(login_frame, bg="#F1F2F6")
login_id_card_frame.pack(side="top", pady=10, fill="x", padx=10)
login_id_card_label = tk.Label(login_id_card_frame, text="Carnet:", bg="#F1F2F6")
login_id_card_label.pack(side="left", padx=10)
login_id_card_entry = CTkEntry(
    login_id_card_frame,
    placeholder_text="Ingresa",
    border_color="#7732FF",
    corner_radius=32
)
login_id_card_entry.pack(side="left", padx=10, fill="x", expand=True)

# Contraseña
login_password_frame = tk.Frame(login_frame, bg="#F1F2F6")
login_password_frame.pack(side="top", pady=10, fill="x", padx=10)
login_password_label = tk.Label(login_password_frame, text="Contraseña:", bg="#F1F2F6")
login_password_label.pack(side="left", padx=10)
login_password_entry = CTkEntry(
    login_password_frame,
    placeholder_text="Ingresa",
    show="*",
    border_color="#7732FF",
    corner_radius=32
)
login_password_entry.pack(side="left", padx=10, fill="x", expand=True)

# Iniciar Sesion
login_button_submit = CTkButton(
    login_frame,
    text="Iniciar Sesion",
    corner_radius=32,
    fg_color="#7732FF",
    text_color="white",
    hover_color="#5A23CC",
    command=login
)
login_button_submit.pack(pady=10)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------

"""Area de contenido"""
content_frame = tk.Frame(window, bg="#F1F2F6")
combo_fg_color = "#F1F2F6"
combo_button_color = "#7732FF"
combo_border_color = "#7732FF"

# Punto de Origen
origin_frame = tk.Frame(content_frame, bg="#F1F2F6")
origin_frame.pack(side="top", pady=10, fill="x", padx=10)
point_origin_txt = tk.Label(origin_frame, text="Punto de Partida:", bg="#F1F2F6")
point_origin_input = CTkComboBox(
    origin_frame,
    values=["Santa Cruz", "La Paz", "Cochabamba", "Potosí", "Chuquisaca", "Oruro", "Tarija", "Beni", "Pando"],
    fg_color=combo_fg_color,
    button_color=combo_button_color,
    border_color=combo_border_color,
    corner_radius=32,
    state="readonly" 
)
point_origin_input.set("Selecciona")
point_origin_txt.pack(side="left", padx=10)
point_origin_input.pack(side="left", padx=10)

# Punto de Destino
destination_frame = tk.Frame(content_frame, bg="#F1F2F6")
destination_frame.pack(side="top", pady=10, fill="x", padx=10)
point_destination_txt = tk.Label(destination_frame, text="Punto de Destino:", bg="#F1F2F6")
point_destination_input = CTkComboBox(
    destination_frame,
    values=["Santa Cruz", "La Paz", "Cochabamba", "Potosí", "Chuquisaca", "Oruro", "Tarija", "Beni", "Pando"],
    fg_color=combo_fg_color,
    button_color=combo_button_color,
    border_color=combo_border_color,
    corner_radius=32,
    state="readonly" 
)
point_destination_input.set("Selecciona")
point_destination_txt.pack(side="left", padx=10)
point_destination_input.pack(side="left", padx=10)

# Calendario
def open_calendar(min_date, max_date, callback):
    calendar_window = tk.Toplevel(window)
    calendar_window.title("Selecciona la Fecha")
    calendar_window.configure(bg="#F1F2F6")
    calendar_window.geometry("320x250+150+85")
    try:
        calendar_window.iconbitmap("../IMAGES/icon.ico")
    except Exception:
        print(f"Error al cargar el icono: {Exception}")
    calendar_frame = tk.Frame(calendar_window, bg="#F1F2F6", relief="flat", bd=1)
    calendar_frame.pack(padx=10, pady=10, fill="both", expand=True)
    calendar = Calendar(
        calendar_frame,
        mindate=min_date,
        maxdate=max_date,
        date_pattern="yyyy-mm-dd",
        selectmode="day",
        background="#FFFFFF",
        foreground="#7732FF",
        headersbackground="#F1F2F6",
        headersforeground="#7732FF",
        selectbackground="#7732FF",
        selectforeground="#FFFFFF",
        weekendforeground="#A9A9A9",
        bordercolor="#F1F2F6"
    )
    calendar.pack(padx=10, pady=10)
    calendar.bind("<<CalendarSelected>>", lambda _: [callback(calendar.get_date()), calendar_window.destroy()])

# Fecha de Partida
departure_date_frame = tk.Frame(content_frame, bg="#F1F2F6")
departure_date_frame.pack(side="top", pady=10, fill="x", padx=10)
departure_date_label = tk.Label(departure_date_frame, text="Fecha de Partida:", bg="#F1F2F6")
departure_date_label.pack(side="left", padx=10)
departure_date_button = CTkButton(
    departure_date_frame,
    text="Selecciona",
    corner_radius=32,
    fg_color="#F1F2F6",
    text_color="#000000",
    hover_color="#E1E1E1",
    border_color="#7732FF",
    border_width=2,
    command=lambda: open_calendar(
        date.today(),
        date(2025, 12, 31),
        lambda d: departure_date_button.configure(text=d)
    )
)
departure_date_button.pack(side="left", padx=10, fill="x", expand=True)

# Fecha de Regreso
return_date_frame = tk.Frame(content_frame, bg="#F1F2F6")
return_date_frame.pack(side="top", pady=10, fill="x", padx=10)
return_date_label = tk.Label(return_date_frame, text="Fecha de Regreso:", bg="#F1F2F6")
return_date_label.pack(side="left", padx=10)

def enable_return_date_selection():
    if departure_date_button.cget("text") == "Selecciona":
        messagebox.showerror("Error", "Primero selecciona la Fecha de Partida")
    else:
        open_calendar(
            date.today(),
            date(2025, 12, 31),
            lambda d: return_date_button.configure(text=d)
        )

return_date_button = CTkButton(
    return_date_frame,
    text="Selecciona",
    corner_radius=32,
    fg_color="#F1F2F6",
    text_color="#000000",
    hover_color="#E1E1E1",
    border_color="#7732FF",
    border_width=2,
    command=enable_return_date_selection
)
return_date_button.pack(side="left", padx=10, fill="x", expand=True)

# Número de Pasajeros
def validate_passengers_input(input_value):
    if input_value.isdigit() and 1 <= int(input_value) <= 60:
        return True
    else:
        messagebox.showerror("Error", "El número de pasajeros debe estar entre 1 y 60.")
        passengers_entry.delete(0, tk.END)
        return False

passengers_frame = tk.Frame(content_frame, bg="#F1F2F6")
passengers_frame.pack(side="top", pady=10, fill="x", padx=10)
passengers_label = tk.Label(passengers_frame, text="Numero de Pasajeros:", bg="#F1F2F6")
passengers_label.pack(side="left", padx=10)
passengers_entry = CTkEntry(
    passengers_frame,
    placeholder_text="Ingresar",
    border_color="#7732FF", 
    corner_radius=32
)
passengers_entry.pack(side="left", padx=10, fill="x", expand=True)

# Buscar Buses
def search():
    origin = point_origin_input.get()
    destination = point_destination_input.get()
    departure_date = departure_date_button.cget("text")
    return_date = return_date_button.cget("text")
    passengers = passengers_entry.get()

    if (origin == "Selecciona" or
        destination == "Selecciona" or
        origin == destination or
        departure_date == "Selecciona" or
        not passengers.isdigit() or
        not 1 <= int(passengers) <= 60):
        messagebox.showerror("Error", "Debe ingresar todos los datos correctamente")
        return

    if return_date != "Selecciona" and return_date < departure_date:
        messagebox.showerror("Error", "La fecha de regreso debe ser posterior a la fecha de partida")
        return

buses_frame = tk.Frame(content_frame, bg="#F1F2F6")
buses_frame.pack(side="top", pady=20, fill="x", padx=10)
bus_button_color = "#7732FF"
buses_available = CTkButton(
    buses_frame,
    text="Buscar Buses",
    corner_radius=32,
    fg_color=bus_button_color,
    hover_color="#5A23CC",
    command=search
)
buses_available.pack(pady=10)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------

all_frames = [loading_frame, start_frame, register_frame, login_frame, content_frame]
loading_screen()

window.mainloop()
