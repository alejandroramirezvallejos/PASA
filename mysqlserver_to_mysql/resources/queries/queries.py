CREAR_DATABASE ="CREATE DATABASE IF NOT EXISTS pasa;"
USAR_DATABASE="USE pasa;"
OBTENER_TABLAS="SELECT table_name FROM information_schema.tables WHERE table_type = 'BASE TABLE' AND table_catalog='pasa' AND table_name != 'sysdiagrams'"
EXTRAER_COLUMNAS="SELECT column_name, data_type, character_maximum_length FROM information_schema.columns WHERE table_name = '{}'"
CREAR_TABLA="CREATE TABLE IF NOT EXISTS {} ({})"
COMPROBAR_TABLA="SHOW TABLES LIKE '{}'"
OBTENER_DATOS="SELECT * FROM {}"
INSERTAR_DATOS="INSERT INTO {} VALUES ({},NOW())"
COMPROBAR_DATOS="SELECT COUNT(*) FROM {}"
OBTENER_PK="SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE TABLE_NAME = '{}' AND CONSTRAINT_NAME LIKE 'PK_%';"
INSERTAR_PK="ALTER TABLE {} ADD PRIMARY KEY ({})"
OBTENER_FK="""SELECT 
        fk.name AS foreign_key_name, 
        tp.name AS parent_table, 
        cp.name AS parent_column, 
        tr.name AS referenced_table, 
        cr.name AS referenced_column 
        FROM sys.foreign_keys AS fk 
        INNER JOIN sys.foreign_key_columns AS fkc 
        ON fk.object_id = fkc.constraint_object_id 
        INNER JOIN sys.tables AS tp 
        ON fk.parent_object_id = tp.object_id 
        INNER JOIN sys.columns AS cp 
        ON fkc.parent_column_id = cp.column_id AND fkc.parent_object_id = cp.object_id 
        INNER JOIN sys.tables AS tr 
        ON fk.referenced_object_id = tr.object_id INNER JOIN sys.columns AS cr 
        ON fkc.referenced_column_id = cr.column_id 
        AND fkc.referenced_object_id = cr.object_id WHERE tp.name = '{}';"""
INSERTAR_FK=""" ALTER TABLE {} ADD CONSTRAINT {} FOREIGN KEY ({}) REFERENCES {}({}) """
EXISTE_BASE="SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'pasa'"