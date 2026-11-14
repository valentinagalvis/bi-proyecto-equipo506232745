-- Extracción del conjunto de datos para el modelo predictivo (Entrega 3).
-- Une la tabla de hechos con las dimensiones de tiempo, sede y producto y agrega
-- las ventas por semana (lunes a domingo), sede y categoría de producto.
-- No filtra filas: toma todo el periodo cargado en el DW (2023-01-01 a 2024-12-31).
SELECT
    DATE_SUB(t.fecha, INTERVAL WEEKDAY(t.fecha) DAY) AS semana_inicio,   -- lunes de la semana
    s.sk_sede,
    s.ciudad,
    p.categoria,
    SUM(f.valor_venta)  AS ventas_netas,
    SUM(f.unidades)     AS unidades,
    COUNT(*)            AS lineas
FROM fact_ventas f
JOIN dim_tiempo   t ON t.sk_tiempo   = f.sk_tiempo
JOIN dim_sede     s ON s.sk_sede     = f.sk_sede
JOIN dim_producto p ON p.sk_producto = f.sk_producto
GROUP BY semana_inicio, s.sk_sede, s.ciudad, p.categoria
ORDER BY semana_inicio, s.sk_sede, p.categoria;
