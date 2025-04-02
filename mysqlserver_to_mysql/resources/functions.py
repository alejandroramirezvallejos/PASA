def valores_columnas(columnas:list)->str:
    """ 
    Genera una cadena de texto con las definiciones de columnas para una tabla SQL. 
    Args: 
    columnas (list): Lista de tuplas que representan las columnas, donde cada tupla contiene el nombre de la columna, el tipo de dato y la longitud (si aplica). 
    Returns: 
    str: Cadena de texto con las definiciones de columnas para una tabla SQL. 
    """
    valorescolumnas:str=""
    for columna in columnas:
        if columna[1] =='bit':
             valorescolumnas:str = valorescolumnas + columna[0] + " BOOLEAN,"
        elif columna[2] != None:
             valorescolumnas:str=valorescolumnas+columna[0] +" "+ columna[1]+f"({columna[2]}),"
        else:
             valorescolumnas:str=valorescolumnas+columna[0] +" "+ columna[1]+","
    valorescolumnas:str=valorescolumnas+"fecha_modificacion DATE"
    return valorescolumnas

def valores_filas(fila:list)->str:
    """ Genera una cadena de texto con los valores de una fila para una inserción SQL. 
    Args: 
    fila (list): Lista de valores que representan una fila de datos. 
    Returns: str: 
    Cadena de texto con los valores de la fila formateados para una inserción SQL. """
    valores:str=""
    for valor in fila:
        if valor==None:
            valor="NULL"
            valores=valores+f"{str(valor)}"+","
        elif valor==True:
            valor=1
            valores=valores+f"'{str(valor)}'"+","
        elif valor==False:
            valor=0
            valores=valores+f"'{str(valor)}'"+","
        else:
            valores=valores+f"'{str(valor)}'"+","
    return valores[:-1]