import sys 
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'resources')))

import conexion as c
from resources import functions_main
from resources import pruebas as p

try: 
    #mysqlserver
    conexionms=c.conectar_mysqlserver()
    cursorms=conexionms.cursor()
    #mysql
    conexionmq =c.conectar_mysql()
    cursormq=conexionmq.cursor()
    migracion1=functions_main.MIGRACION(cursorms,cursormq)
    if(p.prueba_VERIFICACION(cursormq)==True):
        print("La base de datos 'pasa' ya existe. Finalizando el programa.")
    else:
        migracion1.CREAR_BASE()
        tablas:list=migracion1.OBTENER_TABLAS()
        
        for tabla in tablas:
            migracion1.CREAR_TABLA(tabla)
            migracion1.METER_DATOS_TABLA(tabla)
            migracion1.CREAR_PK(tabla)
        
        migracion1.CREAR_FK(tablas)   
        conexionmq.commit()

except Exception as ex:
    print(f"error al conectar a la base de datos {ex}")

finally: 
    c.cerrar_conexion(cursorms,cursormq,conexionms,conexionmq)