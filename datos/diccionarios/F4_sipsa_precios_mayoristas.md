# Diccionario F4 – SIPSA Precios mayoristas (REAL, mensual 2013–2017)

- **Archivo:** `datos/raw/sipsa_precios_mayoristas_2013_2017.xlsx`
- **Origen:** **datos públicos reales** del DANE – SIPSA, componente de precios mayoristas (SIPSA-P). Versión con problemas de calidad inyectados por el equipo para la práctica de limpieza.
- **Ficha:** https://www.datos.gov.co/dataset/Sistema-de-Informaci-n-de-Precios-y-Abastecimiento/gkqq-k3k5
- **Formato:** Excel (.xlsx) · también disponible en CSV/JSON/API en el portal
- **Registros:** 281.386 en la base limpia (una fila = precio de un producto en un mercado mayorista en un mes)
- **Periodo:** enero 2013 a diciembre 2017 (60 meses) · **Cobertura:** 376 productos, 8 grupos, 97 mercados
- **Licencia:** Creative Commons Atribución-CompartirIgual 4.0 (CC BY-SA 4.0)
- **Rol en el modelo:** fuente externa de referencia de costos de abastecimiento (métrica `precio_mayorista_ref`)

| Campo | Tipo | Descripción | Ejemplo | Problema de calidad |
|---|---|---|---|---|
| Fecha | Texto (fecha) | Mes de la cotización (día 1 del mes) | `2016-07-01` | Texto en **tres formatos** (`2016-07-01`, `01/07/2016`, `01-jul-16`); 17.602 celdas |
| Grupo | Texto | Grupo de alimentos (8 reales) | `CARNES` | May/min y espacios: 8 categorías aparecen como **24 variantes** (`carnes`, `  CARNES `) |
| Producto | Texto | Nombre del producto (no trae código) | `Alas de pollo con costillar` | Espacios sobrantes y mayúsculas sostenidas (5.850 filas); la unión con F2 depende del texto |
| Fuente | Texto | Mercado mayorista con la ciudad en el mismo campo | `Bogotá, D.C., Corabastos` | May/min inconsistentes (5.786 filas: `bogotá, d.c., corabastos`); mezcla ciudad y mercado con comas internas |
| Precio | Decimal (COP) | Precio mayorista promedio del mes (incluye IVA) | `3073` | Texto con moneda/separador (17.762 casos: `$ 9.967`, `9.833,00`). La unidad (kilo/unidad) no viene en el archivo |

## Otros problemas de calidad del archivo
- **Duplicados:** 14.095 filas duplicadas exactas (la base limpia no tiene).
- **Rango de precios:** de 82 a 89.556 COP; hay atípicos que conviene revisar.
- **Nota de integración:** es la única fuente real; se usa como referencia de costo por producto–ciudad–mes, no como tabla de hechos.
