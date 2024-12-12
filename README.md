# PASA "Viajar nunca fue más simple"

Este proyecto implementa un sistema de migración y gestión de datos para una empresa de buses, permitiendo la transición desde un sistema heredado en SQL Server a una nueva implementación en MySQL,ademas con una interfaz grafica que complementa al proyecto.

## 🚌 Descripción del Proyecto

El sistema moderniza la gestión de datos de una empresa de buses, facilitando:
- Migración desde SQL Server a MySQL
- Preservación de la integridad de datos
- Manejo eficiente de registros
- Interfaz para agregar informacion en dos partes admin y usuario

## ✨ Funcionalidades

### Implementadas
- Migración completa de esquemas
- Preservación de relaciones
- Validación de datos
- Sistema de prevención de duplicados
- Gestión de errores
- Visualizar registros
- Agregar registros
- Modificar y eliminar registros
- Adaptable a las dos bases de datos
## 🗄️ Estructura del Proyecto

```
├──tkinter_app
│   ├──main.py                    # Codigo de la Interfaz
├──DATABASE             
│   ├──pasa.bak                   # Base de datos en MySQL_Server
├──IMAGES
│   ├──Imagenes varias            # Recursos de la Interfaz
├── mysqlserver_to_mysq
│   ├── conexion.py               # Gestión de conexiones
│   ├── main.py                   # Punto de entrada
│   ├──resources 
│       ├── functions.py          # Funciones auxiliares
│       ├── functions_main.py     # Clase principal
│       ├──queries
│           └── queries.py        # Consultas SQL
├── Readme_data                 
│   └── Imagenes varias e video   # Informacion para hacer mejor el readme 
├──LICENSE                        # Licencia MIT
```

## 🛠️ Tecnologías

### Implementadas
- Python 3.11
- SQL Server
- MySQL
- pyodbc
- mysql-connector-python
- Tkinter
- tkcalendar
- datetime
- sys y os
## 🚀 Instalación

1. Clonar el repositorio
```bash
git clone [https://github.com/alejandroramirezvallejos/PASA.git]
```

2. Configurar credenciales en `conexion.py`:
```python
# SQL Server
SERVER=''
DATABASE=''
Trusted_Connection=''

# MySQL
host=''
user=''
password=''
```

3. Instalar la base de datos en mysql_server 

4. Instalar todos los paquetes necesarios de python

## 📊 Estructura de Base de Datos

### Diagramas de relación entidad

![alt text](Readme_data/diagrama_entidad_relacion.png)

###  Diagramas de clases
#### Traslado de base datos

![alt text](Readme_data/diagrama_clases.png)

#### Interfaz

## 🔄 Funcionalidades de Migración

### Proceso
1. Verificación de base destino
2. Creación de esquema
3. Migración de datos
4. Validación de integridad

### Validaciones
- Verificación de tablas
- Verificacion contra duplicacion
### Pseudocodigo


## 🎯 Interfaz de Usuario 

### Características Implementadas
- [ ] [A completar funcionalidades...]

### Validaciones
```
[A completar con diseños...]
```
### Pseudocodigo


## 🧪 Testing

### Tests Implementados
- Verificación de migración
- Validación de datos
- [Otros tests implementados...]


## 👥 Equipo y Contribuciones

### Equipo Principal
```
Alejandro Ramirez
Josue Balbontin
```

### Cómo Contribuir
1. Fork del proyecto
2. Crear rama feature
3. Commit cambios
4. Push a la rama
5. Crear Pull Request

## 📄 Licencia

MIT License 

Copyright (c) 2024 Alejandro Ramírez and Josue Balbontin