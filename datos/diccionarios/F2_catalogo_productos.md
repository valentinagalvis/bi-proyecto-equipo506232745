# Diccionario F2 – Catálogo de productos (sintética)

- **Archivo:** `datos/raw/catalogo_productos.xlsx`
- **Origen:** conjunto **sintético** que representa el maestro de productos del ERP interno.
- **Formato:** Excel (.xlsx), una hoja
- **Registros:** 46 filas (40 productos + 6 SKU duplicados)
- **Vigencia:** corte 2024
- **Rol en el modelo:** dimensión Producto

| Campo | Tipo | Descripción | Ejemplo | Problema de calidad |
|---|---|---|---|---|
| id_producto | Texto | Identificador del producto / SKU (llave) | `P0007` | **SKU duplicados** (6 casos: `P0021` aparece dos veces) |
| nombre_producto | Texto | Nombre comercial | `Pechuga de pollo` | Espacios sobrantes (6 casos: `Lenteja 500g  `) |
| categoria | Texto | Categoría comercial | `CARNES` | 15 variantes por may/min y espacios (`procesados`, `  VERDURAS Y HORTALIZAS `) |
| grupo | Texto | Grupo de alimento (alineado a SIPSA/F4) | `CARNES` | — |
| marca | Texto | Marca del producto | `Alpina` | Valores **nulos** (6 registros) |
| unidad_medida | Texto | Unidad de venta | `kg` | — |
| costo_referencia | Decimal (COP) | Costo de reposición de referencia | `13796` | Número guardado como **texto** con separador (8 casos: `2.218,00`) |

## Otros problemas de calidad del archivo
- La duplicidad de SKU rompe la unicidad de la llave; hay que deduplicar antes de usarla como dimensión.
- `costo_referencia` sirve para validar el `costo_unitario` de F1 y para contrastar con el precio mayorista de F4.
