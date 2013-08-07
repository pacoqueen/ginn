
-- 05/08/2013
-- Parche para crear funciones de cálculo de crédito 

CREATE OR REPLACE FUNCTION cobro_esta_cobrado(idcobro INTEGER, 
                                   fecha DATE DEFAULT CURRENT_DATE)
    -- Recibe un ID de cobro y una fecha.
    -- Devuelve el importe cobrado en esa fecha, que depende de:
    --  * Si es una transferencia, efectivo, cheque o cualquier otra cosa 
    --    que no sea un confirming o un pagaré; se cuenta como cobrado en 
    --    cuanto se alcanza la fecha de cobro.
    --  * Si es un confirming, cuenta como cobrado siempre que tenga el 
    --    campo pendiente == FALSE. Ya que si no responde el cliente, 
    --    responde el banco por él.
    --  * Si es un pagaré, cuenta como cobrado si no está pendiente o no 
    --    está vencido todavía (fecha_cobro <= DATE recibido).
    RETURNS FLOAT
    AS $$
        DECLARE
            registro_cobro cobro%ROWTYPE;
            registro_pagare_cobro pagare_cobro%ROWTYPE;
            registro_confirming confirming%ROWTYPE;
            cobrado FLOAT;
        BEGIN
            -- Selecciono el cobro en cuestión:
            SELECT * INTO registro_cobro FROM cobro WHERE id = idcobro;
            -- Buscar si es pagaré, confirming u otra cosa. Aquí ya 
            -- me aseguro de que esté recibido mirando la fecha.
            IF NOT (registro_cobro.pagare_cobro_id IS NULL) THEN
                SELECT * INTO registro_pagare_cobro 
                  FROM pagare_cobro 
                 WHERE pagare_cobro.id = registro_cobro.pagare_cobro_id 
                   AND pagare_cobro.fecha_recepcion <= fecha;
                -- Si tiene fecha de cobro y ya ha pasado, he cobrado lo 
                -- que indique el pagaré (que puede ser 0 si está pendiente,  
                -- solo una parte del pagaré por error de alguien o lo que 
                -- sea, o completo --cuando se pone el pendiente=FALSE, el 
                -- cobrado se iguala al importe total del pagaré--).
                IF (NOT (registro_pagare_cobro.fecha_cobrado IS NULL))
                    AND fecha >= registro_pagare_cobro.fecha_cobrado THEN
                    cobrado := registro_pagare_cobro.cobrado;
                -- Si no tiene fecha de cobrado o ésta todavía no ha llegado 
                -- según la recibida, está documentado, pero no cobrado.
                -- O si no tiene fecha de cobrado en abosulto. Que estaría 
                -- no documentado.
                ELSE
                    cobrado := 0.0;
                END IF;
            ELSIF NOT (registro_cobro.confirming_id IS NULL) THEN
                -- Si es un confirming, lo cuento como cobrado si no está 
                -- pendiente o si ya lo he recibido, ya que si no responde 
                -- el cliente, responderá el banco. Pero lo cuento como 
                -- cobrado solo si se ha indicado una fecha de cobro. Ya que 
                -- si se negocia o se cobra, este campo estará informado.
                -- Y si no está informado, es que es un importe documentado 
                -- (si no no existiría el registro) pero no cobrado ni 
                -- negociado. Estaría impagado/vencido.
                SELECT * INTO registro_confirming
                  FROM confirming 
                 WHERE confirming.id = registro_cobro.confirming_id 
                   AND confirming.fecha_recepcion <= fecha;
                IF (NOT (registro_confirming.fecha_cobrado IS NULL))
                    AND fecha >= registro_confirming.fecha_cobrado THEN
                    cobrado := registro_confirming.cobrado;
                -- Si no tiene fecha de cobrado o ésta todavía no ha llegado 
                -- según la recibida, está documentado, pero no cobrado.
                -- O si no tiene fecha de cobrado en abosulto. Que estaría 
                -- no documentado.
                ELSE
                    cobrado := 0.0;
                END IF;
            ELSE
                -- Es un cobro que no implica efectos futuribles 
                -- (transferencia, contado, etc.). Cuenta como cobrado desde 
                -- el momento en que se recibe.
                IF registro_cobro.fecha <= fecha THEN
                    cobrado := registro_cobro.importe;
                ELSE
                    cobrado := 0.0;
                END IF;
            END IF;
            RETURN cobrado;
        END;
    $$ LANGUAGE plpgsql; -- NEW 26/06/2013 MODIFICADO 0/08/2013

