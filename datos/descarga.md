# Registro de Descarga de Fuentes

Las tres fuentes son datos públicos reales; no se usan datos sintéticos. Los archivos de `datos/raw/` se guardan tal como se descargaron (sin limpiar); las muestras de 20 filas están en `datos/muestras/`.

| Fuente | Archivo en `datos/raw/` | Formato | Registros | Periodo | Fecha de descarga | Licencia |
|---|---|---|---|---|---|---|
| F1 SIPSA – Precios mayoristas | `sipsa_precios_mayoristas_mensual_2013_2017.csv` | CSV (`;`, Latin-1) | 281.386 | ene-2013 a dic-2017 (mensual) | 22/10/2026 | CC BY-SA 4.0 |
| F2 SIPSA – Abastecimiento | `sipsa_abastecimiento_series_historicas_2013_2026.xlsx` | Excel (.xlsx) | 165 meses × 32 mercados (hoja mensual) | ene-2013 a sep-2026 (mensual y semanal) | 22/10/2026 | Términos de uso DANE (cita obligatoria) |
| F3 DIVIPOLA – Códigos de municipios | `divipola_municipios.json` | JSON (API Socrata) | 1.122 | Vigente (actualizado ene-2025) | 22/10/2026 | CC BY-SA 4.0 |

---

## F1. SIPSA – Componente de Precios Mayoristas (SIPSA-P)

- **Entidad:** Departamento Administrativo Nacional de Estadística (DANE).
- **Contenido:** precio mayorista mensual (COP por kilo o unidad) de 376 productos agroalimentarios en 97 mercados mayoristas del país.
- **Ficha en datos.gov.co:** https://www.datos.gov.co/dataset/Sistema-de-Informaci-n-de-Precios-y-Abastecimiento/gkqq-k3k5/about_data
- **Descarga directa (zip):** https://microdatos.dane.gov.co/index.php/catalog/776/download/23898
- **Pasos para obtenerla:**
  1. Abrir la ficha de datos.gov.co o el catálogo 776 de microdatos del DANE.
  2. Descargar `BaseDatos-SIPSA_P-Mensual-2013_2017.zip` (15 MB).
  3. Del zip se usa solo `Mensual_2013_2017.csv` (los archivos `.xlsx`, `.dta` y `.sav` contienen los mismos datos en otros formatos). Se renombró a `sipsa_precios_mayoristas_mensual_2013_2017.csv` sin modificar su contenido.
- **Columnas:** `Fecha;Grupo;Producto;Fuente;Precio`.
- **Licencia:** Creative Commons Atribución-CompartirIgual 4.0 (según la ficha de datos.gov.co).

## F2. SIPSA – Componente de Abastecimiento (SIPSA-A)

- **Entidad:** DANE.
- **Contenido:** toneladas de alimentos que ingresan a los mercados mayoristas. Hoja `2. Serie mensual`: total por mercado y mes. Hoja `3. Serie semanal`: total por ciudad y grupo de alimentos por semana.
- **Página:** https://www.dane.gov.co/index.php/estadisticas-por-tema/agropecuario/sistema-de-informacion-de-precios-sipsa/componente-abastecimientos-1
- **Descarga directa:** https://www.dane.gov.co/files/operaciones/SIPSA/Series-historicas-abastecimiento-2013-2026.xlsx
- **Pasos para obtenerla:**
  1. Abrir la página del componente de abastecimientos del SIPSA.
  2. En la sección *Series históricas*, descargar "Series históricas componente abastecimiento (2013-2026)" (0,9 MB).
  3. Se renombró a `sipsa_abastecimiento_series_historicas_2013_2026.xlsx` sin modificar su contenido.
- **Nota:** el DANE actualiza este archivo periódicamente; la versión guardada dice "Fecha de actualización: 2 de octubre de 2026". Los microdatos por producto existen por año en la misma página, pero no se incluyen porque pesan entre 52 y 87 MB cada uno.
- **Licencia:** términos y condiciones del DANE (https://www.dane.gov.co/index.php/terrminos-y-condiciones-dane): se autoriza el uso, transformación y análisis citando "Fuente: Departamento Administrativo Nacional de Estadística: www.dane.gov.co".

## F3. DIVIPOLA – Códigos de municipios

- **Entidad:** DANE, publicado en el Portal de Datos Abiertos de Colombia.
- **Contenido:** división político-administrativa: código y nombre de departamento y municipio, tipo y coordenadas.
- **Ficha:** https://www.datos.gov.co/Mapas-Nacionales/DIVIPOLA-C-digos-municipios/gdxc-w37w
- **Endpoint API usado:** `https://www.datos.gov.co/resource/gdxc-w37w.json?$limit=5000&$order=cod_mpio`
- **Pasos para obtenerla:**

  ```bash
  curl -o datos/raw/divipola_municipios.json "https://www.datos.gov.co/resource/gdxc-w37w.json?\$limit=5000&\$order=cod_mpio"
  ```

- **Licencia:** Creative Commons Atribución-CompartirIgual 4.0.
