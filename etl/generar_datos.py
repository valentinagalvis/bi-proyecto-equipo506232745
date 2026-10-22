"""
generar_datos.py - Generador de datos SINTETICOS
Proyecto final BI - Entrega 1 - Supermercados Alianza Colombia S.A.

DECLARACION: todos los datos que produce este script son sinteticos, generados
por el equipo con apoyo de IA. No representan informacion real de la empresa ni
de personas reales (nombres armados al azar a partir de listas genericas).

Salidas (ejecutar desde la raiz del repositorio):
  datos/raw/ventas_pos_<sede>.csv           F1 Ventas POS (un CSV por sede)
  datos/raw/catalogo_productos.xlsx         F2 Catalogo de productos (Excel)
  datos/raw/clientes_fidelizacion.json      F3 Programa de fidelizacion (JSON anidado)
  datos/muestras/muestra_*.csv              20 filas por archivo, en CSV (indicador F4)
  datos/registro_errores_inyectados.json    Errores de calidad metidos a proposito

Requisitos: pip install pandas numpy openpyxl
Uso:        python etl/generar_datos.py
"""
import json
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

# ---------------------------------------------------------------- configuracion
SEED = 42                                   # semilla fija -> datos reproducibles
rng = np.random.default_rng(SEED)

FECHA_INI, FECHA_FIN = "2024-01-01", "2025-12-31"   # 2 anios completos
DIR_RAW = Path("datos/raw")
DIR_MUESTRAS = Path("datos/muestras")
N_PRODUCTOS = 320
N_CLIENTES = 9000

# Cada sede exporta su POS a su manera (sintoma S1 del caso)
SEDES = [
    dict(id="BOG01", ciudad="Bogotá", base=60, fmt="%Y-%m-%d", sep=",", dec=".",
         archivo="ventas_pos_bogota.csv"),
    dict(id="MED01", ciudad="Medellín", base=45, fmt="%Y/%m/%d", sep=",", dec=".",
         archivo="ventas_pos_medellin.csv"),
    dict(id="CAL01", ciudad="Cali", base=38, fmt="%d/%m/%Y", sep=",", dec=".",
         archivo="ventas_pos_cali.csv"),
    dict(id="BAQ01", ciudad="Barranquilla", base=32, fmt="%m-%d-%Y", sep=";", dec=",",
         archivo="ventas_pos_barranquilla.csv"),
]

# categoria: (subcategorias, rango precio COP, rango margen, unidad, afinidad a promos, peso en ventas)
CATEGORIAS = {
    "Lácteos":            (["Leche", "Yogur", "Quesos", "Mantequilla"], (2500, 18000), (0.12, 0.22), "und", 1.0, 12),
    "Carnes y pescados":  (["Res", "Cerdo", "Pollo", "Pescado"], (9000, 45000), (0.15, 0.28), "kg", 0.8, 9),
    "Frutas y verduras":  (["Frutas", "Verduras", "Tubérculos"], (1500, 9000), (0.25, 0.40), "kg", 0.9, 11),
    "Granos y abarrotes": (["Arroz", "Granos", "Aceites", "Pastas", "Azúcar"], (2000, 25000), (0.08, 0.16), "und", 0.7, 14),
    "Panadería":          (["Pan", "Tortas", "Galletería"], (1500, 15000), (0.30, 0.45), "und", 0.6, 7),
    "Bebidas":            (["Gaseosas", "Jugos", "Agua", "Café"], (1800, 15000), (0.15, 0.25), "und", 1.3, 12),
    "Licores":            (["Cerveza", "Aguardiente", "Vino", "Ron"], (3500, 95000), (0.18, 0.30), "und", 1.2, 5),
    "Aseo hogar":         (["Detergentes", "Limpiadores", "Papel higiénico"], (3000, 40000), (0.15, 0.25), "und", 1.5, 9),
    "Cuidado personal":   (["Shampoo", "Jabón", "Crema dental", "Desodorante"], (3500, 30000), (0.20, 0.32), "und", 1.2, 8),
    "Snacks y dulces":    (["Paquetes", "Chocolates", "Dulces"], (1000, 12000), (0.22, 0.35), "und", 1.4, 8),
    "Mascotas":           (["Alimento perro", "Alimento gato", "Accesorios"], (5000, 80000), (0.18, 0.28), "und", 0.9, 5),
}
CATS = list(CATEGORIAS)
MARCAS = ["Alianza", "Del Campo", "La Sabana", "Andina", "Caribe", "Montaña Verde",
          "Valle Dorado", "Sierra", "Nativa", "Prado", "Cordillera", "Pacífico"]