CREATE OR REPLACE FUNCTION cobro_esta_documentado(idcobro INTEGER, 
                                   fecha DATE DEFAULT CURRENT_DATE)
    -- Recibe un ID de cobro y una fecha.
    -- Devuelve el importe documentado PERO NO COBRADO/VENCIDO en esa fecha, 
    -- que depende de:
    --  * Si es una transferencia, efectivo, cheque o cualquier otra cosa 
    --    que no sea un confirming o un pagaré; se cuenta como cobrado en 
    --    cuanto se alcanza la fecha de cobro. Nunca está documentado.
    --  * Si es un confirming o un pagaré cuentan como documentados si 
    --    no tienen informado el campo fecha_cobrado.
    RETURNS FLOAT
    AS $$
        DECLARE
            registro_cobro cobro%ROWTYPE;
            registro_pagare_cobro pagare_cobro%ROWTYPE;
            registro_confirming confirming%ROWTYPE;
            documentado FLOAT;
        BEGIN
            -- Selecciono el cobro en cuestión:
            SELECT * INTO registro_cobro FROM cobro WHERE id = idcobro;
            -- Buscar si es pagaré, confirming u otra cosa:
            IF NOT (registro_cobro.pagare_cobro_id IS NULL) THEN
                SELECT * INTO registro_pagare_cobro 
                  FROM pagare_cobro 
                 WHERE pagare_cobro.id = registro_cobro.pagare_cobro_id;
                -- Si no tiene fecha de cobro o tiene pero es posterior 
                -- a la fecha consultada, está documentado. Si es posterior 
                -- estaría cobrado y si no tiene y dependiendo de la 
                -- fecha del vencimiento, impagado. Contando siempre con que 
                -- se haya recibido en la fecha indicada.
                IF (registro_pagare_cobro.fecha_cobrado IS NULL OR 
                    registro_pagare_cobro.fecha_cobrado > fecha)
                   AND registro_pagare_cobro.fecha_recepcion <= fecha THEN
                    documentado := registro_pagare_cobro.cantidad;
                ELSE
                    documentado := 0.0;
                END IF;
            ELSIF NOT (registro_cobro.confirming_id IS NULL) THEN
                SELECT * INTO registro_confirming 
                  FROM confirming
                 WHERE confirming.id = registro_cobro.confirming_id;
                -- Si no tiene fecha de cobro o tiene pero es posterior 
                -- a la fecha consultada, está documentado. Si es posterior 
                -- estaría cobrado y si no tiene y dependiendo de la 
                -- fecha del vencimiento, impagado.
                IF (registro_confirming.fecha_cobrado IS NULL OR 
                    registro_confirming.fecha_cobrado > fecha) 
                   AND registro_confirming.fecha_recepcion <= fecha THEN
                    documentado := registro_confirming.cantidad;
                ELSE
                    documentado := 0.0;
                END IF;
            ELSE
                -- Es un cobro que no implica efectos futuribles 
                -- (transferencia, contado, etc.). No llega a tener nunca 
                -- un documento de cobro.
                documentado := 0.0;
            END IF;
            RETURN documentado;
        END;
    $$ LANGUAGE plpgsql; -- NEW 7/08/2013

CREATE OR REPLACE FUNCTION calcular_importe_cobrado_factura_venta(idfra INTEGER, 
								  fecha DATE DEFAULT CURRENT_DATE)
    -- Devuelve el importe cobrado en fecha para la factura cuyo id se recibe.
    RETURNS FLOAT
    AS $$
        SELECT COALESCE(SUM(importe), 0) FROM cobro WHERE cobro.factura_venta_id = $1 AND cobro_esta_cobrado(cobro.id, $2) <> 0;
    $$ LANGUAGE SQL;

