-- Dimensión producto (F2 catálogo). Llave subrogada; id_producto de la fuente se conserva.
USE dw_alianza;
CREATE TABLE dim_producto (
  sk_producto      INT           NOT NULL AUTO_INCREMENT,
  id_producto      VARCHAR(10)   NOT NULL,
  nombre_producto  VARCHAR(100)  NOT NULL,
  categoria        VARCHAR(60)   NOT NULL,
  grupo            VARCHAR(60)   NOT NULL,
  marca            VARCHAR(60)   NOT NULL,
  unidad_medida    VARCHAR(20)   NOT NULL,
  costo_referencia DECIMAL(12,2) NULL,
  CONSTRAINT pk_dim_producto PRIMARY KEY (sk_producto),
  CONSTRAINT uq_dim_producto_id UNIQUE (id_producto)
);
-- Miembro "Desconocido": recibe las ventas cuyo producto no exista en el catálogo.
INSERT INTO dim_producto (sk_producto, id_producto, nombre_producto, categoria, grupo, marca, unidad_medida, costo_referencia)
VALUES (-1, 'N/A', 'Desconocido', 'DESCONOCIDO', 'DESCONOCIDO', 'SIN MARCA', 'N/A', NULL);
