# Diccionario F1 – SIPSA Precios mayoristas (mensual 2013–2017)

- **Archivo:** `datos/raw/sipsa_precios_mayoristas_mensual_2013_2017.csv`
- **Entidad:** DANE – SIPSA, componente de precios mayoristas (SIPSA-P)
- **Formato:** CSV, separador `;`, codificación Latin-1 (ISO-8859-1), fin de línea CRLF
- **Registros:** 281.386 (una fila = precio de un producto en un mercado mayorista en un mes)
- **Periodo:** enero de 2013 a diciembre de 2017 (60 meses)
- **Cobertura:** 376 productos, 8 grupos, 97 mercados

| Campo | Tipo | Descripción | Ejemplo | Problema de calidad |
|---|---|---|---|---|
| Fecha | Texto (fecha d/mm/aaaa) | Mes de la cotización. Siempre es el día 1 del mes | `1/01/2013` | Viene como texto en formato d/mm/aaaa, sin cero inicial en el día; hay que convertirlo a fecha. El día no tiene significado (todo es "1") |
| Grupo | Texto | Grupo de alimentos al que pertenece el producto | `FRUTAS` | Tres productos aparecen en dos grupos distintos: `Arveja enlatada`, `Fríjol enlatado` y `Maíz enlatado` figuran como `GRANOS Y CEREALES` y como `PROCESADOS` |
| Producto | Texto | Nombre del producto cotizado. No trae código | `Alas de pollo con costillar` | No hay código de producto, solo el nombre; la unión con otras fuentes depende del texto. Con Latin-1 leído como UTF-8, las tildes se dañan (`Fr�jol`) |
| Fuente | Texto | Mercado mayorista donde se tomó el precio, con la ciudad en el mismo campo | `Bogotá, D.C., Corabastos` | Mezcla ciudad y mercado en un solo campo, con comas internas (`Bogotá, D.C., …`). Algunos mercados traen comillas dentro (`Medellín, Plaza Minorista "José María Villa"`, 6.580 filas) y otros son solo el municipio y el departamento entre paréntesis, sin mercado (`Tuluá (Valle del Cauca)`) |
| Precio | Entero | Precio mayorista promedio del mes, en pesos colombianos (COP) | `3073` | La unidad (kilo, unidad, etc.) no viene en el archivo: `Huevo rojo extra` vale `229` (por unidad) y `Merluza, filete importado` vale `9667` (por kilo). Hay valores atípicos para revisar, por ejemplo `Cilantro` en `Bucaramanga, Centroabastos` en `1/05/2016` vale `11387`, cinco veces la mediana del producto (`2238`) |

## Otros problemas de calidad del archivo

- **Series incompletas:** de 5.973 combinaciones producto–mercado, solo 3.253 tienen los 60 meses completos.
- **Mercados que entran y salen:** el número de mercados cambia por año (79 en 2013, 77 en 2014, 85 en 2015 y 2016, 77 en 2017).
- **Codificación:** el archivo está en Latin-1; si se abre como UTF-8, `Bogotá` aparece como `Bogot�`.
- No tiene nulos ni filas duplicadas.
