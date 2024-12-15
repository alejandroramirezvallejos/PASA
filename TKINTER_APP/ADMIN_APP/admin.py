""" pip install tk
    pip install pyodbc
    pip install tkcalendar
    pip install pillow
    pip install customtkinter
"""
import tkinter as tk
from tkinter import ttk
import pyodbc
from tkinter import messagebox, font
from tkcalendar import Calendar
from datetime import date
from PIL import Image, ImageTk
import customtkinter as ctk
from customtkinter import CTkComboBox, CTkButton, CTkEntry, set_appearance_mode, set_default_color_theme
import functions_query as f
window = None
current_frame = None
add_frame = None
option_frame = None
update_frame = None
delete_frame = None
fetch_frame = None
navigation_bar = None
action_bar = None
start_frame = None
register_frame = None
login_frame = None
terms_frame = None
loading_frame = None
all_frames = []
# ---------------------------------------------------CONEXION CON BASE DE DATOS------------------------------------------------------------------------------------------------

"""Configurando la Conexion con la Base de Datos"""
driver = '{ODBC Driver 17 for SQL Server}'
server = 'JOSUEPC'  
database = 'pasa'
username = 'JOSUEPC\\user'

"""Creando Conexion con la Base de Datos"""
def make_connection():
    try:
        connection = pyodbc.connect(
            f"DRIVER={driver};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={username};"
            f"Trusted_Connection=yes;"
        )
        return connection
    except pyodbc.Error as e:
        if '28000' in str(e):
            messagebox.showerror(
                "Error de conexión", "Verifica las credenciales de la Base de Datos"
            )
        else:
            messagebox.showerror("Error de conexión", f"No se pudo conectar a SQL Server: {e}")
        return None

# ----------------------------------------------------ENTRADA Y SALIDA DE DATOS-----------------------------------------------------------------------------------------------

