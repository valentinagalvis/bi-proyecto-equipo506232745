# bi-proyecto-equipo506232745

**Proyecto final de Business Intelligence — Entrega 1**
Diseño de la Solución de BI para **Supermercados Alianza Colombia S.A.**
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
ETL: **Pentaho Data Integration (PDI)** · Almacén: **PostgreSQL** · Visualización: **Power BI / Metabase** · Versionado: GitHub. Todas gratuitas / open-source.

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
1. Descargar F4 (ver `datos/descarga.md`); F1–F3 ya están versionadas en `datos/raw/`.
2. Ejecutar las transformaciones de `etl/` (Pentaho) para limpiar y cargar al DW.
3. Crear el esquema con `dw/ddl/` y validar con `dw/conciliacion/`.
4. Conectar el dashboard al DW.
