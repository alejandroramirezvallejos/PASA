import conection as c

#-----------------------------------------------FUNCION OBTENCION DE LLAVE NUEVA--------------------------------------------------------------------------------------------------=

def obtain_pk(cursor,tabla:str)->str:
    cursor.execute(f"SELECT {tabla}_id FROM {tabla} ORDER BY {tabla}_id DESC ")
    return cursor.fetchone()[0]+1

def validate_carnet(carnet:str)->bool:
    conexion=c.make_connection()
    cursor=conexion.cursor()
    cursor.execute(f"EXEC sp_valida_carnet '{carnet}'")
    valor=cursor.fetchone()
    if valor is None:
        return False
    else:
        return True
#-------------------------------------------------------------------QUERYS-----------------------------------------------------------------------------------------

# obtiene tabla rutas
def get_route(cursor):
    cursor.execute(f"EXEC sp_obtiene_tabla_ruta")
    return cursor.fetchall()

# obtiene tabla bus
def get_bus(cursor):
    cursor.execute(f"EXEC sp_obtiene_tabla_bus")
    return cursor.fetchall()

# obtiene tabla chofer
def get_driver(cursor):
    cursor.execute(f"EXEC sp_obtiene_tabla_chofer")
    return cursor.fetchall()

# obtiene reservas
def get_booking(cursor):
    cursor.execute(f"EXEC sp_obtener_reservas")
    return cursor.fetchall()

def get_reportes_total(cursor):
    
    cursor.execute("EXEC sp_obtiene_vista_Reporte")
    return cursor.fetchall()

def get_reportes(cursor):
    
    cursor.execute("SELECT * FROM vw_ReportesReservas")
    return cursor.fetchall()

def get_usuarios(cursor):
    cursor.execute("EXEC sp_obtiene_tabla_usuario")
    return cursor.fetchall()

def get_chofer(cursor):
    cursor.execute("EXEC sp_obtiene_tabla_chofer")
    return cursor.fetchall()

def get_bus_elimacion(cursor):
    cursor.execute("EXEC sp_obtiene_tabla_bus_para_eliminacion")
    return cursor.fetchall()


# addiciona bus
def add_bus(chofer_id,ruta_id,fecha_sal,fecha_ret):
    conexion=c.make_connection()
    cursor=conexion.cursor()
    cursor.execute(f"EXEC sp_adiccionar_bus {obtain_pk(cursor,'bus')},{chofer_id},{ruta_id},'{fecha_sal}','{fecha_ret}';")
    conexion.commit()

# adicciona chofer
def add_driver(nombre,edad,carnet):
    conexion=c.make_connection()
    cursor=conexion.cursor()
    cursor.execute(f"EXEC sp_adiccionar_chofer {obtain_pk(cursor,'chofer')},'{nombre}','{edad}','{carnet}'")
    conexion.commit()

# adicionar ruta
def add_route(dep_inicio,dep_final,costo,costo_vip):
    conexion=c.make_connection()
    cursor=conexion.cursor()
    cursor.execute(f"EXEC sp_adiccionar_ruta {obtain_pk(cursor,'ruta')},'{dep_inicio}','{dep_final}',{costo},{costo_vip}")
    conexion.commit()

#-----------------------------------------------------eliminar--------------------------------------------------

# elimina un bus con su id
def del_bus(bus_id):
    conexion=c.make_connection()
    cursor=conexion.cursor()
    cursor.execute(f"EXEC sp_eliminacion_fisica_bus {bus_id}")
    conexion.commit()

# elimina un chofer con su id
def del_driver(chofer_id):
    conexion=c.make_connection()
    cursor=conexion.cursor()
    cursor.execute(f"EXEC sp_eliminacion_fisica_chofer {chofer_id}")
    conexion.commit()

# elimina una ruta con su id
def del_route(route_id):
    conexion=c.make_connection()
    cursor=conexion.cursor()
    cursor.execute(f"EXEC sp_eliminacion_fisica_ruta {route_id}")
    conexion.commit()

def del_usuario(usuario_id):
    conexion=c.make_connection()
    cursor=conexion.cursor()
    cursor.execute(f"EXEC sp_eliminacion_fisica_usuario {usuario_id}")
    conexion.commit()

# eliminacion logica
def del_bus_logic(bus_id):
    conexion=c.make_connection()
    cursor=conexion.cursor()
    cursor.execute(f"EXEC sp_eliminacion_logica_bus {bus_id}")
    conexion.commit()

