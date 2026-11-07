-- Borra el modelo para recargarlo desde cero (base vacía). Orden: hechos primero, luego dimensiones.
USE dw_alianza;
DROP TABLE IF EXISTS fact_ventas;
DROP TABLE IF EXISTS stg_sipsa_precio;
DROP TABLE IF EXISTS dim_tiempo;
DROP TABLE IF EXISTS dim_producto;
DROP TABLE IF EXISTS dim_sede;
DROP TABLE IF EXISTS dim_cliente;
