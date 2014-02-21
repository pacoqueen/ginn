" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 21 febrero 2014 at 15:00:08.
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
badd +139 ginn/formularios/consulta_producido.py
badd +1 ginn/__init__.py
badd +1505 ginn/formularios/clientes.py
badd +991 ginn/formularios/productos_compra.py
badd +39 ginn/formularios/productos_de_venta_balas.py
badd +525 ginn/formularios/recibos.py
badd +603 ginn/formularios/productos_de_venta_rollos.py
badd +382 ginn/formularios/productos_de_venta_rollos_geocompuestos.py
badd +417 ginn/formularios/productos_de_venta_especial.py
badd +1798 ginn/formularios/partes_de_fabricacion_balas.py
badd +951 ginn/formularios/partes_de_fabricacion_bolsas.py
badd +35 ginn/formularios/partes_de_fabricacion_rollos.py
badd +312 ginn/formularios/proveedores.py
badd +547 ~/workspace/CICAN/src/formularios/menu.py
badd +93 ginn/formularios/launcher.py
badd +625 ginn/formularios/empleados.py
badd +38 ginn/formularios/resultados_geotextiles.py
badd +760 ginn/formularios/menu.py
badd +142 ginn/formularios/autenticacion.py
badd +8819 ginn/informes/geninformes.py
badd +233 ginn/informes/informe_certificado_calidad.py
badd +1518 informes/geninformes.py
badd +2349 ginn/formularios/facturas_venta.py
badd +13 ginn/framework/configuracion.py
badd +4 bin/ginn.sh
badd +10 ginn/main.py
badd +1149 ginn/formularios/ventana.py
badd +2094 ginn/formularios/pedidos_de_venta.py
badd +3879 db/tablas.sql
badd +4772 ginn/formularios/albaranes_de_salida.py
badd +93 ginn/formularios/presupuesto.py
badd +1884 ginn/formularios/presupuestos.py
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
badd +630 ginn/formularios/consumo_balas_partida.py
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
badd +594 ginn/formularios/listado_rollos.py
badd +74 ginn/formularios/consulta_existenciasRollos.py
badd +64 ginn/formularios/listado_rollos_defectuosos.py
badd +500 ginn/formularios/consulta_global.py
badd +145 ginn/formularios/rollos_c.py
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
badd +136 ginn/formularios/consulta_consumo.py
badd +117 ginn/formularios/consulta_existencias_por_tipo.py
badd +82 ginn/formularios/consulta_existencias.py
badd +1 ginn/formularios/consulta_producido.glade
badd +1 ginn/formularios/consumo_balas_partida.pyç
badd +28 db/restore_snapshot.sh
badd +1 extra/scripts/clouseau.py
badd +92 ginn/informes/treeview2csv.py
badd +287 ginn/formularios/consulta_ventas_por_producto.py
args formularios/auditviewer.py
set lines=45 columns=100
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
7wincmd k
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
exe '2resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 2resize ' . ((&columns * 80 + 50) / 100)
exe '3resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 3resize ' . ((&columns * 80 + 50) / 100)
exe '4resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 4resize ' . ((&columns * 80 + 50) / 100)
exe '5resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 5resize ' . ((&columns * 80 + 50) / 100)
exe '6resize ' . ((&lines * 29 + 22) / 45)
exe 'vert 6resize ' . ((&columns * 80 + 50) / 100)
exe '7resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 7resize ' . ((&columns * 80 + 50) / 100)
exe '8resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 8resize ' . ((&columns * 80 + 50) / 100)
exe '9resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 9resize ' . ((&columns * 80 + 50) / 100)
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
1175
normal! zo
2035
normal! zo
2072
normal! zo
2077
normal! zo
2198
normal! zo
2839
normal! zo
3054
normal! zo
3062
normal! zo
3252
normal! zo
3264
normal! zo
3265
normal! zo
3266
normal! zo
3279
normal! zo
4300
normal! zo
let s:l = 4794 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
4794
normal! 05|
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
11635
normal! zo
11635
normal! zo
11635
normal! zo
11635
normal! zo
11635
normal! zo
11635
normal! zo
11635
normal! zo
11635
normal! zo
11635
normal! zo
11635
normal! zo
11656
normal! zo
11656
normal! zo
11656
normal! zo
11656
normal! zo
11656
normal! zo
11656
normal! zo
11697
normal! zo
11698
normal! zo
11720
normal! zo
11876
normal! zo
11876
normal! zo
12025
normal! zo
12025
normal! zo
12025
normal! zo
12039
normal! zo
12076
normal! zo
12087
normal! zo
12092
normal! zo
12110
normal! zo
12110
normal! zo
12110
normal! zo
12110
normal! zo
12111
normal! zo
12116
normal! zo
12132
normal! zo
12132
normal! zo
12132
normal! zo
12132
normal! zo
12141
normal! zo
12141
normal! zo
12141
normal! zo
12141
normal! zo
12141
normal! zo
12165
normal! zo
13328
normal! zo
13462
normal! zo
13462
normal! zo
13462
normal! zo
13472
normal! zo
13477
normal! zo
13478
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
13479
normal! zo
13479
normal! zo
13485
normal! zo
13486
normal! zo
13487
normal! zo
13487
normal! zo
13487
normal! zo
13487
normal! zo
13487
normal! zo
13487
normal! zo
13487
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
13491
normal! zo
13492
normal! zo
13492
normal! zo
13492
normal! zo
13492
normal! zo
13492
normal! zo
13492
normal! zo
13492
normal! zo
13492
normal! zo
13492
normal! zo
13495
normal! zo
13497
normal! zo
13497
normal! zo
13502
normal! zo
13502
normal! zo
13512
normal! zo
13513
normal! zo
13513
normal! zo
13513
normal! zo
13513
normal! zo
13513
normal! zo
13513
normal! zo
13632
normal! zo
13632
normal! zo
13632
normal! zo
13653
normal! zo
13658
normal! zo
13659
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
13660
normal! zo
13660
normal! zo
13666
normal! zo
13667
normal! zo
13668
normal! zo
13668
normal! zo
13668
normal! zo
13668
normal! zo
13668
normal! zo
13668
normal! zo
13668
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
13672
normal! zo
13673
normal! zo
13673
normal! zo
13673
normal! zo
13673
normal! zo
13673
normal! zo
13673
normal! zo
13673
normal! zo
13673
normal! zo
13673
normal! zo
13676
normal! zo
13678
normal! zo
13683
normal! zo
13692
normal! zo
13693
normal! zo
13693
normal! zo
13693
normal! zo
13693
normal! zo
13693
normal! zo
13693
normal! zo
13693
normal! zo
13763
normal! zo
13763
normal! zo
13763
normal! zo
13774
normal! zo
13779
normal! zo
13780
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
13781
normal! zo
13781
normal! zo
13787
normal! zo
13788
normal! zo
13789
normal! zo
13789
normal! zo
13789
normal! zo
13789
normal! zo
13789
normal! zo
13789
normal! zo
13789
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
13793
normal! zo
13794
normal! zo
13794
normal! zo
13794
normal! zo
13794
normal! zo
13794
normal! zo
13794
normal! zo
13794
normal! zo
13794
normal! zo
13794
normal! zo
13797
normal! zo
13799
normal! zo
13804
normal! zo
13813
normal! zo
13814
normal! zo
13814
normal! zo
13814
normal! zo
13814
normal! zo
13814
normal! zo
13814
normal! zo
13814
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
13921
normal! zo
13921
normal! zo
13921
normal! zo
13931
normal! zo
13931
normal! zo
13931
normal! zo
13931
normal! zo
13931
normal! zo
13931
normal! zo
13933
normal! zo
13934
normal! zo
13934
normal! zo
13934
normal! zo
14129
normal! zo
14129
normal! zo
14129
normal! zo
14129
normal! zo
14145
normal! zo
14150
normal! zo
14151
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
14152
normal! zo
14158
normal! zo
14159
normal! zo
14160
normal! zo
14160
normal! zo
14160
normal! zo
14160
normal! zo
14160
normal! zo
14160
normal! zo
14160
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
14164
normal! zo
14165
normal! zo
14165
normal! zo
14165
normal! zo
14165
normal! zo
14165
normal! zo
14165
normal! zo
14165
normal! zo
14165
normal! zo
14165
normal! zo
14168
normal! zo
14170
normal! zo
14170
normal! zo
14175
normal! zo
14175
normal! zo
14185
normal! zo
14186
normal! zo
14186
normal! zo
14186
normal! zo
14186
normal! zo
14186
normal! zo
14186
normal! zo
14246
normal! zo
14246
normal! zo
14246
normal! zo
14246
normal! zo
14258
normal! zo
14263
normal! zo
14264
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
14265
normal! zo
14271
normal! zo
14272
normal! zo
14273
normal! zo
14273
normal! zo
14273
normal! zo
14273
normal! zo
14273
normal! zo
14273
normal! zo
14273
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
14277
normal! zo
14278
normal! zo
14278
normal! zo
14278
normal! zo
14278
normal! zo
14278
normal! zo
14278
normal! zo
14278
normal! zo
14278
normal! zo
14278
normal! zo
14281
normal! zo
14283
normal! zo
14283
normal! zo
14288
normal! zo
14288
normal! zo
14298
normal! zo
14299
normal! zo
14299
normal! zo
14299
normal! zo
14299
normal! zo
14299
normal! zo
14299
normal! zo
14367
normal! zo
14379
normal! zo
14382
normal! zo
14383
normal! zo
14384
normal! zo
14384
normal! zo
14384
normal! zo
14386
normal! zo
14387
normal! zo
14387
normal! zo
14387
normal! zo
14403
normal! zo
14414
normal! zo
14423
normal! zo
14433
normal! zo
14460
normal! zo
14465
normal! zo
14471
normal! zo
14482
normal! zo
14495
normal! zo
14519
normal! zo
14521
normal! zo
14524
normal! zo
14527
normal! zo
14528
normal! zo
14532
normal! zo
14533
normal! zo
14547
normal! zo
14547
normal! zo
14547
normal! zo
14547
normal! zo
14569
normal! zo
14570
normal! zo
14571
normal! zo
14571
normal! zo
14571
normal! zo
14571
normal! zo
14571
normal! zo
14571
normal! zo
14571
normal! zo
14571
normal! zo
14571
normal! zo
14571
normal! zo
14580
normal! zo
14581
normal! zo
14587
normal! zo
14591
normal! zo
14592
normal! zo
14601
normal! zo
14602
normal! zo
14610
normal! zo
14611
normal! zo
14617
normal! zo
14632
normal! zo
14640
normal! zo
14646
normal! zo
14652
normal! zo
14657
normal! zo
14661
normal! zo
14667
normal! zo
14672
normal! zo
14673
normal! zo
14678
normal! zo
14689
normal! zo
14707
normal! zo
14749
normal! zo
14755
normal! zo
14761
normal! zo
14768
normal! zo
14777
normal! zo
14779
normal! zo
14786
normal! zo
14786
normal! zo
14786
normal! zo
14786
normal! zo
14786
normal! zo
14786
normal! zo
14803
normal! zo
14815
normal! zo
14826
normal! zo
14827
normal! zo
14843
normal! zo
14860
normal! zo
14864
normal! zo
14865
normal! zo
14866
normal! zo
14866
normal! zo
14868
normal! zo
14871
normal! zo
14884
normal! zo
14894
normal! zo
14896
normal! zo
14900
normal! zo
14901
normal! zo
14901
normal! zo
14901
normal! zo
14901
normal! zo
14901
normal! zo
14901
normal! zo
14914
normal! zo
14935
normal! zo
14936
normal! zo
14943
normal! zo
14976
normal! zo
14977
normal! zo
14977
normal! zo
14993
normal! zo
14999
normal! zo
15002
normal! zo
15002
normal! zo
15002
normal! zo
15008
normal! zo
15008
normal! zo
15028
normal! zo
15033
normal! zo
15038
normal! zo
15046
normal! zo
15065
normal! zo
15099
normal! zo
15107
normal! zo
15116
normal! zo
15135
normal! zo
15137
normal! zo
15141
normal! zo
15158
normal! zo
15164
normal! zo
15168
normal! zo
15500
normal! zo
15531
normal! zo
15555
normal! zo
15565
normal! zo
15565
normal! zo
15565
normal! zo
15565
normal! zo
15565
normal! zo
15753
normal! zo
15772
normal! zo
15794
normal! zo
15799
normal! zo
15800
normal! zo
15800
normal! zo
15803
normal! zo
15804
normal! zo
15804
normal! zo
15804
normal! zo
15807
normal! zo
15807
normal! zo
15807
normal! zo
15811
normal! zo
15811
normal! zo
15811
normal! zo
15811
normal! zo
15811
normal! zo
15811
normal! zo
15811
normal! zo
15811
normal! zo
15811
normal! zo
16342
normal! zo
16378
normal! zo
16393
normal! zo
16399
normal! zo
16402
normal! zo
16410
normal! zo
16411
normal! zo
16411
normal! zo
16411
normal! zo
16411
normal! zo
16411
normal! zo
16415
normal! zo
16423
normal! zo
16426
normal! zo
16432
normal! zo
16438
normal! zo
16441
normal! zo
16447
normal! zo
16461
normal! zo
16467
normal! zo
16472
normal! zo
16475
normal! zo
16475
normal! zo
16475
normal! zo
16485
normal! zo
16500
normal! zo
16511
normal! zo
16511
normal! zo
16522
normal! zo
16537
normal! zo
16547
normal! zo
16558
normal! zo
16567
normal! zo
16574
normal! zo
16612
normal! zo
16617
normal! zo
16617
normal! zo
16617
normal! zo
16630
normal! zo
16630
normal! zo
16630
normal! zo
16630
normal! zo
16630
normal! zo
16630
normal! zo
16630
normal! zo
16630
normal! zo
16630
normal! zo
16630
normal! zo
16630
normal! zo
16642
normal! zo
16663
normal! zo
16682
normal! zo
16690
normal! zo
16691
normal! zo
16692
normal! zo
16696
normal! zo
16700
normal! zo
16716
normal! zo
16731
normal! zo
16736
normal! zo
16741
normal! zo
16751
normal! zo
16752
normal! zo
16752
normal! zo
16752
normal! zo
16754
normal! zo
16754
normal! zo
16754
normal! zo
16754
normal! zo
16754
normal! zo
16754
normal! zo
16754
normal! zo
16754
normal! zo
16754
normal! zo
16754
normal! zo
16759
normal! zo
16760
normal! zo
16766
normal! zo
16767
normal! zo
16787
normal! zo
16812
normal! zo
16816
normal! zo
16833
normal! zo
16844
normal! zo
16844
normal! zo
16844
normal! zo
16844
normal! zo
16846
normal! zo
16847
normal! zo
16848
normal! zo
16849
normal! zo
16850
normal! zo
16854
normal! zo
16855
normal! zo
16856
normal! zo
16856
normal! zo
16856
normal! zo
16856
normal! zo
16856
normal! zo
16856
normal! zo
16856
normal! zo
16858
normal! zo
16860
normal! zo
16865
normal! zo
16865
normal! zo
16865
normal! zo
16865
normal! zo
16871
normal! zo
16875
normal! zo
16883
normal! zo
16883
normal! zo
16883
normal! zo
16883
normal! zo
16891
normal! zo
16899
normal! zo
16900
normal! zo
16903
normal! zo
16908
normal! zo
16916
normal! zo
16921
normal! zo
16929
normal! zo
16934
normal! zo
16943
normal! zo
16944
normal! zo
16944
normal! zo
16954
normal! zo
16969
normal! zo
16970
normal! zo
16986
normal! zo
17006
normal! zo
17007
normal! zo
17007
normal! zo
17007
normal! zo
17007
normal! zo
17007
normal! zo
17013
normal! zo
17023
normal! zo
17037
normal! zo
17040
normal! zo
17044
normal! zo
17045
normal! zo
17046
normal! zo
17046
normal! zo
17046
normal! zo
17046
normal! zo
17046
normal! zo
17064
normal! zo
17071
normal! zo
17072
normal! zo
17079
normal! zo
17086
normal! zo
17087
normal! zo
17088
normal! zo
17093
normal! zo
17100
normal! zo
17105
normal! zo
17118
normal! zo
17119
normal! zo
17119
normal! zo
17119
normal! zo
17124
normal! zo
17137
normal! zo
17144
normal! zo
17145
normal! zo
17160
normal! zo
17167
normal! zo
17181
normal! zo
17188
normal! zo
17189
normal! zo
17194
normal! zo
17203
normal! zo
17217
normal! zo
17239
normal! zo
17260
normal! zo
17273
normal! zo
17273
normal! zo
17273
normal! zo
17273
normal! zo
17273
normal! zo
17273
normal! zo
17283
normal! zo
17296
normal! zo
17320
normal! zo
17325
normal! zo
17327
normal! zo
17330
normal! zo
17337
normal! zo
17349
normal! zo
17359
normal! zo
17359
normal! zo
17359
normal! zo
17359
normal! zo
17359
normal! zo
17359
normal! zo
17367
normal! zo
17377
normal! zo
17377
normal! zo
17377
normal! zo
17377
normal! zo
17377
normal! zo
17377
normal! zo
17385
normal! zo
17386
normal! zo
17397
normal! zo
17402
normal! zo
17413
normal! zo
17421
normal! zo
17434
normal! zo
17438
normal! zo
17438
normal! zo
17438
normal! zo
17438
normal! zo
17438
normal! zo
17440
normal! zo
17452
normal! zo
17452
normal! zo
17452
normal! zo
17452
normal! zo
17452
normal! zo
17452
normal! zo
17452
normal! zo
17456
normal! zo
17456
normal! zo
17456
normal! zo
17456
normal! zo
17456
normal! zo
17456
normal! zo
17462
normal! zo
17462
normal! zo
17462
normal! zo
17462
normal! zo
17465
normal! zo
17466
normal! zo
17467
normal! zo
17473
normal! zo
17474
normal! zo
17474
normal! zo
17474
normal! zo
17596
normal! zo
17684
normal! zo
17741
normal! zo
17756
normal! zo
17763
normal! zo
17764
normal! zo
17780
normal! zo
17790
normal! zo
17804
normal! zo
17807
normal! zo
17808
normal! zo
17808
normal! zo
17830
normal! zo
17850
normal! zo
17862
normal! zo
17862
normal! zo
17862
normal! zo
17862
normal! zo
17862
normal! zo
17865
normal! zo
17872
normal! zo
17875
normal! zo
17886
normal! zo
17892
normal! zo
17897
normal! zo
17903
normal! zo
17904
normal! zo
17905
normal! zo
17908
normal! zo
17927
normal! zo
17942
normal! zo
17970
normal! zo
17995
normal! zo
18016
normal! zo
18051
normal! zo
18060
normal! zo
18061
normal! zo
18062
normal! zo
18064
normal! zo
18064
normal! zo
18064
normal! zo
18067
normal! zo
18069
normal! zo
18069
normal! zo
18069
normal! zo
18072
normal! zo
18073
normal! zo
18073
normal! zo
18073
normal! zo
18073
normal! zo
18073
normal! zo
18599
normal! zo
18616
normal! zo
18626
normal! zo
18629
normal! zo
18630
normal! zo
18630
normal! zo
18636
normal! zo
18643
normal! zo
18644
normal! zo
18645
normal! zo
18645
normal! zo
18645
normal! zo
18645
normal! zo
18649
normal! zo
18650
normal! zo
18650
normal! zo
18650
normal! zo
18650
normal! zo
18666
normal! zo
18967
normal! zo
19884
normal! zo
19908
normal! zo
19914
normal! zo
19920
normal! zo
19938
normal! zo
19948
normal! zo
19951
normal! zo
19958
normal! zo
19958
normal! zo
19958
normal! zo
19958
normal! zo
19963
normal! zo
20243
normal! zo
20249
normal! zo
20249
normal! zo
20258
normal! zo
20265
normal! zo
20272
normal! zo
20279
normal! zo
20286
normal! zo
20293
normal! zo
20300
normal! zo
20306
normal! zo
20307
normal! zo
20316
normal! zo
20325
normal! zo
20488
normal! zo
20498
normal! zo
20509
normal! zo
20520
normal! zo
20521
normal! zo
20526
normal! zo
20527
normal! zo
20527
normal! zo
20537
normal! zo
20537
normal! zo
20537
normal! zo
20537
normal! zo
20537
normal! zo
20537
normal! zo
20537
normal! zo
20537
normal! zo
20537
normal! zo
20548
normal! zo
20549
normal! zo
20557
normal! zo
20557
normal! zo
20557
normal! zo
20557
normal! zo
20557
normal! zo
20557
normal! zo
20557
normal! zo
20557
normal! zo
20568
normal! zo
20569
normal! zo
20577
normal! zo
20592
normal! zo
20625
normal! zo
20646
normal! zo
20651
normal! zo
20663
normal! zo
20663
normal! zo
20663
normal! zo
20663
normal! zo
20663
normal! zo
20663
normal! zo
20663
normal! zo
20681
normal! zo
20688
normal! zo
let s:l = 20061 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
20061
normal! 017|
lcd ~/Geotexan/src/Geotex-INN
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
44
normal! zo
74
normal! zo
84
normal! zo
94
normal! zo
102
normal! zo
114
normal! zo
123
normal! zo
136
normal! zo
145
normal! zo
155
normal! zo
163
normal! zo
163
normal! zo
163
normal! zo
163
normal! zo
163
normal! zo
191
normal! zo
196
normal! zo
196
normal! zo
201
normal! zo
205
normal! zo
214
normal! zo
215
normal! zo
224
normal! zo
239
normal! zo
239
normal! zo
248
normal! zo
252
normal! zo
252
normal! zo
252
normal! zo
252
normal! zo
252
normal! zo
252
normal! zo
252
normal! zo
252
normal! zo
252
normal! zo
254
normal! zo
254
normal! zo
254
normal! zo
254
normal! zo
254
normal! zo
254
normal! zo
254
normal! zo
254
normal! zo
254
normal! zo
256
normal! zo
260
normal! zo
260
normal! zo
260
normal! zo
260
normal! zo
260
normal! zo
260
normal! zo
260
normal! zo
260
normal! zo
262
normal! zo
262
normal! zo
262
normal! zo
262
normal! zo
262
normal! zo
262
normal! zo
262
normal! zo
262
normal! zo
264
normal! zo
264
normal! zo
264
normal! zo
264
normal! zo
264
normal! zo
264
normal! zo
271
normal! zo
272
normal! zo
let s:l = 212 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
212
normal! 09|
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/db/tablas.sql
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
122
normal! zo
367
normal! zo
let s:l = 168 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
168
normal! 040|
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/partes_de_fabricacion_rollos.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
185
normal! zo
227
normal! zo
227
normal! zo
227
normal! zo
229
normal! zo
229
normal! zo
229
normal! zo
233
normal! zo
234
normal! zo
266
normal! zo
266
normal! zo
1555
normal! zo
1950
normal! zo
2033
normal! zo
2045
normal! zo
2045
normal! zo
2045
normal! zo
2045
normal! zo
2045
normal! zo
2045
normal! zo
2889
normal! zo
2907
normal! zo
2970
normal! zo
2975
normal! zo
2979
normal! zo
2980
normal! zo
3189
normal! zo
3194
normal! zo
3194
normal! zo
3194
normal! zo
3194
normal! zo
3194
normal! zo
3414
normal! zo
3490
normal! zo
3498
normal! zo
3542
normal! zo
3559
normal! zo
3575
normal! zo
3614
normal! zo
3622
normal! zo
3623
normal! zo
3692
normal! zo
3693
normal! zo
3701
normal! zo
3708
normal! zo
3721
normal! zo
3724
normal! zo
3729
normal! zo
3738
normal! zo
3741
normal! zo
3741
normal! zo
3741
normal! zo
3755
normal! zo
3777
normal! zo
3788
normal! zo
3803
normal! zo
3804
normal! zo
3804
normal! zo
3804
normal! zo
3804
normal! zo
3812
normal! zo
let s:l = 228 - ((16 * winheight(0) + 14) / 29)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
228
normal! 044|
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
let s:l = 344 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
344
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
let s:l = 126 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
126
normal! 042|
wincmd w
6wincmd w
exe 'vert 1resize ' . ((&columns * 19 + 50) / 100)
exe '2resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 2resize ' . ((&columns * 80 + 50) / 100)
exe '3resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 3resize ' . ((&columns * 80 + 50) / 100)
exe '4resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 4resize ' . ((&columns * 80 + 50) / 100)
exe '5resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 5resize ' . ((&columns * 80 + 50) / 100)
exe '6resize ' . ((&lines * 29 + 22) / 45)
exe 'vert 6resize ' . ((&columns * 80 + 50) / 100)
exe '7resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 7resize ' . ((&columns * 80 + 50) / 100)
exe '8resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 8resize ' . ((&columns * 80 + 50) / 100)
exe '9resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 9resize ' . ((&columns * 80 + 50) / 100)
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
6wincmd w

" vim: ft=vim ro nowrap smc=128
