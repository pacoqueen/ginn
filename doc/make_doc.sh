#!/bin/bash

#######################################
## Función para "parsear" argumentos ##
#######################################
getopt_simple()
{
#    echo "getopt_simple()"
#    echo "Los parámetros son '$*'"
    until [ -z "$1" ]; do
#        echo "Procesando parámetro: '$1'"
        if [ ${1:0:1} = '-' ]; then
            tmp=${1:1}               # Elimina "-" inicial
            if [ ${tmp:0:1} = '-' ]; then
                tmp=${tmp:1}         # Si la opción es del tipo "--opt" elimino el 2º
            fi
            parameter=${tmp%%=*}     # Nombre  del parámetro
            value=${tmp##*=}         # Valor (si lo tiene, si no será el propio nombre)
#            echo "Parámetro: '$parameter' - Valor: '$value'"
            eval $"$parameter"=$value
        fi
        shift
    done
}

##################################
## Inicialización de parámetros ##
## Si no se le pasa nada,       ##
## ejecuto todo.                ##
##################################
if [ $# -eq 0 ]; then
    cvschangelogbuilder="si"
    cvs2cl="si"
    postgresql_autodoc="si"
    latex="si"
    pydoc="si"
    sloccount="si"
    copiar="si"
fi

# Paso parámetros al "parser"
getopt_simple $*


ayuda()
{
    echo "Uso: ./make_doc [-cvschangelogbuilder] [-cvs2cl] [-postgresql_autodoc [-create_statistics]] [-latex] [-pydoc] [-sloccount] [-copiar] [-h|--help]"
    echo 
    echo
    echo "NOTA: Para que funcionen las estadísticas en -postgresql_autodoc necesitas tener instalado el paquete postgresql-contrib en el servidor y habilitar la extensión pgstattuple con psql -e -f /usr/share/postgresq/8.0/contrib/pgstattuple.sql ginn. NO USAR EN PRODUCCIÓN o las tablas de rendimiento y estadísticas pasarán a formar parte de la copia de seguridad dificultando después la restauración."
    echo
    echo "NOTA 2: SLOCCount necesita python y sloc2html para generar la documentación en HTML."
}

# Y al lío
if [ $h ]; then
    ayuda
    exit 0
fi

if [ $help ]; then
    ayuda
    exit 0
fi

if [ $cvschangelogbuilder ]; then
    ## CVSChangelogBuilder ##
    echo 
    echo "Ejecutando CVSChangelogBuilder..."
    echo
    
    CVSCLB=`which cvschangelogbuilder`
    if [ -z $CVSCLB ]; then
        CVSCLB=~/cvschangelogbuilder-2.3/cvschangelogbuilder.pl
    fi
    cd ..
    $CVSCLB -output=buildhtmlreport -module=geotexinn02 -dir=./doc #-d=:ext:pacoqueen@ginn.cvs.sourceforge.net:/cvsroot/ginn 
    cd doc
    #mv ../cvschangelogbuilder_geotexinn02*.png .
    mv cvschangelogbuilder_geotexinn02.html cvschangelog.html
fi

if [ $cvs2cl ]; then
    ## cvs2cl ##
    # "Porsiaca"...
    #export CVSROOT=":ext:pacoqueen@ginn.cvs.sourceforge.net/cvsroot/ginn"

    echo 
    echo "Ejecutando CVS to ChangeLog (cvs2cl)..."
    echo
    
    # if [ "$(pwd)" = "" ] Hacer un cd .. si estoy en ./doc.

    CVS2CL=$(which cvs2cl)
    if [ -z "$CVS2CL" ]; then
        CVS2CL=./doc/cvs2cl.pl
    fi

    cd ..
    $CVS2CL --file doc/ChangeLog
    cd doc
fi

if [ $postgresql_autodoc ]; then
    ## Postgresql_autodoc ##
    echo 
    echo "Ejecutando PostgreSQL autodoc (postgresql_autodoc)..."
    echo
    if [ $create_statistics ]; then
        # Esta opción NUNCA estará por defecto para evitar que se ejecute accidentalmente en producción.
        if [ $(ls /usr/share/postgresql/8.0/contrib/pgstattuple.sql 2>/dev/null) ]; then
            echo "Creando funciones estadísticas para PostgreSQL 8.0..."
            psql -e -f /usr/share/postgresql/8.0/contrib/pgstattuple.sql ginn
        else if [ $(ls /usr/share/postgresql/7.4/contrib/pgstattuple.sql 2>/dev/null) ]; then
                echo "Creando funciones estadísticas para PostgreSQL 7.4..."
                psql -e -f /usr/share/postgresql/7.4/contrib/pgstattuple.sql ginn
            else
                echo "No se encontraron funciones estadísticas. Asegúrese de instalar el paquete contrib para su versión."
            fi
        fi
    fi
    postgresql_autodoc -d ginn -u geotexan -h localhost --password=gy298d.l --statistics 
    dot -Tpng ginn.dot > ginn.png
fi

if [ $latex ]; then
    ## LATEX ##
    echo 
    echo "Compilando dev.tex (latex)..."
    echo
    
    latex dev.tex
fi

if [ $pydoc ]; then
    ## PyDoc ##
    echo 
    echo "Ejecutando pydoc con salida a html..."
    echo
    
    cd pydoc
    export PYTHONPATH="../../SQLObject/SQLObject-0.6.1:../../framework:../../formularios:../../informes:../../PyChart-1.39"
    pydoc -w ../../framework/pclases.py 
    pydoc -w ../../framework/configuracion.py
    pydoc -w ../../informes/geninformes.py
    pydoc -w ../../formularios/*.py
    cd ..
fi

if [ $sloccount ]; then
    ## SLOCCount ##
    slocout="doc/sloccount_$(date +%Y_%m_%d).txt"
    echo
    echo "Ejecutando SLOCCount..."
    echo
    cd ..
#    sloccount --addlang sql --addlang html --wide --multiproject . > $slocout
    # Si cuento SQL SLOCCount se come también las copias de seguridad de BD...
    sloccount --addlang html --wide --multiproject --personcost 21600 . > $slocout
    python doc/sloc2html.py $slocout > doc/sloccount.html
    cvs add $slocout
    cvs ci -m "Salida documentación SLOCCount del día $(date +%d/%m/%Y) a las $(date +%H:%M)"
    cd -
fi

if [ $copiar ]; then
    ## Copiar a alfred ##
    echo 
    echo "Copiando documentación a alfred..."
    echo 
    scp -r ginn.png dev.dvi ChangeLog cvschangelog* *.html pydoc/ geotexan@alfred:/var/www
fi
