# Diccionario F2 – SIPSA Abastecimiento (series históricas 2013–2026)

- **Archivo:** `datos/raw/sipsa_abastecimiento_series_historicas_2013_2026.xlsx`
- **Entidad:** DANE – SIPSA, componente de abastecimiento de alimentos (SIPSA-A)
- **Formato:** Excel (.xlsx) con 4 hojas: `Índice`, `1. F.Metodológica`, `2. Serie mensual`, `3. Serie semanal`
- **Hoja usada principalmente:** `2. Serie mensual`. Encabezado en la fila 10; datos desde la fila 11
- **Registros:** 165 meses (enero de 2013 a septiembre de 2026) × 32 mercados
- **Unidad:** toneladas (según el título de la hoja)

## Hoja `2. Serie mensual`

| Campo | Tipo | Descripción | Ejemplo | Problema de calidad |
|---|---|---|---|---|
| Fecha | Fecha | Mes del abastecimiento (día 1 del mes) | `2013-01-01` | Al final de la columna hay dos filas que no son datos: `Fuente: DANE-SIPSA.` y `Fecha de actualización: 2 de octubre de 2026` |
| TOTAL ABASTECIMIENTO | Decimal | Toneladas que ingresaron en el mes, sumando todos los mercados | `371651.20048` | Es un total precalculado: si se suma en el cubo junto con los mercados se cuenta dos veces |
| Variación Mensual del Abastecimiento | Decimal | Cambio frente al mes anterior | `-0.10793548652120821` | Es una proporción (−0,108 = −10,8 %), no un porcentaje. Vacía en 10 de los 165 meses (p. ej. `2013-01`, `2013-09`, `2015-03`). No es aditiva |
| Variación Anual del Abastecimiento | Decimal | Cambio frente al mismo mes del año anterior | `0.0033662118802331165` (`2014-09`) | Vacía en 79 de los 165 meses (desde `2013-01` hasta `2014-08` y otros periodos hasta `2024-01`). Proporción, no porcentaje. No es aditiva |
| EMPALME - Total abastecimiento mercados anteriores | Decimal | Total calculado solo con los mercados que existían antes de ampliar la cobertura | (vacío en `2013-01`) | Vacía en 94 de los 165 meses. Mezcla en la misma tabla dos coberturas distintas de mercados |
| EMPALME - Variación anual mercados anteriores | Decimal | Variación anual del total anterior | (vacío en `2013-01`) | Vacía en 98 de los 165 meses |
| *(una columna por mercado, 32 en total)*, p. ej. `Bogotá, D.C., Corabastos` | Decimal | Toneladas que ingresaron a ese mercado en el mes | `139557.1342` | **Formato ancho:** cada mercado es una columna y hay que despivotar la tabla. **Celdas vacías:** 1.511 en total (p. ej. `Florencia (Caquetá)`, `Pereira, La 41-Impala` y `Tibasosa (Boyacá), Coomproriente` no tienen dato en 121 meses). **Nombres que no coinciden con F1:** 6 de 32 mercados se escriben distinto, p. ej. `Medellín, Plaza Minorista José María Villa` (sin comillas) frente a `Medellín, Plaza Minorista "José María Villa"` en F1 |

## Hoja `3. Serie semanal`

| Campo | Tipo | Descripción | Ejemplo | Problema de calidad |
|---|---|---|---|---|
| CIUDAD | Texto | Ciudad o grupo de mercados | `Cali, Cavasa y Santa Helena` | Agrupa varios mercados en un solo nombre, distinto a la hoja mensual. Error de digitación: `Plaza Sampez Mendoza` en vez de `Samper Mendoza`. Las filas del total nacional tienen la ciudad vacía |
| GRUPO | Texto | Grupo de alimentos | `FRUTAS` | Solo 4 grupos (`FRUTAS`, `TUBERCULOS, RAICES Y PLATANOS`, `VERDURAS Y HORTALIZAS`, `OTROS GRUPOS`) frente a 8 en F1; carnes, lácteos, granos y procesados quedan juntos en `OTROS GRUPOS`. Incluye filas de subtotal (`Total`, `TOTAL GENERAL`) |
| *(una columna por semana)*, p. ej. ` 5-11 ene 2013` | Decimal | Toneladas en esa semana | `19741.247` | Formato ancho (más de 700 columnas). El encabezado de la semana es texto con espacio inicial y rangos que cruzan meses (` 26-1 feb 2013`) |
