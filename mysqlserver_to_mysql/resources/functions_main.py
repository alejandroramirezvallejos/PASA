from dataclasses import dataclass
from queries import queries as q
import functions as fs
import pyodbc
import mysql.connector
import pruebas as p
@dataclass
class MIGRACION:
    cursorms:pyodbc.Cursor
    cursormq:mysql.connector.cursor.MySQLCursor
    def CREAR_BASE(self):
        """ Crea la base de datos en MySQL y la selecciona para su uso. 
            Ejecuta las consultas definidas en `q.CREAR_DATABASE` y `q.USAR_DATABASE`. """
        self.cursormq.execute(q.CREAR_DATABASE)
        self.cursormq.execute(q.USAR_DATABASE)

    def OBTENER_TABLAS(self)->list:
        """ Obtiene la lista de tablas desde SQL Server.
          Ejecuta la consulta definida en `q.OBTENER_TABLAS` y devuelve los resultados. 
          Returns: list: Lista de tablas obtenidas de SQL Server. """
        self.cursorms.execute(q.OBTENER_TABLAS)
        return self.cursorms.fetchall()

    def CREAR_TABLA(self,tabla:tuple):
        """ Crea una tabla en MySQL basada en la estructura de una tabla en SQL Server. 
        Args: 
        tabla (tuple): Tupla que contiene el nombre de la tabla. 
        """
        self.cursorms.execute(q.EXTRAER_COLUMNAS.format(tabla[0]))
        columnas=self.cursorms.fetchall()
        self.cursormq.execute(q.CREAR_TABLA.format(tabla[0],fs.valores_columnas(columnas)))
        #verificar si se creo la tabla
        self.cursormq.execute(q.COMPROBAR_TABLA.format(tabla[0]))
        p.prueba_tabla(self.cursormq,tabla[0])

    def METER_DATOS_TABLA(self,tabla:tuple):
        """ Inserta los datos de una tabla de SQL Server en la tabla correspondiente en MySQL. 
        Args: tabla (tuple): Tupla que contiene el nombre de la tabla. """
        self.cursorms.execute(q.OBTENER_DATOS.format(tabla[0]))
        filas:list=self.cursorms.fetchall()
        for fila in filas:
            self.cursormq.execute(q.INSERTAR_DATOS.format(tabla[0],fs.valores_filas(fila)))
        self.cursormq.execute(q.COMPROBAR_DATOS.format(tabla[0]))
        tamañomq:int = self.cursormq.fetchone()[0]
        p.prueba_cantidad(tamañomq,filas,tabla[0])
        

    def CREAR_PK(self,tabla:tuple):
            """ Crea la clave primaria para una tabla en MySQL basada en la clave primaria de SQL Server. 
            Args: 
            tabla (tuple): Tupla que contiene el nombre de la tabla. """
            self.cursorms.execute(q.OBTENER_PK.format(tabla[0]))
            pk:tuple=self.cursorms.fetchall()
            self.cursormq.execute(q.INSERTAR_PK.format(tabla[0],pk[0][0]))

    def CREAR_FK(self,tablas:list):
        """ Crea las claves foráneas para las tablas en MySQL basadas en las claves foráneas de SQL Server. 
        Args: 
        tablas (list): Lista de tuplas que contienen los nombres de las tablas. """
        for tabla in tablas:
            self.cursorms.execute(q.OBTENER_FK.format(tabla[0]))
            llaves_foranesa:list=self.cursorms.fetchall()
            for fk in llaves_foranesa:
                self.cursormq.execute(q.INSERTAR_FK.format(fk[1],fk[0],fk[2],fk[3],fk[4]))

        