CREATE OR REPLACE FUNCTION calcular_importe_documentado_factura_venta(
                                idfra INTEGER, 
                                fecha DATE DEFAULT CURRENT_DATE)
    -- Indica el importe documentado y no vencido ni cobrado de la factura.
    RETURNS FLOAT
    AS $$
        SELECT COALESCE(SUM(importe), 0) 
          FROM cobro 
         WHERE cobro.factura_venta_id = $1 
           AND cobro_esta_documentado(cobro.id, $2) <> 0;
    $$ LANGUAGE SQL;    -- NEW! 7/08/2013

CREATE OR REPLACE FUNCTION calcular_importe_vencido_factura_venta(
                                idfra INTEGER, 
                                fecha DATE DEFAULT CURRENT_DATE)
    RETURNS FLOAT
    AS $$
        SELECT COALESCE(SUM(importe), 0) 
          FROM vencimiento_cobro 
         WHERE vencimiento_cobro.factura_venta_id = $1 
           AND vencimiento_cobro.fecha < $2;
    $$ LANGUAGE SQL;

CREATE OR REPLACE FUNCTION calcular_importe_no_vencido_factura_venta(
                                idfra INTEGER, 
                                fecha DATE DEFAULT CURRENT_DATE)
    RETURNS FLOAT
    AS $$
        SELECT COALESCE(SUM(importe), 0) 
          FROM vencimiento_cobro 
         WHERE vencimiento_cobro.factura_venta_id = $1 
           AND vencimiento_cobro.fecha >= $2;
    $$ LANGUAGE SQL;

CREATE OR REPLACE FUNCTION fra_cobrada(idfra INTEGER, 
                                       fecha DATE DEFAULT CURRENT_DATE)
    -- Devuelve TRUE si el importe de los vencimientos es igual al importe 
    -- de los cobros en la fecha recibida.
    RETURNS BOOLEAN
    AS $BODY$
    DECLARE
        cobrado FLOAT;
        vencido FLOAT;
        no_vencido FLOAT;
    BEGIN
        SELECT calcular_importe_cobrado_factura_venta($1, $2) INTO cobrado;
        SELECT calcular_importe_vencido_factura_venta($1, $2) INTO vencido;
        SELECT calcular_importe_no_vencido_factura_venta($1, $2) INTO no_vencido;
        RETURN cobrado != 0 AND ABS(cobrado) >= ABS(vencido + no_vencido);
    END;
    $BODY$ LANGUAGE plpgsql;    -- NEW! 1/08/2013

CREATE OR REPLACE FUNCTION fra_no_documentada(idfra INTEGER, 
                                              fecha DATE DEFAULT CURRENT_DATE)
    -- Fra. no documentada es la que no ha vencido ni tiene cobros porque 
    -- todavía no ha llegado ni un triste pagaré.
    RETURNS BOOLEAN
    AS $$
    DECLARE
        cobrado FLOAT;
        vencido FLOAT;
        no_vencido FLOAT;
        documentado FLOAT;
    BEGIN
        SELECT calcular_importe_documentado_factura_venta($1, $2) INTO documentado;
        SELECT calcular_importe_cobrado_factura_venta($1, $2) INTO cobrado;
        SELECT calcular_importe_vencido_factura_venta($1, $2) INTO vencido;
        SELECT calcular_importe_no_vencido_factura_venta($1, $2) INTO no_vencido;
        RETURN cobrado = 0 AND vencido = 0 AND documentado = 0;     
            -- OJO: Si tiene cobros o está vencida pero la factura tiene 
            -- importe CERO, entonces va a clasificarse como NO DOCUMENTADA.
    END;
    $$ LANGUAGE plpgsql;        -- NEW! 2/08/2013 MODIFIED 7/08/2013

CREATE OR REPLACE FUNCTION fra_no_vencida(idfra INTEGER, 
                                          fecha DATE DEFAULT CURRENT_DATE)
    RETURNS BOOLEAN
    AS $$
    DECLARE
        cobrado FLOAT;
        vencido FLOAT;
        no_vencido FLOAT;
    BEGIN
        SELECT calcular_importe_cobrado_factura_venta($1, $2) INTO cobrado;
        SELECT calcular_importe_vencido_factura_venta($1, $2) INTO vencido;
        SELECT calcular_importe_no_vencido_factura_venta($1, $2) INTO no_vencido;
        RETURN NOT fra_no_documentada($1, $2)   -- Está documentada, pero
               AND vencido = 0;                 -- no ha vencido. Porque si ha vencido algo
                                                -- entonces la factura está cobrada o impagada.
    END;
    $$ LANGUAGE plpgsql;        -- NEW! 2/08/2013

