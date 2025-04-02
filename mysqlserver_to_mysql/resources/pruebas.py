from queries import queries as q

def prueba_tabla(cursormq,tabla):
    assert cursormq.fetchone() is not None, f"Error: La tabla {tabla} no se creó correctamente en MySQL." 
    print("Prueba: La tabla {tabla} se creo correctamente en MySQL.")

def prueba_cantidad(tamañomq,filas,tabla):
    assert tamañomq == len(filas), f"Error: El número de filas en la tabla {tabla} no coincide. Esperado: {len(filas)}, Actual: {tamañomq}"
    print(f"Prueba: El numero de filas en la tabla {tabla} coincide. Esperado: {len(filas)}, Actual: {tamañomq}")

def prueba_VERIFICACION(cursormq):
     """ Verifica si la base de datos existe en MySQL. 
    Ejecuta la consulta definida en `q.EXISTE_BASE` y devuelve True si la base de datos existe, False en caso contrario. 
    Returns: 
    bool: True si la base de datos existe, False en caso contrario. """
     cursormq.execute(q.EXISTE_BASE)
     existencia=cursormq.fetchone()
     if(existencia is None):
        return False
     else:
        return True
