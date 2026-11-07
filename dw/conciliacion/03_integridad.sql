-- Controles de integridad del modelo cargado.
USE dw_alianza;

-- Hechos asignados a miembros especiales (-1). Producto y sede deben ser 0; cliente -1 = ventas no fidelizadas.
SELECT SUM(sk_producto = -1) AS producto_desconocido,
       SUM(sk_sede = -1)     AS sede_desconocida,
       SUM(sk_cliente = -1)  AS ventas_no_fidelizadas
FROM fact_ventas;

-- La dimensión de tiempo cubre sin huecos el periodo de los hechos (días esperados = días cargados).
SELECT MIN(fecha) AS desde, MAX(fecha) AS hasta,
       DATEDIFF(MAX(fecha), MIN(fecha)) + 1 AS dias_esperados, COUNT(*) AS dias_cargados
FROM dim_tiempo;

SELECT MIN(t.fecha) AS primera_venta, MAX(t.fecha) AS ultima_venta
FROM fact_ventas f JOIN dim_tiempo t ON t.sk_tiempo = f.sk_tiempo;
