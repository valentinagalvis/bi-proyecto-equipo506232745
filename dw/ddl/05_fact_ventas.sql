-- Hechos: una fila = una línea de producto en una transacción POS, en una sede y una fecha.
USE dw_alianza;
CREATE TABLE fact_ventas (
  id_linea         INT           NOT NULL AUTO_INCREMENT,
  id_venta         VARCHAR(10)   NOT NULL,      -- dimensión degenerada (número de transacción)
  sk_tiempo        INT           NOT NULL,
  sk_producto      INT           NOT NULL,
  sk_sede          INT           NOT NULL,
  sk_cliente       INT           NOT NULL,
  canal            VARCHAR(20)   NOT NULL,
  unidades         INT           NOT NULL,
  precio_unitario  DECIMAL(12,2) NOT NULL,
  costo_unitario   DECIMAL(12,2) NOT NULL,
  valor_venta      DECIMAL(14,2) NOT NULL,      -- unidades × precio_unitario
  costo_total      DECIMAL(14,2) NOT NULL,      -- unidades × costo_unitario
  margen_bruto     DECIMAL(14,2) NOT NULL,      -- valor_venta − costo_total
  CONSTRAINT pk_fact_ventas PRIMARY KEY (id_linea),
  CONSTRAINT fk_fv_tiempo   FOREIGN KEY (sk_tiempo)   REFERENCES dim_tiempo (sk_tiempo),
  CONSTRAINT fk_fv_producto FOREIGN KEY (sk_producto) REFERENCES dim_producto (sk_producto),
  CONSTRAINT fk_fv_sede     FOREIGN KEY (sk_sede)     REFERENCES dim_sede (sk_sede),
  CONSTRAINT fk_fv_cliente  FOREIGN KEY (sk_cliente)  REFERENCES dim_cliente (sk_cliente)
);