CREATE OR REPLACE FUNCTION fra_impagada(idfra INTEGER, 
                                        fecha DATE DEFAULT CURRENT_DATE)
    -- Factura impagada es la que ha vencido y ese importe (o parte) vencido 
    -- supera el documentado más el cobrado.
    RETURNS BOOLEAN
    AS $$
    DECLARE
        cobrado FLOAT;
        vencido FLOAT;
        documentado FLOAT;
    BEGIN
        SELECT calcular_importe_cobrado_factura_venta($1, $2) INTO cobrado;
        SELECT calcular_importe_vencido_factura_venta($1, $2) INTO vencido;
        SELECT calcular_importe_documentado_factura_venta($1, $2) INTO documentado;
        RETURN cobrado + documentado >= 0 and cobrado + documentado < vencido;
    END;
    $$ LANGUAGE plpgsql;        -- NEW! 2/08/2013

CREATE OR REPLACE FUNCTION fra_abono(idfra INTEGER, 
                                     fecha DATE DEFAULT CURRENT_DATE)
    -- Por compatibilidad con pclases. Pero en realidad ninguna factura de venta 
    -- es de abono. Las de abono van en otra tabla.
    RETURNS BOOLEAN
    AS $$
    BEGIN
        RETURN FALSE;
    END;
    $$ LANGUAGE plpgsql;        -- NEW! 2/08/2013

CREATE OR REPLACE FUNCTION calcular_importe_factura_venta(idfra INTEGER)
    -- Devuelve el importe total de la factura A PARTIR DE LOS VENCIMIENTOS. Si no tiene 
    -- vencimientos asumo que la factura está incompleta, algún usuario está trabajando 
    -- en ella o lo que sea y no la tengo en cuenta para nada.
    RETURNS FLOAT
    AS $$
        SELECT COALESCE(SUM(importe), 0) FROM vencimiento_cobro WHERE vencimiento_cobro.factura_venta_id = $1;
    $$ LANGUAGE SQL;    -- NEW! 5/08/2013

CREATE OR REPLACE FUNCTION calcular_credito_disponible(idcliente INTEGER, 
                                                       fecha DATE DEFAULT CURRENT_DATE, 
                                                       base FLOAT DEFAULT 0.0)
     -- Devuelve el crédito del cliente cuyo id se recibe. La cantidad "base" se resta 
     -- al crédito para el cálculo de crédito en el momento de formalizar un pedido. La 
     -- "base" debería ser el importe del pedido en ese momento y de ese modo saber si 
     -- el pedido se podría servir con el crédito actual. Por ejemplo: un pedido de 1.5k €
     -- (base) no podrá servirse si el crédito es de 1K.
     RETURNS FLOAT
     AS $$
     DECLARE
        sin_documentar FLOAT;
        sin_vencer FLOAT;
        riesgo_concedido FLOAT;
        fraventa RECORD;
        credito FLOAT;
     BEGIN
        SELECT cliente.riesgo_concedido FROM cliente WHERE cliente.id = $1 INTO riesgo_concedido;
        IF riesgo_concedido = -1 THEN
            credito := 'Infinity'; 
        ELSE
            sin_documentar := 0;
            sin_vencer := 0;
            FOR fraventa IN SELECT * FROM factura_venta WHERE factura_venta.cliente_id = $1 LOOP
                IF fra_impagada(fraventa.id, $2) THEN
                    -- OPTIMIZACIÓN. Si alguna factura está impagada, crédito 0. No sigo.
                    RETURN 0;
                ELSIF fra_no_documentada(fraventa.id, $2) THEN
                    sin_documentar := sin_documentar + calcular_importe_factura_venta(fraventa.id);
                ELSIF fra_no_vencida(fraventa.id, $2) THEN
                    sin_vencer := sin_vencer + calcular_importe_factura_venta(fraventa.id);
                END IF;
            END LOOP;
            credito := riesgo_concedido - (sin_documentar + sin_vencer) - base;
        END IF;
        RETURN credito;
     END;
     $$ LANGUAGE plpgsql;    -- NEW! 5/08/2013


