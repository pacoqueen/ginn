SELECT pv.id AS producto_venta_id, color 
 INTO TEMP fibra_balas_con_campos_especificos_temp
 FROM campos_especificos_bala ceb, producto_venta pv
 WHERE pv.campos_especificos_bala_id = ceb.id
       AND pv.descripcion NOT ILIKE '%GEOCEM%';

SELECT SUM(linea_de_venta.cantidad) AS kilos,
       SUM(linea_de_venta.cantidad * linea_de_venta.precio * (1-linea_de_venta.descuento)) AS euros, 
       fibra_balas_con_campos_especificos_temp.color, 
       cliente.pais 
 FROM linea_de_venta, factura_venta, cliente, fibra_balas_con_campos_especificos_temp
 WHERE linea_de_venta.factura_venta_id = factura_venta.id
       AND factura_venta.fecha >= '2007-01-01'
       AND factura_venta.fecha <= '2007-12-31'
       AND cliente.id = factura_venta.cliente_id
       AND linea_de_venta.producto_venta_id = fibra_balas_con_campos_especificos_temp.producto_venta_id
 GROUP BY cliente.pais, fibra_balas_con_campos_especificos_temp.color; 


SELECT 0.0 AS kilos, 
       SUM(linea_de_abono.cantidad * linea_de_abono.diferencia) AS euros, 
       fibra_balas_con_campos_especificos_temp.color, 
       cliente.pais
 FROM linea_de_abono, factura_de_abono, cliente, abono, linea_de_venta, fibra_balas_con_campos_especificos_temp
 WHERE linea_de_abono.abono_id = abono.id
       AND linea_de_abono.linea_de_venta_id = linea_de_venta.id
       AND linea_de_venta.producto_venta_id = fibra_balas_con_campos_especificos_temp.producto_venta_id
       AND factura_de_abono.fecha >= '2007-01-01'
       AND factura_de_abono.fecha <= '2007-12-31'
       AND cliente.id = abono.cliente_id
       AND factura_de_abono.id = abono.factura_de_abono_id
GROUP BY cliente.pais, fibra_balas_con_campos_especificos_temp.color; 


SELECT linea_de_devolucion.id, linea_de_devolucion.articulo_id, cliente.pais, linea_de_devolucion.precio, fibra_balas_con_campos_especificos_temp.color
 INTO TEMP facturas_de_abono_temp
 FROM linea_de_devolucion, factura_de_abono, cliente, abono, articulo, fibra_balas_con_campos_especificos_temp
 WHERE linea_de_devolucion.abono_id = abono.id
       AND factura_de_abono.id = abono.factura_de_abono_id
       AND factura_de_abono.fecha >= '2007-01-01'
       AND factura_de_abono.fecha <= '2007-12-31'
       AND cliente.id = abono.cliente_id
       AND linea_de_devolucion.albaran_de_entrada_de_abono_id IS NOT NULL
       AND articulo.id = linea_de_devolucion.articulo_id
       AND articulo.producto_venta_id = fibra_balas_con_campos_especificos_temp.producto_venta_id; 

SELECT -1 * SUM(bala.pesobala) AS kilos, 
       -1 * SUM(precio) AS euros, 
       color, 
       pais
 FROM bala, facturas_de_abono_temp, articulo
 WHERE bala.id = articulo.bala_id 
       AND facturas_de_abono_temp.articulo_id = articulo.id
 GROUP BY pais, color;

DROP TABLE fibra_balas_con_campos_especificos_temp;
DROP TABLE facturas_de_abono_temp;


--- ^^^ FIBRA ENVASADA EN BALAS ^^^ --- vvv FIBRA ENVASADA EN BIGBAGS vvv ---


SELECT pv.id AS producto_venta_id
 INTO TEMP fibra_bigbags
 FROM producto_venta pv
 WHERE pv.descripcion ILIKE '%GEOCEM%';

SELECT COALESCE(SUM(linea_de_venta.cantidad), 0.0) AS kilos,
       COALESCE(SUM(linea_de_venta.cantidad * linea_de_venta.precio * (1-linea_de_venta.descuento)), 0.0) AS euros 
 FROM linea_de_venta, factura_venta, fibra_bigbags
 WHERE linea_de_venta.factura_venta_id = factura_venta.id
       AND factura_venta.fecha >= '2007-01-01'
       AND factura_venta.fecha <= '2007-12-31'
       AND linea_de_venta.producto_venta_id = fibra_bigbags.producto_venta_id
 ;

