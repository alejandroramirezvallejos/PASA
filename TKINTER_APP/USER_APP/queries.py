BUSCA_CARNET="SELECT carnet FROM usuario WHERE carnet = {};"
CREAR_LLAVE="SELECT {}_id FROM {} ORDER BY {}_id DESC "
OBTENER_LLAVE="select usuario_id from usuario where carnet={}"
CREAR_USUARIO="""
        INSERT INTO usuario (usuario_id,nombre, apellido, edad, carnet, contraseña, admin) 
        VALUES ({},'{}','{}',{},{},'{}',0);
        """
OBTENER_USUARIO="SELECT * FROM dbo.usuario WHERE carnet = ? AND contraseña = ?"
OBTENER_DATOS_BUS="""
        SELECT b.bus_id, b.fecha_salida, COUNT(r.bus_id) AS asientos_ocupados
        FROM bus AS b
        JOIN chofer AS c ON b.chofer_id = c.chofer_id
        LEFT JOIN reserva AS r ON b.bus_id = r.bus_id
        WHERE b.ruta_id IN (
        SELECT ruta_id 
        FROM ruta 
        WHERE dep_inicio = '{}' AND dep_final = '{}'
        )
        AND b.fecha_salida = '{}'
        GROUP BY b.bus_id, b.fecha_salida
        HAVING COUNT(r.bus_id) <= (60 - {});
        """
INSERTAR_ECONOMICO="""INSERT INTO reserva (reserva_id, usuario_id,bus_id,vip)
                                        VALUES ({}, {},{} ,0);
                        """
INSERTAR_VIP="""INSERT INTO reserva (reserva_id, usuario_id,bus_id,vip)
                                        VALUES ({}, {},{} ,1);
                        """





