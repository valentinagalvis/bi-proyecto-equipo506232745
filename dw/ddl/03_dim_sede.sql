-- Dimensión sede (maestro de sedes derivado de F1). Jerarquía sede → ciudad → región.
USE dw_alianza;
CREATE TABLE dim_sede (
  sk_sede      INT          NOT NULL AUTO_INCREMENT,
  id_sede      VARCHAR(5)   NOT NULL,
  nombre_sede  VARCHAR(60)  NOT NULL,
  ciudad       VARCHAR(40)  NOT NULL,
  region       VARCHAR(20)  NOT NULL,
  CONSTRAINT pk_dim_sede PRIMARY KEY (sk_sede),
  CONSTRAINT uq_dim_sede_id UNIQUE (id_sede)
);
-- Miembro "Desconocida": recibe las ventas cuya sede no exista.
INSERT INTO dim_sede (sk_sede, id_sede, nombre_sede, ciudad, region)
VALUES (-1, 'N/A', 'Desconocida', 'Desconocida', 'Desconocida');
