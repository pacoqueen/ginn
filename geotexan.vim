" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 16 enero 2014 at 19:13:47.
" Open this file in Vim and run :source % to restore your session.

set guioptions=aegimrLtT
silent! set guifont=Inconsolata\ 13
if exists('g:syntax_on') != 1 | syntax on | endif
if exists('g:did_load_filetypes') != 1 | filetype on | endif
if exists('g:did_load_ftplugin') != 1 | filetype plugin on | endif
if exists('g:did_indent_on') != 1 | filetype indent on | endif
if &background != 'light'
	set background=light
endif
if !exists('g:colors_name') || g:colors_name != 'github' | colorscheme github | endif
call setqflist([{'lnum': 0, 'col': 0, 'valid': 0, 'vcol': 0, 'nr': -1, 'type': '', 'pattern': '', 'filename': '/tmp/vQaj7Bk/182', 'text': 'grep: bin: Es un directorio'}, {'lnum': 0, 'col': 0, 'valid': 0, 'vcol': 0, 'nr': -1, 'type': '', 'pattern': '', 'filename': '/tmp/vQaj7Bk/182', 'text': 'grep: db: Es un directorio'}, {'lnum': 0, 'col': 0, 'valid': 0, 'vcol': 0, 'nr': -1, 'type': '', 'pattern': '', 'filename': '/tmp/vQaj7Bk/182', 'text': 'grep: doc: Es un directorio'}, {'lnum': 0, 'col': 0, 'valid': 0, 'vcol': 0, 'nr': -1, 'type': '', 'pattern': '', 'filename': '/tmp/vQaj7Bk/182', 'text': 'grep: extra: Es un directorio'}, {'lnum': 0, 'col': 0, 'valid': 0, 'vcol': 0, 'nr': -1, 'type': '', 'pattern': '', 'filename': '/tmp/vQaj7Bk/182', 'text': 'grep: ginn: Es un directorio'}, {'lnum': 0, 'col': 0, 'valid': 0, 'vcol': 0, 'nr': -1, 'type': '', 'pattern': '', 'filename': '/tmp/vQaj7Bk/182', 'text': 'grep: obsolete: Es un directorio'}, {'lnum': 0, 'col': 0, 'valid': 0, 'vcol': 0, 'nr': -1, 'type': '', 'pattern': '', 'filename': '/tmp/vQaj7Bk/182', 'text': 'grep: tests: Es un directorio'}])
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
badd +353 ginn/formularios/consulta_producido.py
badd +1 ginn/__init__.py
badd +266 ginn/formularios/clientes.py
badd +991 ginn/formularios/productos_compra.py
badd +39 ginn/formularios/productos_de_venta_balas.py
badd +525 ginn/formularios/recibos.py
badd +603 ginn/formularios/productos_de_venta_rollos.py
badd +382 ginn/formularios/productos_de_venta_rollos_geocompuestos.py
badd +417 ginn/formularios/productos_de_venta_especial.py
badd +322 ginn/formularios/partes_de_fabricacion_balas.py
badd +962 ginn/formularios/partes_de_fabricacion_bolsas.py
badd +575 ginn/formularios/partes_de_fabricacion_rollos.py
badd +446 ginn/formularios/proveedores.py
badd +547 ~/workspace/CICAN/src/formularios/menu.py
badd +117 ginn/formularios/launcher.py
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
badd +2578 ginn/formularios/pedidos_de_venta.py
badd +3876 db/tablas.sql
badd +2029 ginn/formularios/albaranes_de_salida.py
badd +227 ginn/formularios/presupuesto.py
badd +1820 ginn/formularios/presupuestos.py
badd +97 ginn/informes/carta_compromiso.py
badd +367 ginn/formularios/tarifas_de_precios.py
badd +88 ginn/formularios/logviewer.py
badd +238 ginn/formularios/facturas_compra.py
badd +4386 ginn/formularios/utils.py
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
badd +19838 ginn/framework/pclases/__init__.py
badd +494 ginn/framework/pclases/superfacturaventa.py
badd +134 ginn/framework/pclases/facturaventa.py
badd +694 ginn/formularios/consulta_mensual_nominas.py
badd +88 ginn/informes/treeview2pdf.py
badd +129 ginn/formularios/balas_cable.py
badd +13 ginn/informes/nied.py
badd +82 ginn/informes/norma2013.py
badd +65 ginn/formularios/widgets.py
badd +1 ginn/informes/ekotex.py
badd +7 ~/.vim/ftplugin/python.vim
badd +140 ginn/formularios/listado_balas.py
badd +254 ginn/formularios/consulta_pendientes_servir.py
badd +130 ginn/formularios/facturas_no_bloqueadas.py
badd +221 ginn/formularios/consumo_balas_partida.py
badd +324 ginn/formularios/categorias_laborales.py
badd +411 ginn/formularios/nominas.py
badd +383 ginn/framework/pclases/cliente.py
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
badd +1 ginn/formularios/prefacturas.py
badd +1 presupuestos
args formularios/auditviewer.py
set lines=58 columns=109
edit ginn/formularios/prefacturas.py
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
exe 'vert 1resize ' . ((&columns * 28 + 54) / 109)
exe '2resize ' . ((&lines * 5 + 29) / 58)
exe 'vert 2resize ' . ((&columns * 80 + 54) / 109)
exe '3resize ' . ((&lines * 31 + 29) / 58)
exe 'vert 3resize ' . ((&columns * 80 + 54) / 109)
exe '4resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 4resize ' . ((&columns * 80 + 54) / 109)
exe '5resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 5resize ' . ((&columns * 80 + 54) / 109)
exe '6resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 6resize ' . ((&columns * 80 + 54) / 109)
exe '7resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 7resize ' . ((&columns * 80 + 54) / 109)
exe '8resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 8resize ' . ((&columns * 80 + 54) / 109)
exe '9resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 9resize ' . ((&columns * 80 + 54) / 109)
exe '10resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 10resize ' . ((&columns * 80 + 54) / 109)
exe '11resize ' . ((&lines * 4 + 29) / 58)
exe 'vert 11resize ' . ((&columns * 80 + 54) / 109)
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
82
normal! zo
371
normal! zo
386
normal! zo
387
normal! zo
387
normal! zo
387
normal! zo
387
normal! zo
389
normal! zo
390
normal! zo
390
normal! zo
390
normal! zo
390
normal! zo
424
normal! zo
430
normal! zo
let s:l = 430 - ((2 * winheight(0) + 2) / 5)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
430
normal! 012|
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
747
normal! zo
1095
normal! zo
1105
normal! zo
1197
normal! zo
1206
normal! zo
1248
normal! zo
1281
normal! zo
1299
normal! zo
1306
normal! zo
1315
normal! zo
1408
normal! zo
1415
normal! zo
1424
normal! zo
1517
normal! zo
1524
normal! zo
2077
normal! zo
3523
normal! zo
3754
normal! zo
3828
normal! zo
3840
normal! zo
3932
normal! zo
4030
normal! zo
4095
normal! zo
4479
normal! zo
4801
normal! zo
5130
normal! zo
5301
normal! zo
5312
normal! zo
5314
normal! zo
5317
normal! zo
5835
normal! zo
5847
normal! zo
6003
normal! zo
7394
normal! zo
7515
normal! zo
7521
normal! zo
7528
normal! zo
7557
normal! zo
7581
normal! zo
7650
normal! zo
7686
normal! zo
7693
normal! zo
7705
normal! zo
7774
normal! zo
7781
normal! zo
7787
normal! zo
7799
normal! zo
7800
normal! zo
7801
normal! zo
7802
normal! zo
7809
normal! zo
7818
normal! zo
7818
normal! zo
7818
normal! zo
7818
normal! zo
7818
normal! zo
7818
normal! zo
7818
normal! zo
7824
normal! zo
7825
normal! zo
7826
normal! zo
7849
normal! zo
7850
normal! zo
7858
normal! zo
7906
normal! zo
7911
normal! zo
7913
normal! zo
7926
normal! zo
7935
normal! zo
7937
normal! zo
7938
normal! zo
7945
normal! zo
7946
normal! zo
7952
normal! zo
7956
normal! zo
7964
normal! zo
7965
normal! zo
7967
normal! zo
7967
normal! zo
7979
normal! zo
7979
normal! zo
7979
normal! zo
8220
normal! zo
8262
normal! zo
9005
normal! zo
9058
normal! zo
9725
normal! zo
9736
normal! zo
9753
normal! zo
9769
normal! zo
9786
normal! zo
9786
normal! zo
9786
normal! zo
9786
normal! zo
9786
normal! zo
9786
normal! zo
9786
normal! zo
9786
normal! zo
9786
normal! zo
9833
normal! zo
9846
normal! zo
9862
normal! zo
9977
normal! zo
9995
normal! zo
9995
normal! zo
9995
normal! zo
9995
normal! zo
9995
normal! zo
10137
normal! zo
10216
normal! zo
10242
normal! zo
10523
normal! zo
10575
normal! zo
10750
normal! zo
10758
normal! zo
10778
normal! zo
10779
normal! zo
10984
normal! zo
11017
normal! zo
11031
normal! zo
11041
normal! zo
11372
normal! zo
11393
normal! zo
11406
normal! zo
11419
normal! zo
11428
normal! zo
11795
normal! zo
11890
normal! zo
11935
normal! zo
11944
normal! zo
13323
normal! zo
13361
normal! zo
13381
normal! zo
13495
normal! zo
13533
normal! zo
13551
normal! zo
13651
normal! zo
13665
normal! zo
13682
normal! zo
13781
normal! zo
13805
normal! zo
13806
normal! zo
13806
normal! zo
13806
normal! zo
13806
normal! zo
13806
normal! zo
13806
normal! zo
14310
normal! zo
14319
normal! zo
14329
normal! zo
14603
normal! zo
14995
normal! zo
15054
normal! zo
15649
normal! zo
16234
normal! zo
16256
normal! zo
16270
normal! zo
16440
normal! zo
17016
normal! zo
17029
normal! zo
17053
normal! zo
17329
normal! zo
17523
normal! zo
17537
normal! zo
19575
normal! zo
19583
normal! zo
19617
normal! zo
19718
normal! zo
19740
normal! zo
19748
normal! zo
19752
normal! zo
19757
normal! zo
19758
normal! zo
19758
normal! zo
19758
normal! zo
19758
normal! zo
19758
normal! zo
19762
normal! zo
19770
normal! zo
19787
normal! zo
19790
normal! zo
19791
normal! zo
19791
normal! zo
19837
normal! zo
19855
normal! zo
19863
normal! zo
19864
normal! zo
19864
normal! zo
19892
normal! zo
19963
normal! zo
let s:l = 19760 - ((27 * winheight(0) + 15) / 31)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
19760
normal! 04|
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
let s:l = 16 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
16
normal! 0
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
let s:l = 1 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
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
let s:l = 942 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
942
normal! 08|
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
59
normal! zo
59
normal! zo
59
normal! zo
59
normal! zo
68
normal! zo
275
normal! zo
276
normal! zo
277
normal! zo
286
normal! zo
1052
normal! zo
1066
normal! zo
1102
normal! zo
1103
normal! zo
1103
normal! zo
1104
normal! zo
1109
normal! zo
1443
normal! zo
1446
normal! zo
1452
normal! zo
2373
normal! zo
2544
normal! zo
2549
normal! zo
2553
normal! zo
2559
normal! zo
2578
normal! zo
2578
normal! zo
2638
normal! zo
let s:l = 3101 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3101
normal! 05|
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
let s:l = 512 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
512
normal! 075|
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/presupuesto.py
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
53
normal! zo
65
normal! zo
65
normal! zo
let s:l = 70 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
70
normal! 035|
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
110
normal! zo
144
normal! zo
147
normal! zo
148
normal! zo
162
normal! zo
163
normal! zo
166
normal! zo
229
normal! zo
362
normal! zo
467
normal! zo
577
normal! zo
593
normal! zo
625
normal! zo
664
normal! zo
676
normal! zo
699
normal! zo
763
normal! zo
919
normal! zo
1007
normal! zo
1012
normal! zo
1258
normal! zo
1340
normal! zo
1340
normal! zo
1340
normal! zo
1340
normal! zo
1340
normal! zo
1340
normal! zo
1685
normal! zo
1823
normal! zo
1862
normal! zo
2545
normal! zo
2554
normal! zo
2800
normal! zo
3087
normal! zo
3098
normal! zo
3192
normal! zo
3204
normal! zo
3220
normal! zo
3228
normal! zo
3327
normal! zo
3793
normal! zo
let s:l = 182 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
182
normal! 05|
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/launcher.py
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
67
normal! zo
71
normal! zo
98
normal! zo
101
normal! zo
112
normal! zo
let s:l = 111 - ((1 * winheight(0) + 2) / 4)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
111
normal! 011|
wincmd w
3wincmd w
exe 'vert 1resize ' . ((&columns * 28 + 54) / 109)
exe '2resize ' . ((&lines * 5 + 29) / 58)
exe 'vert 2resize ' . ((&columns * 80 + 54) / 109)
exe '3resize ' . ((&lines * 31 + 29) / 58)
exe 'vert 3resize ' . ((&columns * 80 + 54) / 109)
exe '4resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 4resize ' . ((&columns * 80 + 54) / 109)
exe '5resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 5resize ' . ((&columns * 80 + 54) / 109)
exe '6resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 6resize ' . ((&columns * 80 + 54) / 109)
exe '7resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 7resize ' . ((&columns * 80 + 54) / 109)
exe '8resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 8resize ' . ((&columns * 80 + 54) / 109)
exe '9resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 9resize ' . ((&columns * 80 + 54) / 109)
exe '10resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 10resize ' . ((&columns * 80 + 54) / 109)
exe '11resize ' . ((&lines * 4 + 29) / 58)
exe 'vert 11resize ' . ((&columns * 80 + 54) / 109)
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
3wincmd w

" vim: ft=vim ro nowrap smc=128
