""" pip install tk
    pip install pyodbc
    pip install tkcalendar
    pip install pillow
    pip install customtkinter
    pip install fpdf
"""
import tkinter as tk 
import pyodbc
from tkinter import messagebox, font, filedialog
from tkcalendar import Calendar
from datetime import date
from PIL import Image, ImageTk
from customtkinter import CTkImage, CTkComboBox, CTkButton, CTkEntry, set_appearance_mode, set_default_color_theme
import time
from datetime import datetime, timedelta
from fpdf import FPDF
window = None
id_card = None  
password = None
id_card_1 = None
password_1 = None
id_card_2 = None
password_2 = None
all_frames = []
sum_cost = 0
num_passengers = 0
total_cost_var = None
selected_departure = None
selected_return = None
passenger_class_user = None
billing_payment_method = None
payment_id_card_entry = None
payment_password_entry = None
expiration_date_button = None
update_user_frame = None

# ---------------------------------------------------CONEXION CON BASE DE DATOS------------------------------------------------------------------------------------------------

"""Configurando la Conexion con la Base de Datos"""
driver = '{ODBC Driver 17 for SQL Server}'
server = 'DESKTOP-T8BJL71'
database = 'pasa'
username = 'dba'
password= 'dba'

"""Creando Conexion con la Base de Datos"""
def make_connection():
    try:
        connection = pyodbc.connect(
            f"DRIVER={driver};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={username};"
            f"PWD={password};"
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

"""Funcion para Validar si un Usuario tiene el mismo Numero de Catnet"""
def validate_carnet(carnet:str)->bool:
    conexion=make_connection()
    cursor=conexion.cursor()
    cursor.execute(f"EXEC sp_valida_carnet '{carnet}'")
    valor=cursor.fetchone()
    if valor is None:
        return False
    else:
        return True

"""Crear llave"""
def obtain_pk(cursor,tabla:str)->str:
    cursor.execute(f"SELECT {tabla}_id FROM {tabla} ORDER BY {tabla}_id DESC")
    return cursor.fetchone()[0]+1
#obtener llave
def obtain_userid(cursor):
    cursor.execute(f"EXEC sp_obtener_llave '{id_card}'")
    return cursor.fetchone()[0]

"""Guardar Datos al Crear una Cuenta"""
def create_account():
    # Entrada de Datos
    global content_frame, name_entry, last_name_entry, age_entry, id_card_entry, password_entry
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
    if validate_carnet(id_card)==True:
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
    id_card_entry.delete(0, tk.END)
    # Conexion con la Base de Datos
    connection = make_connection()
    if not connection:
        return
    try:
        cursor = connection.cursor()
        cursor.execute(f"EXEC sp_crear_usuario {obtain_pk(cursor,'usuario')},'{name}', '{last_name}', {age}, '{id_card}', '{password}'")
        connection.commit()
        # Cambiar al start_frame si todo sale bien
        messagebox.showinfo("Exito", f"Usuario {id_card} creado con exito")
        show_frame(start_frame)
    except pyodbc.Error as e:
        messagebox.showerror("Error", f"Error al registrar la cuenta: {e}")
    finally:
        connection.close()

"""Extraer Datos para Verificar el Inicio de Sesion"""
def login():
    # Entrada de Datos
    global content_frame
    global id_card, id_card_1, password_1
    id_card_1 = login_id_card_entry.get().strip()
    id_card = id_card_1
    password_1 = login_password_entry.get().strip()
    # Verificar la correcta Entrada de Datos
    if not all([id_card_1]):
        messagebox.showerror("Error", "Debes ingresar tu Numero de Carnet")
        return
    if not id_card.isdigit():
        messagebox.showerror("Error", "El Numero de Carnet debe ser un numero natural")
        return
    if not len(id_card_1) == 7:
        messagebox.showerror("Error", "El Numero de Carnet debe tener 7 digitos")
        return
    if not all([password_1]):
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
        cursor.execute(f"EXEC sp_obtener_usuario '{id_card_1}', '{password_1}'")
        usuario = cursor.fetchone()
        # Cambiar al content_frame si todo sale bien
        if usuario:
            show_frame(content_frame)
        else:
            messagebox.showerror("Error", "Datos incorrectos. Verifique su usuario y contraseña")
    except pyodbc.Error as e:
        messagebox.showerror("Error", f"Error al realizar la consulta: {e}")
    finally:
        connection.close()

"""Extraer Datos para Buscar buses"""
def search_buses():
    global point_origin_input, point_destination_input, departure_date_button, return_date_button, passengers_entry, passenger_class_input
    global num_passengers
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
    num_passengers = int(passengers)
    # Conexión con la Base de Datos
    connection = make_connection()
    if not connection:
        return
    try:
        cursor = connection.cursor()
        # Consulta para Fecha de Partida
        cursor.execute(f"EXEC sp_obtener_datos_bus '{origin}', '{destination}', '{departure_date}', {int(passengers)}")
        buses = cursor.fetchall()
        # Consulta para Fecha de Regreso
        buses_2 = []
        if return_date != "Seleccionar":
            cursor.execute(f"EXEC sp_obtener_datos_bus '{destination}', '{origin}', '{return_date}', {int(passengers)}")
            buses_2 = cursor.fetchall()

        # Mostrar Resultados
        results_frame = make_show_results(buses, buses_2, passengers, origin, destination,passenger_class)
        show_frame(results_frame)
    except pyodbc.Error as e:
        messagebox.showerror("Error", f"Error al ejecutar la consulta: {e}")
    finally:
        connection.close()

# ------------------------------------------------------------FRAMES---------------------------------------------------------------------------------------------

"""Pantalla de Carga"""
def make_loading_screen():
    # Creando Frame
    loading_frame = tk.Frame(window, bg="#7732FF") 
    loading_frame.name = "loading" 
    loading_frame.pack(fill="both", expand=True)
    # Agregando Icono
    try:
        pasa_iso = "../../ASSETS/color_negative.png"
        image = Image.open(pasa_iso)
        image = image.resize((200, 200), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        iso_label = tk.Label(loading_frame, image=photo, bg="#7732FF")  
        iso_label.image = photo  
        iso_label.pack(expand=True)
    except Exception as e:
        print(f"Error al cargar el Logo: {e}")
    # Tiempo de Espera
    def delayed_show_start_frame():
        window.configure(bg="#F1F2F6")
        show_frame(start_frame)
    window.after(1500, delayed_show_start_frame)
    return loading_frame

"""Frame de la Barra de Accion"""
def make_action_bar():
    # Creación del frame de la barra de acción
    action_bar = tk.Frame(window, bg="#F1F2F6", width=380, height=40)
    action_bar.name = "action_bar"
    action_bar.pack(side="top", fill="x")
    # Agregar logo al centro
    try:
        pasa_logo = "../../ASSETS/logo.png"
        logo_image = Image.open(pasa_logo).resize((56, 20), Image.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_image)
        global logo_button
        logo_button = tk.Button(
            action_bar,
            image=logo_photo,
            bg="#F1F2F6",
            borderwidth=0,
            command=on_logo_button
        )
        logo_button.image = logo_photo
        logo_button.place(relx=0.430, rely=0.3, anchor="center") 
        logo_button.place_forget()
    except Exception as e:
        print(f"Error al cargar el Logo: {e}")
    # Crear Boton para Regresar pero inicialmente ocultarlo
    try:
        back_image_path = "../../ASSETS/back_button.png"
        back_image = Image.open(back_image_path).resize((12, 15), Image.LANCZOS)
        back_photo = ImageTk.PhotoImage(back_image)
        global back_button
        def on_back_button():
            global current_frame, update_user_frame, pay_frame, results_frame, history_frame, login_frame, register_frame, content_frame, start_frame, terms_frame, payment_confirmation_frame
            # Verificar desde qué frame se está presionando el Boton de Regreso
            if current_frame == results_frame:
                results_frame.pack_forget()
                hide_back_button()
                show_frame(content_frame)
            elif current_frame == history_frame:
                history_frame.pack_forget()
                hide_back_button()
                show_frame(content_frame)
            elif current_frame == login_frame:
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
            elif current_frame == pay_frame:
                pay_frame.pack_forget()
                hide_back_button()
                show_frame(results_frame)
            elif current_frame == payment_confirmation_frame:
                payment_confirmation_frame.pack_forget()
                hide_back_button()
                show_frame(pay_frame)
            elif current_frame == update_user_frame:
                update_user_frame.pack_forget()
                hide_back_button()
                show_frame(content_frame)
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
    # Crear Boton de Historial pero inicialmente ocultarlo
    try:
        history_image_path = "../../ASSETS/history_button.png"
        history_image = Image.open(history_image_path).resize((17, 21), Image.LANCZOS)
        history_photo = ImageTk.PhotoImage(history_image)
        global history_button
        history_button = tk.Button(
            action_bar,
            image=history_photo,
            bg="#F1F2F6",
            borderwidth=0,
            command=on_history_button
        )
        history_button.image = history_photo
        history_button.place(x=25, y=9) 
        history_button.place_forget()
    except Exception as e:
        print(f"Error al cargar el Boton de Historial: {e}")
    # Crear Boton de Pagar pero inicialmente ocultarlo
    try:
        pay_image_path = "../../ASSETS/pay_button.png"
        pay_image = Image.open(pay_image_path).resize((20, 19), Image.LANCZOS)
        pay_photo = ImageTk.PhotoImage(pay_image)
        global pay_button
        pay_button = tk.Button(
            action_bar,
            image=pay_photo,
            bg="#F1F2F6",
            borderwidth=0,
            command=on_pay_button
        )
        pay_button.image = pay_photo
        pay_button.place(x=340, y=12) 
        pay_button.place_forget()
    except Exception as e:
        print(f"Error al cargar el Boton de Pagar: {e}")
    # Boton para Cerrar Sesion
    try:
        log_out_image_path = "../../ASSETS/log_out_button.png"
        log_out_image = Image.open(log_out_image_path).resize((18, 18), Image.LANCZOS)
        log_out_photo = ImageTk.PhotoImage(log_out_image)
        global log_out_button
        def log_out_button():
            global current_frame, results_frame, content_frame
            # Verificar desde qué frame se está presionando el Boton de Cerrar Sesion
            if current_frame == content_frame:
                content_frame.pack_forget()
                hide_log_out_button()
                show_frame(start_frame)
            if content_frame == reservation_frame:
                reservation_frame.pack_forget()
                hide_log_out_button()
                show_frame(start_frame)
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

"""Frame Inicial"""
def make_start_frame():
    # Creacion del Frame
    start_frame = tk.Frame(window, bg="#F1F2F6")
    start_frame.name = "start"
    # Agregando Logo
    try:
        pasa_iso = "../../ASSETS/color_positive.png"
        image = Image.open(pasa_iso)
        image = image.resize((170, 170), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        iso_label = tk.Label(start_frame, image=photo, bg="#F1F2F6")  
        iso_label.image = photo  
        iso_label.pack(expand=True)
    except Exception as e:
        print(f"Error al cargar el Logo: {e}")
    # Texto
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
    # Boton de Inicio de Sesion
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
    # Boton de Creacion de Cuenta
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
    # Texto de Términos y Condiciones
    terms_label = tk.Label(
        start_frame,
        text="Al crear una cuenta, confirmo que he leído y acepto los ",
        font=("Arial", 10),
        bg="#F1F2F6",
        fg="black",
    )
    terms_label.pack(pady=(30, 5), side="top", anchor="center")
    # Crear enlace para "Términos y condiciones"
    terms_link = tk.Label(
        start_frame,
        text="Terminos y Condiciones de Uso",
        font=("Arial", 10, "underline"),
        bg="#F1F2F6",
        fg="#7732FF",
        cursor="hand2",
    )
    terms_link.pack(side="top", anchor="center")
    # Vincular el clic al enlace
    terms_link.bind("<Button-1>", lambda e: show_frame(terms_frame))
    return start_frame

"""Frame para ver los Terminos y Condiciones de Uso"""
def make_terms_frame():
    # Crear el frame principal de términos
    terms_frame = tk.Frame(window, bg="#F1F2F6")
    terms_frame.name = "terms"
    # Título principal 
    title_label = tk.Label(
        terms_frame,
        text="Términos y Condiciones de Uso",
        font=("Arial", 16, "bold"),
        bg="#F1F2F6",
        fg="black",
    )
    title_label.pack(side="top", pady=5)
    # Contenedor para el canvas y el scrollbar
    container = tk.Frame(terms_frame, bg="#F1F2F6")
    container.pack(side="top", fill="both", expand=True)
    # Crear el Scrollbar y el Canvas dentro del contenedor
    scrollbar = tk.Scrollbar(container)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    canvas = tk.Canvas(container, bg="#F1F2F6", yscrollcommand=scrollbar.set, bd=0, highlightthickness=0)
    canvas.pack(side=tk.LEFT, fill="both", expand=True)
    scrollbar.config(command=canvas.yview)
    # Agregar el frame de contenido dentro del canvas
    content_text_frame = tk.Frame(canvas, bg="#F1F2F6")
    canvas.create_window((0, 0), window=content_text_frame, anchor="nw")
    def resize_canvas(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    content_text_frame.bind("<Configure>", resize_canvas)
    # Secciones de contenido
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
    for title, content in sections:
        section_frame = tk.Frame(content_text_frame, bg="#F1F2F6")
        section_frame.pack(fill="x", padx=15, pady=5)
        # Título de la seccion
        section_title = tk.Label(
            section_frame,
            text=title,
            font=("Arial", 12, "bold"),
            bg="#F1F2F6",
            fg="black",
            anchor="w",
        )
        section_title.pack(fill="x")
        # Texto de la seccion
        content_text_label = tk.Label(
            section_frame,
            text=content,
            font=("Arial", 10),
            bg="#F1F2F6",
            fg="black",
            anchor="w",
            justify="left",
            wraplength=335,
        )
        content_text_label.pack(fill="x")
    show_back_button(terms_frame)
    return terms_frame

"""Frame para Crear una Cuenta"""
def make_register_frame():
    global name_entry, last_name_entry, age_entry, id_card_entry, password_entry
    # Creando el Frame
    register_frame = tk.Frame(window, bg="#F1F2F6")
    register_frame.name = "register"
    title_font = font.Font(family="Canva Sans", size=15, weight="bold")
    title_label = tk.Label(
        register_frame,
        text="Crear Cuenta",
        font=title_font,
        bg="#F1F2F6",
        fg="black",
        wraplength=350,
        justify="center",
    )
    title_label.pack(pady=50)
    # Ingresando el Nombre
    name_frame = tk.Frame(register_frame, bg="#F1F2F6")
    name_frame.pack(side="top", pady=10, fill="x", padx=10)
    name_label = tk.Label(name_frame, text="Nombre:", bg="#F1F2F6")
    name_label.pack(side="left", padx=10)
    name_entry = CTkEntry(
        name_frame,
        placeholder_text="Ingresar",
        border_color="#7732FF",
        corner_radius=32
    )
    name_entry.pack(side="left", padx=10, fill="x", expand=True)
    # Ingresando los Apellidos
    last_name_frame = tk.Frame(register_frame, bg="#F1F2F6")
    last_name_frame.pack(side="top", pady=10, fill="x", padx=10)
    last_name_label = tk.Label(last_name_frame, text="Apellidos:", bg="#F1F2F6")
    last_name_label.pack(side="left", padx=10)
    last_name_entry = CTkEntry(
        last_name_frame,
        placeholder_text="Ingresar",
        border_color="#7732FF",
        corner_radius=32
    )
    last_name_entry.pack(side="left", padx=10, fill="x", expand=True)
    # Ingresando la Edad
    age_frame = tk.Frame(register_frame, bg="#F1F2F6")
    age_frame.pack(side="top", pady=10, fill="x", padx=10)
    age_label = tk.Label(age_frame, text="Edad:", bg="#F1F2F6")
    age_label.pack(side="left", padx=10)
    age_entry = CTkEntry(
        age_frame,
        placeholder_text="Ingresar",
        border_color="#7732FF",
        corner_radius=32
    )
    age_entry.pack(side="left", padx=10, fill="x", expand=True)
    # Ingresando el Carnet
    id_card_frame = tk.Frame(register_frame, bg="#F1F2F6")
    id_card_frame.pack(side="top", pady=10, fill="x", padx=10)
    id_card_label = tk.Label(id_card_frame, text="Carnet:", bg="#F1F2F6")
    id_card_label.pack(side="left", padx=10)
    id_card_entry = CTkEntry(
        id_card_frame,
        placeholder_text="Ingresar",
        border_color="#7732FF",
        corner_radius=32
    )
    id_card_entry.pack(side="left", padx=10, fill="x", expand=True)
    # Ingresando la Contraseña
    password_frame = tk.Frame(register_frame, bg="#F1F2F6")
    password_frame.pack(side="top", pady=10, fill="x", padx=10)
    password_label = tk.Label(password_frame, text="Contraseña:", bg="#F1F2F6")
    password_label.pack(side="left", padx=10)
    password_entry = CTkEntry(
        password_frame,
        placeholder_text="Ingresar",
        show="*",
        border_color="#7732FF",
        corner_radius=32
    )
    password_entry.pack(side="left", padx=10, fill="x", expand=True)
    # Boton para Crear Cuenta
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
    # Botón de Regreso
    show_back_button()
    return register_frame

"""Frame para Iniciar Sesion"""
def make_login_frame():
    global login_id_card_entry, login_password_entry
    # Creando Frame
    login_frame = tk.Frame(window, bg="#F1F2F6")
    login_frame.name = "login"
    title_font = font.Font(family="Canva Sans", size=15, weight="bold")
    title_label = tk.Label(
        login_frame,
        text="Iniciar Sesion",
        font=title_font,
        bg="#F1F2F6",
        fg="black",
        wraplength=350,
        justify="center",
    )
    title_label.pack(pady=50)
    # Ingresando el Carnet
    login_id_card_frame = tk.Frame(login_frame, bg="#F1F2F6")
    login_id_card_frame.pack(side="top", pady=10, fill="x", padx=10)
    login_id_card_label = tk.Label(login_id_card_frame, text="Carnet:", bg="#F1F2F6")
    login_id_card_label.pack(side="left", padx=10)
    login_id_card_entry = CTkEntry(
        login_id_card_frame,
        placeholder_text="Ingresar",
        border_color="#7732FF",
        corner_radius=32
    )
    login_id_card_entry.pack(side="left", padx=10, fill="x", expand=True)
    # Ingresando la Contraseña
    login_password_frame = tk.Frame(login_frame, bg="#F1F2F6")
    login_password_frame.pack(side="top", pady=10, fill="x", padx=10)
    login_password_label = tk.Label(login_password_frame, text="Contraseña:", bg="#F1F2F6")
    login_password_label.pack(side="left", padx=10)
    login_password_entry = CTkEntry(
        login_password_frame,
        placeholder_text="Ingresar",
        show="*",
        border_color="#7732FF",
        corner_radius=32
    )
    login_password_entry.pack(side="left", padx=10, fill="x", expand=True)
    # Boton para Iniciar Sesion
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
    # Botón de Regreso
    show_back_button()
    return login_frame

"""Frame del Historial"""
def make_history_frame():
    global id_card
    global history_frame
    # Creando Frame
    history_frame = tk.Frame(window, bg="#F1F2F6")
    history_frame.name = "history"
    history_frame.pack(side="top", anchor="n", fill="x", expand=True)
    title_font = font.Font(family="Canva Sans", size=15, weight="bold")
    title_label = tk.Label(
        history_frame,
        text="Historial",
        font=title_font,
        bg="#F1F2F6",
        fg="black",
        wraplength=350,
        justify="center",
    )
    title_label.pack(side="top", anchor="center", pady=10)
    # Scrollbar
    results_container = tk.Frame(history_frame, bg="#F1F2F6")
    results_container.pack(fill="both", expand=True, padx=10, pady=10)
    scrollbar = tk.Scrollbar(results_container)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas = tk.Canvas(results_container, bg="#F1F2F6", yscrollcommand=scrollbar.set, bd=0, highlightthickness=0, height=500)
    canvas.pack(side=tk.LEFT, fill="both", expand=True)
    scrollbar.config(command=canvas.yview)
    # Creacion del Frame de texto de las Reservas
    inner_frame = tk.Frame(canvas, bg="#F1F2F6")
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")
    window_id = canvas.create_window((0, 0), window=inner_frame, anchor="nw")
    def onFrameConfigure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(window_id, width=canvas.winfo_width())
    inner_frame.bind("<Configure>", onFrameConfigure)
    # Conexion con la base de datos
    try:
        connection = make_connection()
        if connection:
            cursor = connection.cursor()
            # Ejecutar el SP
            cursor.execute("EXEC sp_mostrar_reservas_por_usuario ?", (id_card,))
            reservas = cursor.fetchall()
            if reservas:
                for reserva in reservas:
                    print(f"Reserva: {reserva}")  
                    texto_reserva = f"Reserva ID: {reserva[0]}\nLugar de Partida: {reserva[1]}\nLugar de Destino: {reserva[2]}\nFecha de Embarque: {reserva[3]}\nCosto Unitario: {reserva[4]}"
                    tk.Label(inner_frame, text=texto_reserva, bg="#F1F2F6", anchor="center", justify="center").pack(fill="x", pady=2)
            else:
                tk.Label(inner_frame, text="No se encontraron reservas", bg="#F1F2F6").pack(pady=10, side="top", anchor="center")
            connection.close()
        else:
            tk.Label(inner_frame, text="Error en la conexion a la base de datos", bg="#F1F2F6").pack(pady=10, side="top", anchor="center")
    except Exception as e:
        messagebox.showerror("Error", f"Error al obtener reservas: {e}")
    return history_frame

"""Frame de Pagar"""
def make_pay_frame():
    global sum_cost, total_cost_var, billing_payment_method
    pay_frame = tk.Frame(window, bg="#F1F2F6")
    pay_frame.name = "pay"
    # Titulo
    title_font = font.Font(family="Canva Sans", size=15, weight="bold")
    title_label = tk.Label(               
        pay_frame,
        text="Realiza el pago",
        font=title_font,
        bg="#F1F2F6",
        fg="black",
        wraplength=350,
        justify="center",
    )
    title_label.pack(pady=10)
    # Texto de Costo total
    terms_label = tk.Label(
        pay_frame,
        textvariable=total_cost_var,
        font=("Arial", 10),
        bg="#F1F2F6",
        fg="black",
    )
    terms_label.pack(pady=(30, 5), side="top", anchor="center")
    # Boton de Visa
    try:
        visa_button_frame = tk.Frame(pay_frame, bg="#F1F2F6")
        visa_button_frame.pack(side="top", pady=10, fill="x", padx=10)
        visa_button_label = tk.Label(visa_button_frame, text=" ", bg="#F1F2F6")
        visa_button_label.pack(side="left", padx=10)
        image_path = "../../ASSETS/visa_button.png"
        image = Image.open(image_path)
        image = image.resize((36, 13), Image.LANCZOS)  
        ctk_image = CTkImage(light_image=image, dark_image=image)
        visa_button = CTkButton(
            visa_button_frame,
            text="Visa",
            font=("Canva Sans", 12),
            fg_color="#F1F2F6",
            text_color="#000000",
            hover_color="#E1E1E1",
            border_color="#7732FF",
            border_width=2,
            corner_radius=32,
            image=ctk_image,  
            compound="left",
            command = lambda: on_button_click("Visa")
        )
        visa_button.image = ctk_image  
        visa_button.pack(side="left", padx=10, fill="x", expand=True)
    except Exception as e:
        print(f"Error al cargar la imagen de Visa: {e}")
    # Boton de Mastercard
    try:
        mastercard_button_frame = tk.Frame(pay_frame, bg="#F1F2F6")
        mastercard_button_frame.pack(side="top", pady=10, fill="x", padx=10)
        mastercard_button_label = tk.Label(mastercard_button_frame, text=" ", bg="#F1F2F6")
        mastercard_button_label.pack(side="left", padx=10)
        image_mastercard_path = "../../ASSETS/mastercard_button.png"
        image_mastercard = Image.open(image_mastercard_path)
        image_mastercard = image_mastercard.resize((36, 22), Image.LANCZOS)  
        ctk_image_mastercard = CTkImage(light_image=image_mastercard, dark_image=image_mastercard)
        mastercard_button = CTkButton(
            mastercard_button_frame,
            text="Mastercard",
            font=("Canva Sans", 12),
            fg_color="#F1F2F6",
            text_color="#000000",
            hover_color="#E1E1E1",
            border_color="#7732FF",
            border_width=2,
            corner_radius=32,
            image=ctk_image_mastercard,  
            compound="left",
            command = lambda: on_button_click("Mastercard")
        )
        mastercard_button.image = ctk_image_mastercard 
        mastercard_button.pack(side="left", padx=10, fill="x", expand=True)
    except Exception as e:
        print(f"Error al cargar la imagen de Mastercard: {e}")
    # Boton de PayPal
    try:
        paypal_button_frame = tk.Frame(pay_frame, bg="#F1F2F6")
        paypal_button_frame.pack(side="top", pady=10, fill="x", padx=10)
        paypal_button_label = tk.Label(paypal_button_frame, text=" ", bg="#F1F2F6")
        paypal_button_label.pack(side="left", padx=10)
        image_path_paypal = "../../ASSETS/paypal_button.png"
        image_paypal = Image.open(image_path_paypal)
        image_paypal = image_paypal.resize((36, 36), Image.LANCZOS)  
        ctk_image_paypal = CTkImage(light_image=image_paypal, dark_image=image_paypal)
        paypal_button = CTkButton(
            paypal_button_frame,
            text="PayPal",
            font=("Canva Sans", 12),
            fg_color="#F1F2F6",
            text_color="#000000",
            hover_color="#E1E1E1",
            border_color="#7732FF",
            border_width=2,
            corner_radius=32,
            image=ctk_image_paypal,  
            compound="left",
            command = lambda: on_button_click("PayPal")
        )
        paypal_button.image = ctk_image_paypal  
        paypal_button.pack(side="left", padx=10, fill="x", expand=True)
    except Exception as e:
        print(f"Error al cargar la imagen de PayPal: {e}")
    # Boton de Bitcoin
    try:
        bitcoin_button_frame = tk.Frame(pay_frame, bg="#F1F2F6")
        bitcoin_button_frame.pack(side="top", pady=10, fill="x", padx=10)
        bitcoin_button_label = tk.Label(bitcoin_button_frame, text=" ", bg="#F1F2F6")
        bitcoin_button_label.pack(side="left", padx=10)
        image_path_bitcoin = "../../ASSETS/bitcoin_button.png"
        image_bitcoin = Image.open(image_path_bitcoin)
        image_bitcoin = image_bitcoin.resize((36, 36), Image.LANCZOS)  
        ctk_image_bitcoin = CTkImage(light_image=image_bitcoin, dark_image=image_bitcoin)
        bitcoin_button = CTkButton(
            bitcoin_button_frame,
            text="Bitcoin",
            font=("Canva Sans", 12),
            fg_color="#F1F2F6",
            text_color="#000000",
            hover_color="#E1E1E1",
            border_color="#7732FF",
            border_width=2,
            corner_radius=32,
            image=ctk_image_bitcoin,  
            compound="left",
            command = lambda: on_button_click("Bitcoin")
        )
        bitcoin_button.image = ctk_image_bitcoin  
        bitcoin_button.pack(side="left", padx=10, fill="x", expand=True)
    except Exception as e:
        print(f"Error al cargar la imagen de Bitcoin: {e}")
    # Boton de Yolo
    try:
        yolo_button_frame = tk.Frame(pay_frame, bg="#F1F2F6")
        yolo_button_frame.pack(side="top", pady=10, fill="x", padx=10)
        yolo_button_label = tk.Label(yolo_button_frame, text=" ", bg="#F1F2F6")
        yolo_button_label.pack(side="left", padx=10)
        image_path_yolo = "../../ASSETS/yolo_button.png"
        image_yolo = Image.open(image_path_yolo)
        image_yolo = image_yolo.resize((36, 30), Image.LANCZOS)  
        ctk_image_yolo = CTkImage(light_image=image_yolo, dark_image=image_yolo)
        yolo_button = CTkButton(
            yolo_button_frame,
            text="Yolo",
            font=("Canva Sans", 12),
            fg_color="#F1F2F6",
            text_color="#000000",
            hover_color="#E1E1E1",
            border_color="#7732FF",
            border_width=2,
            corner_radius=32,
            image=ctk_image_yolo,  
            compound="left",
            command = lambda: on_button_click("Yolo")
        )
        yolo_button.image = ctk_image_yolo 
        yolo_button.pack(side="left", padx=10, fill="x", expand=True)
    except Exception as e:
        print(f"Error al cargar la imagen de Yolo: {e}")
    return pay_frame

"""Frame de Confirmacion de la Reserva"""
def make_reservation_confirmed():
    global num_passengers, passenger_class_user, billing_payment_method
    reservation_frame = tk.Frame(window, bg="#F1F2F6")
    reservation_frame.name = "reservation"
    # Agregando Logo
    try:
        pasa_iso = "../../ASSETS/color_positive.png"
        image = Image.open(pasa_iso)
        image = image.resize((170, 170), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        iso_label = tk.Label(reservation_frame, image=photo, bg="#F1F2F6")  
        iso_label.image = photo  
        iso_label.pack(expand=True)
    except Exception as e:
        print(f"Error al cargar el Logo: {e}")
    # Titulo
    title_font = font.Font(family="Canva Sans", size=15, weight="bold")
    title_label = tk.Label(               
        reservation_frame,
        text="¡Reserva Confirmada!",
        font=title_font,
        bg="#F1F2F6",
        fg="black",
        wraplength=350,
        justify="center",
    )
    title_label.pack(pady=10)
    # Factura
    conexion =make_connection()
    cursor=conexion.cursor()
    cursor.execute(f"EXEC sp_obtener_usuario_nombreapellido '{id_card}'")
    print(id_card)
    resultado=cursor.fetchone()
    if resultado is not None:
        name = resultado[0] + " " + resultado[1]
        today = date.today()
        if selected_return != None and selected_departure!=None:
            label_text = f"Lugar y Fecha: Bolivia, {today}\nNombre: {name}\nNIT: {id_card}\nIDs de los Buses: {selected_departure}, {selected_return}\nBoletos Comprados: {num_passengers}\nClase: {passenger_class_user}\nMetodo de Pago: {billing_payment_method}\nTotal: Bs{sum_cost}"
        elif selected_return!=None and selected_departure==None:
            label_text = f"Lugar y Fecha: Bolivia, {today}\nNombre: {name}\nNIT: {id_card}\nID del Bus: {selected_return}\nBoletos Comprados: {num_passengers}\nClase: {passenger_class_user}\nMetodo de Pago: {billing_payment_method}\nTotal: Bs{sum_cost}"
        elif selected_return==None and selected_departure!=None:
            label_text = f"Lugar y Fecha: Bolivia, {today}\nNombre: {name}\nNIT: {id_card}\nID del Bus: {selected_departure}\nBoletos Comprados: {num_passengers}\nClase: {passenger_class_user}\nMetodo de Pago: {billing_payment_method}\nTotal: Bs{sum_cost}"
        else:
            label_text="No se encontraron los buses para emitir la factura"
    else:
        label_text = "No se encontro informacion del usuario"
    factura_text_label = tk.Label(
        reservation_frame,
        text=f"{label_text}",
        font=("Arial", 10),
        bg="#F1F2F6",
        fg="black"
    )
    factura_text_label.pack(pady=10, side="top", anchor="center")
    # Factura Decarga
    download_button = CTkButton(
        reservation_frame,
        text="Descargar Factura",
        corner_radius=32,
        fg_color="#7732FF",
        text_color="white",
        hover_color="#5A23CC",
        command=lambda: descargar_factura(
            today,
            name,
            id_card,
            selected_departure,
            selected_return,
            num_passengers,
            passenger_class_user,
            billing_payment_method,
            sum_cost
        )
    )
    download_button.pack(pady=10)
    # Boton de Volver a Casa
    return_home_button = CTkButton(
        reservation_frame,
        text="Volver a Casa",
        corner_radius=32,
        fg_color="#7732FF",
        text_color="white",
        hover_color="#5A23CC",
        command=on_return_home_button,
    )
    return_home_button.pack(pady=10)
    return reservation_frame

"""Frame de Area de contenido"""
def make_content_frame():
    global content_frame, point_origin_input, point_destination_input, departure_date_button, return_date_button, passengers_entry, passenger_class_input
    # Creando Frame
    content_frame = tk.Frame(window, bg="#F1F2F6")
    content_frame.name = "content"
    # Publicidad
    try:
        advertising_image = Image.open("../../ASSETS/advertising.png")
        advertising_image = advertising_image.resize((380, 150), Image.LANCZOS) 
        advertising_photo = ImageTk.PhotoImage(advertising_image)
        advertising_label = tk.Label(content_frame, image=advertising_photo, bg="#F1F2F6")
        advertising_label.image = advertising_photo
        advertising_label.pack(pady=20)
    except Exception as e:
        print("Error al cargar la imagen de la publicidad", e)
    # Titulo
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
    title_label.pack(pady=10)
    combo_fg_color = "#F1F2F6"
    combo_button_color = "#7732FF"
    combo_border_color = "#7732FF"
    # Boton de Cerrar Sesion
    show_log_out_button(content_frame)
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
        command=search_buses
    )
    buses_available.pack(pady=2)
    return content_frame

"""Frame de los Resultados de la busqueda"""
def make_show_results(buses, buses_2, passengers, origin, destination, passenger_class):
    global results_frame, return_date, sum_cost, total_cost_var, num_passengers, passenger_class_user 
    return_date = return_date_button.cget("text")
    selected_departure = None
    selected_return = None
    passenger_class_user  = passenger_class
    # Creación del Frame principal
    results_frame = tk.Frame(window, bg="#F1F2F6")
    results_frame.name = "results"
    results_frame.pack(fill="both", expand=True, padx=0, pady=10)
    show_back_button(results_frame)
    show_log_out_button(results_frame)
    # Scrollbar
    scrollbar = tk.Scrollbar(results_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas = tk.Canvas(results_frame, bg="#F1F2F6", yscrollcommand=scrollbar.set, bd=0, highlightthickness=0)
    canvas.pack(side=tk.LEFT, fill="both", expand=True)
    scrollbar.config(command=canvas.yview)
    content_frame = tk.Frame(canvas, bg="#F1F2F6")
    canvas.create_window((40, 0), window=content_frame, anchor="nw")
    def resize_canvas(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    content_frame.bind("<Configure>", resize_canvas)
    # Función de control de selección de buses diferenciada por dirección:
    def handle_bus_selection(bus_id, button, bus_cost, direction):
        global selected_departure, selected_return, sum_cost, num_passengers
        if direction == "departure":
            if selected_departure is None:
                selected_departure = bus_id
                button.configure(text="Seleccionado", fg_color="gray", hover_color="gray")
                sum_cost =sum_cost + (num_passengers * bus_cost)
            elif selected_departure == bus_id:
                selected_departure = None
                button.configure(text="Seleccionar", fg_color="#7732FF", hover_color="#5A23CC")
                sum_cost = sum_cost - (num_passengers * bus_cost)
            else:
                messagebox.showinfo("Información", "Solo puedes seleccionar un Bus de Partida")
        elif direction == "return":
            if selected_return is None:
                selected_return = bus_id
                button.configure(text="Seleccionado", fg_color="gray", hover_color="gray")
                sum_cost =sum_cost + (num_passengers * bus_cost)
            elif selected_return == bus_id:
                selected_return = None
                button.configure(text="Seleccionar", fg_color="#7732FF", hover_color="#5A23CC")
                sum_cost = sum_cost - (num_passengers * bus_cost)
            else:
                messagebox.showinfo("Informacion", "Solo puedes seleccionar un Bus de regreso")
        total_cost_var.set(f"El costo total a pagar es: Bs{globals()['sum_cost']}")
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
        no_results_label.pack(expand=True)
    else:
        title_font = font.Font(family="Canva Sans", size=15, weight="bold")
        title_label = tk.Label(
            content_frame,
            text="Selecciona un Bus \npara la Fecha de Partida",
            font=title_font,
            bg="#F1F2F6",
            fg="black",
            wraplength=350,
        )
        title_label.pack(side="top", anchor="center", pady=10)
        for idx, bus in enumerate(buses):
            precio = get_price_per_bus(origin, destination, passenger_class)
            bus_id, fecha_salida, asientos_ocupados = bus
            block_frame = tk.Frame(content_frame, bg="#F1F2F6", padx=10, pady=10)
            block_frame.pack(pady=(10, 0), fill="x")
            detalles = f"""
Bus ID: {bus_id}
Punto de Origen: {origin}
Punto de Destino: {destination}
Fecha de Salida: {fecha_salida}
Asientos Disponibles: {60 - asientos_ocupados}
Precio: Bs{precio}
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
                command=lambda bid=bus_id, btn=None, cost=precio: None
            )
            select_button.pack(pady=(10, 0))
            select_button.configure(command=lambda bid=bus_id, btn=select_button, cost=precio: handle_bus_selection(bid, btn, cost, "departure"))
            if idx < len(buses) - 1:
                separator = tk.Frame(content_frame, bg="#7732FF", height=2, width=300)
                separator.pack(pady=(10, 10))
                separator.pack_propagate(False)

    # Mostrar Buses Disponibles de Regreso 
    if not buses_2 and return_date != "Seleccionar":
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
        title_label_2.pack(pady=10)
        for idx, bus in enumerate(buses_2):
            precio_2 = get_price_per_bus(destination, origin, passenger_class)
            bus_id, fecha_salida, asientos_ocupados = bus
            block_frame = tk.Frame(content_frame, bg="#F1F2F6", padx=10, pady=10)
            block_frame.pack(pady=(10, 0), fill="x")
            detalles = f"""
Bus ID: {bus_id}
Punto de Origen: {destination}
Punto de Destino: {origin}
Fecha de Salida: {fecha_salida}
Asientos Disponibles: {60 - asientos_ocupados}
Precio: Bs{precio_2}
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
                command=lambda bid=bus_id, btn=None, cost=precio_2: None
            )
            select_button.pack(pady=(10, 0))
            select_button.configure(command=lambda bid=bus_id, btn=select_button, cost=precio_2: handle_bus_selection(bid, btn, cost, "return"))
            if idx < len(buses_2) - 1:
                separator = tk.Frame(content_frame, bg="#7732FF", height=2, width=300)
                separator.pack(pady=(10, 10))
                separator.pack_propagate(False)
    return results_frame

"""Frame de confirmacion de Pago"""
def make_payment_confirmation_frame():
    global payment_id_card_entry, payment_password_entry, billing_payment_method, expiration_date_button
    # Creando Frame
    payment_confirmation_frame = tk.Frame(window, bg="#F1F2F6")
    payment_confirmation_frame.name = "payment_confirmation"
    if billing_payment_method == "Visa":
        # Agregando Logo de Visa
        try:
            payment_logo = f"../../ASSETS/visa_button.png"
            image = Image.open(payment_logo)
            image = image.resize((130, 48), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            iso_label = tk.Label(payment_confirmation_frame, image=photo, bg="#F1F2F6")  
            iso_label.image = photo  
            iso_label.pack(expand=True)
        except Exception as e:
            print(f"Error al cargar el Logo de Visa: {e}")
    elif billing_payment_method == "Mastercard":
        # Agregando Logo de Mastercard
        try:
            payment_logo = f"../../ASSETS/mastercard_button.png"
            image = Image.open(payment_logo)
            image = image.resize((150, 92), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            iso_label = tk.Label(payment_confirmation_frame, image=photo, bg="#F1F2F6")  
            iso_label.image = photo  
            iso_label.pack(expand=True)
        except Exception as e:
            print(f"Error al cargar el Logo de Mastercard: {e}")
    elif billing_payment_method == "PayPal":
        # Agregando Logo de PayPal
        try:
            payment_logo = f"../../ASSETS/paypal_logo.png"
            image = Image.open(payment_logo)
            image = image.resize((204, 54), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            iso_label = tk.Label(payment_confirmation_frame, image=photo, bg="#F1F2F6")  
            iso_label.image = photo  
            iso_label.pack(expand=True)
        except Exception as e:
            print(f"Error al cargar el Logo de PayPal: {e}")
    elif billing_payment_method == "Bitcoin":
        # Agregando Logo de Bitcoin
        try:
            payment_logo = f"../../ASSETS/bitcoin_button.png"
            image = Image.open(payment_logo)
            image = image.resize((120, 120), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            iso_label = tk.Label(payment_confirmation_frame, image=photo, bg="#F1F2F6")  
            iso_label.image = photo  
            iso_label.pack(expand=True)
        except Exception as e:
            print(f"Error al cargar el Logo de Bitcoin: {e}")
    elif billing_payment_method == "Yolo":
        # Agregando Logo de Yolo
        try:
            payment_logo = f"../../ASSETS/yolo_logo.png"
            image = Image.open(payment_logo)
            image = image.resize((204, 101), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            iso_label = tk.Label(payment_confirmation_frame, image=photo, bg="#F1F2F6")  
            iso_label.image = photo  
            iso_label.pack(expand=True)
        except Exception as e:
            print(f"Error al cargar el Logo de Yolo: {e}")
    # Titulo
    title_font = font.Font(family="Canva Sans", size=15, weight="bold")
    title_label = tk.Label(
        payment_confirmation_frame,
        text=f"Pagar con {billing_payment_method}",
        font=title_font,
        bg="#F1F2F6",
        fg="black",
        wraplength=350,
        justify="center",
    )
    title_label.pack(pady=50)
    # Ingreso de datos
    if billing_payment_method == "Visa" or billing_payment_method == "Mastercard":
        # Ingresando el Carnet
        payment_confirmation_id_card_frame = tk.Frame(payment_confirmation_frame, bg="#F1F2F6")
        payment_confirmation_id_card_frame.pack(side="top", pady=10, fill="x", padx=10)
        payment_confirmation_id_card_label = tk.Label(payment_confirmation_id_card_frame, text="N° de Tarjeta: ", bg="#F1F2F6")
        payment_confirmation_id_card_label.pack(side="left", padx=10)
        payment_id_card_entry = CTkEntry(
            payment_confirmation_id_card_frame,
            placeholder_text="Ingresar",
            border_color="#7732FF",
            corner_radius=32
        )
        payment_id_card_entry.pack(side="left", padx=10, fill="x", expand=True)
        # Ingresando la Contraseña
        payment_confirmation_password_frame = tk.Frame(payment_confirmation_frame, bg="#F1F2F6")
        payment_confirmation_password_frame.pack(side="top", pady=10, fill="x", padx=10)
        payment_confirmation_password_label = tk.Label(payment_confirmation_password_frame, text="CVC:", bg="#F1F2F6")
        payment_confirmation_password_label.pack(side="left", padx=10)
        payment_password_entry = CTkEntry(
            payment_confirmation_password_frame,
            placeholder_text="Ingresar",
            show="*",
            border_color="#7732FF",
            corner_radius=32
        )
        payment_password_entry.pack(side="left", padx=10, fill="x", expand=True)
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
        # Fecha de Expiracion
        expiration_date_frame = tk.Frame(payment_confirmation_frame, bg="#F1F2F6")
        expiration_date_frame.pack(side="top", pady=10, fill="x", padx=10)
        expiration_date_label = tk.Label(expiration_date_frame, text="Fecha de Expiracion:", bg="#F1F2F6")
        expiration_date_label.pack(side="left", padx=10)
        expiration_date_button = CTkButton(
            expiration_date_frame,
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
                lambda d: expiration_date_button.configure(text=d)
            )
        )
        expiration_date_button.pack(side="left", padx=10, fill="x", expand=True)
    elif billing_payment_method == "PayPal" or billing_payment_method == "Yolo":
        # Ingresando el Carnet
        payment_confirmation_id_card_frame = tk.Frame(payment_confirmation_frame, bg="#F1F2F6")
        payment_confirmation_id_card_frame.pack(side="top", pady=10, fill="x", padx=10)
        payment_confirmation_id_card_label = tk.Label(payment_confirmation_id_card_frame, text="Carnet: ", bg="#F1F2F6")
        payment_confirmation_id_card_label.pack(side="left", padx=10)
        payment_id_card_entry = CTkEntry(
            payment_confirmation_id_card_frame,
            placeholder_text="Ingresar",
            border_color="#7732FF",
            corner_radius=32
        )
        payment_id_card_entry.pack(side="left", padx=10, fill="x", expand=True)
        # Ingresando la Contraseña
        payment_confirmation_password_frame = tk.Frame(payment_confirmation_frame, bg="#F1F2F6")
        payment_confirmation_password_frame.pack(side="top", pady=10, fill="x", padx=10)
        payment_confirmation_password_label = tk.Label(payment_confirmation_password_frame, text="Contraseña:", bg="#F1F2F6")
        payment_confirmation_password_label.pack(side="left", padx=10)
        payment_password_entry = CTkEntry(
            payment_confirmation_password_frame,
            placeholder_text="Ingresar",
            show="*",
            border_color="#7732FF",
            corner_radius=32
        )
        payment_password_entry.pack(side="left", padx=10, fill="x", expand=True)
    elif billing_payment_method == "Bitcoin":
        # Direccion de la billetera
        address_label = tk.Label(
            payment_confirmation_frame,
            text=f"Direccion:\n 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
            font=("Arial", 10),
            bg="#F1F2F6",
            fg="black",
            justify="center",
        )
        address_label.pack(pady=(10, 5), side="top", anchor="center")
        # Ingresando el Carnet
        payment_confirmation_id_card_frame = tk.Frame(payment_confirmation_frame, bg="#F1F2F6")
        payment_confirmation_id_card_frame.pack(side="top", pady=10, fill="x", padx=10)
        payment_confirmation_id_card_label = tk.Label(payment_confirmation_id_card_frame, text="Carnet: ", bg="#F1F2F6")
        payment_confirmation_id_card_label.pack(side="left", padx=10)
        payment_id_card_entry = CTkEntry(
            payment_confirmation_id_card_frame,
            placeholder_text="Ingresar",
            border_color="#7732FF",
            corner_radius=32
        )
        payment_id_card_entry.pack(side="left", padx=10, fill="x", expand=True)
        # Ingresando la Contraseña
        payment_confirmation_password_frame = tk.Frame(payment_confirmation_frame, bg="#F1F2F6")
        payment_confirmation_password_frame.pack(side="top", pady=10, fill="x", padx=10)
        payment_confirmation_password_label = tk.Label(payment_confirmation_password_frame, text="Contraseña:", bg="#F1F2F6")
        payment_confirmation_password_label.pack(side="left", padx=10)
        payment_password_entry = CTkEntry(
            payment_confirmation_password_frame,
            placeholder_text="Ingresar",
            show="*",
            border_color="#7732FF",
            corner_radius=32
        )
        payment_password_entry.pack(side="left", padx=10, fill="x", expand=True)
    # Boton para Confirmar Pago
    payment_confirmation_button_submit = CTkButton(
        payment_confirmation_frame,
        text="Confirmar Pago",
        corner_radius=32,
        fg_color="#7732FF",
        text_color="white",
        hover_color="#5A23CC",
        command=payment_confirmation
    )
    payment_confirmation_button_submit.pack(pady=10)
    # Botón de Regreso
    show_back_button()
    return payment_confirmation_frame

"""Confirmacion de Pago"""
def payment_confirmation():
    # Entrada de Datos
    global reservation_frame, payment_id_card_entry, payment_password_entry, id_card_2, password_2, id_card, password, billing_payment_method, id_card_1, password_1, expiration_date_button
    id_card_2 = payment_id_card_entry.get()
    password_2 = payment_password_entry.get()
    if billing_payment_method == "Visa" or billing_payment_method == "Mastercard":
        expiration_date = expiration_date_button.cget("text")
        # Verificar la correcta Entrada de Datos
        if not all([id_card_2]):
            messagebox.showerror("Error", "Debes ingresar tu Numero de Carnet")
            return
        if not id_card_2.isdigit():
            messagebox.showerror("Error", "El Numero de Carnet debe ser un numero natural")
            return
        if not len(id_card_2) == 7:
            messagebox.showerror("Error", "El Numero de la Tarjeta debe tener 7 digitos")
            return
        if not all([password_2]):
            messagebox.showerror("Error", "Debes ingresar tu Contraseña")
            return
        if expiration_date == "Seleccionar":
            messagebox.showerror("Error", "Debes seleccionar la Fecha de Expiracion de tu tarjeta")
            return
        if id_card_2 != id_card_1 or password_2 != password_1:
            messagebox.showerror("Error", f"Pago rechazado por {billing_payment_method}. Verifique la información de su tarjeta")
            payment_id_card_entry.delete(0, tk.END)
            payment_password_entry.delete(0, tk.END)
            expiration_date_button.configure(text="Seleccionar")
            return
    elif billing_payment_method == "PayPal" or billing_payment_method == "Yolo" or billing_payment_method == "Bitcoin":
        # Verificar la correcta Entrada de Datos
        if not all([id_card_2]):
            messagebox.showerror("Error", "Debes ingresar tu Numero de Carnet")
            return
        if not id_card_2.isdigit():
            messagebox.showerror("Error", "El Numero de Carnet debe ser un numero natural")
            return
        if not len(id_card_2) == 7:
            messagebox.showerror("Error", "El Numero de Carnet debe tener 7 digitos")
            return
        if not all([password_2]):
            messagebox.showerror("Error", "Debes ingresar tu Contraseña")
            return
        if id_card_2 != id_card_1 or password_2 != password_1:
            if billing_payment_method == "Bitcoin":
                messagebox.showerror("Error", f"Pago rechazado por Sparrow Wallet. Verifique la información ingresada")
                payment_id_card_entry.delete(0, tk.END)
                payment_password_entry.delete(0, tk.END)
                return
            else:
                messagebox.showerror("Error", f"Pago rechazado por {billing_payment_method}. Verifique la información ingresada")
                payment_id_card_entry.delete(0, tk.END)
                payment_password_entry.delete(0, tk.END)
                return
    payment_id_card_entry.delete(0, tk.END)
    payment_password_entry.delete(0, tk.END)
    if billing_payment_method == "Visa" or billing_payment_method == "Mastercard":
        expiration_date_button.configure(text="Seleccionar")
    # Cambiar a reservation_frame si todo sale bien
    on_payment_method_button(billing_payment_method)
    return

def make_update_user_frame ():
    global id_card, p_password_entry, u_name_entry, u_last_name_entry, u_age_entry, u_id_card_entry, u_password_entry
    global update_user_frame
    # Creando el Frame
    update_user_frame = tk.Frame(window, bg="#F1F2F6")
    update_user_frame.name = "update_user"
    title_font = font.Font(family="Canva Sans", size=15, weight="bold")
    title_label = tk.Label(
        update_user_frame,
        text="Actualizar Cuenta",
        font=title_font,
        bg="#F1F2F6",
        fg="black",
        wraplength=350,
        justify="center",
    )
    title_label.pack(pady=50)
    # Conexion con la Base de Datos
    connection = make_connection()
    if not connection:
        return
    try:
        cursor = connection.cursor()
        cursor.execute(f"EXEC sp_obtiene_nombre_por_carnet_usuario '{id_card}'") 
        name = cursor.fetchone()[0]
        cursor.execute(f"EXEC sp_obtiene_apellido_por_carnet_usuario '{id_card}'") 
        lastname = cursor.fetchone()[0]
        cursor.execute(f"EXEC sp_obtiene_edad_por_carnet_usuario '{id_card}'") 
        age = cursor.fetchone()[0]
        connection.commit()
    except pyodbc.Error as e:
        messagebox.showerror("Error", f"Error al obtener datos de la cuenta: {e}")
    finally:
        connection.close()
    # Ingresando el Nombre
    name_frame = tk.Frame(update_user_frame, bg="#F1F2F6")
    name_frame.pack(side="top", pady=10, fill="x", padx=10)
    name_label = tk.Label(name_frame, text="Nombre:", bg="#F1F2F6")
    name_label.pack(side="left", padx=10)
    u_name_entry = CTkEntry(
        name_frame,
        placeholder_text="Ingresar",
        border_color="#7732FF",
        corner_radius=32
    )
    u_name_entry.pack(side="left", padx=10, fill="x", expand=True)
    u_name_entry.delete(0, tk.END)
    u_name_entry.insert(0, name)
    # Ingresando los Apellidos
    last_name_frame = tk.Frame(update_user_frame, bg="#F1F2F6")
    last_name_frame.pack(side="top", pady=10, fill="x", padx=10)
    last_name_label = tk.Label(last_name_frame, text="Apellidos:", bg="#F1F2F6")
    last_name_label.pack(side="left", padx=10)
    u_last_name_entry = CTkEntry(
        last_name_frame,
        placeholder_text="Ingresar",
        border_color="#7732FF",
        corner_radius=32
    )
    u_last_name_entry.pack(side="left", padx=10, fill="x", expand=True)
    u_last_name_entry.delete(0, tk.END)
    u_last_name_entry.insert(0, lastname)
    # Ingresando la Edad
    age_frame = tk.Frame(update_user_frame, bg="#F1F2F6")
    age_frame.pack(side="top", pady=10, fill="x", padx=10)
    age_label = tk.Label(age_frame, text="Edad:", bg="#F1F2F6")
    age_label.pack(side="left", padx=10)
    u_age_entry = CTkEntry(
        age_frame,
        placeholder_text="Ingresar",
        border_color="#7732FF",
        corner_radius=32
    )
    u_age_entry.pack(side="left", padx=10, fill="x", expand=True)
    u_age_entry.delete(0, tk.END)
    u_age_entry.insert(0, age)  
    # Ingresando el Carnet
    id_card_frame = tk.Frame(update_user_frame, bg="#F1F2F6")
    id_card_frame.pack(side="top", pady=10, fill="x", padx=10)
    id_card_label = tk.Label(id_card_frame, text="Carnet:", bg="#F1F2F6")
    id_card_label.pack(side="left", padx=10)
    u_id_card_entry = CTkEntry(
        id_card_frame,
        placeholder_text="Ingresar",
        border_color="#7732FF",
        corner_radius=32
    )
    u_id_card_entry.pack(side="left", padx=10, fill="x", expand=True)
    u_id_card_entry.delete(0, tk.END)
    u_id_card_entry.insert(0, id_card)
    # Ingresando la Nueva Contraseña
    password_frame = tk.Frame(update_user_frame, bg="#F1F2F6")
    password_frame.pack(side="top", pady=10, fill="x", padx=10)
    password_label = tk.Label(password_frame, text="Nueva Contraseña:", bg="#F1F2F6")
    password_label.pack(side="left", padx=10)
    u_password_entry = CTkEntry(
        password_frame,
        placeholder_text="Ingresar",
        show="*",
        border_color="#7732FF",
        corner_radius=32
    )
    u_password_entry.pack(side="left", padx=10, fill="x", expand=True)
    # Ingresando la Antigua Contraseña
    p_password_frame = tk.Frame(update_user_frame, bg="#F1F2F6")
    p_password_frame.pack(side="top", pady=10, fill="x", padx=10)
    p_password_label = tk.Label(p_password_frame, text="Contraseña Acual:", bg="#F1F2F6")
    p_password_label.pack(side="left", padx=10)
    p_password_entry = CTkEntry(
        p_password_frame,
        placeholder_text="Ingresar",
        show="*",
        border_color="#7732FF",
        corner_radius=32
    )
    p_password_entry.pack(side="left", padx=10, fill="x", expand=True)
    # Boton para Actualizar Cuenta
    update_account_button = CTkButton(
        update_user_frame,
        text="Actualizar cuenta",
        corner_radius=32,
        fg_color="#7732FF",
        text_color="white",
        hover_color="#5A23CC",
        command=update_account
    )
    update_account_button.pack(pady=10) 
    # Botón de Regreso
    show_back_button()
    return update_user_frame

def descargar_factura(fecha, nombre, nit, salida, regreso, boletos, clase, metodo_pago, total):
    # Construir el contenido de la factura con los parámetros
    if salida and regreso:
        ids = f"{salida}, {regreso}"
    elif salida:
        ids = salida
    elif regreso:
        ids = regreso
    else:
        ids = "N/A"

    factura_contenido = (
        f"Lugar y Fecha: Bolivia, {fecha}\n"
        f"Nombre: {nombre}\n"
        f"NIT: {nit}\n"
        f"IDs de los Buses: {ids}\n"
        f"Boletos Comprados: {boletos}\n"
        f"Clase: {clase}\n"
        f"Método de Pago: {metodo_pago}\n"
        f"Total: Bs{total}"
    )

    # Diálogo para guardar el archivo
    ruta_guardado = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("Archivos PDF", "*.pdf")],
        title="Guardar factura como"
    )

    if ruta_guardado:
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, factura_contenido)
            pdf.output(ruta_guardado)
            messagebox.showinfo("Éxito", "La factura se ha descargado exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el PDF: {e}")

def update_account():
    # Entrada de Datos
    global content_frame, u_name_entry, u_last_name_entry, u_age_entry, u_id_card_entry, u_password_entry, p_password_entry
    u_name = u_name_entry.get().strip()
    u_last_name = u_last_name_entry.get().strip()
    u_age = u_age_entry.get().strip()
    u_id_card = u_id_card_entry.get().strip()
    u_password = u_password_entry.get().strip()
    p_password = p_password_entry.get().strip()
    # Conexion con la Base de Datos para encontrar la contraseña
    connection = make_connection()
    if not connection:
        return
    try:
        cursor = connection.cursor()
        cursor.execute(f"EXEC sp_obtiene_contrasena_por_carnet_usuario '{id_card}'") 
        password_actual = cursor.fetchone()[0]
        cursor.execute(f"EXEC sp_obtener_admin_o_usuario_por_carnet '{id_card}'") 
        admin = cursor.fetchone()[0]
        connection.commit()
    except pyodbc.Error as e:
        messagebox.showerror("Error", f"Error al obtener la contraseña actual de la cuenta: {e}")
    finally:
        connection.close()
    # Manejo de Errores
    if not all([u_name]):
        messagebox.showerror("Error", "Debes ingresar tu Nombre")
        return
    if not all([u_last_name]):
        messagebox.showerror("Error", "Debes ingresar tus Apellidos")
        return
    if not all([u_age]):
        messagebox.showerror("Error", "Debes ingresar tu Edad")
        return
    if not u_age.isdigit():
        messagebox.showerror("Error", "Tu Edad debe ser un numero natural")
        return
    if not int(u_age) >= 18:
        messagebox.showerror("Error", "No puedes Actualizar una Cuenta si eres menor de edad")
        return
    if not all([u_id_card]):
        messagebox.showerror("Error", "Debes ingresar tu Numero de Carnet")
        return
    if not u_id_card.isdigit():
        messagebox.showerror("Error", "El Numero de Carnet debe ser un numero natural")
        return
    if not len(u_id_card) == 7:
        messagebox.showerror("Error", "El Numero de Carnet debe tener 7 digitos")
        return
    if u_id_card != id_card and validate_carnet(u_id_card)==True:
        messagebox.showerror("Error", "Carnet ya existente")
        return
    if not all([u_password]):
        u_password = password_actual
    if not all([p_password]):
        messagebox.showerror("Error", "Debes ingresar la Contraseña Actual para confirmar los cambios")
        return
    # Borrar Datos en caso de Error
    u_name_entry.delete(0, tk.END)
    u_last_name_entry.delete(0, tk.END)
    u_age_entry.delete(0, tk.END)
    u_id_card_entry.delete(0, tk.END)
    u_password_entry.delete(0, tk.END)
    u_id_card_entry.delete(0, tk.END)
    p_password_entry.delete(0, tk.END)
    # Conexion con la Base de Datos
    connection = make_connection()
    if not connection:
        return
    try:
        cursor = connection.cursor()
        cursor.execute(f"EXEC sp_obtener_id_por_carnet_usuario '{id_card}'") 
        id = cursor.fetchone()[0]
        print(f"Carnet: {id_card}")
        print(f"ID: {id}")
        print(f"Nuevo Carnet: {u_id_card}")
        cursor.execute(f"EXEC sp_update_usuario '{id}' , '{u_name}' , '{u_last_name}' , '{u_age}' , '{u_id_card}' , '{u_password}' , '{admin}'")
        connection.commit()
        # Cambiar al start_frame si todo sale bien
        messagebox.showinfo("Exito", f"El usuario con el carnet: {u_id_card} se ha actualizado con exito")
        update_user_frame.pack_forget()  
        show_frame(start_frame)
    except pyodbc.Error as e:
        messagebox.showerror("Error", f"Error al registrar la cuenta: {e}")
    finally:
        connection.close()

# ----------------------------------------------------------MOSTRAR Y OCULTAR FRAMES-----------------------------------------------------------------------------------------------

"""Funcion para Mostrar un Frame"""
def show_frame(frame_to_show):
    global all_frames, action_bar, back_button, current_frame, selected_return, selected_departure, update_user_frame
    current_frame = frame_to_show 
    global sum_cost, num_passengers
    # Ocultar todos los frames
    for frame in all_frames:
        frame.pack_forget()
    # Gestionar visibilidad de la barra de acción
    if hasattr(frame_to_show, "name") and frame_to_show.name in ["loading", "start"]:
        action_bar.pack_forget()
        hide_back_button()
        hide_history_button()
        hide_log_out_button()
        hide_pay_button()
        hide_logo_button()
        sum_cost = 0
        num_passengers = 0
        selected_departure = None
        selected_return = None
    else:
        action_bar.pack(side="top", fill="x")
        hide_back_button()
        hide_history_button()
        hide_log_out_button()
        hide_pay_button()
        show_logo_button()
        if hasattr(frame_to_show, "name"):
            if frame_to_show.name == "content":
                show_log_out_button()
                show_history_button()
                sum_cost = 0
                num_passengers = 0
                selected_departure = None
                selected_return = None
            elif frame_to_show.name == "results":
                show_back_button()
                show_pay_button()
            elif frame_to_show.name == "update_user":
                show_back_button()
                show_log_out_button()
            elif (frame_to_show.name == "pay"):
                show_back_button()
                show_log_out_button()
            elif (frame_to_show.name == "payment_confirmation"):
                show_back_button()
                show_log_out_button()
            elif frame_to_show.name == "history":
                show_back_button()
                show_log_out_button()
            elif frame_to_show.name in ["login", "register", "terms"]:
                show_back_button()
            elif frame_to_show.name == "reservation":
                show_log_out_button()
    frame_to_show.pack(expand=True)

"""Funcion para Mostrar el Boton de Historial"""
def show_history_button(target_frame=None):
    if history_button:
        history_button.place(x=25, y=9)  

"""Funcion para ocultar el Boton de Historial"""
def hide_history_button():
    if history_button:
        history_button.place_forget()

"""Funcion para ocultar Frame al apretar Boton de Historial"""
def on_history_button():
    global current_frame, content_frame, history_frame
    # Ocultar frame actual
    if current_frame == content_frame:
        content_frame.pack_forget()
    hide_history_button()
    history_frame = make_history_frame() 
    show_frame(history_frame)

"""Funcion para Mostrar el Boton de Logo"""
def show_logo_button(target_frame=None):
    if logo_button:
        logo_button.place(relx=0.430, rely=0.3)  

"""Funcion para ocultar el Boton de Logo"""
def hide_logo_button():
    if logo_button:
        logo_button.place_forget()

"""Funcion para ocultar Frame al apretar Boton de Logo"""
def on_logo_button():
    global current_frame, content_frame, update_user_frame
    # Ocultar frame actual
    if current_frame == content_frame:
        content_frame.pack_forget()
        update_user_frame = make_update_user_frame()
        show_frame(update_user_frame)
    else:
        return

"""Funcion para Mostrar el Boton de Pagar"""
def show_pay_button(target_frame=None):
    if pay_button:
        pay_button.place(x=340, y=12)  

"""Funcion para ocultar el Boton de Pagar"""
def hide_pay_button():
    if pay_button:
        pay_button.place_forget()

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
    global current_frame, login_frame, register_frame, start_frame, pay_frame
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

"""Funcion para obtener el Precio de un Bus"""
def get_price_per_bus(origin,destination,passenger_class):
    connection=make_connection()
    if(passenger_class=="Economico"):
        cursor=connection.execute(f"EXEC sp_totaldeventasporruta '{origin}','{destination}',{1}")
    else:
         cursor=connection.execute(f"EXEC sp_totaldeventasporruta '{origin}','{destination}',{0}")
    result =cursor.fetchone()
    print(result)
    if (result!=None):
        return result[0]
    else:
        return ""

"""Funcion para limpiar datos al presionar el Boton Cerrar Sesion"""
def on_log_out_button():
    global current_frame, update_user_frame, reservation_frame, history_frame, start_frame, content_frame, point_origin_input, point_destination_input, departure_date_button, return_date_button, passengers_entry, passenger_class_input, payment_confirmation_frame
    # Borrar datos al cerrar sesión
    if current_frame == content_frame or current_frame == results_frame:
        point_origin_input.set("Seleccionar")  
        point_destination_input.set("Seleccionar")
        departure_date_button.configure(text="Seleccionar") 
        return_date_button.configure(text="Seleccionar")
        passengers_entry.delete(0, tk.END) 
        passenger_class_input.set("Seleccionar")  
    # Ocultar frame actual
    if current_frame == content_frame:
        content_frame.pack_forget()
    if current_frame == reservation_frame:
        reservation_frame.pack_forget()
    if current_frame == history_frame:
        history_frame.pack_forget()
    if current_frame == payment_confirmation_frame:
        payment_confirmation_frame.pack_forget()
    if update_user_frame is not None and current_frame == update_user_frame:
        update_user_frame.pack_forget()
        hide_log_out_button()
        show_frame(content_frame)
    hide_log_out_button()
    show_frame(start_frame)

"""Funcion para ocultar Frame al apretar Boton de Metodo de Pago"""
def on_payment_method_button(billing_payment_method_txt):
    global current_frame, pay_frame, billing_payment_method, sum_cost, total_cost_var, passenger_class_user, payment_confirmation_frame
    billing_payment_method = billing_payment_method_txt
    if billing_payment_method == "Yolo" and passenger_class_user == "VIP":
        sum_cost = sum_cost / 2
        total_cost_var.set(f"El costo total a pagar es: Bs{float(globals()['sum_cost']):g}")
    # Ocultar frame actual
    if current_frame == payment_confirmation_frame:
        payment_confirmation_frame.pack_forget()
    on_paid_method_button()
    hide_history_button()
    show_frame(reservation_frame)

"""Funcion para limpiar datos al presionar el boton de regresar a casa"""
def on_return_home_button():
    global current_frame, reservation_frame, start_frame, content_frame, point_origin_input, point_destination_input, departure_date_button, return_date_button, passengers_entry, passenger_class_input
    # Borrar datos 
    if current_frame == reservation_frame:
        point_origin_input.set("Seleccionar")  
        point_destination_input.set("Seleccionar")
        departure_date_button.configure(text="Seleccionar") 
        return_date_button.configure(text="Seleccionar")
        passengers_entry.delete(0, tk.END) 
        passenger_class_input.set("Seleccionar")  
    # Ocultar frame actual
    if current_frame == reservation_frame:
        reservation_frame.pack_forget()
    show_frame(content_frame)

"""Confirmar seleccion de buses y conectar con la base de datos"""
def on_paid_method_button():
    global selected_departure, selected_return, passengers_entry, passenger_class_input, sum_cost, num_passengers, reservation_frame, billing_payment_method
    try:
        connection = make_connection()
        if not connection:
            print("La conexión falló!")
            return
        cursor = connection.cursor()
        for bus in [selected_departure, selected_return]:
            if bus is not None:
                for i in range(int(passengers_entry.get())):
                    if passenger_class_input.get() == "Economico":
                        cursor.execute(f"EXEC sp_insertar_reserva_economica {obtain_pk(cursor, 'reserva')}, {obtain_userid(cursor)}, {bus}")
                    elif passenger_class_input.get() == "VIP":
                        if billing_payment_method == "Yolo":
                            cursor.execute(f"EXEC sp_insertar_reserva_descuento_yolo {obtain_pk(cursor, 'reserva')}, {obtain_userid(cursor)}, {bus}")
                        else:
                            cursor.execute(f"EXEC sp_insertar_reserva_vip {obtain_pk(cursor, 'reserva')}, {obtain_userid(cursor)}, {bus}")
        user_id = obtain_userid(cursor)
        connection.commit()
        connection.close()
        print(f"Insertando reserva para el usuario {user_id} en el bus {bus} con la clase {passenger_class_input.get()}")
        print("Reserva realizada con exito!")
        reservation_frame=make_reservation_confirmed()
        show_frame(reservation_frame)
    except Exception as e:
        print(f"Error: {e}")
        messagebox.showerror("Error", f"Error al realizar la reserva: {e}")

"""Boton para ir a el frame de pago"""
def on_pay_button(): 
    global current_frame, results_frame, pay_frame, selected_departure, selected_return, passengers_entry, passenger_class_input, sum_cost
    if selected_departure and passengers_entry.get().isdigit() and passenger_class_input.get() != "Seleccionar": 
        if current_frame == results_frame: 
            results_frame.pack_forget()
            hide_pay_button()
            total_cost_var.set(f"El costo total a pagar es: Bs{sum_cost}")
            show_frame(pay_frame) 
    else: 
        messagebox.showerror("Error", "No has seleccionado correctamente los buses")

"""Boton para seleccionar el metodo de pago"""
def on_button_click(payment_method):
    global billing_payment_method, payment_confirmation_frame
    billing_payment_method = payment_method
    print(f"billing_payment_method actualizado a: {billing_payment_method}")
    payment_confirmation_frame = make_payment_confirmation_frame()
    show_frame(payment_confirmation_frame)

# ----------------------------------------------------------------MAIN-----------------------------------------------------------------------------------------------------------------------------------------------

"""Funcion Principal"""
def main():
    global window, all_frames, update_user_frame, reservation_frame, start_frame, register_frame, login_frame, action_bar, content_frame, results_frame, terms_frame, current_frame, loading_frame, history_frame, pay_frame, total_cost_var, payment_confirmation_frame, update_user_frame
    # Configuración de la ventana
    set_appearance_mode("light")
    set_default_color_theme("blue")
    window = tk.Tk()
    total_cost_var = tk.StringVar(window, value="El costo total a pagar es: Bs0")
    window.title("Pasa")
    window.geometry("380x650+120+10")
    window.resizable(False, False)
    window.configure(bg="#7732FF")
    # Agregar Icono
    try:
        window.iconbitmap("../../ASSETS/icon.ico")
    except Exception:
        print("Error al cargar el Icono")
    # Creación de Frames
    loading_frame = make_loading_screen()
    action_bar = make_action_bar()
    action_bar.pack_forget()
    start_frame = make_start_frame()
    register_frame = make_register_frame()
    login_frame = make_login_frame()
    content_frame = make_content_frame()
    pay_frame = make_pay_frame()
    reservation_frame = make_reservation_confirmed()
    results_frame = tk.Frame(window, bg="#F1F2F6") 
    results_frame.name = "results"
    terms_frame = make_terms_frame()
    history_frame = make_history_frame()
    payment_confirmation_frame = make_payment_confirmation_frame()
    # Lista de Frames
    all_frames = [
        loading_frame, start_frame, register_frame,
        login_frame, content_frame, results_frame, terms_frame,
        history_frame, pay_frame, payment_confirmation_frame, reservation_frame
    ]
    # Iniciar el programa
    show_frame(loading_frame)
    window.after(1500, lambda: show_frame(start_frame))
    window.mainloop()

if __name__ == "__main__":
    main()
