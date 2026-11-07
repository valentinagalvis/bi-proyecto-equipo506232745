-- Dimensión cliente (F3 fidelización). Incluye el miembro 'NO FIDELIZADO' para ventas anónimas.
USE dw_alianza;
CREATE TABLE dim_cliente (
  sk_cliente         INT          NOT NULL AUTO_INCREMENT,
  id_cliente         VARCHAR(10)  NOT NULL,
  segmento           VARCHAR(20)  NOT NULL,
  programa           VARCHAR(30)  NOT NULL,
  ciudad             VARCHAR(40)  NOT NULL,
  fecha_inscripcion  DATE         NULL,
  activo             TINYINT(1)   NULL,
  email_valido       TINYINT(1)   NULL,
  puntos             INT          NULL,
  es_fidelizado      TINYINT(1)   NOT NULL,
  CONSTRAINT pk_dim_cliente PRIMARY KEY (sk_cliente),
  CONSTRAINT uq_dim_cliente_id UNIQUE (id_cliente)
);
-- Miembro "No fidelizado": ventas anónimas (id_cliente vacío en F1) y clientes que no existan en F3.
INSERT INTO dim_cliente (sk_cliente, id_cliente, segmento, programa, ciudad, fecha_inscripcion, activo, email_valido, puntos, es_fidelizado)
VALUES (-1, 'NO_FIDEL', 'No fidelizado', 'Ninguno', 'N/A', NULL, NULL, NULL, NULL, 0);
