-- Tabla de predicciones del modelo elegido (Entrega 3).
-- Una fila = ventas netas reales y predichas de una sede y una categoría en una semana.
-- Llaves para unir con las dimensiones: sk_tiempo (lunes de la semana, AAAAMMDD) → dim_tiempo,
-- sk_sede → dim_sede, categoria → dim_producto.categoria.
-- Sin FOREIGN KEY a propósito: 00_reset.sql recrea las dimensiones y no debe bloquearse.
USE dw_alianza;
CREATE TABLE IF NOT EXISTS pred_ventas_semana (
  id                  INT           NOT NULL AUTO_INCREMENT,
  sk_tiempo           INT           NOT NULL,      -- lunes de la semana (AAAAMMDD)
  semana_inicio       DATE          NOT NULL,
  sk_sede             INT           NOT NULL,
  ciudad              VARCHAR(40)   NOT NULL,
  categoria           VARCHAR(60)   NOT NULL,
  tipo_registro       VARCHAR(12)   NOT NULL,      -- 'prueba' (con valor real) o 'pronostico' (semana futura)
  ventas_reales       DECIMAL(14,2) NULL,
  ventas_predichas    DECIMAL(14,2) NOT NULL,
  ventas_referencia   DECIMAL(14,2) NULL,          -- promedio de las 4 semanas anteriores
  modelo              VARCHAR(40)   NOT NULL,
  fecha_generacion    DATETIME      NOT NULL,
  CONSTRAINT pk_pred_ventas_semana PRIMARY KEY (id),
  INDEX ix_pred_tiempo (sk_tiempo),
  INDEX ix_pred_sede (sk_sede)
);
