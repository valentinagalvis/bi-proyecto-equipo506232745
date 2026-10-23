# Registro de Fuentes

El proyecto usa **cuatro fuentes en tres formatos**. Solo **F4 (SIPSA)** es un dato público real; **F1, F2 y F3 son conjuntos sintéticos** que representan las fuentes internas de la empresa (ventas POS, catálogo y fidelización), generados a partir del caso. Se tomó esta decisión porque no era viable correlacionar varias fuentes abiertas reales (precios, abastecimiento y códigos geográficos) en un caso de ventas de supermercado. Los archivos de `datos/raw/` conservan los problemas de calidad; las muestras de 20 filas están en `datos/muestras/` y los diccionarios en `datos/diccionarios/`.

| Fuente | Archivo en `datos/raw/` | Formato | Registros | Periodo | Tipo | Licencia |
|---|---|---|---|---|---|---|
| F1 Ventas POS | `ventas_pos.csv` | CSV (UTF-8) | 16.900 | 2023-01 a 2024-12 | Sintética (hechos) | Interna / uso académico |
| F2 Catálogo de productos | `catalogo_productos.xlsx` | Excel (.xlsx) | 46 | Corte 2024 | Sintética (dim producto) | Interna / uso académico |
| F3 Programa de fidelización | `fidelizacion.json` | JSON | 2.025 | Altas 2019-2024 | Sintética (dim cliente) | Interna / uso académico (Ley 1581/2012) |
| F4 SIPSA – Precios mayoristas | `sipsa_precios_mayoristas_2013_2017.xlsx` | Excel (.xlsx) | 281.386 | 2013-01 a 2017-12 | **REAL (DANE)** | CC BY-SA 4.0 |

---

## F1, F2 y F3 — Fuentes internas (sintéticas)

Representan los sistemas operativos de Supermercados Alianza: el POS (ventas), el ERP (catálogo de productos y costos) y el CRM del programa de fidelización. Se generaron con un script reproducible (semilla fija) y se les inyectaron problemas de calidad reales y verificables (duplicados, fechas y montos como texto en varios formatos, may/min inconsistentes, nulos, booleanos no estandarizados, SKU repetidos, correos inválidos). Cada ejemplo de los diccionarios corresponde a un dato que sí existe en el archivo. Detalle de campos y problemas en `datos/diccionarios/F1_ventas_pos.md`, `F2_catalogo_productos.md` y `F3_fidelizacion.md`.

## F4 — SIPSA Componente de Precios Mayoristas (SIPSA-P) — REAL

- **Entidad:** Departamento Administrativo Nacional de Estadística (DANE).
- **Contenido:** precio mayorista mensual (COP) de 376 productos agroalimentarios en 97 mercados mayoristas.
- **Ficha en datos.gov.co:** https://www.datos.gov.co/dataset/Sistema-de-Informaci-n-de-Precios-y-Abastecimiento/gkqq-k3k5/about_data
- **Descarga directa (zip):** https://microdatos.dane.gov.co/index.php/catalog/776/download/23898
- **Pasos para obtenerla:**
  1. Abrir la ficha de datos.gov.co o el catálogo 776 de microdatos del DANE.
  2. Descargar `BaseDatos-SIPSA_P-Mensual-2013_2017.zip` (≈15 MB).
  3. Del zip se usa `Mensual_2013_2017`. El equipo le inyectó problemas de calidad para la práctica de limpieza y lo guardó como `sipsa_precios_mayoristas_2013_2017.xlsx`.
- **Columnas:** `Fecha, Grupo, Producto, Fuente, Precio`.
- **Licencia:** Creative Commons Atribución-CompartirIgual 4.0.

> Nota: se descartaron las fuentes reales SIPSA-Abastecimiento y DIVIPOLA que se habían explorado antes, porque no se correlacionaban con el proceso de ventas del caso. SIPSA-Precios se conserva como la única fuente real, en rol de referencia de costos.
