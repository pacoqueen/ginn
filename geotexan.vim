" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 20 febrero 2014 at 01:12:43.
" Open this file in Vim and run :source % to restore your session.

set guioptions=aegimrLtT
silent! set guifont=Inconsolata\ 11
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
badd +284 ginn/formularios/consulta_producido.py
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
badd +13 ginn/framework/configuracion.py
badd +4 bin/ginn.sh
badd +10 ginn/main.py
badd +750 ginn/formularios/ventana.py
badd +2094 ginn/formularios/pedidos_de_venta.py
badd +3879 db/tablas.sql
badd +5 ginn/formularios/albaranes_de_salida.py
badd +93 ginn/formularios/presupuesto.py
badd +2619 ginn/formularios/presupuestos.py
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
badd +500 ginn/formularios/consulta_global.py
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
badd +52 ginn/formularios/consumo_fibra_por_partida_gtx.py
badd +138 ginn/lib/charting.py
badd +66 ginn/formularios/consulta_existenciasBalas.py
badd +247 ginn/formularios/consulta_consumo.py
badd +179 ginn/formularios/consulta_existencias_por_tipo.py
badd +82 ginn/formularios/consulta_existencias.py
badd +1 ginn/formularios/consulta_producido.glade
badd +1 ginn/formularios/consumo_balas_partida.pyç
badd +0 extra/scripts/clouseau.py
badd +92 ginn/informes/treeview2csv.py
badd +206 ginn/formularios/consulta_ventas_por_producto.py
args formularios/auditviewer.py
set lines=57 columns=100
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
11wincmd k
wincmd w
wincmd w
wincmd w
wincmd w
wincmd w
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
exe 'vert 1resize ' . ((&columns * 19 + 50) / 100)
exe '2resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 2resize ' . ((&columns * 80 + 50) / 100)
exe '3resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 3resize ' . ((&columns * 80 + 50) / 100)
exe '4resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 4resize ' . ((&columns * 80 + 50) / 100)
exe '5resize ' . ((&lines * 33 + 28) / 57)
exe 'vert 5resize ' . ((&columns * 80 + 50) / 100)
exe '6resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 6resize ' . ((&columns * 80 + 50) / 100)
exe '7resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 7resize ' . ((&columns * 80 + 50) / 100)
exe '8resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 8resize ' . ((&columns * 80 + 50) / 100)
exe '9resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 9resize ' . ((&columns * 80 + 50) / 100)
exe '10resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 10resize ' . ((&columns * 80 + 50) / 100)
exe '11resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 11resize ' . ((&columns * 80 + 50) / 100)
exe '12resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 12resize ' . ((&columns * 80 + 50) / 100)
exe '13resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 13resize ' . ((&columns * 80 + 50) / 100)
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
let s:l = 4756 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
4756
normal! 0
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
6888
normal! zo
7138
normal! zo
7557
normal! zo
7586
normal! zo
7586
normal! zo
7586
normal! zo
7586
normal! zo
7586
normal! zo
7610
normal! zo
7679
normal! zo
7698
normal! zo
7701
normal! zo
7702
normal! zo
7702
normal! zo
7702
normal! zo
7715
normal! zo
7716
normal! zo
7717
normal! zo
7722
normal! zo
7728
normal! zo
7734
normal! zo
7734
normal! zo
7734
normal! zo
7734
normal! zo
7734
normal! zo
7734
normal! zo
7736
normal! zo
7775
normal! zo
7785
normal! zo
7786
normal! zo
7794
normal! zo
7795
normal! zo
7798
normal! zo
7803
normal! zo
7804
normal! zo
7805
normal! zo
7806
normal! zo
7806
normal! zo
7806
normal! zo
7806
normal! zo
7806
normal! zo
7806
normal! zo
7810
normal! zo
7816
normal! zo
7819
normal! zo
7819
normal! zo
7819
normal! zo
7819
normal! zo
7819
normal! zo
7828
normal! zo
7829
normal! zo
7830
normal! zo
7838
normal! zo
7845
normal! zo
7845
normal! zo
7845
normal! zo
7845
normal! zo
7845
normal! zo
7845
normal! zo
7847
normal! zo
7847
normal! zo
7847
normal! zo
7847
normal! zo
7847
normal! zo
7847
normal! zo
7847
normal! zo
7850
normal! zo
7850
normal! zo
7850
normal! zo
7850
normal! zo
7850
normal! zo
7850
normal! zo
7851
normal! zo
7851
normal! zo
7851
normal! zo
7851
normal! zo
7853
normal! zo
7854
normal! zo
7863
normal! zo
7870
normal! zo
7870
normal! zo
7870
normal! zo
7870
normal! zo
7870
normal! zo
7870
normal! zo
7872
normal! zo
7875
normal! zo
7875
normal! zo
7875
normal! zo
7875
normal! zo
7875
normal! zo
7875
normal! zo
7876
normal! zo
7876
normal! zo
7876
normal! zo
7876
normal! zo
7878
normal! zo
7879
normal! zo
7882
normal! zo
7887
normal! zo
7887
normal! zo
7887
normal! zo
7887
normal! zo
7887
normal! zo
7887
normal! zo
7887
normal! zo
7935
normal! zo
7940
normal! zo
7942
normal! zo
7943
normal! zo
7943
normal! zo
7943
normal! zo
7943
normal! zo
7943
normal! zo
7943
normal! zo
7946
normal! zo
7952
normal! zo
7955
normal! zo
7964
normal! zo
7966
normal! zo
7967
normal! zo
7974
normal! zo
7975
normal! zo
7976
normal! zo
7981
normal! zo
7985
normal! zo
7993
normal! zo
7994
normal! zo
7996
normal! zo
7996
normal! zo
8003
normal! zo
8004
normal! zo
8005
normal! zo
8005
normal! zo
8005
normal! zo
8005
normal! zo
8005
normal! zo
8005
normal! zo
8005
normal! zo
8005
normal! zo
8008
normal! zo
8008
normal! zo
8008
normal! zo
8015
normal! zo
8017
normal! zo
8300
normal! zo
8311
normal! zo
8312
normal! zo
8312
normal! zo
8312
normal! zo
8312
normal! zo
8312
normal! zo
8312
normal! zo
8312
normal! zo
8315
normal! zo
8315
normal! zo
8315
normal! zo
8315
normal! zo
8315
normal! zo
8315
normal! zo
8315
normal! zo
8319
normal! zo
8326
normal! zo
8326
normal! zo
8326
normal! zo
8326
normal! zo
8326
normal! zo
8326
normal! zo
8326
normal! zo
8326
normal! zo
8329
normal! zo
8329
normal! zo
8329
normal! zo
8329
normal! zo
8329
normal! zo
8329
normal! zo
8329
normal! zo
8329
normal! zo
8764
normal! zo
8768
normal! zo
8799
normal! zo
8848
normal! zo
8855
normal! zo
9023
normal! zo
9034
normal! zo
9047
normal! zo
9048
normal! zo
9061
normal! zo
9066
normal! zo
9071
normal! zo
9076
normal! zo
9087
normal! zo
9110
normal! zo
9133
normal! zo
9134
normal! zo
9134
normal! zo
9134
normal! zo
9134
normal! zo
9134
normal! zo
9134
normal! zo
9145
normal! zo
9160
normal! zo
9195
normal! zo
9283
normal! zo
9313
normal! zo
9320
normal! zo
9323
normal! zo
9338
normal! zo
9386
normal! zo
9427
normal! zo
9689
normal! zo
9715
normal! zo
9754
normal! zo
9765
normal! zo
9766
normal! zo
9779
normal! zo
9791
normal! zo
9805
normal! zo
9821
normal! zo
9838
normal! zo
9838
normal! zo
9838
normal! zo
9838
normal! zo
9838
normal! zo
9838
normal! zo
9838
normal! zo
9838
normal! zo
9838
normal! zo
9845
normal! zo
9859
normal! zo
9860
normal! zo
9860
normal! zo
9862
normal! zo
9863
normal! zo
9863
normal! zo
9865
normal! zo
9866
normal! zo
9866
normal! zo
9868
normal! zo
9869
normal! zo
9869
normal! zo
9871
normal! zo
9874
normal! zo
9876
normal! zo
9876
normal! zo
9876
normal! zo
9885
normal! zo
9898
normal! zo
9901
normal! zo
9902
normal! zo
9902
normal! zo
9905
normal! zo
9905
normal! zo
9905
normal! zo
9908
normal! zo
9908
normal! zo
9908
normal! zo
9908
normal! zo
9914
normal! zo
9917
normal! zo
9921
normal! zo
9928
normal! zo
9930
normal! zo
9977
normal! zo
9991
normal! zo
9992
normal! zo
9994
normal! zo
10029
normal! zo
10036
normal! zo
10041
normal! zo
10042
normal! zo
10047
normal! zo
10047
normal! zo
10047
normal! zo
10047
normal! zo
10047
normal! zo
10050
normal! zo
10050
normal! zo
10050
normal! zo
10076
normal! zo
10085
normal! zo
10090
normal! zo
10092
normal! zo
10097
normal! zo
10103
normal! zo
10111
normal! zo
10112
normal! zo
10112
normal! zo
10112
normal! zo
10112
normal! zo
10121
normal! zo
10122
normal! zo
10127
normal! zo
10176
normal! zo
10181
normal! zo
10294
normal! zo
10321
normal! zo
10326
normal! zo
10332
normal! zo
10418
normal! zo
10425
normal! zo
10426
normal! zo
10474
normal! zo
10474
normal! zo
10474
normal! zo
10474
normal! zo
10474
normal! zo
10477
normal! zo
10485
normal! zo
10486
normal! zo
10531
normal! zo
10551
normal! zo
10552
normal! zo
10553
normal! zo
10553
normal! zo
10553
normal! zo
10553
normal! zo
10553
normal! zo
10553
normal! zo
10553
normal! zo
10553
normal! zo
10553
normal! zo
10570
normal! zo
10576
normal! zo
10586
normal! zo
10601
normal! zo
10604
normal! zo
10607
normal! zo
10607
normal! zo
10607
normal! zo
10610
normal! zo
10610
normal! zo
10610
normal! zo
10610
normal! zo
10615
normal! zo
10615
normal! zo
10615
normal! zo
10623
normal! zo
10630
normal! zo
10637
normal! zo
10640
normal! zo
10642
normal! zo
10645
normal! zo
10648
normal! zo
10653
normal! zo
10664
normal! zo
10671
normal! zo
10675
normal! zo
10676
normal! zo
10676
normal! zo
10678
normal! zo
10679
normal! zo
10679
normal! zo
10681
normal! zo
10682
normal! zo
10682
normal! zo
10684
normal! zo
10685
normal! zo
10685
normal! zo
10687
normal! zo
10688
normal! zo
10688
normal! zo
10690
normal! zo
10691
normal! zo
10691
normal! zo
10693
normal! zo
10694
normal! zo
10694
normal! zo
10696
normal! zo
10699
normal! zo
10701
normal! zo
10701
normal! zo
10701
normal! zo
10707
normal! zo
10708
normal! zo
10708
normal! zo
10710
normal! zo
10711
normal! zo
10711
normal! zo
10735
normal! zo
10739
normal! zo
10742
normal! zo
10743
normal! zo
10743
normal! zo
10743
normal! zo
10743
normal! zo
10743
normal! zo
10743
normal! zo
10748
normal! zo
10749
normal! zo
10749
normal! zo
10749
normal! zo
10752
normal! zo
10864
normal! zo
10940
normal! zo
10948
normal! zo
10955
normal! zo
10955
normal! zo
10955
normal! zo
10955
normal! zo
10955
normal! zo
10955
normal! zo
10955
normal! zo
10966
normal! zo
10970
normal! zo
10971
normal! zo
10971
normal! zo
10971
normal! zo
10981
normal! zo
10984
normal! zo
10991
normal! zo
11000
normal! zo
11009
normal! zo
11119
normal! zo
11133
normal! zo
11133
normal! zo
11133
normal! zo
11133
normal! zo
11145
normal! zo
11158
normal! zo
11171
normal! zo
11178
normal! zo
11180
normal! zo
11180
normal! zo
11180
normal! zo
11180
normal! zo
11180
normal! zo
11180
normal! zo
11205
normal! zo
11233
normal! zo
11245
normal! zo
11246
normal! zo
11246
normal! zo
11246
normal! zo
11246
normal! zo
11417
normal! zo
11425
normal! zo
11425
normal! zo
11425
normal! zo
11425
normal! zo
11439
normal! zo
11450
normal! zo
11467
normal! zo
11467
normal! zo
11471
normal! zo
11476
normal! zo
11476
normal! zo
11478
normal! zo
11479
normal! zo
11479
normal! zo
11484
normal! zo
11484
normal! zo
11484
normal! zo
11484
normal! zo
11484
normal! zo
11497
normal! zo
11500
normal! zo
11500
normal! zo
11500
normal! zo
11500
normal! zo
11506
normal! zo
11506
normal! zo
11506
normal! zo
11506
normal! zo
11506
normal! zo
11534
normal! zo
11632
normal! zo
11632
normal! zo
11632
normal! zo
11632
normal! zo
11632
normal! zo
11632
normal! zo
11632
normal! zo
11632
normal! zo
11632
normal! zo
11632
normal! zo
11653
normal! zo
11653
normal! zo
11653
normal! zo
11653
normal! zo
11653
normal! zo
11653
normal! zo
11694
normal! zo
11695
normal! zo
11717
normal! zo
11873
normal! zo
11873
normal! zo
12022
normal! zo
12022
normal! zo
12022
normal! zo
12036
normal! zo
12073
normal! zo
12084
normal! zo
12089
normal! zo
12107
normal! zo
12107
normal! zo
12107
normal! zo
12107
normal! zo
12108
normal! zo
12113
normal! zo
12129
normal! zo
12129
normal! zo
12129
normal! zo
12129
normal! zo
12138
normal! zo
12138
normal! zo
12138
normal! zo
12138
normal! zo
12138
normal! zo
12162
normal! zo
13325
normal! zo
13459
normal! zo
13459
normal! zo
13459
normal! zo
13469
normal! zo
13474
normal! zo
13475
normal! zo
13476
normal! zo
13476
normal! zo
13476
normal! zo
13476
normal! zo
13476
normal! zo
13476
normal! zo
13476
normal! zo
13476
normal! zo
13476
normal! zo
13476
normal! zo
13482
normal! zo
13483
normal! zo
13484
normal! zo
13484
normal! zo
13484
normal! zo
13484
normal! zo
13484
normal! zo
13484
normal! zo
13484
normal! zo
13486
normal! zo
13486
normal! zo
13486
normal! zo
13486
normal! zo
13486
normal! zo
13486
normal! zo
13486
normal! zo
13486
normal! zo
13488
normal! zo
13489
normal! zo
13489
normal! zo
13489
normal! zo
13489
normal! zo
13489
normal! zo
13489
normal! zo
13489
normal! zo
13489
normal! zo
13489
normal! zo
13492
normal! zo
13494
normal! zo
13494
normal! zo
13499
normal! zo
13499
normal! zo
13509
normal! zo
13510
normal! zo
13510
normal! zo
13510
normal! zo
13510
normal! zo
13510
normal! zo
13510
normal! zo
13629
normal! zo
13629
normal! zo
13629
normal! zo
13650
normal! zo
13655
normal! zo
13656
normal! zo
13657
normal! zo
13657
normal! zo
13657
normal! zo
13657
normal! zo
13657
normal! zo
13657
normal! zo
13657
normal! zo
13657
normal! zo
13657
normal! zo
13657
normal! zo
13663
normal! zo
13664
normal! zo
13665
normal! zo
13665
normal! zo
13665
normal! zo
13665
normal! zo
13665
normal! zo
13665
normal! zo
13665
normal! zo
13667
normal! zo
13667
normal! zo
13667
normal! zo
13667
normal! zo
13667
normal! zo
13667
normal! zo
13667
normal! zo
13667
normal! zo
13669
normal! zo
13670
normal! zo
13670
normal! zo
13670
normal! zo
13670
normal! zo
13670
normal! zo
13670
normal! zo
13670
normal! zo
13670
normal! zo
13670
normal! zo
13673
normal! zo
13675
normal! zo
13680
normal! zo
13689
normal! zo
13690
normal! zo
13690
normal! zo
13690
normal! zo
13690
normal! zo
13690
normal! zo
13690
normal! zo
13690
normal! zo
13760
normal! zo
13760
normal! zo
13760
normal! zo
13771
normal! zo
13776
normal! zo
13777
normal! zo
13778
normal! zo
13778
normal! zo
13778
normal! zo
13778
normal! zo
13778
normal! zo
13778
normal! zo
13778
normal! zo
13778
normal! zo
13778
normal! zo
13778
normal! zo
13784
normal! zo
13785
normal! zo
13786
normal! zo
13786
normal! zo
13786
normal! zo
13786
normal! zo
13786
normal! zo
13786
normal! zo
13786
normal! zo
13788
normal! zo
13788
normal! zo
13788
normal! zo
13788
normal! zo
13788
normal! zo
13788
normal! zo
13788
normal! zo
13788
normal! zo
13790
normal! zo
13791
normal! zo
13791
normal! zo
13791
normal! zo
13791
normal! zo
13791
normal! zo
13791
normal! zo
13791
normal! zo
13791
normal! zo
13791
normal! zo
13794
normal! zo
13796
normal! zo
13801
normal! zo
13810
normal! zo
13811
normal! zo
13811
normal! zo
13811
normal! zo
13811
normal! zo
13811
normal! zo
13811
normal! zo
13811
normal! zo
13918
normal! zo
13918
normal! zo
13918
normal! zo
13918
normal! zo
13918
normal! zo
13918
normal! zo
13918
normal! zo
13918
normal! zo
13918
normal! zo
13928
normal! zo
13928
normal! zo
13928
normal! zo
13928
normal! zo
13928
normal! zo
13928
normal! zo
13930
normal! zo
13931
normal! zo
13931
normal! zo
13931
normal! zo
14126
normal! zo
14126
normal! zo
14126
normal! zo
14126
normal! zo
14142
normal! zo
14147
normal! zo
14148
normal! zo
14149
normal! zo
14149
normal! zo
14149
normal! zo
14149
normal! zo
14149
normal! zo
14149
normal! zo
14149
normal! zo
14149
normal! zo
14149
normal! zo
14149
normal! zo
14155
normal! zo
14156
normal! zo
14157
normal! zo
14157
normal! zo
14157
normal! zo
14157
normal! zo
14157
normal! zo
14157
normal! zo
14157
normal! zo
14159
normal! zo
14159
normal! zo
14159
normal! zo
14159
normal! zo
14159
normal! zo
14159
normal! zo
14159
normal! zo
14159
normal! zo
14159
normal! zo
14161
normal! zo
14162
normal! zo
14162
normal! zo
14162
normal! zo
14162
normal! zo
14162
normal! zo
14162
normal! zo
14162
normal! zo
14162
normal! zo
14162
normal! zo
14165
normal! zo
14167
normal! zo
14167
normal! zo
14172
normal! zo
14172
normal! zo
14182
normal! zo
14183
normal! zo
14183
normal! zo
14183
normal! zo
14183
normal! zo
14183
normal! zo
14183
normal! zo
14243
normal! zo
14243
normal! zo
14243
normal! zo
14243
normal! zo
14255
normal! zo
14260
normal! zo
14261
normal! zo
14262
normal! zo
14262
normal! zo
14262
normal! zo
14262
normal! zo
14262
normal! zo
14262
normal! zo
14262
normal! zo
14262
normal! zo
14262
normal! zo
14262
normal! zo
14268
normal! zo
14269
normal! zo
14270
normal! zo
14270
normal! zo
14270
normal! zo
14270
normal! zo
14270
normal! zo
14270
normal! zo
14270
normal! zo
14272
normal! zo
14272
normal! zo
14272
normal! zo
14272
normal! zo
14272
normal! zo
14272
normal! zo
14272
normal! zo
14272
normal! zo
14272
normal! zo
14274
normal! zo
14275
normal! zo
14275
normal! zo
14275
normal! zo
14275
normal! zo
14275
normal! zo
14275
normal! zo
14275
normal! zo
14275
normal! zo
14275
normal! zo
14278
normal! zo
14280
normal! zo
14280
normal! zo
14285
normal! zo
14285
normal! zo
14295
normal! zo
14296
normal! zo
14296
normal! zo
14296
normal! zo
14296
normal! zo
14296
normal! zo
14296
normal! zo
14364
normal! zo
14376
normal! zo
14379
normal! zo
14380
normal! zo
14381
normal! zo
14381
normal! zo
14381
normal! zo
14383
normal! zo
14384
normal! zo
14384
normal! zo
14384
normal! zo
14400
normal! zo
14411
normal! zo
14420
normal! zo
14430
normal! zo
14457
normal! zo
14462
normal! zo
14468
normal! zo
14479
normal! zo
14492
normal! zo
14516
normal! zo
14518
normal! zo
14521
normal! zo
14524
normal! zo
14525
normal! zo
14529
normal! zo
14530
normal! zo
14544
normal! zo
14544
normal! zo
14544
normal! zo
14544
normal! zo
14566
normal! zo
14567
normal! zo
14568
normal! zo
14568
normal! zo
14568
normal! zo
14568
normal! zo
14568
normal! zo
14568
normal! zo
14568
normal! zo
14568
normal! zo
14568
normal! zo
14568
normal! zo
14577
normal! zo
14578
normal! zo
14584
normal! zo
14588
normal! zo
14589
normal! zo
14598
normal! zo
14599
normal! zo
14607
normal! zo
14608
normal! zo
14614
normal! zo
14629
normal! zo
14637
normal! zo
14643
normal! zo
14649
normal! zo
14654
normal! zo
14658
normal! zo
14664
normal! zo
14669
normal! zo
14670
normal! zo
14675
normal! zo
14686
normal! zo
14704
normal! zo
14746
normal! zo
14752
normal! zo
14758
normal! zo
14765
normal! zo
14774
normal! zo
14776
normal! zo
14783
normal! zo
14783
normal! zo
14783
normal! zo
14783
normal! zo
14783
normal! zo
14783
normal! zo
14800
normal! zo
14812
normal! zo
14823
normal! zo
14824
normal! zo
14840
normal! zo
14857
normal! zo
14861
normal! zo
14862
normal! zo
14863
normal! zo
14863
normal! zo
14865
normal! zo
14868
normal! zo
14881
normal! zo
14891
normal! zo
14893
normal! zo
14897
normal! zo
14898
normal! zo
14898
normal! zo
14898
normal! zo
14898
normal! zo
14898
normal! zo
14898
normal! zo
14911
normal! zo
14932
normal! zo
14933
normal! zo
14940
normal! zo
14973
normal! zo
14974
normal! zo
14974
normal! zo
14990
normal! zo
14996
normal! zo
14999
normal! zo
14999
normal! zo
14999
normal! zo
15005
normal! zo
15005
normal! zo
15025
normal! zo
15030
normal! zo
15035
normal! zo
15043
normal! zo
15062
normal! zo
15096
normal! zo
15104
normal! zo
15113
normal! zo
15132
normal! zo
15134
normal! zo
15138
normal! zo
15155
normal! zo
15161
normal! zo
15165
normal! zo
15497
normal! zo
15528
normal! zo
15552
normal! zo
15562
normal! zo
15562
normal! zo
15562
normal! zo
15562
normal! zo
15562
normal! zo
15750
normal! zo
15769
normal! zo
15791
normal! zo
15796
normal! zo
15797
normal! zo
15797
normal! zo
15800
normal! zo
15801
normal! zo
15801
normal! zo
15801
normal! zo
15804
normal! zo
15804
normal! zo
15804
normal! zo
15808
normal! zo
15808
normal! zo
15808
normal! zo
15808
normal! zo
15808
normal! zo
15808
normal! zo
15808
normal! zo
15808
normal! zo
15808
normal! zo
16339
normal! zo
16375
normal! zo
16390
normal! zo
16396
normal! zo
16399
normal! zo
16407
normal! zo
16408
normal! zo
16408
normal! zo
16408
normal! zo
16408
normal! zo
16408
normal! zo
16412
normal! zo
16420
normal! zo
16423
normal! zo
16429
normal! zo
16435
normal! zo
16438
normal! zo
16444
normal! zo
16458
normal! zo
16464
normal! zo
16469
normal! zo
16472
normal! zo
16472
normal! zo
16472
normal! zo
16482
normal! zo
16497
normal! zo
16508
normal! zo
16508
normal! zo
16519
normal! zo
16534
normal! zo
16544
normal! zo
16555
normal! zo
16564
normal! zo
16571
normal! zo
16609
normal! zo
16614
normal! zo
16614
normal! zo
16614
normal! zo
16627
normal! zo
16627
normal! zo
16627
normal! zo
16627
normal! zo
16627
normal! zo
16627
normal! zo
16627
normal! zo
16627
normal! zo
16627
normal! zo
16627
normal! zo
16627
normal! zo
16639
normal! zo
16660
normal! zo
16679
normal! zo
16687
normal! zo
16688
normal! zo
16689
normal! zo
16693
normal! zo
16697
normal! zo
16713
normal! zo
16728
normal! zo
16733
normal! zo
16738
normal! zo
16748
normal! zo
16749
normal! zo
16749
normal! zo
16749
normal! zo
16751
normal! zo
16751
normal! zo
16751
normal! zo
16751
normal! zo
16751
normal! zo
16751
normal! zo
16751
normal! zo
16751
normal! zo
16751
normal! zo
16751
normal! zo
16756
normal! zo
16757
normal! zo
16763
normal! zo
16764
normal! zo
16784
normal! zo
16809
normal! zo
16813
normal! zo
16830
normal! zo
16841
normal! zo
16841
normal! zo
16841
normal! zo
16841
normal! zo
16843
normal! zo
16844
normal! zo
16845
normal! zo
16846
normal! zo
16847
normal! zo
16851
normal! zo
16852
normal! zo
16853
normal! zo
16853
normal! zo
16853
normal! zo
16853
normal! zo
16853
normal! zo
16853
normal! zo
16853
normal! zo
16855
normal! zo
16857
normal! zo
16862
normal! zo
16862
normal! zo
16862
normal! zo
16862
normal! zo
16868
normal! zo
16872
normal! zo
16880
normal! zo
16880
normal! zo
16880
normal! zo
16880
normal! zo
16888
normal! zo
16896
normal! zo
16897
normal! zo
16900
normal! zo
16905
normal! zo
16913
normal! zo
16918
normal! zo
16926
normal! zo
16931
normal! zo
16940
normal! zo
16941
normal! zo
16941
normal! zo
16951
normal! zo
16966
normal! zo
16967
normal! zo
16983
normal! zo
17003
normal! zo
17004
normal! zo
17004
normal! zo
17004
normal! zo
17004
normal! zo
17004
normal! zo
17010
normal! zo
17020
normal! zo
17034
normal! zo
17037
normal! zo
17041
normal! zo
17042
normal! zo
17043
normal! zo
17043
normal! zo
17043
normal! zo
17043
normal! zo
17043
normal! zo
17061
normal! zo
17068
normal! zo
17069
normal! zo
17076
normal! zo
17083
normal! zo
17084
normal! zo
17085
normal! zo
17090
normal! zo
17097
normal! zo
17102
normal! zo
17115
normal! zo
17116
normal! zo
17116
normal! zo
17116
normal! zo
17121
normal! zo
17134
normal! zo
17141
normal! zo
17142
normal! zo
17157
normal! zo
17164
normal! zo
17178
normal! zo
17185
normal! zo
17186
normal! zo
17191
normal! zo
17200
normal! zo
17214
normal! zo
17236
normal! zo
17257
normal! zo
17270
normal! zo
17270
normal! zo
17270
normal! zo
17270
normal! zo
17270
normal! zo
17270
normal! zo
17280
normal! zo
17293
normal! zo
17317
normal! zo
17322
normal! zo
17324
normal! zo
17327
normal! zo
17334
normal! zo
17346
normal! zo
17356
normal! zo
17356
normal! zo
17356
normal! zo
17356
normal! zo
17356
normal! zo
17356
normal! zo
17364
normal! zo
17374
normal! zo
17374
normal! zo
17374
normal! zo
17374
normal! zo
17374
normal! zo
17374
normal! zo
17382
normal! zo
17383
normal! zo
17394
normal! zo
17399
normal! zo
17410
normal! zo
17418
normal! zo
17431
normal! zo
17435
normal! zo
17435
normal! zo
17435
normal! zo
17435
normal! zo
17435
normal! zo
17437
normal! zo
17449
normal! zo
17449
normal! zo
17449
normal! zo
17449
normal! zo
17449
normal! zo
17449
normal! zo
17449
normal! zo
17453
normal! zo
17453
normal! zo
17453
normal! zo
17453
normal! zo
17453
normal! zo
17453
normal! zo
17459
normal! zo
17459
normal! zo
17459
normal! zo
17459
normal! zo
17462
normal! zo
17463
normal! zo
17464
normal! zo
17470
normal! zo
17471
normal! zo
17471
normal! zo
17471
normal! zo
17593
normal! zo
17681
normal! zo
17738
normal! zo
17753
normal! zo
17760
normal! zo
17761
normal! zo
17777
normal! zo
17787
normal! zo
17801
normal! zo
17804
normal! zo
17805
normal! zo
17805
normal! zo
17827
normal! zo
17847
normal! zo
17859
normal! zo
17859
normal! zo
17859
normal! zo
17859
normal! zo
17859
normal! zo
17862
normal! zo
17869
normal! zo
17872
normal! zo
17883
normal! zo
17889
normal! zo
17894
normal! zo
17900
normal! zo
17901
normal! zo
17902
normal! zo
17905
normal! zo
17924
normal! zo
17939
normal! zo
17967
normal! zo
17992
normal! zo
18013
normal! zo
18048
normal! zo
18057
normal! zo
18058
normal! zo
18059
normal! zo
18061
normal! zo
18061
normal! zo
18061
normal! zo
18064
normal! zo
18066
normal! zo
18066
normal! zo
18066
normal! zo
18069
normal! zo
18070
normal! zo
18070
normal! zo
18070
normal! zo
18070
normal! zo
18070
normal! zo
18596
normal! zo
18613
normal! zo
18623
normal! zo
18626
normal! zo
18627
normal! zo
18627
normal! zo
18633
normal! zo
18640
normal! zo
18641
normal! zo
18642
normal! zo
18642
normal! zo
18642
normal! zo
18642
normal! zo
18646
normal! zo
18647
normal! zo
18647
normal! zo
18647
normal! zo
18647
normal! zo
18663
normal! zo
18964
normal! zo
19881
normal! zo
19905
normal! zo
19911
normal! zo
19917
normal! zo
19935
normal! zo
19945
normal! zo
19948
normal! zo
19955
normal! zo
19955
normal! zo
19955
normal! zo
19955
normal! zo
19960
normal! zo
20240
normal! zo
20246
normal! zo
20246
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
20297
normal! zo
20303
normal! zo
20304
normal! zo
20313
normal! zo
20322
normal! zo
20485
normal! zo
20495
normal! zo
20506
normal! zo
20517
normal! zo
20518
normal! zo
20523
normal! zo
20524
normal! zo
20524
normal! zo
20534
normal! zo
20534
normal! zo
20534
normal! zo
20534
normal! zo
20534
normal! zo
20534
normal! zo
20534
normal! zo
20534
normal! zo
20534
normal! zo
20545
normal! zo
20546
normal! zo
20554
normal! zo
20554
normal! zo
20554
normal! zo
20554
normal! zo
20554
normal! zo
20554
normal! zo
20554
normal! zo
20554
normal! zo
20565
normal! zo
20566
normal! zo
20622
normal! zo
20643
normal! zo
20648
normal! zo
20660
normal! zo
20660
normal! zo
20660
normal! zo
20660
normal! zo
20660
normal! zo
20660
normal! zo
20660
normal! zo
20678
normal! zo
20685
normal! zo
let s:l = 7164 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
7164
normal! 016|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/consumo_balas_partida.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
51
normal! zo
52
normal! zo
61
normal! zo
61
normal! zo
347
normal! zo
let s:l = 622 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
622
normal! 09|
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/extra/scripts/clouseau.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
16
normal! zo
16
normal! zo
16
normal! zo
16
normal! zo
16
normal! zo
16
normal! zo
16
normal! zo
16
normal! zo
16
normal! zo
16
normal! zo
16
normal! zo
16
normal! zo
16
normal! zo
26
normal! zo
56
normal! zo
66
normal! zo
76
normal! zo
84
normal! zo
87
normal! zo
96
normal! zo
105
normal! zo
108
normal! zo
118
normal! zo
127
normal! zo
137
normal! zo
145
normal! zo
145
normal! zo
145
normal! zo
145
normal! zo
145
normal! zo
173
normal! zo
178
normal! zo
178
normal! zo
183
normal! zo
187
normal! zo
192
normal! zo
193
normal! zo
202
normal! zo
217
normal! zo
217
normal! zo
226
normal! zo
226
normal! zo
230
normal! zo
230
normal! zo
230
normal! zo
230
normal! zo
230
normal! zo
230
normal! zo
230
normal! zo
230
normal! zo
232
normal! zo
232
normal! zo
232
normal! zo
232
normal! zo
232
normal! zo
232
normal! zo
232
normal! zo
232
normal! zo
238
normal! zo
238
normal! zo
238
normal! zo
238
normal! zo
238
normal! zo
238
normal! zo
238
normal! zo
238
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
242
normal! zo
242
normal! zo
242
normal! zo
242
normal! zo
242
normal! zo
242
normal! zo
249
normal! zo
250
normal! zo
let s:l = 201 - ((21 * winheight(0) + 16) / 33)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
201
normal! 065|
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/consulta_consumo.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
49
normal! zo
54
normal! zo
165
normal! zo
196
normal! zo
199
normal! zo
213
normal! zo
213
normal! zo
239
normal! zo
239
normal! zo
let s:l = 86 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
86
normal! 033|
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/consulta_ventas_por_producto.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
47
normal! zo
133
normal! zo
155
normal! zo
176
normal! zo
177
normal! zo
189
normal! zo
189
normal! zo
189
normal! zo
189
normal! zo
189
normal! zo
189
normal! zo
196
normal! zo
202
normal! zo
203
normal! zo
203
normal! zo
203
normal! zo
203
normal! zo
215
normal! zo
222
normal! zo
234
normal! zo
238
normal! zo
247
normal! zo
249
normal! zo
251
normal! zo
251
normal! zo
267
normal! zo
284
normal! zo
300
normal! zo
335
normal! zo
345
normal! zo
346
normal! zo
362
normal! zo
let s:l = 157 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
157
normal! 043|
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
63
normal! zo
80
normal! zo
100
normal! zo
127
normal! zo
135
normal! zo
141
normal! zo
146
normal! zo
154
normal! zo
154
normal! zo
154
normal! zo
154
normal! zo
158
normal! zo
170
normal! zo
171
normal! zo
172
normal! zo
177
normal! zo
let s:l = 1 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/partes_de_fabricacion_bolsas.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
89
normal! zo
791
normal! zo
848
normal! zo
let s:l = 1682 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1682
normal! 034|
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/consulta_consumo.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
49
normal! zo
54
normal! zo
165
normal! zo
196
normal! zo
199
normal! zo
203
normal! zo
213
normal! zo
213
normal! zo
216
normal! zo
218
normal! zo
219
normal! zo
219
normal! zo
219
normal! zo
227
normal! zo
230
normal! zo
231
normal! zo
239
normal! zo
239
normal! zo
255
normal! zo
263
normal! zo
267
normal! zo
270
normal! zo
288
normal! zo
293
normal! zo
293
normal! zo
293
normal! zo
293
normal! zo
308
normal! zo
309
normal! zo
309
normal! zo
309
normal! zo
309
normal! zo
311
normal! zo
311
normal! zo
311
normal! zo
311
normal! zo
313
normal! zo
313
normal! zo
313
normal! zo
313
normal! zo
let s:l = 156 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
156
normal! 028|
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
let s:l = 349 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
349
normal! 018|
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
let s:l = 126 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
126
normal! 042|
wincmd w
5wincmd w
exe 'vert 1resize ' . ((&columns * 19 + 50) / 100)
exe '2resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 2resize ' . ((&columns * 80 + 50) / 100)
exe '3resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 3resize ' . ((&columns * 80 + 50) / 100)
exe '4resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 4resize ' . ((&columns * 80 + 50) / 100)
exe '5resize ' . ((&lines * 33 + 28) / 57)
exe 'vert 5resize ' . ((&columns * 80 + 50) / 100)
exe '6resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 6resize ' . ((&columns * 80 + 50) / 100)
exe '7resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 7resize ' . ((&columns * 80 + 50) / 100)
exe '8resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 8resize ' . ((&columns * 80 + 50) / 100)
exe '9resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 9resize ' . ((&columns * 80 + 50) / 100)
exe '10resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 10resize ' . ((&columns * 80 + 50) / 100)
exe '11resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 11resize ' . ((&columns * 80 + 50) / 100)
exe '12resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 12resize ' . ((&columns * 80 + 50) / 100)
exe '13resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 13resize ' . ((&columns * 80 + 50) / 100)
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
5wincmd w

" vim: ft=vim ro nowrap smc=128
