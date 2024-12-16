import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tkinter as tk 
from tkinter import messagebox, font
from tkcalendar import Calendar
from datetime import date
from PIL import Image, ImageTk
from customtkinter import CTkComboBox, CTkButton, CTkEntry, set_appearance_mode, set_default_color_theme

"""Frame para Buscar Datos"""
def make_fetch_frame():
    global current_frame, navigation_bar, action_bar
    fetch_frame = tk.Frame(window, bg="#09090A")
    fetch_frame.name = "fetch"
    # Función para abrir una ventana con datos de una tabla
    def open_table_window(fetch_function, title):
        connection = c.make_connection()
        if not connection:
            return
        cursor = connection.cursor()
        try:
            data = fetch_function(cursor)  
            if not data:
                messagebox.showinfo("Información", f"No hay datos en la tabla {title}.")
                return
            # Crear una nueva ventana
            table_window = tk.Toplevel(fetch_frame)
            table_window.title(f"Tabla: {title}")
            table_window.geometry("600x400")
            table_window.configure(bg="#09090A")
            # Crear un Treeview para mostrar los datos
            tree = ttk.Treeview(table_window, show="headings", selectmode="browse")
            tree.pack(fill="both", expand=True)
            # Crear encabezados basados en las columnas
            columns = [desc[0] for desc in cursor.description]
            tree["columns"] = columns
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, anchor="center")
            # Insertar datos en el Treeview
            for row in data:
                cleaned_row = [item.strip() if isinstance(item, str) else item for item in row]
                tree.insert("", "end", values=cleaned_row)
            # Botón para cerrar la ventana
            close_button = tk.Button(table_window, text="Cerrar", command=table_window.destroy, bg="#7732FF", fg="white")
            close_button.pack(pady=10)
        except pyodbc.Error as e:
            messagebox.showerror("Error", f"No se pudo obtener datos: {e}")
        finally:
            connection.close()
    # Botón para mostrar la tabla de buses
    bus_button = CTkButton(
        fetch_frame,
        text="Ver Buses",
        corner_radius=32,
        fg_color="#7732FF",
        hover_color="#5A23CC",
        command=lambda: open_table_window(f.get_bus, "Buses")
    )
    bus_button.pack(pady=10, padx=20, fill="x")
    # Botón para mostrar la tabla de choferes
    driver_button = CTkButton(
        fetch_frame,
        text="Ver Choferes",
        corner_radius=32,
        fg_color="#7732FF",
        hover_color="#5A23CC",
        command=lambda: open_table_window(f.get_driver, "Choferes")
    )
    driver_button.pack(pady=10, padx=20, fill="x")
    # Botón para mostrar la tabla de rutas
    route_button = CTkButton(
        fetch_frame,
        text="Ver Rutas",
        corner_radius=32,
        fg_color="#7732FF",
        hover_color="#5A23CC",
        command=lambda: open_table_window(f.get_route, "Rutas")
    )
    route_button.pack(pady=10, padx=20, fill="x")
    # Botón para mostrar la tabla de reservas
    booking_button = CTkButton(
        fetch_frame,
        text="Ver Reservas",
        corner_radius=32,
        fg_color="#7732FF",
        hover_color="#5A23CC",
        command=lambda: open_table_window(f.get_booking, "Reservas")
    )
    booking_button.pack(pady=10, padx=20, fill="x")
    return fetch_frame