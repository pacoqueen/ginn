" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 09 septiembre 2013 at 17:30:03.
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
badd +2258 ginn/formularios/productos_de_venta_rollos.py
badd +507 ginn/formularios/productos_de_venta_rollos_geocompuestos.py
badd +578 ginn/formularios/productos_de_venta_especial.py
badd +1526 ginn/formularios/partes_de_fabricacion_balas.py
badd +1957 ginn/formularios/partes_de_fabricacion_bolsas.py
badd +3779 ginn/formularios/partes_de_fabricacion_rollos.py
badd +550 ginn/formularios/proveedores.py
badd +547 ~/workspace/CICAN/src/formularios/menu.py
badd +105 ginn/formularios/launcher.py
badd +464 ginn/formularios/empleados.py
badd +38 ginn/formularios/resultados_geotextiles.py
badd +230 ginn/formularios/menu.py
badd +142 ginn/formularios/autenticacion.py
badd +3614 ginn/informes/geninformes.py
badd +233 ginn/informes/informe_certificado_calidad.py
badd +1518 informes/geninformes.py
badd +2958 ginn/formularios/facturas_venta.py
badd +417 ginn/framework/configuracion.py
badd +4 bin/ginn.sh
badd +10 ginn/main.py
badd +292 ginn/formularios/ventana.py
badd +375 ginn/formularios/pedidos_de_venta.py
badd +1431 db/tablas.sql
badd +810 ginn/formularios/albaranes_de_salida.py
badd +1 ginn/formularios/presupuesto.py
badd +466 ginn/formularios/presupuestos.py
badd +1 ginn/informes/carta_compromiso.py
badd +367 ginn/formularios/tarifas_de_precios.py
badd +88 ginn/formularios/logviewer.py
badd +724 ginn/formularios/facturas_compra.py
badd +4107 ginn/formularios/utils.py
badd +648 ginn/formularios/resultados_fibra.py
badd +812 ginn/formularios/albaranes_de_entrada.py
badd +1329 ginn/formularios/consulta_ventas.py
badd +37 ginn/formularios/__init__.py
badd +907 ginn/formularios/pagares_pagos.py
badd +331 ginn/formularios/ausencias.py
badd +67 ginn/formularios/partes_no_bloqueados.py
badd +46 ginn/formularios/gtkexcepthook.py
badd +1 ginn/framework/seeker.py
badd +13 ginn/formularios/crm_seguimiento_impagos.py
badd +203 ginn/formularios/productos.py
badd +1064 ginn/formularios/trazabilidad_articulos.py
badd +363 ginn/formularios/consulta_pagos.py
badd +13 ginn/formularios/consulta_vencimientos_pago.py
badd +500 ginn/formularios/trazabilidad.py
badd +1 ginn/framework/pclases/__init__.py
badd +611 ginn/framework/pclases/superfacturaventa.py
badd +47 ginn/framework/pclases/facturaventa.py
badd +689 ginn/formularios/consulta_mensual_nominas.py
badd +269 ginn/informes/treeview2pdf.py
badd +129 ginn/formularios/balas_cable.py
badd +13 ginn/informes/nied.py
badd +249 ginn/informes/norma2013.py
badd +65 ginn/formularios/widgets.py
badd +1 ginn/informes/ekotex.py
badd +7 ~/.vim/ftplugin/python.vim
badd +921 ginn/formularios/listado_balas.py
badd +254 ginn/formularios/consulta_pendientes_servir.py
badd +130 ginn/formularios/facturas_no_bloqueadas.py
badd +221 ginn/formularios/consumo_balas_partida.py
badd +553 ginn/formularios/categorias_laborales.py
badd +411 ginn/formularios/nominas.py
badd +511 ginn/framework/pclases/cliente.py
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
badd +431 ginn/informes/presupuesto2.py
badd +61 ginn/informes/albaran_multipag.py
badd +192 ginn/formularios/silos.py
args formularios/auditviewer.py
set lines=44 columns=111
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
exe '2resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 2resize ' . ((&columns * 80 + 55) / 111)
exe '3resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 3resize ' . ((&columns * 80 + 55) / 111)
exe '4resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 4resize ' . ((&columns * 80 + 55) / 111)
exe '5resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 5resize ' . ((&columns * 80 + 55) / 111)
exe '6resize ' . ((&lines * 24 + 22) / 44)
exe 'vert 6resize ' . ((&columns * 80 + 55) / 111)
exe '7resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 7resize ' . ((&columns * 80 + 55) / 111)
exe '8resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 8resize ' . ((&columns * 80 + 55) / 111)
exe '9resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 9resize ' . ((&columns * 80 + 55) / 111)
exe '10resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 10resize ' . ((&columns * 80 + 55) / 111)
exe '11resize ' . ((&lines * 1 + 22) / 44)
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
silent! normal zo
436
silent! normal zo
641
silent! normal zo
2053
silent! normal zo
2064
silent! normal zo
2064
silent! normal zo
2064
silent! normal zo
2064
silent! normal zo
2064
silent! normal zo
2064
silent! normal zo
4726
silent! normal zo
4739
silent! normal zo
4745
silent! normal zo
10149
silent! normal zo
10199
silent! normal zo
10199
silent! normal zo
10199
silent! normal zo
10199
silent! normal zo
10199
silent! normal zo
10325
silent! normal zo
10328
silent! normal zo
10339
silent! normal zo
10339
silent! normal zo
10339
silent! normal zo
10348
silent! normal zo
10356
silent! normal zo
10372
silent! normal zo
15068
silent! normal zo
17890
silent! normal zo
19417
silent! normal zo
19439
silent! normal zo
19473
silent! normal zo
19505
silent! normal zo
19821
silent! normal zo
19839
silent! normal zo
19844
silent! normal zo
19844
silent! normal zo
19844
silent! normal zo
let s:l = 10320 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
10320
normal! 04l
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
silent! normal zo
150
silent! normal zo
170
silent! normal zo
185
silent! normal zo
190
silent! normal zo
279
silent! normal zo
282
silent! normal zo
282
silent! normal zo
293
silent! normal zo
293
silent! normal zo
293
silent! normal zo
293
silent! normal zo
293
silent! normal zo
311
silent! normal zo
314
silent! normal zo
let s:l = 352 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
352
normal! 024l
wincmd w
argglobal
edit ginn/informes/presupuesto2.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
60
silent! normal zo
61
silent! normal zo
65
silent! normal zo
65
silent! normal zo
65
silent! normal zo
65
silent! normal zo
65
silent! normal zo
72
silent! normal zo
83
silent! normal zo
88
silent! normal zo
92
silent! normal zo
93
silent! normal zo
93
silent! normal zo
105
silent! normal zo
110
silent! normal zo
110
silent! normal zo
112
silent! normal zo
112
silent! normal zo
112
silent! normal zo
158
silent! normal zo
171
silent! normal zo
184
silent! normal zo
203
silent! normal zo
213
silent! normal zo
240
silent! normal zo
262
silent! normal zo
262
silent! normal zo
262
silent! normal zo
262
silent! normal zo
262
silent! normal zo
312
silent! normal zo
348
silent! normal zo
376
silent! normal zo
376
silent! normal zo
376
silent! normal zo
379
silent! normal zo
382
silent! normal zo
383
silent! normal zo
383
silent! normal zo
389
silent! normal zo
389
silent! normal zo
389
silent! normal zo
390
silent! normal zo
390
silent! normal zo
390
silent! normal zo
390
silent! normal zo
396
silent! normal zo
396
silent! normal zo
396
silent! normal zo
396
silent! normal zo
396
silent! normal zo
402
silent! normal zo
404
silent! normal zo
404
silent! normal zo
404
silent! normal zo
404
silent! normal zo
406
silent! normal zo
406
silent! normal zo
406
silent! normal zo
406
silent! normal zo
417
silent! normal zo
420
silent! normal zo
433
silent! normal zo
449
silent! normal zo
458
silent! normal zo
459
silent! normal zo
464
silent! normal zo
464
silent! normal zo
464
silent! normal zo
464
silent! normal zo
467
silent! normal zo
469
silent! normal zo
471
silent! normal zo
474
silent! normal zo
486
silent! normal zo
511
silent! normal zo
528
silent! normal zo
529
silent! normal zo
529
silent! normal zo
529
silent! normal zo
568
silent! normal zo
571
silent! normal zo
let s:l = 112 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
112
normal! 052l
wincmd w
argglobal
edit ginn/formularios/pedidos_de_venta.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
121
silent! normal zo
122
silent! normal zo
134
silent! normal zo
134
silent! normal zo
134
silent! normal zo
320
silent! normal zo
362
silent! normal zo
369
silent! normal zo
402
silent! normal zo
404
silent! normal zo
413
silent! normal zo
642
silent! normal zo
707
silent! normal zo
719
silent! normal zo
724
silent! normal zo
727
silent! normal zo
728
silent! normal zo
761
silent! normal zo
1124
silent! normal zo
1210
silent! normal zo
1430
silent! normal zo
1465
silent! normal zo
1964
silent! normal zo
let s:l = 1430 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1430
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
59
silent! normal zo
60
silent! normal zo
68
silent! normal zo
68
silent! normal zo
68
silent! normal zo
90
silent! normal zo
90
silent! normal zo
90
silent! normal zo
137
silent! normal zo
146
silent! normal zo
155
silent! normal zo
180
silent! normal zo
182
silent! normal zo
183
silent! normal zo
184
silent! normal zo
203
silent! normal zo
235
silent! normal zo
287
silent! normal zo
302
silent! normal zo
310
silent! normal zo
332
silent! normal zo
426
silent! normal zo
431
silent! normal zo
432
silent! normal zo
432
silent! normal zo
444
silent! normal zo
447
silent! normal zo
448
silent! normal zo
448
silent! normal zo
453
silent! normal zo
462
silent! normal zo
465
silent! normal zo
472
silent! normal zo
505
silent! normal zo
507
silent! normal zo
513
silent! normal zo
519
silent! normal zo
523
silent! normal zo
523
silent! normal zo
523
silent! normal zo
523
silent! normal zo
523
silent! normal zo
523
silent! normal zo
546
silent! normal zo
578
silent! normal zo
593
silent! normal zo
598
silent! normal zo
670
silent! normal zo
748
silent! normal zo
755
silent! normal zo
787
silent! normal zo
793
silent! normal zo
793
silent! normal zo
793
silent! normal zo
793
silent! normal zo
793
silent! normal zo
793
silent! normal zo
793
silent! normal zo
793
silent! normal zo
806
silent! normal zo
806
silent! normal zo
867
silent! normal zo
870
silent! normal zo
889
silent! normal zo
893
silent! normal zo
894
silent! normal zo
899
silent! normal zo
908
silent! normal zo
914
silent! normal zo
922
silent! normal zo
1061
silent! normal zo
1091
silent! normal zo
1091
silent! normal zo
1091
silent! normal zo
1091
silent! normal zo
1091
silent! normal zo
1099
silent! normal zo
1103
silent! normal zo
1107
silent! normal zo
1113
silent! normal zo
1114
silent! normal zo
1114
silent! normal zo
1114
silent! normal zo
1114
silent! normal zo
1114
silent! normal zo
1116
silent! normal zo
1118
silent! normal zo
1119
silent! normal zo
1128
silent! normal zo
1128
silent! normal zo
1128
silent! normal zo
1130
silent! normal zo
1130
silent! normal zo
1130
silent! normal zo
1136
silent! normal zo
1136
silent! normal zo
1136
silent! normal zo
1136
silent! normal zo
1142
silent! normal zo
1143
silent! normal zo
1145
silent! normal zo
1145
silent! normal zo
1149
silent! normal zo
1154
silent! normal zo
1161
silent! normal zo
1174
silent! normal zo
1197
silent! normal zo
1219
silent! normal zo
1227
silent! normal zo
1227
silent! normal zo
1241
silent! normal zo
1241
silent! normal zo
1241
silent! normal zo
1241
silent! normal zo
1286
silent! normal zo
1291
silent! normal zo
1292
silent! normal zo
1292
silent! normal zo
1293
silent! normal zo
1293
silent! normal zo
1293
silent! normal zo
1293
silent! normal zo
1293
silent! normal zo
1293
silent! normal zo
1293
silent! normal zo
1296
silent! normal zo
1298
silent! normal zo
1301
silent! normal zo
1301
silent! normal zo
1301
silent! normal zo
1301
silent! normal zo
1307
silent! normal zo
1308
silent! normal zo
1308
silent! normal zo
1325
silent! normal zo
1325
silent! normal zo
1325
silent! normal zo
1325
silent! normal zo
1338
silent! normal zo
1355
silent! normal zo
1356
silent! normal zo
1413
silent! normal zo
1455
silent! normal zo
1461
silent! normal zo
1473
silent! normal zo
1519
silent! normal zo
1530
silent! normal zo
1530
silent! normal zo
1530
silent! normal zo
1530
silent! normal zo
1530
silent! normal zo
1530
silent! normal zo
1530
silent! normal zo
1538
silent! normal zo
1562
silent! normal zo
1605
silent! normal zo
1675
silent! normal zo
1680
silent! normal zo
1708
silent! normal zo
1717
silent! normal zo
1724
silent! normal zo
1735
silent! normal zo
1738
silent! normal zo
1739
silent! normal zo
1739
silent! normal zo
1746
silent! normal zo
1751
silent! normal zo
1751
silent! normal zo
1751
silent! normal zo
1751
silent! normal zo
1785
silent! normal zo
1788
silent! normal zo
let s:l = 1317 - ((18 * winheight(0) + 12) / 24)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1317
normal! 048l
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
silent! normal zo
274
silent! normal zo
299
silent! normal zo
301
silent! normal zo
302
silent! normal zo
302
silent! normal zo
302
silent! normal zo
302
silent! normal zo
302
silent! normal zo
306
silent! normal zo
308
silent! normal zo
309
silent! normal zo
309
silent! normal zo
309
silent! normal zo
309
silent! normal zo
309
silent! normal zo
322
silent! normal zo
327
silent! normal zo
335
silent! normal zo
336
silent! normal zo
336
silent! normal zo
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
silent! normal zo
277
silent! normal zo
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
silent! normal zo
let s:l = 621 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
621
normal! 027l
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
silent! normal zo
51
silent! normal zo
66
silent! normal zo
70
silent! normal zo
let s:l = 97 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
97
normal! 06l
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
silent! normal zo
578
silent! normal zo
593
silent! normal zo
593
silent! normal zo
593
silent! normal zo
593
silent! normal zo
593
silent! normal zo
593
silent! normal zo
624
silent! normal zo
635
silent! normal zo
643
silent! normal zo
651
silent! normal zo
659
silent! normal zo
659
silent! normal zo
659
silent! normal zo
659
silent! normal zo
668
silent! normal zo
673
silent! normal zo
687
silent! normal zo
let s:l = 673 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
673
normal! 027l
wincmd w
6wincmd w
exe 'vert 1resize ' . ((&columns * 30 + 55) / 111)
exe '2resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 2resize ' . ((&columns * 80 + 55) / 111)
exe '3resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 3resize ' . ((&columns * 80 + 55) / 111)
exe '4resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 4resize ' . ((&columns * 80 + 55) / 111)
exe '5resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 5resize ' . ((&columns * 80 + 55) / 111)
exe '6resize ' . ((&lines * 24 + 22) / 44)
exe 'vert 6resize ' . ((&columns * 80 + 55) / 111)
exe '7resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 7resize ' . ((&columns * 80 + 55) / 111)
exe '8resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 8resize ' . ((&columns * 80 + 55) / 111)
exe '9resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 9resize ' . ((&columns * 80 + 55) / 111)
exe '10resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 10resize ' . ((&columns * 80 + 55) / 111)
exe '11resize ' . ((&lines * 1 + 22) / 44)
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
