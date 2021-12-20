# Intercambio de información entre Geotex-INN y SAP



~~Durante el primer trimestre de 2021 estaremos simultaneando SAP Business One con el montaje de Boyum BEAS. Necesitaremos seguir manteniendo la producción en Geotex-INN y volcando las existencias a SAP como lo hacemos actualmente con Murano.~~

Se cancela hasta 2022. Probablemente no haga falta la integración entonces.

UPDATE dicembre 2022: Será necesaria integración externa con las básculas. SAP leerá el peso de las básculas de un fichero de texto. Aquí entra `toodles` al rescate. Será un _demonio_ corriendo de fondo que cada cierto tiempo leerá el valor actual de la báscula y lo guardará en ese fichero.
