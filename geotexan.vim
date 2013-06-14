" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 13 junio 2013 at 20:59:13.
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
badd +0 ginn/formularios/tarifas_de_precios.py
args formularios/auditviewer.py
set lines=62 columns=80
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
4wincmd k
wincmd w
wincmd w
wincmd w
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
exe '1resize ' . ((&lines * 1 + 31) / 62)
exe '2resize ' . ((&lines * 12 + 31) / 62)
exe '3resize ' . ((&lines * 1 + 31) / 62)
exe '4resize ' . ((&lines * 41 + 31) / 62)
exe '5resize ' . ((&lines * 1 + 31) / 62)
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
normal! zo
409
normal! zo
418
normal! zo
421
normal! zo
581
normal! zo
587
normal! zo
588
normal! zo
589
normal! zo
640
normal! zo
641
normal! zo
2041
normal! zo
2217
normal! zo
2238
normal! zo
2351
normal! zo
2550
normal! zo
2591
normal! zo
2596
normal! zo
2616
normal! zo
2617
normal! zo
2747
normal! zo
3130
normal! zo
3778
normal! zo
3827
normal! zo
4690
normal! zo
4703
normal! zo
4709
normal! zo
4717
normal! zo
4730
normal! zo
4787
normal! zo
5283
normal! zo
5396
normal! zo
5463
normal! zo
5463
normal! zo
5463
normal! zo
5463
normal! zo
5463
normal! zo
5525
normal! zo
5931
normal! zo
6064
normal! zo
6201
normal! zo
6227
normal! zo
6363
normal! zo
6390
normal! zo
6650
normal! zo
6658
normal! zo
7430
normal! zo
7436
normal! zo
7459
normal! zo
7459
normal! zo
7459
normal! zo
7459
normal! zo
7459
normal! zo
7483
normal! zo
7607
normal! zo
7607
normal! zo
7607
normal! zo
7607
normal! zo
7607
normal! zo
7607
normal! zo
7701
normal! zo
7702
normal! zo
7711
normal! zo
7726
normal! zo
7736
normal! zo
7760
normal! zo
7760
normal! zo
7760
normal! zo
7760
normal! zo
7760
normal! zo
7760
normal! zo
7760
normal! zo
7847
normal! zo
8162
normal! zo
8202
normal! zo
8248
normal! zo
8251
normal! zo
8252
normal! zo
8345
normal! zo
8349
normal! zo
8349
normal! zo
8349
normal! zo
8831
normal! zo
8856
normal! zo
8857
normal! zo
8866
normal! zo
8867
normal! zo
8868
normal! zo
8896
normal! zo
8949
normal! zo
9200
normal! zo
9643
normal! zo
9659
normal! zo
9676
normal! zo
9676
normal! zo
9676
normal! zo
9676
normal! zo
9676
normal! zo
9676
normal! zo
9676
normal! zo
9676
normal! zo
9676
normal! zo
9683
normal! zo
9689
normal! zo
9690
normal! zo
9693
normal! zo
9695
normal! zo
9695
normal! zo
9695
normal! zo
9701
normal! zo
9703
normal! zo
9705
normal! zo
9705
normal! zo
9708
normal! zo
9709
normal! zo
9709
normal! zo
9716
normal! zo
9724
normal! zo
9727
normal! zo
9731
normal! zo
9733
normal! zo
9765
normal! zo
9832
normal! zo
9844
normal! zo
9845
normal! zo
9930
normal! zo
9936
normal! zo
9942
normal! zo
9949
normal! zo
10124
normal! zo
10132
normal! zo
11317
normal! zo
11317
normal! zo
11317
normal! zo
11783
normal! zo
11783
normal! zo
11783
normal! zo
11783
normal! zo
11783
normal! zo
11783
normal! zo
11783
normal! zo
13220
normal! zo
13220
normal! zo
13220
normal! zo
13220
normal! zo
13241
normal! zo
13249
normal! zo
13258
normal! zo
13259
normal! zo
13670
normal! zo
13856
normal! zo
14668
normal! zo
14681
normal! zo
14686
normal! zo
14694
normal! zo
14707
normal! zo
15108
normal! zo
15124
normal! zo
15129
normal! zo
15344
normal! zo
15356
normal! zo
15357
normal! zo
15718
normal! zo
16156
normal! zo
16166
normal! zo
17441
normal! zo
17500
normal! zo
17514
normal! zo
17520
normal! zo
17525
normal! zo
19544
normal! zo
19558
normal! zo
19630
normal! zo
19683
normal! zo
19690
normal! zo
19695
normal! zo
19695
normal! zo
19695
normal! zo
20384
normal! zo
20405
normal! zo
20414
normal! zo
20414
normal! zo
20414
normal! zo
20567
normal! zo
20665
normal! zo
21133
normal! zo
21155
normal! zo
21189
normal! zo
21221
normal! zo
21353
normal! zo
21915
normal! zo
21922
normal! zo
21924
normal! zo
21928
normal! zo
21938
normal! zo
21943
normal! zo
21943
normal! zo
22084
normal! zo
22102
normal! zo
22105
normal! zo
22124
normal! zo
22139
normal! zo
22140
normal! zo
22215
normal! zo
22219
normal! zo
let s:l = 9698 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
9698
normal! 031|
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
normal! zo
114
normal! zo
132
normal! zo
132
normal! zo
157
normal! zo
215
normal! zo
let s:l = 263 - ((4 * winheight(0) + 6) / 12)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
263
normal! 027|
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
normal! zo
67
normal! zo
68
normal! zo
68
normal! zo
105
normal! zo
275
normal! zo
340
normal! zo
383
normal! zo
561
normal! zo
569
normal! zo
595
normal! zo
612
normal! zo
640
normal! zo
640
normal! zo
640
normal! zo
640
normal! zo
678
normal! zo
679
normal! zo
807
normal! zo
818
normal! zo
879
normal! zo
908
normal! zo
914
normal! zo
1039
normal! zo
let s:l = 109 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
109
normal! 013|
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
normal! zo
103
normal! zo
103
normal! zo
103
normal! zo
103
normal! zo
103
normal! zo
103
normal! zo
121
normal! zo
122
normal! zo
134
normal! zo
134
normal! zo
134
normal! zo
144
normal! zo
174
normal! zo
189
normal! zo
191
normal! zo
191
normal! zo
191
normal! zo
191
normal! zo
191
normal! zo
197
normal! zo
207
normal! zo
214
normal! zo
214
normal! zo
215
normal! zo
218
normal! zo
222
normal! zo
225
normal! zo
230
normal! zo
233
normal! zo
252
normal! zo
259
normal! zo
259
normal! zo
259
normal! zo
259
normal! zo
259
normal! zo
262
normal! zo
264
normal! zo
269
normal! zo
275
normal! zo
282
normal! zo
285
normal! zo
307
normal! zo
307
normal! zo
307
normal! zo
307
normal! zo
307
normal! zo
307
normal! zo
307
normal! zo
307
normal! zo
314
normal! zo
330
normal! zo
332
normal! zo
352
normal! zo
359
normal! zo
392
normal! zo
394
normal! zo
420
normal! zo
481
normal! zo
485
normal! zo
490
normal! zo
502
normal! zo
510
normal! zo
538
normal! zo
629
normal! zo
644
normal! zo
645
normal! zo
645
normal! zo
691
normal! zo
712
normal! zo
747
normal! zo
747
normal! zo
780
normal! zo
780
normal! zo
829
normal! zo
829
normal! zo
847
normal! zo
875
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
943
normal! zo
943
normal! zo
947
normal! zo
950
normal! zo
1032
normal! zo
1040
normal! zo
1043
normal! zo
1045
normal! zo
1052
normal! zo
1053
normal! zo
1075
normal! zo
1109
normal! zo
1127
normal! zo
1136
normal! zo
1137
normal! zo
1137
normal! zo
1137
normal! zo
1144
normal! zo
1144
normal! zo
1144
normal! zo
1144
normal! zo
1144
normal! zo
1144
normal! zo
1144
normal! zo
1144
normal! zo
1159
normal! zo
1283
normal! zo
1332
normal! zo
1376
normal! zo
1377
normal! zo
1380
normal! zo
1397
normal! zo
1403
normal! zo
1417
normal! zo
1427
normal! zo
1428
normal! zo
1471
normal! zo
1483
normal! zo
1555
normal! zo
1568
normal! zo
1569
normal! zo
1583
normal! zo
1613
normal! zo
1655
normal! zo
1674
normal! zo
1687
normal! zo
1687
normal! zo
1687
normal! zo
1698
normal! zo
1788
normal! zo
1840
normal! zo
1840
normal! zo
1840
normal! zo
1846
normal! zo
1861
normal! zo
1876
normal! zo
1902
normal! zo
1914
normal! zo
1915
normal! zo
1915
normal! zo
1916
normal! zo
1937
normal! zo
1950
normal! zo
1951
normal! zo
1954
normal! zo
1991
normal! zo
1994
normal! zo
2042
normal! zo
2051
normal! zo
2127
normal! zo
2140
normal! zo
2148
normal! zo
2192
normal! zo
2209
normal! zo
2212
normal! zo
2213
normal! zo
2214
normal! zo
2219
normal! zo
2221
normal! zo
2222
normal! zo
2230
normal! zo
2343
normal! zo
2381
normal! zo
2392
normal! zo
2402
normal! zo
2413
normal! zo
2454
normal! zo
2462
normal! zo
2471
normal! zo
2476
normal! zo
2489
normal! zo
2508
normal! zo
2525
normal! zo
2534
normal! zo
2594
normal! zo
2594
normal! zo
2594
normal! zo
2594
normal! zo
2595
normal! zo
2599
normal! zo
2626
normal! zo
2631
normal! zo
2633
normal! zo
2634
normal! zo
2666
normal! zo
2680
normal! zo
2680
normal! zo
2680
normal! zo
2680
normal! zo
2680
normal! zo
2680
normal! zo
2680
normal! zo
2692
normal! zo
let s:l = 954 - ((28 * winheight(0) + 20) / 41)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
954
normal! 039|
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
normal! zo
93
normal! zo
288
normal! zo
296
normal! zo
333
normal! zo
335
normal! zo
337
normal! zo
348
normal! zo
352
normal! zo
400
normal! zo
403
normal! zo
415
normal! zo
415
normal! zo
425
normal! zo
428
normal! zo
437
normal! zo
635
normal! zo
639
normal! zo
let s:l = 322 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
322
normal! 021|
wincmd w
4wincmd w
exe '1resize ' . ((&lines * 1 + 31) / 62)
exe '2resize ' . ((&lines * 12 + 31) / 62)
exe '3resize ' . ((&lines * 1 + 31) / 62)
exe '4resize ' . ((&lines * 41 + 31) / 62)
exe '5resize ' . ((&lines * 1 + 31) / 62)
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
