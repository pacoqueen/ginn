" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 12 junio 2013 at 17:10:50.
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
badd +977 ginn/formularios/menu.py
badd +142 ginn/formularios/autenticacion.py
badd +1502 ginn/informes/geninformes.py
badd +233 ginn/informes/informe_certificado_calidad.py
badd +1518 informes/geninformes.py
badd +371 ginn/formularios/facturas_venta.py
badd +468 ginn/framework/configuracion.py
badd +4 bin/ginn.sh
badd +10 ginn/main.py
badd +570 ginn/formularios/ventana.py
badd +258 ginn/formularios/pedidos_de_venta.py
badd +867 db/tablas.sql
badd +0 ginn/formularios/albaranes_de_salida.py
badd +1 ginn/formularios/presupuesto.py
badd +359 ginn/formularios/presupuestos.py
badd +0 ginn/informes/presupuesto2.py
args formularios/auditviewer.py
set lines=44 columns=80
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
5wincmd k
wincmd w
wincmd w
wincmd w
wincmd w
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
exe '1resize ' . ((&lines * 19 + 22) / 44)
exe '2resize ' . ((&lines * 14 + 22) / 44)
exe '3resize ' . ((&lines * 1 + 22) / 44)
exe '4resize ' . ((&lines * 1 + 22) / 44)
exe '5resize ' . ((&lines * 1 + 22) / 44)
exe '6resize ' . ((&lines * 1 + 22) / 44)
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
7483
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
9698
silent! normal zo
9700
silent! normal zo
9702
silent! normal zo
9702
silent! normal zo
9704
silent! normal zo
9704
silent! normal zo
9704
silent! normal zo
9704
silent! normal zo
9705
silent! normal zo
9705
silent! normal zo
9706
silent! normal zo
9706
silent! normal zo
9713
silent! normal zo
9721
silent! normal zo
9724
silent! normal zo
9728
silent! normal zo
9730
silent! normal zo
9762
silent! normal zo
9829
silent! normal zo
9841
silent! normal zo
9842
silent! normal zo
9927
silent! normal zo
9933
silent! normal zo
9939
silent! normal zo
9946
silent! normal zo
10121
silent! normal zo
10129
silent! normal zo
11314
silent! normal zo
11780
silent! normal zo
13217
silent! normal zo
13238
silent! normal zo
13246
silent! normal zo
13255
silent! normal zo
13256
silent! normal zo
13667
silent! normal zo
13853
silent! normal zo
14665
silent! normal zo
14678
silent! normal zo
14683
silent! normal zo
14691
silent! normal zo
14704
silent! normal zo
15105
silent! normal zo
15121
silent! normal zo
15126
silent! normal zo
15341
silent! normal zo
15353
silent! normal zo
15354
silent! normal zo
15715
silent! normal zo
17438
silent! normal zo
17497
silent! normal zo
17511
silent! normal zo
17517
silent! normal zo
17522
silent! normal zo
19541
silent! normal zo
19555
silent! normal zo
19627
silent! normal zo
19680
silent! normal zo
19687
silent! normal zo
19692
silent! normal zo
19692
silent! normal zo
19692
silent! normal zo
20381
silent! normal zo
20402
silent! normal zo
20411
silent! normal zo
20411
silent! normal zo
20411
silent! normal zo
20564
silent! normal zo
20662
silent! normal zo
21130
silent! normal zo
21152
silent! normal zo
21186
silent! normal zo
21218
silent! normal zo
21912
silent! normal zo
21919
silent! normal zo
21921
silent! normal zo
21925
silent! normal zo
21935
silent! normal zo
21940
silent! normal zo
21940
silent! normal zo
22081
silent! normal zo
22099
silent! normal zo
22102
silent! normal zo
22121
silent! normal zo
22136
silent! normal zo
22137
silent! normal zo
22212
silent! normal zo
22216
silent! normal zo
let s:l = 19692 - ((9 * winheight(0) + 9) / 19)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
19692
normal! 026l
wincmd w
argglobal
edit ginn/formularios/menu.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
150
silent! normal zo
213
silent! normal zo
227
silent! normal zo
228
silent! normal zo
229
silent! normal zo
229
silent! normal zo
229
silent! normal zo
238
silent! normal zo
239
silent! normal zo
240
silent! normal zo
240
silent! normal zo
240
silent! normal zo
240
silent! normal zo
240
silent! normal zo
311
silent! normal zo
348
silent! normal zo
349
silent! normal zo
580
silent! normal zo
607
silent! normal zo
614
silent! normal zo
615
silent! normal zo
641
silent! normal zo
643
silent! normal zo
644
silent! normal zo
824
silent! normal zo
835
silent! normal zo
let s:l = 835 - ((6 * winheight(0) + 7) / 14)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
835
normal! 024l
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
edit ginn/formularios/albaranes_de_salida.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
98
silent! normal zo
99
silent! normal zo
111
silent! normal zo
111
silent! normal zo
111
silent! normal zo
1133
silent! normal zo
1980
silent! normal zo
2014
silent! normal zo
2019
silent! normal zo
2040
silent! normal zo
2041
silent! normal zo
2041
silent! normal zo
2042
silent! normal zo
3826
silent! normal zo
3860
silent! normal zo
3914
silent! normal zo
let s:l = 2038 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2038
normal! 028l
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
45
silent! normal zo
49
silent! normal zo
250
silent! normal zo
269
silent! normal zo
311
silent! normal zo
416
silent! normal zo
419
silent! normal zo
let s:l = 389 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
389
normal! 019l
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
95
silent! normal zo
102
silent! normal zo
102
silent! normal zo
102
silent! normal zo
102
silent! normal zo
102
silent! normal zo
102
silent! normal zo
121
silent! normal zo
122
silent! normal zo
135
silent! normal zo
135
silent! normal zo
135
silent! normal zo
145
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
826
silent! normal zo
826
silent! normal zo
844
silent! normal zo
872
silent! normal zo
940
silent! normal zo
940
silent! normal zo
940
silent! normal zo
940
silent! normal zo
940
silent! normal zo
940
silent! normal zo
940
silent! normal zo
940
silent! normal zo
1013
silent! normal zo
1021
silent! normal zo
1024
silent! normal zo
1026
silent! normal zo
1033
silent! normal zo
1034
silent! normal zo
1056
silent! normal zo
1090
silent! normal zo
1108
silent! normal zo
1117
silent! normal zo
1118
silent! normal zo
1118
silent! normal zo
1118
silent! normal zo
1125
silent! normal zo
1125
silent! normal zo
1125
silent! normal zo
1125
silent! normal zo
1125
silent! normal zo
1125
silent! normal zo
1125
silent! normal zo
1125
silent! normal zo
1140
silent! normal zo
1264
silent! normal zo
1313
silent! normal zo
1357
silent! normal zo
1358
silent! normal zo
1361
silent! normal zo
1378
silent! normal zo
1384
silent! normal zo
1398
silent! normal zo
1408
silent! normal zo
1409
silent! normal zo
1452
silent! normal zo
1464
silent! normal zo
1536
silent! normal zo
1549
silent! normal zo
1550
silent! normal zo
1564
silent! normal zo
1594
silent! normal zo
1636
silent! normal zo
1655
silent! normal zo
1668
silent! normal zo
1679
silent! normal zo
1769
silent! normal zo
1821
silent! normal zo
1821
silent! normal zo
1821
silent! normal zo
1827
silent! normal zo
1842
silent! normal zo
1857
silent! normal zo
1883
silent! normal zo
1895
silent! normal zo
1896
silent! normal zo
1896
silent! normal zo
1897
silent! normal zo
1918
silent! normal zo
1931
silent! normal zo
1932
silent! normal zo
1935
silent! normal zo
1972
silent! normal zo
1975
silent! normal zo
2023
silent! normal zo
2032
silent! normal zo
2108
silent! normal zo
2121
silent! normal zo
2129
silent! normal zo
2173
silent! normal zo
2190
silent! normal zo
2193
silent! normal zo
2194
silent! normal zo
2195
silent! normal zo
2200
silent! normal zo
2202
silent! normal zo
2203
silent! normal zo
2211
silent! normal zo
2324
silent! normal zo
2362
silent! normal zo
2373
silent! normal zo
2383
silent! normal zo
2394
silent! normal zo
2435
silent! normal zo
2443
silent! normal zo
2452
silent! normal zo
2457
silent! normal zo
2470
silent! normal zo
2489
silent! normal zo
2506
silent! normal zo
2515
silent! normal zo
2575
silent! normal zo
2575
silent! normal zo
2575
silent! normal zo
2575
silent! normal zo
2576
silent! normal zo
2580
silent! normal zo
2607
silent! normal zo
2612
silent! normal zo
2614
silent! normal zo
2615
silent! normal zo
2647
silent! normal zo
2661
silent! normal zo
2661
silent! normal zo
2661
silent! normal zo
2661
silent! normal zo
2661
silent! normal zo
2661
silent! normal zo
2661
silent! normal zo
2673
silent! normal zo
let s:l = 2704 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2704
normal! 039l
wincmd w
exe '1resize ' . ((&lines * 19 + 22) / 44)
exe '2resize ' . ((&lines * 14 + 22) / 44)
exe '3resize ' . ((&lines * 1 + 22) / 44)
exe '4resize ' . ((&lines * 1 + 22) / 44)
exe '5resize ' . ((&lines * 1 + 22) / 44)
exe '6resize ' . ((&lines * 1 + 22) / 44)
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
1wincmd w

" vim: ft=vim ro nowrap smc=128
