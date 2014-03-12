" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 11 marzo 2014 at 17:40:45.
" Open this file in Vim and run :source % to restore your session.

set guioptions=aegimrLtT
silent! set guifont=Inconsolata\ 9
if exists('g:syntax_on') != 1 | syntax on | endif
if exists('g:did_load_filetypes') != 1 | filetype on | endif
if exists('g:did_load_ftplugin') != 1 | filetype plugin on | endif
if exists('g:did_indent_on') != 1 | filetype indent on | endif
if &background != 'dark'
	set background=dark
endif
if !exists('g:colors_name') || g:colors_name != 'gruvbox' | colorscheme gruvbox | endif
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
badd +9 ginn/formularios/consulta_producido.py
badd +1 ginn/__init__.py
badd +1505 ginn/formularios/clientes.py
badd +991 ginn/formularios/productos_compra.py
badd +206 ginn/formularios/productos_de_venta_balas.py
badd +525 ginn/formularios/recibos.py
badd +374 ginn/formularios/productos_de_venta_rollos.py
badd +315 ginn/formularios/productos_de_venta_rollos_geocompuestos.py
badd +337 ginn/formularios/productos_de_venta_especial.py
badd +2463 ginn/formularios/partes_de_fabricacion_balas.py
badd +737 ginn/formularios/partes_de_fabricacion_bolsas.py
badd +1899 ginn/formularios/partes_de_fabricacion_rollos.py
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
badd +3073 ginn/formularios/albaranes_de_salida.py
badd +93 ginn/formularios/presupuesto.py
badd +1884 ginn/formularios/presupuestos.py
badd +97 ginn/informes/carta_compromiso.py
badd +367 ginn/formularios/tarifas_de_precios.py
badd +88 ginn/formularios/logviewer.py
badd +1527 ginn/formularios/facturas_compra.py
badd +2785 ginn/formularios/utils.py
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
badd +82 ginn/formularios/balas_cable.py
badd +13 ginn/informes/nied.py
badd +82 ginn/informes/norma2013.py
badd +65 ginn/formularios/widgets.py
badd +1 ginn/informes/ekotex.py
badd +7 ~/.vim/ftplugin/python.vim
badd +140 ginn/formularios/listado_balas.py
badd +227 ginn/formularios/consulta_pendientes_servir.py
badd +130 ginn/formularios/facturas_no_bloqueadas.py
badd +611 ginn/formularios/consumo_balas_partida.py
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
badd +193 ginn/formularios/consulta_productividad.py
badd +171 ginn/formularios/mail_sender.py
badd +1143 ginn/formularios/abonos_venta.py
badd +306 ginn/formularios/ventana_progreso.py
badd +993 ginn/formularios/control_personal.py
badd +594 ginn/formularios/listado_rollos.py
badd +74 ginn/formularios/consulta_existenciasRollos.py
badd +64 ginn/formularios/listado_rollos_defectuosos.py
badd +500 ginn/formularios/consulta_global.py
badd +91 ginn/formularios/rollos_c.py
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
badd +121 ginn/formularios/consumo_fibra_por_partida_gtx.py
badd +138 ginn/lib/charting.py
badd +66 ginn/formularios/consulta_existenciasBalas.py
badd +338 ginn/formularios/consulta_consumo.py
badd +182 ginn/formularios/consulta_existencias_por_tipo.py
badd +82 ginn/formularios/consulta_existencias.py
badd +1 ginn/formularios/consulta_producido.glade
badd +1 ginn/formularios/consumo_balas_partida.pyç
badd +28 db/restore_snapshot.sh
badd +1 extra/scripts/clouseau.py
badd +92 ginn/informes/treeview2csv.py
badd +287 ginn/formularios/consulta_ventas_por_producto.py
badd +1 tests/stock_performance.py
badd +1 (clewn)_console
badd +1 ginn/formularios/consulta_productividad.glade
args formularios/auditviewer.py
set lines=51 columns=115
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
exe '1resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 1resize ' . ((&columns * 34 + 57) / 115)
exe '2resize ' . ((&lines * 47 + 25) / 51)
exe 'vert 2resize ' . ((&columns * 34 + 57) / 115)
exe '3resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 3resize ' . ((&columns * 80 + 57) / 115)
exe '4resize ' . ((&lines * 24 + 25) / 51)
exe 'vert 4resize ' . ((&columns * 80 + 57) / 115)
exe '5resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 5resize ' . ((&columns * 80 + 57) / 115)
exe '6resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 6resize ' . ((&columns * 80 + 57) / 115)
exe '7resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 7resize ' . ((&columns * 80 + 57) / 115)
exe '8resize ' . ((&lines * 8 + 25) / 51)
exe 'vert 8resize ' . ((&columns * 80 + 57) / 115)
exe '9resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 9resize ' . ((&columns * 80 + 57) / 115)
exe '10resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 10resize ' . ((&columns * 80 + 57) / 115)
exe '11resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 11resize ' . ((&columns * 80 + 57) / 115)
exe '12resize ' . ((&lines * 1 + 25) / 51)
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
let s:l = 1 - ((0 * winheight(0) + 0) / 1)
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
2019
normal! zo
2032
normal! zo
2032
normal! zo
2032
normal! zo
2032
normal! zo
2032
normal! zo
2032
normal! zo
2032
normal! zo
2041
normal! zo
2063
normal! zo
2068
normal! zo
2068
normal! zo
2194
normal! zo
2828
normal! zo
2837
normal! zo
3060
normal! zo
3258
normal! zo
3270
normal! zo
3271
normal! zo
3272
normal! zo
3289
normal! zo
3289
normal! zo
4212
normal! zo
4242
normal! zo
let s:l = 4799 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
4799
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
6340
normal! zo
6889
normal! zo
7139
normal! zo
7146
normal! zo
7164
normal! zo
7175
normal! zo
7175
normal! zo
7175
normal! zo
7178
normal! zo
7178
normal! zo
7181
normal! zo
7181
normal! zo
7184
normal! zo
7184
normal! zo
7188
normal! zo
7192
normal! zo
7200
normal! zo
7218
normal! zo
7219
normal! zo
7228
normal! zo
7229
normal! zo
7616
normal! zo
7645
normal! zo
7645
normal! zo
7645
normal! zo
7645
normal! zo
7645
normal! zo
7669
normal! zo
7738
normal! zo
7757
normal! zo
7760
normal! zo
7761
normal! zo
7761
normal! zo
7761
normal! zo
7774
normal! zo
7775
normal! zo
7776
normal! zo
7781
normal! zo
7787
normal! zo
7793
normal! zo
7793
normal! zo
7793
normal! zo
7793
normal! zo
7793
normal! zo
7793
normal! zo
7795
normal! zo
7834
normal! zo
7844
normal! zo
7845
normal! zo
7853
normal! zo
7854
normal! zo
7857
normal! zo
7862
normal! zo
7863
normal! zo
7864
normal! zo
7865
normal! zo
7865
normal! zo
7865
normal! zo
7865
normal! zo
7865
normal! zo
7865
normal! zo
7869
normal! zo
7875
normal! zo
7878
normal! zo
7878
normal! zo
7878
normal! zo
7878
normal! zo
7878
normal! zo
7887
normal! zo
7888
normal! zo
7889
normal! zo
7897
normal! zo
7904
normal! zo
7904
normal! zo
7904
normal! zo
7904
normal! zo
7904
normal! zo
7904
normal! zo
7906
normal! zo
7906
normal! zo
7906
normal! zo
7906
normal! zo
7906
normal! zo
7906
normal! zo
7906
normal! zo
7909
normal! zo
7909
normal! zo
7909
normal! zo
7909
normal! zo
7909
normal! zo
7909
normal! zo
7910
normal! zo
7910
normal! zo
7910
normal! zo
7910
normal! zo
7912
normal! zo
7913
normal! zo
7922
normal! zo
7929
normal! zo
7929
normal! zo
7929
normal! zo
7929
normal! zo
7929
normal! zo
7929
normal! zo
7931
normal! zo
7934
normal! zo
7934
normal! zo
7934
normal! zo
7934
normal! zo
7934
normal! zo
7934
normal! zo
7935
normal! zo
7935
normal! zo
7935
normal! zo
7935
normal! zo
7937
normal! zo
7938
normal! zo
7941
normal! zo
7946
normal! zo
7946
normal! zo
7946
normal! zo
7946
normal! zo
7946
normal! zo
7946
normal! zo
7946
normal! zo
7994
normal! zo
7999
normal! zo
8001
normal! zo
8002
normal! zo
8002
normal! zo
8002
normal! zo
8002
normal! zo
8002
normal! zo
8002
normal! zo
8005
normal! zo
8011
normal! zo
8014
normal! zo
8023
normal! zo
8025
normal! zo
8026
normal! zo
8033
normal! zo
8034
normal! zo
8035
normal! zo
8040
normal! zo
8044
normal! zo
8052
normal! zo
8053
normal! zo
8055
normal! zo
8055
normal! zo
8062
normal! zo
8063
normal! zo
8064
normal! zo
8064
normal! zo
8064
normal! zo
8064
normal! zo
8064
normal! zo
8064
normal! zo
8064
normal! zo
8064
normal! zo
8067
normal! zo
8067
normal! zo
8067
normal! zo
8074
normal! zo
8076
normal! zo
8359
normal! zo
8370
normal! zo
8371
normal! zo
8371
normal! zo
8371
normal! zo
8371
normal! zo
8371
normal! zo
8371
normal! zo
8371
normal! zo
8374
normal! zo
8374
normal! zo
8374
normal! zo
8374
normal! zo
8374
normal! zo
8374
normal! zo
8374
normal! zo
8378
normal! zo
8385
normal! zo
8385
normal! zo
8385
normal! zo
8385
normal! zo
8385
normal! zo
8385
normal! zo
8385
normal! zo
8385
normal! zo
8388
normal! zo
8388
normal! zo
8388
normal! zo
8388
normal! zo
8388
normal! zo
8388
normal! zo
8388
normal! zo
8388
normal! zo
8823
normal! zo
8827
normal! zo
8858
normal! zo
8907
normal! zo
8914
normal! zo
9082
normal! zo
9093
normal! zo
9106
normal! zo
9107
normal! zo
9120
normal! zo
9125
normal! zo
9130
normal! zo
9135
normal! zo
9146
normal! zo
9169
normal! zo
9192
normal! zo
9193
normal! zo
9193
normal! zo
9193
normal! zo
9193
normal! zo
9193
normal! zo
9193
normal! zo
9204
normal! zo
9219
normal! zo
9254
normal! zo
9342
normal! zo
9374
normal! zo
9381
normal! zo
9385
normal! zo
9390
normal! zo
9405
normal! zo
9453
normal! zo
9494
normal! zo
9515
normal! zo
9756
normal! zo
9782
normal! zo
9821
normal! zo
9832
normal! zo
9833
normal! zo
9846
normal! zo
9862
normal! zo
9878
normal! zo
9882
normal! zo
9882
normal! zo
9884
normal! zo
9890
normal! zo
9901
normal! zo
9917
normal! zo
9934
normal! zo
9934
normal! zo
9934
normal! zo
9934
normal! zo
9934
normal! zo
9934
normal! zo
9934
normal! zo
9934
normal! zo
9934
normal! zo
9941
normal! zo
9955
normal! zo
9956
normal! zo
9956
normal! zo
9958
normal! zo
9959
normal! zo
9959
normal! zo
9961
normal! zo
9962
normal! zo
9962
normal! zo
9964
normal! zo
9965
normal! zo
9965
normal! zo
9967
normal! zo
9970
normal! zo
9972
normal! zo
9972
normal! zo
9972
normal! zo
9981
normal! zo
9994
normal! zo
9997
normal! zo
9998
normal! zo
9998
normal! zo
10001
normal! zo
10001
normal! zo
10001
normal! zo
10004
normal! zo
10004
normal! zo
10004
normal! zo
10004
normal! zo
10010
normal! zo
10013
normal! zo
10017
normal! zo
10024
normal! zo
10026
normal! zo
10073
normal! zo
10087
normal! zo
10088
normal! zo
10090
normal! zo
10125
normal! zo
10132
normal! zo
10137
normal! zo
10138
normal! zo
10143
normal! zo
10143
normal! zo
10143
normal! zo
10143
normal! zo
10143
normal! zo
10146
normal! zo
10146
normal! zo
10146
normal! zo
10172
normal! zo
10181
normal! zo
10186
normal! zo
10188
normal! zo
10193
normal! zo
10199
normal! zo
10207
normal! zo
10208
normal! zo
10208
normal! zo
10208
normal! zo
10208
normal! zo
10217
normal! zo
10218
normal! zo
10223
normal! zo
10272
normal! zo
10277
normal! zo
10390
normal! zo
10417
normal! zo
10422
normal! zo
10428
normal! zo
10514
normal! zo
10521
normal! zo
10522
normal! zo
10570
normal! zo
10570
normal! zo
10570
normal! zo
10570
normal! zo
10570
normal! zo
10573
normal! zo
10581
normal! zo
10582
normal! zo
10627
normal! zo
10647
normal! zo
10648
normal! zo
10649
normal! zo
10649
normal! zo
10649
normal! zo
10649
normal! zo
10649
normal! zo
10649
normal! zo
10649
normal! zo
10649
normal! zo
10649
normal! zo
10666
normal! zo
10672
normal! zo
10682
normal! zo
10697
normal! zo
10700
normal! zo
10703
normal! zo
10703
normal! zo
10703
normal! zo
10706
normal! zo
10706
normal! zo
10706
normal! zo
10706
normal! zo
10711
normal! zo
10711
normal! zo
10711
normal! zo
10719
normal! zo
10726
normal! zo
10733
normal! zo
10736
normal! zo
10738
normal! zo
10741
normal! zo
10744
normal! zo
10749
normal! zo
10760
normal! zo
10767
normal! zo
10771
normal! zo
10772
normal! zo
10772
normal! zo
10774
normal! zo
10775
normal! zo
10775
normal! zo
10777
normal! zo
10778
normal! zo
10778
normal! zo
10780
normal! zo
10781
normal! zo
10781
normal! zo
10783
normal! zo
10784
normal! zo
10784
normal! zo
10786
normal! zo
10787
normal! zo
10787
normal! zo
10789
normal! zo
10790
normal! zo
10790
normal! zo
10792
normal! zo
10795
normal! zo
10797
normal! zo
10797
normal! zo
10797
normal! zo
10803
normal! zo
10804
normal! zo
10804
normal! zo
10806
normal! zo
10807
normal! zo
10807
normal! zo
10831
normal! zo
10835
normal! zo
10838
normal! zo
10839
normal! zo
10839
normal! zo
10839
normal! zo
10839
normal! zo
10839
normal! zo
10839
normal! zo
10844
normal! zo
10845
normal! zo
10845
normal! zo
10845
normal! zo
10848
normal! zo
10960
normal! zo
11036
normal! zo
11044
normal! zo
11051
normal! zo
11051
normal! zo
11051
normal! zo
11051
normal! zo
11051
normal! zo
11051
normal! zo
11051
normal! zo
11062
normal! zo
11066
normal! zo
11067
normal! zo
11067
normal! zo
11067
normal! zo
11077
normal! zo
11080
normal! zo
11087
normal! zo
11096
normal! zo
11105
normal! zo
11215
normal! zo
11216
normal! zc
11229
normal! zo
11229
normal! zo
11229
normal! zo
11229
normal! zo
11238
normal! zc
11241
normal! zo
11254
normal! zo
11267
normal! zo
11274
normal! zo
11276
normal! zo
11276
normal! zo
11276
normal! zo
11276
normal! zo
11276
normal! zo
11276
normal! zo
11284
normal! zc
11301
normal! zo
11329
normal! zo
11341
normal! zo
11342
normal! zo
11342
normal! zo
11342
normal! zo
11342
normal! zo
11301
normal! zc
11347
normal! zo
11347
normal! zc
11398
normal! zo
11398
normal! zc
11513
normal! zo
11521
normal! zo
11521
normal! zo
11521
normal! zo
11521
normal! zo
11513
normal! zc
11529
normal! zc
11535
normal! zo
11535
normal! zc
11546
normal! zo
11546
normal! zc
11563
normal! zo
11563
normal! zo
11567
normal! zo
11572
normal! zo
11572
normal! zo
11574
normal! zo
11575
normal! zo
11575
normal! zo
11580
normal! zo
11580
normal! zo
11580
normal! zo
11580
normal! zo
11580
normal! zo
11580
normal! zc
11593
normal! zo
11596
normal! zo
11596
normal! zo
11596
normal! zo
11596
normal! zo
11602
normal! zo
11602
normal! zo
11602
normal! zo
11602
normal! zo
11602
normal! zo
11602
normal! zc
11630
normal! zo
11668
normal! zc
11675
normal! zc
11683
normal! zo
11683
normal! zc
11691
normal! zc
11699
normal! zc
11713
normal! zo
11713
normal! zc
11731
normal! zo
11731
normal! zo
11731
normal! zo
11731
normal! zo
11731
normal! zo
11731
normal! zo
11731
normal! zo
11731
normal! zo
11731
normal! zo
11731
normal! zo
11731
normal! zc
11752
normal! zo
11752
normal! zo
11752
normal! zo
11752
normal! zo
11752
normal! zo
11752
normal! zo
11793
normal! zo
11794
normal! zo
11816
normal! zo
11816
normal! zc
11923
normal! zo
11923
normal! zc
11972
normal! zo
11972
normal! zo
11974
normal! zo
11984
normal! zo
11972
normal! zc
12067
normal! zo
12067
normal! zc
12121
normal! zo
12121
normal! zo
12121
normal! zo
12121
normal! zc
12121
normal! zc
12135
normal! zo
12172
normal! zo
12183
normal! zo
12188
normal! zo
12206
normal! zo
12206
normal! zo
12206
normal! zo
12206
normal! zo
12207
normal! zo
12212
normal! zo
12228
normal! zo
12228
normal! zo
12228
normal! zo
12228
normal! zo
12237
normal! zo
12237
normal! zo
12237
normal! zo
12237
normal! zo
12237
normal! zo
12261
normal! zo
12285
normal! zo
12285
normal! zc
12326
normal! zo
12326
normal! zo
12326
normal! zo
12326
normal! zo
12388
normal! zo
12404
normal! zo
12404
normal! zc
12428
normal! zo
12428
normal! zo
12428
normal! zo
12428
normal! zc
12453
normal! zo
12453
normal! zo
12453
normal! zo
12453
normal! zc
12528
normal! zo
12528
normal! zo
12528
normal! zo
12528
normal! zo
12528
normal! zo
12528
normal! zo
12528
normal! zo
12528
normal! zo
12528
normal! zc
12544
normal! zo
12544
normal! zc
12566
normal! zo
12566
normal! zc
12587
normal! zo
12587
normal! zo
12587
normal! zo
12587
normal! zo
12587
normal! zo
12587
normal! zo
12587
normal! zo
12587
normal! zc
12587
normal! zc
12707
normal! zo
12707
normal! zo
12707
normal! zo
12707
normal! zo
12707
normal! zo
12707
normal! zc
12975
normal! zo
12975
normal! zc
13005
normal! zo
13005
normal! zo
13005
normal! zo
13005
normal! zo
13005
normal! zo
13005
normal! zo
13005
normal! zo
13005
normal! zo
13020
normal! zo
13035
normal! zo
13037
normal! zo
13059
normal! zo
13067
normal! zo
13067
normal! zc
13083
normal! zo
13083
normal! zo
13122
normal! zo
13184
normal! zo
13185
normal! zo
13203
normal! zo
13245
normal! zo
13246
normal! zo
13274
normal! zo
13306
normal! zo
13307
normal! zo
13335
normal! zo
13371
normal! zo
13372
normal! zo
13390
normal! zo
13417
normal! zc
13427
normal! zo
13427
normal! zc
13447
normal! zo
13448
normal! zo
13449
normal! zo
13447
normal! zc
13503
normal! zo
13503
normal! zc
13561
normal! zo
13561
normal! zo
13561
normal! zo
13571
normal! zo
13576
normal! zo
13577
normal! zo
13578
normal! zo
13578
normal! zo
13578
normal! zo
13578
normal! zo
13578
normal! zo
13578
normal! zo
13578
normal! zo
13578
normal! zo
13578
normal! zo
13578
normal! zo
13584
normal! zo
13585
normal! zo
13586
normal! zo
13586
normal! zo
13586
normal! zo
13586
normal! zo
13586
normal! zo
13586
normal! zo
13586
normal! zo
13588
normal! zo
13588
normal! zo
13588
normal! zo
13588
normal! zo
13588
normal! zo
13588
normal! zo
13588
normal! zo
13588
normal! zo
13590
normal! zo
13591
normal! zo
13591
normal! zo
13591
normal! zo
13591
normal! zo
13591
normal! zo
13591
normal! zo
13591
normal! zo
13591
normal! zo
13591
normal! zo
13594
normal! zo
13596
normal! zo
13596
normal! zo
13601
normal! zo
13601
normal! zo
13611
normal! zo
13612
normal! zo
13612
normal! zo
13612
normal! zo
13612
normal! zo
13612
normal! zo
13612
normal! zo
13619
normal! zo
13619
normal! zo
13619
normal! zo
13625
normal! zo
13626
normal! zo
13635
normal! zo
13636
normal! zo
13636
normal! zo
13636
normal! zo
13636
normal! zo
13640
normal! zo
13640
normal! zo
13640
normal! zo
13648
normal! zo
13649
normal! zo
13651
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
13664
normal! zo
13664
normal! zo
13664
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
13674
normal! zo
13675
normal! zo
13676
normal! zo
13677
normal! zo
13677
normal! zo
13678
normal! zo
13690
normal! zo
13691
normal! zo
13691
normal! zo
13691
normal! zo
13698
normal! zo
13699
normal! zo
13700
normal! zo
13700
normal! zo
13701
normal! zo
13712
normal! zo
13713
normal! zo
13714
normal! zo
13714
normal! zo
13715
normal! zo
13730
normal! zo
13731
normal! zo
13732
normal! zo
13733
normal! zo
13733
normal! zo
13734
normal! zo
13746
normal! zo
13747
normal! zo
13747
normal! zo
13747
normal! zo
13748
normal! zo
13754
normal! zo
13755
normal! zo
13756
normal! zo
13756
normal! zo
13757
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
13786
normal! zo
13786
normal! zo
13786
normal! zo
13807
normal! zo
13812
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
13814
normal! zo
13814
normal! zo
13814
normal! zo
13820
normal! zo
13821
normal! zo
13822
normal! zo
13822
normal! zo
13822
normal! zo
13822
normal! zo
13822
normal! zo
13822
normal! zo
13822
normal! zo
13824
normal! zo
13824
normal! zo
13824
normal! zo
13824
normal! zo
13824
normal! zo
13824
normal! zo
13824
normal! zo
13824
normal! zo
13826
normal! zo
13827
normal! zo
13827
normal! zo
13827
normal! zo
13827
normal! zo
13827
normal! zo
13827
normal! zo
13827
normal! zo
13827
normal! zo
13827
normal! zo
13830
normal! zo
13832
normal! zo
13837
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
13854
normal! zo
13856
normal! zo
13857
normal! zo
13858
normal! zo
13858
normal! zo
13859
normal! zo
13869
normal! zo
13870
normal! zo
13871
normal! zo
13871
normal! zo
13872
normal! zo
13886
normal! zo
13887
normal! zo
13888
normal! zo
13889
normal! zo
13889
normal! zo
13890
normal! zo
13900
normal! zo
13901
normal! zo
13902
normal! zo
13902
normal! zo
13903
normal! zo
13917
normal! zo
13917
normal! zo
13917
normal! zo
13928
normal! zo
13933
normal! zo
13934
normal! zo
13935
normal! zo
13935
normal! zo
13935
normal! zo
13935
normal! zo
13935
normal! zo
13935
normal! zo
13935
normal! zo
13935
normal! zo
13935
normal! zo
13935
normal! zo
13941
normal! zo
13942
normal! zo
13943
normal! zo
13943
normal! zo
13943
normal! zo
13943
normal! zo
13943
normal! zo
13943
normal! zo
13943
normal! zo
13945
normal! zo
13945
normal! zo
13945
normal! zo
13945
normal! zo
13945
normal! zo
13945
normal! zo
13945
normal! zo
13945
normal! zo
13947
normal! zo
13948
normal! zo
13948
normal! zo
13948
normal! zo
13948
normal! zo
13948
normal! zo
13948
normal! zo
13948
normal! zo
13948
normal! zo
13948
normal! zo
13951
normal! zo
13953
normal! zo
13958
normal! zo
13967
normal! zo
13968
normal! zo
13968
normal! zo
13968
normal! zo
13968
normal! zo
13968
normal! zo
13968
normal! zo
13968
normal! zo
13975
normal! zo
13980
normal! zo
13981
normal! zo
13982
normal! zo
13989
normal! zo
13990
normal! zo
13991
normal! zo
13997
normal! zo
13998
normal! zo
13999
normal! zo
14004
normal! zo
14005
normal! zo
14006
normal! zo
14006
normal! zo
14016
normal! zo
14017
normal! zo
14018
normal! zo
14018
normal! zo
14018
normal! zo
14018
normal! zo
14018
normal! zo
14018
normal! zo
14025
normal! zo
14026
normal! zo
14026
normal! zo
14026
normal! zo
14026
normal! zo
14026
normal! zo
14026
normal! zo
14026
normal! zo
14033
normal! zo
14034
normal! zo
14034
normal! zo
14034
normal! zo
14034
normal! zo
14034
normal! zo
14034
normal! zo
14034
normal! zo
14040
normal! zo
14041
normal! zo
14041
normal! zo
14041
normal! zo
14041
normal! zo
14041
normal! zo
14041
normal! zo
14041
normal! zo
14051
normal! zo
14057
normal! zo
14057
normal! zo
14063
normal! zo
14069
normal! zo
14075
normal! zo
14075
normal! zo
14075
normal! zo
14075
normal! zo
14075
normal! zo
14075
normal! zo
14075
normal! zo
14075
normal! zo
14075
normal! zo
14085
normal! zo
14085
normal! zo
14085
normal! zo
14085
normal! zo
14085
normal! zo
14085
normal! zo
14087
normal! zo
14088
normal! zo
14088
normal! zo
14088
normal! zo
14094
normal! zo
14094
normal! zo
14094
normal! zo
14094
normal! zo
14094
normal! zo
14094
normal! zo
14094
normal! zo
14094
normal! zo
14094
normal! zo
14105
normal! zo
14105
normal! zo
14105
normal! zo
14105
normal! zo
14105
normal! zo
14105
normal! zo
14107
normal! zo
14108
normal! zo
14108
normal! zo
14108
normal! zo
14114
normal! zo
14114
normal! zo
14114
normal! zo
14114
normal! zo
14122
normal! zo
14127
normal! zo
14130
normal! zo
14135
normal! zo
14136
normal! zo
14137
normal! zo
14137
normal! zo
14137
normal! zo
14137
normal! zo
14137
normal! zo
14137
normal! zo
14137
normal! zo
14137
normal! zo
14137
normal! zo
14137
normal! zo
14143
normal! zo
14144
normal! zo
14147
normal! zo
14148
normal! zo
14148
normal! zo
14148
normal! zo
14148
normal! zo
14148
normal! zo
14148
normal! zo
14148
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
14150
normal! zo
14150
normal! zo
14152
normal! zo
14153
normal! zo
14156
normal! zo
14156
normal! zo
14156
normal! zo
14156
normal! zo
14156
normal! zo
14156
normal! zo
14156
normal! zo
14156
normal! zo
14156
normal! zo
14159
normal! zo
14160
normal! zo
14164
normal! zo
14164
normal! zo
14169
normal! zo
14169
normal! zo
14174
normal! zo
14175
normal! zo
14182
normal! zo
14183
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
14193
normal! zo
14194
normal! zo
14195
normal! zo
14196
normal! zo
14202
normal! zo
14203
normal! zo
14204
normal! zo
14210
normal! zo
14211
normal! zo
14211
normal! zo
14212
normal! zo
14217
normal! zo
14218
normal! zo
14218
normal! zo
14219
normal! zo
14228
normal! zo
14229
normal! zo
14230
normal! zo
14230
normal! zo
14230
normal! zo
14230
normal! zo
14230
normal! zo
14230
normal! zo
14237
normal! zo
14238
normal! zo
14239
normal! zo
14245
normal! zo
14246
normal! zo
14246
normal! zo
14246
normal! zo
14246
normal! zo
14246
normal! zo
14246
normal! zo
14246
normal! zo
14252
normal! zo
14253
normal! zo
14253
normal! zo
14253
normal! zo
14253
normal! zo
14253
normal! zo
14253
normal! zo
14253
normal! zo
14264
normal! zo
14265
normal! zo
14265
normal! zo
14271
normal! zo
14277
normal! zo
14277
normal! zo
14283
normal! zo
14283
normal! zo
14283
normal! zo
14283
normal! zo
14299
normal! zo
14304
normal! zo
14305
normal! zo
14306
normal! zo
14306
normal! zo
14306
normal! zo
14306
normal! zo
14306
normal! zo
14306
normal! zo
14306
normal! zo
14306
normal! zo
14306
normal! zo
14306
normal! zo
14312
normal! zo
14313
normal! zo
14314
normal! zo
14314
normal! zo
14314
normal! zo
14314
normal! zo
14314
normal! zo
14314
normal! zo
14314
normal! zo
14316
normal! zo
14316
normal! zo
14316
normal! zo
14316
normal! zo
14316
normal! zo
14316
normal! zo
14316
normal! zo
14316
normal! zo
14316
normal! zo
14318
normal! zo
14319
normal! zo
14319
normal! zo
14319
normal! zo
14319
normal! zo
14319
normal! zo
14319
normal! zo
14319
normal! zo
14319
normal! zo
14319
normal! zo
14322
normal! zo
14324
normal! zo
14324
normal! zo
14329
normal! zo
14329
normal! zo
14339
normal! zo
14340
normal! zo
14340
normal! zo
14340
normal! zo
14340
normal! zo
14340
normal! zo
14340
normal! zo
14347
normal! zo
14348
normal! zo
14349
normal! zo
14350
normal! zo
14355
normal! zo
14356
normal! zo
14357
normal! zo
14367
normal! zo
14368
normal! zo
14369
normal! zo
14369
normal! zo
14369
normal! zo
14369
normal! zo
14369
normal! zo
14369
normal! zo
14374
normal! zo
14375
normal! zo
14375
normal! zo
14375
normal! zo
14376
normal! zo
14386
normal! zo
14387
normal! zo
14387
normal! zo
14393
normal! zo
14394
normal! zo
14394
normal! zo
14400
normal! zo
14400
normal! zo
14400
normal! zo
14400
normal! zo
14412
normal! zo
14417
normal! zo
14418
normal! zo
14419
normal! zo
14419
normal! zo
14419
normal! zo
14419
normal! zo
14419
normal! zo
14419
normal! zo
14419
normal! zo
14419
normal! zo
14419
normal! zo
14419
normal! zo
14425
normal! zo
14426
normal! zo
14427
normal! zo
14427
normal! zo
14427
normal! zo
14427
normal! zo
14427
normal! zo
14427
normal! zo
14427
normal! zo
14429
normal! zo
14429
normal! zo
14429
normal! zo
14429
normal! zo
14429
normal! zo
14429
normal! zo
14429
normal! zo
14429
normal! zo
14429
normal! zo
14431
normal! zo
14432
normal! zo
14432
normal! zo
14432
normal! zo
14432
normal! zo
14432
normal! zo
14432
normal! zo
14432
normal! zo
14432
normal! zo
14432
normal! zo
14435
normal! zo
14437
normal! zo
14437
normal! zo
14442
normal! zo
14442
normal! zo
14452
normal! zo
14453
normal! zo
14453
normal! zo
14453
normal! zo
14453
normal! zo
14453
normal! zo
14453
normal! zo
14460
normal! zo
14467
normal! zo
14468
normal! zo
14470
normal! zo
14470
normal! zo
14470
normal! zo
14476
normal! zo
14478
normal! zo
14480
normal! zo
14486
normal! zo
14488
normal! zo
14490
normal! zo
14501
normal! zo
14521
normal! zo
14533
normal! zo
14534
normal! zo
14535
normal! zo
14537
normal! zo
14538
normal! zo
14539
normal! zo
14539
normal! zo
14539
normal! zo
14541
normal! zo
14542
normal! zo
14542
normal! zo
14542
normal! zo
14558
normal! zo
14569
normal! zo
14578
normal! zo
14588
normal! zo
14615
normal! zo
14620
normal! zo
14626
normal! zo
14637
normal! zo
14650
normal! zo
14674
normal! zo
14676
normal! zo
14679
normal! zo
14682
normal! zo
14683
normal! zo
14687
normal! zo
14688
normal! zo
14702
normal! zo
14702
normal! zo
14702
normal! zo
14702
normal! zo
14724
normal! zo
14725
normal! zo
14726
normal! zo
14726
normal! zo
14726
normal! zo
14726
normal! zo
14726
normal! zo
14726
normal! zo
14726
normal! zo
14726
normal! zo
14726
normal! zo
14726
normal! zo
14735
normal! zo
14736
normal! zo
14742
normal! zo
14746
normal! zo
14747
normal! zo
14756
normal! zo
14757
normal! zo
14765
normal! zo
14766
normal! zo
14772
normal! zo
14787
normal! zo
14795
normal! zo
14801
normal! zo
14807
normal! zo
14812
normal! zo
14816
normal! zo
14822
normal! zo
14827
normal! zo
14828
normal! zo
14833
normal! zo
14844
normal! zo
14862
normal! zo
14904
normal! zo
14910
normal! zo
14916
normal! zo
14923
normal! zo
14932
normal! zo
14934
normal! zo
14941
normal! zo
14941
normal! zo
14941
normal! zo
14941
normal! zo
14941
normal! zo
14941
normal! zo
14958
normal! zo
14970
normal! zo
14981
normal! zo
14982
normal! zo
14998
normal! zo
15015
normal! zo
15019
normal! zo
15020
normal! zo
15021
normal! zo
15021
normal! zo
15023
normal! zo
15026
normal! zo
15039
normal! zo
15049
normal! zo
15051
normal! zo
15055
normal! zo
15056
normal! zo
15056
normal! zo
15056
normal! zo
15056
normal! zo
15056
normal! zo
15056
normal! zo
15069
normal! zo
15090
normal! zo
15091
normal! zo
15098
normal! zo
15131
normal! zo
15132
normal! zo
15132
normal! zo
15148
normal! zo
15154
normal! zo
15157
normal! zo
15157
normal! zo
15157
normal! zo
15163
normal! zo
15163
normal! zo
15183
normal! zo
15188
normal! zo
15193
normal! zo
15201
normal! zo
15220
normal! zo
15254
normal! zo
15262
normal! zo
15271
normal! zo
15290
normal! zo
15292
normal! zo
15296
normal! zo
15313
normal! zo
15319
normal! zo
15323
normal! zo
15362
normal! zo
15466
normal! zo
15466
normal! zo
15542
normal! zo
15542
normal! zo
15542
normal! zo
15655
normal! zo
15686
normal! zo
15710
normal! zo
15720
normal! zo
15720
normal! zo
15720
normal! zo
15720
normal! zo
15720
normal! zo
15908
normal! zo
15927
normal! zo
15949
normal! zo
15954
normal! zo
15955
normal! zo
15955
normal! zo
15958
normal! zo
15959
normal! zo
15959
normal! zo
15959
normal! zo
15962
normal! zo
15962
normal! zo
15962
normal! zo
15966
normal! zo
15966
normal! zo
15966
normal! zo
15966
normal! zo
15966
normal! zo
15966
normal! zo
15966
normal! zo
15966
normal! zo
15966
normal! zo
16271
normal! zo
16429
normal! zo
16497
normal! zo
16533
normal! zo
16548
normal! zo
16554
normal! zo
16557
normal! zo
16565
normal! zo
16566
normal! zo
16566
normal! zo
16566
normal! zo
16566
normal! zo
16566
normal! zo
16570
normal! zo
16578
normal! zo
16581
normal! zo
16587
normal! zo
16593
normal! zo
16596
normal! zo
16602
normal! zo
16616
normal! zo
16622
normal! zo
16627
normal! zo
16630
normal! zo
16630
normal! zo
16630
normal! zo
16640
normal! zo
16655
normal! zo
16666
normal! zo
16666
normal! zo
16677
normal! zo
16692
normal! zo
16702
normal! zo
16713
normal! zo
16721
normal! zo
16726
normal! zo
16742
normal! zo
16780
normal! zo
16811
normal! zo
16832
normal! zo
16851
normal! zo
16859
normal! zo
16860
normal! zo
16869
normal! zo
16885
normal! zo
16905
normal! zo
16910
normal! zo
16923
normal! zo
16923
normal! zo
16923
normal! zo
16923
normal! zo
16923
normal! zo
16923
normal! zo
16923
normal! zo
16923
normal! zo
16923
normal! zo
16923
normal! zo
17002
normal! zo
17015
normal! zo
17016
normal! zo
17017
normal! zo
17023
normal! zo
17027
normal! zo
17029
normal! zo
17044
normal! zo
17060
normal! zo
17068
normal! zo
17072
normal! zo
17077
normal! zo
17085
normal! zo
17090
normal! zo
17098
normal! zo
17103
normal! zo
17123
normal! zo
17138
normal! zo
17139
normal! zo
17155
normal! zo
17192
normal! zo
17206
normal! zo
17209
normal! zo
17213
normal! zo
17214
normal! zo
17233
normal! zo
17248
normal! zo
17255
normal! zo
17256
normal! zo
17262
normal! zo
17269
normal! zo
17274
normal! zo
17302
normal! zo
17322
normal! zo
17323
normal! zo
17345
normal! zo
17359
normal! zo
17366
normal! zo
17367
normal! zo
17381
normal! zo
17417
normal! zo
17438
normal! zo
17461
normal! zo
17474
normal! zo
17498
normal! zo
17503
normal! zo
17527
normal! zo
17545
normal! zo
17563
normal! zo
17564
normal! zo
17575
normal! zo
17599
normal! zo
17612
normal! zo
17616
normal! zo
17616
normal! zo
17616
normal! zo
17616
normal! zo
17616
normal! zo
17630
normal! zo
17630
normal! zo
17630
normal! zo
17630
normal! zo
17630
normal! zo
17630
normal! zo
17630
normal! zo
17744
normal! zo
17752
normal! zo
17774
normal! zo
17797
normal! zo
17862
normal! zo
17919
normal! zo
17934
normal! zo
17968
normal! zo
17982
normal! zo
18008
normal! zo
18028
normal! zo
18040
normal! zo
18040
normal! zo
18040
normal! zo
18040
normal! zo
18040
normal! zo
18043
normal! zo
18050
normal! zo
18053
normal! zo
18064
normal! zo
18070
normal! zo
18075
normal! zo
18086
normal! zo
18105
normal! zo
18148
normal! zo
18173
normal! zo
18229
normal! zo
18238
normal! zo
18683
normal! zo
18755
normal! zo
18761
normal! zo
18764
normal! zo
18777
normal! zo
18794
normal! zo
18804
normal! zo
18807
normal! zo
18808
normal! zo
18808
normal! zo
18814
normal! zo
18821
normal! zo
19073
normal! zo
19119
normal! zo
19129
normal! zo
19130
normal! zo
19130
normal! zo
19130
normal! zo
19130
normal! zo
19130
normal! zo
20020
normal! zo
20028
normal! zo
20062
normal! zo
20074
normal! zo
20079
normal! zo
20086
normal! zo
20098
normal! zo
20116
normal! zo
20126
normal! zo
20337
normal! zo
20408
normal! zo
20409
normal! zo
20421
normal! zo
20436
normal! zo
20443
normal! zo
20450
normal! zo
20457
normal! zo
20464
normal! zo
20471
normal! zo
20478
normal! zo
20484
normal! zo
20603
normal! zo
20621
normal! zo
20650
normal! zo
20666
normal! zo
20676
normal! zo
20687
normal! zo
20698
normal! zo
20715
normal! zo
20715
normal! zo
20715
normal! zo
20715
normal! zo
20715
normal! zo
20715
normal! zo
20715
normal! zo
20715
normal! zo
20715
normal! zo
20735
normal! zo
20735
normal! zo
20735
normal! zo
20735
normal! zo
20735
normal! zo
20735
normal! zo
20735
normal! zo
20735
normal! zo
20755
normal! zo
20803
normal! zo
20815
normal! zo
20816
normal! zo
20824
normal! zo
20841
normal! zo
20841
normal! zo
20841
normal! zo
20841
normal! zo
20841
normal! zo
20841
normal! zo
20841
normal! zo
let s:l = 16796 - ((17 * winheight(0) + 12) / 24)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
16796
normal! 0
lcd ~/Geotexan/src/Geotex-INN
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
298
normal! zo
398
normal! zo
400
normal! zo
400
normal! zo
400
normal! zo
400
normal! zo
400
normal! zo
400
normal! zo
602
normal! zo
602
normal! zo
602
normal! zo
602
normal! zo
602
normal! zo
608
normal! zo
608
normal! zo
608
normal! zo
608
normal! zo
608
normal! zo
608
normal! zo
658
normal! zo
3685
normal! zo
3709
normal! zo
3709
normal! zo
3709
normal! zo
3709
normal! zo
3719
normal! zo
3720
normal! zo
3720
normal! zo
3720
normal! zo
3723
normal! zo
3724
normal! zo
3728
normal! zo
3737
normal! zo
3885
normal! zo
3909
normal! zo
3919
normal! zo
3932
normal! zo
let s:l = 3714 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3714
normal! 07|
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
50
normal! zo
50
normal! zo
50
normal! zo
52
normal! zo
52
normal! zo
141
normal! zo
163
normal! zo
168
normal! zo
184
normal! zo
185
normal! zo
185
normal! zo
185
normal! zo
185
normal! zo
185
normal! zo
195
normal! zo
199
normal! zo
205
normal! zo
219
normal! zo
219
normal! zo
219
normal! zo
219
normal! zo
219
normal! zo
219
normal! zo
231
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
242
normal! zo
249
normal! zo
250
normal! zo
250
normal! zo
250
normal! zo
250
normal! zo
272
normal! zo
286
normal! zo
290
normal! zo
291
normal! zo
292
normal! zo
296
normal! zo
318
normal! zo
323
normal! zo
356
normal! zo
362
normal! zo
362
normal! zo
362
normal! zo
362
normal! zo
362
normal! zo
364
normal! zo
364
normal! zo
364
normal! zo
364
normal! zo
364
normal! zo
365
normal! zo
398
normal! zo
415
normal! zo
421
normal! zo
426
normal! zo
439
normal! zo
445
normal! zo
let s:l = 63 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
63
normal! 073|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/utils.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
90
normal! zo
108
normal! zo
let s:l = 116 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
116
normal! 035|
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
59
normal! zo
60
normal! zo
73
normal! zo
73
normal! zo
73
normal! zo
85
normal! zo
85
normal! zo
85
normal! zo
85
normal! zo
85
normal! zo
85
normal! zo
85
normal! zo
85
normal! zo
85
normal! zo
98
normal! zo
98
normal! zo
98
normal! zo
98
normal! zo
98
normal! zo
98
normal! zo
98
normal! zo
100
normal! zo
100
normal! zo
100
normal! zo
100
normal! zo
100
normal! zo
100
normal! zo
100
normal! zo
116
normal! zo
117
normal! zo
117
normal! zo
117
normal! zo
117
normal! zo
117
normal! zo
117
normal! zo
117
normal! zo
117
normal! zo
117
normal! zo
156
normal! zo
181
normal! zo
219
normal! zo
232
normal! zo
243
normal! zo
267
normal! zo
280
normal! zo
297
normal! zo
301
normal! zo
302
normal! zo
302
normal! zo
325
normal! zo
326
normal! zo
326
normal! zo
344
normal! zo
345
normal! zo
350
normal! zo
351
normal! zo
356
normal! zo
365
normal! zo
368
normal! zo
369
normal! zo
369
normal! zo
369
normal! zo
369
normal! zo
369
normal! zo
369
normal! zo
419
normal! zo
420
normal! zo
421
normal! zo
421
normal! zo
424
normal! zo
425
normal! zo
425
normal! zo
425
normal! zo
425
normal! zo
438
normal! zo
439
normal! zo
440
normal! zo
440
normal! zo
443
normal! zo
444
normal! zo
444
normal! zo
444
normal! zo
444
normal! zo
448
normal! zo
453
normal! zo
453
normal! zo
453
normal! zo
453
normal! zo
456
normal! zo
457
normal! zo
478
normal! zo
478
normal! zo
478
normal! zo
478
normal! zo
487
normal! zo
488
normal! zo
488
normal! zo
488
normal! zo
488
normal! zo
497
normal! zo
502
normal! zo
502
normal! zo
502
normal! zo
502
normal! zo
505
normal! zo
505
normal! zo
505
normal! zo
505
normal! zo
510
normal! zo
546
normal! zo
555
normal! zo
555
normal! zo
555
normal! zo
555
normal! zo
561
normal! zo
721
normal! zo
727
normal! zo
727
normal! zo
727
normal! zo
727
normal! zo
727
normal! zo
748
normal! zo
754
normal! zo
754
normal! zo
775
normal! zo
790
normal! zo
791
normal! zo
792
normal! zo
792
normal! zo
792
normal! zo
792
normal! zo
792
normal! zo
792
normal! zo
796
normal! zo
796
normal! zo
796
normal! zo
806
normal! zo
816
normal! zo
816
normal! zo
824
normal! zo
838
normal! zo
839
normal! zo
845
normal! zo
876
normal! zo
896
normal! zo
896
normal! zo
896
normal! zo
896
normal! zo
896
normal! zo
907
normal! zo
989
normal! zo
996
normal! zo
1003
normal! zo
1041
normal! zo
1047
normal! zo
1048
normal! zo
1049
normal! zo
1074
normal! zo
1094
normal! zo
1105
normal! zo
1105
normal! zo
1105
normal! zo
1105
normal! zo
1105
normal! zo
1105
normal! zo
1105
normal! zo
1134
normal! zo
let s:l = 1020 - ((0 * winheight(0) + 4) / 8)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1020
normal! 05|
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
47
normal! zo
69
normal! zo
77
normal! zo
87
normal! zo
91
normal! zo
110
normal! zo
115
normal! zo
152
normal! zo
163
normal! zo
176
normal! zo
185
normal! zo
195
normal! zo
203
normal! zo
203
normal! zo
203
normal! zo
203
normal! zo
203
normal! zo
231
normal! zo
241
normal! zo
245
normal! zo
254
normal! zo
264
normal! zo
279
normal! zo
279
normal! zo
288
normal! zo
297
normal! zo
297
normal! zo
297
normal! zo
297
normal! zo
297
normal! zo
297
normal! zo
297
normal! zo
314
normal! zo
315
normal! zo
let s:l = 53 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
53
normal! 0
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
173
normal! zo
173
normal! zo
173
normal! zo
173
normal! zo
173
normal! zo
173
normal! zo
173
normal! zo
367
normal! zo
let s:l = 173 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
173
normal! 037|
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
let s:l = 1140 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1140
normal! 012|
wincmd w
4wincmd w
exe '1resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 1resize ' . ((&columns * 34 + 57) / 115)
exe '2resize ' . ((&lines * 47 + 25) / 51)
exe 'vert 2resize ' . ((&columns * 34 + 57) / 115)
exe '3resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 3resize ' . ((&columns * 80 + 57) / 115)
exe '4resize ' . ((&lines * 24 + 25) / 51)
exe 'vert 4resize ' . ((&columns * 80 + 57) / 115)
exe '5resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 5resize ' . ((&columns * 80 + 57) / 115)
exe '6resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 6resize ' . ((&columns * 80 + 57) / 115)
exe '7resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 7resize ' . ((&columns * 80 + 57) / 115)
exe '8resize ' . ((&lines * 8 + 25) / 51)
exe 'vert 8resize ' . ((&columns * 80 + 57) / 115)
exe '9resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 9resize ' . ((&columns * 80 + 57) / 115)
exe '10resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 10resize ' . ((&columns * 80 + 57) / 115)
exe '11resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 11resize ' . ((&columns * 80 + 57) / 115)
exe '12resize ' . ((&lines * 1 + 25) / 51)
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
4wincmd w

" vim: ft=vim ro nowrap smc=128
