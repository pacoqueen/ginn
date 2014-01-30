" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 30 enero 2014 at 17:59:11.
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
badd +624 ginn/formularios/consulta_producido.py
badd +1 ginn/__init__.py
badd +1183 ginn/formularios/clientes.py
badd +991 ginn/formularios/productos_compra.py
badd +39 ginn/formularios/productos_de_venta_balas.py
badd +525 ginn/formularios/recibos.py
badd +603 ginn/formularios/productos_de_venta_rollos.py
badd +382 ginn/formularios/productos_de_venta_rollos_geocompuestos.py
badd +417 ginn/formularios/productos_de_venta_especial.py
badd +3989 ginn/formularios/partes_de_fabricacion_balas.py
badd +580 ginn/formularios/partes_de_fabricacion_bolsas.py
badd +2250 ginn/formularios/partes_de_fabricacion_rollos.py
badd +446 ginn/formularios/proveedores.py
badd +547 ~/workspace/CICAN/src/formularios/menu.py
badd +93 ginn/formularios/launcher.py
badd +625 ginn/formularios/empleados.py
badd +38 ginn/formularios/resultados_geotextiles.py
badd +760 ginn/formularios/menu.py
badd +142 ginn/formularios/autenticacion.py
badd +1202 ginn/informes/geninformes.py
badd +233 ginn/informes/informe_certificado_calidad.py
badd +1518 informes/geninformes.py
badd +1260 ginn/formularios/facturas_venta.py
badd +419 ginn/framework/configuracion.py
badd +4 bin/ginn.sh
badd +10 ginn/main.py
badd +750 ginn/formularios/ventana.py
badd +992 ginn/formularios/pedidos_de_venta.py
badd +1559 db/tablas.sql
badd +799 ginn/formularios/albaranes_de_salida.py
badd +93 ginn/formularios/presupuesto.py
badd +1 ginn/formularios/presupuestos.py
badd +97 ginn/informes/carta_compromiso.py
badd +367 ginn/formularios/tarifas_de_precios.py
badd +88 ginn/formularios/logviewer.py
badd +238 ginn/formularios/facturas_compra.py
badd +138 ginn/formularios/utils.py
badd +648 ginn/formularios/resultados_fibra.py
badd +955 ginn/formularios/albaranes_de_entrada.py
badd +751 ginn/formularios/consulta_ventas.py
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
badd +704 ginn/framework/pclases/__init__.py
badd +494 ginn/framework/pclases/superfacturaventa.py
badd +134 ginn/framework/pclases/facturaventa.py
badd +694 ginn/formularios/consulta_mensual_nominas.py
badd +88 ginn/informes/treeview2pdf.py
badd +189 ginn/formularios/balas_cable.py
badd +13 ginn/informes/nied.py
badd +82 ginn/informes/norma2013.py
badd +65 ginn/formularios/widgets.py
badd +1 ginn/informes/ekotex.py
badd +7 ~/.vim/ftplugin/python.vim
badd +140 ginn/formularios/listado_balas.py
badd +254 ginn/formularios/consulta_pendientes_servir.py
badd +130 ginn/formularios/facturas_no_bloqueadas.py
badd +289 ginn/formularios/consumo_balas_partida.py
badd +324 ginn/formularios/categorias_laborales.py
badd +411 ginn/formularios/nominas.py
badd +93 ginn/framework/pclases/cliente.py
badd +1 ginn/formularios/consulta_cobros.py
badd +1020 ginn/formularios/pagares_cobros.py
badd +24 extra/patches/calcular_credito_disponible.sql
badd +301 ginn/formularios/pclase2tv.py
badd +94 ginn/formularios/consulta_control_horas.py
badd +533 ginn/formularios/horas_trabajadas.py
badd +550 ginn/formularios/horas_trabajadas_dia.py
badd +1 ginn/formularios/pedidos_de_compra.glade
badd +523 ginn/formularios/postomatic.py
badd +36 ginn/formularios/custom_widgets/cellrendererautocomplete.py
badd +47 ginn/formularios/custom_widgets/__init__.py
badd +39 ginn/informes/presupuesto2.py
badd +61 ginn/informes/albaran_multipag.py
badd +192 ginn/formularios/silos.py
badd +1 ginn/framework/__init__.py
badd +1 ginn/formularios/vencimientos_pendientes_por_cliente.glade
badd +416 ginn/formularios/consulta_productividad.py
badd +171 ginn/formularios/mail_sender.py
badd +1143 ginn/formularios/abonos_venta.py
badd +306 ginn/formularios/ventana_progreso.py
badd +993 ginn/formularios/control_personal.py
badd +195 ginn/formularios/listado_rollos.py
badd +74 ginn/formularios/consulta_existenciasRollos.py
badd +91 ginn/formularios/listado_rollos_defectuosos.py
badd +3498 ginn/formularios/consulta_global.py
badd +168 ginn/formularios/rollos_c.py
badd +56 extra/scripts/enviar_exitencias_geotextiles_a_comerciales.py
badd +1 ginn/informes/presupuesto.py
badd +112 ginn/formularios/consulta_libro_iva.py
badd +298 ginn/formularios/consulta_ofertas.py
badd +24 extra/patches/create_ventana_consultas.py
badd +203 ginn/lib/ezodf/ezodf/const.py
badd +61 ginn/lib/ezodf/ezodf/xmlns.py
badd +21 ginn/lib/simple_odspy/simpleodspy/sodsods.py
badd +17 ginn/lib/simple_odspy/simpleodspy/sodsspreadsheet.py
badd +41 ginn/lib/simple_odspy/simpleodspy/sodstable.py
badd +66 ginn/lib/odfpy/contrib/odscell/odscell
badd +127 ginn/lib/odfpy/contrib/odscell/odscell.py
badd +76 ginn/formularios/consulta_ofertas_pendientes_validar.py
badd +392 ginn/formularios/consulta_ofertas_estudio.py
badd +1075 ginn/formularios/confirmings.py
badd +177 ginn/formularios/transferencias.py
badd +66 ginn/formularios/cuentas_destino.py
badd +509 ginn/formularios/facturacion_por_cliente_y_fechas.py
badd +1 ginn/formularios/presupuestos.glade
badd +24 ginn/lib/simple_odspy/simpleodspy/sodsxls.py
badd +1 ginn/formularios/ofer
badd +1 ginn/formularios/usuarios.glade
badd +251 ginn/formularios/usuarios.py
badd +7 ginn/lib/xlutils/xlutils/copy.py
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
badd +65 ginn/formularios/consulta_albaranesPorFacturar.py
badd +1 ginn/formularios/checklist_window.py
args formularios/auditviewer.py
set lines=45 columns=102
edit ginn/formularios/presupuestos.py
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
9wincmd k
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
exe 'vert 1resize ' . ((&columns * 21 + 51) / 102)
exe '2resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 2resize ' . ((&columns * 80 + 51) / 102)
exe '3resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 3resize ' . ((&columns * 80 + 51) / 102)
exe '4resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 4resize ' . ((&columns * 80 + 51) / 102)
exe '5resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 5resize ' . ((&columns * 80 + 51) / 102)
exe '6resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 6resize ' . ((&columns * 80 + 51) / 102)
exe '7resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 7resize ' . ((&columns * 80 + 51) / 102)
exe '8resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 8resize ' . ((&columns * 80 + 51) / 102)
exe '9resize ' . ((&lines * 25 + 22) / 45)
exe 'vert 9resize ' . ((&columns * 80 + 51) / 102)
exe '10resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 10resize ' . ((&columns * 80 + 51) / 102)
exe '11resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 11resize ' . ((&columns * 80 + 51) / 102)
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
let s:l = 3168 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3168
normal! 025|
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
780
normal! zo
1105
normal! zo
1197
normal! zo
1206
normal! zo
1248
normal! zo
1254
normal! zo
1254
normal! zo
1254
normal! zo
1281
normal! zo
1287
normal! zo
1287
normal! zo
1287
normal! zo
1306
normal! zo
1315
normal! zo
1415
normal! zo
1424
normal! zo
1524
normal! zo
1533
normal! zo
1633
normal! zo
1754
normal! zo
2455
normal! zo
2834
normal! zo
3532
normal! zo
3844
normal! zo
3878
normal! zo
3880
normal! zo
3936
normal! zo
3941
normal! zo
3943
normal! zo
3944
normal! zo
3944
normal! zo
3944
normal! zo
3944
normal! zo
3944
normal! zo
3944
normal! zo
3968
normal! zo
4031
normal! zo
4031
normal! zo
4031
normal! zo
4031
normal! zo
4031
normal! zo
4031
normal! zo
4053
normal! zo
4080
normal! zo
4034
normal! zo
4034
normal! zo
4040
normal! zo
4042
normal! zo
4047
normal! zo
4050
normal! zo
4052
normal! zo
4057
normal! zo
4058
normal! zo
4068
normal! zo
4076
normal! zo
4077
normal! zo
4077
normal! zo
4077
normal! zo
4077
normal! zo
4081
normal! zo
4084
normal! zo
4085
normal! zo
4085
normal! zo
4085
normal! zo
4085
normal! zo
4085
normal! zo
4099
normal! zo
4122
normal! zo
4153
normal! zo
4166
normal! zo
4579
normal! zo
4590
normal! zo
4724
normal! zo
4809
normal! zo
4848
normal! zo
4860
normal! zo
4861
normal! zo
4861
normal! zo
4861
normal! zo
5138
normal! zo
5162
normal! zo
5173
normal! zo
5173
normal! zo
5173
normal! zo
5217
normal! zo
5239
normal! zo
5239
normal! zo
5239
normal! zo
5239
normal! zo
5239
normal! zo
5225
normal! zo
5231
normal! zo
5231
normal! zo
5231
normal! zo
5231
normal! zo
5247
normal! zo
5247
normal! zo
5247
normal! zo
5247
normal! zo
5247
normal! zo
5343
normal! zo
5349
normal! zo
5373
normal! zo
5400
normal! zo
5454
normal! zo
5490
normal! zo
5502
normal! zo
5503
normal! zo
5504
normal! zo
5504
normal! zo
5504
normal! zo
5504
normal! zo
5506
normal! zo
5506
normal! zo
5506
normal! zo
5506
normal! zo
5506
normal! zo
5557
normal! zo
5557
normal! zo
5557
normal! zo
5557
normal! zo
5557
normal! zo
5585
normal! zo
5588
normal! zo
5607
normal! zo
5608
normal! zo
5609
normal! zo
5792
normal! zo
5847
normal! zo
5859
normal! zo
5924
normal! zo
5968
normal! zo
5976
normal! zo
6002
normal! zo
6015
normal! zo
6019
normal! zo
6025
normal! zo
6158
normal! zo
6284
normal! zo
7540
normal! zo
7569
normal! zo
7569
normal! zo
7569
normal! zo
7569
normal! zo
7569
normal! zo
7593
normal! zo
7654
normal! zo
7686
normal! zo
7687
normal! zo
7688
normal! zo
7693
normal! zo
7699
normal! zo
7662
normal! zo
7681
normal! zo
7684
normal! zo
7685
normal! zo
7685
normal! zo
7685
normal! zo
7698
normal! zo
7699
normal! zo
7700
normal! zo
7705
normal! zo
7711
normal! zo
7717
normal! zo
7717
normal! zo
7717
normal! zo
7717
normal! zo
7717
normal! zo
7717
normal! zo
7719
normal! zo
7758
normal! zo
7768
normal! zo
7769
normal! zo
7777
normal! zo
7778
normal! zo
7781
normal! zo
7786
normal! zo
7787
normal! zo
7788
normal! zo
7789
normal! zo
7789
normal! zo
7789
normal! zo
7789
normal! zo
7789
normal! zo
7789
normal! zo
7793
normal! zo
7799
normal! zo
7802
normal! zo
7802
normal! zo
7802
normal! zo
7802
normal! zo
7802
normal! zo
7811
normal! zo
7812
normal! zo
7813
normal! zo
7821
normal! zo
7828
normal! zo
7828
normal! zo
7828
normal! zo
7828
normal! zo
7828
normal! zo
7828
normal! zo
7830
normal! zo
7830
normal! zo
7830
normal! zo
7830
normal! zo
7830
normal! zo
7830
normal! zo
7830
normal! zo
7833
normal! zo
7833
normal! zo
7833
normal! zo
7833
normal! zo
7833
normal! zo
7833
normal! zo
7834
normal! zo
7834
normal! zo
7834
normal! zo
7834
normal! zo
7836
normal! zo
7837
normal! zo
7846
normal! zo
7853
normal! zo
7853
normal! zo
7853
normal! zo
7853
normal! zo
7853
normal! zo
7853
normal! zo
7855
normal! zo
7858
normal! zo
7858
normal! zo
7858
normal! zo
7858
normal! zo
7858
normal! zo
7858
normal! zo
7859
normal! zo
7859
normal! zo
7859
normal! zo
7859
normal! zo
7861
normal! zo
7862
normal! zo
7865
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
7870
normal! zo
7918
normal! zo
7919
normal! zo
7920
normal! zo
7935
normal! zo
7937
normal! zo
7923
normal! zo
7925
normal! zo
7926
normal! zo
7926
normal! zo
7926
normal! zo
7926
normal! zo
7926
normal! zo
7926
normal! zo
7929
normal! zo
7935
normal! zo
7938
normal! zo
7947
normal! zo
7949
normal! zo
7950
normal! zo
7957
normal! zo
7958
normal! zo
7959
normal! zo
7964
normal! zo
7965
normal! zo
7964
normal! zo
7968
normal! zo
7976
normal! zo
7977
normal! zo
7979
normal! zo
7979
normal! zo
7986
normal! zo
7987
normal! zo
7988
normal! zo
7988
normal! zo
7988
normal! zo
7988
normal! zo
7988
normal! zo
7988
normal! zo
7988
normal! zo
7988
normal! zo
7991
normal! zo
7991
normal! zo
7991
normal! zo
7998
normal! zo
8000
normal! zo
8283
normal! zo
8294
normal! zo
8295
normal! zo
8295
normal! zo
8295
normal! zo
8295
normal! zo
8295
normal! zo
8295
normal! zo
8295
normal! zo
8298
normal! zo
8298
normal! zo
8298
normal! zo
8298
normal! zo
8298
normal! zo
8298
normal! zo
8298
normal! zo
8302
normal! zo
8309
normal! zo
8309
normal! zo
8309
normal! zo
8309
normal! zo
8309
normal! zo
8309
normal! zo
8309
normal! zo
8309
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
8312
normal! zo
8747
normal! zo
8751
normal! zo
8782
normal! zo
8831
normal! zo
8838
normal! zo
9006
normal! zo
9017
normal! zo
9030
normal! zo
9031
normal! zo
9044
normal! zo
9049
normal! zo
9054
normal! zo
9059
normal! zo
9070
normal! zo
9093
normal! zo
9116
normal! zo
9117
normal! zo
9117
normal! zo
9117
normal! zo
9117
normal! zo
9117
normal! zo
9117
normal! zo
9128
normal! zo
9143
normal! zo
9266
normal! zo
9296
normal! zo
9303
normal! zo
9306
normal! zo
9410
normal! zo
9672
normal! zo
9698
normal! zo
9737
normal! zo
9748
normal! zo
9749
normal! zo
9762
normal! zo
9777
normal! zo
9793
normal! zo
9810
normal! zo
9810
normal! zo
9810
normal! zo
9810
normal! zo
9810
normal! zo
9810
normal! zo
9810
normal! zo
9810
normal! zo
9810
normal! zo
9817
normal! zo
9831
normal! zo
9832
normal! zo
9832
normal! zo
9834
normal! zo
9835
normal! zo
9835
normal! zo
9837
normal! zo
9838
normal! zo
9838
normal! zo
9840
normal! zo
9841
normal! zo
9841
normal! zo
9843
normal! zo
9846
normal! zo
9848
normal! zo
9848
normal! zo
9848
normal! zo
9857
normal! zo
9859
normal! zo
9865
normal! zo
9865
normal! zo
9865
normal! zo
9881
normal! zo
9870
normal! zo
9873
normal! zo
9874
normal! zo
9874
normal! zo
9877
normal! zo
9877
normal! zo
9877
normal! zo
9880
normal! zo
9880
normal! zo
9880
normal! zo
9880
normal! zo
9886
normal! zo
9889
normal! zo
9893
normal! zo
9900
normal! zo
9902
normal! zo
9949
normal! zo
9963
normal! zo
9964
normal! zo
9966
normal! zo
10001
normal! zo
10008
normal! zo
10013
normal! zo
10014
normal! zo
10019
normal! zo
10019
normal! zo
10019
normal! zo
10019
normal! zo
10019
normal! zo
10022
normal! zo
10022
normal! zo
10022
normal! zo
10048
normal! zo
10057
normal! zo
10062
normal! zo
10064
normal! zo
10069
normal! zo
10075
normal! zo
10083
normal! zo
10084
normal! zo
10084
normal! zo
10084
normal! zo
10084
normal! zo
10093
normal! zo
10094
normal! zo
10099
normal! zo
10148
normal! zo
10153
normal! zo
10266
normal! zo
10293
normal! zo
10298
normal! zo
10304
normal! zo
10390
normal! zo
10397
normal! zo
10398
normal! zo
10416
normal! zo
10446
normal! zo
10446
normal! zo
10446
normal! zo
10446
normal! zo
10446
normal! zo
10449
normal! zo
10457
normal! zo
10458
normal! zo
10503
normal! zo
10523
normal! zo
10524
normal! zo
10525
normal! zo
10525
normal! zo
10525
normal! zo
10525
normal! zo
10525
normal! zo
10525
normal! zo
10525
normal! zo
10525
normal! zo
10525
normal! zo
10542
normal! zo
10548
normal! zo
10558
normal! zo
10565
normal! zo
10566
normal! zo
10567
normal! zo
10567
normal! zo
10567
normal! zo
10590
normal! zo
10608
normal! zo
10573
normal! zo
10576
normal! zo
10579
normal! zo
10579
normal! zo
10579
normal! zo
10582
normal! zo
10582
normal! zo
10582
normal! zo
10582
normal! zo
10587
normal! zo
10587
normal! zo
10587
normal! zo
10595
normal! zo
10602
normal! zo
10609
normal! zo
10612
normal! zo
10614
normal! zo
10617
normal! zo
10620
normal! zo
10625
normal! zo
10636
normal! zo
10643
normal! zo
10647
normal! zo
10648
normal! zo
10648
normal! zo
10650
normal! zo
10651
normal! zo
10651
normal! zo
10653
normal! zo
10654
normal! zo
10654
normal! zo
10656
normal! zo
10657
normal! zo
10657
normal! zo
10659
normal! zo
10660
normal! zo
10660
normal! zo
10662
normal! zo
10663
normal! zo
10663
normal! zo
10665
normal! zo
10666
normal! zo
10666
normal! zo
10668
normal! zo
10671
normal! zo
10673
normal! zo
10673
normal! zo
10673
normal! zo
10679
normal! zo
10680
normal! zo
10680
normal! zo
10682
normal! zo
10683
normal! zo
10683
normal! zo
10707
normal! zo
10711
normal! zo
10714
normal! zo
10715
normal! zo
10715
normal! zo
10715
normal! zo
10715
normal! zo
10715
normal! zo
10715
normal! zo
10720
normal! zo
10721
normal! zo
10721
normal! zo
10721
normal! zo
10724
normal! zo
10836
normal! zo
10912
normal! zo
10920
normal! zo
10927
normal! zo
10927
normal! zo
10927
normal! zo
10927
normal! zo
10927
normal! zo
10927
normal! zo
10927
normal! zo
10938
normal! zo
10942
normal! zo
10943
normal! zo
10943
normal! zo
10943
normal! zo
10953
normal! zo
10956
normal! zo
10963
normal! zo
10972
normal! zo
10981
normal! zo
11091
normal! zo
11105
normal! zo
11105
normal! zo
11105
normal! zo
11105
normal! zo
11117
normal! zo
11130
normal! zo
11143
normal! zo
11150
normal! zo
11152
normal! zo
11152
normal! zo
11152
normal! zo
11152
normal! zo
11152
normal! zo
11152
normal! zo
11169
normal! zo
11177
normal! zo
11205
normal! zo
11217
normal! zo
11218
normal! zo
11218
normal! zo
11218
normal! zo
11218
normal! zo
11411
normal! zo
11422
normal! zo
11439
normal! zo
11439
normal! zo
11443
normal! zo
11448
normal! zo
11448
normal! zo
11450
normal! zo
11451
normal! zo
11451
normal! zo
11456
normal! zo
11456
normal! zo
11456
normal! zo
11456
normal! zo
11456
normal! zo
11469
normal! zo
11472
normal! zo
11472
normal! zo
11472
normal! zo
11472
normal! zo
11478
normal! zo
11478
normal! zo
11478
normal! zo
11478
normal! zo
11478
normal! zo
11506
normal! zo
11604
normal! zo
11604
normal! zo
11604
normal! zo
11604
normal! zo
11604
normal! zo
11604
normal! zo
11604
normal! zo
11604
normal! zo
11604
normal! zo
11604
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
11666
normal! zo
11667
normal! zo
11994
normal! zo
11994
normal! zo
11994
normal! zo
12008
normal! zo
12045
normal! zo
12056
normal! zo
12061
normal! zo
12079
normal! zo
12079
normal! zo
12079
normal! zo
12079
normal! zo
12080
normal! zo
12085
normal! zo
12101
normal! zo
12101
normal! zo
12101
normal! zo
12101
normal! zo
13297
normal! zo
13431
normal! zo
13436
normal! zo
13439
normal! zo
13441
normal! zo
13446
normal! zo
13447
normal! zo
13448
normal! zo
13448
normal! zo
13448
normal! zo
13448
normal! zo
13448
normal! zo
13448
normal! zo
13448
normal! zo
13448
normal! zo
13448
normal! zo
13448
normal! zo
13454
normal! zo
13455
normal! zo
13456
normal! zo
13456
normal! zo
13456
normal! zo
13456
normal! zo
13456
normal! zo
13456
normal! zo
13456
normal! zo
13458
normal! zo
13458
normal! zo
13458
normal! zo
13458
normal! zo
13458
normal! zo
13458
normal! zo
13458
normal! zo
13458
normal! zo
13460
normal! zo
13461
normal! zo
13461
normal! zo
13461
normal! zo
13461
normal! zo
13461
normal! zo
13461
normal! zo
13461
normal! zo
13461
normal! zo
13461
normal! zo
13464
normal! zo
13466
normal! zo
13466
normal! zo
13471
normal! zo
13471
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
13601
normal! zo
13601
normal! zo
13601
normal! zo
13616
normal! zo
13617
normal! zo
13622
normal! zo
13627
normal! zo
13628
normal! zo
13629
normal! zo
13629
normal! zo
13629
normal! zo
13629
normal! zo
13629
normal! zo
13629
normal! zo
13629
normal! zo
13629
normal! zo
13629
normal! zo
13629
normal! zo
13635
normal! zo
13636
normal! zo
13637
normal! zo
13637
normal! zo
13637
normal! zo
13637
normal! zo
13637
normal! zo
13637
normal! zo
13637
normal! zo
13639
normal! zo
13639
normal! zo
13639
normal! zo
13639
normal! zo
13639
normal! zo
13639
normal! zo
13639
normal! zo
13639
normal! zo
13641
normal! zo
13642
normal! zo
13642
normal! zo
13642
normal! zo
13642
normal! zo
13642
normal! zo
13642
normal! zo
13642
normal! zo
13642
normal! zo
13642
normal! zo
13645
normal! zo
13647
normal! zo
13652
normal! zo
13661
normal! zo
13662
normal! zo
13662
normal! zo
13662
normal! zo
13662
normal! zo
13662
normal! zo
13662
normal! zo
13662
normal! zo
13732
normal! zo
13743
normal! zo
13748
normal! zo
13749
normal! zo
13750
normal! zo
13750
normal! zo
13750
normal! zo
13750
normal! zo
13750
normal! zo
13750
normal! zo
13750
normal! zo
13750
normal! zo
13750
normal! zo
13750
normal! zo
13756
normal! zo
13757
normal! zo
13758
normal! zo
13758
normal! zo
13758
normal! zo
13758
normal! zo
13758
normal! zo
13758
normal! zo
13758
normal! zo
13760
normal! zo
13760
normal! zo
13760
normal! zo
13760
normal! zo
13760
normal! zo
13760
normal! zo
13760
normal! zo
13760
normal! zo
13762
normal! zo
13763
normal! zo
13763
normal! zo
13763
normal! zo
13763
normal! zo
13763
normal! zo
13763
normal! zo
13763
normal! zo
13763
normal! zo
13763
normal! zo
13766
normal! zo
13768
normal! zo
13773
normal! zo
13782
normal! zo
13783
normal! zo
13783
normal! zo
13783
normal! zo
13783
normal! zo
13783
normal! zo
13783
normal! zo
13783
normal! zo
13890
normal! zo
13890
normal! zo
13890
normal! zo
13890
normal! zo
13890
normal! zo
13890
normal! zo
13890
normal! zo
13890
normal! zo
13890
normal! zo
13900
normal! zo
13900
normal! zo
13900
normal! zo
13900
normal! zo
13900
normal! zo
13900
normal! zo
13902
normal! zo
13903
normal! zo
13903
normal! zo
13903
normal! zo
14098
normal! zo
14098
normal! zo
14098
normal! zo
14098
normal! zo
14114
normal! zo
14119
normal! zo
14120
normal! zo
14121
normal! zo
14121
normal! zo
14121
normal! zo
14121
normal! zo
14121
normal! zo
14121
normal! zo
14121
normal! zo
14121
normal! zo
14121
normal! zo
14121
normal! zo
14127
normal! zo
14128
normal! zo
14129
normal! zo
14129
normal! zo
14129
normal! zo
14129
normal! zo
14129
normal! zo
14129
normal! zo
14129
normal! zo
14131
normal! zo
14131
normal! zo
14131
normal! zo
14131
normal! zo
14131
normal! zo
14131
normal! zo
14131
normal! zo
14131
normal! zo
14131
normal! zo
14133
normal! zo
14134
normal! zo
14134
normal! zo
14134
normal! zo
14134
normal! zo
14134
normal! zo
14134
normal! zo
14134
normal! zo
14134
normal! zo
14134
normal! zo
14137
normal! zo
14139
normal! zo
14139
normal! zo
14144
normal! zo
14144
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
14215
normal! zo
14215
normal! zo
14215
normal! zo
14215
normal! zo
14227
normal! zo
14232
normal! zo
14233
normal! zo
14234
normal! zo
14234
normal! zo
14234
normal! zo
14234
normal! zo
14234
normal! zo
14234
normal! zo
14234
normal! zo
14234
normal! zo
14234
normal! zo
14234
normal! zo
14240
normal! zo
14241
normal! zo
14242
normal! zo
14242
normal! zo
14242
normal! zo
14242
normal! zo
14242
normal! zo
14242
normal! zo
14242
normal! zo
14244
normal! zo
14244
normal! zo
14244
normal! zo
14244
normal! zo
14244
normal! zo
14244
normal! zo
14244
normal! zo
14244
normal! zo
14244
normal! zo
14246
normal! zo
14247
normal! zo
14247
normal! zo
14247
normal! zo
14247
normal! zo
14247
normal! zo
14247
normal! zo
14247
normal! zo
14247
normal! zo
14247
normal! zo
14250
normal! zo
14252
normal! zo
14252
normal! zo
14257
normal! zo
14257
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
14336
normal! zo
14348
normal! zo
14351
normal! zo
14352
normal! zo
14353
normal! zo
14353
normal! zo
14353
normal! zo
14355
normal! zo
14356
normal! zo
14356
normal! zo
14356
normal! zo
14372
normal! zo
14641
normal! zo
14683
normal! zo
15069
normal! zo
15071
normal! zo
15075
normal! zo
15102
normal! zo
14383
normal! zo
14392
normal! zo
14402
normal! zo
14429
normal! zo
14434
normal! zo
14440
normal! zo
14451
normal! zo
14464
normal! zo
14488
normal! zo
14490
normal! zo
14493
normal! zo
14496
normal! zo
14497
normal! zo
14501
normal! zo
14502
normal! zo
14516
normal! zo
14516
normal! zo
14516
normal! zo
14516
normal! zo
14538
normal! zo
14539
normal! zo
14540
normal! zo
14540
normal! zo
14540
normal! zo
14540
normal! zo
14540
normal! zo
14540
normal! zo
14540
normal! zo
14540
normal! zo
14540
normal! zo
14540
normal! zo
14549
normal! zo
14550
normal! zo
14556
normal! zo
14560
normal! zo
14561
normal! zo
14570
normal! zo
14571
normal! zo
14579
normal! zo
14580
normal! zo
14586
normal! zo
14601
normal! zo
14609
normal! zo
14615
normal! zo
14621
normal! zo
14626
normal! zo
14630
normal! zo
14636
normal! zo
14641
normal! zo
14642
normal! zo
14647
normal! zo
14658
normal! zo
14676
normal! zo
14718
normal! zo
14724
normal! zo
14730
normal! zo
14737
normal! zo
14746
normal! zo
14748
normal! zo
14755
normal! zo
14755
normal! zo
14755
normal! zo
14755
normal! zo
14755
normal! zo
14755
normal! zo
14772
normal! zo
14784
normal! zo
14795
normal! zo
14796
normal! zo
14812
normal! zo
14829
normal! zo
14833
normal! zo
14834
normal! zo
14835
normal! zo
14835
normal! zo
14837
normal! zo
14840
normal! zo
14853
normal! zo
14863
normal! zo
14865
normal! zo
14869
normal! zo
14870
normal! zo
14870
normal! zo
14870
normal! zo
14870
normal! zo
14870
normal! zo
14870
normal! zo
14883
normal! zo
14904
normal! zo
14905
normal! zo
14912
normal! zo
14945
normal! zo
14946
normal! zo
14946
normal! zo
14962
normal! zo
14968
normal! zo
14971
normal! zo
14971
normal! zo
14971
normal! zo
14977
normal! zo
14977
normal! zo
14997
normal! zo
15002
normal! zo
15007
normal! zo
15015
normal! zo
15034
normal! zo
15068
normal! zo
15076
normal! zo
15085
normal! zo
15104
normal! zo
15106
normal! zo
15110
normal! zo
15127
normal! zo
15133
normal! zo
15137
normal! zo
15469
normal! zo
15500
normal! zo
15524
normal! zo
15534
normal! zo
15534
normal! zo
15534
normal! zo
15534
normal! zo
15534
normal! zo
15722
normal! zo
15741
normal! zo
15763
normal! zo
15768
normal! zo
15769
normal! zo
15769
normal! zo
15772
normal! zo
15773
normal! zo
15773
normal! zo
15773
normal! zo
15776
normal! zo
15776
normal! zo
15776
normal! zo
15780
normal! zo
15780
normal! zo
15780
normal! zo
15780
normal! zo
15780
normal! zo
15780
normal! zo
15780
normal! zo
15780
normal! zo
15780
normal! zo
16311
normal! zo
16405
normal! zo
16420
normal! zo
16431
normal! zo
16431
normal! zo
16478
normal! zo
16511
normal! zo
16702
normal! zo
16713
normal! zo
16713
normal! zo
16713
normal! zo
16713
normal! zo
16715
normal! zo
16716
normal! zo
16717
normal! zo
16718
normal! zo
16719
normal! zo
16723
normal! zo
16724
normal! zo
16725
normal! zo
16725
normal! zo
16725
normal! zo
16725
normal! zo
16725
normal! zo
16725
normal! zo
16725
normal! zo
16727
normal! zo
16729
normal! zo
16734
normal! zo
16734
normal! zo
16734
normal! zo
16734
normal! zo
16740
normal! zo
16347
normal! zo
16362
normal! zo
16374
normal! zo
16382
normal! zo
16385
normal! zo
16391
normal! zo
16397
normal! zo
16400
normal! zo
16406
normal! zo
16420
normal! zo
16426
normal! zo
16431
normal! zo
16434
normal! zo
16434
normal! zo
16434
normal! zo
16444
normal! zo
16459
normal! zo
16470
normal! zo
16470
normal! zo
16481
normal! zo
16496
normal! zo
16506
normal! zo
16517
normal! zo
16522
normal! zo
16522
normal! zo
16522
normal! zo
16535
normal! zo
16561
normal! zo
16582
normal! zo
16601
normal! zo
16609
normal! zo
16610
normal! zo
16611
normal! zo
16615
normal! zo
16619
normal! zo
16635
normal! zo
16650
normal! zo
16655
normal! zo
16660
normal! zo
16670
normal! zo
16671
normal! zo
16671
normal! zo
16671
normal! zo
16673
normal! zo
16673
normal! zo
16673
normal! zo
16673
normal! zo
16673
normal! zo
16673
normal! zo
16673
normal! zo
16673
normal! zo
16673
normal! zo
16673
normal! zo
16678
normal! zo
16679
normal! zo
16685
normal! zo
16686
normal! zo
16706
normal! zo
16731
normal! zo
16735
normal! zo
16752
normal! zo
16763
normal! zo
16763
normal! zo
16763
normal! zo
16763
normal! zo
16765
normal! zo
16766
normal! zo
16767
normal! zo
16768
normal! zo
16769
normal! zo
16773
normal! zo
16774
normal! zo
16775
normal! zo
16775
normal! zo
16775
normal! zo
16775
normal! zo
16775
normal! zo
16775
normal! zo
16775
normal! zo
16777
normal! zo
16779
normal! zo
16784
normal! zo
16784
normal! zo
16784
normal! zo
16784
normal! zo
16790
normal! zo
16794
normal! zo
16802
normal! zo
16802
normal! zo
16802
normal! zo
16802
normal! zo
16810
normal! zo
16818
normal! zo
16819
normal! zo
16822
normal! zo
16827
normal! zo
16835
normal! zo
16840
normal! zo
16848
normal! zo
16853
normal! zo
16862
normal! zo
16863
normal! zo
16863
normal! zo
16873
normal! zo
16881
normal! zo
16883
normal! zo
16886
normal! zo
16887
normal! zo
16890
normal! zo
16892
normal! zo
16914
normal! zo
16921
normal! zo
16926
normal! zo
16939
normal! zo
16940
normal! zo
16940
normal! zo
16940
normal! zo
16945
normal! zo
16958
normal! zo
16965
normal! zo
16966
normal! zo
16981
normal! zo
16988
normal! zo
17002
normal! zo
17009
normal! zo
17010
normal! zo
17015
normal! zo
17024
normal! zo
17038
normal! zo
17060
normal! zo
17081
normal! zo
17094
normal! zo
17094
normal! zo
17094
normal! zo
17094
normal! zo
17094
normal! zo
17094
normal! zo
17104
normal! zo
17105
normal! zo
17107
normal! zo
17109
normal! zo
17112
normal! zo
17119
normal! zo
17131
normal! zo
17141
normal! zo
17141
normal! zo
17141
normal! zo
17141
normal! zo
17141
normal! zo
17141
normal! zo
17117
normal! zo
17141
normal! zo
17146
normal! zo
17148
normal! zo
17151
normal! zo
17158
normal! zo
17170
normal! zo
17180
normal! zo
17180
normal! zo
17180
normal! zo
17180
normal! zo
17180
normal! zo
17180
normal! zo
17188
normal! zo
17198
normal! zo
17198
normal! zo
17198
normal! zo
17198
normal! zo
17198
normal! zo
17198
normal! zo
17206
normal! zo
17207
normal! zo
17218
normal! zo
17223
normal! zo
17234
normal! zo
17242
normal! zo
17255
normal! zo
17259
normal! zo
17259
normal! zo
17259
normal! zo
17259
normal! zo
17259
normal! zo
17261
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
17273
normal! zo
17277
normal! zo
17277
normal! zo
17277
normal! zo
17277
normal! zo
17277
normal! zo
17277
normal! zo
17283
normal! zo
17283
normal! zo
17283
normal! zo
17283
normal! zo
17286
normal! zo
17287
normal! zo
17288
normal! zo
17294
normal! zo
17295
normal! zo
17295
normal! zo
17295
normal! zo
17505
normal! zo
17506
normal! zo
17496
normal! zo
17562
normal! zo
17577
normal! zo
17584
normal! zo
17585
normal! zo
17601
normal! zo
17611
normal! zo
17625
normal! zo
17628
normal! zo
17629
normal! zo
17629
normal! zo
17647
normal! zo
17654
normal! zo
17657
normal! zo
17651
normal! zo
17671
normal! zo
17683
normal! zo
17683
normal! zo
17683
normal! zo
17683
normal! zo
17683
normal! zo
17686
normal! zo
17693
normal! zo
17696
normal! zo
17707
normal! zo
17713
normal! zo
17718
normal! zo
17724
normal! zo
17725
normal! zo
17726
normal! zo
17729
normal! zo
17748
normal! zo
17763
normal! zo
17791
normal! zo
17816
normal! zo
17837
normal! zo
17872
normal! zo
17881
normal! zo
17882
normal! zo
17883
normal! zo
17885
normal! zo
17885
normal! zo
17885
normal! zo
17888
normal! zo
17890
normal! zo
17890
normal! zo
17890
normal! zo
17893
normal! zo
17894
normal! zo
17894
normal! zo
17894
normal! zo
17894
normal! zo
17894
normal! zo
18420
normal! zo
18437
normal! zo
18447
normal! zo
18450
normal! zo
18451
normal! zo
18451
normal! zo
18457
normal! zo
18464
normal! zo
18465
normal! zo
18466
normal! zo
18466
normal! zo
18466
normal! zo
18466
normal! zo
18470
normal! zo
18471
normal! zo
18471
normal! zo
18471
normal! zo
18471
normal! zo
18487
normal! zo
19705
normal! zo
19729
normal! zo
19735
normal! zo
19741
normal! zo
19759
normal! zo
19769
normal! zo
19772
normal! zo
19779
normal! zo
19779
normal! zo
19779
normal! zo
19779
normal! zo
19784
normal! zo
20064
normal! zo
20070
normal! zo
20070
normal! zo
20075
normal! zo
20079
normal! zo
20086
normal! zo
20093
normal! zo
20100
normal! zo
20107
normal! zo
20114
normal! zo
20121
normal! zo
20127
normal! zo
20128
normal! zo
20137
normal! zo
20146
normal! zo
20309
normal! zo
20319
normal! zo
20330
normal! zo
20331
normal! zo
20341
normal! zo
20342
normal! zo
20347
normal! zo
20348
normal! zo
20348
normal! zo
20358
normal! zo
20358
normal! zo
20358
normal! zo
20358
normal! zo
20358
normal! zo
20358
normal! zo
20358
normal! zo
20358
normal! zo
20358
normal! zo
20369
normal! zo
20370
normal! zo
20378
normal! zo
20378
normal! zo
20378
normal! zo
20378
normal! zo
20378
normal! zo
20378
normal! zo
20378
normal! zo
20378
normal! zo
20389
normal! zo
20390
normal! zo
20428
normal! zo
20446
normal! zo
20463
normal! zo
20467
normal! zo
20472
normal! zo
20484
normal! zo
20484
normal! zo
20484
normal! zo
20484
normal! zo
20484
normal! zo
20484
normal! zo
20484
normal! zo
20502
normal! zo
let s:l = 16551 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
16551
normal! 037|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/lib/xlutils/xlutils/copy.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
10
normal! zo
let s:l = 20 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
20
normal! 09|
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
let s:l = 314 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
314
normal! 017|
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
922
normal! zo
1068
normal! zo
let s:l = 926 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
926
normal! 020|
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/partes_de_fabricacion_balas.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
108
normal! zo
3524
normal! zo
3536
normal! zo
3553
normal! zo
3562
normal! zo
let s:l = 3592 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3592
normal! 021|
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/consulta_albaranesPorFacturar.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
52
normal! zo
57
normal! zo
65
normal! zo
65
normal! zo
65
normal! zo
178
normal! zo
193
normal! zo
204
normal! zo
213
normal! zo
214
normal! zo
325
normal! zo
336
normal! zo
339
normal! zo
340
normal! zo
343
normal! zo
343
normal! zo
344
normal! zo
344
normal! zo
347
normal! zo
348
normal! zo
348
normal! zo
349
normal! zo
349
normal! zo
352
normal! zo
352
normal! zo
353
normal! zo
353
normal! zo
358
normal! zo
360
normal! zo
361
normal! zo
365
normal! zo
366
normal! zo
369
normal! zo
372
normal! zo
373
normal! zo
374
normal! zo
377
normal! zo
378
normal! zo
382
normal! zo
385
normal! zo
385
normal! zo
385
normal! zo
385
normal! zo
389
normal! zo
392
normal! zo
392
normal! zo
392
normal! zo
392
normal! zo
403
normal! zo
409
normal! zo
410
normal! zo
412
normal! zo
413
normal! zo
let s:l = 385 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
385
normal! 034|
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/consulta_productividad.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
53
normal! zo
57
normal! zo
73
normal! zo
73
normal! zo
153
normal! zo
212
normal! zo
253
normal! zo
254
normal! zo
385
normal! zo
398
normal! zo
417
normal! zo
417
normal! zo
417
normal! zo
430
normal! zo
481
normal! zo
491
normal! zo
503
normal! zo
let s:l = 466 - ((19 * winheight(0) + 12) / 25)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
466
normal! 050|
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
68
normal! zo
69
normal! zo
77
normal! zo
77
normal! zo
77
normal! zo
77
normal! zo
161
normal! zo
161
normal! zo
161
normal! zo
224
normal! zo
230
normal! zo
271
normal! zo
288
normal! zo
384
normal! zo
405
normal! zo
414
normal! zo
460
normal! zo
471
normal! zo
480
normal! zo
1133
normal! zo
1140
normal! zo
1142
normal! zo
1200
normal! zo
1234
normal! zo
1573
normal! zo
1720
normal! zo
1729
normal! zo
1730
normal! zo
1768
normal! zo
1842
normal! zo
1848
normal! zo
1849
normal! zo
1897
normal! zo
1899
normal! zo
1905
normal! zo
1910
normal! zo
1915
normal! zo
1915
normal! zo
2105
normal! zo
2114
normal! zo
2114
normal! zo
2114
normal! zo
2114
normal! zo
2114
normal! zo
2151
normal! zo
2151
normal! zo
2151
normal! zo
2151
normal! zo
2151
normal! zo
2151
normal! zo
2151
normal! zo
2151
normal! zo
2227
normal! zo
2239
normal! zo
2240
normal! zo
2258
normal! zo
2259
normal! zo
2264
normal! zo
2264
normal! zo
2300
normal! zo
2312
normal! zo
2313
normal! zo
2314
normal! zo
2314
normal! zo
2314
normal! zo
2314
normal! zo
2314
normal! zo
2314
normal! zo
2314
normal! zo
2314
normal! zo
2392
normal! zo
2406
normal! zo
2406
normal! zo
2406
normal! zo
2406
normal! zo
2406
normal! zo
2406
normal! zo
2407
normal! zo
2411
normal! zo
2419
normal! zo
2430
normal! zo
2431
normal! zo
2431
normal! zo
2431
normal! zo
2431
normal! zo
2447
normal! zo
2447
normal! zo
2473
normal! zo
2474
normal! zo
2475
normal! zo
2487
normal! zo
2503
normal! zo
2505
normal! zo
2520
normal! zo
2552
normal! zo
2553
normal! zo
2553
normal! zo
2554
normal! zo
2560
normal! zo
3001
normal! zo
3003
normal! zo
3043
normal! zo
let s:l = 1236 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1236
normal! 037|
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
let s:l = 523 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
523
normal! 022|
wincmd w
9wincmd w
exe 'vert 1resize ' . ((&columns * 21 + 51) / 102)
exe '2resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 2resize ' . ((&columns * 80 + 51) / 102)
exe '3resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 3resize ' . ((&columns * 80 + 51) / 102)
exe '4resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 4resize ' . ((&columns * 80 + 51) / 102)
exe '5resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 5resize ' . ((&columns * 80 + 51) / 102)
exe '6resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 6resize ' . ((&columns * 80 + 51) / 102)
exe '7resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 7resize ' . ((&columns * 80 + 51) / 102)
exe '8resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 8resize ' . ((&columns * 80 + 51) / 102)
exe '9resize ' . ((&lines * 25 + 22) / 45)
exe 'vert 9resize ' . ((&columns * 80 + 51) / 102)
exe '10resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 10resize ' . ((&columns * 80 + 51) / 102)
exe '11resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 11resize ' . ((&columns * 80 + 51) / 102)
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
9wincmd w

" vim: ft=vim ro nowrap smc=128
