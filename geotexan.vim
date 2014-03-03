" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 03 marzo 2014 at 20:25:04.
" Open this file in Vim and run :source % to restore your session.

set guioptions=aegimrLtT
silent! set guifont=Inconsolata\ 12
if exists('g:syntax_on') != 1 | syntax on | endif
if exists('g:did_load_filetypes') != 1 | filetype on | endif
if exists('g:did_load_ftplugin') != 1 | filetype plugin on | endif
if exists('g:did_indent_on') != 1 | filetype indent on | endif
if &background != 'dark'
	set background=dark
endif
if !exists('g:colors_name') || g:colors_name != 'distinguished' | colorscheme distinguished | endif
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
badd +339 ginn/formularios/consulta_producido.py
badd +1 ginn/__init__.py
badd +1505 ginn/formularios/clientes.py
badd +991 ginn/formularios/productos_compra.py
badd +39 ginn/formularios/productos_de_venta_balas.py
badd +525 ginn/formularios/recibos.py
badd +603 ginn/formularios/productos_de_venta_rollos.py
badd +382 ginn/formularios/productos_de_venta_rollos_geocompuestos.py
badd +417 ginn/formularios/productos_de_venta_especial.py
badd +3326 ginn/formularios/partes_de_fabricacion_balas.py
badd +951 ginn/formularios/partes_de_fabricacion_bolsas.py
badd +35 ginn/formularios/partes_de_fabricacion_rollos.py
badd +312 ginn/formularios/proveedores.py
badd +547 ~/workspace/CICAN/src/formularios/menu.py
badd +93 ginn/formularios/launcher.py
badd +625 ginn/formularios/empleados.py
badd +38 ginn/formularios/resultados_geotextiles.py
badd +760 ginn/formularios/menu.py
badd +142 ginn/formularios/autenticacion.py
badd +1148 ginn/informes/geninformes.py
badd +233 ginn/informes/informe_certificado_calidad.py
badd +1518 informes/geninformes.py
badd +2349 ginn/formularios/facturas_venta.py
badd +144 ginn/framework/configuracion.py
badd +4 bin/ginn.sh
badd +10 ginn/main.py
badd +1149 ginn/formularios/ventana.py
badd +2094 ginn/formularios/pedidos_de_venta.py
badd +3879 db/tablas.sql
badd +1 ginn/formularios/albaranes_de_salida.py
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
badd +21254 ginn/framework/pclases/__init__.py
badd +494 ginn/framework/pclases/superfacturaventa.py
badd +149 ginn/framework/pclases/facturaventa.py
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
badd +4 ginn/framework/__init__.py
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
badd +134 ginn/formularios/consulta_existencias_por_tipo.py
badd +82 ginn/formularios/consulta_existencias.py
badd +1 ginn/formularios/consulta_producido.glade
badd +1 ginn/formularios/consumo_balas_partida.pyç
badd +28 db/restore_snapshot.sh
badd +1 extra/scripts/clouseau.py
badd +92 ginn/informes/treeview2csv.py
badd +287 ginn/formularios/consulta_ventas_por_producto.py
badd +1 tests/stock_performance.py
badd +0 (clewn)_console
args formularios/auditviewer.py
set lines=64 columns=115
edit (clewn)_console
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd _ | wincmd |
split
1wincmd k
wincmd w
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
exe '1resize ' . ((&lines * 12 + 32) / 64)
exe 'vert 1resize ' . ((&columns * 34 + 57) / 115)
exe '2resize ' . ((&lines * 49 + 32) / 64)
exe 'vert 2resize ' . ((&columns * 34 + 57) / 115)
exe '3resize ' . ((&lines * 1 + 32) / 64)
exe 'vert 3resize ' . ((&columns * 80 + 57) / 115)
exe '4resize ' . ((&lines * 1 + 32) / 64)
exe 'vert 4resize ' . ((&columns * 80 + 57) / 115)
exe '5resize ' . ((&lines * 1 + 32) / 64)
exe 'vert 5resize ' . ((&columns * 80 + 57) / 115)
exe '6resize ' . ((&lines * 25 + 32) / 64)
exe 'vert 6resize ' . ((&columns * 80 + 57) / 115)
exe '7resize ' . ((&lines * 1 + 32) / 64)
exe 'vert 7resize ' . ((&columns * 80 + 57) / 115)
exe '8resize ' . ((&lines * 1 + 32) / 64)
exe 'vert 8resize ' . ((&columns * 80 + 57) / 115)
exe '9resize ' . ((&lines * 1 + 32) / 64)
exe 'vert 9resize ' . ((&columns * 80 + 57) / 115)
exe '10resize ' . ((&lines * 1 + 32) / 64)
exe 'vert 10resize ' . ((&columns * 80 + 57) / 115)
exe '11resize ' . ((&lines * 1 + 32) / 64)
exe 'vert 11resize ' . ((&columns * 80 + 57) / 115)
exe '12resize ' . ((&lines * 20 + 32) / 64)
exe 'vert 12resize ' . ((&columns * 80 + 57) / 115)
argglobal
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 1 - ((0 * winheight(0) + 6) / 12)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
enew
file ~/Geotexan/src/Geotex-INN/__Tag_List__
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
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/albaranes_de_salida.py
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
2021
normal! zo
2034
normal! zo
2034
normal! zo
2034
normal! zo
2034
normal! zo
2034
normal! zo
2034
normal! zo
2034
normal! zo
2043
normal! zo
2065
normal! zo
2070
normal! zo
2070
normal! zo
2196
normal! zo
2830
normal! zo
2839
normal! zo
3062
normal! zo
3260
normal! zo
3272
normal! zo
3273
normal! zo
3274
normal! zo
4209
normal! zo
4239
normal! zo
let s:l = 4794 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
4794
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
461
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
1806
normal! zo
1847
normal! zo
1847
normal! zo
1847
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
6013
normal! zo
6026
normal! zo
6030
normal! zo
6036
normal! zo
6169
normal! zo
6295
normal! zo
6889
normal! zo
7139
normal! zo
7558
normal! zo
7587
normal! zo
7587
normal! zo
7587
normal! zo
7587
normal! zo
7587
normal! zo
7611
normal! zo
7680
normal! zo
7699
normal! zo
7702
normal! zo
7703
normal! zo
7703
normal! zo
7703
normal! zo
7716
normal! zo
7717
normal! zo
7718
normal! zo
7723
normal! zo
7729
normal! zo
7735
normal! zo
7735
normal! zo
7735
normal! zo
7735
normal! zo
7735
normal! zo
7735
normal! zo
7737
normal! zo
7776
normal! zo
7786
normal! zo
7787
normal! zo
7795
normal! zo
7796
normal! zo
7799
normal! zo
7804
normal! zo
7805
normal! zo
7806
normal! zo
7807
normal! zo
7807
normal! zo
7807
normal! zo
7807
normal! zo
7807
normal! zo
7807
normal! zo
7811
normal! zo
7817
normal! zo
7820
normal! zo
7820
normal! zo
7820
normal! zo
7820
normal! zo
7820
normal! zo
7829
normal! zo
7830
normal! zo
7831
normal! zo
7839
normal! zo
7846
normal! zo
7846
normal! zo
7846
normal! zo
7846
normal! zo
7846
normal! zo
7846
normal! zo
7848
normal! zo
7848
normal! zo
7848
normal! zo
7848
normal! zo
7848
normal! zo
7848
normal! zo
7848
normal! zo
7851
normal! zo
7851
normal! zo
7851
normal! zo
7851
normal! zo
7851
normal! zo
7851
normal! zo
7852
normal! zo
7852
normal! zo
7852
normal! zo
7852
normal! zo
7854
normal! zo
7855
normal! zo
7864
normal! zo
7871
normal! zo
7871
normal! zo
7871
normal! zo
7871
normal! zo
7871
normal! zo
7871
normal! zo
7873
normal! zo
7876
normal! zo
7876
normal! zo
7876
normal! zo
7876
normal! zo
7876
normal! zo
7876
normal! zo
7877
normal! zo
7877
normal! zo
7877
normal! zo
7877
normal! zo
7879
normal! zo
7880
normal! zo
7883
normal! zo
7888
normal! zo
7888
normal! zo
7888
normal! zo
7888
normal! zo
7888
normal! zo
7888
normal! zo
7888
normal! zo
7936
normal! zo
7941
normal! zo
7943
normal! zo
7944
normal! zo
7944
normal! zo
7944
normal! zo
7944
normal! zo
7944
normal! zo
7944
normal! zo
7947
normal! zo
7953
normal! zo
7956
normal! zo
7965
normal! zo
7967
normal! zo
7968
normal! zo
7975
normal! zo
7976
normal! zo
7977
normal! zo
7982
normal! zo
7986
normal! zo
7994
normal! zo
7995
normal! zo
7997
normal! zo
7997
normal! zo
8004
normal! zo
8005
normal! zo
8006
normal! zo
8006
normal! zo
8006
normal! zo
8006
normal! zo
8006
normal! zo
8006
normal! zo
8006
normal! zo
8006
normal! zo
8009
normal! zo
8009
normal! zo
8009
normal! zo
8016
normal! zo
8018
normal! zo
8301
normal! zo
8312
normal! zo
8313
normal! zo
8313
normal! zo
8313
normal! zo
8313
normal! zo
8313
normal! zo
8313
normal! zo
8313
normal! zo
8316
normal! zo
8316
normal! zo
8316
normal! zo
8316
normal! zo
8316
normal! zo
8316
normal! zo
8316
normal! zo
8320
normal! zo
8327
normal! zo
8327
normal! zo
8327
normal! zo
8327
normal! zo
8327
normal! zo
8327
normal! zo
8327
normal! zo
8327
normal! zo
8330
normal! zo
8330
normal! zo
8330
normal! zo
8330
normal! zo
8330
normal! zo
8330
normal! zo
8330
normal! zo
8330
normal! zo
8765
normal! zo
8769
normal! zo
8800
normal! zo
8849
normal! zo
8856
normal! zo
9024
normal! zo
9035
normal! zo
9048
normal! zo
9049
normal! zo
9062
normal! zo
9067
normal! zo
9072
normal! zo
9077
normal! zo
9088
normal! zo
9111
normal! zo
9134
normal! zo
9135
normal! zo
9135
normal! zo
9135
normal! zo
9135
normal! zo
9135
normal! zo
9135
normal! zo
9146
normal! zo
9161
normal! zo
9196
normal! zo
9284
normal! zo
9315
normal! zo
9322
normal! zo
9326
normal! zo
9331
normal! zo
9346
normal! zo
9394
normal! zo
9435
normal! zo
9697
normal! zo
9723
normal! zo
9762
normal! zo
9773
normal! zo
9774
normal! zo
9787
normal! zo
9799
normal! zo
9813
normal! zo
9829
normal! zo
9846
normal! zo
9846
normal! zo
9846
normal! zo
9846
normal! zo
9846
normal! zo
9846
normal! zo
9846
normal! zo
9846
normal! zo
9846
normal! zo
9853
normal! zo
9867
normal! zo
9868
normal! zo
9868
normal! zo
9870
normal! zo
9871
normal! zo
9871
normal! zo
9873
normal! zo
9874
normal! zo
9874
normal! zo
9876
normal! zo
9877
normal! zo
9877
normal! zo
9879
normal! zo
9882
normal! zo
9884
normal! zo
9884
normal! zo
9884
normal! zo
9893
normal! zo
9906
normal! zo
9909
normal! zo
9910
normal! zo
9910
normal! zo
9913
normal! zo
9913
normal! zo
9913
normal! zo
9916
normal! zo
9916
normal! zo
9916
normal! zo
9916
normal! zo
9922
normal! zo
9925
normal! zo
9929
normal! zo
9936
normal! zo
9938
normal! zo
9985
normal! zo
9999
normal! zo
10000
normal! zo
10002
normal! zo
10037
normal! zo
10044
normal! zo
10049
normal! zo
10050
normal! zo
10055
normal! zo
10055
normal! zo
10055
normal! zo
10055
normal! zo
10055
normal! zo
10058
normal! zo
10058
normal! zo
10058
normal! zo
10084
normal! zo
10093
normal! zo
10098
normal! zo
10100
normal! zo
10105
normal! zo
10111
normal! zo
10119
normal! zo
10120
normal! zo
10120
normal! zo
10120
normal! zo
10120
normal! zo
10129
normal! zo
10130
normal! zo
10135
normal! zo
10184
normal! zo
10189
normal! zo
10302
normal! zo
10329
normal! zo
10334
normal! zo
10340
normal! zo
10426
normal! zo
10433
normal! zo
10434
normal! zo
10482
normal! zo
10482
normal! zo
10482
normal! zo
10482
normal! zo
10482
normal! zo
10485
normal! zo
10493
normal! zo
10494
normal! zo
10539
normal! zo
10559
normal! zo
10560
normal! zo
10561
normal! zo
10561
normal! zo
10561
normal! zo
10561
normal! zo
10561
normal! zo
10561
normal! zo
10561
normal! zo
10561
normal! zo
10561
normal! zo
10578
normal! zo
10584
normal! zo
10594
normal! zo
10609
normal! zo
10612
normal! zo
10615
normal! zo
10615
normal! zo
10615
normal! zo
10618
normal! zo
10618
normal! zo
10618
normal! zo
10618
normal! zo
10623
normal! zo
10623
normal! zo
10623
normal! zo
10631
normal! zo
10638
normal! zo
10645
normal! zo
10648
normal! zo
10650
normal! zo
10653
normal! zo
10656
normal! zo
10661
normal! zo
10672
normal! zo
10679
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
10690
normal! zo
10690
normal! zo
10692
normal! zo
10693
normal! zo
10693
normal! zo
10695
normal! zo
10696
normal! zo
10696
normal! zo
10698
normal! zo
10699
normal! zo
10699
normal! zo
10701
normal! zo
10702
normal! zo
10702
normal! zo
10704
normal! zo
10707
normal! zo
10709
normal! zo
10709
normal! zo
10709
normal! zo
10715
normal! zo
10716
normal! zo
10716
normal! zo
10718
normal! zo
10719
normal! zo
10719
normal! zo
10743
normal! zo
10747
normal! zo
10750
normal! zo
10751
normal! zo
10751
normal! zo
10751
normal! zo
10751
normal! zo
10751
normal! zo
10751
normal! zo
10756
normal! zo
10757
normal! zo
10757
normal! zo
10757
normal! zo
10760
normal! zo
10872
normal! zo
10948
normal! zo
10956
normal! zo
10963
normal! zo
10963
normal! zo
10963
normal! zo
10963
normal! zo
10963
normal! zo
10963
normal! zo
10963
normal! zo
10974
normal! zo
10978
normal! zo
10979
normal! zo
10979
normal! zo
10979
normal! zo
10989
normal! zo
10992
normal! zo
10999
normal! zo
11008
normal! zo
11017
normal! zo
11127
normal! zo
11128
normal! zc
11141
normal! zo
11141
normal! zo
11141
normal! zo
11141
normal! zo
11150
normal! zc
11153
normal! zo
11166
normal! zo
11179
normal! zo
11186
normal! zo
11188
normal! zo
11188
normal! zo
11188
normal! zo
11188
normal! zo
11188
normal! zo
11188
normal! zo
11196
normal! zc
11213
normal! zo
11241
normal! zo
11253
normal! zo
11254
normal! zo
11254
normal! zo
11254
normal! zo
11254
normal! zo
11213
normal! zc
11259
normal! zo
11259
normal! zc
11310
normal! zo
11310
normal! zc
11425
normal! zo
11433
normal! zo
11433
normal! zo
11433
normal! zo
11433
normal! zo
11425
normal! zc
11441
normal! zc
11447
normal! zo
11447
normal! zc
11458
normal! zo
11458
normal! zc
11475
normal! zo
11475
normal! zo
11479
normal! zo
11484
normal! zo
11484
normal! zo
11486
normal! zo
11487
normal! zo
11487
normal! zo
11492
normal! zo
11492
normal! zo
11492
normal! zo
11492
normal! zo
11492
normal! zo
11492
normal! zc
11505
normal! zo
11508
normal! zo
11508
normal! zo
11508
normal! zo
11508
normal! zo
11514
normal! zo
11514
normal! zo
11514
normal! zo
11514
normal! zo
11514
normal! zo
11514
normal! zc
11542
normal! zo
11580
normal! zc
11587
normal! zc
11595
normal! zo
11595
normal! zc
11603
normal! zc
11611
normal! zc
11625
normal! zo
11625
normal! zc
11643
normal! zo
11643
normal! zo
11643
normal! zo
11643
normal! zo
11643
normal! zo
11643
normal! zo
11643
normal! zo
11643
normal! zo
11643
normal! zo
11643
normal! zo
11643
normal! zc
11664
normal! zo
11664
normal! zo
11664
normal! zo
11664
normal! zo
11664
normal! zo
11664
normal! zo
11705
normal! zo
11706
normal! zo
11728
normal! zo
11728
normal! zc
11835
normal! zo
11835
normal! zc
11884
normal! zo
11884
normal! zo
11886
normal! zo
11896
normal! zo
11884
normal! zc
11979
normal! zo
11979
normal! zc
12033
normal! zo
12033
normal! zo
12033
normal! zo
12033
normal! zc
12033
normal! zc
12047
normal! zo
12084
normal! zo
12095
normal! zo
12100
normal! zo
12118
normal! zo
12118
normal! zo
12118
normal! zo
12118
normal! zo
12119
normal! zo
12124
normal! zo
12140
normal! zo
12140
normal! zo
12140
normal! zo
12140
normal! zo
12149
normal! zo
12149
normal! zo
12149
normal! zo
12149
normal! zo
12149
normal! zo
12173
normal! zo
12197
normal! zo
12197
normal! zc
12238
normal! zo
12238
normal! zo
12238
normal! zo
12238
normal! zo
12300
normal! zo
12316
normal! zo
12316
normal! zc
12340
normal! zo
12340
normal! zo
12340
normal! zo
12340
normal! zc
12365
normal! zo
12365
normal! zo
12365
normal! zo
12365
normal! zc
12440
normal! zo
12440
normal! zo
12440
normal! zo
12440
normal! zo
12440
normal! zo
12440
normal! zo
12440
normal! zo
12440
normal! zo
12440
normal! zc
12456
normal! zo
12456
normal! zc
12478
normal! zo
12478
normal! zc
12499
normal! zo
12499
normal! zo
12499
normal! zo
12499
normal! zo
12499
normal! zo
12499
normal! zo
12499
normal! zo
12499
normal! zc
12499
normal! zc
12619
normal! zo
12619
normal! zo
12619
normal! zo
12619
normal! zo
12619
normal! zo
12619
normal! zc
12887
normal! zo
12887
normal! zc
12917
normal! zo
12917
normal! zo
12917
normal! zo
12917
normal! zo
12917
normal! zo
12917
normal! zo
12917
normal! zo
12917
normal! zo
12932
normal! zo
12947
normal! zo
12949
normal! zo
12971
normal! zo
12979
normal! zo
12979
normal! zc
12995
normal! zo
12995
normal! zo
13034
normal! zo
13096
normal! zo
13097
normal! zo
13115
normal! zo
13157
normal! zo
13158
normal! zo
13186
normal! zo
13218
normal! zo
13219
normal! zo
13247
normal! zo
13283
normal! zo
13284
normal! zo
13302
normal! zo
13329
normal! zc
13339
normal! zo
13339
normal! zc
13359
normal! zo
13360
normal! zo
13361
normal! zo
13359
normal! zc
13415
normal! zo
13415
normal! zc
13473
normal! zo
13473
normal! zo
13473
normal! zo
13483
normal! zo
13488
normal! zo
13489
normal! zo
13490
normal! zo
13490
normal! zo
13490
normal! zo
13490
normal! zo
13490
normal! zo
13490
normal! zo
13490
normal! zo
13490
normal! zo
13490
normal! zo
13490
normal! zo
13496
normal! zo
13497
normal! zo
13498
normal! zo
13498
normal! zo
13498
normal! zo
13498
normal! zo
13498
normal! zo
13498
normal! zo
13498
normal! zo
13500
normal! zo
13500
normal! zo
13500
normal! zo
13500
normal! zo
13500
normal! zo
13500
normal! zo
13500
normal! zo
13500
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
13503
normal! zo
13503
normal! zo
13503
normal! zo
13506
normal! zo
13508
normal! zo
13508
normal! zo
13513
normal! zo
13513
normal! zo
13523
normal! zo
13524
normal! zo
13524
normal! zo
13524
normal! zo
13524
normal! zo
13524
normal! zo
13524
normal! zo
13531
normal! zo
13531
normal! zo
13531
normal! zo
13537
normal! zo
13538
normal! zo
13547
normal! zo
13548
normal! zo
13548
normal! zo
13548
normal! zo
13548
normal! zo
13552
normal! zo
13552
normal! zo
13552
normal! zo
13560
normal! zo
13561
normal! zo
13563
normal! zo
13571
normal! zo
13572
normal! zo
13572
normal! zo
13572
normal! zo
13572
normal! zo
13576
normal! zo
13576
normal! zo
13576
normal! zo
13583
normal! zo
13583
normal! zo
13583
normal! zo
13583
normal! zo
13583
normal! zo
13586
normal! zo
13587
normal! zo
13588
normal! zo
13589
normal! zo
13589
normal! zo
13590
normal! zo
13602
normal! zo
13603
normal! zo
13603
normal! zo
13603
normal! zo
13610
normal! zo
13611
normal! zo
13612
normal! zo
13612
normal! zo
13613
normal! zo
13624
normal! zo
13625
normal! zo
13626
normal! zo
13626
normal! zo
13627
normal! zo
13642
normal! zo
13643
normal! zo
13644
normal! zo
13645
normal! zo
13645
normal! zo
13646
normal! zo
13658
normal! zo
13659
normal! zo
13659
normal! zo
13659
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
13669
normal! zo
13680
normal! zo
13681
normal! zo
13682
normal! zo
13682
normal! zo
13683
normal! zo
13698
normal! zo
13698
normal! zo
13698
normal! zo
13719
normal! zo
13724
normal! zo
13725
normal! zo
13726
normal! zo
13726
normal! zo
13726
normal! zo
13726
normal! zo
13726
normal! zo
13726
normal! zo
13726
normal! zo
13726
normal! zo
13726
normal! zo
13726
normal! zo
13732
normal! zo
13733
normal! zo
13734
normal! zo
13734
normal! zo
13734
normal! zo
13734
normal! zo
13734
normal! zo
13734
normal! zo
13734
normal! zo
13736
normal! zo
13736
normal! zo
13736
normal! zo
13736
normal! zo
13736
normal! zo
13736
normal! zo
13736
normal! zo
13736
normal! zo
13738
normal! zo
13739
normal! zo
13739
normal! zo
13739
normal! zo
13739
normal! zo
13739
normal! zo
13739
normal! zo
13739
normal! zo
13739
normal! zo
13739
normal! zo
13742
normal! zo
13744
normal! zo
13749
normal! zo
13758
normal! zo
13759
normal! zo
13759
normal! zo
13759
normal! zo
13759
normal! zo
13759
normal! zo
13759
normal! zo
13759
normal! zo
13766
normal! zo
13768
normal! zo
13769
normal! zo
13770
normal! zo
13770
normal! zo
13771
normal! zo
13781
normal! zo
13782
normal! zo
13783
normal! zo
13783
normal! zo
13784
normal! zo
13798
normal! zo
13799
normal! zo
13800
normal! zo
13801
normal! zo
13801
normal! zo
13802
normal! zo
13812
normal! zo
13813
normal! zo
13814
normal! zo
13814
normal! zo
13815
normal! zo
13829
normal! zo
13829
normal! zo
13829
normal! zo
13840
normal! zo
13845
normal! zo
13846
normal! zo
13847
normal! zo
13847
normal! zo
13847
normal! zo
13847
normal! zo
13847
normal! zo
13847
normal! zo
13847
normal! zo
13847
normal! zo
13847
normal! zo
13847
normal! zo
13853
normal! zo
13854
normal! zo
13855
normal! zo
13855
normal! zo
13855
normal! zo
13855
normal! zo
13855
normal! zo
13855
normal! zo
13855
normal! zo
13857
normal! zo
13857
normal! zo
13857
normal! zo
13857
normal! zo
13857
normal! zo
13857
normal! zo
13857
normal! zo
13857
normal! zo
13859
normal! zo
13860
normal! zo
13860
normal! zo
13860
normal! zo
13860
normal! zo
13860
normal! zo
13860
normal! zo
13860
normal! zo
13860
normal! zo
13860
normal! zo
13863
normal! zo
13865
normal! zo
13870
normal! zo
13879
normal! zo
13880
normal! zo
13880
normal! zo
13880
normal! zo
13880
normal! zo
13880
normal! zo
13880
normal! zo
13880
normal! zo
13887
normal! zo
13892
normal! zo
13893
normal! zo
13894
normal! zo
13901
normal! zo
13902
normal! zo
13903
normal! zo
13909
normal! zo
13910
normal! zo
13911
normal! zo
13916
normal! zo
13917
normal! zo
13918
normal! zo
13918
normal! zo
13928
normal! zo
13929
normal! zo
13930
normal! zo
13930
normal! zo
13930
normal! zo
13930
normal! zo
13930
normal! zo
13930
normal! zo
13937
normal! zo
13938
normal! zo
13938
normal! zo
13938
normal! zo
13938
normal! zo
13938
normal! zo
13938
normal! zo
13938
normal! zo
13945
normal! zo
13946
normal! zo
13946
normal! zo
13946
normal! zo
13946
normal! zo
13946
normal! zo
13946
normal! zo
13946
normal! zo
13952
normal! zo
13953
normal! zo
13953
normal! zo
13953
normal! zo
13953
normal! zo
13953
normal! zo
13953
normal! zo
13953
normal! zo
13963
normal! zo
13969
normal! zo
13969
normal! zo
13975
normal! zo
13981
normal! zo
13987
normal! zo
13987
normal! zo
13987
normal! zo
13987
normal! zo
13987
normal! zo
13987
normal! zo
13987
normal! zo
13987
normal! zo
13987
normal! zo
13997
normal! zo
13997
normal! zo
13997
normal! zo
13997
normal! zo
13997
normal! zo
13997
normal! zo
13999
normal! zo
14000
normal! zo
14000
normal! zo
14000
normal! zo
14006
normal! zo
14006
normal! zo
14006
normal! zo
14006
normal! zo
14006
normal! zo
14006
normal! zo
14006
normal! zo
14006
normal! zo
14006
normal! zo
14017
normal! zo
14017
normal! zo
14017
normal! zo
14017
normal! zo
14017
normal! zo
14017
normal! zo
14019
normal! zo
14020
normal! zo
14020
normal! zo
14020
normal! zo
14026
normal! zo
14026
normal! zo
14026
normal! zo
14026
normal! zo
14034
normal! zo
14039
normal! zo
14042
normal! zo
14047
normal! zo
14048
normal! zo
14049
normal! zo
14049
normal! zo
14049
normal! zo
14049
normal! zo
14049
normal! zo
14049
normal! zo
14049
normal! zo
14049
normal! zo
14049
normal! zo
14049
normal! zo
14055
normal! zo
14056
normal! zo
14059
normal! zo
14060
normal! zo
14060
normal! zo
14060
normal! zo
14060
normal! zo
14060
normal! zo
14060
normal! zo
14060
normal! zo
14062
normal! zo
14062
normal! zo
14062
normal! zo
14062
normal! zo
14062
normal! zo
14062
normal! zo
14062
normal! zo
14062
normal! zo
14062
normal! zo
14064
normal! zo
14065
normal! zo
14068
normal! zo
14068
normal! zo
14068
normal! zo
14068
normal! zo
14068
normal! zo
14068
normal! zo
14068
normal! zo
14068
normal! zo
14068
normal! zo
14071
normal! zo
14072
normal! zo
14076
normal! zo
14076
normal! zo
14081
normal! zo
14081
normal! zo
14086
normal! zo
14087
normal! zo
14094
normal! zo
14095
normal! zo
14098
normal! zo
14098
normal! zo
14098
normal! zo
14098
normal! zo
14098
normal! zo
14098
normal! zo
14105
normal! zo
14106
normal! zo
14107
normal! zo
14108
normal! zo
14114
normal! zo
14115
normal! zo
14116
normal! zo
14122
normal! zo
14123
normal! zo
14123
normal! zo
14124
normal! zo
14129
normal! zo
14130
normal! zo
14130
normal! zo
14131
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
14149
normal! zo
14150
normal! zo
14151
normal! zo
14157
normal! zo
14158
normal! zo
14158
normal! zo
14158
normal! zo
14158
normal! zo
14158
normal! zo
14158
normal! zo
14158
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
14176
normal! zo
14177
normal! zo
14177
normal! zo
14183
normal! zo
14189
normal! zo
14189
normal! zo
14195
normal! zo
14195
normal! zo
14195
normal! zo
14195
normal! zo
14211
normal! zo
14216
normal! zo
14217
normal! zo
14218
normal! zo
14218
normal! zo
14218
normal! zo
14218
normal! zo
14218
normal! zo
14218
normal! zo
14218
normal! zo
14218
normal! zo
14218
normal! zo
14218
normal! zo
14224
normal! zo
14225
normal! zo
14226
normal! zo
14226
normal! zo
14226
normal! zo
14226
normal! zo
14226
normal! zo
14226
normal! zo
14226
normal! zo
14228
normal! zo
14228
normal! zo
14228
normal! zo
14228
normal! zo
14228
normal! zo
14228
normal! zo
14228
normal! zo
14228
normal! zo
14228
normal! zo
14230
normal! zo
14231
normal! zo
14231
normal! zo
14231
normal! zo
14231
normal! zo
14231
normal! zo
14231
normal! zo
14231
normal! zo
14231
normal! zo
14231
normal! zo
14234
normal! zo
14236
normal! zo
14236
normal! zo
14241
normal! zo
14241
normal! zo
14251
normal! zo
14252
normal! zo
14252
normal! zo
14252
normal! zo
14252
normal! zo
14252
normal! zo
14252
normal! zo
14259
normal! zo
14260
normal! zo
14261
normal! zo
14262
normal! zo
14267
normal! zo
14268
normal! zo
14269
normal! zo
14279
normal! zo
14280
normal! zo
14281
normal! zo
14281
normal! zo
14281
normal! zo
14281
normal! zo
14281
normal! zo
14281
normal! zo
14286
normal! zo
14287
normal! zo
14287
normal! zo
14287
normal! zo
14288
normal! zo
14298
normal! zo
14299
normal! zo
14299
normal! zo
14305
normal! zo
14306
normal! zo
14306
normal! zo
14312
normal! zo
14312
normal! zo
14312
normal! zo
14312
normal! zo
14324
normal! zo
14329
normal! zo
14330
normal! zo
14331
normal! zo
14331
normal! zo
14331
normal! zo
14331
normal! zo
14331
normal! zo
14331
normal! zo
14331
normal! zo
14331
normal! zo
14331
normal! zo
14331
normal! zo
14337
normal! zo
14338
normal! zo
14339
normal! zo
14339
normal! zo
14339
normal! zo
14339
normal! zo
14339
normal! zo
14339
normal! zo
14339
normal! zo
14341
normal! zo
14341
normal! zo
14341
normal! zo
14341
normal! zo
14341
normal! zo
14341
normal! zo
14341
normal! zo
14341
normal! zo
14341
normal! zo
14343
normal! zo
14344
normal! zo
14344
normal! zo
14344
normal! zo
14344
normal! zo
14344
normal! zo
14344
normal! zo
14344
normal! zo
14344
normal! zo
14344
normal! zo
14347
normal! zo
14349
normal! zo
14349
normal! zo
14354
normal! zo
14354
normal! zo
14364
normal! zo
14365
normal! zo
14365
normal! zo
14365
normal! zo
14365
normal! zo
14365
normal! zo
14365
normal! zo
14372
normal! zo
14379
normal! zo
14380
normal! zo
14382
normal! zo
14382
normal! zo
14382
normal! zo
14388
normal! zo
14390
normal! zo
14392
normal! zo
14398
normal! zo
14400
normal! zo
14402
normal! zo
14413
normal! zo
14433
normal! zo
14445
normal! zo
14448
normal! zo
14449
normal! zo
14450
normal! zo
14450
normal! zo
14450
normal! zo
14452
normal! zo
14453
normal! zo
14453
normal! zo
14453
normal! zo
14469
normal! zo
14480
normal! zo
14489
normal! zo
14499
normal! zo
14526
normal! zo
14531
normal! zo
14537
normal! zo
14548
normal! zo
14561
normal! zo
14585
normal! zo
14587
normal! zo
14590
normal! zo
14593
normal! zo
14594
normal! zo
14598
normal! zo
14599
normal! zo
14613
normal! zo
14613
normal! zo
14613
normal! zo
14613
normal! zo
14635
normal! zo
14636
normal! zo
14637
normal! zo
14637
normal! zo
14637
normal! zo
14637
normal! zo
14637
normal! zo
14637
normal! zo
14637
normal! zo
14637
normal! zo
14637
normal! zo
14637
normal! zo
14646
normal! zo
14647
normal! zo
14653
normal! zo
14657
normal! zo
14658
normal! zo
14667
normal! zo
14668
normal! zo
14676
normal! zo
14677
normal! zo
14683
normal! zo
14698
normal! zo
14706
normal! zo
14712
normal! zo
14718
normal! zo
14723
normal! zo
14727
normal! zo
14733
normal! zo
14738
normal! zo
14739
normal! zo
14744
normal! zo
14755
normal! zo
14773
normal! zo
14815
normal! zo
14821
normal! zo
14827
normal! zo
14834
normal! zo
14843
normal! zo
14845
normal! zo
14852
normal! zo
14852
normal! zo
14852
normal! zo
14852
normal! zo
14852
normal! zo
14852
normal! zo
14869
normal! zo
14881
normal! zo
14892
normal! zo
14893
normal! zo
14909
normal! zo
14926
normal! zo
14930
normal! zo
14931
normal! zo
14932
normal! zo
14932
normal! zo
14934
normal! zo
14937
normal! zo
14950
normal! zo
14960
normal! zo
14962
normal! zo
14966
normal! zo
14967
normal! zo
14967
normal! zo
14967
normal! zo
14967
normal! zo
14967
normal! zo
14967
normal! zo
14980
normal! zo
15001
normal! zo
15002
normal! zo
15009
normal! zo
15042
normal! zo
15043
normal! zo
15043
normal! zo
15059
normal! zo
15065
normal! zo
15068
normal! zo
15068
normal! zo
15068
normal! zo
15074
normal! zo
15074
normal! zo
15094
normal! zo
15099
normal! zo
15104
normal! zo
15112
normal! zo
15131
normal! zo
15165
normal! zo
15173
normal! zo
15182
normal! zo
15201
normal! zo
15203
normal! zo
15207
normal! zo
15224
normal! zo
15230
normal! zo
15234
normal! zo
15273
normal! zo
15377
normal! zo
15377
normal! zo
15453
normal! zo
15453
normal! zo
15453
normal! zo
15566
normal! zo
15597
normal! zo
15621
normal! zo
15631
normal! zo
15631
normal! zo
15631
normal! zo
15631
normal! zo
15631
normal! zo
15819
normal! zo
15838
normal! zo
15860
normal! zo
15865
normal! zo
15866
normal! zo
15866
normal! zo
15869
normal! zo
15870
normal! zo
15870
normal! zo
15870
normal! zo
15873
normal! zo
15873
normal! zo
15873
normal! zo
15877
normal! zo
15877
normal! zo
15877
normal! zo
15877
normal! zo
15877
normal! zo
15877
normal! zo
15877
normal! zo
15877
normal! zo
15877
normal! zo
16408
normal! zo
16444
normal! zo
16459
normal! zo
16465
normal! zo
16468
normal! zo
16476
normal! zo
16477
normal! zo
16477
normal! zo
16477
normal! zo
16477
normal! zo
16477
normal! zo
16481
normal! zo
16489
normal! zo
16492
normal! zo
16498
normal! zo
16504
normal! zo
16507
normal! zo
16513
normal! zo
16527
normal! zo
16533
normal! zo
16538
normal! zo
16541
normal! zo
16541
normal! zo
16541
normal! zo
16551
normal! zo
16566
normal! zo
16577
normal! zo
16577
normal! zo
16588
normal! zo
16603
normal! zo
16613
normal! zo
16624
normal! zo
16633
normal! zo
16640
normal! zo
16678
normal! zo
16683
normal! zo
16683
normal! zo
16683
normal! zo
16696
normal! zo
16696
normal! zo
16696
normal! zo
16696
normal! zo
16696
normal! zo
16696
normal! zo
16696
normal! zo
16696
normal! zo
16696
normal! zo
16696
normal! zo
16696
normal! zo
16708
normal! zo
16729
normal! zo
16748
normal! zo
16756
normal! zo
16757
normal! zo
16758
normal! zo
16762
normal! zo
16766
normal! zo
16782
normal! zo
16797
normal! zo
16802
normal! zo
16807
normal! zo
16817
normal! zo
16818
normal! zo
16818
normal! zo
16818
normal! zo
16820
normal! zo
16820
normal! zo
16820
normal! zo
16820
normal! zo
16820
normal! zo
16820
normal! zo
16820
normal! zo
16820
normal! zo
16820
normal! zo
16820
normal! zo
16825
normal! zo
16826
normal! zo
16832
normal! zo
16833
normal! zo
16853
normal! zo
16878
normal! zo
16882
normal! zo
16899
normal! zo
16910
normal! zo
16910
normal! zo
16910
normal! zo
16910
normal! zo
16912
normal! zo
16913
normal! zo
16914
normal! zo
16915
normal! zo
16916
normal! zo
16920
normal! zo
16921
normal! zo
16922
normal! zo
16922
normal! zo
16922
normal! zo
16922
normal! zo
16922
normal! zo
16922
normal! zo
16922
normal! zo
16924
normal! zo
16926
normal! zo
16931
normal! zo
16931
normal! zo
16931
normal! zo
16931
normal! zo
16937
normal! zo
16941
normal! zo
16949
normal! zo
16949
normal! zo
16949
normal! zo
16949
normal! zo
16957
normal! zo
16965
normal! zo
16966
normal! zo
16969
normal! zo
16974
normal! zo
16982
normal! zo
16987
normal! zo
16995
normal! zo
17000
normal! zo
17009
normal! zo
17010
normal! zo
17010
normal! zo
17020
normal! zo
17035
normal! zo
17036
normal! zo
17052
normal! zo
17072
normal! zo
17073
normal! zo
17073
normal! zo
17073
normal! zo
17073
normal! zo
17073
normal! zo
17079
normal! zo
17089
normal! zo
17103
normal! zo
17106
normal! zo
17110
normal! zo
17111
normal! zo
17112
normal! zo
17112
normal! zo
17112
normal! zo
17112
normal! zo
17112
normal! zo
17130
normal! zo
17137
normal! zo
17138
normal! zo
17145
normal! zo
17152
normal! zo
17153
normal! zo
17154
normal! zo
17159
normal! zo
17166
normal! zo
17171
normal! zo
17184
normal! zo
17185
normal! zo
17185
normal! zo
17185
normal! zo
17190
normal! zo
17203
normal! zo
17210
normal! zo
17211
normal! zo
17226
normal! zo
17233
normal! zo
17247
normal! zo
17254
normal! zo
17255
normal! zo
17260
normal! zo
17269
normal! zo
17283
normal! zo
17305
normal! zo
17326
normal! zo
17339
normal! zo
17339
normal! zo
17339
normal! zo
17339
normal! zo
17339
normal! zo
17339
normal! zo
17349
normal! zo
17362
normal! zo
17386
normal! zo
17391
normal! zo
17393
normal! zo
17396
normal! zo
17403
normal! zo
17415
normal! zo
17425
normal! zo
17425
normal! zo
17425
normal! zo
17425
normal! zo
17425
normal! zo
17425
normal! zo
17433
normal! zo
17443
normal! zo
17443
normal! zo
17443
normal! zo
17443
normal! zo
17443
normal! zo
17443
normal! zo
17451
normal! zo
17452
normal! zo
17463
normal! zo
17468
normal! zo
17479
normal! zo
17487
normal! zo
17500
normal! zo
17504
normal! zo
17504
normal! zo
17504
normal! zo
17504
normal! zo
17504
normal! zo
17506
normal! zo
17518
normal! zo
17518
normal! zo
17518
normal! zo
17518
normal! zo
17518
normal! zo
17518
normal! zo
17518
normal! zo
17522
normal! zo
17522
normal! zo
17522
normal! zo
17522
normal! zo
17522
normal! zo
17522
normal! zo
17528
normal! zo
17528
normal! zo
17528
normal! zo
17528
normal! zo
17531
normal! zo
17532
normal! zo
17533
normal! zo
17539
normal! zo
17540
normal! zo
17540
normal! zo
17540
normal! zo
17662
normal! zo
17717
normal! zo
17750
normal! zo
17807
normal! zo
17822
normal! zo
17829
normal! zo
17830
normal! zo
17846
normal! zo
17856
normal! zo
17870
normal! zo
17873
normal! zo
17874
normal! zo
17874
normal! zo
17896
normal! zo
17916
normal! zo
17928
normal! zo
17928
normal! zo
17928
normal! zo
17928
normal! zo
17928
normal! zo
17931
normal! zo
17938
normal! zo
17941
normal! zo
17952
normal! zo
17958
normal! zo
17963
normal! zo
17969
normal! zo
17970
normal! zo
17971
normal! zo
17974
normal! zo
17993
normal! zo
18008
normal! zo
18036
normal! zo
18061
normal! zo
18082
normal! zo
18117
normal! zo
18126
normal! zo
18127
normal! zo
18128
normal! zo
18130
normal! zo
18130
normal! zo
18130
normal! zo
18133
normal! zo
18135
normal! zo
18135
normal! zo
18135
normal! zo
18138
normal! zo
18139
normal! zo
18139
normal! zo
18139
normal! zo
18139
normal! zo
18139
normal! zo
18665
normal! zo
18682
normal! zo
18692
normal! zo
18695
normal! zo
18696
normal! zo
18696
normal! zo
18702
normal! zo
18709
normal! zo
18710
normal! zo
18711
normal! zo
18711
normal! zo
18711
normal! zo
18711
normal! zo
18715
normal! zo
18716
normal! zo
18716
normal! zo
18716
normal! zo
18716
normal! zo
18732
normal! zo
19033
normal! zo
19950
normal! zo
19974
normal! zo
19980
normal! zo
19986
normal! zo
20004
normal! zo
20014
normal! zo
20017
normal! zo
20024
normal! zo
20024
normal! zo
20024
normal! zo
20024
normal! zo
20029
normal! zo
20309
normal! zo
20315
normal! zo
20315
normal! zo
20324
normal! zo
20331
normal! zo
20338
normal! zo
20345
normal! zo
20352
normal! zo
20359
normal! zo
20366
normal! zo
20372
normal! zo
20373
normal! zo
20382
normal! zo
20391
normal! zo
20554
normal! zo
20564
normal! zo
20575
normal! zo
20586
normal! zo
20587
normal! zo
20592
normal! zo
20593
normal! zo
20593
normal! zo
20603
normal! zo
20603
normal! zo
20603
normal! zo
20603
normal! zo
20603
normal! zo
20603
normal! zo
20603
normal! zo
20603
normal! zo
20603
normal! zo
20614
normal! zo
20615
normal! zo
20623
normal! zo
20623
normal! zo
20623
normal! zo
20623
normal! zo
20623
normal! zo
20623
normal! zo
20623
normal! zo
20623
normal! zo
20634
normal! zo
20635
normal! zo
20643
normal! zo
20658
normal! zo
20691
normal! zo
20712
normal! zo
20717
normal! zo
20729
normal! zo
20729
normal! zo
20729
normal! zo
20729
normal! zo
20729
normal! zo
20729
normal! zo
20729
normal! zo
20747
normal! zo
20754
normal! zo
21244
normal! zo
let s:l = 7164 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
7164
normal! 027|
lcd ~/Geotexan/src/Geotex-INN
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
131
normal! zo
132
normal! zo
132
normal! zo
165
normal! zo
173
normal! zo
174
normal! zo
174
normal! zo
174
normal! zo
174
normal! zo
174
normal! zo
174
normal! zo
181
normal! zo
196
normal! zo
239
normal! zo
255
normal! zo
263
normal! zo
321
normal! zo
330
normal! zo
331
normal! zo
333
normal! zo
334
normal! zo
334
normal! zo
334
normal! zo
334
normal! zo
337
normal! zo
let s:l = 331 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
331
normal! 035|
lcd ~/Geotexan/src/Geotex-INN
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
48
normal! zo
56
normal! zo
56
normal! zo
63
normal! zo
139
normal! zo
161
normal! zo
176
normal! zo
177
normal! zo
177
normal! zo
177
normal! zo
177
normal! zo
177
normal! zo
187
normal! zo
191
normal! zo
207
normal! zo
207
normal! zo
207
normal! zo
207
normal! zo
207
normal! zo
207
normal! zo
219
normal! zo
220
normal! zo
220
normal! zo
220
normal! zo
220
normal! zo
220
normal! zo
230
normal! zo
236
normal! zo
237
normal! zo
237
normal! zo
237
normal! zo
237
normal! zo
259
normal! zo
274
normal! zo
303
normal! zo
308
normal! zo
341
normal! zo
347
normal! zo
347
normal! zo
347
normal! zo
347
normal! zo
347
normal! zo
349
normal! zo
349
normal! zo
349
normal! zo
349
normal! zo
349
normal! zo
350
normal! zo
383
normal! zo
400
normal! zo
406
normal! zo
411
normal! zo
424
normal! zo
430
normal! zo
let s:l = 282 - ((12 * winheight(0) + 12) / 25)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
282
normal! 019|
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
66
normal! zo
74
normal! zo
84
normal! zo
88
normal! zo
107
normal! zo
112
normal! zo
149
normal! zo
158
normal! zo
171
normal! zo
180
normal! zo
190
normal! zo
226
normal! zo
236
normal! zo
240
normal! zo
249
normal! zo
259
normal! zo
274
normal! zo
274
normal! zo
283
normal! zo
283
normal! zo
292
normal! zo
292
normal! zo
292
normal! zo
292
normal! zo
292
normal! zo
292
normal! zo
309
normal! zo
310
normal! zo
let s:l = 110 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
110
normal! 034|
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
227
normal! zo
227
normal! zo
227
normal! zo
227
normal! zo
227
normal! zo
227
normal! zo
227
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
3414
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
3701
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
3777
normal! zo
3777
normal! zo
3777
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
let s:l = 235 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
235
normal! 034|
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
55
normal! zo
63
normal! zo
63
normal! zo
274
normal! zo
let s:l = 254 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
254
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
let s:l = 1137 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1137
normal! 043|
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/consulta_producido.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
58
normal! zo
59
normal! zo
84
normal! zo
84
normal! zo
84
normal! zo
84
normal! zo
84
normal! zo
84
normal! zo
84
normal! zo
84
normal! zo
84
normal! zo
95
normal! zo
95
normal! zo
95
normal! zo
95
normal! zo
95
normal! zo
95
normal! zo
95
normal! zo
106
normal! zo
110
normal! zo
115
normal! zo
132
normal! zo
145
normal! zo
170
normal! zo
205
normal! zo
218
normal! zo
227
normal! zo
248
normal! zo
261
normal! zo
269
normal! zo
269
normal! zo
269
normal! zo
269
normal! zo
276
normal! zo
276
normal! zo
276
normal! zo
276
normal! zo
280
normal! zo
281
normal! zo
281
normal! zo
304
normal! zo
305
normal! zo
305
normal! zo
329
normal! zo
330
normal! zo
335
normal! zo
344
normal! zo
345
normal! zo
345
normal! zo
345
normal! zo
347
normal! zo
348
normal! zo
348
normal! zo
348
normal! zo
348
normal! zo
348
normal! zo
348
normal! zo
364
normal! zo
367
normal! zo
367
normal! zo
367
normal! zo
367
normal! zo
367
normal! zo
367
normal! zo
367
normal! zo
367
normal! zo
367
normal! zo
367
normal! zo
367
normal! zo
367
normal! zo
369
normal! zo
373
normal! zo
381
normal! zo
382
normal! zo
382
normal! zo
383
normal! zo
387
normal! zo
389
normal! zo
391
normal! zo
395
normal! zo
400
normal! zo
401
normal! zo
401
normal! zo
401
normal! zo
401
normal! zo
405
normal! zo
411
normal! zo
411
normal! zo
411
normal! zo
411
normal! zo
414
normal! zo
419
normal! zo
420
normal! zo
420
normal! zo
420
normal! zo
420
normal! zo
424
normal! zo
429
normal! zo
429
normal! zo
429
normal! zo
429
normal! zo
432
normal! zo
433
normal! zo
450
normal! zo
450
normal! zo
450
normal! zo
450
normal! zo
452
normal! zo
452
normal! zo
452
normal! zo
452
normal! zo
457
normal! zo
458
normal! zo
458
normal! zo
458
normal! zo
458
normal! zo
460
normal! zo
460
normal! zo
460
normal! zo
460
normal! zo
465
normal! zo
470
normal! zo
470
normal! zo
470
normal! zo
470
normal! zo
472
normal! zo
472
normal! zo
472
normal! zo
472
normal! zo
476
normal! zo
477
normal! zo
480
normal! zo
493
normal! zo
493
normal! zo
493
normal! zo
493
normal! zo
495
normal! zo
495
normal! zo
495
normal! zo
495
normal! zo
500
normal! zo
501
normal! zo
501
normal! zo
501
normal! zo
501
normal! zo
504
normal! zo
504
normal! zo
504
normal! zo
504
normal! zo
510
normal! zo
515
normal! zo
515
normal! zo
515
normal! zo
515
normal! zo
518
normal! zo
518
normal! zo
518
normal! zo
518
normal! zo
523
normal! zo
524
normal! zo
527
normal! zo
541
normal! zo
541
normal! zo
541
normal! zo
541
normal! zo
543
normal! zo
543
normal! zo
543
normal! zo
543
normal! zo
548
normal! zo
549
normal! zo
549
normal! zo
549
normal! zo
549
normal! zo
552
normal! zo
552
normal! zo
552
normal! zo
552
normal! zo
558
normal! zo
563
normal! zo
563
normal! zo
563
normal! zo
563
normal! zo
567
normal! zo
567
normal! zo
567
normal! zo
567
normal! zo
572
normal! zo
573
normal! zo
575
normal! zo
575
normal! zo
575
normal! zo
575
normal! zo
575
normal! zo
575
normal! zo
575
normal! zo
575
normal! zo
575
normal! zo
575
normal! zo
575
normal! zo
575
normal! zo
575
normal! zo
595
normal! zo
615
normal! zo
621
normal! zo
627
normal! zo
628
normal! zo
636
normal! zo
641
normal! zo
646
normal! zo
646
normal! zo
650
normal! zo
652
normal! zo
652
normal! zo
652
normal! zo
662
normal! zo
663
normal! zo
664
normal! zo
670
normal! zo
671
normal! zo
675
normal! zo
681
normal! zo
681
normal! zo
681
normal! zo
681
normal! zo
681
normal! zo
693
normal! zo
696
normal! zo
696
normal! zo
696
normal! zo
696
normal! zo
702
normal! zo
713
normal! zo
727
normal! zo
728
normal! zo
738
normal! zo
740
normal! zo
746
normal! zo
750
normal! zo
750
normal! zo
762
normal! zo
766
normal! zo
766
normal! zo
781
normal! zo
781
normal! zo
781
normal! zo
781
normal! zo
781
normal! zo
795
normal! zo
796
normal! zo
796
normal! zo
814
normal! zo
815
normal! zo
815
normal! zo
815
normal! zo
815
normal! zo
815
normal! zo
815
normal! zo
815
normal! zo
815
normal! zo
815
normal! zo
828
normal! zo
828
normal! zo
828
normal! zo
828
normal! zo
828
normal! zo
845
normal! zo
let s:l = 131 - ((7 * winheight(0) + 10) / 20)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
131
normal! 05|
wincmd w
6wincmd w
exe '1resize ' . ((&lines * 12 + 32) / 64)
exe 'vert 1resize ' . ((&columns * 34 + 57) / 115)
exe '2resize ' . ((&lines * 49 + 32) / 64)
exe 'vert 2resize ' . ((&columns * 34 + 57) / 115)
exe '3resize ' . ((&lines * 1 + 32) / 64)
exe 'vert 3resize ' . ((&columns * 80 + 57) / 115)
exe '4resize ' . ((&lines * 1 + 32) / 64)
exe 'vert 4resize ' . ((&columns * 80 + 57) / 115)
exe '5resize ' . ((&lines * 1 + 32) / 64)
exe 'vert 5resize ' . ((&columns * 80 + 57) / 115)
exe '6resize ' . ((&lines * 25 + 32) / 64)
exe 'vert 6resize ' . ((&columns * 80 + 57) / 115)
exe '7resize ' . ((&lines * 1 + 32) / 64)
exe 'vert 7resize ' . ((&columns * 80 + 57) / 115)
exe '8resize ' . ((&lines * 1 + 32) / 64)
exe 'vert 8resize ' . ((&columns * 80 + 57) / 115)
exe '9resize ' . ((&lines * 1 + 32) / 64)
exe 'vert 9resize ' . ((&columns * 80 + 57) / 115)
exe '10resize ' . ((&lines * 1 + 32) / 64)
exe 'vert 10resize ' . ((&columns * 80 + 57) / 115)
exe '11resize ' . ((&lines * 1 + 32) / 64)
exe 'vert 11resize ' . ((&columns * 80 + 57) / 115)
exe '12resize ' . ((&lines * 20 + 32) / 64)
exe 'vert 12resize ' . ((&columns * 80 + 57) / 115)
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
