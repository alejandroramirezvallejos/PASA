"""Extraer Datos para Buscar buses"""
def search_buses():
    global point_origin_input, point_destination_input, departure_date_button, return_date_button, passengers_entry, passenger_class_input
    origin = point_origin_input.get()
    destination = point_destination_input.get()
    departure_date = departure_date_button.cget("text")
    return_date = return_date_button.cget("text")
    passengers = passengers_entry.get()
    passenger_class = passenger_class_input.get()
    # Validaciones
    if origin == "Seleccionar":
        messagebox.showerror("Error", "Debes seleccionar un Punto de Origen")
        return
    if destination == "Seleccionar":
        messagebox.showerror("Error", "Debes seleccionar un Punto de Destino")
        return
    if origin == destination:
        messagebox.showerror("Error", "El Punto de Origen no puede ser igual al Punto de Destino")
        return
    if departure_date == "Seleccionar":
        messagebox.showerror("Error", "Debes seleccionar una Fecha de Partida")
        return
    if not passengers.isdigit() or not (1 <= int(passengers) <= 60):
        messagebox.showerror("Error", "El Número de Pasajeros debe ser un número entre 1 y 60")
        return
    if passenger_class == "Seleccionar":
        messagebox.showerror("Error", "Debes seleccionar la Clase de los Pasajeros")
        return
    # Conexión con la Base de Datos
    connection = make_connection()
    if not connection:
        return
    try:
        cursor = connection.cursor()
        # Consulta para Fecha de Partida
        query = """
        SELECT b.bus_id, b.fecha_salida, COUNT(r.bus_id) AS asientos_ocupados
        FROM bus AS b
        JOIN chofer AS c ON b.chofer_id = c.chofer_id
        LEFT JOIN reserva AS r ON b.bus_id = r.bus_id
        WHERE b.ruta_id IN (
        SELECT ruta_id 
        FROM ruta 
        WHERE dep_inicio = '{}' AND dep_final = '{}'
        )
        AND b.fecha_salida = '{}'
        GROUP BY b.bus_id, b.fecha_salida
        HAVING COUNT(r.bus_id) <= (60 - {});
        """
        cursor.execute(query.format(origin, destination, departure_date, int(passengers)))
        buses = cursor.fetchall()
        # Consulta para Fecha de Regreso
        buses_2 = []
        if return_date != "Seleccionar":
            cursor.execute(query.format(destination, origin, return_date, int(passengers)))
            buses_2 = cursor.fetchall()

        # Mostrar Resultados
        results_frame = make_show_results(buses, buses_2, passengers, origin, destination,passenger_class)
        show_frame(results_frame)
    except pyodbc.Error as e:
        messagebox.showerror("Error", f"Error al ejecutar la consulta: {e}")
    finally:
        connection.close()

