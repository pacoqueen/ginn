" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 10 septiembre 2015 at 17:31:14.
" Open this file in Vim and run :source % to restore your session.

set guioptions=aegimrLtT
silent! set guifont=Monaco\ for\ Powerline\ 10
if exists('g:syntax_on') != 1 | syntax on | endif
if exists('g:did_load_filetypes') != 1 | filetype on | endif
if exists('g:did_load_ftplugin') != 1 | filetype plugin on | endif
if exists('g:did_indent_on') != 1 | filetype indent on | endif
if &background != 'dark'
	set background=dark
endif
if !exists('g:colors_name') || g:colors_name != 'vividchalk' | colorscheme vividchalk | endif
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
badd +1 ginn/formularios/partes_de_ancho_multiple.py
badd +4174 ginn/formularios/partes_de_fabricacion_balas.py
badd +1 fugitive:///home/bogado/Geotexan/src/Geotex-INN/.git//0/ginn/formularios/utils.py
badd +9 ginn/lib/fuzzywuzzy/fuzzywuzzy/utils.py
badd +1 formularios/auditviewer.py
badd +2185 ginn/formularios/utils.py
badd +38 ginn/informes/treeview2pdf.py
badd +138 ginn/formularios/listado_rollos.py
badd +2 ginn/lib/fuzzywuzzy/fuzzywuzzy/__init__.py
badd +706 ginn/formularios/consulta_ventas.py
badd +367 ginn/formularios/productos_compra.py
badd +902 ginn/formularios/productos_de_venta_rollos.py
badd +357 ginn/formularios/proveedores.py
badd +517 ginn/framework/pclases/cliente.py
badd +914 ginn/formularios/ventana.py
badd +17 ginn/formularios/custom_widgets/cellrendererautocomplete.py
badd +1 ginn/formularios/consulta_saldo_proveedores.py
badd +123 ginn/lib/charting.py
badd +1864 ginn/formularios/partes_de_fabricacion_rollos.py
badd +72 ginn/formularios/consulta_existenciasRollos.py
badd +17 ginn/formularios/consulta_existenciasBalas.py
badd +10434 ginn/informes/geninformes.py
badd +452 db/tablas.sql
badd +1 ginn/framework/__init__.py
badd +3136 ginn/formularios/facturas_venta.py
badd +10 ginn/informes/alians_trade.py
badd +52 ginn/informes/barcode/EANBarCode.py
badd +63 ginn/informes/barcode/_barcode.py
badd +227 ginn/informes/barcode/common.py
badd +53 ginn/informes/presupuesto.py
badd +1156 ginn/formularios/abonos_venta.py
badd +3507 ginn/formularios/albaranes_de_salida.py
badd +19 ginn/formularios/consulta_ofertas.py
badd +1134 ginn/formularios/pagares_pagos.py
badd +0 ginn/formularios/pedidos_de_compra.py
argglobal
silent! argdel *
argadd formularios/auditviewer.py
set lines=48 columns=111
edit ginn/informes/geninformes.py
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
3wincmd k
wincmd w
wincmd w
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
exe 'vert 1resize ' . ((&columns * 24 + 55) / 111)
exe '2resize ' . ((&lines * 25 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 86 + 55) / 111)
exe '3resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 3resize ' . ((&columns * 86 + 55) / 111)
exe '4resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 4resize ' . ((&columns * 86 + 55) / 111)
exe '5resize ' . ((&lines * 16 + 24) / 48)
exe 'vert 5resize ' . ((&columns * 86 + 55) / 111)
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
83
normal! zo
84
normal! zo
85
normal! zo
85
normal! zo
85
normal! zo
87
normal! zo
88
normal! zo
88
normal! zo
88
normal! zo
120
normal! zo
138
normal! zo
239
normal! zo
253
normal! zo
260
normal! zo
260
normal! zo
261
normal! zo
279
normal! zo
279
normal! zo
279
normal! zo
279
normal! zo
279
normal! zo
279
normal! zo
283
normal! zo
294
normal! zo
294
normal! zo
294
normal! zo
294
normal! zo
294
normal! zo
294
normal! zo
294
normal! zo
294
normal! zo
300
normal! zo
300
normal! zo
303
normal! zo
310
normal! zo
310
normal! zo
310
normal! zo
310
normal! zo
310
normal! zo
310
normal! zo
310
normal! zo
310
normal! zo
310
normal! zo
310
normal! zo
313
normal! zo
313
normal! zo
314
normal! zo
314
normal! zo
314
normal! zo
314
normal! zo
314
normal! zo
314
normal! zo
318
normal! zo
329
normal! zo
329
normal! zo
329
normal! zo
329
normal! zo
329
normal! zo
329
normal! zo
329
normal! zo
329
normal! zo
335
normal! zo
335
normal! zo
338
normal! zo
347
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
352
normal! zo
361
normal! zo
361
normal! zo
367
normal! zo
380
normal! zo
380
normal! zo
380
normal! zo
388
normal! zo
388
normal! zo
388
normal! zo
391
normal! zo
391
normal! zo
391
normal! zo
391
normal! zo
395
normal! zo
399
normal! zo
400
normal! zo
401
normal! zo
406
normal! zo
407
normal! zo
408
normal! zo
414
normal! zo
414
normal! zo
414
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
425
normal! zo
426
normal! zo
426
normal! zo
433
normal! zo
434
normal! zo
434
normal! zo
442
normal! zo
442
normal! zo
442
normal! zo
458
normal! zo
486
normal! zo
1206
normal! zo
1305
normal! zo
1361
normal! zo
1396
normal! zo
1463
normal! zo
1544
normal! zo
1544
normal! zo
1577
normal! zo
1616
normal! zo
1718
normal! zo
1727
normal! zo
1729
normal! zo
1730
normal! zo
1730
normal! zo
1739
normal! zo
1742
normal! zo
1742
normal! zo
1769
normal! zo
2007
normal! zo
2104
normal! zo
2502
normal! zo
2549
normal! zo
2681
normal! zo
2854
normal! zo
2983
normal! zo
2983
normal! zo
3150
normal! zo
3150
normal! zo
3270
normal! zo
3301
normal! zo
3947
normal! zo
3947
normal! zo
4041
normal! zo
4059
normal! zo
4591
normal! zo
4673
normal! zo
4701
normal! zo
4701
normal! zo
4704
normal! zo
4704
normal! zo
4704
normal! zo
4704
normal! zo
4704
normal! zo
4704
normal! zo
4704
normal! zo
4704
normal! zo
4704
normal! zo
4704
normal! zo
4704
normal! zo
4738
normal! zo
4738
normal! zo
4740
normal! zo
4740
normal! zo
4756
normal! zo
4756
normal! zo
4758
normal! zo
4758
normal! zo
4777
normal! zo
4777
normal! zo
4777
normal! zo
4777
normal! zo
4777
normal! zo
4777
normal! zo
4777
normal! zo
4777
normal! zo
4816
normal! zo
4816
normal! zo
4840
normal! zo
4840
normal! zo
4840
normal! zo
4840
normal! zo
4840
normal! zo
4840
normal! zo
4840
normal! zo
4840
normal! zo
4842
normal! zo
4842
normal! zo
4842
normal! zo
4842
normal! zo
4842
normal! zo
4842
normal! zo
4842
normal! zo
4842
normal! zo
4847
normal! zo
4848
normal! zo
4848
normal! zo
4861
normal! zo
4863
normal! zo
4865
normal! zo
4867
normal! zo
4869
normal! zo
4887
normal! zo
4888
normal! zo
4892
normal! zo
4892
normal! zo
4892
normal! zo
4892
normal! zo
4892
normal! zo
4897
normal! zo
4897
normal! zo
4897
normal! zo
4897
normal! zo
4897
normal! zo
4897
normal! zo
4897
normal! zo
4897
normal! zo
4917
normal! zo
4920
normal! zo
4922
normal! zo
4922
normal! zo
4922
normal! zo
4922
normal! zo
4926
normal! zo
4926
normal! zo
4926
normal! zo
4935
normal! zo
4935
normal! zo
4944
normal! zo
4944
normal! zo
4944
normal! zo
4944
normal! zo
4950
normal! zo
4951
normal! zo
4951
normal! zo
4951
normal! zo
4953
normal! zo
4954
normal! zo
4954
normal! zo
4954
normal! zo
4958
normal! zo
4958
normal! zo
4958
normal! zo
4961
normal! zo
4963
normal! zo
4968
normal! zo
4968
normal! zo
4968
normal! zo
4974
normal! zo
4977
normal! zo
4977
normal! zo
4980
normal! zo
4986
normal! zo
4992
normal! zo
4998
normal! zo
5017
normal! zo
5017
normal! zo
5023
normal! zo
5024
normal! zo
5027
normal! zo
5028
normal! zo
5035
normal! zo
5038
normal! zo
5040
normal! zo
5046
normal! zo
5046
normal! zo
5048
normal! zo
5052
normal! zo
5060
normal! zo
5062
normal! zo
5062
normal! zo
5065
normal! zo
5065
normal! zo
5068
normal! zo
5068
normal! zo
5076
normal! zo
5081
normal! zo
5088
normal! zo
5088
normal! zo
5113
normal! zo
5117
normal! zo
5117
normal! zo
5117
normal! zo
5117
normal! zo
5117
normal! zo
5117
normal! zo
5117
normal! zo
5122
normal! zo
5122
normal! zo
5122
normal! zo
5122
normal! zo
5122
normal! zo
5122
normal! zo
5126
normal! zo
5126
normal! zo
5126
normal! zo
5126
normal! zo
5131
normal! zo
5131
normal! zo
5131
normal! zo
5131
normal! zo
5196
normal! zo
5209
normal! zo
5937
normal! zo
5953
normal! zo
6341
normal! zo
6547
normal! zo
6561
normal! zo
6727
normal! zo
6739
normal! zo
7212
normal! zo
7245
normal! zo
7245
normal! zo
7253
normal! zo
7253
normal! zo
7253
normal! zo
7253
normal! zo
7253
normal! zo
7253
normal! zo
7253
normal! zo
7253
normal! zo
7346
normal! zo
7391
normal! zo
7391
normal! zo
7391
normal! zo
7392
normal! zo
7392
normal! zo
7392
normal! zo
7400
normal! zo
7400
normal! zo
7400
normal! zo
7400
normal! zo
7400
normal! zo
7400
normal! zo
7400
normal! zo
7400
normal! zo
7427
normal! zo
7431
normal! zo
9135
normal! zo
9193
normal! zo
9241
normal! zo
9887
normal! zo
9893
normal! zo
9947
normal! zo
9956
normal! zo
9959
normal! zo
10016
normal! zo
10059
normal! zo
10072
normal! zo
10073
normal! zo
10073
normal! zo
10073
normal! zo
10125
normal! zo
10126
normal! zo
10126
normal! zo
10126
normal! zo
10259
normal! zo
10322
normal! zo
10447
normal! zo
10615
normal! zo
10621
normal! zo
11189
normal! zo
11819
normal! zo
12030
normal! zo
let s:l = 9147 - ((15 * winheight(0) + 12) / 25)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
9147
normal! 042|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/pedidos_de_compra.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
81
normal! zo
let s:l = 1264 - ((1 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1264
normal! 046|
lcd ~/Geotexan/src/Geotex-INN
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
187
normal! zo
235
normal! zo
369
normal! zo
619
normal! zo
635
normal! zo
667
normal! zo
1022
normal! zo
1027
normal! zo
1049
normal! zo
1054
normal! zo
1415
normal! zo
1428
normal! zo
1618
normal! zo
1754
normal! zo
1771
normal! zo
2148
normal! zo
2160
normal! zo
2168
normal! zo
2187
normal! zo
2211
normal! zo
2218
normal! zo
2258
normal! zo
2368
normal! zo
2393
normal! zo
2459
normal! zo
2477
normal! zo
2484
normal! zo
2825
normal! zo
2826
normal! zo
2962
normal! zo
2980
normal! zo
3011
normal! zo
3014
normal! zo
3015
normal! zo
3019
normal! zo
3043
normal! zo
3286
normal! zo
3298
normal! zo
3314
normal! zo
3322
normal! zo
3504
normal! zo
3504
normal! zo
3504
normal! zo
3524
normal! zo
3538
normal! zo
3548
normal! zo
3553
normal! zo
3560
normal! zo
3570
normal! zo
3590
normal! zo
3716
normal! zo
3724
normal! zo
3725
normal! zo
3794
normal! zo
3803
normal! zo
3803
normal! zo
3803
normal! zo
3810
normal! zo
3823
normal! zo
3841
normal! zo
3930
normal! zo
3966
normal! zo
let s:l = 1865 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1865
normal! 015|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/partes_de_ancho_multiple.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 16 - ((5 * winheight(0) + 8) / 16)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
16
normal! 03|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
2wincmd w
exe 'vert 1resize ' . ((&columns * 24 + 55) / 111)
exe '2resize ' . ((&lines * 25 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 86 + 55) / 111)
exe '3resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 3resize ' . ((&columns * 86 + 55) / 111)
exe '4resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 4resize ' . ((&columns * 86 + 55) / 111)
exe '5resize ' . ((&lines * 16 + 24) / 48)
exe 'vert 5resize ' . ((&columns * 86 + 55) / 111)
tabnext 1
if exists('s:wipebuf')
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=1 shortmess=aoO
let s:sx = expand("<sfile>:p:r")."x.vim"
if file_readable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &so = s:so_save | let &siso = s:siso_save
doautoall SessionLoadPost
unlet SessionLoad
tabnext 1
2wincmd w

" vim: ft=vim ro nowrap smc=128
