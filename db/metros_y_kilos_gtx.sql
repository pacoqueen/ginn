SELECT id
 INTO TEMP partes_gtx_temp
 FROM parte_de_produccion 
 WHERE (fecha >= '2007-01-01'                     -- Parámetro fecha ini
        AND fecha <= '2007-12-31'                 -- Parámetro fecha fin
        AND observaciones NOT LIKE '%;%;%;%;%;%'); -- GTX. Hay que escapar los %

SELECT pv.id AS producto_venta_id, 
       peso_embalaje, 
       metros_lineales, 
       ancho, 
       metros_lineales * ancho AS metros_cuadrados, 
       gramos AS gramaje, 
       (metros_lineales * ancho * gramos) / 1000 AS peso_teorico
 INTO TEMP producto_venta_con_campos_especificos_temp
 FROM campos_especificos_rollo cer, producto_venta pv
 WHERE (pv.campos_especificos_rollo_id = cer.id);

SELECT id, rollo_id, rollo_defectuoso_id, peso_embalaje, pv.producto_venta_id
 INTO TEMP articulos_rollo_fabricados_temp
 FROM articulo a, producto_venta_con_campos_especificos_temp pv
 WHERE parte_de_produccion_id IN (SELECT id FROM partes_gtx_temp) 
        AND (rollo_id IS NOT NULL
             OR rollo_defectuoso_id IS NOT NULL)
        AND a.producto_venta_id = pv.producto_venta_id;

SELECT id, peso - peso_embalaje AS peso_se, ancho * metros_lineales AS metros_cuadrados
 INTO TEMP articulos_rollo_b_temp
 FROM rollo_defectuoso
 WHERE id IN (SELECT rollo_defectuoso_id 
               FROM articulo 
               WHERE parte_de_produccion_id IN (SELECT id FROM partes_gtx_temp)
                     AND rollo_defectuoso_id IS NOT NULL);

SELECT peso AS peso_ce, peso_embalaje AS peso_e, peso - peso_embalaje AS peso_se
 INTO TEMP pesos_rollos_temp
 FROM rollo r, articulos_rollo_fabricados_temp
 WHERE r.id = articulos_rollo_fabricados_temp.rollo_id;

SELECT SUM(peso_ce) AS sum_peso_ce, SUM(peso_se) AS sum_peso_se FROM pesos_rollos_temp;

SELECT COUNT(rollo_id) AS rollos_a, producto_venta_id 
 INTO TEMP rollos_a_y_producto_venta_temp
 FROM articulos_rollo_fabricados_temp 
 GROUP BY producto_venta_id;

-- Metros cuadrados y kilos teóricos de A ----------------------------
SELECT SUM(rollos_a * metros_cuadrados) AS metros_a,                --
       SUM(rollos_a * peso_teorico) AS kilos_a                      --
 FROM rollos_a_y_producto_venta_temp raypvt,                        --
      producto_venta_con_campos_especificos_temp pvccet             --
 WHERE raypvt.producto_venta_id = pvccet.producto_venta_id;         --
----------------------------------------------------------------------

-- Metros cuadrados y kilos de B -------------------------------------
SELECT SUM(metros_cuadrados) AS metros_b, SUM(peso_se) AS kilos_b   --
 FROM articulos_rollo_b_temp;                                       --
----------------------------------------------------------------------

DROP TABLE rollos_a_y_producto_venta_temp;
DROP TABLE pesos_rollos_temp;
DROP TABLE articulos_rollo_b_temp;
DROP TABLE articulos_rollo_fabricados_temp;
DROP TABLE producto_venta_con_campos_especificos_temp;
DROP TABLE partes_gtx_temp;

----------------------------------------------------------------------
-- Consumo de fibra de los partes de producción de geotextiles      --
----------------------------------------------------------------------
SELECT id
 INTO TEMP partes_gtx_temp
 FROM parte_de_produccion 
 WHERE (fecha >= '2007-01-01'                     -- Parámetro fecha ini
        AND fecha <= '2007-01-31'                 -- Parámetro fecha fin
        AND observaciones NOT LIKE '%;%;%;%;%;%'); -- GTX. Hay que escapar los %

SELECT rollo_id, rollo_defectuoso_id
 INTO TEMP articulos_rollo_fabricados_temp
 FROM articulo
 WHERE parte_de_produccion_id IN (SELECT id FROM partes_gtx_temp);

SELECT partida_id 
 INTO TEMP partidas_rollos_defectuosos_temp 
 FROM rollo_defectuoso rd
 WHERE rd.id IN (SELECT rollo_defectuoso_id FROM articulos_rollo_fabricados_temp)
 GROUP BY partida_id;

SELECT partida_id 
 INTO TEMP partidas_rollos_temp 
 FROM rollo r
 WHERE r.id IN (SELECT rollo_id FROM articulos_rollo_fabricados_temp)
 GROUP BY partida_id;

