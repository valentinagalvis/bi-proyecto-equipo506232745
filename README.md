# bi-proyecto-equipo506232745

**Proyecto final de Business Intelligence — Entregas 1 y 2**
Solución de BI para **Supermercados Alianza Colombia S.A.**: diseño (Entrega 1) y construcción del data warehouse, ETL y tablero (Entrega 2).
Fundación Universitaria Konrad Lorenz · Docente: Leandro Pájaro Fuentes

## Integrantes
| Integrante | Código |
|---|---|
| Ángel Nicolas Ayala Ríos | 506232067 |
| Danna Valentina Galvis Sánchez | 506232745 |
| Yefry Esteban Ávila Zuluaga | 506232728 |

## Caso
Cadena retail con sedes en Bogotá, Medellín, Cali y Barranquilla, hoy en Fase 1 del BIMM (no existe BI). El proyecto diseña una solución para llevarla a la Fase 4 (Data Warehouse) con un modelo dimensional en estrella centrado en la venta POS.

## Fuentes
| ID | Fuente | Formato | Tipo |
|----|--------|---------|------|
| F1 | Ventas POS | CSV | Sintética (hechos) |
| F2 | Catálogo de productos | XLSX | Sintética (dim producto) |
| F3 | Programa de fidelización | JSON | Sintética (dim cliente) |
| F4 | SIPSA Precios mayoristas | XLSX | **REAL** — DANE (CC BY-SA 4.0) |

Una sola fuente real (F4); F1–F3 son sintéticas que representan las fuentes internas. Detalle en `datos/descarga.md`.

## Herramientas
ETL: **Pentaho Data Integration (PDI) 9.4** · Almacén: **MySQL 8.0** (base `dw_alianza`, modelo estrella) · Visualización: **Power BI Desktop** · Versionado: GitHub. Todas gratuitas.

En la Entrega 1 se propuso PostgreSQL; en la construcción se usó MySQL 8.0, el motor recomendado en el enunciado de la Entrega 2.

## Estructura
```
docs/entregas/      PDF y Word de cada entrega
docs/diagramas/     arquitectura y esquema estrella (PNG + .mmd editable)
datos/raw/          fuentes con problemas de calidad (sin limpiar)
datos/muestras/     20 filas por fuente
datos/diccionarios/ un diccionario por fuente
datos/descarga.md   origen, formato y licencia de cada fuente
dw/ddl/             scripts CREATE TABLE de dimensiones y hechos
dw/conciliacion/    consultas de conteo y totales por fuente
etl/transformaciones/  .ktr de Pentaho
etl/trabajos/          .kjb de Pentaho
dashboard/          .pbix o enlace publicado y capturas
modelo/             notebooks del modelo predictivo (entregas siguientes)
```

## Cómo reproducir
1. Clonar el repositorio. Las cuatro fuentes ya están en `datos/raw/` (origen de F4 en `datos/descarga.md`).
2. Instalar MySQL 8.0 y crear la base `dw_alianza` y el usuario `bi_alianza` (script en `etl/README.md`).
3. En Pentaho PDI 9.4, configurar las variables de conexión `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER` y `DB_PASS` en `kettle.properties` (ver `etl/README.md`; la contraseña nunca se sube al repositorio).
4. Ejecutar `etl/trabajos/j_carga_dw.kjb`: crea las tablas con `dw/ddl/`, pobla la dimensión de tiempo, carga las dimensiones y al final la tabla de hechos.
5. Validar la carga con las consultas de `dw/conciliacion/`.
6. Abrir `dashboard/` en Power BI Desktop y actualizar los datos contra la base `dw_alianza`.

## Modelo predictivo (Entrega 3)
Pronóstico de **ventas netas semanales por sede y categoría** (regresión). Carpeta `modelo/`:
- `extraccion.sql`: consulta al DW que agrega `fact_ventas` por semana, sede y categoría.
- `modelo_prediccion_ventas.ipynb`: exploración, preparación, regresión lineal vs árbol de decisión, evaluación (MAE, RMSE) y despliegue.
- `requirements.txt`: librerías y versiones. `figuras/`: gráficos que genera el notebook.

Para ejecutarlo:
1. Tener cargado el DW (`etl/trabajos/j_carga_dw.kjb`).
2. `pip install -r modelo/requirements.txt`
3. Definir las variables de entorno de conexión (la contraseña nunca va en el repo): `DB_PASS` (si no está definida, el notebook pide la contraseña al ejecutarse); `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER` opcionales (por defecto `localhost`, `3307`, `dw_alianza`, `bi_alianza`). En PowerShell: `$env:DB_PASS="..."`.
4. Desde la carpeta `modelo/`, abrir el notebook en Jupyter y ejecutar *Reiniciar y ejecutar todo*. Se usa Jupyter local (no Colab) porque el DW es un MySQL local al que Colab no puede conectarse.
5. El notebook crea (con `dw/ddl/08_pred_ventas_semana.sql`) y llena la tabla `pred_ventas_semana`. Para verlo en el tablero, abrir `dashboard/tablero_alianza.pbix`, pulsar **Actualizar** e ir a la página **Predicciones**.

## Resultado de la carga (Entrega 2)
| Tabla | Registros |
|---|---|
| `dim_tiempo` | 731 (2023-01-01 a 2024-12-31) |
| `dim_producto` | 40 + miembro "Desconocido" |
| `dim_sede` | 4 + miembro "Desconocida" |
| `dim_cliente` | 2.000 + miembro "No fidelizado" |
| `fact_ventas` | 16.275 líneas de venta |
| `stg_sipsa_precio` | 281.374 precios mayoristas (staging de referencia) |
