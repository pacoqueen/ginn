" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 06 marzo 2014 at 17:29:52.
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
exe '1resize ' . ((&lines * 3 + 25) / 51)
exe 'vert 1resize ' . ((&columns * 34 + 57) / 115)
exe '2resize ' . ((&lines * 45 + 25) / 51)
exe 'vert 2resize ' . ((&columns * 34 + 57) / 115)
exe '3resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 3resize ' . ((&columns * 80 + 57) / 115)
exe '4resize ' . ((&lines * 11 + 25) / 51)
exe 'vert 4resize ' . ((&columns * 80 + 57) / 115)
exe '5resize ' . ((&lines * 25 + 25) / 51)
exe 'vert 5resize ' . ((&columns * 80 + 57) / 115)
exe '6resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 6resize ' . ((&columns * 80 + 57) / 115)
exe '7resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 7resize ' . ((&columns * 80 + 57) / 115)
exe '8resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 8resize ' . ((&columns * 80 + 57) / 115)
exe '9resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 9resize ' . ((&columns * 80 + 57) / 115)
exe '10resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 10resize ' . ((&columns * 80 + 57) / 115)
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
7231
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
9857
normal! zo
9871
normal! zo
9887
normal! zo
9904
normal! zo
9904
normal! zo
9904
normal! zo
9904
normal! zo
9904
normal! zo
9904
normal! zo
9904
normal! zo
9904
normal! zo
9904
normal! zo
9911
normal! zo
9925
normal! zo
9926
normal! zo
9926
normal! zo
9928
normal! zo
9929
normal! zo
9929
normal! zo
9931
normal! zo
9932
normal! zo
9932
normal! zo
9934
normal! zo
9935
normal! zo
9935
normal! zo
9937
normal! zo
9940
normal! zo
9942
normal! zo
9942
normal! zo
9942
normal! zo
9951
normal! zo
9964
normal! zo
9967
normal! zo
9968
normal! zo
9968
normal! zo
9971
normal! zo
9971
normal! zo
9971
normal! zo
9974
normal! zo
9974
normal! zo
9974
normal! zo
9974
normal! zo
9980
normal! zo
9983
normal! zo
9987
normal! zo
9994
normal! zo
9996
normal! zo
10043
normal! zo
10057
normal! zo
10058
normal! zo
10060
normal! zo
10095
normal! zo
10102
normal! zo
10107
normal! zo
10108
normal! zo
10113
normal! zo
10113
normal! zo
10113
normal! zo
10113
normal! zo
10113
normal! zo
10116
normal! zo
10116
normal! zo
10116
normal! zo
10142
normal! zo
10151
normal! zo
10156
normal! zo
10158
normal! zo
10163
normal! zo
10169
normal! zo
10177
normal! zo
10178
normal! zo
10178
normal! zo
10178
normal! zo
10178
normal! zo
10187
normal! zo
10188
normal! zo
10193
normal! zo
10242
normal! zo
10247
normal! zo
10360
normal! zo
10387
normal! zo
10392
normal! zo
10398
normal! zo
10484
normal! zo
10491
normal! zo
10492
normal! zo
10540
normal! zo
10540
normal! zo
10540
normal! zo
10540
normal! zo
10540
normal! zo
10543
normal! zo
10551
normal! zo
10552
normal! zo
10597
normal! zo
10617
normal! zo
10618
normal! zo
10619
normal! zo
10619
normal! zo
10619
normal! zo
10619
normal! zo
10619
normal! zo
10619
normal! zo
10619
normal! zo
10619
normal! zo
10619
normal! zo
10636
normal! zo
10642
normal! zo
10652
normal! zo
10667
normal! zo
10670
normal! zo
10673
normal! zo
10673
normal! zo
10673
normal! zo
10676
normal! zo
10676
normal! zo
10676
normal! zo
10676
normal! zo
10681
normal! zo
10681
normal! zo
10681
normal! zo
10689
normal! zo
10696
normal! zo
10703
normal! zo
10706
normal! zo
10708
normal! zo
10711
normal! zo
10714
normal! zo
10719
normal! zo
10730
normal! zo
10737
normal! zo
10741
normal! zo
10742
normal! zo
10742
normal! zo
10744
normal! zo
10745
normal! zo
10745
normal! zo
10747
normal! zo
10748
normal! zo
10748
normal! zo
10750
normal! zo
10751
normal! zo
10751
normal! zo
10753
normal! zo
10754
normal! zo
10754
normal! zo
10756
normal! zo
10757
normal! zo
10757
normal! zo
10759
normal! zo
10760
normal! zo
10760
normal! zo
10762
normal! zo
10765
normal! zo
10767
normal! zo
10767
normal! zo
10767
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
10801
normal! zo
10805
normal! zo
10808
normal! zo
10809
normal! zo
10809
normal! zo
10809
normal! zo
10809
normal! zo
10809
normal! zo
10809
normal! zo
10814
normal! zo
10815
normal! zo
10815
normal! zo
10815
normal! zo
10818
normal! zo
10930
normal! zo
11006
normal! zo
11014
normal! zo
11021
normal! zo
11021
normal! zo
11021
normal! zo
11021
normal! zo
11021
normal! zo
11021
normal! zo
11021
normal! zo
11032
normal! zo
11036
normal! zo
11037
normal! zo
11037
normal! zo
11037
normal! zo
11047
normal! zo
11050
normal! zo
11057
normal! zo
11066
normal! zo
11075
normal! zo
11185
normal! zo
11186
normal! zc
11199
normal! zo
11199
normal! zo
11199
normal! zo
11199
normal! zo
11208
normal! zc
11211
normal! zo
11224
normal! zo
11237
normal! zo
11244
normal! zo
11246
normal! zo
11246
normal! zo
11246
normal! zo
11246
normal! zo
11246
normal! zo
11246
normal! zo
11254
normal! zc
11271
normal! zo
11299
normal! zo
11311
normal! zo
11312
normal! zo
11312
normal! zo
11312
normal! zo
11312
normal! zo
11271
normal! zc
11317
normal! zo
11317
normal! zc
11368
normal! zo
11368
normal! zc
11483
normal! zo
11491
normal! zo
11491
normal! zo
11491
normal! zo
11491
normal! zo
11483
normal! zc
11499
normal! zc
11505
normal! zo
11505
normal! zc
11516
normal! zo
11516
normal! zc
11533
normal! zo
11533
normal! zo
11537
normal! zo
11542
normal! zo
11542
normal! zo
11544
normal! zo
11545
normal! zo
11545
normal! zo
11550
normal! zo
11550
normal! zo
11550
normal! zo
11550
normal! zo
11550
normal! zo
11550
normal! zc
11563
normal! zo
11566
normal! zo
11566
normal! zo
11566
normal! zo
11566
normal! zo
11572
normal! zo
11572
normal! zo
11572
normal! zo
11572
normal! zo
11572
normal! zo
11572
normal! zc
11600
normal! zo
11638
normal! zc
11645
normal! zc
11653
normal! zo
11653
normal! zc
11661
normal! zc
11669
normal! zc
11683
normal! zo
11683
normal! zc
11701
normal! zo
11701
normal! zo
11701
normal! zo
11701
normal! zo
11701
normal! zo
11701
normal! zo
11701
normal! zo
11701
normal! zo
11701
normal! zo
11701
normal! zo
11701
normal! zc
11722
normal! zo
11722
normal! zo
11722
normal! zo
11722
normal! zo
11722
normal! zo
11722
normal! zo
11763
normal! zo
11764
normal! zo
11786
normal! zo
11786
normal! zc
11893
normal! zo
11893
normal! zc
11942
normal! zo
11942
normal! zo
11944
normal! zo
11954
normal! zo
11942
normal! zc
12037
normal! zo
12037
normal! zc
12091
normal! zo
12091
normal! zo
12091
normal! zo
12091
normal! zc
12091
normal! zc
12105
normal! zo
12142
normal! zo
12153
normal! zo
12158
normal! zo
12176
normal! zo
12176
normal! zo
12176
normal! zo
12176
normal! zo
12177
normal! zo
12182
normal! zo
12198
normal! zo
12198
normal! zo
12198
normal! zo
12198
normal! zo
12207
normal! zo
12207
normal! zo
12207
normal! zo
12207
normal! zo
12207
normal! zo
12231
normal! zo
12255
normal! zo
12255
normal! zc
12296
normal! zo
12296
normal! zo
12296
normal! zo
12296
normal! zo
12358
normal! zo
12374
normal! zo
12374
normal! zc
12398
normal! zo
12398
normal! zo
12398
normal! zo
12398
normal! zc
12423
normal! zo
12423
normal! zo
12423
normal! zo
12423
normal! zc
12498
normal! zo
12498
normal! zo
12498
normal! zo
12498
normal! zo
12498
normal! zo
12498
normal! zo
12498
normal! zo
12498
normal! zo
12498
normal! zc
12514
normal! zo
12514
normal! zc
12536
normal! zo
12536
normal! zc
12557
normal! zo
12557
normal! zo
12557
normal! zo
12557
normal! zo
12557
normal! zo
12557
normal! zo
12557
normal! zo
12557
normal! zc
12557
normal! zc
12677
normal! zo
12677
normal! zo
12677
normal! zo
12677
normal! zo
12677
normal! zo
12677
normal! zc
12945
normal! zo
12945
normal! zc
12975
normal! zo
12975
normal! zo
12975
normal! zo
12975
normal! zo
12975
normal! zo
12975
normal! zo
12975
normal! zo
12975
normal! zo
12990
normal! zo
13005
normal! zo
13007
normal! zo
13029
normal! zo
13037
normal! zo
13037
normal! zc
13053
normal! zo
13053
normal! zo
13092
normal! zo
13154
normal! zo
13155
normal! zo
13173
normal! zo
13215
normal! zo
13216
normal! zo
13244
normal! zo
13276
normal! zo
13277
normal! zo
13305
normal! zo
13341
normal! zo
13342
normal! zo
13360
normal! zo
13387
normal! zc
13397
normal! zo
13397
normal! zc
13417
normal! zo
13418
normal! zo
13419
normal! zo
13417
normal! zc
13473
normal! zo
13473
normal! zc
13531
normal! zo
13531
normal! zo
13531
normal! zo
13541
normal! zo
13546
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
13548
normal! zo
13548
normal! zo
13548
normal! zo
13548
normal! zo
13548
normal! zo
13548
normal! zo
13554
normal! zo
13555
normal! zo
13556
normal! zo
13556
normal! zo
13556
normal! zo
13556
normal! zo
13556
normal! zo
13556
normal! zo
13556
normal! zo
13558
normal! zo
13558
normal! zo
13558
normal! zo
13558
normal! zo
13558
normal! zo
13558
normal! zo
13558
normal! zo
13558
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
13561
normal! zo
13561
normal! zo
13564
normal! zo
13566
normal! zo
13566
normal! zo
13571
normal! zo
13571
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
13589
normal! zo
13589
normal! zo
13589
normal! zo
13595
normal! zo
13596
normal! zo
13605
normal! zo
13606
normal! zo
13606
normal! zo
13606
normal! zo
13606
normal! zo
13610
normal! zo
13610
normal! zo
13610
normal! zo
13618
normal! zo
13619
normal! zo
13621
normal! zo
13629
normal! zo
13630
normal! zo
13630
normal! zo
13630
normal! zo
13630
normal! zo
13634
normal! zo
13634
normal! zo
13634
normal! zo
13641
normal! zo
13641
normal! zo
13641
normal! zo
13641
normal! zo
13641
normal! zo
13644
normal! zo
13645
normal! zo
13646
normal! zo
13647
normal! zo
13647
normal! zo
13648
normal! zo
13660
normal! zo
13661
normal! zo
13661
normal! zo
13661
normal! zo
13668
normal! zo
13669
normal! zo
13670
normal! zo
13670
normal! zo
13671
normal! zo
13682
normal! zo
13683
normal! zo
13684
normal! zo
13684
normal! zo
13685
normal! zo
13700
normal! zo
13701
normal! zo
13702
normal! zo
13703
normal! zo
13703
normal! zo
13704
normal! zo
13716
normal! zo
13717
normal! zo
13717
normal! zo
13717
normal! zo
13718
normal! zo
13724
normal! zo
13725
normal! zo
13726
normal! zo
13726
normal! zo
13727
normal! zo
13738
normal! zo
13739
normal! zo
13740
normal! zo
13740
normal! zo
13741
normal! zo
13756
normal! zo
13756
normal! zo
13756
normal! zo
13777
normal! zo
13782
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
13784
normal! zo
13790
normal! zo
13791
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
13797
normal! zo
13797
normal! zo
13800
normal! zo
13802
normal! zo
13807
normal! zo
13816
normal! zo
13817
normal! zo
13817
normal! zo
13817
normal! zo
13817
normal! zo
13817
normal! zo
13817
normal! zo
13817
normal! zo
13824
normal! zo
13826
normal! zo
13827
normal! zo
13828
normal! zo
13828
normal! zo
13829
normal! zo
13839
normal! zo
13840
normal! zo
13841
normal! zo
13841
normal! zo
13842
normal! zo
13856
normal! zo
13857
normal! zo
13858
normal! zo
13859
normal! zo
13859
normal! zo
13860
normal! zo
13870
normal! zo
13871
normal! zo
13872
normal! zo
13872
normal! zo
13873
normal! zo
13887
normal! zo
13887
normal! zo
13887
normal! zo
13898
normal! zo
13903
normal! zo
13904
normal! zo
13905
normal! zo
13905
normal! zo
13905
normal! zo
13905
normal! zo
13905
normal! zo
13905
normal! zo
13905
normal! zo
13905
normal! zo
13905
normal! zo
13905
normal! zo
13911
normal! zo
13912
normal! zo
13913
normal! zo
13913
normal! zo
13913
normal! zo
13913
normal! zo
13913
normal! zo
13913
normal! zo
13913
normal! zo
13915
normal! zo
13915
normal! zo
13915
normal! zo
13915
normal! zo
13915
normal! zo
13915
normal! zo
13915
normal! zo
13915
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
13918
normal! zo
13918
normal! zo
13921
normal! zo
13923
normal! zo
13928
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
13950
normal! zo
13951
normal! zo
13952
normal! zo
13959
normal! zo
13960
normal! zo
13961
normal! zo
13967
normal! zo
13968
normal! zo
13969
normal! zo
13974
normal! zo
13975
normal! zo
13976
normal! zo
13976
normal! zo
13986
normal! zo
13987
normal! zo
13988
normal! zo
13988
normal! zo
13988
normal! zo
13988
normal! zo
13988
normal! zo
13988
normal! zo
13995
normal! zo
13996
normal! zo
13996
normal! zo
13996
normal! zo
13996
normal! zo
13996
normal! zo
13996
normal! zo
13996
normal! zo
14003
normal! zo
14004
normal! zo
14004
normal! zo
14004
normal! zo
14004
normal! zo
14004
normal! zo
14004
normal! zo
14004
normal! zo
14010
normal! zo
14011
normal! zo
14011
normal! zo
14011
normal! zo
14011
normal! zo
14011
normal! zo
14011
normal! zo
14011
normal! zo
14021
normal! zo
14027
normal! zo
14027
normal! zo
14033
normal! zo
14039
normal! zo
14045
normal! zo
14045
normal! zo
14045
normal! zo
14045
normal! zo
14045
normal! zo
14045
normal! zo
14045
normal! zo
14045
normal! zo
14045
normal! zo
14055
normal! zo
14055
normal! zo
14055
normal! zo
14055
normal! zo
14055
normal! zo
14055
normal! zo
14057
normal! zo
14058
normal! zo
14058
normal! zo
14058
normal! zo
14064
normal! zo
14064
normal! zo
14064
normal! zo
14064
normal! zo
14064
normal! zo
14064
normal! zo
14064
normal! zo
14064
normal! zo
14064
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
14077
normal! zo
14078
normal! zo
14078
normal! zo
14078
normal! zo
14084
normal! zo
14084
normal! zo
14084
normal! zo
14084
normal! zo
14092
normal! zo
14097
normal! zo
14100
normal! zo
14105
normal! zo
14106
normal! zo
14107
normal! zo
14107
normal! zo
14107
normal! zo
14107
normal! zo
14107
normal! zo
14107
normal! zo
14107
normal! zo
14107
normal! zo
14107
normal! zo
14107
normal! zo
14113
normal! zo
14114
normal! zo
14117
normal! zo
14118
normal! zo
14118
normal! zo
14118
normal! zo
14118
normal! zo
14118
normal! zo
14118
normal! zo
14118
normal! zo
14120
normal! zo
14120
normal! zo
14120
normal! zo
14120
normal! zo
14120
normal! zo
14120
normal! zo
14120
normal! zo
14120
normal! zo
14120
normal! zo
14122
normal! zo
14123
normal! zo
14126
normal! zo
14126
normal! zo
14126
normal! zo
14126
normal! zo
14126
normal! zo
14126
normal! zo
14126
normal! zo
14126
normal! zo
14126
normal! zo
14129
normal! zo
14130
normal! zo
14134
normal! zo
14134
normal! zo
14139
normal! zo
14139
normal! zo
14144
normal! zo
14145
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
14163
normal! zo
14164
normal! zo
14165
normal! zo
14166
normal! zo
14172
normal! zo
14173
normal! zo
14174
normal! zo
14180
normal! zo
14181
normal! zo
14181
normal! zo
14182
normal! zo
14187
normal! zo
14188
normal! zo
14188
normal! zo
14189
normal! zo
14198
normal! zo
14199
normal! zo
14200
normal! zo
14200
normal! zo
14200
normal! zo
14200
normal! zo
14200
normal! zo
14200
normal! zo
14207
normal! zo
14208
normal! zo
14209
normal! zo
14215
normal! zo
14216
normal! zo
14216
normal! zo
14216
normal! zo
14216
normal! zo
14216
normal! zo
14216
normal! zo
14216
normal! zo
14222
normal! zo
14223
normal! zo
14223
normal! zo
14223
normal! zo
14223
normal! zo
14223
normal! zo
14223
normal! zo
14223
normal! zo
14234
normal! zo
14235
normal! zo
14235
normal! zo
14241
normal! zo
14247
normal! zo
14247
normal! zo
14253
normal! zo
14253
normal! zo
14253
normal! zo
14253
normal! zo
14269
normal! zo
14274
normal! zo
14275
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
14276
normal! zo
14282
normal! zo
14283
normal! zo
14284
normal! zo
14284
normal! zo
14284
normal! zo
14284
normal! zo
14284
normal! zo
14284
normal! zo
14284
normal! zo
14286
normal! zo
14286
normal! zo
14286
normal! zo
14286
normal! zo
14286
normal! zo
14286
normal! zo
14286
normal! zo
14286
normal! zo
14286
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
14289
normal! zo
14289
normal! zo
14292
normal! zo
14294
normal! zo
14294
normal! zo
14299
normal! zo
14299
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
14317
normal! zo
14318
normal! zo
14319
normal! zo
14320
normal! zo
14325
normal! zo
14326
normal! zo
14327
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
14344
normal! zo
14345
normal! zo
14345
normal! zo
14345
normal! zo
14346
normal! zo
14356
normal! zo
14357
normal! zo
14357
normal! zo
14363
normal! zo
14364
normal! zo
14364
normal! zo
14370
normal! zo
14370
normal! zo
14370
normal! zo
14370
normal! zo
14382
normal! zo
14387
normal! zo
14388
normal! zo
14389
normal! zo
14389
normal! zo
14389
normal! zo
14389
normal! zo
14389
normal! zo
14389
normal! zo
14389
normal! zo
14389
normal! zo
14389
normal! zo
14389
normal! zo
14395
normal! zo
14396
normal! zo
14397
normal! zo
14397
normal! zo
14397
normal! zo
14397
normal! zo
14397
normal! zo
14397
normal! zo
14397
normal! zo
14399
normal! zo
14399
normal! zo
14399
normal! zo
14399
normal! zo
14399
normal! zo
14399
normal! zo
14399
normal! zo
14399
normal! zo
14399
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
14402
normal! zo
14402
normal! zo
14405
normal! zo
14407
normal! zo
14407
normal! zo
14412
normal! zo
14412
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
14430
normal! zo
14437
normal! zo
14438
normal! zo
14440
normal! zo
14440
normal! zo
14440
normal! zo
14446
normal! zo
14448
normal! zo
14450
normal! zo
14456
normal! zo
14458
normal! zo
14460
normal! zo
14471
normal! zo
14491
normal! zo
14503
normal! zo
14506
normal! zo
14507
normal! zo
14508
normal! zo
14508
normal! zo
14508
normal! zo
14510
normal! zo
14511
normal! zo
14511
normal! zo
14511
normal! zo
14527
normal! zo
14538
normal! zo
14547
normal! zo
14557
normal! zo
14584
normal! zo
14589
normal! zo
14595
normal! zo
14606
normal! zo
14619
normal! zo
14643
normal! zo
14645
normal! zo
14648
normal! zo
14651
normal! zo
14652
normal! zo
14656
normal! zo
14657
normal! zo
14671
normal! zo
14671
normal! zo
14671
normal! zo
14671
normal! zo
14693
normal! zo
14694
normal! zo
14695
normal! zo
14695
normal! zo
14695
normal! zo
14695
normal! zo
14695
normal! zo
14695
normal! zo
14695
normal! zo
14695
normal! zo
14695
normal! zo
14695
normal! zo
14704
normal! zo
14705
normal! zo
14711
normal! zo
14715
normal! zo
14716
normal! zo
14725
normal! zo
14726
normal! zo
14734
normal! zo
14735
normal! zo
14741
normal! zo
14756
normal! zo
14764
normal! zo
14770
normal! zo
14776
normal! zo
14781
normal! zo
14785
normal! zo
14791
normal! zo
14796
normal! zo
14797
normal! zo
14802
normal! zo
14813
normal! zo
14831
normal! zo
14873
normal! zo
14879
normal! zo
14885
normal! zo
14892
normal! zo
14901
normal! zo
14903
normal! zo
14910
normal! zo
14910
normal! zo
14910
normal! zo
14910
normal! zo
14910
normal! zo
14910
normal! zo
14927
normal! zo
14939
normal! zo
14950
normal! zo
14951
normal! zo
14967
normal! zo
14984
normal! zo
14988
normal! zo
14989
normal! zo
14990
normal! zo
14990
normal! zo
14992
normal! zo
14995
normal! zo
15008
normal! zo
15018
normal! zo
15020
normal! zo
15024
normal! zo
15025
normal! zo
15025
normal! zo
15025
normal! zo
15025
normal! zo
15025
normal! zo
15025
normal! zo
15038
normal! zo
15059
normal! zo
15060
normal! zo
15067
normal! zo
15100
normal! zo
15101
normal! zo
15101
normal! zo
15117
normal! zo
15123
normal! zo
15126
normal! zo
15126
normal! zo
15126
normal! zo
15132
normal! zo
15132
normal! zo
15152
normal! zo
15157
normal! zo
15162
normal! zo
15170
normal! zo
15189
normal! zo
15223
normal! zo
15231
normal! zo
15240
normal! zo
15259
normal! zo
15261
normal! zo
15265
normal! zo
15282
normal! zo
15288
normal! zo
15292
normal! zo
15331
normal! zo
15435
normal! zo
15435
normal! zo
15511
normal! zo
15511
normal! zo
15511
normal! zo
15624
normal! zo
15655
normal! zo
15679
normal! zo
15689
normal! zo
15689
normal! zo
15689
normal! zo
15689
normal! zo
15689
normal! zo
15877
normal! zo
15896
normal! zo
15918
normal! zo
15923
normal! zo
15924
normal! zo
15924
normal! zo
15927
normal! zo
15928
normal! zo
15928
normal! zo
15928
normal! zo
15931
normal! zo
15931
normal! zo
15931
normal! zo
15935
normal! zo
15935
normal! zo
15935
normal! zo
15935
normal! zo
15935
normal! zo
15935
normal! zo
15935
normal! zo
15935
normal! zo
15935
normal! zo
16466
normal! zo
16502
normal! zo
16517
normal! zo
16523
normal! zo
16526
normal! zo
16534
normal! zo
16535
normal! zo
16535
normal! zo
16535
normal! zo
16535
normal! zo
16535
normal! zo
16539
normal! zo
16547
normal! zo
16550
normal! zo
16556
normal! zo
16562
normal! zo
16565
normal! zo
16571
normal! zo
16585
normal! zo
16591
normal! zo
16596
normal! zo
16599
normal! zo
16599
normal! zo
16599
normal! zo
16609
normal! zo
16624
normal! zo
16635
normal! zo
16635
normal! zo
16646
normal! zo
16661
normal! zo
16671
normal! zo
16682
normal! zo
16691
normal! zo
16698
normal! zo
16736
normal! zo
16741
normal! zo
16741
normal! zo
16741
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
16754
normal! zo
16766
normal! zo
16787
normal! zo
16806
normal! zo
16814
normal! zo
16815
normal! zo
16816
normal! zo
16820
normal! zo
16824
normal! zo
16840
normal! zo
16855
normal! zo
16860
normal! zo
16865
normal! zo
16875
normal! zo
16876
normal! zo
16876
normal! zo
16876
normal! zo
16878
normal! zo
16878
normal! zo
16878
normal! zo
16878
normal! zo
16878
normal! zo
16878
normal! zo
16878
normal! zo
16878
normal! zo
16878
normal! zo
16878
normal! zo
16883
normal! zo
16884
normal! zo
16890
normal! zo
16891
normal! zo
16911
normal! zo
16936
normal! zo
16940
normal! zo
16957
normal! zo
16968
normal! zo
16968
normal! zo
16968
normal! zo
16968
normal! zo
16970
normal! zo
16971
normal! zo
16972
normal! zo
16973
normal! zo
16974
normal! zo
16978
normal! zo
16979
normal! zo
16980
normal! zo
16980
normal! zo
16980
normal! zo
16980
normal! zo
16980
normal! zo
16980
normal! zo
16980
normal! zo
16982
normal! zo
16984
normal! zo
16989
normal! zo
16989
normal! zo
16989
normal! zo
16989
normal! zo
16995
normal! zo
16999
normal! zo
17007
normal! zo
17007
normal! zo
17007
normal! zo
17007
normal! zo
17015
normal! zo
17023
normal! zo
17024
normal! zo
17027
normal! zo
17032
normal! zo
17040
normal! zo
17045
normal! zo
17053
normal! zo
17058
normal! zo
17067
normal! zo
17068
normal! zo
17068
normal! zo
17078
normal! zo
17093
normal! zo
17094
normal! zo
17110
normal! zo
17130
normal! zo
17131
normal! zo
17131
normal! zo
17131
normal! zo
17131
normal! zo
17131
normal! zo
17137
normal! zo
17147
normal! zo
17161
normal! zo
17164
normal! zo
17168
normal! zo
17169
normal! zo
17170
normal! zo
17170
normal! zo
17170
normal! zo
17170
normal! zo
17170
normal! zo
17188
normal! zo
17195
normal! zo
17196
normal! zo
17203
normal! zo
17210
normal! zo
17211
normal! zo
17212
normal! zo
17217
normal! zo
17224
normal! zo
17229
normal! zo
17242
normal! zo
17243
normal! zo
17243
normal! zo
17243
normal! zo
17257
normal! zo
17270
normal! zo
17277
normal! zo
17278
normal! zo
17293
normal! zo
17300
normal! zo
17314
normal! zo
17321
normal! zo
17322
normal! zo
17327
normal! zo
17336
normal! zo
17350
normal! zo
17372
normal! zo
17393
normal! zo
17406
normal! zo
17406
normal! zo
17406
normal! zo
17406
normal! zo
17406
normal! zo
17406
normal! zo
17416
normal! zo
17429
normal! zo
17453
normal! zo
17458
normal! zo
17460
normal! zo
17463
normal! zo
17470
normal! zo
17482
normal! zo
17492
normal! zo
17492
normal! zo
17492
normal! zo
17492
normal! zo
17492
normal! zo
17492
normal! zo
17500
normal! zo
17510
normal! zo
17510
normal! zo
17510
normal! zo
17510
normal! zo
17510
normal! zo
17510
normal! zo
17518
normal! zo
17519
normal! zo
17530
normal! zo
17535
normal! zo
17546
normal! zo
17554
normal! zo
17567
normal! zo
17571
normal! zo
17571
normal! zo
17571
normal! zo
17571
normal! zo
17571
normal! zo
17573
normal! zo
17585
normal! zo
17585
normal! zo
17585
normal! zo
17585
normal! zo
17585
normal! zo
17585
normal! zo
17585
normal! zo
17589
normal! zo
17589
normal! zo
17589
normal! zo
17589
normal! zo
17589
normal! zo
17589
normal! zo
17595
normal! zo
17595
normal! zo
17595
normal! zo
17595
normal! zo
17598
normal! zo
17599
normal! zo
17600
normal! zo
17606
normal! zo
17607
normal! zo
17607
normal! zo
17607
normal! zo
17729
normal! zo
17784
normal! zo
17817
normal! zo
17874
normal! zo
17889
normal! zo
17896
normal! zo
17897
normal! zo
17913
normal! zo
17923
normal! zo
17937
normal! zo
17940
normal! zo
17941
normal! zo
17941
normal! zo
17963
normal! zo
17983
normal! zo
17995
normal! zo
17995
normal! zo
17995
normal! zo
17995
normal! zo
17995
normal! zo
17998
normal! zo
18005
normal! zo
18008
normal! zo
18019
normal! zo
18025
normal! zo
18030
normal! zo
18036
normal! zo
18037
normal! zo
18038
normal! zo
18041
normal! zo
18060
normal! zo
18075
normal! zo
18103
normal! zo
18128
normal! zo
18149
normal! zo
18184
normal! zo
18193
normal! zo
18194
normal! zo
18195
normal! zo
18197
normal! zo
18197
normal! zo
18197
normal! zo
18200
normal! zo
18202
normal! zo
18202
normal! zo
18202
normal! zo
18205
normal! zo
18206
normal! zo
18206
normal! zo
18206
normal! zo
18206
normal! zo
18206
normal! zo
18732
normal! zo
18749
normal! zo
18759
normal! zo
18762
normal! zo
18763
normal! zo
18763
normal! zo
18769
normal! zo
18776
normal! zo
18777
normal! zo
18778
normal! zo
18778
normal! zo
18778
normal! zo
18778
normal! zo
18782
normal! zo
18783
normal! zo
18783
normal! zo
18783
normal! zo
18783
normal! zo
18799
normal! zo
19100
normal! zo
20017
normal! zo
20041
normal! zo
20047
normal! zo
20053
normal! zo
20071
normal! zo
20081
normal! zo
20084
normal! zo
20091
normal! zo
20091
normal! zo
20091
normal! zo
20091
normal! zo
20096
normal! zo
20376
normal! zo
20382
normal! zo
20382
normal! zo
20391
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
20439
normal! zo
20440
normal! zo
20449
normal! zo
20458
normal! zo
20621
normal! zo
20631
normal! zo
20642
normal! zo
20653
normal! zo
20654
normal! zo
20659
normal! zo
20660
normal! zo
20660
normal! zo
20670
normal! zo
20670
normal! zo
20670
normal! zo
20670
normal! zo
20670
normal! zo
20670
normal! zo
20670
normal! zo
20670
normal! zo
20670
normal! zo
20681
normal! zo
20682
normal! zo
20690
normal! zo
20690
normal! zo
20690
normal! zo
20690
normal! zo
20690
normal! zo
20690
normal! zo
20690
normal! zo
20690
normal! zo
20701
normal! zo
20702
normal! zo
20710
normal! zo
20725
normal! zo
20758
normal! zo
20779
normal! zo
20784
normal! zo
20796
normal! zo
20796
normal! zo
20796
normal! zo
20796
normal! zo
20796
normal! zo
20796
normal! zo
20796
normal! zo
20814
normal! zo
20821
normal! zo
21311
normal! zo
let s:l = 7223 - ((10 * winheight(0) + 5) / 11)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
7223
normal! 030|
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
166
normal! zo
182
normal! zo
183
normal! zo
183
normal! zo
183
normal! zo
183
normal! zo
183
normal! zo
193
normal! zo
197
normal! zo
203
normal! zo
217
normal! zo
217
normal! zo
217
normal! zo
217
normal! zo
217
normal! zo
217
normal! zo
229
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
240
normal! zo
247
normal! zo
248
normal! zo
248
normal! zo
248
normal! zo
248
normal! zo
270
normal! zo
284
normal! zo
288
normal! zo
289
normal! zo
290
normal! zo
294
normal! zo
316
normal! zo
321
normal! zo
354
normal! zo
360
normal! zo
360
normal! zo
360
normal! zo
360
normal! zo
360
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
363
normal! zo
396
normal! zo
413
normal! zo
419
normal! zo
424
normal! zo
437
normal! zo
443
normal! zo
let s:l = 171 - ((11 * winheight(0) + 12) / 25)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
171
normal! 0199|
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
let s:l = 43 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
43
normal! 029|
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
let s:l = 173 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
173
normal! 032|
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
461
normal! zo
461
normal! zo
461
normal! zo
461
normal! zo
467
normal! zo
472
normal! zo
472
normal! zo
472
normal! zo
472
normal! zo
475
normal! zo
475
normal! zo
475
normal! zo
475
normal! zo
480
normal! zo
481
normal! zo
484
normal! zo
497
normal! zo
497
normal! zo
497
normal! zo
497
normal! zo
499
normal! zo
499
normal! zo
499
normal! zo
499
normal! zo
504
normal! zo
505
normal! zo
505
normal! zo
505
normal! zo
505
normal! zo
509
normal! zo
509
normal! zo
509
normal! zo
509
normal! zo
516
normal! zo
521
normal! zo
521
normal! zo
521
normal! zo
521
normal! zo
525
normal! zo
525
normal! zo
525
normal! zo
525
normal! zo
531
normal! zo
532
normal! zo
535
normal! zo
549
normal! zo
549
normal! zo
549
normal! zo
549
normal! zo
551
normal! zo
551
normal! zo
551
normal! zo
551
normal! zo
556
normal! zo
557
normal! zo
557
normal! zo
557
normal! zo
557
normal! zo
561
normal! zo
561
normal! zo
561
normal! zo
561
normal! zo
568
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
578
normal! zo
578
normal! zo
578
normal! zo
584
normal! zo
585
normal! zo
587
normal! zo
587
normal! zo
587
normal! zo
587
normal! zo
587
normal! zo
587
normal! zo
587
normal! zo
587
normal! zo
587
normal! zo
587
normal! zo
587
normal! zo
587
normal! zo
587
normal! zo
607
normal! zo
627
normal! zo
633
normal! zo
639
normal! zo
640
normal! zo
649
normal! zo
654
normal! zo
659
normal! zo
659
normal! zo
663
normal! zo
665
normal! zo
665
normal! zo
665
normal! zo
678
normal! zo
679
normal! zo
680
normal! zo
686
normal! zo
687
normal! zo
691
normal! zo
697
normal! zo
697
normal! zo
697
normal! zo
697
normal! zo
697
normal! zo
709
normal! zo
712
normal! zo
712
normal! zo
712
normal! zo
712
normal! zo
718
normal! zo
729
normal! zo
743
normal! zo
744
normal! zo
754
normal! zo
756
normal! zo
762
normal! zo
766
normal! zo
766
normal! zo
778
normal! zo
782
normal! zo
782
normal! zo
797
normal! zo
797
normal! zo
797
normal! zo
797
normal! zo
797
normal! zo
816
normal! zo
817
normal! zo
817
normal! zo
835
normal! zo
836
normal! zo
836
normal! zo
836
normal! zo
836
normal! zo
836
normal! zo
836
normal! zo
836
normal! zo
836
normal! zo
836
normal! zo
849
normal! zo
849
normal! zo
849
normal! zo
849
normal! zo
849
normal! zo
869
normal! zo
let s:l = 1 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
wincmd w
5wincmd w
exe '1resize ' . ((&lines * 3 + 25) / 51)
exe 'vert 1resize ' . ((&columns * 34 + 57) / 115)
exe '2resize ' . ((&lines * 45 + 25) / 51)
exe 'vert 2resize ' . ((&columns * 34 + 57) / 115)
exe '3resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 3resize ' . ((&columns * 80 + 57) / 115)
exe '4resize ' . ((&lines * 11 + 25) / 51)
exe 'vert 4resize ' . ((&columns * 80 + 57) / 115)
exe '5resize ' . ((&lines * 25 + 25) / 51)
exe 'vert 5resize ' . ((&columns * 80 + 57) / 115)
exe '6resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 6resize ' . ((&columns * 80 + 57) / 115)
exe '7resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 7resize ' . ((&columns * 80 + 57) / 115)
exe '8resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 8resize ' . ((&columns * 80 + 57) / 115)
exe '9resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 9resize ' . ((&columns * 80 + 57) / 115)
exe '10resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 10resize ' . ((&columns * 80 + 57) / 115)
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
