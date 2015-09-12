" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 12 septiembre 2015 at 11:51:05.
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
badd +14 ginn/formularios/consulta_existenciasBalas.py
badd +1 ginn/informes/geninformes.py
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
badd +1272 ginn/formularios/pedidos_de_compra.py
argglobal
silent! argdel *
argadd formularios/auditviewer.py
set lines=54 columns=111
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
exe '2resize ' . ((&lines * 22 + 27) / 54)
exe 'vert 2resize ' . ((&columns * 86 + 55) / 111)
exe '3resize ' . ((&lines * 25 + 27) / 54)
exe 'vert 3resize ' . ((&columns * 86 + 55) / 111)
exe '4resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 4resize ' . ((&columns * 86 + 55) / 111)
exe '5resize ' . ((&lines * 1 + 27) / 54)
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
73
normal! zo
73
normal! zo
73
normal! zo
73
normal! zo
73
normal! zo
86
normal! zo
89
normal! zo
90
normal! zo
91
normal! zo
91
normal! zo
107
normal! zo
125
normal! zo
125
normal! zo
226
normal! zo
240
normal! zo
247
normal! zo
247
normal! zo
248
normal! zo
266
normal! zo
266
normal! zo
266
normal! zo
266
normal! zo
266
normal! zo
266
normal! zo
270
normal! zo
281
normal! zo
281
normal! zo
281
normal! zo
281
normal! zo
281
normal! zo
281
normal! zo
281
normal! zo
281
normal! zo
287
normal! zo
287
normal! zo
290
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
297
normal! zo
297
normal! zo
297
normal! zo
300
normal! zo
300
normal! zo
301
normal! zo
301
normal! zo
301
normal! zo
301
normal! zo
301
normal! zo
301
normal! zo
305
normal! zo
316
normal! zo
316
normal! zo
316
normal! zo
316
normal! zo
316
normal! zo
316
normal! zo
316
normal! zo
316
normal! zo
322
normal! zo
322
normal! zo
325
normal! zo
334
normal! zo
334
normal! zo
335
normal! zo
335
normal! zo
335
normal! zo
335
normal! zo
335
normal! zo
335
normal! zo
339
normal! zo
348
normal! zo
348
normal! zo
354
normal! zo
367
normal! zo
367
normal! zo
367
normal! zo
375
normal! zo
375
normal! zo
375
normal! zo
378
normal! zo
378
normal! zo
378
normal! zo
378
normal! zo
382
normal! zo
386
normal! zo
387
normal! zo
388
normal! zo
393
normal! zo
394
normal! zo
395
normal! zo
401
normal! zo
401
normal! zo
401
normal! zo
404
normal! zo
404
normal! zo
404
normal! zo
404
normal! zo
408
normal! zo
412
normal! zo
413
normal! zo
413
normal! zo
420
normal! zo
421
normal! zo
421
normal! zo
429
normal! zo
429
normal! zo
429
normal! zo
445
normal! zo
464
normal! zo
464
normal! zo
464
normal! zo
464
normal! zo
464
normal! zo
464
normal! zo
464
normal! zo
464
normal! zo
477
normal! zo
1199
normal! zo
1298
normal! zo
1298
normal! zo
1298
normal! zo
1298
normal! zo
1298
normal! zo
1354
normal! zo
1392
normal! zo
1393
normal! zo
1462
normal! zo
1543
normal! zo
1543
normal! zo
1576
normal! zo
1615
normal! zo
1615
normal! zo
1717
normal! zo
1726
normal! zo
1728
normal! zo
1729
normal! zo
1729
normal! zo
1738
normal! zo
1741
normal! zo
1741
normal! zo
1768
normal! zo
2006
normal! zo
2006
normal! zo
2006
normal! zo
2006
normal! zo
2103
normal! zo
2501
normal! zo
2548
normal! zo
2680
normal! zo
2680
normal! zo
2680
normal! zo
2853
normal! zo
2982
normal! zo
2982
normal! zo
3149
normal! zo
3149
normal! zo
3269
normal! zo
3300
normal! zo
3946
normal! zo
3946
normal! zo
4040
normal! zo
4058
normal! zo
4590
normal! zo
4672
normal! zo
4700
normal! zo
4700
normal! zo
4703
normal! zo
4703
normal! zo
4703
normal! zo
4703
normal! zo
4703
normal! zo
4703
normal! zo
4703
normal! zo
4703
normal! zo
4703
normal! zo
4703
normal! zo
4703
normal! zo
4737
normal! zo
4737
normal! zo
4739
normal! zo
4739
normal! zo
4755
normal! zo
4755
normal! zo
4757
normal! zo
4757
normal! zo
4776
normal! zo
4776
normal! zo
4776
normal! zo
4776
normal! zo
4776
normal! zo
4776
normal! zo
4776
normal! zo
4776
normal! zo
4815
normal! zo
4815
normal! zo
4839
normal! zo
4839
normal! zo
4839
normal! zo
4839
normal! zo
4839
normal! zo
4839
normal! zo
4839
normal! zo
4839
normal! zo
4841
normal! zo
4841
normal! zo
4841
normal! zo
4841
normal! zo
4841
normal! zo
4841
normal! zo
4841
normal! zo
4841
normal! zo
4846
normal! zo
4847
normal! zo
4847
normal! zo
4860
normal! zo
4862
normal! zo
4864
normal! zo
4866
normal! zo
4868
normal! zo
4886
normal! zo
4887
normal! zo
4891
normal! zo
4891
normal! zo
4891
normal! zo
4891
normal! zo
4891
normal! zo
4896
normal! zo
4896
normal! zo
4896
normal! zo
4896
normal! zo
4896
normal! zo
4896
normal! zo
4896
normal! zo
4896
normal! zo
4916
normal! zo
4919
normal! zo
4921
normal! zo
4921
normal! zo
4921
normal! zo
4921
normal! zo
4925
normal! zo
4925
normal! zo
4925
normal! zo
4934
normal! zo
4934
normal! zo
4943
normal! zo
4943
normal! zo
4943
normal! zo
4943
normal! zo
4949
normal! zo
4950
normal! zo
4950
normal! zo
4950
normal! zo
4952
normal! zo
4953
normal! zo
4953
normal! zo
4953
normal! zo
4957
normal! zo
4957
normal! zo
4957
normal! zo
4960
normal! zo
4962
normal! zo
4967
normal! zo
4967
normal! zo
4967
normal! zo
4973
normal! zo
4976
normal! zo
4976
normal! zo
4979
normal! zo
4985
normal! zo
4991
normal! zo
4997
normal! zo
5016
normal! zo
5016
normal! zo
5022
normal! zo
5023
normal! zo
5026
normal! zo
5027
normal! zo
5034
normal! zo
5037
normal! zo
5039
normal! zo
5045
normal! zo
5045
normal! zo
5047
normal! zo
5051
normal! zo
5059
normal! zo
5061
normal! zo
5061
normal! zo
5064
normal! zo
5064
normal! zo
5067
normal! zo
5067
normal! zo
5075
normal! zo
5080
normal! zo
5087
normal! zo
5087
normal! zo
5112
normal! zo
5116
normal! zo
5116
normal! zo
5116
normal! zo
5116
normal! zo
5116
normal! zo
5116
normal! zo
5116
normal! zo
5121
normal! zo
5121
normal! zo
5121
normal! zo
5121
normal! zo
5121
normal! zo
5121
normal! zo
5125
normal! zo
5125
normal! zo
5125
normal! zo
5125
normal! zo
5130
normal! zo
5130
normal! zo
5130
normal! zo
5130
normal! zo
5195
normal! zo
5208
normal! zo
5936
normal! zo
5952
normal! zo
6340
normal! zo
6340
normal! zo
6411
normal! zo
6498
normal! zo
6504
normal! zo
6504
normal! zo
6504
normal! zo
6504
normal! zo
6504
normal! zo
6504
normal! zo
6507
normal! zo
6514
normal! zo
6550
normal! zo
6551
normal! zo
6564
normal! zo
6600
normal! zo
6602
normal! zo
6656
normal! zo
6675
normal! zo
6683
normal! zo
6695
normal! zo
6704
normal! zo
6737
normal! zo
6737
normal! zo
6737
normal! zo
6737
normal! zo
6749
normal! zo
6827
normal! zo
6910
normal! zo
6922
normal! zo
7222
normal! zo
7255
normal! zo
7255
normal! zo
7263
normal! zo
7263
normal! zo
7263
normal! zo
7263
normal! zo
7263
normal! zo
7263
normal! zo
7263
normal! zo
7263
normal! zo
7356
normal! zo
7401
normal! zo
7401
normal! zo
7401
normal! zo
7402
normal! zo
7402
normal! zo
7402
normal! zo
7410
normal! zo
7410
normal! zo
7410
normal! zo
7410
normal! zo
7410
normal! zo
7410
normal! zo
7410
normal! zo
7410
normal! zo
7437
normal! zo
7441
normal! zo
9145
normal! zo
9206
normal! zo
9254
normal! zo
9675
normal! zo
9692
normal! zo
9729
normal! zo
9740
normal! zo
9900
normal! zo
9906
normal! zo
9960
normal! zo
9969
normal! zo
9972
normal! zo
10029
normal! zo
10072
normal! zo
10085
normal! zo
10086
normal! zo
10086
normal! zo
10086
normal! zo
10138
normal! zo
10139
normal! zo
10139
normal! zo
10272
normal! zo
10272
normal! zo
10272
normal! zo
10272
normal! zo
10335
normal! zo
10335
normal! zo
10335
normal! zo
10335
normal! zo
10335
normal! zo
10460
normal! zo
10628
normal! zo
10634
normal! zo
10852
normal! zo
10906
normal! zo
10924
normal! zo
10935
normal! zo
11020
normal! zo
11202
normal! zo
11832
normal! zo
12043
normal! zo
let s:l = 5820 - ((6 * winheight(0) + 11) / 22)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
5820
normal! 05|
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
111
normal! zo
let s:l = 3241 - ((16 * winheight(0) + 12) / 25)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3241
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
let s:l = 16 - ((4 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
16
normal! 03|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
2wincmd w
exe 'vert 1resize ' . ((&columns * 24 + 55) / 111)
exe '2resize ' . ((&lines * 22 + 27) / 54)
exe 'vert 2resize ' . ((&columns * 86 + 55) / 111)
exe '3resize ' . ((&lines * 25 + 27) / 54)
exe 'vert 3resize ' . ((&columns * 86 + 55) / 111)
exe '4resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 4resize ' . ((&columns * 86 + 55) / 111)
exe '5resize ' . ((&lines * 1 + 27) / 54)
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
