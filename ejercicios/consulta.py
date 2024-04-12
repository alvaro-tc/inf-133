# Importar módulo sqlite3
import sqlite3

# Crear conexión a la base de datos
conn = sqlite3.connect("personal.db")





# Consultar datos de empleados y salarios 
print("----Mostrando empleados y sus salarios: ")
cursor = conn.execute(
    """
    SELECT EMPLEADOS.nombres, EMPLEADOS.apellido_paterno, EMPLEADOS.apellido_materno, SALARIOS.salario 
    FROM EMPLEADOS
    JOIN SALARIOS ON EMPLEADOS.id = SALARIOS.empleado_id
    """
)
for row in cursor:
    print(row)
# Consultar datos de empleados, departamento y cargo
print("----Mostrando empleados, departamento y cargo: ")
cursor = conn.execute(
    """
    SELECT EMPLEADOS.nombres, EMPLEADOS.apellido_paterno, EMPLEADOS.apellido_materno, DEPARTAMENTOS.nombre, CARGOS.nombre,CARGOS.nivel 
    FROM EMPLEADOS
    JOIN DEPARTAMENTOS ON EMPLEADOS.departamento_id = DEPARTAMENTOS.id
    JOIN CARGOS ON EMPLEADOS.cargo_id = CARGOS.id
    """
)
for row in cursor:
    print(row)
    
    
# Consultar datos de empleados, departamento, cargo y salario
print("----Mostrando empleados, departamento, cargocargo: ")
cursor = conn.execute(
    """
    SELECT EMPLEADOS.nombres, EMPLEADOS.apellido_paterno, EMPLEADOS.apellido_materno, DEPARTAMENTOS.nombre, CARGOS.nombre,CARGOS.nivel, SALARIOS.salario 
    FROM EMPLEADOS
    JOIN DEPARTAMENTOS ON EMPLEADOS.departamento_id = DEPARTAMENTOS.id
    JOIN CARGOS ON EMPLEADOS.cargo_id = CARGOS.id
    JOIN SALARIOS ON EMPLEADOS.id = SALARIOS.empleado_id
    """
)
for row in cursor:
    print(row)



# Actualizar el cargo de María Lopez Martinez
conn.execute(
    """
    UPDATE EMPLEADOS 
    SET cargo_id = 3 
    WHERE id = 2
    """
)
# Actualizar el salario de Representante de Ventas
conn.execute(
    """
    UPDATE SALARIOS 
    SET salario = 3600
    WHERE empleado_id = 2
    """
)


# Eliminar a María Lopez Martinez
conn.execute(
    """
    DELETE FROM SALARIOS 
    WHERE empleado_id = 2
    """
)
conn.execute(
    """
    DELETE FROM EMPLEADOS 
    WHERE id = 2
    """
)











# Insertar datos de empleados
conn.execute(
    """
    INSERT INTO EMPLEADOS (nombres,apellido_paterno, apellido_materno,fecha_contratacion,departamento_id,cargo_id,fecha_creacion) 
    VALUES ('Carlos','Sanchez','Rodriguez','09-04-2024',1,1, '09-04-2024')
    """
)
#Insertar datos de Salarios
conn.execute(
    """
    INSERT INTO SALARIOS (empleado_id,salario, fecha_inicio,fecha_fin,fecha_creacion) 
    VALUES (3,3500,'05-05-2023','05-12-2024','09-04-2024')
    """
)


# Confirmar cambios
conn.commit()

# Cerrar conexión
conn.close()
