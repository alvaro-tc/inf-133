# Importar módulo sqlite3
import sqlite3

# Crear conexión a la base de datos
conn = sqlite3.connect("restaurantes.db")

conn.execute(
    """
    UPDATE PLATOS
    SET precio= 9.99
    WHERE id=1 
    """
)

conn.execute(
    """
    UPDATE PLATOS
    SET categoria='fusion'
    WHERE id=3 
    """
)

conn.execute(
    """
    DELETE FROM PEDIDOS
    WHERE id=3 
    """
)


# Consultar datos de pedidos INNER JOIN
print("\PEDIDOS: INNER JOIN")
cursor = conn.execute(
    """
    SELECT PLATOS.nombre, PLATOS.precio,PLATOS.categoria, MESAS.numero, PEDIDOS.cantidad, PEDIDOS.fecha 
    FROM PEDIDOS
    JOIN PLATOS ON PEDIDOS.plato_id = PLATOS.id 
    JOIN MESAS ON PEDIDOS.mesa_id = MESAS.id
    """
)
for row in cursor:
    print(row)


# Consultar datos de pedidos LEFT JOIN
print("\PEDIDOS: LEFT JOIN")
cursor = conn.execute(
    """
    SELECT PLATOS.nombre, PLATOS.precio, PLATOS.categoria, PEDIDOS.cantidad, PEDIDOS.fecha 
    FROM PLATOS
    LEFT JOIN PEDIDOS ON PLATOS.id = PEDIDOS.plato_id;
    """
)
for row in cursor:
    print(row)



# Confirmar cambios
conn.commit()

# Cerrar conexión
conn.close()