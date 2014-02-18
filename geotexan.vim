" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 18 febrero 2014 at 17:31:23.
" Open this file in Vim and run :source % to restore your session.

set guioptions=aegimrLtT
silent! set guifont=Inconsolata\ 10
if exists('g:syntax_on') != 1 | syntax on | endif
if exists('g:did_load_filetypes') != 1 | filetype on | endif
if exists('g:did_load_ftplugin') != 1 | filetype plugin on | endif
if exists('g:did_indent_on') != 1 | filetype indent on | endif
if &background != 'light'
	set background=light
endif
if !exists('g:colors_name') || g:colors_name != 'github' | colorscheme github | endif
call setqflist([])
let SessionLoad = 1
if &cp | set nocp | endif
let s:so_save = &so | let s:siso_save = &siso | set so=0 siso=0
let v:this_session=expand("<sfile>:p")
silent only
cd ~/Geotexan/src/Geotex-INN
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
badd +163 ~/.vimrc
badd +1 formularios/auditviewer.py
badd +13 ~/.vim/plugin/ack.vim
badd +249 formularios/consulta_existenciasBolsas.py
badd +1 formularios/dynconsulta.py
badd +1 framework/pclases.py
badd +168 formularios/gestor_mensajes.py
badd +181 formularios/menu.py
badd +85 formularios/autenticacion.py
badd +1 formularios/dynconsulta.glade
badd +179 formularios/consulta_facturas_sin_doc_pago.py
badd +73 formularios/utils_almacen.py
badd +1 ginn/formularios/dynconsulta.glade
badd +279 ginn/formularios/dynconsulta.py
badd +77 ginn/framework/pclases.py
badd +201 ginn/formularios/historico_existencias_compra.py
badd +39 ginn/formularios/historico_existencias.py
badd +46 ginn/formularios/consulta_incidencias.py
badd +757 ginn/formularios/consulta_producido.py
badd +1 ginn/__init__.py
badd +1505 ginn/formularios/clientes.py
badd +991 ginn/formularios/productos_compra.py
badd +39 ginn/formularios/productos_de_venta_balas.py
badd +525 ginn/formularios/recibos.py
badd +603 ginn/formularios/productos_de_venta_rollos.py
badd +382 ginn/formularios/productos_de_venta_rollos_geocompuestos.py
badd +417 ginn/formularios/productos_de_venta_especial.py
badd +1798 ginn/formularios/partes_de_fabricacion_balas.py
badd +580 ginn/formularios/partes_de_fabricacion_bolsas.py
badd +1834 ginn/formularios/partes_de_fabricacion_rollos.py
badd +312 ginn/formularios/proveedores.py
badd +547 ~/workspace/CICAN/src/formularios/menu.py
badd +93 ginn/formularios/launcher.py
badd +625 ginn/formularios/empleados.py
badd +38 ginn/formularios/resultados_geotextiles.py
badd +760 ginn/formularios/menu.py
badd +142 ginn/formularios/autenticacion.py
badd +353 ginn/informes/geninformes.py
badd +233 ginn/informes/informe_certificado_calidad.py
badd +1518 informes/geninformes.py
badd +2349 ginn/formularios/facturas_venta.py
badd +419 ginn/framework/configuracion.py
badd +4 bin/ginn.sh
badd +10 ginn/main.py
badd +750 ginn/formularios/ventana.py
badd +2094 ginn/formularios/pedidos_de_venta.py
badd +3879 db/tablas.sql
badd +1 ginn/formularios/albaranes_de_salida.py
badd +93 ginn/formularios/presupuesto.py
badd +176 ginn/formularios/presupuestos.py
badd +97 ginn/informes/carta_compromiso.py
badd +367 ginn/formularios/tarifas_de_precios.py
badd +88 ginn/formularios/logviewer.py
badd +1527 ginn/formularios/facturas_compra.py
badd +1129 ginn/formularios/utils.py
badd +648 ginn/formularios/resultados_fibra.py
badd +955 ginn/formularios/albaranes_de_entrada.py
badd +611 ginn/formularios/consulta_ventas.py
badd +37 ginn/formularios/__init__.py
badd +907 ginn/formularios/pagares_pagos.py
badd +331 ginn/formularios/ausencias.py
badd +67 ginn/formularios/partes_no_bloqueados.py
badd +218 ginn/formularios/gtkexcepthook.py
badd +402 ginn/framework/seeker.py
badd +13 ginn/formularios/crm_seguimiento_impagos.py
badd +203 ginn/formularios/productos.py
badd +1064 ginn/formularios/trazabilidad_articulos.py
badd +363 ginn/formularios/consulta_pagos.py
badd +13 ginn/formularios/consulta_vencimientos_pago.py
badd +500 ginn/formularios/trazabilidad.py
badd +756 ginn/framework/pclases/__init__.py
badd +494 ginn/framework/pclases/superfacturaventa.py
badd +134 ginn/framework/pclases/facturaventa.py
badd +694 ginn/formularios/consulta_mensual_nominas.py
badd +44 ginn/informes/treeview2pdf.py
badd +163 ginn/formularios/balas_cable.py
badd +13 ginn/informes/nied.py
badd +82 ginn/informes/norma2013.py
badd +65 ginn/formularios/widgets.py
badd +1 ginn/informes/ekotex.py
badd +7 ~/.vim/ftplugin/python.vim
badd +435 ginn/formularios/listado_balas.py
badd +227 ginn/formularios/consulta_pendientes_servir.py
badd +130 ginn/formularios/facturas_no_bloqueadas.py
badd +111 ginn/formularios/consumo_balas_partida.py
badd +324 ginn/formularios/categorias_laborales.py
badd +411 ginn/formularios/nominas.py
badd +511 ginn/framework/pclases/cliente.py
badd +1 ginn/formularios/consulta_cobros.py
badd +1020 ginn/formularios/pagares_cobros.py
badd +24 extra/patches/calcular_credito_disponible.sql
badd +301 ginn/formularios/pclase2tv.py
badd +94 ginn/formularios/consulta_control_horas.py
badd +533 ginn/formularios/horas_trabajadas.py
badd +550 ginn/formularios/horas_trabajadas_dia.py
badd +1 ginn/formularios/pedidos_de_compra.glade
badd +542 ginn/formularios/postomatic.py
badd +18 ginn/formularios/custom_widgets/cellrendererautocomplete.py
badd +47 ginn/formularios/custom_widgets/__init__.py
badd +549 ginn/informes/presupuesto2.py
badd +61 ginn/informes/albaran_multipag.py
badd +192 ginn/formularios/silos.py
badd +1 ginn/framework/__init__.py
badd +1 ginn/formularios/vencimientos_pendientes_por_cliente.glade
badd +365 ginn/formularios/consulta_productividad.py
badd +171 ginn/formularios/mail_sender.py
badd +1143 ginn/formularios/abonos_venta.py
badd +306 ginn/formularios/ventana_progreso.py
badd +993 ginn/formularios/control_personal.py
badd +195 ginn/formularios/listado_rollos.py
badd +74 ginn/formularios/consulta_existenciasRollos.py
badd +91 ginn/formularios/listado_rollos_defectuosos.py
badd +2497 ginn/formularios/consulta_global.py
badd +69 ginn/formularios/rollos_c.py
badd +56 extra/scripts/enviar_exitencias_geotextiles_a_comerciales.py
badd +1 ginn/informes/presupuesto.py
badd +112 ginn/formularios/consulta_libro_iva.py
badd +531 ginn/formularios/consulta_ofertas.py
badd +24 extra/patches/create_ventana_consultas.py
badd +203 ginn/lib/ezodf/ezodf/const.py
badd +61 ginn/lib/ezodf/ezodf/xmlns.py
badd +21 ginn/lib/simple_odspy/simpleodspy/sodsods.py
badd +17 ginn/lib/simple_odspy/simpleodspy/sodsspreadsheet.py
badd +41 ginn/lib/simple_odspy/simpleodspy/sodstable.py
badd +66 ginn/lib/odfpy/contrib/odscell/odscell
badd +127 ginn/lib/odfpy/contrib/odscell/odscell.py
badd +280 ginn/formularios/consulta_ofertas_pendientes_validar.py
badd +538 ginn/formularios/consulta_ofertas_estudio.py
badd +1075 ginn/formularios/confirmings.py
badd +213 ginn/formularios/transferencias.py
badd +66 ginn/formularios/cuentas_destino.py
badd +509 ginn/formularios/facturacion_por_cliente_y_fechas.py
badd +1 ginn/formularios/presupuestos.glade
badd +24 ginn/lib/simple_odspy/simpleodspy/sodsxls.py
badd +1 ginn/formularios/ofer
badd +1 ginn/formularios/usuarios.glade
badd +251 ginn/formularios/usuarios.py
badd +22 ginn/lib/xlutils/xlutils/copy.py
badd +108 ginn/lib/xlutils/xlutils/filter.py
badd +10 ginn/lib/xlutils/xlutils/display.py
badd +8 ginn/lib/xlutils/xlutils/margins.py
badd +1 ginn/lib/xlutils/xlutils/filter.pyç
badd +381 ginn/lib/xlrd/xlrd/__init__.py
badd +9 ginn/lib/xlwt/xlwt/__init__.py
badd +659 ginn/lib/xlwt/xlwt/Workbook.py
badd +123 ginn/formularios/gestor_mensajes.py
badd +450 ginn/formularios/prefacturas.py
badd +1 presupuestos
badd +1 ginn/formularios/consulta_albaranesPorFacturar.glade
badd +393 ginn/formularios/consulta_albaranesPorFacturar.py
badd +1 ginn/formularios/checklist_window.py
badd +506 ginn/formularios/pedidos_de_compra.py
badd +92 ginn/formularios/utils_almacen.py
badd +357 ginn/formularios/consumo_fibra_por_partida_gtx.py
badd +138 ginn/lib/charting.py
badd +66 ginn/formularios/consulta_existenciasBalas.py
badd +247 ginn/formularios/consulta_consumo.py
badd +1 ginn/formularios/consulta_existencias_por_tipo.py
badd +82 ginn/formularios/consulta_existencias.py
badd +1 ginn/formularios/consulta_producido.glade
badd +1 ginn/formularios/consumo_balas_partida.pyç
args formularios/auditviewer.py
set lines=45 columns=101
edit ginn/formularios/albaranes_de_salida.py
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd w
wincmd _ | wincmd |
split
wincmd _ | wincmd |
split
wincmd _ | wincmd |
split
wincmd _ | wincmd |
split
wincmd _ | wincmd |
split
wincmd _ | wincmd |
split
6wincmd k
wincmd w
wincmd w
wincmd w
wincmd w
wincmd w
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
exe 'vert 1resize ' . ((&columns * 20 + 50) / 101)
exe '2resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 2resize ' . ((&columns * 80 + 50) / 101)
exe '3resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 3resize ' . ((&columns * 80 + 50) / 101)
exe '4resize ' . ((&lines * 31 + 22) / 45)
exe 'vert 4resize ' . ((&columns * 80 + 50) / 101)
exe '5resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 5resize ' . ((&columns * 80 + 50) / 101)
exe '6resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 6resize ' . ((&columns * 80 + 50) / 101)
exe '7resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 7resize ' . ((&columns * 80 + 50) / 101)
exe '8resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 8resize ' . ((&columns * 80 + 50) / 101)
argglobal
enew
file __Tag_List__
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=9999
setlocal fml=0
setlocal fdn=20
setlocal fen
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
98
normal! zo
99
normal! zo
111
normal! zo
111
normal! zo
111
normal! zo
1173
normal! zo
2029
normal! zo
2066
normal! zo
2071
normal! zo
2192
normal! zo
2828
normal! zo
3043
normal! zo
3051
normal! zo
3241
normal! zo
3253
normal! zo
3254
normal! zo
3255
normal! zo
4275
normal! zo
let s:l = 4750 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
4750
normal! 020|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/framework/pclases/__init__.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
270
normal! zo
361
normal! zo
370
normal! zo
375
normal! zo
390
normal! zo
644
normal! zo
683
normal! zo
747
normal! zo
757
normal! zo
763
normal! zo
790
normal! zo
1115
normal! zo
1207
normal! zo
1216
normal! zo
1258
normal! zo
1264
normal! zo
1264
normal! zo
1264
normal! zo
1291
normal! zo
1297
normal! zo
1297
normal! zo
1297
normal! zo
1316
normal! zo
1325
normal! zo
1400
normal! zo
1425
normal! zo
1434
normal! zo
1509
normal! zo
1534
normal! zo
1543
normal! zo
1618
normal! zo
1643
normal! zo
1764
normal! zo
2465
normal! zo
2844
normal! zo
3053
normal! zo
3542
normal! zo
3854
normal! zo
3888
normal! zo
3890
normal! zo
3946
normal! zo
3953
normal! zo
3954
normal! zo
3954
normal! zo
3954
normal! zo
3954
normal! zo
3954
normal! zo
3954
normal! zo
3978
normal! zo
4028
normal! zo
4031
normal! zo
4036
normal! zo
4037
normal! zo
4037
normal! zo
4037
normal! zo
4041
normal! zo
4041
normal! zo
4041
normal! zo
4041
normal! zo
4041
normal! zo
4041
normal! zo
4044
normal! zo
4044
normal! zo
4050
normal! zo
4052
normal! zo
4057
normal! zo
4060
normal! zo
4062
normal! zo
4067
normal! zo
4068
normal! zo
4078
normal! zo
4086
normal! zo
4087
normal! zo
4087
normal! zo
4087
normal! zo
4087
normal! zo
4091
normal! zo
4094
normal! zo
4095
normal! zo
4095
normal! zo
4095
normal! zo
4095
normal! zo
4095
normal! zo
4109
normal! zo
4132
normal! zo
4176
normal! zo
4589
normal! zo
4600
normal! zo
4734
normal! zo
4819
normal! zo
4858
normal! zo
4870
normal! zo
4871
normal! zo
4871
normal! zo
4871
normal! zo
5148
normal! zo
5172
normal! zo
5183
normal! zo
5183
normal! zo
5183
normal! zo
5192
normal! zo
5212
normal! zo
5221
normal! zo
5222
normal! zo
5235
normal! zo
5241
normal! zo
5241
normal! zo
5241
normal! zo
5241
normal! zo
5257
normal! zo
5257
normal! zo
5257
normal! zo
5257
normal! zo
5257
normal! zo
5353
normal! zo
5359
normal! zo
5383
normal! zo
5410
normal! zo
5500
normal! zo
5512
normal! zo
5513
normal! zo
5514
normal! zo
5514
normal! zo
5514
normal! zo
5514
normal! zo
5516
normal! zo
5516
normal! zo
5516
normal! zo
5516
normal! zo
5516
normal! zo
5567
normal! zo
5567
normal! zo
5567
normal! zo
5567
normal! zo
5567
normal! zo
5595
normal! zo
5598
normal! zo
5617
normal! zo
5618
normal! zo
5619
normal! zo
5629
normal! zo
5681
normal! zo
5682
normal! zo
5802
normal! zo
5857
normal! zo
5869
normal! zo
5934
normal! zo
5978
normal! zo
5986
normal! zo
6012
normal! zo
6025
normal! zo
6029
normal! zo
6035
normal! zo
6168
normal! zo
6294
normal! zo
7550
normal! zo
7579
normal! zo
7579
normal! zo
7579
normal! zo
7579
normal! zo
7579
normal! zo
7603
normal! zo
7672
normal! zo
7691
normal! zo
7694
normal! zo
7695
normal! zo
7695
normal! zo
7695
normal! zo
7708
normal! zo
7709
normal! zo
7710
normal! zo
7715
normal! zo
7721
normal! zo
7727
normal! zo
7727
normal! zo
7727
normal! zo
7727
normal! zo
7727
normal! zo
7727
normal! zo
7729
normal! zo
7768
normal! zo
7778
normal! zo
7779
normal! zo
7787
normal! zo
7788
normal! zo
7791
normal! zo
7796
normal! zo
7797
normal! zo
7798
normal! zo
7799
normal! zo
7799
normal! zo
7799
normal! zo
7799
normal! zo
7799
normal! zo
7799
normal! zo
7803
normal! zo
7809
normal! zo
7812
normal! zo
7812
normal! zo
7812
normal! zo
7812
normal! zo
7812
normal! zo
7821
normal! zo
7822
normal! zo
7823
normal! zo
7831
normal! zo
7838
normal! zo
7838
normal! zo
7838
normal! zo
7838
normal! zo
7838
normal! zo
7838
normal! zo
7840
normal! zo
7840
normal! zo
7840
normal! zo
7840
normal! zo
7840
normal! zo
7840
normal! zo
7840
normal! zo
7843
normal! zo
7843
normal! zo
7843
normal! zo
7843
normal! zo
7843
normal! zo
7843
normal! zo
7844
normal! zo
7844
normal! zo
7844
normal! zo
7844
normal! zo
7846
normal! zo
7847
normal! zo
7856
normal! zo
7863
normal! zo
7863
normal! zo
7863
normal! zo
7863
normal! zo
7863
normal! zo
7863
normal! zo
7865
normal! zo
7868
normal! zo
7868
normal! zo
7868
normal! zo
7868
normal! zo
7868
normal! zo
7868
normal! zo
7869
normal! zo
7869
normal! zo
7869
normal! zo
7869
normal! zo
7871
normal! zo
7872
normal! zo
7875
normal! zo
7880
normal! zo
7880
normal! zo
7880
normal! zo
7880
normal! zo
7880
normal! zo
7880
normal! zo
7880
normal! zo
7928
normal! zo
7933
normal! zo
7935
normal! zo
7936
normal! zo
7936
normal! zo
7936
normal! zo
7936
normal! zo
7936
normal! zo
7936
normal! zo
7939
normal! zo
7945
normal! zo
7948
normal! zo
7957
normal! zo
7959
normal! zo
7960
normal! zo
7967
normal! zo
7968
normal! zo
7969
normal! zo
7974
normal! zo
7978
normal! zo
7986
normal! zo
7987
normal! zo
7989
normal! zo
7989
normal! zo
7996
normal! zo
7997
normal! zo
7998
normal! zo
7998
normal! zo
7998
normal! zo
7998
normal! zo
7998
normal! zo
7998
normal! zo
7998
normal! zo
7998
normal! zo
8001
normal! zo
8001
normal! zo
8001
normal! zo
8008
normal! zo
8010
normal! zo
8293
normal! zo
8304
normal! zo
8305
normal! zo
8305
normal! zo
8305
normal! zo
8305
normal! zo
8305
normal! zo
8305
normal! zo
8305
normal! zo
8308
normal! zo
8308
normal! zo
8308
normal! zo
8308
normal! zo
8308
normal! zo
8308
normal! zo
8308
normal! zo
8312
normal! zo
8319
normal! zo
8319
normal! zo
8319
normal! zo
8319
normal! zo
8319
normal! zo
8319
normal! zo
8319
normal! zo
8319
normal! zo
8322
normal! zo
8322
normal! zo
8322
normal! zo
8322
normal! zo
8322
normal! zo
8322
normal! zo
8322
normal! zo
8322
normal! zo
8757
normal! zo
8761
normal! zo
8792
normal! zo
8841
normal! zo
8848
normal! zo
9016
normal! zo
9027
normal! zo
9040
normal! zo
9041
normal! zo
9054
normal! zo
9059
normal! zo
9064
normal! zo
9069
normal! zo
9080
normal! zo
9103
normal! zo
9126
normal! zo
9127
normal! zo
9127
normal! zo
9127
normal! zo
9127
normal! zo
9127
normal! zo
9127
normal! zo
9138
normal! zo
9153
normal! zo
9276
normal! zo
9306
normal! zo
9313
normal! zo
9316
normal! zo
9331
normal! zo
9379
normal! zo
9420
normal! zo
9682
normal! zo
9708
normal! zo
9747
normal! zo
9758
normal! zo
9759
normal! zo
9772
normal! zo
9784
normal! zo
9798
normal! zo
9814
normal! zo
9831
normal! zo
9831
normal! zo
9831
normal! zo
9831
normal! zo
9831
normal! zo
9831
normal! zo
9831
normal! zo
9831
normal! zo
9831
normal! zo
9838
normal! zo
9852
normal! zo
9853
normal! zo
9853
normal! zo
9855
normal! zo
9856
normal! zo
9856
normal! zo
9858
normal! zo
9859
normal! zo
9859
normal! zo
9861
normal! zo
9862
normal! zo
9862
normal! zo
9864
normal! zo
9867
normal! zo
9869
normal! zo
9869
normal! zo
9869
normal! zo
9878
normal! zo
9891
normal! zo
9894
normal! zo
9895
normal! zo
9895
normal! zo
9898
normal! zo
9898
normal! zo
9898
normal! zo
9901
normal! zo
9901
normal! zo
9901
normal! zo
9901
normal! zo
9907
normal! zo
9910
normal! zo
9914
normal! zo
9921
normal! zo
9923
normal! zo
9970
normal! zo
9984
normal! zo
9985
normal! zo
9987
normal! zo
10022
normal! zo
10029
normal! zo
10034
normal! zo
10035
normal! zo
10040
normal! zo
10040
normal! zo
10040
normal! zo
10040
normal! zo
10040
normal! zo
10043
normal! zo
10043
normal! zo
10043
normal! zo
10069
normal! zo
10078
normal! zo
10083
normal! zo
10085
normal! zo
10090
normal! zo
10096
normal! zo
10104
normal! zo
10105
normal! zo
10105
normal! zo
10105
normal! zo
10105
normal! zo
10114
normal! zo
10115
normal! zo
10120
normal! zo
10169
normal! zo
10174
normal! zo
10287
normal! zo
10314
normal! zo
10319
normal! zo
10325
normal! zo
10411
normal! zo
10418
normal! zo
10419
normal! zo
10467
normal! zo
10467
normal! zo
10467
normal! zo
10467
normal! zo
10467
normal! zo
10470
normal! zo
10478
normal! zo
10479
normal! zo
10524
normal! zo
10544
normal! zo
10545
normal! zo
10546
normal! zo
10546
normal! zo
10546
normal! zo
10546
normal! zo
10546
normal! zo
10546
normal! zo
10546
normal! zo
10546
normal! zo
10546
normal! zo
10563
normal! zo
10569
normal! zo
10579
normal! zo
10594
normal! zo
10597
normal! zo
10600
normal! zo
10600
normal! zo
10600
normal! zo
10603
normal! zo
10603
normal! zo
10603
normal! zo
10603
normal! zo
10608
normal! zo
10608
normal! zo
10608
normal! zo
10616
normal! zo
10623
normal! zo
10630
normal! zo
10633
normal! zo
10635
normal! zo
10638
normal! zo
10641
normal! zo
10646
normal! zo
10657
normal! zo
10664
normal! zo
10668
normal! zo
10669
normal! zo
10669
normal! zo
10671
normal! zo
10672
normal! zo
10672
normal! zo
10674
normal! zo
10675
normal! zo
10675
normal! zo
10677
normal! zo
10678
normal! zo
10678
normal! zo
10680
normal! zo
10681
normal! zo
10681
normal! zo
10683
normal! zo
10684
normal! zo
10684
normal! zo
10686
normal! zo
10687
normal! zo
10687
normal! zo
10689
normal! zo
10692
normal! zo
10694
normal! zo
10694
normal! zo
10694
normal! zo
10700
normal! zo
10701
normal! zo
10701
normal! zo
10703
normal! zo
10704
normal! zo
10704
normal! zo
10728
normal! zo
10732
normal! zo
10735
normal! zo
10736
normal! zo
10736
normal! zo
10736
normal! zo
10736
normal! zo
10736
normal! zo
10736
normal! zo
10741
normal! zo
10742
normal! zo
10742
normal! zo
10742
normal! zo
10745
normal! zo
10857
normal! zo
10933
normal! zo
10941
normal! zo
10948
normal! zo
10948
normal! zo
10948
normal! zo
10948
normal! zo
10948
normal! zo
10948
normal! zo
10948
normal! zo
10959
normal! zo
10963
normal! zo
10964
normal! zo
10964
normal! zo
10964
normal! zo
10974
normal! zo
10977
normal! zo
10984
normal! zo
10993
normal! zo
11002
normal! zo
11112
normal! zo
11126
normal! zo
11126
normal! zo
11126
normal! zo
11126
normal! zo
11138
normal! zo
11151
normal! zo
11164
normal! zo
11171
normal! zo
11173
normal! zo
11173
normal! zo
11173
normal! zo
11173
normal! zo
11173
normal! zo
11173
normal! zo
11198
normal! zo
11226
normal! zo
11238
normal! zo
11239
normal! zo
11239
normal! zo
11239
normal! zo
11239
normal! zo
11410
normal! zo
11418
normal! zo
11418
normal! zo
11418
normal! zo
11418
normal! zo
11432
normal! zo
11443
normal! zo
11460
normal! zo
11460
normal! zo
11464
normal! zo
11469
normal! zo
11469
normal! zo
11471
normal! zo
11472
normal! zo
11472
normal! zo
11477
normal! zo
11477
normal! zo
11477
normal! zo
11477
normal! zo
11477
normal! zo
11490
normal! zo
11493
normal! zo
11493
normal! zo
11493
normal! zo
11493
normal! zo
11499
normal! zo
11499
normal! zo
11499
normal! zo
11499
normal! zo
11499
normal! zo
11527
normal! zo
11625
normal! zo
11625
normal! zo
11625
normal! zo
11625
normal! zo
11625
normal! zo
11625
normal! zo
11625
normal! zo
11625
normal! zo
11625
normal! zo
11625
normal! zo
11646
normal! zo
11646
normal! zo
11646
normal! zo
11646
normal! zo
11646
normal! zo
11646
normal! zo
11687
normal! zo
11688
normal! zo
11710
normal! zo
11866
normal! zo
11866
normal! zo
12015
normal! zo
12015
normal! zo
12015
normal! zo
12029
normal! zo
12066
normal! zo
12077
normal! zo
12082
normal! zo
12100
normal! zo
12100
normal! zo
12100
normal! zo
12100
normal! zo
12101
normal! zo
12106
normal! zo
12122
normal! zo
12122
normal! zo
12122
normal! zo
12122
normal! zo
12131
normal! zo
12131
normal! zo
12131
normal! zo
12131
normal! zo
12131
normal! zo
12155
normal! zo
13318
normal! zo
13452
normal! zo
13452
normal! zo
13452
normal! zo
13462
normal! zo
13467
normal! zo
13468
normal! zo
13469
normal! zo
13469
normal! zo
13469
normal! zo
13469
normal! zo
13469
normal! zo
13469
normal! zo
13469
normal! zo
13469
normal! zo
13469
normal! zo
13469
normal! zo
13475
normal! zo
13476
normal! zo
13477
normal! zo
13477
normal! zo
13477
normal! zo
13477
normal! zo
13477
normal! zo
13477
normal! zo
13477
normal! zo
13479
normal! zo
13479
normal! zo
13479
normal! zo
13479
normal! zo
13479
normal! zo
13479
normal! zo
13479
normal! zo
13479
normal! zo
13481
normal! zo
13482
normal! zo
13482
normal! zo
13482
normal! zo
13482
normal! zo
13482
normal! zo
13482
normal! zo
13482
normal! zo
13482
normal! zo
13482
normal! zo
13485
normal! zo
13487
normal! zo
13487
normal! zo
13492
normal! zo
13492
normal! zo
13502
normal! zo
13503
normal! zo
13503
normal! zo
13503
normal! zo
13503
normal! zo
13503
normal! zo
13503
normal! zo
13622
normal! zo
13622
normal! zo
13622
normal! zo
13643
normal! zo
13648
normal! zo
13649
normal! zo
13650
normal! zo
13650
normal! zo
13650
normal! zo
13650
normal! zo
13650
normal! zo
13650
normal! zo
13650
normal! zo
13650
normal! zo
13650
normal! zo
13650
normal! zo
13656
normal! zo
13657
normal! zo
13658
normal! zo
13658
normal! zo
13658
normal! zo
13658
normal! zo
13658
normal! zo
13658
normal! zo
13658
normal! zo
13660
normal! zo
13660
normal! zo
13660
normal! zo
13660
normal! zo
13660
normal! zo
13660
normal! zo
13660
normal! zo
13660
normal! zo
13662
normal! zo
13663
normal! zo
13663
normal! zo
13663
normal! zo
13663
normal! zo
13663
normal! zo
13663
normal! zo
13663
normal! zo
13663
normal! zo
13663
normal! zo
13666
normal! zo
13668
normal! zo
13673
normal! zo
13682
normal! zo
13683
normal! zo
13683
normal! zo
13683
normal! zo
13683
normal! zo
13683
normal! zo
13683
normal! zo
13683
normal! zo
13753
normal! zo
13753
normal! zo
13753
normal! zo
13764
normal! zo
13769
normal! zo
13770
normal! zo
13771
normal! zo
13771
normal! zo
13771
normal! zo
13771
normal! zo
13771
normal! zo
13771
normal! zo
13771
normal! zo
13771
normal! zo
13771
normal! zo
13771
normal! zo
13777
normal! zo
13778
normal! zo
13779
normal! zo
13779
normal! zo
13779
normal! zo
13779
normal! zo
13779
normal! zo
13779
normal! zo
13779
normal! zo
13781
normal! zo
13781
normal! zo
13781
normal! zo
13781
normal! zo
13781
normal! zo
13781
normal! zo
13781
normal! zo
13781
normal! zo
13783
normal! zo
13784
normal! zo
13784
normal! zo
13784
normal! zo
13784
normal! zo
13784
normal! zo
13784
normal! zo
13784
normal! zo
13784
normal! zo
13784
normal! zo
13787
normal! zo
13789
normal! zo
13794
normal! zo
13803
normal! zo
13804
normal! zo
13804
normal! zo
13804
normal! zo
13804
normal! zo
13804
normal! zo
13804
normal! zo
13804
normal! zo
13911
normal! zo
13911
normal! zo
13911
normal! zo
13911
normal! zo
13911
normal! zo
13911
normal! zo
13911
normal! zo
13911
normal! zo
13911
normal! zo
13921
normal! zo
13921
normal! zo
13921
normal! zo
13921
normal! zo
13921
normal! zo
13921
normal! zo
13923
normal! zo
13924
normal! zo
13924
normal! zo
13924
normal! zo
14119
normal! zo
14119
normal! zo
14119
normal! zo
14119
normal! zo
14135
normal! zo
14140
normal! zo
14141
normal! zo
14142
normal! zo
14142
normal! zo
14142
normal! zo
14142
normal! zo
14142
normal! zo
14142
normal! zo
14142
normal! zo
14142
normal! zo
14142
normal! zo
14142
normal! zo
14148
normal! zo
14149
normal! zo
14150
normal! zo
14150
normal! zo
14150
normal! zo
14150
normal! zo
14150
normal! zo
14150
normal! zo
14150
normal! zo
14152
normal! zo
14152
normal! zo
14152
normal! zo
14152
normal! zo
14152
normal! zo
14152
normal! zo
14152
normal! zo
14152
normal! zo
14152
normal! zo
14154
normal! zo
14155
normal! zo
14155
normal! zo
14155
normal! zo
14155
normal! zo
14155
normal! zo
14155
normal! zo
14155
normal! zo
14155
normal! zo
14155
normal! zo
14158
normal! zo
14160
normal! zo
14160
normal! zo
14165
normal! zo
14165
normal! zo
14175
normal! zo
14176
normal! zo
14176
normal! zo
14176
normal! zo
14176
normal! zo
14176
normal! zo
14176
normal! zo
14236
normal! zo
14236
normal! zo
14236
normal! zo
14236
normal! zo
14248
normal! zo
14253
normal! zo
14254
normal! zo
14255
normal! zo
14255
normal! zo
14255
normal! zo
14255
normal! zo
14255
normal! zo
14255
normal! zo
14255
normal! zo
14255
normal! zo
14255
normal! zo
14255
normal! zo
14261
normal! zo
14262
normal! zo
14263
normal! zo
14263
normal! zo
14263
normal! zo
14263
normal! zo
14263
normal! zo
14263
normal! zo
14263
normal! zo
14265
normal! zo
14265
normal! zo
14265
normal! zo
14265
normal! zo
14265
normal! zo
14265
normal! zo
14265
normal! zo
14265
normal! zo
14265
normal! zo
14267
normal! zo
14268
normal! zo
14268
normal! zo
14268
normal! zo
14268
normal! zo
14268
normal! zo
14268
normal! zo
14268
normal! zo
14268
normal! zo
14268
normal! zo
14271
normal! zo
14273
normal! zo
14273
normal! zo
14278
normal! zo
14278
normal! zo
14288
normal! zo
14289
normal! zo
14289
normal! zo
14289
normal! zo
14289
normal! zo
14289
normal! zo
14289
normal! zo
14357
normal! zo
14369
normal! zo
14372
normal! zo
14373
normal! zo
14374
normal! zo
14374
normal! zo
14374
normal! zo
14376
normal! zo
14377
normal! zo
14377
normal! zo
14377
normal! zo
14393
normal! zo
14404
normal! zo
14413
normal! zo
14423
normal! zo
14450
normal! zo
14455
normal! zo
14461
normal! zo
14472
normal! zo
14485
normal! zo
14509
normal! zo
14511
normal! zo
14514
normal! zo
14517
normal! zo
14518
normal! zo
14522
normal! zo
14523
normal! zo
14537
normal! zo
14537
normal! zo
14537
normal! zo
14537
normal! zo
14559
normal! zo
14560
normal! zo
14561
normal! zo
14561
normal! zo
14561
normal! zo
14561
normal! zo
14561
normal! zo
14561
normal! zo
14561
normal! zo
14561
normal! zo
14561
normal! zo
14561
normal! zo
14570
normal! zo
14571
normal! zo
14577
normal! zo
14581
normal! zo
14582
normal! zo
14591
normal! zo
14592
normal! zo
14600
normal! zo
14601
normal! zo
14607
normal! zo
14622
normal! zo
14630
normal! zo
14636
normal! zo
14642
normal! zo
14647
normal! zo
14651
normal! zo
14657
normal! zo
14662
normal! zo
14663
normal! zo
14668
normal! zo
14679
normal! zo
14697
normal! zo
14739
normal! zo
14745
normal! zo
14751
normal! zo
14758
normal! zo
14767
normal! zo
14769
normal! zo
14776
normal! zo
14776
normal! zo
14776
normal! zo
14776
normal! zo
14776
normal! zo
14776
normal! zo
14793
normal! zo
14805
normal! zo
14816
normal! zo
14817
normal! zo
14833
normal! zo
14850
normal! zo
14854
normal! zo
14855
normal! zo
14856
normal! zo
14856
normal! zo
14858
normal! zo
14861
normal! zo
14874
normal! zo
14884
normal! zo
14886
normal! zo
14890
normal! zo
14891
normal! zo
14891
normal! zo
14891
normal! zo
14891
normal! zo
14891
normal! zo
14891
normal! zo
14904
normal! zo
14925
normal! zo
14926
normal! zo
14933
normal! zo
14966
normal! zo
14967
normal! zo
14967
normal! zo
14983
normal! zo
14989
normal! zo
14992
normal! zo
14992
normal! zo
14992
normal! zo
14998
normal! zo
14998
normal! zo
15018
normal! zo
15023
normal! zo
15028
normal! zo
15036
normal! zo
15055
normal! zo
15089
normal! zo
15097
normal! zo
15106
normal! zo
15125
normal! zo
15127
normal! zo
15131
normal! zo
15148
normal! zo
15154
normal! zo
15158
normal! zo
15490
normal! zo
15521
normal! zo
15545
normal! zo
15555
normal! zo
15555
normal! zo
15555
normal! zo
15555
normal! zo
15555
normal! zo
15743
normal! zo
15762
normal! zo
15784
normal! zo
15789
normal! zo
15790
normal! zo
15790
normal! zo
15793
normal! zo
15794
normal! zo
15794
normal! zo
15794
normal! zo
15797
normal! zo
15797
normal! zo
15797
normal! zo
15801
normal! zo
15801
normal! zo
15801
normal! zo
15801
normal! zo
15801
normal! zo
15801
normal! zo
15801
normal! zo
15801
normal! zo
15801
normal! zo
16332
normal! zo
16368
normal! zo
16383
normal! zo
16389
normal! zo
16392
normal! zo
16400
normal! zo
16401
normal! zo
16401
normal! zo
16401
normal! zo
16401
normal! zo
16401
normal! zo
16405
normal! zo
16413
normal! zo
16416
normal! zo
16422
normal! zo
16428
normal! zo
16431
normal! zo
16437
normal! zo
16451
normal! zo
16457
normal! zo
16462
normal! zo
16465
normal! zo
16465
normal! zo
16465
normal! zo
16475
normal! zo
16490
normal! zo
16501
normal! zo
16501
normal! zo
16512
normal! zo
16527
normal! zo
16537
normal! zo
16548
normal! zo
16557
normal! zo
16564
normal! zo
16602
normal! zo
16607
normal! zo
16607
normal! zo
16607
normal! zo
16620
normal! zo
16620
normal! zo
16620
normal! zo
16620
normal! zo
16620
normal! zo
16620
normal! zo
16620
normal! zo
16620
normal! zo
16620
normal! zo
16620
normal! zo
16620
normal! zo
16632
normal! zo
16653
normal! zo
16672
normal! zo
16680
normal! zo
16681
normal! zo
16682
normal! zo
16686
normal! zo
16690
normal! zo
16706
normal! zo
16721
normal! zo
16726
normal! zo
16731
normal! zo
16741
normal! zo
16742
normal! zo
16742
normal! zo
16742
normal! zo
16744
normal! zo
16744
normal! zo
16744
normal! zo
16744
normal! zo
16744
normal! zo
16744
normal! zo
16744
normal! zo
16744
normal! zo
16744
normal! zo
16744
normal! zo
16749
normal! zo
16750
normal! zo
16756
normal! zo
16757
normal! zo
16777
normal! zo
16802
normal! zo
16806
normal! zo
16823
normal! zo
16834
normal! zo
16834
normal! zo
16834
normal! zo
16834
normal! zo
16836
normal! zo
16837
normal! zo
16838
normal! zo
16839
normal! zo
16840
normal! zo
16844
normal! zo
16845
normal! zo
16846
normal! zo
16846
normal! zo
16846
normal! zo
16846
normal! zo
16846
normal! zo
16846
normal! zo
16846
normal! zo
16848
normal! zo
16850
normal! zo
16855
normal! zo
16855
normal! zo
16855
normal! zo
16855
normal! zo
16861
normal! zo
16865
normal! zo
16873
normal! zo
16873
normal! zo
16873
normal! zo
16873
normal! zo
16881
normal! zo
16889
normal! zo
16890
normal! zo
16893
normal! zo
16898
normal! zo
16906
normal! zo
16911
normal! zo
16919
normal! zo
16924
normal! zo
16933
normal! zo
16934
normal! zo
16934
normal! zo
16944
normal! zo
16959
normal! zo
16960
normal! zo
16976
normal! zo
16996
normal! zo
16997
normal! zo
16997
normal! zo
16997
normal! zo
16997
normal! zo
16997
normal! zo
17003
normal! zo
17013
normal! zo
17027
normal! zo
17030
normal! zo
17034
normal! zo
17035
normal! zo
17036
normal! zo
17036
normal! zo
17036
normal! zo
17036
normal! zo
17036
normal! zo
17054
normal! zo
17061
normal! zo
17062
normal! zo
17069
normal! zo
17076
normal! zo
17077
normal! zo
17078
normal! zo
17083
normal! zo
17090
normal! zo
17095
normal! zo
17108
normal! zo
17109
normal! zo
17109
normal! zo
17109
normal! zo
17114
normal! zo
17127
normal! zo
17134
normal! zo
17135
normal! zo
17150
normal! zo
17157
normal! zo
17171
normal! zo
17178
normal! zo
17179
normal! zo
17184
normal! zo
17193
normal! zo
17207
normal! zo
17229
normal! zo
17250
normal! zo
17263
normal! zo
17263
normal! zo
17263
normal! zo
17263
normal! zo
17263
normal! zo
17263
normal! zo
17273
normal! zo
17286
normal! zo
17310
normal! zo
17315
normal! zo
17317
normal! zo
17320
normal! zo
17327
normal! zo
17339
normal! zo
17349
normal! zo
17349
normal! zo
17349
normal! zo
17349
normal! zo
17349
normal! zo
17349
normal! zo
17357
normal! zo
17367
normal! zo
17367
normal! zo
17367
normal! zo
17367
normal! zo
17367
normal! zo
17367
normal! zo
17375
normal! zo
17376
normal! zo
17387
normal! zo
17392
normal! zo
17403
normal! zo
17411
normal! zo
17424
normal! zo
17428
normal! zo
17428
normal! zo
17428
normal! zo
17428
normal! zo
17428
normal! zo
17430
normal! zo
17442
normal! zo
17442
normal! zo
17442
normal! zo
17442
normal! zo
17442
normal! zo
17442
normal! zo
17442
normal! zo
17446
normal! zo
17446
normal! zo
17446
normal! zo
17446
normal! zo
17446
normal! zo
17446
normal! zo
17452
normal! zo
17452
normal! zo
17452
normal! zo
17452
normal! zo
17455
normal! zo
17456
normal! zo
17457
normal! zo
17463
normal! zo
17464
normal! zo
17464
normal! zo
17464
normal! zo
17586
normal! zo
17674
normal! zo
17731
normal! zo
17746
normal! zo
17753
normal! zo
17754
normal! zo
17770
normal! zo
17780
normal! zo
17794
normal! zo
17797
normal! zo
17798
normal! zo
17798
normal! zo
17820
normal! zo
17840
normal! zo
17852
normal! zo
17852
normal! zo
17852
normal! zo
17852
normal! zo
17852
normal! zo
17855
normal! zo
17862
normal! zo
17865
normal! zo
17876
normal! zo
17882
normal! zo
17887
normal! zo
17893
normal! zo
17894
normal! zo
17895
normal! zo
17898
normal! zo
17917
normal! zo
17932
normal! zo
17960
normal! zo
17985
normal! zo
18006
normal! zo
18041
normal! zo
18050
normal! zo
18051
normal! zo
18052
normal! zo
18054
normal! zo
18054
normal! zo
18054
normal! zo
18057
normal! zo
18059
normal! zo
18059
normal! zo
18059
normal! zo
18062
normal! zo
18063
normal! zo
18063
normal! zo
18063
normal! zo
18063
normal! zo
18063
normal! zo
18589
normal! zo
18606
normal! zo
18616
normal! zo
18619
normal! zo
18620
normal! zo
18620
normal! zo
18626
normal! zo
18633
normal! zo
18634
normal! zo
18635
normal! zo
18635
normal! zo
18635
normal! zo
18635
normal! zo
18639
normal! zo
18640
normal! zo
18640
normal! zo
18640
normal! zo
18640
normal! zo
18656
normal! zo
18957
normal! zo
19874
normal! zo
19898
normal! zo
19904
normal! zo
19910
normal! zo
19928
normal! zo
19938
normal! zo
19941
normal! zo
19948
normal! zo
19948
normal! zo
19948
normal! zo
19948
normal! zo
19953
normal! zo
20233
normal! zo
20239
normal! zo
20239
normal! zo
20248
normal! zo
20255
normal! zo
20262
normal! zo
20269
normal! zo
20276
normal! zo
20283
normal! zo
20290
normal! zo
20296
normal! zo
20297
normal! zo
20306
normal! zo
20315
normal! zo
20478
normal! zo
20488
normal! zo
20499
normal! zo
20510
normal! zo
20511
normal! zo
20516
normal! zo
20517
normal! zo
20517
normal! zo
20527
normal! zo
20527
normal! zo
20527
normal! zo
20527
normal! zo
20527
normal! zo
20527
normal! zo
20527
normal! zo
20527
normal! zo
20527
normal! zo
20538
normal! zo
20539
normal! zo
20547
normal! zo
20547
normal! zo
20547
normal! zo
20547
normal! zo
20547
normal! zo
20547
normal! zo
20547
normal! zo
20547
normal! zo
20558
normal! zo
20559
normal! zo
20615
normal! zo
20636
normal! zo
20641
normal! zo
20653
normal! zo
20653
normal! zo
20653
normal! zo
20653
normal! zo
20653
normal! zo
20653
normal! zo
20653
normal! zo
20671
normal! zo
20678
normal! zo
let s:l = 15135 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
15135
normal! 043|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/presupuestos.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
67
normal! zo
68
normal! zo
160
normal! zo
160
normal! zo
160
normal! zo
167
normal! zo
168
normal! zo
223
normal! zo
270
normal! zo
275
normal! zo
279
normal! zo
280
normal! zo
280
normal! zo
281
normal! zo
281
normal! zo
423
normal! zo
432
normal! zo
478
normal! zo
486
normal! zo
487
normal! zo
487
normal! zo
487
normal! zo
487
normal! zo
487
normal! zo
490
normal! zo
490
normal! zo
510
normal! zo
512
normal! zo
513
normal! zo
516
normal! zo
516
normal! zo
524
normal! zo
526
normal! zo
527
normal! zo
528
normal! zo
539
normal! zo
541
normal! zo
559
normal! zo
778
normal! zo
797
normal! zo
830
normal! zo
892
normal! zo
926
normal! zo
941
normal! zo
951
normal! zo
1086
normal! zo
1102
normal! zo
1118
normal! zo
1118
normal! zo
1118
normal! zo
1118
normal! zo
1118
normal! zo
1118
normal! zo
1651
normal! zo
1695
normal! zo
1699
normal! zo
1703
normal! zo
1712
normal! zo
1714
normal! zo
2183
normal! zo
2202
normal! zo
2203
normal! zo
2204
normal! zo
2209
normal! zo
2209
normal! zo
2261
normal! zo
2263
normal! zo
2266
normal! zo
2268
normal! zo
2565
normal! zo
2581
normal! zo
2583
normal! zo
2651
normal! zo
2657
normal! zo
2666
normal! zo
2684
normal! zo
2763
normal! zo
2963
normal! zo
2977
normal! zo
2982
normal! zo
2988
normal! zo
3001
normal! zo
3009
normal! zo
3080
normal! zo
3094
normal! zo
let s:l = 3110 - ((25 * winheight(0) + 15) / 31)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3110
normal! 046|
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/consulta_existencias_por_tipo.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
46
normal! zo
47
normal! zo
51
normal! zo
51
normal! zo
57
normal! zo
63
normal! zo
72
normal! zo
80
normal! zo
87
normal! zo
88
normal! zo
90
normal! zo
91
normal! zo
100
normal! zo
107
normal! zo
127
normal! zo
135
normal! zo
141
normal! zo
146
normal! zo
148
normal! zo
148
normal! zo
148
normal! zo
149
normal! zo
157
normal! zo
169
normal! zo
170
normal! zo
177
normal! zo
194
normal! zo
223
normal! zo
223
normal! zo
223
normal! zo
223
normal! zo
223
normal! zo
223
normal! zo
231
normal! zo
240
normal! zo
240
normal! zo
240
normal! zo
240
normal! zo
240
normal! zo
240
normal! zo
240
normal! zo
240
normal! zo
240
normal! zo
let s:l = 130 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
130
normal! 013|
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/consulta_cobros.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
50
normal! zo
274
normal! zo
let s:l = 322 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
322
normal! 023|
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/ventana.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
66
normal! zo
104
normal! zo
105
normal! zo
105
normal! zo
137
normal! zo
154
normal! zo
155
normal! zo
161
normal! zo
169
normal! zo
170
normal! zo
210
normal! zo
210
normal! zo
210
normal! zo
210
normal! zo
210
normal! zo
210
normal! zo
210
normal! zo
211
normal! zo
211
normal! zo
211
normal! zo
211
normal! zo
576
normal! zo
580
normal! zo
922
normal! zo
1068
normal! zo
1124
normal! zo
1140
normal! zo
1145
normal! zo
1146
normal! zo
1146
normal! zo
1146
normal! zo
1148
normal! zo
let s:l = 1147 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1147
normal! 09|
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/framework/configuracion.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
71
normal! zo
85
normal! zo
435
normal! zo
461
normal! zo
461
normal! zo
461
normal! zo
503
normal! zo
let s:l = 456 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
456
normal! 027|
wincmd w
4wincmd w
exe 'vert 1resize ' . ((&columns * 20 + 50) / 101)
exe '2resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 2resize ' . ((&columns * 80 + 50) / 101)
exe '3resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 3resize ' . ((&columns * 80 + 50) / 101)
exe '4resize ' . ((&lines * 31 + 22) / 45)
exe 'vert 4resize ' . ((&columns * 80 + 50) / 101)
exe '5resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 5resize ' . ((&columns * 80 + 50) / 101)
exe '6resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 6resize ' . ((&columns * 80 + 50) / 101)
exe '7resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 7resize ' . ((&columns * 80 + 50) / 101)
exe '8resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 8resize ' . ((&columns * 80 + 50) / 101)
tabnext 1
if exists('s:wipebuf')
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=20 shortmess=filnxtToO
let s:sx = expand("<sfile>:p:r")."x.vim"
if file_readable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &so = s:so_save | let &siso = s:siso_save
doautoall SessionLoadPost
unlet SessionLoad
tabnext 1
4wincmd w

" vim: ft=vim ro nowrap smc=128