"""Frame de los Resultados de la busqueda"""
def make_show_results(buses, buses_2, passengers, origin, destination,passenger_class):
    global results_frame, return_date, selected_buses
    return_date = return_date_button.cget("text")
    selected_buses = []  
    # Creación del Frame principal
    results_frame = tk.Frame(window, bg="#F1F2F6")
    results_frame.name = "results"
    results_frame.pack(fill="both", expand=True, padx=10, pady=10)
    # Botón de Regreso y Cerrar Sesión en la parte superior
    show_back_button(results_frame)
    show_log_out_button(results_frame)
    # Crear el sistema de Scroll
    scrollbar = tk.Scrollbar(results_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas = tk.Canvas(results_frame, bg="#F1F2F6", yscrollcommand=scrollbar.set, bd=0, highlightthickness=0)
    canvas.pack(side=tk.LEFT, fill="both", expand=True)
    scrollbar.config(command=canvas.yview)
    content_frame = tk.Frame(canvas, bg="#F1F2F6")
    canvas.create_window((70, 30), window=content_frame, anchor="nw")
    def resize_canvas(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    content_frame.bind("<Configure>", resize_canvas)
    def confirm_booking():
        confirm_window = tk.Toplevel(window)
        confirm_window.title("Confirmación")
        confirm_window.geometry("300x150")
        confirm_window.configure(bg="#F1F2F6")
        confirm_window.geometry("+%d+%d" % (
            window.winfo_x() + window.winfo_width()/2 - 150,
            window.winfo_y() + window.winfo_height()/2 - 75
        ))
        tk.Label(
            confirm_window,
            text="¡Reserva realizada con éxito!",
            bg="#F1F2F6",
            font=("Canva Sans", 12, "bold")
        ).pack(pady=20) 
        try:
            conexion = make_connection()
            cursor=conexion.cursor()
            for bus in selected_buses:
                for i in range(int(passengers)):
                    if(passenger_class=="Economico"):
                        cursor.execute(f"""INSERT INTO reserva (reserva_id, usuario_id,bus_id,vip)
                                        VALUES ({obtain_pk(cursor,"reserva")}, {obtain_userid(cursor)},{bus} ,0);
                        """)
                        conexion.commit()
                    elif(passenger_class=="VIP"):
                        cursor.execute(f"""INSERT INTO reserva (reserva_id, usuario_id,bus_id,vip)
                                        VALUES ({obtain_pk(cursor,"reserva")}, {obtain_userid(cursor)},{bus} ,1);
                        """)
                        conexion.commit()
            conexion.close()
            confirm_window.after(2000, confirm_window.destroy)
            results_frame.after(2100, lambda: on_log_out_button())  
        except Exception as e:
            tk.Label(
                confirm_window,
                text=f"Error: {str(e)}",
                bg="#F1F2F6",
                fg="red",
                font=("Canva Sans", 10)
            ).pack(pady=10)
    def handle_bus_selection(bus_id, button):
        if button.cget("text") == "Seleccionar":
            if len(selected_buses) < 2:
                selected_buses.append(bus_id)
                button.configure(
                    text="Seleccionado",
                    fg_color="gray",
                    hover_color="gray",
                    state="disabled"
                )
                commit_button.configure(state="normal")
        if len(selected_buses) >= 2:
            for child in content_frame.winfo_children():
                if isinstance(child, tk.Frame):
                    for widget in child.winfo_children():
                        if isinstance(widget, CTkButton) and widget.cget("text") == "Seleccionar":
                            widget.configure(state="disabled")
    # Botón para confirmar Selección
    commit_button = CTkButton(
        content_frame,
        text="Confirmar Seleccion",
        corner_radius=32,
        fg_color="#7732FF",
        hover_color="#5A23CC",
        state="disabled",
        command=confirm_booking
    )
    commit_button.grid(row=0, column=0, pady=(0, 30), padx=(70, 0))
    commit_button.place_forget()
    # Mostrar Buses Disponibles de Partida
    if not buses:
        no_results_label = tk.Label(
            content_frame,
            text="No se encontraron Buses Disponibles para la Fecha de Partida",
            bg="#F1F2F6",
            font=("Canva Sans", 12),
            wraplength=350,
            justify="center"
        )
        commit_button.pack(pady=(0, 30))
        commit_button.pack(padx=(70, 0))
        no_results_label.pack(expand=True)
    else:
        commit_button.pack(pady=(0, 30))
        commit_button.pack(padx=(70, 0))
        title_font = font.Font(family="Canva Sans", size=15, weight="bold")
        title_label = tk.Label(
            content_frame,
            text="Selecciona un Bus \npara la Fecha de Partida",
            font=title_font,
            bg="#F1F2F6",
            fg="black",
            wraplength=350,
        )
        title_label.pack(pady=50)
        for idx, bus in enumerate(buses):
            bus_id, fecha_salida, asientos_ocupados = bus
            block_frame = tk.Frame(content_frame, bg="#F1F2F6", padx=10, pady=10)
            block_frame.pack(pady=(10, 0), fill="x")
            detalles = f"""
Bus ID: {bus_id}
Punto de Origen: {origin}
Punto de Destino: {destination}
Fecha de Salida: {fecha_salida}
Asientos Disponibles: {60 - asientos_ocupados}
            """
            label = tk.Label(
                block_frame,
                text=detalles.strip(),
                bg="#F1F2F6",
                anchor="center",  
                justify="center",  
                font=("Arial", 11)
            )
            label.pack(pady=5)
            select_button = CTkButton(
                block_frame,
                text="Seleccionar",
                corner_radius=32,
                fg_color="#7732FF",
                hover_color="#5A23CC",
                command=lambda bid=bus_id, btn=None: handle_bus_selection(bid, btn)
            )
            select_button.pack(pady=(10, 0))
            select_button.configure(command=lambda bid=bus_id, btn=select_button: handle_bus_selection(bid, btn))
            if idx < len(buses) - 1:
                separator = tk.Frame(content_frame, bg="#7732FF", height=2, width=300)
                separator.pack(pady=(10, 10))
                separator.pack_propagate(False)
    # Mostrar Buses Disponibles de Regreso
    if not buses_2 and not return_date == "Seleccionar":
        no_results_label = tk.Label(
            content_frame,
            text="No se encontraron Buses \nDisponibles para la Fecha de Regreso",
            bg="#F1F2F6",
            font=("Canva Sans", 12),
            wraplength=350,
            justify="center"
        )
        no_results_label.pack(expand=True)
    elif not buses_2 and return_date == "Seleccionar":
        no_results_label = tk.Label(
            content_frame,
            text="",
            bg="#F1F2F6",
            font=("Canva Sans", 12)
        )
        no_results_label.pack(expand=True)
    else:
        title_font_2 = font.Font(family="Canva Sans", size=15, weight="bold")
        title_label_2 = tk.Label(
            content_frame,
            text="Selecciona un Bus \npara la Fecha de Regreso",
            font=title_font_2,
            bg="#F1F2F6",
            fg="black",
            wraplength=350,
            justify="center",
        )
        title_label_2.pack(pady=50)
        for idx, bus in enumerate(buses_2):
            bus_id, fecha_salida, asientos_ocupados = bus
            block_frame = tk.Frame(content_frame, bg="#F1F2F6", padx=10, pady=10)
            block_frame.pack(pady=(10, 0), fill="x")
            detalles = f"""
Bus ID: {bus_id}
Punto de Origen: {origin}
Punto de Destino: {destination}
Fecha de Salida: {fecha_salida}
Asientos Disponibles: {60 - asientos_ocupados}
            """
            label = tk.Label(
                block_frame,
                text=detalles.strip(),
                bg="#F1F2F6",
                anchor="center",  
                justify="center",  
                font=("Arial", 11)
            )
            label.pack(pady=5) 
            select_button = CTkButton(
                block_frame,
                text="Seleccionar",
                corner_radius=32,
                fg_color="#7732FF",
                hover_color="#5A23CC",
                command=lambda bid=bus_id, btn=None: handle_bus_selection(bid, btn)
            )
            select_button.pack(pady=(10, 0))
            select_button.configure(command=lambda bid=bus_id, btn=select_button: handle_bus_selection(bid, btn))
            if idx < len(buses_2) - 1:
                separator = tk.Frame(content_frame, bg="#7732FF", height=2, width=300)
                separator.pack(pady=(10, 10))
                separator.pack_propagate(False)
    return results_frame