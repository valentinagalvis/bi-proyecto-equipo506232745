-- Staging de F4 SIPSA (referencia mensual de precio mayorista). No va en la tabla de hechos:
-- su grano es producto–mercado–mes (2013–2017) y no coincide con la línea de venta POS.
USE dw_alianza;
CREATE TABLE stg_sipsa_precio (
  id           INT           NOT NULL AUTO_INCREMENT,
  fecha_mes    DATE          NOT NULL,
  grupo        VARCHAR(60)   NOT NULL,
  producto     VARCHAR(120)  NOT NULL,
  ciudad       VARCHAR(60)   NOT NULL,
  mercado      VARCHAR(120)  NOT NULL,
  precio       DECIMAL(12,2) NOT NULL,
  CONSTRAINT pk_stg_sipsa_precio PRIMARY KEY (id)
);
