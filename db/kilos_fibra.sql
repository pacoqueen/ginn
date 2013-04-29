SELECT id
 INTO TEMP partes_fib_temp
 FROM parte_de_produccion 
 WHERE (fecha >= '2007-01-01'                     -- Parámetro fecha ini
        AND fecha <= '2007-12-31'                 -- Parámetro fecha fin
        AND observaciones LIKE '%;%;%;%;%;%');    -- GTX. Hay que escapar los porcientos

SELECT pv.id AS producto_venta_id, color 
 INTO TEMP producto_venta_con_campos_especificos_temp
 FROM campos_especificos_bala ceb, producto_venta pv
 WHERE (pv.campos_especificos_bala_id = ceb.id);

SELECT bala_id AS id, color
 INTO TEMP ids_balas_fabricadas_temp
 FROM articulo, producto_venta_con_campos_especificos_temp AS pv
 WHERE parte_de_produccion_id IN (SELECT id FROM partes_fib_temp)
    AND articulo.producto_venta_id = pv.producto_venta_id;

SELECT bigbag_id AS id
 INTO TEMP ids_bigbags_fabricados_temp
 FROM articulo 
 WHERE parte_de_produccion_id IN (SELECT id FROM partes_fib_temp);

SELECT bala.id, pesobala AS peso_ce, color
 INTO TEMP balas_fabricadas_temp
 FROM bala, ids_balas_fabricadas_temp
 WHERE bala.id IN (SELECT id FROM ids_balas_fabricadas_temp)
    AND bala.id = ids_balas_fabricadas_temp.id;

SELECT id, pesobigbag AS peso_ce
 INTO TEMP bigbags_fabricados_temp
 FROM bigbag
 WHERE id IN (SELECT id FROM ids_bigbags_fabricados_temp);

------------------------------------------------------
SELECT COUNT(id), SUM(peso_ce) AS kilos_bb          --
 FROM bigbags_fabricados_temp;                      --
                                                    --
SELECT COUNT(id), SUM(peso_ce), color AS kilos_b    --
 FROM balas_fabricadas_temp                         --
 GROUP BY color;                                    --
------------------------------------------------------
 
DROP TABLE balas_fabricadas_temp;
DROP TABLE bigbags_fabricados_temp;
DROP TABLE ids_balas_fabricadas_temp;
DROP TABLE ids_bigbags_fabricados_temp;
DROP TABLE producto_venta_con_campos_especificos_temp;
DROP TABLE partes_fib_temp;

