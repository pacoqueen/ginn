" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 17 junio 2013 at 17:06:56.
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
badd +175 ~/.vimrc
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
badd +10 ginn/formularios/dynconsulta.py
badd +1 ginn/framework/pclases.py
badd +43 ginn/formularios/historico_existencias_compra.py
badd +39 ginn/formularios/historico_existencias.py
badd +46 ginn/formularios/consulta_incidencias.py
badd +39 ginn/formularios/consulta_producido.py
badd +1 ginn/__init__.py
badd +1542 ginn/formularios/clientes.py
badd +314 ginn/formularios/productos_compra.py
badd +323 ginn/formularios/productos_de_venta_balas.py
badd +525 ginn/formularios/recibos.py
badd +2147 ginn/formularios/productos_de_venta_rollos.py
badd +643 ginn/formularios/productos_de_venta_rollos_geocompuestos.py
badd +305 ginn/formularios/productos_de_venta_especial.py
badd +3998 ginn/formularios/partes_de_fabricacion_balas.py
badd +1927 ginn/formularios/partes_de_fabricacion_bolsas.py
badd +961 ginn/formularios/partes_de_fabricacion_rollos.py
badd +669 ginn/formularios/proveedores.py
badd +547 ~/workspace/CICAN/src/formularios/menu.py
badd +68 ginn/formularios/launcher.py
badd +492 ginn/formularios/empleados.py
badd +38 ginn/formularios/resultados_geotextiles.py
badd +854 ginn/formularios/menu.py
badd +142 ginn/formularios/autenticacion.py
badd +1502 ginn/informes/geninformes.py
badd +233 ginn/informes/informe_certificado_calidad.py
badd +1518 informes/geninformes.py
badd +371 ginn/formularios/facturas_venta.py
badd +468 ginn/framework/configuracion.py
badd +4 bin/ginn.sh
badd +10 ginn/main.py
badd +570 ginn/formularios/ventana.py
badd +2713 ginn/formularios/pedidos_de_venta.py
badd +867 db/tablas.sql
badd +2045 ginn/formularios/albaranes_de_salida.py
badd +1 ginn/formularios/presupuesto.py
badd +359 ginn/formularios/presupuestos.py
badd +412 ginn/informes/presupuesto2.py
badd +1 ginn/formularios/tarifas_de_precios.py
args formularios/auditviewer.py
set lines=58 columns=80
edit ginn/framework/pclases.py
set splitbelow splitright
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
6wincmd k
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
exe '1resize ' . ((&lines * 1 + 29) / 58)
exe '2resize ' . ((&lines * 1 + 29) / 58)
exe '3resize ' . ((&lines * 1 + 29) / 58)
exe '4resize ' . ((&lines * 1 + 29) / 58)
exe '5resize ' . ((&lines * 20 + 29) / 58)
exe '6resize ' . ((&lines * 19 + 29) / 58)
exe '7resize ' . ((&lines * 7 + 29) / 58)
argglobal
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
263
silent! normal zo
409
silent! normal zo
418
silent! normal zo
421
silent! normal zo
581
silent! normal zo
587
silent! normal zo
588
silent! normal zo
589
silent! normal zo
640
silent! normal zo
641
silent! normal zo
2041
silent! normal zo
2217
silent! normal zo
2238
silent! normal zo
2351
silent! normal zo
2550
silent! normal zo
2591
silent! normal zo
2596
silent! normal zo
2616
silent! normal zo
2617
silent! normal zo
2747
silent! normal zo
3130
silent! normal zo
3778
silent! normal zo
3827
silent! normal zo
4690
silent! normal zo
4703
silent! normal zo
4709
silent! normal zo
4717
silent! normal zo
4730
silent! normal zo
4787
silent! normal zo
5283
silent! normal zo
5396
silent! normal zo
5463
silent! normal zo
5463
silent! normal zo
5463
silent! normal zo
5463
silent! normal zo
5463
silent! normal zo
5525
silent! normal zo
5931
silent! normal zo
6064
silent! normal zo
6201
silent! normal zo
6227
silent! normal zo
6363
silent! normal zo
6390
silent! normal zo
6650
silent! normal zo
6658
silent! normal zo
7430
silent! normal zo
7436
silent! normal zo
7459
silent! normal zo
7459
silent! normal zo
7459
silent! normal zo
7459
silent! normal zo
7459
silent! normal zo
7483
silent! normal zo
7607
silent! normal zo
7607
silent! normal zo
7607
silent! normal zo
7607
silent! normal zo
7607
silent! normal zo
7607
silent! normal zo
7701
silent! normal zo
7702
silent! normal zo
7711
silent! normal zo
7726
silent! normal zo
7736
silent! normal zo
7760
silent! normal zo
7760
silent! normal zo
7760
silent! normal zo
7760
silent! normal zo
7760
silent! normal zo
7760
silent! normal zo
7760
silent! normal zo
7847
silent! normal zo
8162
silent! normal zo
8202
silent! normal zo
8248
silent! normal zo
8251
silent! normal zo
8252
silent! normal zo
8345
silent! normal zo
8349
silent! normal zo
8349
silent! normal zo
8349
silent! normal zo
8831
silent! normal zo
8856
silent! normal zo
8857
silent! normal zo
8866
silent! normal zo
8867
silent! normal zo
8868
silent! normal zo
8896
silent! normal zo
8949
silent! normal zo
9200
silent! normal zo
9643
silent! normal zo
9659
silent! normal zo
9676
silent! normal zo
9676
silent! normal zo
9676
silent! normal zo
9676
silent! normal zo
9676
silent! normal zo
9676
silent! normal zo
9676
silent! normal zo
9676
silent! normal zo
9676
silent! normal zo
9683
silent! normal zo
9689
silent! normal zo
9690
silent! normal zo
9693
silent! normal zo
9695
silent! normal zo
9695
silent! normal zo
9695
silent! normal zo
9701
silent! normal zo
9703
silent! normal zo
9705
silent! normal zo
9705
silent! normal zo
9708
silent! normal zo
9709
silent! normal zo
9709
silent! normal zo
9716
silent! normal zo
9724
silent! normal zo
9727
silent! normal zo
9731
silent! normal zo
9733
silent! normal zo
9765
silent! normal zo
9832
silent! normal zo
9844
silent! normal zo
9845
silent! normal zo
9930
silent! normal zo
9936
silent! normal zo
9942
silent! normal zo
9949
silent! normal zo
10124
silent! normal zo
10132
silent! normal zo
11317
silent! normal zo
11317
silent! normal zo
11317
silent! normal zo
11783
silent! normal zo
11783
silent! normal zo
11783
silent! normal zo
11783
silent! normal zo
11783
silent! normal zo
11783
silent! normal zo
11783
silent! normal zo
13220
silent! normal zo
13220
silent! normal zo
13220
silent! normal zo
13220
silent! normal zo
13241
silent! normal zo
13249
silent! normal zo
13258
silent! normal zo
13259
silent! normal zo
13670
silent! normal zo
13856
silent! normal zo
14668
silent! normal zo
14681
silent! normal zo
14686
silent! normal zo
14694
silent! normal zo
14707
silent! normal zo
15108
silent! normal zo
15124
silent! normal zo
15129
silent! normal zo
15344
silent! normal zo
15356
silent! normal zo
15357
silent! normal zo
15718
silent! normal zo
16156
silent! normal zo
16166
silent! normal zo
17441
silent! normal zo
17500
silent! normal zo
17514
silent! normal zo
17520
silent! normal zo
17525
silent! normal zo
19544
silent! normal zo
19558
silent! normal zo
19630
silent! normal zo
19683
silent! normal zo
19690
silent! normal zo
19695
silent! normal zo
19695
silent! normal zo
19695
silent! normal zo
20384
silent! normal zo
20405
silent! normal zo
20414
silent! normal zo
20414
silent! normal zo
20414
silent! normal zo
20567
silent! normal zo
20665
silent! normal zo
21133
silent! normal zo
21155
silent! normal zo
21189
silent! normal zo
21221
silent! normal zo
21353
silent! normal zo
21915
silent! normal zo
21922
silent! normal zo
21924
silent! normal zo
21928
silent! normal zo
21938
silent! normal zo
21943
silent! normal zo
21943
silent! normal zo
22084
silent! normal zo
22102
silent! normal zo
22105
silent! normal zo
22124
silent! normal zo
22139
silent! normal zo
22140
silent! normal zo
22215
silent! normal zo
22219
silent! normal zo
let s:l = 9698 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
9698
normal! 030l
wincmd w
argglobal
edit ginn/formularios/dynconsulta.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
113
silent! normal zo
114
silent! normal zo
114
silent! normal zo
132
silent! normal zo
132
silent! normal zo
157
silent! normal zo
215
silent! normal zo
let s:l = 263 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
263
normal! 026l
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
41
silent! normal zo
67
silent! normal zo
68
silent! normal zo
68
silent! normal zo
105
silent! normal zo
275
silent! normal zo
340
silent! normal zo
383
silent! normal zo
561
silent! normal zo
569
silent! normal zo
595
silent! normal zo
612
silent! normal zo
640
silent! normal zo
640
silent! normal zo
640
silent! normal zo
640
silent! normal zo
678
silent! normal zo
679
silent! normal zo
807
silent! normal zo
818
silent! normal zo
879
silent! normal zo
908
silent! normal zo
914
silent! normal zo
1039
silent! normal zo
let s:l = 109 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
109
normal! 012l
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
96
silent! normal zo
103
silent! normal zo
103
silent! normal zo
103
silent! normal zo
103
silent! normal zo
103
silent! normal zo
103
silent! normal zo
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
144
silent! normal zo
174
silent! normal zo
189
silent! normal zo
191
silent! normal zo
191
silent! normal zo
191
silent! normal zo
191
silent! normal zo
191
silent! normal zo
197
silent! normal zo
207
silent! normal zo
214
silent! normal zo
214
silent! normal zo
215
silent! normal zo
218
silent! normal zo
222
silent! normal zo
225
silent! normal zo
230
silent! normal zo
233
silent! normal zo
252
silent! normal zo
259
silent! normal zo
259
silent! normal zo
259
silent! normal zo
259
silent! normal zo
259
silent! normal zo
262
silent! normal zo
264
silent! normal zo
269
silent! normal zo
275
silent! normal zo
282
silent! normal zo
285
silent! normal zo
307
silent! normal zo
307
silent! normal zo
307
silent! normal zo
307
silent! normal zo
307
silent! normal zo
307
silent! normal zo
307
silent! normal zo
307
silent! normal zo
314
silent! normal zo
330
silent! normal zo
332
silent! normal zo
352
silent! normal zo
359
silent! normal zo
392
silent! normal zo
394
silent! normal zo
420
silent! normal zo
481
silent! normal zo
485
silent! normal zo
490
silent! normal zo
502
silent! normal zo
510
silent! normal zo
538
silent! normal zo
629
silent! normal zo
644
silent! normal zo
645
silent! normal zo
645
silent! normal zo
691
silent! normal zo
712
silent! normal zo
747
silent! normal zo
747
silent! normal zo
780
silent! normal zo
780
silent! normal zo
829
silent! normal zo
829
silent! normal zo
847
silent! normal zo
875
silent! normal zo
943
silent! normal zo
943
silent! normal zo
943
silent! normal zo
943
silent! normal zo
943
silent! normal zo
943
silent! normal zo
943
silent! normal zo
943
silent! normal zo
947
silent! normal zo
950
silent! normal zo
1032
silent! normal zo
1040
silent! normal zo
1043
silent! normal zo
1045
silent! normal zo
1052
silent! normal zo
1053
silent! normal zo
1075
silent! normal zo
1109
silent! normal zo
1127
silent! normal zo
1136
silent! normal zo
1137
silent! normal zo
1137
silent! normal zo
1137
silent! normal zo
1144
silent! normal zo
1144
silent! normal zo
1144
silent! normal zo
1144
silent! normal zo
1144
silent! normal zo
1144
silent! normal zo
1144
silent! normal zo
1144
silent! normal zo
1159
silent! normal zo
1283
silent! normal zo
1332
silent! normal zo
1376
silent! normal zo
1377
silent! normal zo
1380
silent! normal zo
1397
silent! normal zo
1403
silent! normal zo
1417
silent! normal zo
1427
silent! normal zo
1428
silent! normal zo
1471
silent! normal zo
1483
silent! normal zo
1555
silent! normal zo
1568
silent! normal zo
1569
silent! normal zo
1583
silent! normal zo
1613
silent! normal zo
1655
silent! normal zo
1674
silent! normal zo
1687
silent! normal zo
1687
silent! normal zo
1687
silent! normal zo
1698
silent! normal zo
1788
silent! normal zo
1840
silent! normal zo
1840
silent! normal zo
1840
silent! normal zo
1846
silent! normal zo
1861
silent! normal zo
1876
silent! normal zo
1902
silent! normal zo
1914
silent! normal zo
1915
silent! normal zo
1915
silent! normal zo
1916
silent! normal zo
1937
silent! normal zo
1950
silent! normal zo
1951
silent! normal zo
1954
silent! normal zo
1991
silent! normal zo
1994
silent! normal zo
2042
silent! normal zo
2051
silent! normal zo
2127
silent! normal zo
2140
silent! normal zo
2148
silent! normal zo
2192
silent! normal zo
2209
silent! normal zo
2212
silent! normal zo
2213
silent! normal zo
2214
silent! normal zo
2219
silent! normal zo
2221
silent! normal zo
2222
silent! normal zo
2230
silent! normal zo
2343
silent! normal zo
2381
silent! normal zo
2392
silent! normal zo
2402
silent! normal zo
2413
silent! normal zo
2454
silent! normal zo
2462
silent! normal zo
2471
silent! normal zo
2476
silent! normal zo
2489
silent! normal zo
2508
silent! normal zo
2525
silent! normal zo
2534
silent! normal zo
2594
silent! normal zo
2594
silent! normal zo
2594
silent! normal zo
2594
silent! normal zo
2595
silent! normal zo
2599
silent! normal zo
2626
silent! normal zo
2631
silent! normal zo
2633
silent! normal zo
2634
silent! normal zo
2666
silent! normal zo
2680
silent! normal zo
2680
silent! normal zo
2680
silent! normal zo
2680
silent! normal zo
2680
silent! normal zo
2680
silent! normal zo
2680
silent! normal zo
2692
silent! normal zo
let s:l = 971 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
971
normal! 035l
wincmd w
argglobal
edit ginn/formularios/partes_de_fabricacion_rollos.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 2315 - ((17 * winheight(0) + 10) / 20)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2315
normal! 022l
wincmd w
argglobal
edit ginn/formularios/partes_de_fabricacion_balas.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
108
silent! normal zo
571
silent! normal zo
578
silent! normal zo
let s:l = 590 - ((12 * winheight(0) + 9) / 19)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
590
normal! 058l
wincmd w
argglobal
edit ginn/formularios/tarifas_de_precios.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
92
silent! normal zo
93
silent! normal zo
288
silent! normal zo
296
silent! normal zo
333
silent! normal zo
335
silent! normal zo
337
silent! normal zo
348
silent! normal zo
352
silent! normal zo
400
silent! normal zo
403
silent! normal zo
415
silent! normal zo
415
silent! normal zo
425
silent! normal zo
428
silent! normal zo
437
silent! normal zo
635
silent! normal zo
639
silent! normal zo
let s:l = 322 - ((4 * winheight(0) + 3) / 7)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
322
normal! 032l
wincmd w
6wincmd w
exe '1resize ' . ((&lines * 1 + 29) / 58)
exe '2resize ' . ((&lines * 1 + 29) / 58)
exe '3resize ' . ((&lines * 1 + 29) / 58)
exe '4resize ' . ((&lines * 1 + 29) / 58)
exe '5resize ' . ((&lines * 20 + 29) / 58)
exe '6resize ' . ((&lines * 19 + 29) / 58)
exe '7resize ' . ((&lines * 7 + 29) / 58)
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
