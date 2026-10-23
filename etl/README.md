# Documentación del proceso ETL (Pentaho Data Integration)

El ETL se implementa en **Pentaho Data Integration (PDI / Kettle)**. Una transformación `.ktr` por fuente deja los datos limpios en el área de *staging*; un trabajo `.kjb` orquesta el orden y la carga al Data Warehouse en PostgreSQL.

## Transformaciones (`etl/transformaciones/`)
| Archivo | Fuente | Limpieza principal |
|---|---|---|
| `t_f1_ventas_pos.ktr` | F1 Ventas POS (.csv) | Unificar formato de fecha; convertir precio/costo (quitar `$` y separadores); corregir unidades negativas; estandarizar ciudad y categoría; quitar duplicados |
| `t_f2_catalogo.ktr` | F2 Catálogo (.xlsx) | Deduplicar SKU; convertir costo a número; estandarizar categoría; recortar espacios; resolver marca nula |
| `t_f3_fidelizacion.ktr` | F3 Fidelización (.json) | Deduplicar id_cliente; mapear `activo` a booleano; validar email; unificar fecha; normalizar ciudad |
| `t_f4_sipsa.ktr` | F4 SIPSA (.xlsx) | Unificar fecha; convertir precio a número; estandarizar grupo y plaza; separar ciudad/mercado; quitar duplicados |

## Trabajo (`etl/trabajos/`)
`j_carga_dw.kjb`: ejecuta las cuatro transformaciones → carga dimensiones (Tiempo, Producto, Sede, Cliente) → carga la tabla de hechos → corre las consultas de conciliación de `dw/conciliacion/`.

## Orden de ejecución
1. Dimensiones: Tiempo, Producto (F2), Sede, Cliente (F3).
2. Hechos: Ventas (F1), enriquecido con `precio_mayorista_ref` desde F4.
3. Conciliación: conteos y totales por fuente contra el origen.
