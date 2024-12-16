
import conection as c

#-----------------------------------------------FUNCION OBTENCION DE LLAVE NUEVA--------------------------------------------------------------------------------------------------=
def obtain_pk(cursor,tabla:str)->str:
    cursor.execute(f"SELECT {tabla}_id FROM {tabla} ORDER BY {tabla}_id DESC ")
    return cursor.fetchone()[0]+1


def validate_carnet(carnet:str)->bool:
    conexion=c.make_connection()
    cursor=conexion.cursor()
    cursor.execute(f"SELECT carnet FROM usuario WHERE carnet = {carnet};")
    valor=cursor.fetchone()
    if valor is None:
        return False
    else:
        return True
#---------------------------------------------QUERYS-----------------------------------------------------------------------------------------
#obtiene tabla rutas
def get_route(cursor):
    cursor.execute(f"SELECT * FROM ruta;")
    return cursor.fetchall()
#obtiene tabla bus
def get_bus(cursor):
    cursor.execute(f"SELECT * FROM bus;")
    return cursor.fetchall()
#obtiene tabla chofer
def get_driver(cursor):
    cursor.execute(f"SELECT * FROM chofer;")
    return cursor.fetchall()
#obtiene  reservas
def get_booking(cursor):
    cursor.execute(f"""
SELECT reserva_id, reserva.usuario_id, usuario.nombre, usuario.apellido, bus.bus_id,
    CASE
        WHEN vip = 0 THEN costo
        WHEN vip = 1 THEN costo_vip
    END AS costo
FROM reserva
INNER JOIN usuario ON reserva.usuario_id = usuario.usuario_id
INNER JOIN bus ON bus.bus_id = reserva.bus_id
INNER JOIN ruta ON bus.ruta_id = ruta.ruta_id;
""")
    return cursor.fetchall()

# adicionan cosas
#addiciona bus
def add_bus(chofer_id,ruta_id,fecha_sal,fecha_ret):
    conexion=c.make_connection()
    cursor=conexion.cursor()
    cursor.execute(f"""INSERT INTO bus (bus_id, chofer_id, ruta_id, fecha_salida,fecha_retorno)
VALUES ({obtain_pk(cursor,"bus")},{chofer_id},{ruta_id},'{fecha_sal}','{fecha_ret}');
""")
    conexion.commit()
#adicciona chofer
def add_driver(nombre,edad,carnet):
    conexion=c.make_connection()
    cursor=conexion.cursor()
    cursor.execute(f"""INSERT INTO chofer 
                           (chofer_id,nombre,edad,carnet)
                            VALUES ({obtain_pk(cursor,"chofer")},'{nombre}',{edad},{carnet});
                           """)
    conexion.commit()
#adicionar ruta
def add_route(dep_inicio,dep_final,costo,costo_vip):
    conexion=c.make_connection()
    cursor=conexion.cursor()
    cursor.execute(f"""INSERT INTO ruta (ruta_id,dep_inicio,dep_final,costo,costo_vip)
VALUES ({obtain_pk(cursor,"ruta")},'{dep_inicio}','{dep_final}',{costo},{costo_vip});
""")
    conexion.commit()
#-------------------------eliminar----------------------------------------------
#elimina un bus con su id
def del_bus(bus_id):
    conexion=c.make_connection()
    cursor=conexion.cursor()
    cursor.execute(f"""DELETE FROM bus
    WHERE bus_id = {bus_id};
""")
    conexion.commit()
#elimina un chofer con su id
def del_driver(chofer_id):
    conexion=c.make_connection()
    cursor=conexion.cursor()
    cursor.execute(f"""DELETE FROM chofer
    WHERE chofer_id = {chofer_id};
""")
    conexion.commit()
#elimina una ruta con su id
def del_route(route_id):
    conexion=c.make_connection()
    cursor=conexion.cursor()
    cursor.execute(f"""DELETE FROM ruta
    WHERE ruta_id = {route_id};
""")
    conexion.commit()
#------------------------modificar------------------------------
#verifica si un id de una tabla existe
def verification_id(cursor,table,id):
    cursor.execute(f"SELECT {table}_id FROM {table} WHERE {table}_id = {id};")
    valor=cursor.fetchone()
    if valor is None:
        return False
    else:
        return True
#actualiza bus y si no existe lo crea
def update_bus(bus_id,chofer_id,ruta_id,fecha_salida,fecha_retorno):
    conexion=c.make_connection()
    cursor=conexion.cursor()
    if(verification_id(cursor,"bus",bus_id)==True):
        cursor.execute(f"""UPDATE bus
    SET chofer_id ={chofer_id}, 
        ruta_id = {ruta_id},  
        fecha_retorno = '{fecha_retorno}',
        fecha_salida='{fecha_salida}'
    WHERE bus_id = {bus_id};
    """)
    else:
        add_bus(chofer_id,ruta_id,fecha_salida,fecha_retorno)
    conexion.commit()
#actualiza chofer y si no existe lo crea
def update_driver(chofer_id,nombre,edad,carnet):
    conexion=c.make_connection()
    cursor=conexion.cursor()
    if(verification_id(cursor,"chofer",chofer_id)==True):
        cursor.execute(f"""UPDATE chofer
        SET nombre = '{nombre}', 
            edad= {edad}, 
            carnet = {carnet}
        WHERE chofer_id ={chofer_id} ;
    """)
    else:
        add_driver(nombre,edad,carnet)
    conexion.commit()
#actualiza ruta y si no existe lo crea 
def update_route(ruta_id,dep_inicio,dep_final,costo,costo_vip):
    conexion=c.make_connection()
    cursor=conexion.cursor()
    if(verification_id(cursor,"ruta",ruta_id)==True):
        cursor.execute(f"""UPDATE ruta
        SET dep_inicio = '{dep_inicio}', 
            dep_final= '{dep_final}', 
            costo = {costo},
            costo_vip= {costo_vip}
        WHERE ruta_id = {ruta_id};
    """)
    else:
        add_route(dep_inicio,dep_final,costo,costo_vip)
    conexion.commit()