# elimina un chofer con su id
def del_driver_logic(chofer_id):
    conexion=c.make_connection()
    cursor=conexion.cursor()
    cursor.execute(f"EXEC sp_eliminacion_logica_chofer {chofer_id}")
    conexion.commit()

# elimina una ruta con su id
def del_route_logic(route_id):
    conexion=c.make_connection()
    cursor=conexion.cursor()
    cursor.execute(f"EXEC sp_eliminacion_logica_ruta {route_id}")
    conexion.commit()

def del_usuario_logic(usuario_id):
    conexion=c.make_connection()
    cursor=conexion.cursor()
    cursor.execute(f"EXEC sp_eliminacion_logica_usuario {usuario_id}")
    conexion.commit()

#------------------------------------------------------------modificar--------------------------------------------------

# verifica si un id de una tabla existe
def verification_id(cursor,table,id):
    cursor.execute(f"SELECT {table}_id FROM {table} WHERE {table}_id = {id};")
    valor=cursor.fetchone()
    if valor is None:
        return False
    else:
        return True
    
# actualiza bus 
def update_bus(bus_id,chofer_id,ruta_id,fecha_salida,fecha_retorno):
    conexion=c.make_connection()
    cursor=conexion.cursor()
    cursor.execute(f"EXEC sp_update_bus {chofer_id},{ruta_id},'{fecha_salida}','{fecha_retorno}',{bus_id}")
    conexion.commit()

# actualiza chofer 
def update_driver(chofer_id,nombre,edad,carnet):
    conexion=c.make_connection()
    cursor=conexion.cursor()
    cursor.execute(f"EXEC sp_update_chofer {chofer_id},'{nombre}','{edad}','{carnet}'")
    conexion.commit()

# actualiza ruta 
def update_route(ruta_id,dep_inicio,dep_final,costo,costo_vip):
    conexion=c.make_connection()
    cursor=conexion.cursor()
    cursor.execute(f"EXEC sp_update_ruta {ruta_id},'{dep_inicio}','{dep_final}',{costo},{costo_vip}")
    conexion.commit()



# actualiza un usuario
def update_user(usuario_id,nombre,apellido,edad,carnet,contraseña,admin):
    conexion=c.make_connection()
    cursor=conexion.cursor()
    cursor.execute(f"EXEC sp_update_usuario {usuario_id} , '{nombre}' , '{apellido}' , {edad} , '{carnet}' , '{contraseña}' , {admin}")
    conexion.commit()

#-------------------
# obtiene tabla rutas
def get_route_res(cursor):
    cursor.execute(f"EXEC sp_ver_eliminados_logicos_ruta")
    return cursor.fetchall()

# obtiene tabla bus
def get_bus_res(cursor):
    cursor.execute(f"EXEC sp_ver_eliminados_logicos_bus")
    return cursor.fetchall()

# obtiene tabla chofer
def get_driver_res(cursor):
    cursor.execute(f"EXEC sp_ver_eliminados_logicos_chofer")
    return cursor.fetchall()

# Obtiene tabla usuario
def get_user_res(cursor):
    cursor.execute(f"EXEC sp_ver_eliminados_logicos_usuario")
    return cursor.fetchall()




# restauracion logica
def res_bus_logic(bus_id):
    conexion=c.make_connection()
    cursor=conexion.cursor()
    cursor.execute(f"""UPDATE bus 
SET registro_eliminado = 0
WHERE bus_id = {bus_id};
""")
    conexion.commit()

# elimina un chofer con su id
def res_driver_logic(chofer_id):
    conexion=c.make_connection()
    cursor=conexion.cursor()
    cursor.execute(f"""UPDATE chofer 
SET registro_eliminado = 0
WHERE chofer_id = {chofer_id};""")
    conexion.commit()

# elimina una ruta con su id
def res_route_logic(route_id):
    conexion=c.make_connection()
    cursor=conexion.cursor()
    cursor.execute(f"""
UPDATE ruta 
SET registro_eliminado = 0
WHERE ruta_id = {route_id};
""")
    conexion.commit()

def res_usuario_logic(usuario_id):
    conexion=c.make_connection()
    cursor=conexion.cursor()
    cursor.execute(f"""UPDATE usuario 
SET registro_eliminado = 0
WHERE usuario_id = {usuario_id};""")
    conexion.commit()