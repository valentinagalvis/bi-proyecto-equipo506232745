# Diccionario F1 – Ventas POS (sintética, 2023–2024)

- **Archivo:** `datos/raw/ventas_pos.csv`
- **Origen:** conjunto **sintético** que representa el sistema POS interno de Supermercados Alianza (no hay acceso a datos transaccionales reales de la empresa ficticia).
- **Formato:** CSV, separador `,`, codificación UTF-8
- **Registros:** 16.900 (16.605 válidos + 295 duplicados exactos inyectados)
- **Periodo:** enero 2023 a diciembre 2024 (grano diario)
- **Cobertura:** 4 sedes (Bogotá, Medellín, Cali, Barranquilla), 40 productos, 8 categorías
- **Rol en el modelo:** tabla de hechos (Hechos_Ventas)

| Campo | Tipo | Descripción | Ejemplo | Problema de calidad |
|---|---|---|---|---|
| id_venta | Texto | Identificador único de la transacción POS | `V0000123` | — |
| fecha | Texto (fecha) | Fecha de la venta | `2024-03-15` | Viene como texto en **tres formatos mezclados** (`2024-03-15`, `15/03/2024`, `15-mar-24`); 1.184 filas en formato no ISO. Evidencia directa del síntoma S1 |
| id_sede | Texto | Código de la sede | `S01` | — |
| ciudad | Texto | Ciudad de la sede | `Bogotá` | May/min inconsistentes (`bogotá`); 1.674 filas |
| id_producto | Texto | Llave foránea al catálogo (F2) | `P0007` | — |
| categoria | Texto | Categoría del producto (redundante con F2) | `CARNES` | 24 variantes por may/min y espacios (`frutas`, `  PESCADOS `) |
| unidades | Entero | Unidades vendidas en la línea | `4` | Valores **negativos** por devoluciones mal registradas (538 filas); a veces texto |
| precio_unitario | Decimal (COP) | Precio de venta unitario | `20640` | Texto con símbolo de moneda (1.981: `$ 20.640`) y **nulos** (330 filas) |
| costo_unitario | Decimal (COP) | Costo unitario de la mercancía | `13796` | Texto con coma decimal (1.309: `13.796,00`) |
| id_cliente | Texto | FK al cliente fidelizado (F3); vacío si venta anónima | `C00482` | Vacío **legítimo** en 9.360 filas (no fidelizado) — no confundir con nulo por error |
| canal | Texto | Canal de venta | `Tienda física` | — |

## Otros problemas de calidad del archivo
- **Duplicados:** 295 filas duplicadas exactas.
- **Mezcla de tipos:** fecha, precio y costo conviven como número y como texto en la misma columna; hay que normalizarlos antes de cargar.
- **Dependencia funcional rota:** `categoria` debería derivarse de `id_producto` (F2), pero aquí llega escrita a mano y con variantes.
