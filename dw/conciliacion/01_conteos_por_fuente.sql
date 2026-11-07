-- Conciliación de conteos: registros cargados en el DW por fuente.
-- Los leídos y descartados salen de las métricas de pasos de PDI (log de j_carga_dw.kjb).
-- Debe cumplirse: leídos = cargados + descartados.
USE dw_alianza;

-- F1 ventas_pos.csv → fact_ventas   (leídos 16.900 = cargados 16.275 + 295 duplicados exactos + 330 precio nulo)
SELECT 'F1 ventas_pos.csv' AS fuente, COUNT(*) AS cargados FROM fact_ventas;

-- F2 catalogo_productos.xlsx → dim_producto   (leídos 46 = cargados 40 + 6 SKU duplicados); se excluye el miembro -1
SELECT 'F2 catalogo_productos.xlsx' AS fuente, COUNT(*) AS cargados FROM dim_producto WHERE sk_producto > 0;

-- F3 fidelizacion.json → dim_cliente   (leídos 2.025 = cargados 2.000 + 25 id_cliente duplicados); se excluye el miembro -1
SELECT 'F3 fidelizacion.json' AS fuente, COUNT(*) AS cargados FROM dim_cliente WHERE sk_cliente > 0;

-- F1 → dim_sede   (16.900 filas leídas, 4 sedes distintas)
SELECT 'F1 → dim_sede' AS fuente, COUNT(*) AS cargados FROM dim_sede WHERE sk_sede > 0;

-- F4 sipsa_precios_mayoristas_2013_2017.xlsx → stg_sipsa_precio   (leídos 295.481 = cargados + duplicados exactos)
SELECT 'F4 SIPSA' AS fuente, COUNT(*) AS cargados FROM stg_sipsa_precio;
