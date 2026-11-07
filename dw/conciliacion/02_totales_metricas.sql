-- Conciliación de totales: métricas de la tabla de hechos en el DW.
-- Se comparan con el total calculado sobre ventas_pos.csv aplicando las mismas reglas
-- (sin duplicados exactos, sin precio nulo, unidades en valor absoluto, montos de texto convertidos a número).
USE dw_alianza;

SELECT COUNT(*)                     AS lineas,
       SUM(unidades)                AS total_unidades,       -- fuente: 170.273
       ROUND(SUM(valor_venta), 2)   AS total_valor_venta,    -- fuente: 5.244.619.720,00
       ROUND(SUM(costo_total), 2)   AS total_costo,          -- fuente: 3.884.859.012,00
       ROUND(SUM(margen_bruto), 2)  AS total_margen_bruto
FROM fact_ventas;

-- Total por sede (para comparar con la fuente agrupada por id_sede)
SELECT s.id_sede, s.ciudad, COUNT(*) AS lineas, ROUND(SUM(f.valor_venta), 2) AS valor_venta
FROM fact_ventas f JOIN dim_sede s ON s.sk_sede = f.sk_sede
GROUP BY s.id_sede, s.ciudad ORDER BY s.id_sede;
