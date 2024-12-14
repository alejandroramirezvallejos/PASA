import pyodbc
import mysql.connector


def conectar_mysqlserver():
    """ Establece una conexión con el servidor SQL Server. 
    Returns: 
    conexion (pyodbc.Connection): Objeto de conexión a SQL Server. 
    """
    conexion=pyodbc.connect('''
        DRIVER={ODBC Driver 17 for SQL Server};
        SERVER=;
        DATABASE=pasa;
        Trusted_Connection=yes;
    ''')
    print("conexion exitosa mysqlserver")
    return conexion
def conectar_mysql():
    """ Establece una conexión con el servidor MySQL.
      Returns: 
      conexion (mysql.connector.connection.MySQLConnection): Objeto de conexión a MySQL. 
    """
    conexion= mysql.connector.connect( host='localhost'
                                   , user='', 
                                   password='')
    print("conexion exitosa mysql")
    return conexion
def cerrar_conexion(cursorms,cursormq,conexionms,conexionmq):
    """ Cierra las conexiones y cursores de SQL Server y MySQL. 
    Args: 
    cursorms (pyodbc.Cursor): Cursor de SQL Server. 
    cursormq (mysql.connector.cursor.MySQLCursor): Cursor de MySQL. 
    conexionms (pyodbc.Connection): Conexión a SQL Server. 
    conexionmq (mysql.connector.connection.MySQLConnection): Conexión a MySQL. 
    """
    cursorms.close()
    cursormq.close()
    conexionms.close()
    conexionmq.close()

    print("conexion cerrada")