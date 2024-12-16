import tkinter as tk
from tkinter import messagebox, font
import pyodbc
from customtkinter import CTkComboBox, CTkButton, CTkEntry
from . import connection as con, user_show_frames as usf, action_bar as a

"""Funcion para Validar si un Usuario tiene el mismo Numero de Catnet"""
def validate_carnet(carnet:str)->bool:
    conexion=con.make_connection()
    cursor=conexion.cursor()
    cursor.execute(f"SELECT carnet FROM usuario WHERE carnet = {carnet};")
    valor=cursor.fetchone()
    if valor is None:
        return False
    else:
        return True

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
    connection = con.make_connection()
    if not connection:
        return
    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO usuario (usuario_id,nombre, apellido, edad, carnet, contraseña, admin) 
        VALUES ({},'{}','{}',{},{},'{}',0);
        """
        cursor.execute(query.format(obtain_pk(cursor,"usuario"),name, last_name, age, id_card, password))
        connection.commit()
        # Cambiar al content_frame si todo sale bien
        usf.show_frame(content_frame)
    except pyodbc.Error as e:
        messagebox.showerror("Error", f"Error al registrar la cuenta: {e}")
    finally:
        connection.close()

"""Extraer Datos para Verificar el Inicio de Sesion"""
def login():
    # Entrada de Datos
    global content_frame
    global id_card 
    id_card=login_id_card_entry.get().strip()
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
    connection = con.make_connection()
    if not connection:
        return
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM dbo.usuario WHERE carnet = ? AND contraseña = ?"
        cursor.execute(query, (id_card, password))
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

"""Frame para Crear una Cuenta"""
def make_register_frame(window):
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
    a.show_back_button()
    return register_frame

"""Frame para Iniciar Sesion"""
def make_login_frame(window):
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
    a.show_back_button()
    return login_frame