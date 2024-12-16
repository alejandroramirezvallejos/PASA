import pyodbc

from tkinter import messagebox

# ---------------------------------------------------CONEXION CON BASE DE DATOS------------------------------------------------------------------------------------------------

"""Configurando la Conexion con la Base de Datos"""
driver = '{ODBC Driver 17 for SQL Server}'
server = ''  
database = 'pasa'
username = '\\user'

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
