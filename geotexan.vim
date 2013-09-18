" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 18 septiembre 2013 at 20:52:27.
" Open this file in Vim and run :source % to restore your session.

set guioptions=aegimrLtT
silent! set guifont=Droid\ Sans\ Mono\ Slashed\ 10
if exists('g:syntax_on') != 1 | syntax on | endif
if exists('g:did_load_filetypes') != 1 | filetype on | endif
if exists('g:did_load_ftplugin') != 1 | filetype plugin on | endif
if exists('g:did_indent_on') != 1 | filetype indent on | endif
if &background != 'dark'
	set background=dark
endif
if !exists('g:colors_name') || g:colors_name != 'desert' | colorscheme desert | endif
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
badd +392 ginn/formularios/consulta_producido.py
badd +1 ginn/__init__.py
badd +592 ginn/formularios/clientes.py
badd +991 ginn/formularios/productos_compra.py
badd +310 ginn/formularios/productos_de_venta_balas.py
badd +525 ginn/formularios/recibos.py
badd +325 ginn/formularios/productos_de_venta_rollos.py
badd +507 ginn/formularios/productos_de_venta_rollos_geocompuestos.py
badd +578 ginn/formularios/productos_de_venta_especial.py
badd +1 ginn/formularios/partes_de_fabricacion_balas.py
badd +1931 ginn/formularios/partes_de_fabricacion_bolsas.py
badd +1406 ginn/formularios/partes_de_fabricacion_rollos.py
badd +550 ginn/formularios/proveedores.py
badd +547 ~/workspace/CICAN/src/formularios/menu.py
badd +117 ginn/formularios/launcher.py
badd +464 ginn/formularios/empleados.py
badd +38 ginn/formularios/resultados_geotextiles.py
badd +230 ginn/formularios/menu.py
badd +142 ginn/formularios/autenticacion.py
badd +7934 ginn/informes/geninformes.py
badd +233 ginn/informes/informe_certificado_calidad.py
badd +1518 informes/geninformes.py
badd +2714 ginn/formularios/facturas_venta.py
badd +419 ginn/framework/configuracion.py
badd +4 bin/ginn.sh
badd +10 ginn/main.py
badd +292 ginn/formularios/ventana.py
badd +535 ginn/formularios/pedidos_de_venta.py
badd +3664 db/tablas.sql
badd +2956 ginn/formularios/albaranes_de_salida.py
badd +1 ginn/formularios/presupuesto.py
badd +1283 ginn/formularios/presupuestos.py
badd +1 ginn/informes/carta_compromiso.py
badd +367 ginn/formularios/tarifas_de_precios.py
badd +88 ginn/formularios/logviewer.py
badd +724 ginn/formularios/facturas_compra.py
badd +4363 ginn/formularios/utils.py
badd +648 ginn/formularios/resultados_fibra.py
badd +812 ginn/formularios/albaranes_de_entrada.py
badd +751 ginn/formularios/consulta_ventas.py
badd +37 ginn/formularios/__init__.py
badd +907 ginn/formularios/pagares_pagos.py
badd +331 ginn/formularios/ausencias.py
badd +67 ginn/formularios/partes_no_bloqueados.py
badd +46 ginn/formularios/gtkexcepthook.py
badd +476 ginn/framework/seeker.py
badd +13 ginn/formularios/crm_seguimiento_impagos.py
badd +203 ginn/formularios/productos.py
badd +1064 ginn/formularios/trazabilidad_articulos.py
badd +363 ginn/formularios/consulta_pagos.py
badd +13 ginn/formularios/consulta_vencimientos_pago.py
badd +500 ginn/formularios/trazabilidad.py
badd +1 ginn/framework/pclases/__init__.py
badd +803 ginn/framework/pclases/superfacturaventa.py
badd +47 ginn/framework/pclases/facturaventa.py
badd +689 ginn/formularios/consulta_mensual_nominas.py
badd +269 ginn/informes/treeview2pdf.py
badd +129 ginn/formularios/balas_cable.py
badd +13 ginn/informes/nied.py
badd +118 ginn/informes/norma2013.py
badd +65 ginn/formularios/widgets.py
badd +1 ginn/informes/ekotex.py
badd +7 ~/.vim/ftplugin/python.vim
badd +140 ginn/formularios/listado_balas.py
badd +254 ginn/formularios/consulta_pendientes_servir.py
badd +130 ginn/formularios/facturas_no_bloqueadas.py
badd +221 ginn/formularios/consumo_balas_partida.py
badd +553 ginn/formularios/categorias_laborales.py
badd +411 ginn/formularios/nominas.py
badd +535 ginn/framework/pclases/cliente.py
badd +1 ginn/formularios/consulta_cobros.py
badd +628 ginn/formularios/pagares_cobros.py
badd +24 extra/patches/calcular_credito_disponible.sql
badd +301 ginn/formularios/pclase2tv.py
badd +94 ginn/formularios/consulta_control_horas.py
badd +533 ginn/formularios/horas_trabajadas.py
badd +550 ginn/formularios/horas_trabajadas_dia.py
badd +1 ginn/formularios/pedidos_de_compra.glade
badd +523 ginn/formularios/postomatic.py
badd +36 ginn/formularios/custom_widgets/cellrendererautocomplete.py
badd +47 ginn/formularios/custom_widgets/__init__.py
badd +394 ginn/informes/presupuesto2.py
badd +61 ginn/informes/albaran_multipag.py
badd +192 ginn/formularios/silos.py
badd +1 ginn/framework/__init__.py
badd +1 ginn/formularios/vencimientos_pendientes_por_cliente.glade
badd +416 ginn/formularios/consulta_productividad.py
args formularios/auditviewer.py
set lines=69 columns=111
edit ginn/framework/pclases/__init__.py
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
exe 'vert 1resize ' . ((&columns * 30 + 55) / 111)
exe '2resize ' . ((&lines * 1 + 34) / 69)
exe 'vert 2resize ' . ((&columns * 80 + 55) / 111)
exe '3resize ' . ((&lines * 1 + 34) / 69)
exe 'vert 3resize ' . ((&columns * 80 + 55) / 111)
exe '4resize ' . ((&lines * 1 + 34) / 69)
exe 'vert 4resize ' . ((&columns * 80 + 55) / 111)
exe '5resize ' . ((&lines * 1 + 34) / 69)
exe 'vert 5resize ' . ((&columns * 80 + 55) / 111)
exe '6resize ' . ((&lines * 49 + 34) / 69)
exe 'vert 6resize ' . ((&columns * 80 + 55) / 111)
exe '7resize ' . ((&lines * 1 + 34) / 69)
exe 'vert 7resize ' . ((&columns * 80 + 55) / 111)
exe '8resize ' . ((&lines * 1 + 34) / 69)
exe 'vert 8resize ' . ((&columns * 80 + 55) / 111)
exe '9resize ' . ((&lines * 1 + 34) / 69)
exe 'vert 9resize ' . ((&columns * 80 + 55) / 111)
exe '10resize ' . ((&lines * 1 + 34) / 69)
exe 'vert 10resize ' . ((&columns * 80 + 55) / 111)
exe '11resize ' . ((&lines * 1 + 34) / 69)
exe 'vert 11resize ' . ((&columns * 80 + 55) / 111)
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
270
normal! zo
436
normal! zo
641
normal! zo
2053
normal! zo
2064
normal! zo
2064
normal! zo
2064
normal! zo
2064
normal! zo
2064
normal! zo
2064
normal! zo
2229
normal! zo
2250
normal! zo
2292
normal! zo
2760
normal! zo
2810
normal! zo
3019
normal! zo
3031
normal! zo
3043
normal! zo
3070
normal! zo
3085
normal! zo
4730
normal! zo
4743
normal! zo
4749
normal! zo
7550
normal! zo
7969
normal! zo
7969
normal! zo
7969
normal! zo
7969
normal! zo
7969
normal! zo
7969
normal! zo
7969
normal! zo
7969
normal! zo
7969
normal! zo
7969
normal! zo
7997
normal! zo
9722
normal! zo
9738
normal! zo
10072
normal! zo
10151
normal! zo
10177
normal! zo
10189
normal! zo
10194
normal! zo
10204
normal! zo
10209
normal! zo
10215
normal! zo
10223
normal! zo
10229
normal! zo
10235
normal! zo
10245
normal! zo
10251
normal! zo
10252
normal! zo
10258
normal! zo
10268
normal! zo
10277
normal! zo
10279
normal! zo
10418
normal! zo
10424
normal! zo
10449
normal! zo
10452
normal! zo
10472
normal! zo
14191
normal! zo
14620
normal! zo
14630
normal! zo
14943
normal! zo
15138
normal! zo
15138
normal! zo
15138
normal! zo
15138
normal! zo
15138
normal! zo
15138
normal! zo
15138
normal! zo
15165
normal! zo
17909
normal! zo
17955
normal! zo
19422
normal! zo
19476
normal! zo
19523
normal! zo
19545
normal! zo
19554
normal! zo
19579
normal! zo
19834
normal! zo
19897
normal! zo
19911
normal! zo
let s:l = 663 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
663
normal! 034|
wincmd w
argglobal
edit ginn/informes/carta_compromiso.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
60
normal! zo
150
normal! zo
170
normal! zo
185
normal! zo
190
normal! zo
279
normal! zo
282
normal! zo
282
normal! zo
293
normal! zo
293
normal! zo
293
normal! zo
293
normal! zo
293
normal! zo
311
normal! zo
314
normal! zo
let s:l = 352 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
352
normal! 025|
wincmd w
argglobal
edit ginn/formularios/ventana.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
104
normal! zo
733
normal! zo
733
normal! zo
733
normal! zo
733
normal! zo
let s:l = 814 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
814
normal! 035|
wincmd w
argglobal
edit ginn/formularios/clientes.py
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
let s:l = 1950 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1950
normal! 0
wincmd w
argglobal
edit ginn/formularios/presupuestos.py
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
67
normal! zo
67
normal! zo
67
normal! zo
89
normal! zo
89
normal! zo
89
normal! zo
128
normal! zo
129
normal! zo
130
normal! zo
130
normal! zo
140
normal! zo
141
normal! zo
142
normal! zo
143
normal! zo
158
normal! zo
159
normal! zo
169
normal! zo
170
normal! zo
175
normal! zo
176
normal! zo
180
normal! zo
183
normal! zo
189
normal! zo
190
normal! zo
190
normal! zo
190
normal! zo
190
normal! zo
190
normal! zo
190
normal! zo
195
normal! zo
196
normal! zo
197
normal! zo
197
normal! zo
197
normal! zo
197
normal! zo
197
normal! zo
197
normal! zo
221
normal! zo
230
normal! zo
239
normal! zo
266
normal! zo
268
normal! zo
269
normal! zo
270
normal! zo
376
normal! zo
391
normal! zo
393
normal! zo
393
normal! zo
393
normal! zo
393
normal! zo
393
normal! zo
399
normal! zo
421
normal! zo
558
normal! zo
673
normal! zo
682
normal! zo
699
normal! zo
741
normal! zo
874
normal! zo
883
normal! zo
909
normal! zo
930
normal! zo
934
normal! zo
937
normal! zo
943
normal! zo
943
normal! zo
943
normal! zo
943
normal! zo
943
normal! zo
943
normal! zo
971
normal! zo
1006
normal! zo
1009
normal! zo
1020
normal! zo
1039
normal! zo
1050
normal! zo
1079
normal! zo
1079
normal! zo
1079
normal! zo
1082
normal! zo
1102
normal! zo
1102
normal! zo
1123
normal! zo
1127
normal! zo
1131
normal! zo
1166
normal! zo
1168
normal! zo
1170
normal! zo
1170
normal! zo
1254
normal! zo
1265
normal! zo
1265
normal! zo
1265
normal! zo
1268
normal! zo
1268
normal! zo
1268
normal! zo
1319
normal! zo
1323
normal! zo
1323
normal! zo
1364
normal! zo
1438
normal! zo
1438
normal! zo
1438
normal! zo
1438
normal! zo
1438
normal! zo
1438
normal! zo
1438
normal! zo
1453
normal! zo
1458
normal! zo
1460
normal! zo
1468
normal! zo
1472
normal! zo
1476
normal! zo
1477
normal! zo
1478
normal! zo
1478
normal! zo
1478
normal! zo
1478
normal! zo
1482
normal! zo
1483
normal! zo
1483
normal! zo
1483
normal! zo
1483
normal! zo
1487
normal! zo
1488
normal! zo
1488
normal! zo
1488
normal! zo
1488
normal! zo
1488
normal! zo
1492
normal! zo
1492
normal! zo
1492
normal! zo
1492
normal! zo
1492
normal! zo
1492
normal! zo
1492
normal! zo
1492
normal! zo
1492
normal! zo
1495
normal! zo
1497
normal! zo
1499
normal! zo
1499
normal! zo
1517
normal! zo
1638
normal! zo
1679
normal! zo
1691
normal! zo
1692
normal! zo
1771
normal! zo
1790
normal! zo
1806
normal! zo
1809
normal! zo
1810
normal! zo
1810
normal! zo
1810
normal! zo
1810
normal! zo
1823
normal! zo
1823
normal! zo
1823
normal! zo
1823
normal! zo
1823
normal! zo
1823
normal! zo
1939
normal! zo
1944
normal! zo
1972
normal! zo
1981
normal! zo
1999
normal! zo
2002
normal! zo
2003
normal! zo
2003
normal! zo
2010
normal! zo
2015
normal! zo
2015
normal! zo
2015
normal! zo
2015
normal! zo
2026
normal! zo
2052
normal! zo
2055
normal! zo
2059
normal! zo
2060
normal! zo
2097
normal! zo
2119
normal! zo
2263
normal! zo
2263
normal! zo
2263
normal! zo
2263
normal! zo
2263
normal! zo
let s:l = 1437 - ((24 * winheight(0) + 24) / 49)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1437
normal! 09|
wincmd w
argglobal
edit ginn/formularios/consulta_cobros.py
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
299
normal! zo
301
normal! zo
302
normal! zo
302
normal! zo
302
normal! zo
302
normal! zo
302
normal! zo
306
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
309
normal! zo
322
normal! zo
327
normal! zo
335
normal! zo
336
normal! zo
336
normal! zo
let s:l = 320 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
320
normal! 0
wincmd w
argglobal
edit ginn/formularios/ventana.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
104
normal! zo
277
normal! zo
let s:l = 1 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
wincmd w
argglobal
edit ginn/framework/pclases/superfacturaventa.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
38
normal! zo
let s:l = 621 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
621
normal! 028|
wincmd w
argglobal
edit ginn/formularios/launcher.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
34
normal! zo
51
normal! zo
66
normal! zo
70
normal! zo
let s:l = 97 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
97
normal! 07|
wincmd w
argglobal
edit ginn/formularios/clientes.py
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
578
normal! zo
593
normal! zo
593
normal! zo
593
normal! zo
593
normal! zo
593
normal! zo
593
normal! zo
624
normal! zo
635
normal! zo
643
normal! zo
651
normal! zo
659
normal! zo
659
normal! zo
659
normal! zo
659
normal! zo
668
normal! zo
673
normal! zo
687
normal! zo
let s:l = 673 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
673
normal! 028|
wincmd w
6wincmd w
exe 'vert 1resize ' . ((&columns * 30 + 55) / 111)
exe '2resize ' . ((&lines * 1 + 34) / 69)
exe 'vert 2resize ' . ((&columns * 80 + 55) / 111)
exe '3resize ' . ((&lines * 1 + 34) / 69)
exe 'vert 3resize ' . ((&columns * 80 + 55) / 111)
exe '4resize ' . ((&lines * 1 + 34) / 69)
exe 'vert 4resize ' . ((&columns * 80 + 55) / 111)
exe '5resize ' . ((&lines * 1 + 34) / 69)
exe 'vert 5resize ' . ((&columns * 80 + 55) / 111)
exe '6resize ' . ((&lines * 49 + 34) / 69)
exe 'vert 6resize ' . ((&columns * 80 + 55) / 111)
exe '7resize ' . ((&lines * 1 + 34) / 69)
exe 'vert 7resize ' . ((&columns * 80 + 55) / 111)
exe '8resize ' . ((&lines * 1 + 34) / 69)
exe 'vert 8resize ' . ((&columns * 80 + 55) / 111)
exe '9resize ' . ((&lines * 1 + 34) / 69)
exe 'vert 9resize ' . ((&columns * 80 + 55) / 111)
exe '10resize ' . ((&lines * 1 + 34) / 69)
exe 'vert 10resize ' . ((&columns * 80 + 55) / 111)
exe '11resize ' . ((&lines * 1 + 34) / 69)
exe 'vert 11resize ' . ((&columns * 80 + 55) / 111)
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
