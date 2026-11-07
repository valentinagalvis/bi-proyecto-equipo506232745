-- Dimensión de tiempo: una fila por día. Jerarquía día → mes → trimestre → año.
USE dw_alianza;
CREATE TABLE dim_tiempo (
  sk_tiempo        INT          NOT NULL,          -- AAAAMMDD
  fecha            DATE         NOT NULL,
  dia              TINYINT      NOT NULL,
  mes              TINYINT      NOT NULL,
  nombre_mes       VARCHAR(12)  NOT NULL,
  trimestre        TINYINT      NOT NULL,
  anio             SMALLINT     NOT NULL,
  dia_semana       TINYINT      NOT NULL,          -- 1 = lunes … 7 = domingo
  nombre_dia       VARCHAR(10)  NOT NULL,
  es_fin_de_semana TINYINT(1)   NOT NULL,
  CONSTRAINT pk_dim_tiempo PRIMARY KEY (sk_tiempo),
  CONSTRAINT uq_dim_tiempo_fecha UNIQUE (fecha)
);