CREATE OR REPLACE FUNCTION partes_de_partida (INTEGER) RETURNS BIGINT
AS '
    SELECT COUNT(id)
    FROM parte_de_produccion 
    WHERE id IN (SELECT parte_de_produccion_id
                 FROM articulo 
                 WHERE rollo_id IS NOT NULL AND rollo_id IN (SELECT id 
                                                             FROM rollo 
                                                             WHERE partida_id = $1) 
                    OR rollo_defectuoso_id IS NOT NULL AND rollo_defectuoso_id IN (SELECT id 
                                                                                   FROM rollo_defectuoso 
                                                                                   WHERE partida_id = $1) 
                GROUP BY parte_de_produccion_id)
    ;
' LANGUAGE 'sql';

CREATE OR REPLACE FUNCTION partes_de_partida_antes_de_fecha (INTEGER, DATE) RETURNS BIGINT
AS '
    SELECT COUNT(id) 
     FROM parte_de_produccion 
     WHERE fecha <= $2
        AND id IN (SELECT parte_de_produccion_id
                     FROM articulo 
                     WHERE rollo_id IS NOT NULL AND rollo_id IN (SELECT id 
                                                                 FROM rollo 
                                                                 WHERE partida_id = $1) 
                        OR rollo_defectuoso_id IS NOT NULL AND rollo_defectuoso_id IN (SELECT id 
                                                                                       FROM rollo_defectuoso 
                                                                                       WHERE partida_id = $1)
                    GROUP BY parte_de_produccion_id) 
     ;
' LANGUAGE 'sql';

CREATE OR REPLACE FUNCTION partida_entra_en_fecha(INTEGER, DATE) RETURNS BOOLEAN 
    -- Recibe un ID de partida de geotextiles y una fecha. Devuelve TRUE si ningún 
    -- parte de producción de la partida tiene fecha posterior a la recibida Y la 
    -- partida existe y tiene producción.
    -- TODO: Esto se puede optimizar bastante.
AS '
    SELECT partes_de_partida($1) > 0 AND partes_de_partida($1) = partes_de_partida_antes_de_fecha($1, $2);
' LANGUAGE 'sql';

CREATE OR REPLACE FUNCTION partida_carga_entra_en_fecha(INTEGER, DATE) RETURNS BOOLEAN 
    -- Recibe el ID de una partida de carga y devuelve TRUE si todas las partidas 
    -- de geotextiles de la misma pertenecen a partes de producción de fecha anterior 
    -- o igual al segundo parámetro.
AS' 
    SELECT COUNT(*) > 0 
    FROM partida
    WHERE partida_carga_id = $1 
          AND partida_entra_en_fecha(partida.id, $2);
' LANGUAGE 'sql';

SELECT partida_carga_id
 INTO TEMP partidas_carga_id_temp
 FROM partida
 WHERE (id IN (SELECT partida_id FROM partidas_rollos_defectuosos_temp)
        OR id IN (SELECT partida_id FROM partidas_rollos_temp)) 
 GROUP BY partida_carga_id;

SELECT partida_carga_id 
 INTO TEMP partidas_de_carga_de_partidas_en_fecha_temp
 FROM partidas_carga_id_temp
 WHERE partida_carga_entra_en_fecha(partida_carga_id, '2007-01-31');       -- Parámetro fecha fin

SELECT id, AVG(pesobala) AS _pesobala    -- Si sale una bala más de una vez, la media dará el mismo peso de la bala en sí.
 INTO TEMP balas_con_peso_de_partida_de_carga 
 FROM bala 
 WHERE partida_carga_id IN (SELECT partida_carga_id 
                            FROM partidas_de_carga_de_partidas_en_fecha_temp)
 GROUP BY id; 
-- OJO: Las balas llevan en torno a kilo o kilo y medio de plástico de embalar que se cuenta como fibra consumida.

SELECT COUNT(id) AS balas, SUM(_pesobala) AS peso_ce
 FROM balas_con_peso_de_partida_de_carga;

DROP FUNCTION partes_de_partida(INTEGER);
DROP FUNCTION partes_de_partida_antes_de_fecha(INTEGER, DATE);
DROP FUNCTION partida_entra_en_fecha(INTEGER, DATE);
DROP FUNCTION partida_carga_entra_en_fecha(INTEGER, DATE);

DROP TABLE partidas_carga_id_temp;
DROP TABLE balas_con_peso_de_partida_de_carga;
DROP TABLE partidas_de_carga_de_partidas_en_fecha_temp;
DROP TABLE partidas_rollos_defectuosos_temp;
DROP TABLE partidas_rollos_temp;
DROP TABLE articulos_rollo_fabricados_temp;
DROP TABLE partes_gtx_temp;

