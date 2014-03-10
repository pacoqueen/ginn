" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 10 marzo 2014 at 22:33:37.
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
badd +663 ginn/formularios/consulta_producido.py
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
set lines=63 columns=110
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
exe '1resize ' . ((&lines * 3 + 31) / 63)
exe 'vert 1resize ' . ((&columns * 29 + 55) / 110)
exe '2resize ' . ((&lines * 57 + 31) / 63)
exe 'vert 2resize ' . ((&columns * 29 + 55) / 110)
exe '3resize ' . ((&lines * 1 + 31) / 63)
exe 'vert 3resize ' . ((&columns * 80 + 55) / 110)
exe '4resize ' . ((&lines * 17 + 31) / 63)
exe 'vert 4resize ' . ((&columns * 80 + 55) / 110)
exe '5resize ' . ((&lines * 1 + 31) / 63)
exe 'vert 5resize ' . ((&columns * 80 + 55) / 110)
exe '6resize ' . ((&lines * 1 + 31) / 63)
exe 'vert 6resize ' . ((&columns * 80 + 55) / 110)
exe '7resize ' . ((&lines * 12 + 31) / 63)
exe 'vert 7resize ' . ((&columns * 80 + 55) / 110)
exe '8resize ' . ((&lines * 1 + 31) / 63)
exe 'vert 8resize ' . ((&columns * 80 + 55) / 110)
exe '9resize ' . ((&lines * 1 + 31) / 63)
exe 'vert 9resize ' . ((&columns * 80 + 55) / 110)
exe '10resize ' . ((&lines * 1 + 31) / 63)
exe 'vert 10resize ' . ((&columns * 80 + 55) / 110)
exe '11resize ' . ((&lines * 1 + 31) / 63)
exe 'vert 11resize ' . ((&columns * 80 + 55) / 110)
exe '12resize ' . ((&lines * 16 + 31) / 63)
exe 'vert 12resize ' . ((&columns * 80 + 55) / 110)
argglobal
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 1 - ((0 * winheight(0) + 1) / 3)
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
9373
normal! zo
9380
normal! zo
9384
normal! zo
9389
normal! zo
9404
normal! zo
9452
normal! zo
9493
normal! zo
9514
normal! zo
9755
normal! zo
9781
normal! zo
9820
normal! zo
9831
normal! zo
9832
normal! zo
9845
normal! zo
9858
normal! zo
9873
normal! zo
9874
normal! zo
9878
normal! zo
9878
normal! zo
9880
normal! zo
9886
normal! zo
9889
normal! zo
9897
normal! zo
9913
normal! zo
9930
normal! zo
9930
normal! zo
9930
normal! zo
9930
normal! zo
9930
normal! zo
9930
normal! zo
9930
normal! zo
9930
normal! zo
9930
normal! zo
9937
normal! zo
9951
normal! zo
9952
normal! zo
9952
normal! zo
9954
normal! zo
9955
normal! zo
9955
normal! zo
9957
normal! zo
9958
normal! zo
9958
normal! zo
9960
normal! zo
9961
normal! zo
9961
normal! zo
9963
normal! zo
9966
normal! zo
9968
normal! zo
9968
normal! zo
9968
normal! zo
9977
normal! zo
9990
normal! zo
9993
normal! zo
9994
normal! zo
9994
normal! zo
9997
normal! zo
9997
normal! zo
9997
normal! zo
10000
normal! zo
10000
normal! zo
10000
normal! zo
10000
normal! zo
10006
normal! zo
10009
normal! zo
10013
normal! zo
10020
normal! zo
10022
normal! zo
10069
normal! zo
10083
normal! zo
10084
normal! zo
10086
normal! zo
10121
normal! zo
10128
normal! zo
10133
normal! zo
10134
normal! zo
10139
normal! zo
10139
normal! zo
10139
normal! zo
10139
normal! zo
10139
normal! zo
10142
normal! zo
10142
normal! zo
10142
normal! zo
10168
normal! zo
10177
normal! zo
10182
normal! zo
10184
normal! zo
10189
normal! zo
10195
normal! zo
10203
normal! zo
10204
normal! zo
10204
normal! zo
10204
normal! zo
10204
normal! zo
10213
normal! zo
10214
normal! zo
10219
normal! zo
10268
normal! zo
10273
normal! zo
10386
normal! zo
10413
normal! zo
10418
normal! zo
10424
normal! zo
10510
normal! zo
10517
normal! zo
10518
normal! zo
10566
normal! zo
10566
normal! zo
10566
normal! zo
10566
normal! zo
10566
normal! zo
10569
normal! zo
10577
normal! zo
10578
normal! zo
10623
normal! zo
10643
normal! zo
10644
normal! zo
10645
normal! zo
10645
normal! zo
10645
normal! zo
10645
normal! zo
10645
normal! zo
10645
normal! zo
10645
normal! zo
10645
normal! zo
10645
normal! zo
10662
normal! zo
10668
normal! zo
10678
normal! zo
10693
normal! zo
10696
normal! zo
10699
normal! zo
10699
normal! zo
10699
normal! zo
10702
normal! zo
10702
normal! zo
10702
normal! zo
10702
normal! zo
10707
normal! zo
10707
normal! zo
10707
normal! zo
10715
normal! zo
10722
normal! zo
10729
normal! zo
10732
normal! zo
10734
normal! zo
10737
normal! zo
10740
normal! zo
10745
normal! zo
10756
normal! zo
10763
normal! zo
10767
normal! zo
10768
normal! zo
10768
normal! zo
10770
normal! zo
10771
normal! zo
10771
normal! zo
10773
normal! zo
10774
normal! zo
10774
normal! zo
10776
normal! zo
10777
normal! zo
10777
normal! zo
10779
normal! zo
10780
normal! zo
10780
normal! zo
10782
normal! zo
10783
normal! zo
10783
normal! zo
10785
normal! zo
10786
normal! zo
10786
normal! zo
10788
normal! zo
10791
normal! zo
10793
normal! zo
10793
normal! zo
10793
normal! zo
10799
normal! zo
10800
normal! zo
10800
normal! zo
10802
normal! zo
10803
normal! zo
10803
normal! zo
10827
normal! zo
10831
normal! zo
10834
normal! zo
10835
normal! zo
10835
normal! zo
10835
normal! zo
10835
normal! zo
10835
normal! zo
10835
normal! zo
10840
normal! zo
10841
normal! zo
10841
normal! zo
10841
normal! zo
10844
normal! zo
10956
normal! zo
11032
normal! zo
11040
normal! zo
11047
normal! zo
11047
normal! zo
11047
normal! zo
11047
normal! zo
11047
normal! zo
11047
normal! zo
11047
normal! zo
11058
normal! zo
11062
normal! zo
11063
normal! zo
11063
normal! zo
11063
normal! zo
11073
normal! zo
11076
normal! zo
11083
normal! zo
11092
normal! zo
11101
normal! zo
11211
normal! zo
11212
normal! zc
11225
normal! zo
11225
normal! zo
11225
normal! zo
11225
normal! zo
11234
normal! zc
11237
normal! zo
11250
normal! zo
11263
normal! zo
11270
normal! zo
11272
normal! zo
11272
normal! zo
11272
normal! zo
11272
normal! zo
11272
normal! zo
11272
normal! zo
11280
normal! zc
11297
normal! zo
11325
normal! zo
11337
normal! zo
11338
normal! zo
11338
normal! zo
11338
normal! zo
11338
normal! zo
11297
normal! zc
11343
normal! zo
11343
normal! zc
11394
normal! zo
11394
normal! zc
11509
normal! zo
11517
normal! zo
11517
normal! zo
11517
normal! zo
11517
normal! zo
11509
normal! zc
11525
normal! zc
11531
normal! zo
11531
normal! zc
11542
normal! zo
11542
normal! zc
11559
normal! zo
11559
normal! zo
11563
normal! zo
11568
normal! zo
11568
normal! zo
11570
normal! zo
11571
normal! zo
11571
normal! zo
11576
normal! zo
11576
normal! zo
11576
normal! zo
11576
normal! zo
11576
normal! zo
11576
normal! zc
11589
normal! zo
11592
normal! zo
11592
normal! zo
11592
normal! zo
11592
normal! zo
11598
normal! zo
11598
normal! zo
11598
normal! zo
11598
normal! zo
11598
normal! zo
11598
normal! zc
11626
normal! zo
11664
normal! zc
11671
normal! zc
11679
normal! zo
11679
normal! zc
11687
normal! zc
11695
normal! zc
11709
normal! zo
11709
normal! zc
11727
normal! zo
11727
normal! zo
11727
normal! zo
11727
normal! zo
11727
normal! zo
11727
normal! zo
11727
normal! zo
11727
normal! zo
11727
normal! zo
11727
normal! zo
11727
normal! zc
11748
normal! zo
11748
normal! zo
11748
normal! zo
11748
normal! zo
11748
normal! zo
11748
normal! zo
11789
normal! zo
11790
normal! zo
11812
normal! zo
11812
normal! zc
11919
normal! zo
11919
normal! zc
11968
normal! zo
11968
normal! zo
11970
normal! zo
11980
normal! zo
11968
normal! zc
12063
normal! zo
12063
normal! zc
12117
normal! zo
12117
normal! zo
12117
normal! zo
12117
normal! zc
12117
normal! zc
12131
normal! zo
12168
normal! zo
12179
normal! zo
12184
normal! zo
12202
normal! zo
12202
normal! zo
12202
normal! zo
12202
normal! zo
12203
normal! zo
12208
normal! zo
12224
normal! zo
12224
normal! zo
12224
normal! zo
12224
normal! zo
12233
normal! zo
12233
normal! zo
12233
normal! zo
12233
normal! zo
12233
normal! zo
12257
normal! zo
12281
normal! zo
12281
normal! zc
12322
normal! zo
12322
normal! zo
12322
normal! zo
12322
normal! zo
12384
normal! zo
12400
normal! zo
12400
normal! zc
12424
normal! zo
12424
normal! zo
12424
normal! zo
12424
normal! zc
12449
normal! zo
12449
normal! zo
12449
normal! zo
12449
normal! zc
12524
normal! zo
12524
normal! zo
12524
normal! zo
12524
normal! zo
12524
normal! zo
12524
normal! zo
12524
normal! zo
12524
normal! zo
12524
normal! zc
12540
normal! zo
12540
normal! zc
12562
normal! zo
12562
normal! zc
12583
normal! zo
12583
normal! zo
12583
normal! zo
12583
normal! zo
12583
normal! zo
12583
normal! zo
12583
normal! zo
12583
normal! zc
12583
normal! zc
12703
normal! zo
12703
normal! zo
12703
normal! zo
12703
normal! zo
12703
normal! zo
12703
normal! zc
12971
normal! zo
12971
normal! zc
13001
normal! zo
13001
normal! zo
13001
normal! zo
13001
normal! zo
13001
normal! zo
13001
normal! zo
13001
normal! zo
13001
normal! zo
13016
normal! zo
13031
normal! zo
13033
normal! zo
13055
normal! zo
13063
normal! zo
13063
normal! zc
13079
normal! zo
13079
normal! zo
13118
normal! zo
13180
normal! zo
13181
normal! zo
13199
normal! zo
13241
normal! zo
13242
normal! zo
13270
normal! zo
13302
normal! zo
13303
normal! zo
13331
normal! zo
13367
normal! zo
13368
normal! zo
13386
normal! zo
13413
normal! zc
13423
normal! zo
13423
normal! zc
13443
normal! zo
13444
normal! zo
13445
normal! zo
13443
normal! zc
13499
normal! zo
13499
normal! zc
13557
normal! zo
13557
normal! zo
13557
normal! zo
13567
normal! zo
13572
normal! zo
13573
normal! zo
13574
normal! zo
13574
normal! zo
13574
normal! zo
13574
normal! zo
13574
normal! zo
13574
normal! zo
13574
normal! zo
13574
normal! zo
13574
normal! zo
13574
normal! zo
13580
normal! zo
13581
normal! zo
13582
normal! zo
13582
normal! zo
13582
normal! zo
13582
normal! zo
13582
normal! zo
13582
normal! zo
13582
normal! zo
13584
normal! zo
13584
normal! zo
13584
normal! zo
13584
normal! zo
13584
normal! zo
13584
normal! zo
13584
normal! zo
13584
normal! zo
13586
normal! zo
13587
normal! zo
13587
normal! zo
13587
normal! zo
13587
normal! zo
13587
normal! zo
13587
normal! zo
13587
normal! zo
13587
normal! zo
13587
normal! zo
13590
normal! zo
13592
normal! zo
13592
normal! zo
13597
normal! zo
13597
normal! zo
13607
normal! zo
13608
normal! zo
13608
normal! zo
13608
normal! zo
13608
normal! zo
13608
normal! zo
13608
normal! zo
13615
normal! zo
13615
normal! zo
13615
normal! zo
13621
normal! zo
13622
normal! zo
13631
normal! zo
13632
normal! zo
13632
normal! zo
13632
normal! zo
13632
normal! zo
13636
normal! zo
13636
normal! zo
13636
normal! zo
13644
normal! zo
13645
normal! zo
13647
normal! zo
13655
normal! zo
13656
normal! zo
13656
normal! zo
13656
normal! zo
13656
normal! zo
13660
normal! zo
13660
normal! zo
13660
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
13670
normal! zo
13671
normal! zo
13672
normal! zo
13673
normal! zo
13673
normal! zo
13674
normal! zo
13686
normal! zo
13687
normal! zo
13687
normal! zo
13687
normal! zo
13694
normal! zo
13695
normal! zo
13696
normal! zo
13696
normal! zo
13697
normal! zo
13708
normal! zo
13709
normal! zo
13710
normal! zo
13710
normal! zo
13711
normal! zo
13726
normal! zo
13727
normal! zo
13728
normal! zo
13729
normal! zo
13729
normal! zo
13730
normal! zo
13742
normal! zo
13743
normal! zo
13743
normal! zo
13743
normal! zo
13744
normal! zo
13750
normal! zo
13751
normal! zo
13752
normal! zo
13752
normal! zo
13753
normal! zo
13764
normal! zo
13765
normal! zo
13766
normal! zo
13766
normal! zo
13767
normal! zo
13782
normal! zo
13782
normal! zo
13782
normal! zo
13803
normal! zo
13808
normal! zo
13809
normal! zo
13810
normal! zo
13810
normal! zo
13810
normal! zo
13810
normal! zo
13810
normal! zo
13810
normal! zo
13810
normal! zo
13810
normal! zo
13810
normal! zo
13810
normal! zo
13816
normal! zo
13817
normal! zo
13818
normal! zo
13818
normal! zo
13818
normal! zo
13818
normal! zo
13818
normal! zo
13818
normal! zo
13818
normal! zo
13820
normal! zo
13820
normal! zo
13820
normal! zo
13820
normal! zo
13820
normal! zo
13820
normal! zo
13820
normal! zo
13820
normal! zo
13822
normal! zo
13823
normal! zo
13823
normal! zo
13823
normal! zo
13823
normal! zo
13823
normal! zo
13823
normal! zo
13823
normal! zo
13823
normal! zo
13823
normal! zo
13826
normal! zo
13828
normal! zo
13833
normal! zo
13842
normal! zo
13843
normal! zo
13843
normal! zo
13843
normal! zo
13843
normal! zo
13843
normal! zo
13843
normal! zo
13843
normal! zo
13850
normal! zo
13852
normal! zo
13853
normal! zo
13854
normal! zo
13854
normal! zo
13855
normal! zo
13865
normal! zo
13866
normal! zo
13867
normal! zo
13867
normal! zo
13868
normal! zo
13882
normal! zo
13883
normal! zo
13884
normal! zo
13885
normal! zo
13885
normal! zo
13886
normal! zo
13896
normal! zo
13897
normal! zo
13898
normal! zo
13898
normal! zo
13899
normal! zo
13913
normal! zo
13913
normal! zo
13913
normal! zo
13924
normal! zo
13929
normal! zo
13930
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
13931
normal! zo
13931
normal! zo
13931
normal! zo
13931
normal! zo
13937
normal! zo
13938
normal! zo
13939
normal! zo
13939
normal! zo
13939
normal! zo
13939
normal! zo
13939
normal! zo
13939
normal! zo
13939
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
13943
normal! zo
13944
normal! zo
13944
normal! zo
13944
normal! zo
13944
normal! zo
13944
normal! zo
13944
normal! zo
13944
normal! zo
13944
normal! zo
13944
normal! zo
13947
normal! zo
13949
normal! zo
13954
normal! zo
13963
normal! zo
13964
normal! zo
13964
normal! zo
13964
normal! zo
13964
normal! zo
13964
normal! zo
13964
normal! zo
13964
normal! zo
13971
normal! zo
13976
normal! zo
13977
normal! zo
13978
normal! zo
13985
normal! zo
13986
normal! zo
13987
normal! zo
13993
normal! zo
13994
normal! zo
13995
normal! zo
14000
normal! zo
14001
normal! zo
14002
normal! zo
14002
normal! zo
14012
normal! zo
14013
normal! zo
14014
normal! zo
14014
normal! zo
14014
normal! zo
14014
normal! zo
14014
normal! zo
14014
normal! zo
14021
normal! zo
14022
normal! zo
14022
normal! zo
14022
normal! zo
14022
normal! zo
14022
normal! zo
14022
normal! zo
14022
normal! zo
14029
normal! zo
14030
normal! zo
14030
normal! zo
14030
normal! zo
14030
normal! zo
14030
normal! zo
14030
normal! zo
14030
normal! zo
14036
normal! zo
14037
normal! zo
14037
normal! zo
14037
normal! zo
14037
normal! zo
14037
normal! zo
14037
normal! zo
14037
normal! zo
14047
normal! zo
14053
normal! zo
14053
normal! zo
14059
normal! zo
14065
normal! zo
14071
normal! zo
14071
normal! zo
14071
normal! zo
14071
normal! zo
14071
normal! zo
14071
normal! zo
14071
normal! zo
14071
normal! zo
14071
normal! zo
14081
normal! zo
14081
normal! zo
14081
normal! zo
14081
normal! zo
14081
normal! zo
14081
normal! zo
14083
normal! zo
14084
normal! zo
14084
normal! zo
14084
normal! zo
14090
normal! zo
14090
normal! zo
14090
normal! zo
14090
normal! zo
14090
normal! zo
14090
normal! zo
14090
normal! zo
14090
normal! zo
14090
normal! zo
14101
normal! zo
14101
normal! zo
14101
normal! zo
14101
normal! zo
14101
normal! zo
14101
normal! zo
14103
normal! zo
14104
normal! zo
14104
normal! zo
14104
normal! zo
14110
normal! zo
14110
normal! zo
14110
normal! zo
14110
normal! zo
14118
normal! zo
14123
normal! zo
14126
normal! zo
14131
normal! zo
14132
normal! zo
14133
normal! zo
14133
normal! zo
14133
normal! zo
14133
normal! zo
14133
normal! zo
14133
normal! zo
14133
normal! zo
14133
normal! zo
14133
normal! zo
14133
normal! zo
14139
normal! zo
14140
normal! zo
14143
normal! zo
14144
normal! zo
14144
normal! zo
14144
normal! zo
14144
normal! zo
14144
normal! zo
14144
normal! zo
14144
normal! zo
14146
normal! zo
14146
normal! zo
14146
normal! zo
14146
normal! zo
14146
normal! zo
14146
normal! zo
14146
normal! zo
14146
normal! zo
14146
normal! zo
14148
normal! zo
14149
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
14155
normal! zo
14156
normal! zo
14160
normal! zo
14160
normal! zo
14165
normal! zo
14165
normal! zo
14170
normal! zo
14171
normal! zo
14178
normal! zo
14179
normal! zo
14182
normal! zo
14182
normal! zo
14182
normal! zo
14182
normal! zo
14182
normal! zo
14182
normal! zo
14189
normal! zo
14190
normal! zo
14191
normal! zo
14192
normal! zo
14198
normal! zo
14199
normal! zo
14200
normal! zo
14206
normal! zo
14207
normal! zo
14207
normal! zo
14208
normal! zo
14213
normal! zo
14214
normal! zo
14214
normal! zo
14215
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
14233
normal! zo
14234
normal! zo
14235
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
14248
normal! zo
14249
normal! zo
14249
normal! zo
14249
normal! zo
14249
normal! zo
14249
normal! zo
14249
normal! zo
14249
normal! zo
14260
normal! zo
14261
normal! zo
14261
normal! zo
14267
normal! zo
14273
normal! zo
14273
normal! zo
14279
normal! zo
14279
normal! zo
14279
normal! zo
14279
normal! zo
14295
normal! zo
14300
normal! zo
14301
normal! zo
14302
normal! zo
14302
normal! zo
14302
normal! zo
14302
normal! zo
14302
normal! zo
14302
normal! zo
14302
normal! zo
14302
normal! zo
14302
normal! zo
14302
normal! zo
14308
normal! zo
14309
normal! zo
14310
normal! zo
14310
normal! zo
14310
normal! zo
14310
normal! zo
14310
normal! zo
14310
normal! zo
14310
normal! zo
14312
normal! zo
14312
normal! zo
14312
normal! zo
14312
normal! zo
14312
normal! zo
14312
normal! zo
14312
normal! zo
14312
normal! zo
14312
normal! zo
14314
normal! zo
14315
normal! zo
14315
normal! zo
14315
normal! zo
14315
normal! zo
14315
normal! zo
14315
normal! zo
14315
normal! zo
14315
normal! zo
14315
normal! zo
14318
normal! zo
14320
normal! zo
14320
normal! zo
14325
normal! zo
14325
normal! zo
14335
normal! zo
14336
normal! zo
14336
normal! zo
14336
normal! zo
14336
normal! zo
14336
normal! zo
14336
normal! zo
14343
normal! zo
14344
normal! zo
14345
normal! zo
14346
normal! zo
14351
normal! zo
14352
normal! zo
14353
normal! zo
14363
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
14370
normal! zo
14371
normal! zo
14371
normal! zo
14371
normal! zo
14372
normal! zo
14382
normal! zo
14383
normal! zo
14383
normal! zo
14389
normal! zo
14390
normal! zo
14390
normal! zo
14396
normal! zo
14396
normal! zo
14396
normal! zo
14396
normal! zo
14408
normal! zo
14413
normal! zo
14414
normal! zo
14415
normal! zo
14415
normal! zo
14415
normal! zo
14415
normal! zo
14415
normal! zo
14415
normal! zo
14415
normal! zo
14415
normal! zo
14415
normal! zo
14415
normal! zo
14421
normal! zo
14422
normal! zo
14423
normal! zo
14423
normal! zo
14423
normal! zo
14423
normal! zo
14423
normal! zo
14423
normal! zo
14423
normal! zo
14425
normal! zo
14425
normal! zo
14425
normal! zo
14425
normal! zo
14425
normal! zo
14425
normal! zo
14425
normal! zo
14425
normal! zo
14425
normal! zo
14427
normal! zo
14428
normal! zo
14428
normal! zo
14428
normal! zo
14428
normal! zo
14428
normal! zo
14428
normal! zo
14428
normal! zo
14428
normal! zo
14428
normal! zo
14431
normal! zo
14433
normal! zo
14433
normal! zo
14438
normal! zo
14438
normal! zo
14448
normal! zo
14449
normal! zo
14449
normal! zo
14449
normal! zo
14449
normal! zo
14449
normal! zo
14449
normal! zo
14456
normal! zo
14463
normal! zo
14464
normal! zo
14466
normal! zo
14466
normal! zo
14466
normal! zo
14472
normal! zo
14474
normal! zo
14476
normal! zo
14482
normal! zo
14484
normal! zo
14486
normal! zo
14497
normal! zo
14517
normal! zo
14529
normal! zo
14530
normal! zo
14531
normal! zo
14533
normal! zo
14534
normal! zo
14535
normal! zo
14535
normal! zo
14535
normal! zo
14537
normal! zo
14538
normal! zo
14538
normal! zo
14538
normal! zo
14554
normal! zo
14565
normal! zo
14574
normal! zo
14584
normal! zo
14611
normal! zo
14616
normal! zo
14622
normal! zo
14633
normal! zo
14646
normal! zo
14670
normal! zo
14672
normal! zo
14675
normal! zo
14678
normal! zo
14679
normal! zo
14683
normal! zo
14684
normal! zo
14698
normal! zo
14698
normal! zo
14698
normal! zo
14698
normal! zo
14720
normal! zo
14721
normal! zo
14722
normal! zo
14722
normal! zo
14722
normal! zo
14722
normal! zo
14722
normal! zo
14722
normal! zo
14722
normal! zo
14722
normal! zo
14722
normal! zo
14722
normal! zo
14731
normal! zo
14732
normal! zo
14738
normal! zo
14742
normal! zo
14743
normal! zo
14752
normal! zo
14753
normal! zo
14761
normal! zo
14762
normal! zo
14768
normal! zo
14783
normal! zo
14791
normal! zo
14797
normal! zo
14803
normal! zo
14808
normal! zo
14812
normal! zo
14818
normal! zo
14823
normal! zo
14824
normal! zo
14829
normal! zo
14840
normal! zo
14858
normal! zo
14900
normal! zo
14906
normal! zo
14912
normal! zo
14919
normal! zo
14928
normal! zo
14930
normal! zo
14937
normal! zo
14937
normal! zo
14937
normal! zo
14937
normal! zo
14937
normal! zo
14937
normal! zo
14954
normal! zo
14966
normal! zo
14977
normal! zo
14978
normal! zo
14994
normal! zo
15011
normal! zo
15015
normal! zo
15016
normal! zo
15017
normal! zo
15017
normal! zo
15019
normal! zo
15022
normal! zo
15035
normal! zo
15045
normal! zo
15047
normal! zo
15051
normal! zo
15052
normal! zo
15052
normal! zo
15052
normal! zo
15052
normal! zo
15052
normal! zo
15052
normal! zo
15065
normal! zo
15086
normal! zo
15087
normal! zo
15094
normal! zo
15127
normal! zo
15128
normal! zo
15128
normal! zo
15144
normal! zo
15150
normal! zo
15153
normal! zo
15153
normal! zo
15153
normal! zo
15159
normal! zo
15159
normal! zo
15179
normal! zo
15184
normal! zo
15189
normal! zo
15197
normal! zo
15216
normal! zo
15250
normal! zo
15258
normal! zo
15267
normal! zo
15286
normal! zo
15288
normal! zo
15292
normal! zo
15309
normal! zo
15315
normal! zo
15319
normal! zo
15358
normal! zo
15462
normal! zo
15462
normal! zo
15538
normal! zo
15538
normal! zo
15538
normal! zo
15651
normal! zo
15682
normal! zo
15706
normal! zo
15716
normal! zo
15716
normal! zo
15716
normal! zo
15716
normal! zo
15716
normal! zo
15904
normal! zo
15923
normal! zo
15945
normal! zo
15950
normal! zo
15951
normal! zo
15951
normal! zo
15954
normal! zo
15955
normal! zo
15955
normal! zo
15955
normal! zo
15958
normal! zo
15958
normal! zo
15958
normal! zo
15962
normal! zo
15962
normal! zo
15962
normal! zo
15962
normal! zo
15962
normal! zo
15962
normal! zo
15962
normal! zo
15962
normal! zo
15962
normal! zo
16267
normal! zo
16425
normal! zo
16493
normal! zo
16529
normal! zo
16544
normal! zo
16550
normal! zo
16553
normal! zo
16561
normal! zo
16562
normal! zo
16562
normal! zo
16562
normal! zo
16562
normal! zo
16562
normal! zo
16566
normal! zo
16574
normal! zo
16577
normal! zo
16583
normal! zo
16589
normal! zo
16592
normal! zo
16598
normal! zo
16612
normal! zo
16618
normal! zo
16623
normal! zo
16626
normal! zo
16626
normal! zo
16626
normal! zo
16636
normal! zo
16651
normal! zo
16662
normal! zo
16662
normal! zo
16673
normal! zo
16688
normal! zo
16698
normal! zo
16709
normal! zo
16717
normal! zo
16722
normal! zo
16738
normal! zo
16776
normal! zo
16807
normal! zo
16828
normal! zo
16847
normal! zo
16855
normal! zo
16856
normal! zo
16865
normal! zo
16881
normal! zo
16901
normal! zo
16906
normal! zo
16919
normal! zo
16919
normal! zo
16919
normal! zo
16919
normal! zo
16919
normal! zo
16919
normal! zo
16919
normal! zo
16919
normal! zo
16919
normal! zo
16919
normal! zo
16998
normal! zo
17011
normal! zo
17012
normal! zo
17013
normal! zo
17019
normal! zo
17023
normal! zo
17025
normal! zo
17040
normal! zo
17056
normal! zo
17064
normal! zo
17068
normal! zo
17073
normal! zo
17081
normal! zo
17086
normal! zo
17094
normal! zo
17099
normal! zo
17119
normal! zo
17134
normal! zo
17135
normal! zo
17151
normal! zo
17188
normal! zo
17202
normal! zo
17205
normal! zo
17209
normal! zo
17210
normal! zo
17229
normal! zo
17244
normal! zo
17251
normal! zo
17252
normal! zo
17258
normal! zo
17265
normal! zo
17270
normal! zo
17298
normal! zo
17318
normal! zo
17319
normal! zo
17341
normal! zo
17355
normal! zo
17362
normal! zo
17363
normal! zo
17377
normal! zo
17413
normal! zo
17434
normal! zo
17457
normal! zo
17470
normal! zo
17494
normal! zo
17499
normal! zo
17523
normal! zo
17541
normal! zo
17559
normal! zo
17560
normal! zo
17571
normal! zo
17595
normal! zo
17608
normal! zo
17612
normal! zo
17612
normal! zo
17612
normal! zo
17612
normal! zo
17626
normal! zo
17626
normal! zo
17626
normal! zo
17626
normal! zo
17626
normal! zo
17626
normal! zo
17626
normal! zo
17740
normal! zo
17748
normal! zo
17770
normal! zo
17793
normal! zo
17858
normal! zo
17915
normal! zo
17930
normal! zo
17964
normal! zo
17978
normal! zo
18004
normal! zo
18024
normal! zo
18036
normal! zo
18036
normal! zo
18036
normal! zo
18036
normal! zo
18036
normal! zo
18039
normal! zo
18046
normal! zo
18049
normal! zo
18060
normal! zo
18066
normal! zo
18071
normal! zo
18082
normal! zo
18101
normal! zo
18144
normal! zo
18169
normal! zo
18225
normal! zo
18234
normal! zo
18679
normal! zo
18751
normal! zo
18757
normal! zo
18760
normal! zo
18773
normal! zo
18790
normal! zo
18800
normal! zo
18803
normal! zo
18804
normal! zo
18804
normal! zo
18810
normal! zo
18817
normal! zo
19069
normal! zo
19115
normal! zo
19125
normal! zo
19126
normal! zo
19126
normal! zo
19126
normal! zo
19126
normal! zo
19126
normal! zo
20016
normal! zo
20024
normal! zo
20058
normal! zo
20070
normal! zo
20075
normal! zo
20082
normal! zo
20094
normal! zo
20112
normal! zo
20122
normal! zo
20333
normal! zo
20404
normal! zo
20405
normal! zo
20417
normal! zo
20432
normal! zo
20439
normal! zo
20446
normal! zo
20453
normal! zo
20460
normal! zo
20467
normal! zo
20474
normal! zo
20480
normal! zo
20599
normal! zo
20617
normal! zo
20646
normal! zo
20662
normal! zo
20672
normal! zo
20683
normal! zo
20694
normal! zo
20711
normal! zo
20731
normal! zo
20751
normal! zo
20799
normal! zo
20811
normal! zo
20812
normal! zo
20820
normal! zo
20837
normal! zo
let s:l = 16760 - ((0 * winheight(0) + 8) / 17)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
16760
normal! 09|
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
97
normal! zo
97
normal! zo
97
normal! zo
97
normal! zo
97
normal! zo
97
normal! zo
97
normal! zo
99
normal! zo
99
normal! zo
99
normal! zo
99
normal! zo
99
normal! zo
99
normal! zo
99
normal! zo
115
normal! zo
116
normal! zo
116
normal! zo
116
normal! zo
116
normal! zo
116
normal! zo
116
normal! zo
116
normal! zo
116
normal! zo
116
normal! zo
151
normal! zo
176
normal! zo
227
normal! zo
238
normal! zo
275
normal! zo
345
normal! zo
346
normal! zo
351
normal! zo
360
normal! zo
363
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
364
normal! zo
414
normal! zo
415
normal! zo
416
normal! zo
416
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
433
normal! zo
434
normal! zo
435
normal! zo
435
normal! zo
438
normal! zo
439
normal! zo
439
normal! zo
439
normal! zo
439
normal! zo
443
normal! zo
448
normal! zo
448
normal! zo
448
normal! zo
448
normal! zo
451
normal! zo
452
normal! zo
473
normal! zo
473
normal! zo
473
normal! zo
473
normal! zo
482
normal! zo
483
normal! zo
483
normal! zo
483
normal! zo
483
normal! zo
492
normal! zo
497
normal! zo
497
normal! zo
497
normal! zo
497
normal! zo
500
normal! zo
500
normal! zo
500
normal! zo
500
normal! zo
505
normal! zo
541
normal! zo
550
normal! zo
550
normal! zo
550
normal! zo
550
normal! zo
556
normal! zo
716
normal! zo
722
normal! zo
743
normal! zo
749
normal! zo
749
normal! zo
770
normal! zo
806
normal! zo
820
normal! zo
821
normal! zo
855
normal! zo
875
normal! zo
875
normal! zo
875
normal! zo
875
normal! zo
875
normal! zo
886
normal! zo
1020
normal! zo
1026
normal! zo
1027
normal! zo
1028
normal! zo
1053
normal! zo
1073
normal! zo
1084
normal! zo
1084
normal! zo
1084
normal! zo
1084
normal! zo
1084
normal! zo
1084
normal! zo
1084
normal! zo
1113
normal! zo
let s:l = 775 - ((7 * winheight(0) + 6) / 12)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
775
normal! 039|
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
97
normal! zo
97
normal! zo
97
normal! zo
97
normal! zo
97
normal! zo
97
normal! zo
97
normal! zo
99
normal! zo
99
normal! zo
99
normal! zo
99
normal! zo
99
normal! zo
99
normal! zo
99
normal! zo
111
normal! zo
115
normal! zo
116
normal! zo
116
normal! zo
116
normal! zo
116
normal! zo
116
normal! zo
116
normal! zo
116
normal! zo
116
normal! zo
116
normal! zo
121
normal! zo
138
normal! zo
151
normal! zo
176
normal! zo
214
normal! zo
227
normal! zo
238
normal! zo
262
normal! zo
275
normal! zo
285
normal! zo
285
normal! zo
285
normal! zo
285
normal! zo
292
normal! zo
292
normal! zo
292
normal! zo
292
normal! zo
296
normal! zo
297
normal! zo
297
normal! zo
320
normal! zo
321
normal! zo
321
normal! zo
345
normal! zo
346
normal! zo
351
normal! zo
360
normal! zo
361
normal! zo
361
normal! zo
361
normal! zo
363
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
364
normal! zo
381
normal! zo
399
normal! zo
405
normal! zo
407
normal! zo
414
normal! zo
415
normal! zo
416
normal! zo
416
normal! zo
417
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
430
normal! zo
430
normal! zo
430
normal! zo
430
normal! zo
433
normal! zo
434
normal! zo
435
normal! zo
435
normal! zo
436
normal! zo
438
normal! zo
439
normal! zo
439
normal! zo
439
normal! zo
439
normal! zo
443
normal! zo
448
normal! zo
448
normal! zo
448
normal! zo
448
normal! zo
451
normal! zo
452
normal! zo
473
normal! zo
473
normal! zo
473
normal! zo
473
normal! zo
482
normal! zo
483
normal! zo
483
normal! zo
483
normal! zo
483
normal! zo
492
normal! zo
497
normal! zo
497
normal! zo
497
normal! zo
497
normal! zo
500
normal! zo
500
normal! zo
500
normal! zo
500
normal! zo
505
normal! zo
506
normal! zo
529
normal! zo
530
normal! zo
530
normal! zo
530
normal! zo
530
normal! zo
541
normal! zo
546
normal! zo
546
normal! zo
546
normal! zo
546
normal! zo
550
normal! zo
550
normal! zo
550
normal! zo
550
normal! zo
556
normal! zo
557
normal! zo
581
normal! zo
582
normal! zo
582
normal! zo
582
normal! zo
582
normal! zo
593
normal! zo
598
normal! zo
598
normal! zo
598
normal! zo
598
normal! zo
603
normal! zo
603
normal! zo
603
normal! zo
603
normal! zo
609
normal! zo
632
normal! zo
633
normal! zo
652
normal! zo
658
normal! zo
664
normal! zo
665
normal! zo
674
normal! zo
684
normal! zo
684
normal! zo
703
normal! zo
704
normal! zo
711
normal! zo
716
normal! zo
722
normal! zo
734
normal! zo
737
normal! zo
737
normal! zo
737
normal! zo
737
normal! zo
743
normal! zo
749
normal! zo
749
normal! zo
770
normal! zo
795
normal! zo
806
normal! zo
820
normal! zo
821
normal! zo
855
normal! zo
875
normal! zo
875
normal! zo
875
normal! zo
875
normal! zo
875
normal! zo
894
normal! zo
913
normal! zo
1020
normal! zo
1026
normal! zo
1027
normal! zo
1028
normal! zo
1053
normal! zo
1073
normal! zo
1084
normal! zo
1084
normal! zo
1084
normal! zo
1084
normal! zo
1084
normal! zo
1084
normal! zo
1084
normal! zo
1113
normal! zo
let s:l = 770 - ((7 * winheight(0) + 8) / 16)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
770
normal! 018|
wincmd w
12wincmd w
exe '1resize ' . ((&lines * 3 + 31) / 63)
exe 'vert 1resize ' . ((&columns * 29 + 55) / 110)
exe '2resize ' . ((&lines * 57 + 31) / 63)
exe 'vert 2resize ' . ((&columns * 29 + 55) / 110)
exe '3resize ' . ((&lines * 1 + 31) / 63)
exe 'vert 3resize ' . ((&columns * 80 + 55) / 110)
exe '4resize ' . ((&lines * 17 + 31) / 63)
exe 'vert 4resize ' . ((&columns * 80 + 55) / 110)
exe '5resize ' . ((&lines * 1 + 31) / 63)
exe 'vert 5resize ' . ((&columns * 80 + 55) / 110)
exe '6resize ' . ((&lines * 1 + 31) / 63)
exe 'vert 6resize ' . ((&columns * 80 + 55) / 110)
exe '7resize ' . ((&lines * 12 + 31) / 63)
exe 'vert 7resize ' . ((&columns * 80 + 55) / 110)
exe '8resize ' . ((&lines * 1 + 31) / 63)
exe 'vert 8resize ' . ((&columns * 80 + 55) / 110)
exe '9resize ' . ((&lines * 1 + 31) / 63)
exe 'vert 9resize ' . ((&columns * 80 + 55) / 110)
exe '10resize ' . ((&lines * 1 + 31) / 63)
exe 'vert 10resize ' . ((&columns * 80 + 55) / 110)
exe '11resize ' . ((&lines * 1 + 31) / 63)
exe 'vert 11resize ' . ((&columns * 80 + 55) / 110)
exe '12resize ' . ((&lines * 16 + 31) / 63)
exe 'vert 12resize ' . ((&columns * 80 + 55) / 110)
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
12wincmd w

" vim: ft=vim ro nowrap smc=128
