# Diccionario F3 – Programa de fidelización (sintética)

- **Archivo:** `datos/raw/fidelizacion.json`
- **Origen:** conjunto **sintético** que representa la exportación del CRM del programa de fidelización.
- **Formato:** JSON (lista de objetos)
- **Registros:** 2.025 (2.000 clientes + 25 IDs duplicados)
- **Periodo:** altas 2019–2024
- **Rol en el modelo:** dimensión Cliente · **Datos personales → Ley 1581/2012**

| Campo | Tipo | Descripción | Ejemplo | Problema de calidad |
|---|---|---|---|---|
| id_cliente | Texto | Identificador del cliente (llave) | `C00482` | **IDs duplicados** (25 registros repetidos) |
| nombre | Texto | Nombre del titular | `Camila Gómez` | — |
| ciudad | Texto | Ciudad de residencia | `Medellín` | May/min inconsistentes (252 casos: `medellín`) |
| segmento | Texto | Nivel del programa | `Oro` | Valores **nulos** (133 registros) |
| email | Texto | Correo de contacto | `camila12@correo.com` | Correos **sin `@`** (160 registros: `isabela781correo.com`) |
| telefono | Texto | Teléfono de contacto | `3001234567` | Formatos inconsistentes (`(57) 3961685926`, truncados, con texto) |
| fecha_inscripcion | Texto (fecha) | Fecha de alta en el programa | `2022-05-10` | Formatos mezclados (62 no ISO: `10/05/2022`, `10-may-22`) |
| activo | Booleano | Estado de la membresía | `true` | **9 representaciones** distintas: `0`, `1`, `False`, `N`, `Sí`, `True`, `no`, `si`, `true` |
| puntos | Entero | Puntos acumulados | `12500` | A veces almacenado como texto |

## Otros problemas de calidad del archivo
- El campo `activo` necesita un mapeo explícito a booleano (`Sí/si/1/true/True` → verdadero; `no/0/N/False` → falso).
- Al contener datos personales, el tratamiento debe cumplir la Ley 1581 de 2012 (finalidad, autorización y seguridad).
