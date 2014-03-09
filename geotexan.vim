" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 09 marzo 2014 at 16:42:54.
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
set lines=51 columns=113
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
exe '1resize ' . ((&lines * 3 + 25) / 51)
exe 'vert 1resize ' . ((&columns * 32 + 56) / 113)
exe '2resize ' . ((&lines * 45 + 25) / 51)
exe 'vert 2resize ' . ((&columns * 32 + 56) / 113)
exe '3resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 3resize ' . ((&columns * 80 + 56) / 113)
exe '4resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 4resize ' . ((&columns * 80 + 56) / 113)
exe '5resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 5resize ' . ((&columns * 80 + 56) / 113)
exe '6resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 6resize ' . ((&columns * 80 + 56) / 113)
exe '7resize ' . ((&lines * 31 + 25) / 51)
exe 'vert 7resize ' . ((&columns * 80 + 56) / 113)
exe '8resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 8resize ' . ((&columns * 80 + 56) / 113)
exe '9resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 9resize ' . ((&columns * 80 + 56) / 113)
exe '10resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 10resize ' . ((&columns * 80 + 56) / 113)
exe '11resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 11resize ' . ((&columns * 80 + 56) / 113)
exe '12resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 12resize ' . ((&columns * 80 + 56) / 113)
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
9876
normal! zo
9892
normal! zo
9909
normal! zo
9909
normal! zo
9909
normal! zo
9909
normal! zo
9909
normal! zo
9909
normal! zo
9909
normal! zo
9909
normal! zo
9909
normal! zo
9916
normal! zo
9930
normal! zo
9931
normal! zo
9931
normal! zo
9933
normal! zo
9934
normal! zo
9934
normal! zo
9936
normal! zo
9937
normal! zo
9937
normal! zo
9939
normal! zo
9940
normal! zo
9940
normal! zo
9942
normal! zo
9945
normal! zo
9947
normal! zo
9947
normal! zo
9947
normal! zo
9956
normal! zo
9969
normal! zo
9972
normal! zo
9973
normal! zo
9973
normal! zo
9976
normal! zo
9976
normal! zo
9976
normal! zo
9979
normal! zo
9979
normal! zo
9979
normal! zo
9979
normal! zo
9985
normal! zo
9988
normal! zo
9992
normal! zo
9999
normal! zo
10001
normal! zo
10048
normal! zo
10062
normal! zo
10063
normal! zo
10065
normal! zo
10100
normal! zo
10107
normal! zo
10112
normal! zo
10113
normal! zo
10118
normal! zo
10118
normal! zo
10118
normal! zo
10118
normal! zo
10118
normal! zo
10121
normal! zo
10121
normal! zo
10121
normal! zo
10147
normal! zo
10156
normal! zo
10161
normal! zo
10163
normal! zo
10168
normal! zo
10174
normal! zo
10182
normal! zo
10183
normal! zo
10183
normal! zo
10183
normal! zo
10183
normal! zo
10192
normal! zo
10193
normal! zo
10198
normal! zo
10247
normal! zo
10252
normal! zo
10365
normal! zo
10392
normal! zo
10397
normal! zo
10403
normal! zo
10489
normal! zo
10496
normal! zo
10497
normal! zo
10545
normal! zo
10545
normal! zo
10545
normal! zo
10545
normal! zo
10545
normal! zo
10548
normal! zo
10556
normal! zo
10557
normal! zo
10602
normal! zo
10622
normal! zo
10623
normal! zo
10624
normal! zo
10624
normal! zo
10624
normal! zo
10624
normal! zo
10624
normal! zo
10624
normal! zo
10624
normal! zo
10624
normal! zo
10624
normal! zo
10641
normal! zo
10647
normal! zo
10657
normal! zo
10672
normal! zo
10675
normal! zo
10678
normal! zo
10678
normal! zo
10678
normal! zo
10681
normal! zo
10681
normal! zo
10681
normal! zo
10681
normal! zo
10686
normal! zo
10686
normal! zo
10686
normal! zo
10694
normal! zo
10701
normal! zo
10708
normal! zo
10711
normal! zo
10713
normal! zo
10716
normal! zo
10719
normal! zo
10724
normal! zo
10735
normal! zo
10742
normal! zo
10746
normal! zo
10747
normal! zo
10747
normal! zo
10749
normal! zo
10750
normal! zo
10750
normal! zo
10752
normal! zo
10753
normal! zo
10753
normal! zo
10755
normal! zo
10756
normal! zo
10756
normal! zo
10758
normal! zo
10759
normal! zo
10759
normal! zo
10761
normal! zo
10762
normal! zo
10762
normal! zo
10764
normal! zo
10765
normal! zo
10765
normal! zo
10767
normal! zo
10770
normal! zo
10772
normal! zo
10772
normal! zo
10772
normal! zo
10778
normal! zo
10779
normal! zo
10779
normal! zo
10781
normal! zo
10782
normal! zo
10782
normal! zo
10806
normal! zo
10810
normal! zo
10813
normal! zo
10814
normal! zo
10814
normal! zo
10814
normal! zo
10814
normal! zo
10814
normal! zo
10814
normal! zo
10819
normal! zo
10820
normal! zo
10820
normal! zo
10820
normal! zo
10823
normal! zo
10935
normal! zo
11011
normal! zo
11019
normal! zo
11026
normal! zo
11026
normal! zo
11026
normal! zo
11026
normal! zo
11026
normal! zo
11026
normal! zo
11026
normal! zo
11037
normal! zo
11041
normal! zo
11042
normal! zo
11042
normal! zo
11042
normal! zo
11052
normal! zo
11055
normal! zo
11062
normal! zo
11071
normal! zo
11080
normal! zo
11190
normal! zo
11191
normal! zc
11204
normal! zo
11204
normal! zo
11204
normal! zo
11204
normal! zo
11213
normal! zc
11216
normal! zo
11229
normal! zo
11242
normal! zo
11249
normal! zo
11251
normal! zo
11251
normal! zo
11251
normal! zo
11251
normal! zo
11251
normal! zo
11251
normal! zo
11259
normal! zc
11276
normal! zo
11304
normal! zo
11316
normal! zo
11317
normal! zo
11317
normal! zo
11317
normal! zo
11317
normal! zo
11276
normal! zc
11322
normal! zo
11322
normal! zc
11373
normal! zo
11373
normal! zc
11488
normal! zo
11496
normal! zo
11496
normal! zo
11496
normal! zo
11496
normal! zo
11488
normal! zc
11504
normal! zc
11510
normal! zo
11510
normal! zc
11521
normal! zo
11521
normal! zc
11538
normal! zo
11538
normal! zo
11542
normal! zo
11547
normal! zo
11547
normal! zo
11549
normal! zo
11550
normal! zo
11550
normal! zo
11555
normal! zo
11555
normal! zo
11555
normal! zo
11555
normal! zo
11555
normal! zo
11555
normal! zc
11568
normal! zo
11571
normal! zo
11571
normal! zo
11571
normal! zo
11571
normal! zo
11577
normal! zo
11577
normal! zo
11577
normal! zo
11577
normal! zo
11577
normal! zo
11577
normal! zc
11605
normal! zo
11643
normal! zc
11650
normal! zc
11658
normal! zo
11658
normal! zc
11666
normal! zc
11674
normal! zc
11688
normal! zo
11688
normal! zc
11706
normal! zo
11706
normal! zo
11706
normal! zo
11706
normal! zo
11706
normal! zo
11706
normal! zo
11706
normal! zo
11706
normal! zo
11706
normal! zo
11706
normal! zo
11706
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
11768
normal! zo
11769
normal! zo
11791
normal! zo
11791
normal! zc
11898
normal! zo
11898
normal! zc
11947
normal! zo
11947
normal! zo
11949
normal! zo
11959
normal! zo
11947
normal! zc
12042
normal! zo
12042
normal! zc
12096
normal! zo
12096
normal! zo
12096
normal! zo
12096
normal! zc
12096
normal! zc
12110
normal! zo
12147
normal! zo
12158
normal! zo
12163
normal! zo
12181
normal! zo
12181
normal! zo
12181
normal! zo
12181
normal! zo
12182
normal! zo
12187
normal! zo
12203
normal! zo
12203
normal! zo
12203
normal! zo
12203
normal! zo
12212
normal! zo
12212
normal! zo
12212
normal! zo
12212
normal! zo
12212
normal! zo
12236
normal! zo
12260
normal! zo
12260
normal! zc
12301
normal! zo
12301
normal! zo
12301
normal! zo
12301
normal! zo
12363
normal! zo
12379
normal! zo
12379
normal! zc
12403
normal! zo
12403
normal! zo
12403
normal! zo
12403
normal! zc
12428
normal! zo
12428
normal! zo
12428
normal! zo
12428
normal! zc
12503
normal! zo
12503
normal! zo
12503
normal! zo
12503
normal! zo
12503
normal! zo
12503
normal! zo
12503
normal! zo
12503
normal! zo
12503
normal! zc
12519
normal! zo
12519
normal! zc
12541
normal! zo
12541
normal! zc
12562
normal! zo
12562
normal! zo
12562
normal! zo
12562
normal! zo
12562
normal! zo
12562
normal! zo
12562
normal! zo
12562
normal! zc
12562
normal! zc
12682
normal! zo
12682
normal! zo
12682
normal! zo
12682
normal! zo
12682
normal! zo
12682
normal! zc
12950
normal! zo
12950
normal! zc
12980
normal! zo
12980
normal! zo
12980
normal! zo
12980
normal! zo
12980
normal! zo
12980
normal! zo
12980
normal! zo
12980
normal! zo
12995
normal! zo
13010
normal! zo
13012
normal! zo
13034
normal! zo
13042
normal! zo
13042
normal! zc
13058
normal! zo
13058
normal! zo
13097
normal! zo
13159
normal! zo
13160
normal! zo
13178
normal! zo
13220
normal! zo
13221
normal! zo
13249
normal! zo
13281
normal! zo
13282
normal! zo
13310
normal! zo
13346
normal! zo
13347
normal! zo
13365
normal! zo
13392
normal! zc
13402
normal! zo
13402
normal! zc
13422
normal! zo
13423
normal! zo
13424
normal! zo
13422
normal! zc
13478
normal! zo
13478
normal! zc
13536
normal! zo
13536
normal! zo
13536
normal! zo
13546
normal! zo
13551
normal! zo
13552
normal! zo
13553
normal! zo
13553
normal! zo
13553
normal! zo
13553
normal! zo
13553
normal! zo
13553
normal! zo
13553
normal! zo
13553
normal! zo
13553
normal! zo
13553
normal! zo
13559
normal! zo
13560
normal! zo
13561
normal! zo
13561
normal! zo
13561
normal! zo
13561
normal! zo
13561
normal! zo
13561
normal! zo
13561
normal! zo
13563
normal! zo
13563
normal! zo
13563
normal! zo
13563
normal! zo
13563
normal! zo
13563
normal! zo
13563
normal! zo
13563
normal! zo
13565
normal! zo
13566
normal! zo
13566
normal! zo
13566
normal! zo
13566
normal! zo
13566
normal! zo
13566
normal! zo
13566
normal! zo
13566
normal! zo
13566
normal! zo
13569
normal! zo
13571
normal! zo
13571
normal! zo
13576
normal! zo
13576
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
13594
normal! zo
13594
normal! zo
13594
normal! zo
13600
normal! zo
13601
normal! zo
13610
normal! zo
13611
normal! zo
13611
normal! zo
13611
normal! zo
13611
normal! zo
13615
normal! zo
13615
normal! zo
13615
normal! zo
13623
normal! zo
13624
normal! zo
13626
normal! zo
13634
normal! zo
13635
normal! zo
13635
normal! zo
13635
normal! zo
13635
normal! zo
13639
normal! zo
13639
normal! zo
13639
normal! zo
13646
normal! zo
13646
normal! zo
13646
normal! zo
13646
normal! zo
13646
normal! zo
13649
normal! zo
13650
normal! zo
13651
normal! zo
13652
normal! zo
13652
normal! zo
13653
normal! zo
13665
normal! zo
13666
normal! zo
13666
normal! zo
13666
normal! zo
13673
normal! zo
13674
normal! zo
13675
normal! zo
13675
normal! zo
13676
normal! zo
13687
normal! zo
13688
normal! zo
13689
normal! zo
13689
normal! zo
13690
normal! zo
13705
normal! zo
13706
normal! zo
13707
normal! zo
13708
normal! zo
13708
normal! zo
13709
normal! zo
13721
normal! zo
13722
normal! zo
13722
normal! zo
13722
normal! zo
13723
normal! zo
13729
normal! zo
13730
normal! zo
13731
normal! zo
13731
normal! zo
13732
normal! zo
13743
normal! zo
13744
normal! zo
13745
normal! zo
13745
normal! zo
13746
normal! zo
13761
normal! zo
13761
normal! zo
13761
normal! zo
13782
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
13789
normal! zo
13789
normal! zo
13789
normal! zo
13795
normal! zo
13796
normal! zo
13797
normal! zo
13797
normal! zo
13797
normal! zo
13797
normal! zo
13797
normal! zo
13797
normal! zo
13797
normal! zo
13799
normal! zo
13799
normal! zo
13799
normal! zo
13799
normal! zo
13799
normal! zo
13799
normal! zo
13799
normal! zo
13799
normal! zo
13801
normal! zo
13802
normal! zo
13802
normal! zo
13802
normal! zo
13802
normal! zo
13802
normal! zo
13802
normal! zo
13802
normal! zo
13802
normal! zo
13802
normal! zo
13805
normal! zo
13807
normal! zo
13812
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
13829
normal! zo
13831
normal! zo
13832
normal! zo
13833
normal! zo
13833
normal! zo
13834
normal! zo
13844
normal! zo
13845
normal! zo
13846
normal! zo
13846
normal! zo
13847
normal! zo
13861
normal! zo
13862
normal! zo
13863
normal! zo
13864
normal! zo
13864
normal! zo
13865
normal! zo
13875
normal! zo
13876
normal! zo
13877
normal! zo
13877
normal! zo
13878
normal! zo
13892
normal! zo
13892
normal! zo
13892
normal! zo
13903
normal! zo
13908
normal! zo
13909
normal! zo
13910
normal! zo
13910
normal! zo
13910
normal! zo
13910
normal! zo
13910
normal! zo
13910
normal! zo
13910
normal! zo
13910
normal! zo
13910
normal! zo
13910
normal! zo
13916
normal! zo
13917
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
13920
normal! zo
13920
normal! zo
13920
normal! zo
13920
normal! zo
13920
normal! zo
13920
normal! zo
13920
normal! zo
13920
normal! zo
13922
normal! zo
13923
normal! zo
13923
normal! zo
13923
normal! zo
13923
normal! zo
13923
normal! zo
13923
normal! zo
13923
normal! zo
13923
normal! zo
13923
normal! zo
13926
normal! zo
13928
normal! zo
13933
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
13950
normal! zo
13955
normal! zo
13956
normal! zo
13957
normal! zo
13964
normal! zo
13965
normal! zo
13966
normal! zo
13972
normal! zo
13973
normal! zo
13974
normal! zo
13979
normal! zo
13980
normal! zo
13981
normal! zo
13981
normal! zo
13991
normal! zo
13992
normal! zo
13993
normal! zo
13993
normal! zo
13993
normal! zo
13993
normal! zo
13993
normal! zo
13993
normal! zo
14000
normal! zo
14001
normal! zo
14001
normal! zo
14001
normal! zo
14001
normal! zo
14001
normal! zo
14001
normal! zo
14001
normal! zo
14008
normal! zo
14009
normal! zo
14009
normal! zo
14009
normal! zo
14009
normal! zo
14009
normal! zo
14009
normal! zo
14009
normal! zo
14015
normal! zo
14016
normal! zo
14016
normal! zo
14016
normal! zo
14016
normal! zo
14016
normal! zo
14016
normal! zo
14016
normal! zo
14026
normal! zo
14032
normal! zo
14032
normal! zo
14038
normal! zo
14044
normal! zo
14050
normal! zo
14050
normal! zo
14050
normal! zo
14050
normal! zo
14050
normal! zo
14050
normal! zo
14050
normal! zo
14050
normal! zo
14050
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
14063
normal! zo
14063
normal! zo
14063
normal! zo
14069
normal! zo
14069
normal! zo
14069
normal! zo
14069
normal! zo
14069
normal! zo
14069
normal! zo
14069
normal! zo
14069
normal! zo
14069
normal! zo
14080
normal! zo
14080
normal! zo
14080
normal! zo
14080
normal! zo
14080
normal! zo
14080
normal! zo
14082
normal! zo
14083
normal! zo
14083
normal! zo
14083
normal! zo
14089
normal! zo
14089
normal! zo
14089
normal! zo
14089
normal! zo
14097
normal! zo
14102
normal! zo
14105
normal! zo
14110
normal! zo
14111
normal! zo
14112
normal! zo
14112
normal! zo
14112
normal! zo
14112
normal! zo
14112
normal! zo
14112
normal! zo
14112
normal! zo
14112
normal! zo
14112
normal! zo
14112
normal! zo
14118
normal! zo
14119
normal! zo
14122
normal! zo
14123
normal! zo
14123
normal! zo
14123
normal! zo
14123
normal! zo
14123
normal! zo
14123
normal! zo
14123
normal! zo
14125
normal! zo
14125
normal! zo
14125
normal! zo
14125
normal! zo
14125
normal! zo
14125
normal! zo
14125
normal! zo
14125
normal! zo
14125
normal! zo
14127
normal! zo
14128
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
14134
normal! zo
14135
normal! zo
14139
normal! zo
14139
normal! zo
14144
normal! zo
14144
normal! zo
14149
normal! zo
14150
normal! zo
14157
normal! zo
14158
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
14168
normal! zo
14169
normal! zo
14170
normal! zo
14171
normal! zo
14177
normal! zo
14178
normal! zo
14179
normal! zo
14185
normal! zo
14186
normal! zo
14186
normal! zo
14187
normal! zo
14192
normal! zo
14193
normal! zo
14193
normal! zo
14194
normal! zo
14203
normal! zo
14204
normal! zo
14205
normal! zo
14205
normal! zo
14205
normal! zo
14205
normal! zo
14205
normal! zo
14205
normal! zo
14212
normal! zo
14213
normal! zo
14214
normal! zo
14220
normal! zo
14221
normal! zo
14221
normal! zo
14221
normal! zo
14221
normal! zo
14221
normal! zo
14221
normal! zo
14221
normal! zo
14227
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
14239
normal! zo
14240
normal! zo
14240
normal! zo
14246
normal! zo
14252
normal! zo
14252
normal! zo
14258
normal! zo
14258
normal! zo
14258
normal! zo
14258
normal! zo
14274
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
14281
normal! zo
14281
normal! zo
14281
normal! zo
14281
normal! zo
14287
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
14289
normal! zo
14291
normal! zo
14291
normal! zo
14291
normal! zo
14291
normal! zo
14291
normal! zo
14291
normal! zo
14291
normal! zo
14291
normal! zo
14291
normal! zo
14293
normal! zo
14294
normal! zo
14294
normal! zo
14294
normal! zo
14294
normal! zo
14294
normal! zo
14294
normal! zo
14294
normal! zo
14294
normal! zo
14294
normal! zo
14297
normal! zo
14299
normal! zo
14299
normal! zo
14304
normal! zo
14304
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
14322
normal! zo
14323
normal! zo
14324
normal! zo
14325
normal! zo
14330
normal! zo
14331
normal! zo
14332
normal! zo
14342
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
14349
normal! zo
14350
normal! zo
14350
normal! zo
14350
normal! zo
14351
normal! zo
14361
normal! zo
14362
normal! zo
14362
normal! zo
14368
normal! zo
14369
normal! zo
14369
normal! zo
14375
normal! zo
14375
normal! zo
14375
normal! zo
14375
normal! zo
14387
normal! zo
14392
normal! zo
14393
normal! zo
14394
normal! zo
14394
normal! zo
14394
normal! zo
14394
normal! zo
14394
normal! zo
14394
normal! zo
14394
normal! zo
14394
normal! zo
14394
normal! zo
14394
normal! zo
14400
normal! zo
14401
normal! zo
14402
normal! zo
14402
normal! zo
14402
normal! zo
14402
normal! zo
14402
normal! zo
14402
normal! zo
14402
normal! zo
14404
normal! zo
14404
normal! zo
14404
normal! zo
14404
normal! zo
14404
normal! zo
14404
normal! zo
14404
normal! zo
14404
normal! zo
14404
normal! zo
14406
normal! zo
14407
normal! zo
14407
normal! zo
14407
normal! zo
14407
normal! zo
14407
normal! zo
14407
normal! zo
14407
normal! zo
14407
normal! zo
14407
normal! zo
14410
normal! zo
14412
normal! zo
14412
normal! zo
14417
normal! zo
14417
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
14435
normal! zo
14442
normal! zo
14443
normal! zo
14445
normal! zo
14445
normal! zo
14445
normal! zo
14451
normal! zo
14453
normal! zo
14455
normal! zo
14461
normal! zo
14463
normal! zo
14465
normal! zo
14476
normal! zo
14496
normal! zo
14508
normal! zo
14509
normal! zo
14510
normal! zo
14512
normal! zo
14513
normal! zo
14514
normal! zo
14514
normal! zo
14514
normal! zo
14516
normal! zo
14517
normal! zo
14517
normal! zo
14517
normal! zo
14533
normal! zo
14544
normal! zo
14553
normal! zo
14563
normal! zo
14590
normal! zo
14595
normal! zo
14601
normal! zo
14612
normal! zo
14625
normal! zo
14649
normal! zo
14651
normal! zo
14654
normal! zo
14657
normal! zo
14658
normal! zo
14662
normal! zo
14663
normal! zo
14677
normal! zo
14677
normal! zo
14677
normal! zo
14677
normal! zo
14699
normal! zo
14700
normal! zo
14701
normal! zo
14701
normal! zo
14701
normal! zo
14701
normal! zo
14701
normal! zo
14701
normal! zo
14701
normal! zo
14701
normal! zo
14701
normal! zo
14701
normal! zo
14710
normal! zo
14711
normal! zo
14717
normal! zo
14721
normal! zo
14722
normal! zo
14731
normal! zo
14732
normal! zo
14740
normal! zo
14741
normal! zo
14747
normal! zo
14762
normal! zo
14770
normal! zo
14776
normal! zo
14782
normal! zo
14787
normal! zo
14791
normal! zo
14797
normal! zo
14802
normal! zo
14803
normal! zo
14808
normal! zo
14819
normal! zo
14837
normal! zo
14879
normal! zo
14885
normal! zo
14891
normal! zo
14898
normal! zo
14907
normal! zo
14909
normal! zo
14916
normal! zo
14916
normal! zo
14916
normal! zo
14916
normal! zo
14916
normal! zo
14916
normal! zo
14933
normal! zo
14945
normal! zo
14956
normal! zo
14957
normal! zo
14973
normal! zo
14990
normal! zo
14994
normal! zo
14995
normal! zo
14996
normal! zo
14996
normal! zo
14998
normal! zo
15001
normal! zo
15014
normal! zo
15024
normal! zo
15026
normal! zo
15030
normal! zo
15031
normal! zo
15031
normal! zo
15031
normal! zo
15031
normal! zo
15031
normal! zo
15031
normal! zo
15044
normal! zo
15065
normal! zo
15066
normal! zo
15073
normal! zo
15106
normal! zo
15107
normal! zo
15107
normal! zo
15123
normal! zo
15129
normal! zo
15132
normal! zo
15132
normal! zo
15132
normal! zo
15138
normal! zo
15138
normal! zo
15158
normal! zo
15163
normal! zo
15168
normal! zo
15176
normal! zo
15195
normal! zo
15229
normal! zo
15237
normal! zo
15246
normal! zo
15265
normal! zo
15267
normal! zo
15271
normal! zo
15288
normal! zo
15294
normal! zo
15298
normal! zo
15337
normal! zo
15441
normal! zo
15441
normal! zo
15517
normal! zo
15517
normal! zo
15517
normal! zo
15630
normal! zo
15661
normal! zo
15685
normal! zo
15695
normal! zo
15695
normal! zo
15695
normal! zo
15695
normal! zo
15695
normal! zo
15883
normal! zo
15902
normal! zo
15924
normal! zo
15929
normal! zo
15930
normal! zo
15930
normal! zo
15933
normal! zo
15934
normal! zo
15934
normal! zo
15934
normal! zo
15937
normal! zo
15937
normal! zo
15937
normal! zo
15941
normal! zo
15941
normal! zo
15941
normal! zo
15941
normal! zo
15941
normal! zo
15941
normal! zo
15941
normal! zo
15941
normal! zo
15941
normal! zo
16246
normal! zo
16404
normal! zo
16472
normal! zo
16508
normal! zo
16523
normal! zo
16529
normal! zo
16532
normal! zo
16540
normal! zo
16541
normal! zo
16541
normal! zo
16541
normal! zo
16541
normal! zo
16541
normal! zo
16545
normal! zo
16553
normal! zo
16556
normal! zo
16562
normal! zo
16568
normal! zo
16571
normal! zo
16577
normal! zo
16591
normal! zo
16597
normal! zo
16602
normal! zo
16605
normal! zo
16605
normal! zo
16605
normal! zo
16615
normal! zo
16630
normal! zo
16641
normal! zo
16641
normal! zo
16652
normal! zo
16667
normal! zo
16677
normal! zo
16688
normal! zo
16697
normal! zo
16704
normal! zo
16742
normal! zo
16747
normal! zo
16747
normal! zo
16747
normal! zo
16761
normal! zo
16761
normal! zo
16761
normal! zo
16761
normal! zo
16761
normal! zo
16761
normal! zo
16761
normal! zo
16761
normal! zo
16761
normal! zo
16761
normal! zo
16761
normal! zo
16773
normal! zo
16794
normal! zo
16813
normal! zo
16821
normal! zo
16822
normal! zo
16823
normal! zo
16827
normal! zo
16831
normal! zo
16847
normal! zo
16862
normal! zo
16867
normal! zo
16872
normal! zo
16882
normal! zo
16883
normal! zo
16883
normal! zo
16883
normal! zo
16885
normal! zo
16885
normal! zo
16885
normal! zo
16885
normal! zo
16885
normal! zo
16885
normal! zo
16885
normal! zo
16885
normal! zo
16885
normal! zo
16885
normal! zo
16890
normal! zo
16891
normal! zo
16897
normal! zo
16898
normal! zo
16918
normal! zo
16943
normal! zo
16947
normal! zo
16964
normal! zo
16975
normal! zo
16975
normal! zo
16975
normal! zo
16975
normal! zo
16977
normal! zo
16978
normal! zo
16979
normal! zo
16980
normal! zo
16981
normal! zo
16985
normal! zo
16986
normal! zo
16987
normal! zo
16987
normal! zo
16987
normal! zo
16987
normal! zo
16987
normal! zo
16987
normal! zo
16987
normal! zo
16989
normal! zo
16991
normal! zo
16996
normal! zo
16996
normal! zo
16996
normal! zo
16996
normal! zo
17002
normal! zo
17006
normal! zo
17014
normal! zo
17014
normal! zo
17014
normal! zo
17014
normal! zo
17022
normal! zo
17030
normal! zo
17031
normal! zo
17034
normal! zo
17039
normal! zo
17047
normal! zo
17052
normal! zo
17060
normal! zo
17065
normal! zo
17074
normal! zo
17075
normal! zo
17075
normal! zo
17085
normal! zo
17100
normal! zo
17101
normal! zo
17117
normal! zo
17137
normal! zo
17138
normal! zo
17138
normal! zo
17138
normal! zo
17138
normal! zo
17138
normal! zo
17144
normal! zo
17154
normal! zo
17168
normal! zo
17171
normal! zo
17175
normal! zo
17176
normal! zo
17177
normal! zo
17177
normal! zo
17177
normal! zo
17177
normal! zo
17177
normal! zo
17195
normal! zo
17202
normal! zo
17203
normal! zo
17210
normal! zo
17217
normal! zo
17218
normal! zo
17219
normal! zo
17224
normal! zo
17231
normal! zo
17236
normal! zo
17249
normal! zo
17250
normal! zo
17250
normal! zo
17250
normal! zo
17264
normal! zo
17277
normal! zo
17284
normal! zo
17285
normal! zo
17300
normal! zo
17307
normal! zo
17321
normal! zo
17328
normal! zo
17329
normal! zo
17334
normal! zo
17343
normal! zo
17357
normal! zo
17379
normal! zo
17400
normal! zo
17413
normal! zo
17413
normal! zo
17413
normal! zo
17413
normal! zo
17413
normal! zo
17413
normal! zo
17423
normal! zo
17436
normal! zo
17460
normal! zo
17465
normal! zo
17467
normal! zo
17470
normal! zo
17477
normal! zo
17489
normal! zo
17499
normal! zo
17499
normal! zo
17499
normal! zo
17499
normal! zo
17499
normal! zo
17499
normal! zo
17507
normal! zo
17517
normal! zo
17517
normal! zo
17517
normal! zo
17517
normal! zo
17517
normal! zo
17517
normal! zo
17525
normal! zo
17526
normal! zo
17537
normal! zo
17542
normal! zo
17553
normal! zo
17561
normal! zo
17574
normal! zo
17578
normal! zo
17578
normal! zo
17578
normal! zo
17578
normal! zo
17578
normal! zo
17580
normal! zo
17592
normal! zo
17592
normal! zo
17592
normal! zo
17592
normal! zo
17592
normal! zo
17592
normal! zo
17592
normal! zo
17596
normal! zo
17596
normal! zo
17596
normal! zo
17596
normal! zo
17596
normal! zo
17596
normal! zo
17602
normal! zo
17602
normal! zo
17602
normal! zo
17602
normal! zo
17605
normal! zo
17606
normal! zo
17607
normal! zo
17613
normal! zo
17614
normal! zo
17614
normal! zo
17614
normal! zo
17736
normal! zo
17791
normal! zo
17824
normal! zo
17881
normal! zo
17896
normal! zo
17903
normal! zo
17904
normal! zo
17920
normal! zo
17930
normal! zo
17944
normal! zo
17947
normal! zo
17948
normal! zo
17948
normal! zo
17970
normal! zo
17990
normal! zo
18002
normal! zo
18002
normal! zo
18002
normal! zo
18002
normal! zo
18002
normal! zo
18005
normal! zo
18012
normal! zo
18015
normal! zo
18026
normal! zo
18032
normal! zo
18037
normal! zo
18043
normal! zo
18044
normal! zo
18045
normal! zo
18048
normal! zo
18067
normal! zo
18082
normal! zo
18110
normal! zo
18135
normal! zo
18156
normal! zo
18191
normal! zo
18200
normal! zo
18201
normal! zo
18202
normal! zo
18204
normal! zo
18204
normal! zo
18204
normal! zo
18207
normal! zo
18209
normal! zo
18209
normal! zo
18209
normal! zo
18212
normal! zo
18213
normal! zo
18213
normal! zo
18213
normal! zo
18213
normal! zo
18213
normal! zo
18739
normal! zo
18756
normal! zo
18766
normal! zo
18769
normal! zo
18770
normal! zo
18770
normal! zo
18776
normal! zo
18783
normal! zo
18784
normal! zo
18785
normal! zo
18785
normal! zo
18785
normal! zo
18785
normal! zo
18789
normal! zo
18790
normal! zo
18790
normal! zo
18790
normal! zo
18790
normal! zo
18806
normal! zo
19107
normal! zo
20024
normal! zo
20048
normal! zo
20054
normal! zo
20060
normal! zo
20078
normal! zo
20088
normal! zo
20091
normal! zo
20098
normal! zo
20098
normal! zo
20098
normal! zo
20098
normal! zo
20103
normal! zo
20383
normal! zo
20389
normal! zo
20389
normal! zo
20398
normal! zo
20405
normal! zo
20412
normal! zo
20419
normal! zo
20426
normal! zo
20433
normal! zo
20440
normal! zo
20446
normal! zo
20447
normal! zo
20456
normal! zo
20465
normal! zo
20628
normal! zo
20638
normal! zo
20649
normal! zo
20660
normal! zo
20661
normal! zo
20666
normal! zo
20667
normal! zo
20667
normal! zo
20677
normal! zo
20677
normal! zo
20677
normal! zo
20677
normal! zo
20677
normal! zo
20677
normal! zo
20677
normal! zo
20677
normal! zo
20677
normal! zo
20688
normal! zo
20689
normal! zo
20697
normal! zo
20697
normal! zo
20697
normal! zo
20697
normal! zo
20697
normal! zo
20697
normal! zo
20697
normal! zo
20697
normal! zo
20708
normal! zo
20709
normal! zo
20717
normal! zo
20732
normal! zo
20765
normal! zo
20786
normal! zo
20791
normal! zo
20803
normal! zo
20803
normal! zo
20803
normal! zo
20803
normal! zo
20803
normal! zo
20803
normal! zo
20803
normal! zo
20821
normal! zo
20828
normal! zo
21318
normal! zo
let s:l = 9860 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
9860
normal! 026|
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
448
normal! zo
449
normal! zo
470
normal! zo
470
normal! zo
470
normal! zo
470
normal! zo
473
normal! zo
473
normal! zo
473
normal! zo
473
normal! zo
479
normal! zo
480
normal! zo
480
normal! zo
480
normal! zo
480
normal! zo
483
normal! zo
483
normal! zo
483
normal! zo
483
normal! zo
489
normal! zo
494
normal! zo
494
normal! zo
494
normal! zo
494
normal! zo
497
normal! zo
497
normal! zo
497
normal! zo
497
normal! zo
502
normal! zo
503
normal! zo
526
normal! zo
538
normal! zo
553
normal! zo
554
normal! zo
578
normal! zo
590
normal! zo
800
normal! zo
804
normal! zo
804
normal! zo
820
normal! zo
820
normal! zo
820
normal! zo
820
normal! zo
820
normal! zo
839
normal! zo
858
normal! zo
859
normal! zo
859
normal! zo
859
normal! zo
859
normal! zo
859
normal! zo
859
normal! zo
859
normal! zo
859
normal! zo
859
normal! zo
863
normal! zo
863
normal! zo
863
normal! zo
863
normal! zo
863
normal! zo
863
normal! zo
863
normal! zo
863
normal! zo
863
normal! zo
876
normal! zo
876
normal! zo
876
normal! zo
876
normal! zo
876
normal! zo
let s:l = 871 - ((23 * winheight(0) + 15) / 31)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
871
normal! 084|
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
let s:l = 52 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
52
normal! 0131|
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
380
normal! zo
383
normal! zo
383
normal! zo
383
normal! zo
383
normal! zo
383
normal! zo
383
normal! zo
383
normal! zo
383
normal! zo
383
normal! zo
383
normal! zo
383
normal! zo
383
normal! zo
385
normal! zo
389
normal! zo
397
normal! zo
398
normal! zo
398
normal! zo
399
normal! zo
403
normal! zo
405
normal! zo
407
normal! zo
411
normal! zo
416
normal! zo
417
normal! zo
417
normal! zo
417
normal! zo
417
normal! zo
421
normal! zo
427
normal! zo
427
normal! zo
427
normal! zo
427
normal! zo
430
normal! zo
435
normal! zo
436
normal! zo
436
normal! zo
436
normal! zo
436
normal! zo
440
normal! zo
445
normal! zo
445
normal! zo
445
normal! zo
445
normal! zo
448
normal! zo
449
normal! zo
470
normal! zo
470
normal! zo
470
normal! zo
470
normal! zo
473
normal! zo
473
normal! zo
473
normal! zo
473
normal! zo
479
normal! zo
480
normal! zo
480
normal! zo
480
normal! zo
480
normal! zo
483
normal! zo
483
normal! zo
483
normal! zo
483
normal! zo
489
normal! zo
494
normal! zo
494
normal! zo
494
normal! zo
494
normal! zo
497
normal! zo
497
normal! zo
497
normal! zo
497
normal! zo
502
normal! zo
503
normal! zo
506
normal! zo
519
normal! zo
519
normal! zo
519
normal! zo
519
normal! zo
521
normal! zo
521
normal! zo
521
normal! zo
521
normal! zo
526
normal! zo
527
normal! zo
527
normal! zo
527
normal! zo
527
normal! zo
531
normal! zo
531
normal! zo
531
normal! zo
531
normal! zo
538
normal! zo
543
normal! zo
543
normal! zo
543
normal! zo
543
normal! zo
547
normal! zo
547
normal! zo
547
normal! zo
547
normal! zo
553
normal! zo
554
normal! zo
557
normal! zo
571
normal! zo
571
normal! zo
571
normal! zo
571
normal! zo
573
normal! zo
573
normal! zo
573
normal! zo
573
normal! zo
578
normal! zo
579
normal! zo
579
normal! zo
579
normal! zo
579
normal! zo
583
normal! zo
583
normal! zo
583
normal! zo
583
normal! zo
590
normal! zo
595
normal! zo
595
normal! zo
595
normal! zo
595
normal! zo
600
normal! zo
600
normal! zo
600
normal! zo
600
normal! zo
606
normal! zo
607
normal! zo
609
normal! zo
609
normal! zo
609
normal! zo
609
normal! zo
609
normal! zo
609
normal! zo
609
normal! zo
609
normal! zo
609
normal! zo
609
normal! zo
609
normal! zo
609
normal! zo
609
normal! zo
629
normal! zo
649
normal! zo
655
normal! zo
661
normal! zo
662
normal! zo
671
normal! zo
676
normal! zo
681
normal! zo
681
normal! zo
685
normal! zo
687
normal! zo
687
normal! zo
687
normal! zo
700
normal! zo
701
normal! zo
702
normal! zo
708
normal! zo
709
normal! zo
713
normal! zo
719
normal! zo
719
normal! zo
719
normal! zo
719
normal! zo
719
normal! zo
731
normal! zo
734
normal! zo
734
normal! zo
734
normal! zo
734
normal! zo
740
normal! zo
751
normal! zo
765
normal! zo
766
normal! zo
776
normal! zo
778
normal! zo
784
normal! zo
788
normal! zo
788
normal! zo
800
normal! zo
804
normal! zo
804
normal! zo
820
normal! zo
820
normal! zo
820
normal! zo
820
normal! zo
820
normal! zo
839
normal! zo
840
normal! zo
840
normal! zo
858
normal! zo
859
normal! zo
859
normal! zo
859
normal! zo
859
normal! zo
859
normal! zo
859
normal! zo
859
normal! zo
859
normal! zo
859
normal! zo
863
normal! zo
863
normal! zo
863
normal! zo
863
normal! zo
863
normal! zo
863
normal! zo
863
normal! zo
863
normal! zo
863
normal! zo
876
normal! zo
876
normal! zo
876
normal! zo
876
normal! zo
876
normal! zo
896
normal! zo
let s:l = 1 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 012|
wincmd w
7wincmd w
exe '1resize ' . ((&lines * 3 + 25) / 51)
exe 'vert 1resize ' . ((&columns * 32 + 56) / 113)
exe '2resize ' . ((&lines * 45 + 25) / 51)
exe 'vert 2resize ' . ((&columns * 32 + 56) / 113)
exe '3resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 3resize ' . ((&columns * 80 + 56) / 113)
exe '4resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 4resize ' . ((&columns * 80 + 56) / 113)
exe '5resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 5resize ' . ((&columns * 80 + 56) / 113)
exe '6resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 6resize ' . ((&columns * 80 + 56) / 113)
exe '7resize ' . ((&lines * 31 + 25) / 51)
exe 'vert 7resize ' . ((&columns * 80 + 56) / 113)
exe '8resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 8resize ' . ((&columns * 80 + 56) / 113)
exe '9resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 9resize ' . ((&columns * 80 + 56) / 113)
exe '10resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 10resize ' . ((&columns * 80 + 56) / 113)
exe '11resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 11resize ' . ((&columns * 80 + 56) / 113)
exe '12resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 12resize ' . ((&columns * 80 + 56) / 113)
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
