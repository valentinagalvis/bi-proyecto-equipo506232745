# Diccionario F3 – DIVIPOLA Códigos de municipios

- **Archivo:** `datos/raw/divipola_municipios.json`
- **Entidad:** DANE, publicado en el Portal de Datos Abiertos (datos.gov.co, conjunto `gdxc-w37w`)
- **Formato:** JSON (lista de objetos), obtenido por la API Socrata
- **Registros:** 1.122 municipios
- **Vigencia:** catálogo actualizado en enero de 2025

| Campo | Tipo | Descripción | Ejemplo | Problema de calidad |
|---|---|---|---|---|
| cod_dpto | Texto (2 dígitos) | Código DANE del departamento | `05` | Es texto con cero inicial; si se convierte a número se pierde el `0` (`05` → `5`) |
| dpto | Texto | Nombre del departamento, en mayúsculas | `ANTIOQUIA` | En mayúsculas y con tildes, distinto a como lo escribe F1 (`Antioquia` entre paréntesis) |
| cod_mpio | Texto (5 dígitos) | Código DANE del municipio (llave natural) | `05001` | Mismo riesgo del cero inicial que `cod_dpto` |
| nom_mpio | Texto | Nombre oficial del municipio, en mayúsculas | `MEDELLÍN` | **No coincide con F1/F2:** Cali aparece como `SANTIAGO DE CALI` y Bogotá como `BOGOTÁ, D.C.`. **Nombres repetidos:** hay municipios con el mismo nombre en distintos departamentos (`ARMENIA`, `BARBOSA`, `CALDAS`, `CONCORDIA`…), así que el nombre solo no basta para unir con F1 (`Armenia, Mercar`) |
| tipo_municipio | Texto | Tipo de entidad territorial | `Municipio` | — |
| longitud | Texto | Longitud geográfica del centro del municipio | `-75,581775` | Número guardado como texto con coma decimal; hay que reemplazar la coma por punto y convertirlo |
| latitud | Texto | Latitud geográfica del centro del municipio | `6,246631` | Igual que `longitud` |