PRESENT = {"und": ["x1", "250 g", "500 g", "1 kg", "400 ml", "1 L", "2 L", "x6", "x12"],
           "kg": ["granel"]}

# Patrones de demanda (para que el dashboard y el modelo predictivo tengan señal)
MES_F = np.array([0.92, 0.88, 0.95, 0.97, 1.00, 1.02, 1.03, 0.98, 0.96, 1.00, 1.08, 1.45])
DIA_F = np.array([0.85, 0.85, 0.90, 0.95, 1.10, 1.30, 1.15])          # lun..dom
HORAS = np.arange(7, 22)
HORA_P = np.array([2, 3, 4, 5, 6, 7, 6, 5, 5, 6, 8, 9, 8, 6, 3], float)
HORA_P /= HORA_P.sum()
CRECIMIENTO_ANUAL = 1.06
MEDIOS_PAGO = ["Efectivo", "Tarjeta débito", "Tarjeta crédito", "Billetera digital"]
MEDIOS_P = [0.35, 0.30, 0.20, 0.15]

VARIANTES_CIUDAD = {
    "Bogotá": ["BOGOTA", "Bogota D.C.", "bogotá"],
    "Medellín": ["MEDELLIN", "Medellin"],
    "Cali": ["CALI", "Santiago de Cali"],
    "Barranquilla": ["B/quilla", "BARRANQUILLA", "Barranquilla "],
}

NOMBRES_F = ["Camila", "Valentina", "Laura", "Daniela", "María", "Paula", "Natalia", "Juliana", "Carolina", "Alejandra"]
NOMBRES_M = ["Andrés", "Juan", "Santiago", "Carlos", "Luis", "Sebastián", "Diego", "Felipe", "Jorge", "David"]
APELLIDOS = ["Gómez", "Rodríguez", "Martínez", "López", "García", "Hernández", "Pérez", "Ramírez", "Torres", "Díaz",
             "Moreno", "Rojas", "Vargas", "Castro", "Ortiz", "Jiménez", "Ruiz", "Suárez", "Mejía", "Ospina"]

# ------------------------------------------------- registro de errores inyectados
registro = {}


def registrar(fuente, campo, problema, n, ejemplos):
    """Guarda cuántas filas se ensuciaron y ejemplos reales (sirve para la tabla 2.2)."""
    clave = f"{fuente} | {campo} | {problema}"
    r = registro.setdefault(clave, {"fuente": fuente, "campo": campo, "problema": problema,
                                    "filas_afectadas": 0, "ejemplos": []})
    r["filas_afectadas"] += int(n)
    r["ejemplos"] = (r["ejemplos"] + [str(e) for e in list(ejemplos)])[:5]


