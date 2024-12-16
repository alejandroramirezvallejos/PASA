import tkinter as tk 
import pyodbc
from tkinter import messagebox, font
from tkcalendar import Calendar
from datetime import date
from PIL import Image, ImageTk
from customtkinter import CTkComboBox, CTkButton, CTkEntry, set_appearance_mode, set_default_color_theme

"""Configurando la Conexion con la Base de Datos"""
driver = '{ODBC Driver 17 for SQL Server}'
server = 'LENOVO'  
database = 'pasa'
username = 'LENOVO\\user' 

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

"""Crear llave"""
def obtain_pk(cursor,tabla:str)->str:
    cursor.execute(f"SELECT {tabla}_id FROM {tabla} ORDER BY {tabla}_id DESC ")
    return cursor.fetchone()[0]+1
#obtener llave
def obtain_userid(cursor):
    cursor.execute(f"""select usuario_id from usuario where carnet={id_card}""")
    return cursor.fetchone()[0]
