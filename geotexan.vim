" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 27 febrero 2014 at 12:15:50.
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
badd +574 ginn/formularios/consulta_producido.py
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
badd +34 ginn/formularios/consulta_existencias_por_tipo.py
badd +82 ginn/formularios/consulta_existencias.py
badd +1 ginn/formularios/consulta_producido.glade
badd +1 ginn/formularios/consumo_balas_partida.pyç
badd +28 db/restore_snapshot.sh
badd +1 extra/scripts/clouseau.py
badd +92 ginn/informes/treeview2csv.py
badd +287 ginn/formularios/consulta_ventas_por_producto.py
badd +1 (clewn)_console
args formularios/auditviewer.py
set lines=68 columns=120
edit ginn/formularios/albaranes_de_salida.py
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
8wincmd k
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
exe '1resize ' . ((&lines * 12 + 34) / 68)
exe 'vert 1resize ' . ((&columns * 39 + 60) / 120)
exe '2resize ' . ((&lines * 53 + 34) / 68)
exe 'vert 2resize ' . ((&columns * 39 + 60) / 120)
exe '3resize ' . ((&lines * 1 + 34) / 68)
exe 'vert 3resize ' . ((&columns * 80 + 60) / 120)
exe '4resize ' . ((&lines * 18 + 34) / 68)
exe 'vert 4resize ' . ((&columns * 80 + 60) / 120)
exe '5resize ' . ((&lines * 1 + 34) / 68)
exe 'vert 5resize ' . ((&columns * 80 + 60) / 120)
exe '6resize ' . ((&lines * 1 + 34) / 68)
exe 'vert 6resize ' . ((&columns * 80 + 60) / 120)
exe '7resize ' . ((&lines * 33 + 34) / 68)
exe 'vert 7resize ' . ((&columns * 80 + 60) / 120)
exe '8resize ' . ((&lines * 1 + 34) / 68)
exe 'vert 8resize ' . ((&columns * 80 + 60) / 120)
exe '9resize ' . ((&lines * 1 + 34) / 68)
exe 'vert 9resize ' . ((&columns * 80 + 60) / 120)
exe '10resize ' . ((&lines * 1 + 34) / 68)
exe 'vert 10resize ' . ((&columns * 80 + 60) / 120)
exe '11resize ' . ((&lines * 1 + 34) / 68)
exe 'vert 11resize ' . ((&columns * 80 + 60) / 120)
argglobal
enew
file (clewn)_console
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
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
9314
normal! zo
9321
normal! zo
9324
normal! zo
9339
normal! zo
9387
normal! zo
9428
normal! zo
9690
normal! zo
9716
normal! zo
9755
normal! zo
9766
normal! zo
9767
normal! zo
9780
normal! zo
9792
normal! zo
9806
normal! zo
9822
normal! zo
9839
normal! zo
9839
normal! zo
9839
normal! zo
9839
normal! zo
9839
normal! zo
9839
normal! zo
9839
normal! zo
9839
normal! zo
9839
normal! zo
9846
normal! zo
9860
normal! zo
9861
normal! zo
9861
normal! zo
9863
normal! zo
9864
normal! zo
9864
normal! zo
9866
normal! zo
9867
normal! zo
9867
normal! zo
9869
normal! zo
9870
normal! zo
9870
normal! zo
9872
normal! zo
9875
normal! zo
9877
normal! zo
9877
normal! zo
9877
normal! zo
9886
normal! zo
9899
normal! zo
9902
normal! zo
9903
normal! zo
9903
normal! zo
9906
normal! zo
9906
normal! zo
9906
normal! zo
9909
normal! zo
9909
normal! zo
9909
normal! zo
9909
normal! zo
9915
normal! zo
9918
normal! zo
9922
normal! zo
9929
normal! zo
9931
normal! zo
9978
normal! zo
9992
normal! zo
9993
normal! zo
9995
normal! zo
10030
normal! zo
10037
normal! zo
10042
normal! zo
10043
normal! zo
10048
normal! zo
10048
normal! zo
10048
normal! zo
10048
normal! zo
10048
normal! zo
10051
normal! zo
10051
normal! zo
10051
normal! zo
10077
normal! zo
10086
normal! zo
10091
normal! zo
10093
normal! zo
10098
normal! zo
10104
normal! zo
10112
normal! zo
10113
normal! zo
10113
normal! zo
10113
normal! zo
10113
normal! zo
10122
normal! zo
10123
normal! zo
10128
normal! zo
10177
normal! zo
10182
normal! zo
10295
normal! zo
10322
normal! zo
10327
normal! zo
10333
normal! zo
10419
normal! zo
10426
normal! zo
10427
normal! zo
10475
normal! zo
10475
normal! zo
10475
normal! zo
10475
normal! zo
10475
normal! zo
10478
normal! zo
10486
normal! zo
10487
normal! zo
10532
normal! zo
10552
normal! zo
10553
normal! zo
10554
normal! zo
10554
normal! zo
10554
normal! zo
10554
normal! zo
10554
normal! zo
10554
normal! zo
10554
normal! zo
10554
normal! zo
10554
normal! zo
10571
normal! zo
10577
normal! zo
10587
normal! zo
10602
normal! zo
10605
normal! zo
10608
normal! zo
10608
normal! zo
10608
normal! zo
10611
normal! zo
10611
normal! zo
10611
normal! zo
10611
normal! zo
10616
normal! zo
10616
normal! zo
10616
normal! zo
10624
normal! zo
10631
normal! zo
10638
normal! zo
10641
normal! zo
10643
normal! zo
10646
normal! zo
10649
normal! zo
10654
normal! zo
10665
normal! zo
10672
normal! zo
10676
normal! zo
10677
normal! zo
10677
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
10685
normal! zo
10686
normal! zo
10686
normal! zo
10688
normal! zo
10689
normal! zo
10689
normal! zo
10691
normal! zo
10692
normal! zo
10692
normal! zo
10694
normal! zo
10695
normal! zo
10695
normal! zo
10697
normal! zo
10700
normal! zo
10702
normal! zo
10702
normal! zo
10702
normal! zo
10708
normal! zo
10709
normal! zo
10709
normal! zo
10711
normal! zo
10712
normal! zo
10712
normal! zo
10736
normal! zo
10740
normal! zo
10743
normal! zo
10744
normal! zo
10744
normal! zo
10744
normal! zo
10744
normal! zo
10744
normal! zo
10744
normal! zo
10749
normal! zo
10750
normal! zo
10750
normal! zo
10750
normal! zo
10753
normal! zo
10865
normal! zo
10941
normal! zo
10949
normal! zo
10956
normal! zo
10956
normal! zo
10956
normal! zo
10956
normal! zo
10956
normal! zo
10956
normal! zo
10956
normal! zo
10967
normal! zo
10971
normal! zo
10972
normal! zo
10972
normal! zo
10972
normal! zo
10982
normal! zo
10985
normal! zo
10992
normal! zo
11001
normal! zo
11010
normal! zo
11120
normal! zo
11121
normal! zc
11134
normal! zo
11134
normal! zo
11134
normal! zo
11134
normal! zo
11143
normal! zc
11146
normal! zo
11159
normal! zo
11172
normal! zo
11179
normal! zo
11181
normal! zo
11181
normal! zo
11181
normal! zo
11181
normal! zo
11181
normal! zo
11181
normal! zo
11146
normal! zc
11189
normal! zc
11206
normal! zo
11234
normal! zo
11246
normal! zo
11247
normal! zo
11247
normal! zo
11247
normal! zo
11247
normal! zo
11206
normal! zc
11252
normal! zo
11252
normal! zc
11303
normal! zo
11303
normal! zc
11418
normal! zo
11426
normal! zo
11426
normal! zo
11426
normal! zo
11426
normal! zo
11418
normal! zc
11434
normal! zc
11440
normal! zo
11440
normal! zc
11451
normal! zo
11468
normal! zo
11468
normal! zo
11472
normal! zo
11477
normal! zo
11477
normal! zo
11479
normal! zo
11480
normal! zo
11480
normal! zo
11451
normal! zc
11485
normal! zo
11485
normal! zo
11485
normal! zo
11485
normal! zo
11485
normal! zo
11498
normal! zo
11501
normal! zo
11501
normal! zo
11501
normal! zo
11501
normal! zo
11485
normal! zc
11507
normal! zo
11507
normal! zo
11507
normal! zo
11507
normal! zo
11507
normal! zo
11535
normal! zo
11507
normal! zc
11573
normal! zc
11580
normal! zc
11588
normal! zo
11588
normal! zc
11596
normal! zc
11604
normal! zc
11618
normal! zo
11618
normal! zc
11636
normal! zo
11636
normal! zo
11636
normal! zo
11636
normal! zo
11636
normal! zo
11636
normal! zo
11636
normal! zo
11636
normal! zo
11636
normal! zo
11636
normal! zo
11657
normal! zo
11657
normal! zo
11657
normal! zo
11657
normal! zo
11657
normal! zo
11657
normal! zo
11698
normal! zo
11699
normal! zo
11636
normal! zc
11721
normal! zo
11721
normal! zc
11828
normal! zo
11828
normal! zc
11877
normal! zo
11877
normal! zo
11879
normal! zo
11889
normal! zo
11877
normal! zc
11972
normal! zo
11972
normal! zc
12026
normal! zo
12026
normal! zo
12026
normal! zo
12026
normal! zc
12040
normal! zo
12077
normal! zo
12088
normal! zo
12093
normal! zo
12111
normal! zo
12111
normal! zo
12111
normal! zo
12111
normal! zo
12112
normal! zo
12117
normal! zo
12133
normal! zo
12133
normal! zo
12133
normal! zo
12133
normal! zo
12026
normal! zc
12142
normal! zo
12142
normal! zo
12142
normal! zo
12142
normal! zo
12142
normal! zo
12166
normal! zo
12190
normal! zo
12190
normal! zc
12231
normal! zo
12293
normal! zo
12309
normal! zo
12309
normal! zc
12333
normal! zo
12333
normal! zc
12358
normal! zo
12358
normal! zc
12433
normal! zo
12433
normal! zc
12449
normal! zo
12449
normal! zc
12471
normal! zo
12471
normal! zc
12492
normal! zo
12492
normal! zo
12492
normal! zo
12492
normal! zo
12492
normal! zo
12492
normal! zo
12492
normal! zo
12492
normal! zc
12492
normal! zc
12612
normal! zo
12612
normal! zc
12880
normal! zo
12880
normal! zc
12910
normal! zo
12910
normal! zc
12969
normal! zo
12969
normal! zc
12985
normal! zo
12985
normal! zc
13319
normal! zc
13329
normal! zo
13329
normal! zc
13349
normal! zo
13350
normal! zo
13351
normal! zo
13349
normal! zc
13405
normal! zo
13405
normal! zc
13463
normal! zo
13463
normal! zo
13463
normal! zo
13473
normal! zo
13478
normal! zo
13479
normal! zo
13480
normal! zo
13480
normal! zo
13480
normal! zo
13480
normal! zo
13480
normal! zo
13480
normal! zo
13480
normal! zo
13480
normal! zo
13480
normal! zo
13480
normal! zo
13486
normal! zo
13487
normal! zo
13488
normal! zo
13488
normal! zo
13488
normal! zo
13488
normal! zo
13488
normal! zo
13488
normal! zo
13488
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
13492
normal! zo
13493
normal! zo
13493
normal! zo
13493
normal! zo
13493
normal! zo
13493
normal! zo
13493
normal! zo
13493
normal! zo
13493
normal! zo
13493
normal! zo
13496
normal! zo
13498
normal! zo
13498
normal! zo
13503
normal! zo
13503
normal! zo
13513
normal! zo
13514
normal! zo
13514
normal! zo
13514
normal! zo
13514
normal! zo
13514
normal! zo
13514
normal! zo
13463
normal! zc
13521
normal! zo
13521
normal! zc
13577
normal! zo
13577
normal! zc
13633
normal! zo
13633
normal! zo
13633
normal! zo
13654
normal! zo
13659
normal! zo
13660
normal! zo
13661
normal! zo
13661
normal! zo
13661
normal! zo
13661
normal! zo
13661
normal! zo
13661
normal! zo
13661
normal! zo
13661
normal! zo
13661
normal! zo
13661
normal! zo
13667
normal! zo
13668
normal! zo
13669
normal! zo
13669
normal! zo
13669
normal! zo
13669
normal! zo
13669
normal! zo
13669
normal! zo
13669
normal! zo
13671
normal! zo
13671
normal! zo
13671
normal! zo
13671
normal! zo
13671
normal! zo
13671
normal! zo
13671
normal! zo
13671
normal! zo
13673
normal! zo
13674
normal! zo
13674
normal! zo
13674
normal! zo
13674
normal! zo
13674
normal! zo
13674
normal! zo
13674
normal! zo
13674
normal! zo
13674
normal! zo
13677
normal! zo
13679
normal! zo
13684
normal! zo
13693
normal! zo
13694
normal! zo
13694
normal! zo
13694
normal! zo
13694
normal! zo
13694
normal! zo
13694
normal! zo
13694
normal! zo
13633
normal! zc
13701
normal! zo
13701
normal! zc
13733
normal! zo
13733
normal! zc
13764
normal! zo
13764
normal! zo
13764
normal! zo
13775
normal! zo
13780
normal! zo
13781
normal! zo
13782
normal! zo
13782
normal! zo
13782
normal! zo
13782
normal! zo
13782
normal! zo
13782
normal! zo
13782
normal! zo
13782
normal! zo
13782
normal! zo
13782
normal! zo
13788
normal! zo
13789
normal! zo
13790
normal! zo
13790
normal! zo
13790
normal! zo
13790
normal! zo
13790
normal! zo
13790
normal! zo
13790
normal! zo
13792
normal! zo
13792
normal! zo
13792
normal! zo
13792
normal! zo
13792
normal! zo
13792
normal! zo
13792
normal! zo
13792
normal! zo
13794
normal! zo
13795
normal! zo
13795
normal! zo
13795
normal! zo
13795
normal! zo
13795
normal! zo
13795
normal! zo
13795
normal! zo
13795
normal! zo
13795
normal! zo
13798
normal! zo
13800
normal! zo
13805
normal! zo
13814
normal! zo
13815
normal! zo
13815
normal! zo
13815
normal! zo
13815
normal! zo
13815
normal! zo
13815
normal! zo
13815
normal! zo
13764
normal! zc
13822
normal! zo
13822
normal! zc
13863
normal! zo
13863
normal! zc
13898
normal! zo
13898
normal! zc
13910
normal! zo
13910
normal! zc
13922
normal! zo
13922
normal! zo
13922
normal! zo
13922
normal! zo
13922
normal! zo
13922
normal! zo
13922
normal! zo
13922
normal! zo
13922
normal! zo
13932
normal! zo
13932
normal! zo
13932
normal! zo
13932
normal! zo
13932
normal! zo
13932
normal! zo
13934
normal! zo
13935
normal! zo
13935
normal! zo
13935
normal! zo
13922
normal! zc
13941
normal! zo
13941
normal! zo
13941
normal! zo
13941
normal! zo
13941
normal! zo
13941
normal! zo
13941
normal! zo
13941
normal! zo
13941
normal! zo
13941
normal! zc
13961
normal! zo
13961
normal! zc
14040
normal! zo
14040
normal! zc
14075
normal! zo
14075
normal! zc
14111
normal! zo
14111
normal! zc
14118
normal! zo
14118
normal! zc
14130
normal! zo
14130
normal! zo
14130
normal! zo
14130
normal! zo
14146
normal! zo
14151
normal! zo
14152
normal! zo
14153
normal! zo
14153
normal! zo
14153
normal! zo
14153
normal! zo
14153
normal! zo
14153
normal! zo
14153
normal! zo
14153
normal! zo
14153
normal! zo
14153
normal! zo
14159
normal! zo
14160
normal! zo
14161
normal! zo
14161
normal! zo
14161
normal! zo
14161
normal! zo
14161
normal! zo
14161
normal! zo
14161
normal! zo
14163
normal! zo
14163
normal! zo
14163
normal! zo
14163
normal! zo
14163
normal! zo
14163
normal! zo
14163
normal! zo
14163
normal! zo
14163
normal! zo
14165
normal! zo
14166
normal! zo
14166
normal! zo
14166
normal! zo
14166
normal! zo
14166
normal! zo
14166
normal! zo
14166
normal! zo
14166
normal! zo
14166
normal! zo
14169
normal! zo
14171
normal! zo
14171
normal! zo
14176
normal! zo
14176
normal! zo
14186
normal! zo
14187
normal! zo
14187
normal! zo
14187
normal! zo
14187
normal! zo
14187
normal! zo
14187
normal! zo
14130
normal! zc
14194
normal! zo
14194
normal! zc
14214
normal! zo
14214
normal! zc
14233
normal! zo
14233
normal! zc
14240
normal! zo
14240
normal! zc
14247
normal! zo
14247
normal! zo
14247
normal! zo
14247
normal! zo
14259
normal! zo
14264
normal! zo
14265
normal! zo
14266
normal! zo
14266
normal! zo
14266
normal! zo
14266
normal! zo
14266
normal! zo
14266
normal! zo
14266
normal! zo
14266
normal! zo
14266
normal! zo
14266
normal! zo
14272
normal! zo
14273
normal! zo
14274
normal! zo
14274
normal! zo
14274
normal! zo
14274
normal! zo
14274
normal! zo
14274
normal! zo
14274
normal! zo
14276
normal! zo
14276
normal! zo
14276
normal! zo
14276
normal! zo
14276
normal! zo
14276
normal! zo
14276
normal! zo
14276
normal! zo
14276
normal! zo
14278
normal! zo
14279
normal! zo
14279
normal! zo
14279
normal! zo
14279
normal! zo
14279
normal! zo
14279
normal! zo
14279
normal! zo
14279
normal! zo
14279
normal! zo
14282
normal! zo
14284
normal! zo
14284
normal! zo
14289
normal! zo
14289
normal! zo
14299
normal! zo
14300
normal! zo
14300
normal! zo
14300
normal! zo
14300
normal! zo
14300
normal! zo
14300
normal! zo
14247
normal! zc
14307
normal! zo
14307
normal! zc
14348
normal! zo
14348
normal! zc
14363
normal! zc
14368
normal! zo
14380
normal! zo
14383
normal! zo
14384
normal! zo
14385
normal! zo
14385
normal! zo
14385
normal! zo
14387
normal! zo
14388
normal! zo
14388
normal! zo
14388
normal! zo
14368
normal! zc
14404
normal! zo
14415
normal! zo
14424
normal! zo
14434
normal! zo
14461
normal! zo
14466
normal! zo
14472
normal! zo
14483
normal! zo
14496
normal! zo
14520
normal! zo
14522
normal! zo
14525
normal! zo
14528
normal! zo
14529
normal! zo
14533
normal! zo
14534
normal! zo
14548
normal! zo
14548
normal! zo
14548
normal! zo
14548
normal! zo
14570
normal! zo
14571
normal! zo
14572
normal! zo
14572
normal! zo
14572
normal! zo
14572
normal! zo
14572
normal! zo
14572
normal! zo
14572
normal! zo
14572
normal! zo
14572
normal! zo
14572
normal! zo
14581
normal! zo
14582
normal! zo
14588
normal! zo
14592
normal! zo
14593
normal! zo
14602
normal! zo
14603
normal! zo
14611
normal! zo
14612
normal! zo
14618
normal! zo
14633
normal! zo
14641
normal! zo
14647
normal! zo
14653
normal! zo
14658
normal! zo
14662
normal! zo
14668
normal! zo
14673
normal! zo
14674
normal! zo
14679
normal! zo
14690
normal! zo
14708
normal! zo
14750
normal! zo
14756
normal! zo
14762
normal! zo
14769
normal! zo
14778
normal! zo
14780
normal! zo
14787
normal! zo
14787
normal! zo
14787
normal! zo
14787
normal! zo
14787
normal! zo
14787
normal! zo
14804
normal! zo
14816
normal! zo
14827
normal! zo
14828
normal! zo
14844
normal! zo
14861
normal! zo
14865
normal! zo
14866
normal! zo
14867
normal! zo
14867
normal! zo
14869
normal! zo
14872
normal! zo
14885
normal! zo
14895
normal! zo
14897
normal! zo
14901
normal! zo
14902
normal! zo
14902
normal! zo
14902
normal! zo
14902
normal! zo
14902
normal! zo
14902
normal! zo
14915
normal! zo
14936
normal! zo
14937
normal! zo
14944
normal! zo
14977
normal! zo
14978
normal! zo
14978
normal! zo
14994
normal! zo
15000
normal! zo
15003
normal! zo
15003
normal! zo
15003
normal! zo
15009
normal! zo
15009
normal! zo
15029
normal! zo
15034
normal! zo
15039
normal! zo
15047
normal! zo
15066
normal! zo
15100
normal! zo
15108
normal! zo
15117
normal! zo
15136
normal! zo
15138
normal! zo
15142
normal! zo
15159
normal! zo
15165
normal! zo
15169
normal! zo
15208
normal! zo
15312
normal! zo
15501
normal! zo
15532
normal! zo
15556
normal! zo
15566
normal! zo
15566
normal! zo
15566
normal! zo
15566
normal! zo
15566
normal! zo
15754
normal! zo
15773
normal! zo
15795
normal! zo
15800
normal! zo
15801
normal! zo
15801
normal! zo
15804
normal! zo
15805
normal! zo
15805
normal! zo
15805
normal! zo
15808
normal! zo
15808
normal! zo
15808
normal! zo
15812
normal! zo
15812
normal! zo
15812
normal! zo
15812
normal! zo
15812
normal! zo
15812
normal! zo
15812
normal! zo
15812
normal! zo
15812
normal! zo
16343
normal! zo
16379
normal! zo
16394
normal! zo
16400
normal! zo
16403
normal! zo
16411
normal! zo
16412
normal! zo
16412
normal! zo
16412
normal! zo
16412
normal! zo
16412
normal! zo
16416
normal! zo
16424
normal! zo
16427
normal! zo
16433
normal! zo
16439
normal! zo
16442
normal! zo
16448
normal! zo
16462
normal! zo
16468
normal! zo
16473
normal! zo
16476
normal! zo
16476
normal! zo
16476
normal! zo
16486
normal! zo
16501
normal! zo
16512
normal! zo
16512
normal! zo
16523
normal! zo
16538
normal! zo
16548
normal! zo
16559
normal! zo
16568
normal! zo
16575
normal! zo
16613
normal! zo
16618
normal! zo
16618
normal! zo
16618
normal! zo
16631
normal! zo
16631
normal! zo
16631
normal! zo
16631
normal! zo
16631
normal! zo
16631
normal! zo
16631
normal! zo
16631
normal! zo
16631
normal! zo
16631
normal! zo
16631
normal! zo
16643
normal! zo
16664
normal! zo
16683
normal! zo
16691
normal! zo
16692
normal! zo
16693
normal! zo
16697
normal! zo
16701
normal! zo
16717
normal! zo
16732
normal! zo
16737
normal! zo
16742
normal! zo
16752
normal! zo
16753
normal! zo
16753
normal! zo
16753
normal! zo
16755
normal! zo
16755
normal! zo
16755
normal! zo
16755
normal! zo
16755
normal! zo
16755
normal! zo
16755
normal! zo
16755
normal! zo
16755
normal! zo
16755
normal! zo
16760
normal! zo
16761
normal! zo
16767
normal! zo
16768
normal! zo
16788
normal! zo
16813
normal! zo
16817
normal! zo
16834
normal! zo
16845
normal! zo
16845
normal! zo
16845
normal! zo
16845
normal! zo
16847
normal! zo
16848
normal! zo
16849
normal! zo
16850
normal! zo
16851
normal! zo
16855
normal! zo
16856
normal! zo
16857
normal! zo
16857
normal! zo
16857
normal! zo
16857
normal! zo
16857
normal! zo
16857
normal! zo
16857
normal! zo
16859
normal! zo
16861
normal! zo
16866
normal! zo
16866
normal! zo
16866
normal! zo
16866
normal! zo
16872
normal! zo
16876
normal! zo
16884
normal! zo
16884
normal! zo
16884
normal! zo
16884
normal! zo
16892
normal! zo
16900
normal! zo
16901
normal! zo
16904
normal! zo
16909
normal! zo
16917
normal! zo
16922
normal! zo
16930
normal! zo
16935
normal! zo
16944
normal! zo
16945
normal! zo
16945
normal! zo
16955
normal! zo
16970
normal! zo
16971
normal! zo
16987
normal! zo
17007
normal! zo
17008
normal! zo
17008
normal! zo
17008
normal! zo
17008
normal! zo
17008
normal! zo
17014
normal! zo
17024
normal! zo
17038
normal! zo
17041
normal! zo
17045
normal! zo
17046
normal! zo
17047
normal! zo
17047
normal! zo
17047
normal! zo
17047
normal! zo
17047
normal! zo
17065
normal! zo
17072
normal! zo
17073
normal! zo
17080
normal! zo
17087
normal! zo
17088
normal! zo
17089
normal! zo
17094
normal! zo
17101
normal! zo
17106
normal! zo
17119
normal! zo
17120
normal! zo
17120
normal! zo
17120
normal! zo
17125
normal! zo
17138
normal! zo
17145
normal! zo
17146
normal! zo
17161
normal! zo
17168
normal! zo
17182
normal! zo
17189
normal! zo
17190
normal! zo
17195
normal! zo
17204
normal! zo
17218
normal! zo
17240
normal! zo
17261
normal! zo
17274
normal! zo
17274
normal! zo
17274
normal! zo
17274
normal! zo
17274
normal! zo
17274
normal! zo
17284
normal! zo
17297
normal! zo
17321
normal! zo
17326
normal! zo
17328
normal! zo
17331
normal! zo
17338
normal! zo
17350
normal! zo
17360
normal! zo
17360
normal! zo
17360
normal! zo
17360
normal! zo
17360
normal! zo
17360
normal! zo
17368
normal! zo
17378
normal! zo
17378
normal! zo
17378
normal! zo
17378
normal! zo
17378
normal! zo
17378
normal! zo
17386
normal! zo
17387
normal! zo
17398
normal! zo
17403
normal! zo
17414
normal! zo
17422
normal! zo
17435
normal! zo
17439
normal! zo
17439
normal! zo
17439
normal! zo
17439
normal! zo
17439
normal! zo
17441
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
17453
normal! zo
17457
normal! zo
17457
normal! zo
17457
normal! zo
17457
normal! zo
17457
normal! zo
17457
normal! zo
17463
normal! zo
17463
normal! zo
17463
normal! zo
17463
normal! zo
17466
normal! zo
17467
normal! zo
17468
normal! zo
17474
normal! zo
17475
normal! zo
17475
normal! zo
17475
normal! zo
17597
normal! zo
17685
normal! zo
17742
normal! zo
17757
normal! zo
17764
normal! zo
17765
normal! zo
17781
normal! zo
17791
normal! zo
17805
normal! zo
17808
normal! zo
17809
normal! zo
17809
normal! zo
17831
normal! zo
17851
normal! zo
17863
normal! zo
17863
normal! zo
17863
normal! zo
17863
normal! zo
17863
normal! zo
17866
normal! zo
17873
normal! zo
17876
normal! zo
17887
normal! zo
17893
normal! zo
17898
normal! zo
17904
normal! zo
17905
normal! zo
17906
normal! zo
17909
normal! zo
17928
normal! zo
17943
normal! zo
17971
normal! zo
17996
normal! zo
18017
normal! zo
18052
normal! zo
18061
normal! zo
18062
normal! zo
18063
normal! zo
18065
normal! zo
18065
normal! zo
18065
normal! zo
18068
normal! zo
18070
normal! zo
18070
normal! zo
18070
normal! zo
18073
normal! zo
18074
normal! zo
18074
normal! zo
18074
normal! zo
18074
normal! zo
18074
normal! zo
18600
normal! zo
18617
normal! zo
18627
normal! zo
18630
normal! zo
18631
normal! zo
18631
normal! zo
18637
normal! zo
18644
normal! zo
18645
normal! zo
18646
normal! zo
18646
normal! zo
18646
normal! zo
18646
normal! zo
18650
normal! zo
18651
normal! zo
18651
normal! zo
18651
normal! zo
18651
normal! zo
18667
normal! zo
18968
normal! zo
19885
normal! zo
19909
normal! zo
19915
normal! zo
19921
normal! zo
19939
normal! zo
19949
normal! zo
19952
normal! zo
19959
normal! zo
19959
normal! zo
19959
normal! zo
19959
normal! zo
19964
normal! zo
20244
normal! zo
20250
normal! zo
20250
normal! zo
20259
normal! zo
20266
normal! zo
20273
normal! zo
20280
normal! zo
20287
normal! zo
20294
normal! zo
20301
normal! zo
20307
normal! zo
20308
normal! zo
20317
normal! zo
20326
normal! zo
20489
normal! zo
20499
normal! zo
20510
normal! zo
20521
normal! zo
20522
normal! zo
20527
normal! zo
20528
normal! zo
20528
normal! zo
20538
normal! zo
20538
normal! zo
20538
normal! zo
20538
normal! zo
20538
normal! zo
20538
normal! zo
20538
normal! zo
20538
normal! zo
20538
normal! zo
20549
normal! zo
20550
normal! zo
20558
normal! zo
20558
normal! zo
20558
normal! zo
20558
normal! zo
20558
normal! zo
20558
normal! zo
20558
normal! zo
20558
normal! zo
20569
normal! zo
20570
normal! zo
20578
normal! zo
20593
normal! zo
20626
normal! zo
20647
normal! zo
20652
normal! zo
20664
normal! zo
20664
normal! zo
20664
normal! zo
20664
normal! zo
20664
normal! zo
20664
normal! zo
20664
normal! zo
20682
normal! zo
20689
normal! zo
let s:l = 12293 - ((2 * winheight(0) + 9) / 18)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
12293
normal! 013|
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
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/consulta_existencias_por_tipo.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
45
normal! zo
46
normal! zo
56
normal! zo
67
normal! zo
68
normal! zo
114
normal! zo
121
normal! zo
141
normal! zo
149
normal! zo
164
normal! zo
169
normal! zo
182
normal! zo
182
normal! zo
182
normal! zo
182
normal! zo
184
normal! zo
185
normal! zo
191
normal! zo
193
normal! zo
194
normal! zo
204
normal! zo
209
normal! zo
220
normal! zo
234
normal! zo
243
normal! zo
244
normal! zo
245
normal! zo
271
normal! zo
301
normal! zo
301
normal! zo
301
normal! zo
301
normal! zo
301
normal! zo
301
normal! zo
309
normal! zo
309
normal! zo
309
normal! zo
309
normal! zo
322
normal! zo
322
normal! zo
322
normal! zo
322
normal! zo
322
normal! zo
322
normal! zo
322
normal! zo
322
normal! zo
322
normal! zo
let s:l = 297 - ((28 * winheight(0) + 16) / 33)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
297
normal! 08|
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
let s:l = 228 - ((0 * winheight(0) + 0) / 1)
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
55
normal! zo
63
normal! zo
63
normal! zo
274
normal! zo
let s:l = 249 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
249
normal! 015|
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
202
normal! zo
215
normal! zo
224
normal! zo
242
normal! zo
255
normal! zo
263
normal! zo
263
normal! zo
263
normal! zo
263
normal! zo
270
normal! zo
270
normal! zo
270
normal! zo
270
normal! zo
274
normal! zo
275
normal! zo
275
normal! zo
298
normal! zo
299
normal! zo
299
normal! zo
329
normal! zo
338
normal! zo
339
normal! zo
339
normal! zo
339
normal! zo
341
normal! zo
342
normal! zo
342
normal! zo
342
normal! zo
342
normal! zo
342
normal! zo
342
normal! zo
358
normal! zo
361
normal! zo
361
normal! zo
361
normal! zo
361
normal! zo
361
normal! zo
361
normal! zo
361
normal! zo
361
normal! zo
361
normal! zo
361
normal! zo
361
normal! zo
361
normal! zo
363
normal! zo
367
normal! zo
375
normal! zo
376
normal! zo
376
normal! zo
377
normal! zo
381
normal! zo
383
normal! zo
385
normal! zo
389
normal! zo
399
normal! zo
405
normal! zo
405
normal! zo
405
normal! zo
405
normal! zo
408
normal! zo
418
normal! zo
423
normal! zo
423
normal! zo
423
normal! zo
423
normal! zo
426
normal! zo
427
normal! zo
431
normal! zo
444
normal! zo
444
normal! zo
444
normal! zo
444
normal! zo
446
normal! zo
446
normal! zo
446
normal! zo
446
normal! zo
451
normal! zo
451
normal! zo
451
normal! zo
451
normal! zo
453
normal! zo
453
normal! zo
453
normal! zo
453
normal! zo
457
normal! zo
458
normal! zo
461
normal! zo
474
normal! zo
474
normal! zo
474
normal! zo
474
normal! zo
476
normal! zo
476
normal! zo
476
normal! zo
476
normal! zo
481
normal! zo
481
normal! zo
481
normal! zo
481
normal! zo
484
normal! zo
484
normal! zo
484
normal! zo
484
normal! zo
489
normal! zo
490
normal! zo
493
normal! zo
507
normal! zo
507
normal! zo
507
normal! zo
507
normal! zo
509
normal! zo
509
normal! zo
509
normal! zo
509
normal! zo
514
normal! zo
515
normal! zo
515
normal! zo
515
normal! zo
515
normal! zo
522
normal! zo
523
normal! zo
523
normal! zo
523
normal! zo
523
normal! zo
527
normal! zo
528
normal! zo
530
normal! zo
530
normal! zo
530
normal! zo
530
normal! zo
530
normal! zo
530
normal! zo
530
normal! zo
530
normal! zo
530
normal! zo
530
normal! zo
530
normal! zo
530
normal! zo
530
normal! zo
550
normal! zo
570
normal! zo
576
normal! zo
582
normal! zo
627
normal! zo
633
normal! zo
633
normal! zo
633
normal! zo
633
normal! zo
633
normal! zo
645
normal! zo
648
normal! zo
648
normal! zo
648
normal! zo
648
normal! zo
654
normal! zo
665
normal! zo
698
normal! zo
702
normal! zo
702
normal! zo
714
normal! zo
718
normal! zo
718
normal! zo
733
normal! zo
733
normal! zo
733
normal! zo
733
normal! zo
733
normal! zo
742
normal! zo
743
normal! zo
743
normal! zo
757
normal! zo
758
normal! zo
758
normal! zo
758
normal! zo
758
normal! zo
758
normal! zo
758
normal! zo
758
normal! zo
758
normal! zo
758
normal! zo
771
normal! zo
771
normal! zo
771
normal! zo
771
normal! zo
771
normal! zo
780
normal! zo
let s:l = 36 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
36
normal! 0
wincmd w
7wincmd w
exe '1resize ' . ((&lines * 12 + 34) / 68)
exe 'vert 1resize ' . ((&columns * 39 + 60) / 120)
exe '2resize ' . ((&lines * 53 + 34) / 68)
exe 'vert 2resize ' . ((&columns * 39 + 60) / 120)
exe '3resize ' . ((&lines * 1 + 34) / 68)
exe 'vert 3resize ' . ((&columns * 80 + 60) / 120)
exe '4resize ' . ((&lines * 18 + 34) / 68)
exe 'vert 4resize ' . ((&columns * 80 + 60) / 120)
exe '5resize ' . ((&lines * 1 + 34) / 68)
exe 'vert 5resize ' . ((&columns * 80 + 60) / 120)
exe '6resize ' . ((&lines * 1 + 34) / 68)
exe 'vert 6resize ' . ((&columns * 80 + 60) / 120)
exe '7resize ' . ((&lines * 33 + 34) / 68)
exe 'vert 7resize ' . ((&columns * 80 + 60) / 120)
exe '8resize ' . ((&lines * 1 + 34) / 68)
exe 'vert 8resize ' . ((&columns * 80 + 60) / 120)
exe '9resize ' . ((&lines * 1 + 34) / 68)
exe 'vert 9resize ' . ((&columns * 80 + 60) / 120)
exe '10resize ' . ((&lines * 1 + 34) / 68)
exe 'vert 10resize ' . ((&columns * 80 + 60) / 120)
exe '11resize ' . ((&lines * 1 + 34) / 68)
exe 'vert 11resize ' . ((&columns * 80 + 60) / 120)
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
7wincmd w

" vim: ft=vim ro nowrap smc=128
