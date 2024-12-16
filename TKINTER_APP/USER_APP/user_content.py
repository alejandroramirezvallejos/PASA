import tkinter as tk
from tkinter import messagebox, font
from tkcalendar import Calendar
from datetime import date
from customtkinter import CTkComboBox, CTkButton, CTkEntry
from USER_APP import action_bar as a, search_bus as sh

"""Frame de Area de contenido"""
def make_content_frame(window):
    global content_frame, point_origin_input, point_destination_input, departure_date_button, return_date_button, passengers_entry, passenger_class_input
    # Creando Frame
    content_frame = tk.Frame(window, bg="#F1F2F6")
    content_frame.name = "content"
    title_font = font.Font(family="Canva Sans", size=15, weight="bold")
    title_label = tk.Label(
        content_frame,
        text="¿Cuales son tus planes de viaje?",
        font=title_font,
        bg="#F1F2F6",
        fg="black",
        wraplength=350,
        justify="center",
    )
    title_label.pack(pady=50)
    combo_fg_color = "#F1F2F6"
    combo_button_color = "#7732FF"
    combo_border_color = "#7732FF"
    # Boton de Cerrar Sesion
    a.show_log_out_button(content_frame)
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
    point_origin_input.set("Seleccionar")
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
    point_destination_input.set("Seleccionar")
    point_destination_txt.pack(side="left", padx=10)
    point_destination_input.pack(side="left", padx=10)
    # Calendario
    def open_calendar(min_date, max_date, callback):
        calendar_window = tk.Toplevel(window)
        calendar_window.title("Selecciona la Fecha")
        calendar_window.configure(bg="#F1F2F6")
        calendar_window.geometry("320x250+150+85")
        try:
            calendar_window.iconbitmap("../../ASSETS/icon.ico")
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
        text="Seleccionar",
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
    # Verificando el correcto orden de selección de Fecha de Regreso
    def enable_return_date_selection():
        departure_date = departure_date_button.cget("text")  
        if departure_date == "Seleccionar":
            messagebox.showerror("Error", "Primero selecciona la Fecha de Partida")
        else:
            try:
                # Convertir la fecha de partida a un objeto datetime
                min_date = date.fromisoformat(departure_date)
                open_calendar(
                    min_date, 
                    date(2025, 12, 31),  
                    lambda selected_date: validate_return_date(min_date, selected_date)
                )
            except ValueError:
                messagebox.showerror("Error", "Fecha de Partida invalida")
    # Verificando que a Fecha de Regreso sea posterior a la Fecha de Partida
    def validate_return_date(departure_date, return_date):
        try:
            return_date_obj = date.fromisoformat(return_date)
            if return_date_obj <= departure_date:
                messagebox.showerror("Error", "La Fecha de Regreso debe ser posterior a la Fecha de Partida")
            else:
                return_date_button.configure(text=return_date)  
        except ValueError:
            messagebox.showerror("Error", "Fecha de Regreso invalida")
    return_date_button = CTkButton(
        return_date_frame,
        text="Seleccionar",
        corner_radius=32,
        fg_color="#F1F2F6",
        text_color="#000000",
        hover_color="#E1E1E1",
        border_color="#7732FF",
        border_width=2,
        command=enable_return_date_selection
    )
    return_date_button.pack(side="left", padx=10, fill="x", expand=True)
    # Numero de Pasajeros
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
    # Clase del Pasajero
    passenger_class_frame = tk.Frame(content_frame, bg="#F1F2F6")
    passenger_class_frame.pack(side="top", pady=10, fill="x", padx=10)
    passenger_class_txt = tk.Label(passenger_class_frame, text="Clase:", bg="#F1F2F6")
    passenger_class_input = CTkComboBox(
        passenger_class_frame,
        values=["Economico", "VIP"],
        fg_color=combo_fg_color,
        button_color=combo_button_color,
        border_color=combo_border_color,
        corner_radius=32,
        state="readonly" 
    )
    passenger_class_input.set("Seleccionar")
    passenger_class_txt.pack(side="left", padx=10)
    passenger_class_input.pack(side="left", padx=10)
    # Boton de Buscar Buses
    buses_frame = tk.Frame(content_frame, bg="#F1F2F6")
    buses_frame.pack(side="top", pady=20, fill="x", padx=10)
    bus_button_color = "#7732FF"
    buses_available = CTkButton(
        buses_frame,
        text="Buscar Buses",
        corner_radius=32,
        fg_color=bus_button_color,
        hover_color="#5A23CC",
        command=sh.search_buses
    )
    buses_available.pack(pady=10)
    return content_frame