SELECT 0.0 AS kilos, 
       COALESCE(SUM(linea_de_abono.cantidad * linea_de_abono.diferencia), 0.0) AS euros 
 FROM linea_de_abono, factura_de_abono, abono, linea_de_venta, fibra_bigbags
 WHERE linea_de_abono.abono_id = abono.id
       AND linea_de_abono.linea_de_venta_id = linea_de_venta.id
       AND linea_de_venta.producto_venta_id = fibra_bigbags.producto_venta_id
       AND factura_de_abono.fecha >= '2007-01-01'
       AND factura_de_abono.fecha <= '2007-12-31'
       AND factura_de_abono.id = abono.factura_de_abono_id
 ; 

SELECT linea_de_devolucion.id, linea_de_devolucion.articulo_id, linea_de_devolucion.precio
 INTO TEMP facturas_de_abono_temp
 FROM linea_de_devolucion, factura_de_abono, abono, articulo, fibra_bigbags
 WHERE linea_de_devolucion.abono_id = abono.id
       AND factura_de_abono.id = abono.factura_de_abono_id
       AND factura_de_abono.fecha >= '2007-01-01'
       AND factura_de_abono.fecha <= '2007-12-31'
       AND linea_de_devolucion.albaran_de_entrada_de_abono_id IS NOT NULL
       AND articulo.id = linea_de_devolucion.articulo_id
       AND articulo.producto_venta_id = fibra_bigbags.producto_venta_id; 

SELECT COALESCE(-1 * SUM(bigbag.pesobigbag), 0.0) AS kilos, 
       COALESCE(-1 * SUM(precio), 0.0) AS euros 
 FROM bigbag, facturas_de_abono_temp, articulo
 WHERE bigbag.id = articulo.bigbag_id 
       AND facturas_de_abono_temp.articulo_id = articulo.id
 ;

DROP TABLE fibra_bigbags;
DROP TABLE facturas_de_abono_temp;

--- vvv FIBRA B vvv ---

SELECT albaran_salida.id AS albaran_salida_id, 
       linea_de_venta.precio * (1 - linea_de_venta.descuento) AS precio, 
       linea_de_venta.producto_venta_id, 
       linea_de_venta.id AS linea_de_venta_id
 INTO albaranes_facturados_en_fecha_temp 
 FROM albaran_salida, linea_de_venta
 WHERE albaran_salida.id = linea_de_venta.albaran_salida_id 
   AND linea_de_venta.producto_venta_id IS NOT NULL
   AND linea_de_venta.factura_venta_id 
       IN (SELECT factura_venta.id
            FROM factura_venta
            WHERE factura_venta.fecha >= '2007-01-01'
              AND factura_venta.fecha <= '2007-01-31')
 ;

SELECT bala.pesobala, articulo.producto_venta_id, articulo.albaran_salida_id
 FROM bala, articulo
 WHERE bala.claseb = TRUE
   AND articulo.bala_id = bala.id
   AND articulo.albaran_salida_id IN (SELECT albaran_salida_id 
                                       FROM albaranes_facturados_en_fecha_temp)
 ;

SELECT bigbag.pesobigbag, articulo.producto_venta_id, articulo.albaran_salida_id
 FROM bigbag, articulo
 WHERE bigbag.claseb = TRUE
   AND articulo.bigbag_id = bigbag.id
   AND articulo.albaran_salida_id IN (SELECT albaran_salida_id 
                                       FROM albaranes_facturados_en_fecha_temp)
 ;

SELECT COALESCE(SUM(bala.pesobala), 0) AS kilos_b_b
 FROM articulo, bala
 WHERE articulo.albaran_salida_id IN (SELECT albaran_salida_id 
                                       FROM albaranes_facturados_en_fecha_temp)
   AND articulo.bala_id = bala.id
   AND bala.claseb = TRUE;

SELECT COALESCE(SUM(bigbag.pesobigbag), 0) AS kilos_bb_b
 FROM articulo, bigbag
 WHERE articulo.albaran_salida_id IN (SELECT albaran_salida_id 
                                       FROM albaranes_facturados_en_fecha_temp)
   AND articulo.bigbag_id = bigbag.id
   AND bigbag.claseb = TRUE;

DROP TABLE albaranes_facturados_en_fecha_temp;

