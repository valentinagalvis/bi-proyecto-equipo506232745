-- Pobla dim_tiempo sin huecos para todo el periodo de los hechos (2023-01-01 a 2024-12-31).
USE dw_alianza;
SET SESSION cte_max_recursion_depth = 5000;
SET lc_time_names = 'es_ES';
INSERT INTO dim_tiempo
WITH RECURSIVE dias AS (
  SELECT DATE('2023-01-01') AS fecha
  UNION ALL
  SELECT fecha + INTERVAL 1 DAY FROM dias WHERE fecha < '2024-12-31'
)
SELECT CAST(DATE_FORMAT(fecha, '%Y%m%d') AS UNSIGNED),
       fecha, DAY(fecha), MONTH(fecha), MONTHNAME(fecha), QUARTER(fecha), YEAR(fecha),
       WEEKDAY(fecha) + 1, DAYNAME(fecha), WEEKDAY(fecha) >= 5
FROM dias;
