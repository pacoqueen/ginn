API tests
=========

Pequeños *scripts* de control para evitar incoherencias entre ***ginn*** y ***Murano***.

## Sr. Lobo

Corrige las posibles incidencias producidas en la API de traspaso entre ERP ←→ Murano. Se debería ejecutar periódicamente y especialmente antes de `ramanujan.py`.

1. Procesa las importaciones pendientes de artículos procedentes del ERP que puedan quedar en Murano.

2. Recorre todos los artículos de Murano con dimensiones nulas y corrige los campos de acuerdo con los valores del artículo en ***ginn***.

3. Comprueba que no hay ningún producto con tratamiento de series con unidades negativas. Si es así, aborta la ejecución para que se corrija manualmente.

4. Vuelca todos los consumos del ERP pendientes de traspasar a Murano.

  * En el caso de las partidas de carga, si todos los partes de producción fabricados con ella están verificados, consume las balas en Murano.

  * Para los bigbag, comprueba si los partes de producción donde se han consumido están bloqueados. Si es así, consume el bigbag en Murano.

  * Para el resto de materiales sin trazabilidad, decrementa el *stock*.

5. Por cada producto de ***ginn*** sincroniza ERP ← Murano los datos comunes y específicos.

6. Para **cada artículo** de ***ginn***, comprueba que existe en Murano, que es del producto indicado en el ERP y que los valores de peso bruto, neto, superficie, palé, etc. coinciden.

## Ramanujan

> De momento no desglosa por A, B y C y solo se tiene en cuenta el almacén principal `GTX`.

Toma la última hoja de cálculo de inventario y calcula las desviaciones según: existencias inciales + producción en el periodo - ventas - consumos - ajustes = existencias finales.

Las existencias iniciales proceden de la hoja de cálculo.

La producción la extrae de *ginn*.

Las ventas las saca de *Murano* (*SQLServer*).

Los consumos los saca de *ginn*, pero los coteja con los movimientos de tipo consumo en Murano.

Los ajustes los saca de *Murano*.

Las existencias finales las saca de *Murano*.

Finalmente genera una nueva hoja de cálculo con toda la información para que sirva de entrada para la siguiente ejecución.

## Clouseau

Para las posibles desviaciones detectadas por `ramanujan.py` este *script* hace un informe y genera una hoja de cálculo con el rastreo bulto a bulto de los artículos creados en *ginn*.

Idealmente se debe ejecutar **justo después** de `ramanujan.py` para que usen los mismos datos de producción (que cambia en tiempo real) y demás. También es aconsejable hacer una réplica de la base de datos de *PostgreSQL* para comprobaciones posteriores.

## E. F. Codd

Dado que en Murano las existencias totales y por partida se guarda en tablas independientes de las de las series (artículos), a veces muestra totales que no se corresponden con la suma de las series.

Este *script* corrige esas tablas **de *Murano*** para hacerlas coincidir con los acumulados reales de los registros de las series. No afecta al inventario de `ramanujan.py` ya que este se basa solo en las tablas de artículos y movimientos y no en las de acumulados.
