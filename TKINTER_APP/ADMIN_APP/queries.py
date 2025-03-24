INSERTAR_USUARIO="""
        INSERT INTO usuario (usuario_id,nombre, apellido, edad, carnet, contraseña, admin) 
        VALUES ({},'{}','{}',{},{},'{}',1);
        """
OBTENER_USUARIO="SELECT * FROM dbo.usuario WHERE carnet = ? AND contraseña = ?"




