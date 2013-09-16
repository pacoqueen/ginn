" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 13 septiembre 2013 at 15:05:20.
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
badd +1526 ginn/formularios/partes_de_fabricacion_balas.py
badd +1957 ginn/formularios/partes_de_fabricacion_bolsas.py
badd +1406 ginn/formularios/partes_de_fabricacion_rollos.py
badd +550 ginn/formularios/proveedores.py
badd +547 ~/workspace/CICAN/src/formularios/menu.py
badd +117 ginn/formularios/launcher.py
badd +464 ginn/formularios/empleados.py
badd +38 ginn/formularios/resultados_geotextiles.py
badd +230 ginn/formularios/menu.py
badd +142 ginn/formularios/autenticacion.py
badd +3614 ginn/informes/geninformes.py
badd +233 ginn/informes/informe_certificado_calidad.py
badd +1518 informes/geninformes.py
badd +2958 ginn/formularios/facturas_venta.py
badd +419 ginn/framework/configuracion.py
badd +4 bin/ginn.sh
badd +10 ginn/main.py
badd +292 ginn/formularios/ventana.py
badd +1858 ginn/formularios/pedidos_de_venta.py
badd +1431 db/tablas.sql
badd +810 ginn/formularios/albaranes_de_salida.py
badd +1 ginn/formularios/presupuesto.py
badd +1283 ginn/formularios/presupuestos.py
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
badd +476 ginn/framework/seeker.py
badd +13 ginn/formularios/crm_seguimiento_impagos.py
badd +203 ginn/formularios/productos.py
badd +1064 ginn/formularios/trazabilidad_articulos.py
badd +363 ginn/formularios/consulta_pagos.py
badd +13 ginn/formularios/consulta_vencimientos_pago.py
badd +500 ginn/formularios/trazabilidad.py
badd +83 ginn/framework/pclases/__init__.py
badd +611 ginn/framework/pclases/superfacturaventa.py
badd +47 ginn/framework/pclases/facturaventa.py
badd +689 ginn/formularios/consulta_mensual_nominas.py
badd +269 ginn/informes/treeview2pdf.py
badd +129 ginn/formularios/balas_cable.py
badd +13 ginn/informes/nied.py
badd +118 ginn/informes/norma2013.py
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
badd +1 ginn/framework/__init__.py
badd +1 ginn/formularios/vencimientos_pendientes_por_cliente.glade
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
wincmd _ | wincmd |
split
10wincmd k
wincmd w
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
exe '6resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 6resize ' . ((&columns * 80 + 55) / 111)
exe '7resize ' . ((&lines * 22 + 22) / 44)
exe 'vert 7resize ' . ((&columns * 80 + 55) / 111)
exe '8resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 8resize ' . ((&columns * 80 + 55) / 111)
exe '9resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 9resize ' . ((&columns * 80 + 55) / 111)
exe '10resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 10resize ' . ((&columns * 80 + 55) / 111)
exe '11resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 11resize ' . ((&columns * 80 + 55) / 111)
exe '12resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 12resize ' . ((&columns * 80 + 55) / 111)
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
2229
silent! normal zo
2250
silent! normal zo
2292
silent! normal zo
4726
silent! normal zo
4739
silent! normal zo
4745
silent! normal zo
9718
silent! normal zo
9734
silent! normal zo
10068
silent! normal zo
10147
silent! normal zo
10173
silent! normal zo
10185
silent! normal zo
10190
silent! normal zo
10200
silent! normal zo
10205
silent! normal zo
10211
silent! normal zo
10382
silent! normal zo
10388
silent! normal zo
10413
silent! normal zo
10416
silent! normal zo
10436
silent! normal zo
14155
silent! normal zo
14584
silent! normal zo
14594
silent! normal zo
14907
silent! normal zo
15102
silent! normal zo
15129
silent! normal zo
17891
silent! normal zo
17937
silent! normal zo
19404
silent! normal zo
19458
silent! normal zo
19505
silent! normal zo
19527
silent! normal zo
19536
silent! normal zo
19561
silent! normal zo
19816
silent! normal zo
19879
silent! normal zo
19893
silent! normal zo
let s:l = 10225 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
10225
normal! 041l
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
let s:l = 513 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
513
normal! 046l
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
733
silent! normal zo
let s:l = 814 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
814
normal! 034l
wincmd w
argglobal
edit db/tablas.sql
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
1391
silent! normal zo
let s:l = 1442 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1442
normal! 012l
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
silent! normal zo
493
silent! normal zo
1006
silent! normal zo
1047
silent! normal zo
1270
silent! normal zo
1344
silent! normal zo
1344
silent! normal zo
1344
silent! normal zo
1344
silent! normal zo
1344
silent! normal zo
1344
silent! normal zo
1344
silent! normal zo
1352
silent! normal zo
1353
silent! normal zo
1354
silent! normal zo
1361
silent! normal zo
1362
silent! normal zo
1362
silent! normal zo
1363
silent! normal zo
1365
silent! normal zo
1366
silent! normal zo
1366
silent! normal zo
1366
silent! normal zo
1370
silent! normal zo
1371
silent! normal zo
1371
silent! normal zo
1374
silent! normal zo
1376
silent! normal zo
1389
silent! normal zo
1389
silent! normal zo
1389
silent! normal zo
1395
silent! normal zo
1395
silent! normal zo
1395
silent! normal zo
1395
silent! normal zo
1665
silent! normal zo
1684
silent! normal zo
1700
silent! normal zo
1703
silent! normal zo
1704
silent! normal zo
1704
silent! normal zo
1704
silent! normal zo
1704
silent! normal zo
1704
silent! normal zo
1717
silent! normal zo
1717
silent! normal zo
1717
silent! normal zo
1717
silent! normal zo
1717
silent! normal zo
1717
silent! normal zo
1943
silent! normal zo
1946
silent! normal zo
1950
silent! normal zo
let s:l = 1398 - ((13 * winheight(0) + 11) / 22)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1398
normal! 08l
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
7wincmd w
exe 'vert 1resize ' . ((&columns * 30 + 55) / 111)
exe '2resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 2resize ' . ((&columns * 80 + 55) / 111)
exe '3resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 3resize ' . ((&columns * 80 + 55) / 111)
exe '4resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 4resize ' . ((&columns * 80 + 55) / 111)
exe '5resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 5resize ' . ((&columns * 80 + 55) / 111)
exe '6resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 6resize ' . ((&columns * 80 + 55) / 111)
exe '7resize ' . ((&lines * 22 + 22) / 44)
exe 'vert 7resize ' . ((&columns * 80 + 55) / 111)
exe '8resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 8resize ' . ((&columns * 80 + 55) / 111)
exe '9resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 9resize ' . ((&columns * 80 + 55) / 111)
exe '10resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 10resize ' . ((&columns * 80 + 55) / 111)
exe '11resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 11resize ' . ((&columns * 80 + 55) / 111)
exe '12resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 12resize ' . ((&columns * 80 + 55) / 111)
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
