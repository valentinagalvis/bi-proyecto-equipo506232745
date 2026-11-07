# Proceso ETL (Pentaho Data Integration)

## Motor y herramientas
| Componente | Versión |
|---|---|
| Base de datos | MySQL Community Server 8.0 (local) |
| ETL | Pentaho Data Integration (PDI) CE 9.4.0.0-343 |
| Driver JDBC | MySQL Connector/J 8.4.0 (`data-integration/lib/mysql-connector-j-8.4.0.jar`) |
| Java | JDK 24 (el que usa `Spoon.bat` / `Kitchen.bat`) |

## Parámetros de conexión (sin contraseñas)
Todas las transformaciones y el trabajo usan la conexión `dw_alianza`, definida con variables. Las variables se configuran en el archivo `kettle.properties` del usuario (`C:\Users\<usuario>\.kettle\kettle.properties`), **que no se sube al repositorio**:

```properties
DB_HOST=localhost
DB_PORT=3307          # puerto de la instalación local; por defecto MySQL usa 3306
DB_NAME=dw_alianza
DB_USER=bi_alianza
DB_PASS=<contraseña del usuario bi_alianza>
```

La conexión es de tipo *Generic database* con URL `jdbc:mysql://${DB_HOST}:${DB_PORT}/${DB_NAME}?useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=America/Bogota&rewriteBatchedStatements=true` y driver `com.mysql.cj.jdbc.Driver`.

Antes de la primera ejecución se crean la base y el usuario como `root` (una sola vez):

```sql
CREATE DATABASE dw_alianza CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
CREATE USER 'bi_alianza'@'localhost' IDENTIFIED BY '<contraseña>';
GRANT ALL PRIVILEGES ON dw_alianza.* TO 'bi_alianza'@'localhost';
```

## Ubicación esperada de las fuentes
Las rutas son relativas al archivo `.ktr` (`${Internal.Entry.Current.Directory}/../../datos/raw/`), así que basta clonar el repositorio completo:

| Fuente | Archivo | Formato |
|---|---|---|
| F1 Ventas POS | `datos/raw/ventas_pos.csv` | CSV |
| F2 Catálogo de productos | `datos/raw/catalogo_productos.xlsx` (hoja `catalogo`) | Excel |
| F3 Programa de fidelización | `datos/raw/fidelizacion.json` | JSON |
| F4 SIPSA precios mayoristas | `datos/raw/sipsa_precios_mayoristas_2013_2017.xlsx` (hoja `precios_mayoristas`) | Excel |

Las fuentes se leen tal como están; ninguna se limpia a mano antes de PDI.

## Orden de ejecución
El trabajo `etl/trabajos/j_carga_dw.kjb` hace la carga completa sobre una base vacía:

1. `00 reset modelo` … `06 crear stg_sipsa_precio`: ejecuta los scripts de `dw/ddl/` (borra y crea las tablas).
2. `07 poblar dim_tiempo`: llena la dimensión de tiempo del 2023-01-01 al 2024-12-31 (731 días).
3. `t_dim_producto.ktr` → `dim_producto` (F2).
4. `t_dim_sede.ktr` → `dim_sede` (sedes distintas de F1).
5. `t_dim_cliente.ktr` → `dim_cliente` (F3).
6. `t_stg_sipsa.ktr` → `stg_sipsa_precio` (F4, referencia mensual fuera de la tabla de hechos).
7. `t_fact_ventas.ktr` → `fact_ventas` (F1, al final porque busca las llaves de las dimensiones).

Ejecución desde Spoon: abrir `j_carga_dw.kjb` y pulsar *Run*. Desde consola (Windows):

```bat
cd <ruta>\pdi-ce-9.4.0.0-343\data-integration
Kitchen.bat /file:"<ruta_repo>\etl\trabajos\j_carga_dw.kjb" /level:Basic
```

Después de la carga se validan los resultados con las consultas de `dw/conciliacion/`.

## Transformaciones y reglas de limpieza
| Archivo | Fuente | Pasos de limpieza (nombre del paso en PDI) |
|---|---|---|
| `t_dim_producto.ktr` | F2 (Excel) | `dedup_sku`, `normaliza_categoria`, `recorta_espacios_nombre`, `marca_nula_sin_marca`, `costo_texto_a_numero` |
| `t_dim_sede.ktr` | F1 (CSV) | `normaliza_ciudad`, `sedes_distintas`, `deriva_nombre_y_region` |
| `t_dim_cliente.ktr` | F3 (JSON) | `dedup_id_cliente`, `normaliza_activo`, `normaliza_fecha_inscripcion`, `normaliza_ciudad`, `segmento_nulo_sin_segmento`, `valida_email`, `puntos_texto_a_entero` |
| `t_stg_sipsa.ktr` | F4 (Excel) | `precio_texto_a_numero`, `normaliza_fecha_mes`, `normaliza_grupo_y_producto`, `separa_ciudad_mercado`, `elimina_duplicados_exactos` |
| `t_fact_ventas.ktr` | F1 (CSV) | `elimina_duplicados_exactos`, `normaliza_fecha`, `precio_texto_a_numero`, `costo_texto_a_numero`, `unidades_negativas_a_positivas`, `filtra_precio_nulo` (rechazos a `rechazo_precio_nulo`), `cliente_vacio_no_fidelizado`, búsqueda de llaves `busca_sk_producto` / `busca_sk_sede` / `busca_sk_cliente`, `calcula_metricas` |

Las ventas sin cliente (venta anónima) y cualquier llave que no exista en su dimensión se asignan al miembro `-1` de la dimensión ("No fidelizado" / "Desconocido").