def sin_tildes(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def peso_categoria(cat, mes, ciudad):
    """Estacionalidad por categoría y ciudad."""
    w = CATEGORIAS[cat][5]
    if cat == "Licores":
        w *= {12: 2.2, 6: 1.2, 1: 1.2}.get(mes, 1.0)
    if cat in ("Carnes y pescados", "Panadería") and mes == 12:
        w *= 1.4
    if cat == "Bebidas" and ciudad == "Barranquilla":
        w *= 1.4
    if cat == "Aseo hogar" and mes in (1, 7):
        w *= 1.2
    return w


# ---------------------------------------------------------------- F2 catálogo
def generar_catalogo():
    pesos = np.array([CATEGORIAS[c][5] for c in CATS], float)
    n_cat = np.maximum(10, np.round(pesos / pesos.sum() * N_PRODUCTOS)).astype(int)
    filas, k = [], 1
    for cat, n in zip(CATS, n_cat):
        subs, (pmin, pmax), (mmin, mmax), unidad, _, _ = CATEGORIAS[cat]
        for _ in range(n):
            sub, marca = str(rng.choice(subs)), str(rng.choice(MARCAS))
            precio = int(round(rng.uniform(pmin, pmax) / 50) * 50)
            costo = int(round(precio * (1 - rng.uniform(mmin, mmax))))
            filas.append(dict(
                codigo_producto=f"P{k:05d}",
                descripcion=f"{sub} {marca} {rng.choice(PRESENT[unidad])}",
                categoria=cat, subcategoria=sub, marca=marca, unidad_medida=unidad,
                precio_venta=precio, costo_unitario=costo,
                proveedor=f"PRV{rng.integers(1, 41):03d}",
                estado="Descontinuado" if rng.random() < 0.03 else "Activo",
                fecha_creacion=(pd.Timestamp("2018-01-01")
                                + pd.Timedelta(days=int(rng.integers(0, 2190)))).strftime("%Y-%m-%d"),
            ))
            k += 1
    cat = pd.DataFrame(filas)
    cat["popularidad"] = rng.lognormal(0, 0.8, len(cat))   # interno, no se exporta
    return cat


def ensuciar_catalogo(cat):
    f = "F2 catalogo_productos.xlsx"
    c = cat.drop(columns="popularidad").copy().astype({"precio_venta": object, "costo_unitario": object})
    n = len(c)

    sel = rng.random(n) < 0.08                                  # categoría escrita distinto
    nuevas = [str(rng.choice([v.upper(), sin_tildes(v), v.lower()])) for v in c.loc[sel, "categoria"]]
    c.loc[sel, "categoria"] = nuevas
    registrar(f, "categoria", "Misma categoría escrita de formas distintas", sel.sum(), nuevas[:5])

    sel = rng.random(n) < 0.30                                  # unidades inconsistentes
    mapa = {"und": ["UND", "Unidad", "un"], "kg": ["KG", "Kilo", "kilogramo"]}
    nuevas = [str(rng.choice(mapa[u])) for u in c.loc[sel, "unidad_medida"]]
    c.loc[sel, "unidad_medida"] = nuevas
    registrar(f, "unidad_medida", "Unidad de medida sin estandarizar", sel.sum(), nuevas[:5])

    sel = rng.random(n) < 0.03                                  # costo nulo
    c.loc[sel, "costo_unitario"] = None
    registrar(f, "costo_unitario", "Costo nulo (no se puede calcular margen)", sel.sum(),
              c.loc[sel, "codigo_producto"].head(5))

    sel = (rng.random(n) < 0.01) & c["costo_unitario"].notna()  # costo mayor que precio
    c.loc[sel, "costo_unitario"] = [int(p * 1.15) for p in c.loc[sel, "precio_venta"]]
    registrar(f, "costo_unitario", "Costo mayor que el precio de venta", sel.sum(),
              (c.loc[sel, "codigo_producto"] + ": precio " + c.loc[sel, "precio_venta"].astype(str)
               + " / costo " + c.loc[sel, "costo_unitario"].astype(str)).head(5))

    sel = rng.random(n) < 0.02                                  # precio guardado como texto
    c.loc[sel, "precio_venta"] = ["$ " + f"{int(p):,}".replace(",", ".") for p in c.loc[sel, "precio_venta"]]
    registrar(f, "precio_venta", "Precio guardado como texto con símbolo $", sel.sum(),
              c.loc[sel, "precio_venta"].head(5))

    dup = c.sample(8, random_state=SEED).copy()                 # código duplicado
    dup["descripcion"] = dup["descripcion"].str.upper()
    registrar(f, "codigo_producto", "Código duplicado con descripción diferente", len(dup),
              dup["codigo_producto"].head(5))
    return pd.concat([c, dup]).sort_values("codigo_producto", kind="stable").reset_index(drop=True)


# ---------------------------------------------------------------- F3 clientes
def generar_clientes():
    n = N_CLIENTES
    pesos = np.array([s["base"] for s in SEDES], float)
    ciudades = rng.choice([s["ciudad"] for s in SEDES], n, p=pesos / pesos.sum())
    genero = rng.choice(["F", "M"], n)
    nombres = np.where(genero == "F", rng.choice(NOMBRES_F, n), rng.choice(NOMBRES_M, n))
    apellidos = [f"{a} {b}" for a, b in zip(rng.choice(APELLIDOS, n), rng.choice(APELLIDOS, n))]

    # 40 % afiliados antes del periodo y 60 % durante él (el programa crece -> P2 tiene tendencia)
    ini, p_ini = pd.Timestamp("2019-01-01"), pd.Timestamp(FECHA_INI)
    d_antes, d_per = (p_ini - ini).days, (pd.Timestamp(FECHA_FIN) - p_ini).days
    antes = rng.random(n) < 0.40
    dias = np.where(antes, rng.integers(0, d_antes, n), d_antes + (rng.random(n) ** 0.7 * d_per).astype(int))
    afil = ini + pd.to_timedelta(dias, unit="D")

    nac = pd.Timestamp("1955-01-01") + pd.to_timedelta(rng.integers(0, 18250, n), unit="D")
    emails = [f"{sin_tildes(a).lower()}.{sin_tildes(b.split()[0]).lower()}{i}@correo-demo.co"
              for i, (a, b) in enumerate(zip(nombres, apellidos))]
    return pd.DataFrame(dict(
        id_cliente=[f"CLI{i:05d}" for i in range(1, n + 1)],
        nombres=nombres, apellidos=apellidos, genero=genero,
        fecha_nacimiento=nac.strftime("%Y-%m-%d"), email=emails, ciudad=ciudades,
        nivel=rng.choice(["Bronce", "Plata", "Oro"], n, p=[0.6, 0.3, 0.1]),
        fecha_afiliacion=afil, puntos=rng.integers(0, 25000, n),
        acepta_marketing=rng.random(n) < 0.7,
    ))


def exportar_clientes(cli, ruta):
    """Escribe el JSON completo (ensuciado) y devuelve la lista de registros anidados."""
    f = "F3 clientes_fidelizacion.json"
    c = cli.copy()
    c["fecha_afiliacion"] = c["fecha_afiliacion"].dt.strftime("%Y-%m-%d").astype(object)
    n = len(c)
    sel = rng.random(n) < 0.10
    c.loc[sel, "fecha_afiliacion"] = pd.to_datetime(c.loc[sel, "fecha_afiliacion"]).dt.strftime("%d/%m/%Y")
    registrar(f, "programa.fecha_afiliacion", "Fechas en dos formatos (ISO y dd/mm/aaaa)", sel.sum(),
              c.loc[sel, "fecha_afiliacion"].head(5))

    sel = rng.random(n) < 0.07
    c.loc[sel, "ciudad"] = [str(rng.choice(VARIANTES_CIUDAD[x])) for x in c.loc[sel, "ciudad"]]
    registrar(f, "contacto.ciudad", "Ciudad escrita de formas distintas", sel.sum(), c.loc[sel, "ciudad"].head(5))

    sel = rng.random(n) < 0.30
    c.loc[sel, "genero"] = [str(rng.choice(["Femenino", "f"] if g == "F" else ["Masculino", "m"]))
                            for g in c.loc[sel, "genero"]]
    registrar(f, "genero", "Género codificado de varias formas", sel.sum(), c.loc[sel, "genero"].head(5))

    sel = rng.random(n) < 0.02
    c.loc[sel, "nivel"] = None
    registrar(f, "programa.nivel", "Nivel del programa nulo", sel.sum(), c.loc[sel, "id_cliente"].head(5))

    sel = rng.random(n) < 0.015
    c.loc[sel, "email"] = c.loc[sel, "email"].str.replace("@", "", regex=False)
    registrar(f, "contacto.email", "Correo inválido (sin @)", sel.sum(), c.loc[sel, "email"].head(5))

    dup = c.sample(frac=0.015, random_state=SEED).copy()
    dup["nombres"], dup["email"] = dup["nombres"].str.upper(), dup["email"].str.upper()
    registrar(f, "id_cliente", "Cliente duplicado con nombre/correo en mayúsculas", len(dup),
              dup["id_cliente"].head(5))
    c = pd.concat([c, dup]).sort_values("id_cliente", kind="stable")

    def nulo(v):
        return None if pd.isna(v) else v

    registros = [{
        "id_cliente": r.id_cliente, "nombres": r.nombres, "apellidos": r.apellidos, "genero": r.genero,
        "fecha_nacimiento": r.fecha_nacimiento,
        "contacto": {"email": r.email, "ciudad": r.ciudad},
        "programa": {"nivel": nulo(r.nivel), "fecha_afiliacion": r.fecha_afiliacion,
                     "puntos": int(r.puntos), "acepta_marketing": bool(r.acepta_marketing)},
    } for r in c.itertuples(index=False)]
    doc = {"programa": "Alianza Puntos", "exportado_en": "2026-01-05T08:00:00",
           "total_registros": len(cli),   # no cuadra con los duplicados (error a propósito)
           "datos_sinteticos": True, "clientes": registros}
    ruta.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    return registros


# ---------------------------------------------------------------- F1 ventas POS
def generar_ventas(sede, cat, cli):
    fechas = pd.date_range(FECHA_INI, FECHA_FIN, freq="D")
    t = (fechas - fechas[0]).days.values / 365.0
    quincena = np.where(np.isin(fechas.day, [1, 2, 15, 16, 30, 31]), 1.15, 1.0)
    lam = sede["base"] * MES_F[fechas.month - 1] * DIA_F[fechas.dayofweek] * quincena * CRECIMIENTO_ANUAL ** t
    f_tix = pd.DatetimeIndex(np.repeat(fechas.values, rng.poisson(lam)))
    n = len(f_tix)

    # ---- encabezado de tiquete
    anio = f_tix.year.values
    seq = pd.Series(1, index=range(n)).groupby(anio).cumsum().values
    id_tx = (sede["id"] + "-" + pd.Series(anio).astype(str) + "-"
             + pd.Series(seq).astype(str).str.zfill(7)).values
    hora = pd.Series(rng.choice(HORAS, n, p=HORA_P)).astype(str).str.zfill(2) + ":" + \
        pd.Series(rng.integers(0, 60, n)).astype(str).str.zfill(2)
    caja = "C" + pd.Series(rng.integers(1, 9, n)).astype(str).str.zfill(2)
    medio = rng.choice(MEDIOS_PAGO, n, p=MEDIOS_P)

    # ---- cliente fidelizado: participación crece de ~25 % a ~45 %
    avance = (f_tix - f_tix[0]).days.values / max(1, (f_tix[-1] - f_tix[0]).days)
    es_fiel = rng.random(n) < (0.25 + 0.20 * avance)
    id_cli = np.full(n, None, dtype=object)
    cli_c = cli[cli["ciudad"] == sede["ciudad"]]
    w_nivel = cli_c["nivel"].map({"Bronce": 1.0, "Plata": 1.8, "Oro": 3.0}).values
    mes_key = anio * 100 + f_tix.month.values
    for mk in np.unique(mes_key):
        m = (mes_key == mk) & es_fiel
        ok = (cli_c["fecha_afiliacion"] <= pd.Timestamp(year=mk // 100, month=mk % 100, day=1)).values
        if m.sum() and ok.sum():
            p = w_nivel[ok] / w_nivel[ok].sum()
            id_cli[m] = rng.choice(cli_c["id_cliente"].values[ok], m.sum(), p=p)

    # ---- líneas del tiquete
    n_lin = 1 + rng.poisson(1.6, n)
    ix = np.repeat(np.arange(n), n_lin)
    linea = np.arange(len(ix)) - np.repeat(np.cumsum(n_lin) - n_lin, n_lin) + 1
    f_lin = f_tix[ix]
    mes, dow = f_lin.month.values, f_lin.dayofweek.values

    cat_lin = np.empty(len(ix), dtype=object)
    for m in range(1, 13):
        sel = mes == m
        w = np.array([peso_categoria(c, m, sede["ciudad"]) for c in CATS])
        cat_lin[sel] = rng.choice(CATS, sel.sum(), p=w / w.sum())

    prod = np.empty(len(ix), dtype=object)
    for c in CATS:
        sel = cat_lin == c
        pc = cat[cat["categoria"] == c]
        prod[sel] = rng.choice(pc["codigo_producto"].values, sel.sum(),
                               p=(pc["popularidad"] / pc["popularidad"].sum()).values)

    info = cat.set_index("codigo_producto")
    unidad = info.loc[prod, "unidad_medida"].values
    precio = info.loc[prod, "precio_venta"].values.astype(float)
    cant = np.where(unidad == "kg", np.round(rng.uniform(0.25, 2.5, len(ix)), 3),
                    1 + rng.poisson(0.5, len(ix))).astype(float)

    # ---- promociones: más en fin de semana (Cali más agresiva) -> P3 tiene respuesta
    finde = dow >= 5
    if sede["ciudad"] == "Cali":
        p_promo = np.where(finde, 0.32, 0.07)
        p_desc = np.where(finde[:, None], [[0.15, 0.20, 0.25, 0.20, 0.20]], [[0.35, 0.25, 0.20, 0.12, 0.08]])
    else:
        p_promo = np.where(finde, 0.20, 0.07)
        p_desc = np.tile([0.35, 0.25, 0.20, 0.12, 0.08], (len(ix), 1))
    afin = np.array([CATEGORIAS[c][4] for c in cat_lin])
    con_promo = rng.random(len(ix)) < np.clip(p_promo * afin + np.where(mes == 12, 0.05, 0), 0, 0.9)
    niveles = np.array([0.10, 0.15, 0.20, 0.25, 0.30])
    u = rng.random(len(ix))[:, None]
    desc = np.where(con_promo, niveles[(u > np.cumsum(p_desc, axis=1)).sum(axis=1).clip(0, 4)], 0.0)

    return pd.DataFrame(dict(
        id_transaccion=id_tx[ix], linea=linea, fecha=f_lin, hora=hora.values[ix],
        id_sede=sede["id"], ciudad=sede["ciudad"], id_caja=caja.values[ix],
        codigo_producto=prod, unidad=unidad, cantidad=cant, precio_unitario=precio,
        descuento_pct=desc, valor_total=np.round(cant * precio * (1 - desc)),
        medio_pago=medio[ix], id_cliente=id_cli[ix],
    ))


def ensuciar_ventas(df, sede):
    f = f"F1 {sede['archivo']}"
    d = df.copy()
    n = len(d)

    # -- errores numéricos
    sel = rng.random(n) < 0.006
    d.loc[sel, "cantidad"] = np.nan
    registrar(f, "cantidad", "Cantidad nula", sel.sum(), d.loc[sel, "id_transaccion"].head(5))

    sel = rng.random(n) < 0.0015
    d.loc[sel, ["cantidad", "valor_total"]] *= -1
    registrar(f, "cantidad / valor_total", "Devolución registrada como venta negativa", sel.sum(),
              d.loc[sel, "cantidad"].head(5))

    sel = rng.random(n) < 0.0005
    d.loc[sel, "precio_unitario"] *= 100
    registrar(f, "precio_unitario", "Error de digitación (precio x100)", sel.sum(),
              d.loc[sel, "precio_unitario"].head(5))

    # -- a texto, con el formato propio de la sede
    fechas = d["fecha"].dt.strftime(sede["fmt"]).copy()
    registrar(f, "fecha", f"Formato de fecha propio de la sede ({sede['fmt']})", n, fechas.head(2))
    if sede["ciudad"] == "Bogotá":                              # además, mezcla dentro del mismo archivo
        sel = rng.random(n) < 0.01
        fechas[sel] = d.loc[sel, "fecha"].dt.strftime("%d/%m/%Y")
        registrar(f, "fecha", "Formatos de fecha mezclados en el mismo archivo", sel.sum(), fechas[sel].head(5))
    d["fecha"] = fechas

    d["cantidad"] = [("" if pd.isna(q) else (f"{q:.3f}" if u == "kg" else str(int(q))))
                     for q, u in zip(d["cantidad"], d["unidad"])]
    d["descuento_pct"] = d["descuento_pct"].map(lambda x: f"{x:.2f}")
    d["precio_unitario"] = d["precio_unitario"].astype(int).astype(str)
    d["valor_total"] = d["valor_total"].astype(int).astype(str)
    if sede["dec"] == ",":
        for col in ("cantidad", "descuento_pct"):
            d[col] = d[col].str.replace(".", ",", regex=False)
        registrar(f, "cantidad / descuento_pct", "Separador ';' y coma decimal (configuración regional)",
                  n, d["descuento_pct"].head(2))
    d = d.drop(columns="unidad")

    # -- errores de texto
    sel = rng.random(n) < 0.05
    d.loc[sel, "ciudad"] = [str(rng.choice(VARIANTES_CIUDAD[sede["ciudad"]])) for _ in range(sel.sum())]
    registrar(f, "ciudad", "Ciudad escrita de formas distintas", sel.sum(), d.loc[sel, "ciudad"].head(5))

    sel = rng.random(n) < 0.015
    def variante(cod):
        num = cod[1:]
        return str(rng.choice([cod.lower(), "P" + str(int(num)), f" {cod} ", "P-" + num]))
    d.loc[sel, "codigo_producto"] = [variante(c) for c in d.loc[sel, "codigo_producto"]]
    registrar(f, "codigo_producto", "Código de producto con formato inconsistente", sel.sum(),
              d.loc[sel, "codigo_producto"].head(5))

    sel = rng.random(n) < 0.001
    d.loc[sel, "codigo_producto"] = [f"P9{rng.integers(1000, 9999)}" for _ in range(sel.sum())]
    registrar(f, "codigo_producto", "Código que no existe en el catálogo (huérfano)", sel.sum(),
              d.loc[sel, "codigo_producto"].head(5))

    if sede["ciudad"] == "Medellín":
        sel = rng.random(n) < 0.03
        d.loc[sel, "precio_unitario"] = ["$" + f"{int(p):,}".replace(",", ".") for p in d.loc[sel, "precio_unitario"]]
        registrar(f, "precio_unitario", "Precio como texto con $ y punto de miles", sel.sum(),
                  d.loc[sel, "precio_unitario"].head(5))

    if sede["ciudad"] == "Cali":
        sel = (rng.random(n) < 0.03) & d["id_cliente"].isna()
        d.loc[sel, "id_cliente"] = rng.choice(["N/A", "0", "SIN CLIENTE"], sel.sum())
        registrar(f, "id_cliente", "Cliente vacío codificado como texto", sel.sum(), d.loc[sel, "id_cliente"].head(5))

    dup = d.sample(frac=0.004, random_state=SEED)
    registrar(f, "registro completo", "Filas duplicadas exactas", len(dup), dup["id_transaccion"].head(5))
    d = pd.concat([d, dup]).sort_index(kind="stable").reset_index(drop=True)
    return d


# ---------------------------------------------------------------- principal
def main():
    DIR_RAW.mkdir(parents=True, exist_ok=True)
    DIR_MUESTRAS.mkdir(parents=True, exist_ok=True)

    catalogo = generar_catalogo()
    clientes = generar_clientes()

    total = 0
    for s in SEDES:
        limpio = generar_ventas(s, catalogo, clientes)
        total += len(limpio)
        sucio = ensuciar_ventas(limpio, s)
        sucio.to_csv(DIR_RAW / s["archivo"], sep=s["sep"], index=False, encoding="utf-8")
        sucio.sample(20, random_state=SEED).sort_index().to_csv(
            DIR_MUESTRAS / f"muestra_{s['archivo']}", sep=s["sep"], index=False, encoding="utf-8")
        print(f"  {s['archivo']:<32} {len(sucio):>9,} filas")

    cat_sucio = ensuciar_catalogo(catalogo)
    cat_sucio.to_excel(DIR_RAW / "catalogo_productos.xlsx", sheet_name="Catalogo", index=False)
    cat_sucio.head(20).to_csv(DIR_MUESTRAS / "muestra_catalogo_productos.csv", index=False, encoding="utf-8")

    registros = exportar_clientes(clientes, DIR_RAW / "clientes_fidelizacion.json")
    pd.json_normalize(registros[:20]).to_csv(            # JSON anidado aplanado: contacto.email, programa.nivel...
        DIR_MUESTRAS / "muestra_clientes_fidelizacion.csv", index=False, encoding="utf-8")

    Path("datos/registro_errores_inyectados.json").write_text(
        json.dumps(list(registro.values()), ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\nLíneas de venta (filas de hechos, antes de limpiar): {total:,}")
    print(f"Productos: {len(catalogo)} | Clientes: {len(clientes)} | Periodo: {FECHA_INI} a {FECHA_FIN}")
    print(f"Tipos de error inyectados: {len(registro)} -> datos/registro_errores_inyectados.json")


if __name__ == "__main__":
    main()