"""Guardar Datos al Crear una Cuenta"""
def create_account():
    # Entrada de Datos
    global fetch_frame, name_entry, last_name_entry, age_entry, id_card_entry, password_entry
    name = name_entry.get().strip()
    last_name = last_name_entry.get().strip()
    age = age_entry.get().strip()
    id_card = id_card_entry.get().strip()
    password = password_entry.get().strip()
    # Manejo de Errores
    if not all([name]):
        messagebox.showerror("Error", "Debes ingresar tu Nombre")
        return
    if not all([last_name]):
        messagebox.showerror("Error", "Debes ingresar tus Apellidos")
        return
    if not all([age]):
        messagebox.showerror("Error", "Debes ingresar tu Edad")
        return
    if not age.isdigit():
        messagebox.showerror("Error", "Tu Edad debe ser un numero natural")
        return
    if not int(age) >= 18:
        messagebox.showerror("Error", "No puedes Crear una Cuenta si eres menor de edad")
        return
    if not all([id_card]):
        messagebox.showerror("Error", "Debes ingresar tu Numero de Carnet")
        return
    if not id_card.isdigit():
        messagebox.showerror("Error", "El Numero de Carnet debe ser un numero natural")
        return
    if not len(id_card) == 7:
        messagebox.showerror("Error", "El Numero de Carnet debe tener 7 digitos")
        return
    if f.validate_carnet(id_card)==True:
        messagebox.showerror("Error", "Carnet ya existente")
        return
    if not all([password]):
        messagebox.showerror("Error", "Debes crear una Contraseña")
        return
    # Borrar Datos en caso de Error
    name_entry.delete(0, tk.END)
    last_name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    id_card_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    # Conexion con la Base de Datos
    connection = make_connection()
    if not connection:
        return
    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO usuario (usuario_id,nombre, apellido, edad, carnet, contraseña, admin) 
        VALUES ({},'{}','{}',{},{},'{}',0);
        """
        cursor.execute(query.format(f.obtain_pk(cursor,"usuario"),name, last_name, age, id_card, password))
        connection.commit()
        # Cambiar al fetch_frame si todo sale bien
        show_frame(fetch_frame)
    except pyodbc.Error as e:
        messagebox.showerror("Error", f"Error al registrar la cuenta: {e}")
    finally:
        connection.close()

"""Extraer Datos para Verificar el Inicio de Sesion"""
def login():
    # Entrada de Datos
    global fetch_frame
    id_card = login_id_card_entry.get().strip()
    password = login_password_entry.get().strip()
    # Verificar la correcta Entrada de Datos
    if not all([id_card]):
        messagebox.showerror("Error", "Debes ingresar tu Numero de Carnet")
        return
    if not id_card.isdigit():
        messagebox.showerror("Error", "El Numero de Carnet debe ser un numero natural")
        return
    if not len(id_card) == 7:
        messagebox.showerror("Error", "El Numero de Carnet debe tener 7 digitos")
        return
    if not all([password]):
        messagebox.showerror("Error", "Debes ingresar tu Contraseña")
        return
    # Borrar Datos en caso de Error
    login_id_card_entry.delete(0, tk.END)
    login_password_entry.delete(0, tk.END)
    # Conexion con la Base de Datos
    connection = make_connection()
    if not connection:
        return
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM dbo.usuario WHERE carnet = ? AND contraseña = ?"
        cursor.execute(query, (id_card, password))
        usuario = cursor.fetchone()
        # Cambiar al fetch_frame si todo sale bien
        if usuario:
            show_frame(fetch_frame)
        else:
            messagebox.showerror("Error", "Datos incorrectos. Verifique su usuario y contraseña")
    except pyodbc.Error as e:
        messagebox.showerror("Error", f"Error al realizar la consulta: {e}")
    finally:
        connection.close()

"""Funcion para Realizar Consultas"""
def queries_option():
    # Obtener datos del frame actual
    global option, current_frame, point_origin_input, point_destination_input, departure_date_button, return_date_button
    # Establecer la conexión con la base de datos
    connection = make_connection()
    if not connection:
        return
    cursor = connection.cursor()
    try:
        # Determinar el tipo de operación y frame actual
        if current_frame == add_frame:
            action = "add"
        elif current_frame == delete_frame:
            action = "delete"
        elif current_frame == update_frame:
            action = "update"
        else:
            messagebox.showerror("Error", "Operación no válida o Frame desconocido.")
            return
        # Operaciones según el Frame
        if action == "add":
            if "Agregar Bus" in option.get():
                # Extraer datos para agregar un bus
                chofer_id = int(option.get())  
                ruta_id = int(point_destination_input.get())
                nombre = "Bus_" + option.get() 
                fecha_sal = departure_date_button.cget("text")
                fecha_ret = return_date_button.cget("text")
                # Llamar a la función de agregar bus
                f.add_bus(chofer_id, ruta_id, nombre, fecha_sal, fecha_ret)
                messagebox.showinfo("Éxito", "Bus agregado correctamente.")
            elif "Agregar Chofer" in option.get():
                # Extraer datos para agregar un chofer
                nombre = option.get()
                edad = int(point_origin_input.get())
                carnet = int(return_date_button.cget("text"))  
                f.add_driver(nombre, edad, carnet)
                messagebox.showinfo("Éxito", "Chofer agregado correctamente")
            elif "Agregar Ruta" in option.get():
                dep_inicio = point_origin_input.get()
                dep_final = point_destination_input.get()
                costo = float(departure_date_button.cget("text"))
                costo_vip = float(return_date_button.cget("text"))
                f.add_route(dep_inicio, dep_final, costo, costo_vip)
                messagebox.showinfo("Éxito", "Ruta agregada correctamente")
        elif action == "delete":
            if "Eliminar Bus" in option.get():
                # Obtener el ID del bus
                bus_id = int(option.get())
                f.del_bus(bus_id)
                messagebox.showinfo("Éxito", "Bus eliminado correctamente")
            elif "Eliminar Chofer" in option.get():
                chofer_id = int(option.get())
                f.del_driver(chofer_id)
                messagebox.showinfo("Éxito", "Chofer eliminado correctamente")
            elif "Eliminar Ruta" in option.get():
                ruta_id = int(option.get())
                f.del_route(ruta_id)
                messagebox.showinfo("Éxito", "Ruta eliminada correctamente")
        elif action == "update":
            if "Actualizar Bus" in option.get():
                # Obtener datos del bus para actualizar
                bus_id = int(option.get())
                chofer_id = int(point_origin_input.get())
                ruta_id = int(point_destination_input.get())
                nombre = "Bus_" + option.get()
                fecha_sal = departure_date_button.cget("text")
                fecha_ret = return_date_button.cget("text")
                # Llamar a la función de actualizar bus
                f.update_bus(bus_id, chofer_id, ruta_id, nombre, fecha_ret, fecha_sal)
                messagebox.showinfo("Éxito", "Bus actualizado correctamente")
            elif "Actualizar Chofer" in option.get():
                chofer_id = int(option.get())
                nombre = point_origin_input.get()
                edad = int(point_destination_input.get())
                carnet = int(departure_date_button.cget("text"))
                f.update_driver(chofer_id, nombre, edad, carnet)
                messagebox.showinfo("Éxito", "Chofer actualizado correctamente")
            elif "Actualizar Ruta" in option.get():
                ruta_id = int(option.get())
                dep_inicio = point_origin_input.get()
                dep_final = point_destination_input.get()
                costo = float(departure_date_button.cget("text"))
                costo_vip = float(return_date_button.cget("text"))
                f.update_route(ruta_id, dep_inicio, dep_final, costo, costo_vip)
                messagebox.showinfo("Éxito", "Ruta actualizada correctamente")
    except ValueError as ve:
        messagebox.showerror("Error", f"Datos inválidos: {ve}")
    except pyodbc.Error as e:
        messagebox.showerror("Error", f"Error en la base de datos: {e}")
    finally:
        # Cerrar la conexión
        connection.close()

# ------------------------------------------------------------FRAMES---------------------------------------------------------------------------------------------

"""Pantalla de Carga"""
def make_loading_screen():
    # Creando Frame
    loading_frame = tk.Frame(window, bg="#09090A")  
    loading_frame.name = "loading"
    loading_frame.pack(fill="both", expand=True)
    # Agregando Icono
    try:
        pasa_iso = "../../ASSETS/color_negative_admin.png"
        image = Image.open(pasa_iso)
        image = image.resize((200, 200), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        iso_label = tk.Label(loading_frame, image=photo, bg="#09090A")  
        iso_label.image = photo  
        iso_label.pack(expand=True)
    except Exception as e:
        print(f"Error al cargar el Logo: {e}")
    # Tiempo de Espera
    def delayed_show_start_frame():
        window.configure(bg="#09090A")
        show_frame(start_frame)
    window.after(1500, delayed_show_start_frame)
    return loading_frame

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
            elif current_frame == fetch_frame:
                fetch_frame.pack_forget()
                hide_log_out_button()
                show_frame(start_frame)
            elif current_frame == update_frame:
                update_frame.pack_forget()
                hide_log_out_button()
                show_frame(start_frame)
            elif current_frame == delete_frame:
                delete_frame.pack_forget()
                hide_log_out_button()
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

"""Frame Inicial"""
def make_start_frame():
    # Creacion del Frame
    start_frame = tk.Frame(window, bg="#09090A")
    start_frame.name = "start"
    # Agregando Icono
    try:
        pasa_iso = "../../ASSETS/color_positive_admin.png"
        image = Image.open(pasa_iso)
        image = image.resize((170, 170), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        iso_label = tk.Label(start_frame, image=photo, bg="#09090A")  
        iso_label.image = photo  
        iso_label.pack(expand=True)
    except Exception as e:
        print(f"Error al cargar el Logo: {e}")
    # Texto
    title_font = font.Font(family="Canva Sans", size=15, weight="bold")
    title_label = tk.Label(
        start_frame,
        text="¡Gestionar una Base de Datos nunca fue mas sencillo!",
        font=title_font,
        bg="#090906",
        fg="#7732FF",
        wraplength=350,
        justify="center",
    )
    title_label.pack(pady=50)
    # Boton de Inicio de Sesion
    login_button = CTkButton(
        start_frame,
        text="Iniciar Sesion",
        corner_radius=32,
        fg_color="#C8BCF6",
        text_color="#09090A",
        hover_color="#C8BCF6",
        command=lambda: show_frame(login_frame),
    )
    login_button.pack(pady=10)
    # Boton de Creacion de Cuenta
    signup_button = CTkButton(
        start_frame,
        text="Crear cuenta",
        corner_radius=32,
        fg_color="#C8BCF6",
        text_color="#09090A",
        hover_color="#C8BCF6",
        command=lambda: show_frame(register_frame),
    )
    signup_button.pack(pady=10)
    # Texto de Términos y Condiciones
    terms_label = tk.Label(
        start_frame,
        text="Al crear una cuenta, confirmo que he leído y acepto los ",
        font=("Arial", 10),
        bg="#09090A",
        fg="#C8BCF6",
    )
    terms_label.pack(pady=(30, 5), side="top", anchor="center")
    # Crear enlace para "Términos y condiciones"
    terms_link = tk.Label(
        start_frame,
        text="Terminos y Condiciones de Uso",
        font=("Arial", 10, "underline"),
        bg="#09090A",
        fg="#7732FF",
        cursor="hand2",
    )
    terms_link.pack(side="top", anchor="center")
    # Vincular el clic al enlace
    terms_link.bind("<Button-1>", lambda e: show_frame(terms_frame))
    return start_frame

"""Frame para ver los Terminos y Condiciones de Uso"""
def make_terms_frame():
    # Crear el frame de términos y condiciones
    terms_frame = tk.Frame(window, bg="#09090A")
    terms_frame.name = "terms"
    # Título principal
    title_label = tk.Label(
        terms_frame,
        text="Términos y Condiciones de Uso",
        font=("Arial", 16, "bold"),
        bg="#09090A",
        fg="#7732FF",
    )
    title_label.pack(pady=20)
    # Crear un Scrollbar
    scrollbar = tk.Scrollbar(terms_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas = tk.Canvas(terms_frame, bg="#09090A", yscrollcommand=scrollbar.set, bd=0, highlightthickness=0)
    canvas.pack(side=tk.LEFT, fill="both", expand=True)
    scrollbar.config(command=canvas.yview)
    # Agregando el Contenido
    content_text_frame = tk.Frame(canvas, bg="#09090A")
    canvas.create_window((0, 0), window=content_text_frame, anchor="nw")
    def resize_canvas(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    content_text_frame.bind("<Configure>", resize_canvas)
    # Contenido por Secciones
    sections = [
        (
            "1. Aceptación de los Términos",
            """Al crear una cuenta en nuestra plataforma, usted declara que ha leído, comprendido y aceptado en su totalidad los presentes Términos y Condiciones. Asimismo, se compromete a cumplir con todas las leyes, normativas y reglamentos aplicables, incluidos aquellos que pudieran requerir una interpretación exhaustiva."""
        ),
        (
            "2. Privacidad y Tratamiento de Datos",
            """Al aceptar, usted otorga permiso para que compartamos, distribuyamos o regalemos sus datos personales a entidades selectas. Estas pueden incluir agencias gubernamentales misteriosas, civilizaciones extraterrestres y organizaciones con nombres demasiado interesantes para ser ignorados. Nos reservamos el derecho de decidir, a nuestra entera discreción, las entidades receptoras de esta información, todo esto, por supuesto, en aras de la innovación, seguridad y el progreso."""
        ),
        (
            "3. Responsabilidades del Usuario",
            """Como usuario registrado, usted asume la obligación de colaborar con los proyectos y objetivos educativos establecidos por la plataforma. Esto incluye, pero no se limita a, garantizar un puntaje perfecto de 100 en cualquier examen final presentado por los creadores de esta aplicación."""
        ),
        (
            "4. Modificaciones a los Términos",
            """Nos reservamos el derecho de modificar estos términos en cualquier momento. No prometemos avisarle, pero contamos con su confianza ciega. La continuación en el uso de nuestra plataforma tras cualquier modificación implicará la aceptación implícita de los cambios realizados."""
        ),
        (
            "5. Limitación de Responsabilidad",
            """La plataforma no se hará responsable por cualquier consecuencia derivada del uso indebido de su tiempo, datos personales, o información sensible, incluyendo, pero no limitado a, datos bancarios o información financiera. Al aceptar estos términos, usted exonera a la plataforma de cualquier reclamación derivada de tales eventos."""
        ),
        (
            "6. Aceptación y Carácter Vinculante",
            """Al continuar con el uso de nuestros servicios, usted acepta de manera irrevocable y vinculante los presentes Términos y Condiciones, comprometiéndose a no impugnar su validez o aplicación en ningún momento."""
        ),
    ]
    # Secciones
    for title, content in sections:
        section_frame = tk.Frame(content_text_frame, bg="#09090A")
        section_frame.pack(fill="x", padx=20, pady=10)
        # Título en negrita
        title_label = tk.Label(
            section_frame,
            text=title,
            font=("Arial", 12, "bold"),
            bg="#09090A",
            fg="#7732FF",
            anchor="w",
        )
        title_label.pack(fill="x")
        # Contenido justificado
        content_text_label = tk.Label(
            section_frame,
            text=content,
            font=("Arial", 10),
            bg="#09090A",
            fg="#C8BCF6",
            anchor="w",
            justify="left",
            wraplength=335,
        )
        content_text_label.pack(fill="x")
    # Botón para regresar
    show_back_button(terms_frame)
    return terms_frame

"""Frame para Crear una Cuenta"""
def make_register_frame():
    global name_entry, last_name_entry, age_entry, id_card_entry, password_entry
    # Creando el Frame
    register_frame = tk.Frame(window, bg="#09090A")
    register_frame.name = "register"
    title_font = font.Font(family="Canva Sans", size=15, weight="bold")
    title_label = tk.Label(
        register_frame,
        text="Crear Cuenta Administrativa",
        font=title_font,
        bg="#09090A",
        fg="#7732FF",
        wraplength=350,
        justify="center",
    )
    title_label.pack(pady=50)
    # Ingresando el Nombre
    name_frame = tk.Frame(register_frame, bg="#09090A")
    name_frame.pack(side="top", pady=10, fill="x", padx=10)
    name_label = tk.Label(name_frame, text="Nombre:", bg="#09090A", fg="#C8BCF6")
    name_label.pack(side="left", padx=10)
    name_entry = CTkEntry(
        name_frame,
        placeholder_text="Ingresar",
        border_color="#C8BCF6",
        corner_radius=32
    )
    name_entry.pack(side="left", padx=10, fill="x", expand=True)
    # Ingresando los Apellidos
    last_name_frame = tk.Frame(register_frame, bg="#09090A")
    last_name_frame.pack(side="top", pady=10, fill="x", padx=10)
    last_name_label = tk.Label(last_name_frame, text="Apellidos:", bg="#09090A", fg="#C8BCF6")
    last_name_label.pack(side="left", padx=10)
    last_name_entry = CTkEntry(
        last_name_frame,
        placeholder_text="Ingresar",
        border_color="#C8BCF6",
        corner_radius=32
    )
    last_name_entry.pack(side="left", padx=10, fill="x", expand=True)
    # Ingresando la Edad
    age_frame = tk.Frame(register_frame, bg="#09090A")
    age_frame.pack(side="top", pady=10, fill="x", padx=10)
    age_label = tk.Label(age_frame, text="Edad:", bg="#09090A", fg="#C8BCF6")
    age_label.pack(side="left", padx=10)
    age_entry = CTkEntry(
        age_frame,
        placeholder_text="Ingresar",
        border_color="#C8BCF6",
        corner_radius=32
    )
    age_entry.pack(side="left", padx=10, fill="x", expand=True)
    # Ingresando el Carnet
    id_card_frame = tk.Frame(register_frame, bg="#09090A")
    id_card_frame.pack(side="top", pady=10, fill="x", padx=10)
    id_card_label = tk.Label(id_card_frame, text="Carnet:", bg="#09090A", fg="#C8BCF6")
    id_card_label.pack(side="left", padx=10)
    id_card_entry = CTkEntry(
        id_card_frame,
        placeholder_text="Ingresar",
        border_color="#C8BCF6",
        corner_radius=32
    )
    id_card_entry.pack(side="left", padx=10, fill="x", expand=True)
    # Ingresando la Contraseña
    password_frame = tk.Frame(register_frame, bg="#09090A")
    password_frame.pack(side="top", pady=10, fill="x", padx=10)
    password_label = tk.Label(password_frame, text="Contraseña:", bg="#09090A", fg="#C8BCF6")
    password_label.pack(side="left", padx=10)
    password_entry = CTkEntry(
        password_frame,
        placeholder_text="Ingresa",
        show="*",
        border_color="#C8BCF6",
        corner_radius=32
    )
    password_entry.pack(side="left", padx=10, fill="x", expand=True)
    # Boton para Crear Cuenta
    create_account_button = CTkButton(
        register_frame,
        text="Crear cuenta",
        corner_radius=32,
        fg_color="#C8BCF6",
        text_color="#09090A",
        hover_color="#09090A",
        command=create_account
    )
    create_account_button.pack(pady=10) 
    # Botón de Regreso
    show_back_button()
    return register_frame

"""Frame para Iniciar Sesion"""
def make_login_frame():
    global login_frame, login_id_card_entry, login_password_entry
    # Creando Frame
    login_frame = tk.Frame(window, bg="#09090A")
    login_frame.name = "login"
    title_font = font.Font(family="Canva Sans", size=15, weight="bold")
    title_label = tk.Label(
        login_frame,
        text="Inicio de Sesion Administrativa",
        font=title_font,
        bg="#09090A",
        fg="#7732FF",
        wraplength=350,
        justify="center",
    )
    title_label.pack(pady=50)
    # Ingresando el Carnet
    login_id_card_frame = tk.Frame(login_frame, bg="#09090A")
    login_id_card_frame.pack(side="top", pady=10, fill="x", padx=10)
    login_id_card_label = tk.Label(login_id_card_frame, text="Carnet:", bg="#09090A", fg="#C8BCF6")
    login_id_card_label.pack(side="left", padx=10)
    login_id_card_entry = CTkEntry(
        login_id_card_frame,
        placeholder_text="Ingresar",
        border_color="#C8BCF6",
        corner_radius=32
    )
    login_id_card_entry.pack(side="left", padx=10, fill="x", expand=True)
    # Ingresando la Contraseña
    login_password_frame = tk.Frame(login_frame, bg="#09090A")
    login_password_frame.pack(side="top", pady=10, fill="x", padx=10)
    login_password_label = tk.Label(login_password_frame, text="Contraseña:", bg="#09090A", fg="#C8BCF6")
    login_password_label.pack(side="left", padx=10)
    login_password_entry = CTkEntry(
        login_password_frame,
        placeholder_text="Ingresar",
        show="*",
        border_color="#C8BCF6",
        corner_radius=32
    )
    login_password_entry.pack(side="left", padx=10, fill="x", expand=True)
    # Boton para Iniciar Sesion
    login_button_submit = CTkButton(
        login_frame,
        text="Iniciar Sesion",
        corner_radius=32,
        fg_color="#7732FF",
        text_color="black",
        hover_color="#5A23CC",
        command=login
    )
    login_button_submit.pack(pady=10)
    # Botón de Regreso
    show_back_button()
    return login_frame

# ------------------------------------------------------------MANEJO DE COMANDOS---------------------------------------------------------------------------------------------

"""Frame para Buscar Datos"""
def make_fetch_frame():
    global current_frame, navigation_bar, action_bar
    fetch_frame = tk.Frame(window, bg="#09090A")
    fetch_frame.name = "fetch"
    # Función para abrir una ventana con datos de una tabla
    def open_table_window(fetch_function, title):
        connection = make_connection()
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

"""Frame para Crear Botones Predeterminados"""
def make_option_frame(parent, title_name):
    option_frame = ttk.Frame(parent)
    global option 
    option = ttk.Entry(option_frame) 
    option.pack(padx=10, pady=10)
    # Scrollbar
    canvas = tk.Canvas(option_frame, bg="#09090A", highlightthickness=0)
    scrollbar = tk.Scrollbar(option_frame, orient="vertical", command=canvas.yview)
    # Crear un marco interno dentro del canvas
    scrollable_frame = tk.Frame(canvas, bg="#09090A")
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    # Vincular el marco interno con el canvas
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
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
    # Función auxiliar para crear campos de entrada
    def create_input_field(parent, label_text, placeholder):
        frame = tk.Frame(parent, bg="#09090A")
        frame.pack(side="top", pady=10, fill="x", padx=10)
        label = tk.Label(frame, text=label_text, bg="#09090A", fg="#C8BCF6")
        label.pack(side="left", padx=10)
        entry = CTkEntry(
            frame,
            placeholder_text=placeholder,
            border_color="#C8BCF6",
            corner_radius=32,
        )
        entry.pack(side="left", padx=10, fill="x", expand=True)
    create_input_field(scrollable_frame, "Bus ID:", "Ingresar")
    create_input_field(scrollable_frame, "Nombre del Bus:", "Ingresar")
    create_input_field(scrollable_frame, "Chofer ID:", "Ingresar")
    create_input_field(scrollable_frame, "Ruta ID:", "Ingresar")
    # Boton de Bus
    bus_frame = tk.Frame(scrollable_frame, bg="#F1F2F6")
    bus_frame.pack(side="top", pady=20, fill="x", padx=10)
    bus_button_color = "#7732FF"
    bus_available = CTkButton(
        bus_frame,
        text=f"{title_name} Bus",
        corner_radius=32,
        fg_color=bus_button_color,
        hover_color="#5A23CC",
    )
    bus_available.pack(pady=10)
    return option_frame

"""Frame para Agregar Datos"""
def make_add_frame():
    global current_frame, add_frame, option_frame
    if add_frame is None:
        add_frame = tk.Frame(window, bg="#09090A")
        add_frame.name = "add"
    # Asegurar que `option_frame` está correctamente asociado al frame actual
    if option_frame is None or option_frame.master != add_frame:
        option_frame = make_option_frame(add_frame, "Agregar")
        option_frame.pack(fill="both", expand=True)
    # Cambiar al nuevo frame
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
    # Asegurar que `option_frame` está correctamente asociado al frame actual
    if option_frame is None or option_frame.master != update_frame:
        option_frame = make_option_frame(update_frame, "Actualizar")
        option_frame.pack(fill="both", expand=True)
    # Cambiar al nuevo frame
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
    # Asegurar que `option_frame` está correctamente asociado al frame actual
    if option_frame is None or option_frame.master != delete_frame:
        option_frame = make_option_frame(delete_frame, "Eliminar")
        option_frame.pack(fill="both", expand=True)
    # Cambiar al nuevo frame
    if current_frame:
        current_frame.pack_forget()
    current_frame = delete_frame
    current_frame.pack(fill="both", expand=True)
    show_option(target_frame=delete_frame)
    return delete_frame

# ----------------------------------------------------------MOSTRAR Y OCULTAR FRAMES-----------------------------------------------------------------------------------------------

"""Funcion para Mostrar un Frame"""
def show_frame(frame_to_show):
    global all_frames, action_bar, back_button, log_out_button, current_frame
    # Ocultar frame actual
    if current_frame:
        current_frame.pack_forget()
    current_frame = frame_to_show  
    frame_to_show.pack(expand=True)
    # Ocultar todos los frames
    for frame in all_frames:
        frame.pack_forget()
    # Gestionar visibilidad de la barra de acción
    if hasattr(frame_to_show, "name") and frame_to_show.name in ["loading", "start"]:
        action_bar.pack_forget()
        hide_back_button()
        hide_log_out_button()
        navigation_bar.pack_forget()
    else:
        if frame_to_show.name in ["login", "register", "terms"]:
            action_bar.pack(side="top", fill="x")
            show_back_button()
            hide_log_out_button()
            navigation_bar.pack_forget()
        else:
            hide_option()
            action_bar.pack(side="top", fill="x")
            hide_back_button()
            show_log_out_button()
            navigation_bar.pack(side="bottom", fill="x")
    frame_to_show.pack(expand=True)

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

# ----------------------------------------------------------------MAIN--------------------------------------------------------------------------------------------

"""Funcion Principal"""
def main():
    global window, all_frames, start_frame, register_frame, login_frame, action_bar, terms_frame
    global current_frame, loading_frame, add_frame, update_frame, delete_frame, fetch_frame, navigation_bar
    # Configuración de la ventana
    set_appearance_mode("#09090A")
    set_default_color_theme("blue")
    window = tk.Tk()
    window.title("Pasa")
    window.geometry("380x750+120+10")
    window.resizable(False, False)
    window.configure(bg="#09090A")
    # Crear barras y frames
    action_bar = make_action_bar()
    action_bar.pack_forget()
    navigation_bar = make_navigation_bar(window, None, None, None, None)
    navigation_bar.pack_forget()
    # Crear Frames
    loading_frame = make_loading_screen()
    start_frame = make_start_frame()
    register_frame = make_register_frame()
    login_frame = make_login_frame()
    add_frame = make_add_frame()
    update_frame = make_update_frame()
    delete_frame = make_delete_frame()
    fetch_frame = make_fetch_frame()
    terms_frame = make_terms_frame()
    all_frames = [
        loading_frame, start_frame, register_frame,
        login_frame, fetch_frame, terms_frame,
        add_frame, update_frame, delete_frame
    ]
    # Mostrar pantalla de carga
    current_frame = loading_frame
    show_frame(loading_frame)
    window.after(1500, lambda: show_frame(start_frame))
    window.mainloop()

if __name__ == "__main__":
    main()