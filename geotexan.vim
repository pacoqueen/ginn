" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 18 septiembre 2015 at 12:31:06.
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
badd +3236 ginn/formularios/partes_de_fabricacion_balas.py
badd +1 fugitive:///home/bogado/Geotexan/src/Geotex-INN/.git//0/ginn/formularios/utils.py
badd +9 ginn/lib/fuzzywuzzy/fuzzywuzzy/utils.py
badd +1 formularios/auditviewer.py
badd +1 ginn/formularios/utils.py
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
badd +5820 ginn/informes/geninformes.py
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
badd +1 ginn/formularios/presupuestos.py
badd +1316 ginn/formularios/facturas_compra.py
badd +1 ginn/framework/pclases/__init__.py
argglobal
silent! argdel *
argadd formularios/auditviewer.py
set lines=52 columns=108
edit ginn/formularios/utils.py
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
4wincmd k
wincmd w
wincmd w
wincmd w
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
exe 'vert 1resize ' . ((&columns * 23 + 54) / 108)
exe '2resize ' . ((&lines * 6 + 26) / 52)
exe 'vert 2resize ' . ((&columns * 84 + 54) / 108)
exe '3resize ' . ((&lines * 33 + 26) / 52)
exe 'vert 3resize ' . ((&columns * 84 + 54) / 108)
exe '4resize ' . ((&lines * 1 + 26) / 52)
exe 'vert 4resize ' . ((&columns * 84 + 54) / 108)
exe '5resize ' . ((&lines * 1 + 26) / 52)
exe 'vert 5resize ' . ((&columns * 84 + 54) / 108)
exe '6resize ' . ((&lines * 5 + 26) / 52)
exe 'vert 6resize ' . ((&columns * 84 + 54) / 108)
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
507
normal! zo
507
normal! zo
507
normal! zo
689
normal! zo
689
normal! zo
689
normal! zo
689
normal! zo
689
normal! zo
1196
normal! zo
1214
normal! zo
1257
normal! zo
1271
normal! zo
let s:l = 1273 - ((1 * winheight(0) + 3) / 6)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1273
normal! 0260|
lcd ~/Geotexan/src/Geotex-INN
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
77
normal! zo
78
normal! zo
86
normal! zo
86
normal! zo
86
normal! zo
86
normal! zo
170
normal! zo
170
normal! zo
170
normal! zo
481
normal! zo
857
normal! zo
876
normal! zo
949
normal! zo
968
normal! zo
1063
normal! zo
1102
normal! zo
1108
normal! zo
1109
normal! zo
1352
normal! zo
1359
normal! zo
1361
normal! zo
1419
normal! zo
1425
normal! zo
1426
normal! zo
1426
normal! zo
1426
normal! zo
1426
normal! zo
1426
normal! zo
1430
normal! zo
1439
normal! zo
1455
normal! zo
1602
normal! zo
1702
normal! zo
1790
normal! zo
1794
normal! zo
1797
normal! zo
1803
normal! zo
1814
normal! zo
1821
normal! zo
1860
normal! zo
1929
normal! zo
1940
normal! zo
1943
normal! zo
1961
normal! zo
1972
normal! zo
2009
normal! zo
2053
normal! zo
2057
normal! zo
2061
normal! zo
2070
normal! zo
2209
normal! zo
2284
normal! zo
2287
normal! zo
2340
normal! zo
2363
normal! zo
2389
normal! zo
2420
normal! zo
2429
normal! zo
2429
normal! zo
2576
normal! zo
2596
normal! zo
2597
normal! zo
2606
normal! zo
2610
normal! zo
2656
normal! zo
2700
normal! zo
2712
normal! zo
2713
normal! zo
2719
normal! zo
2720
normal! zo
2725
normal! zo
2726
normal! zo
2731
normal! zo
2732
normal! zo
2737
normal! zo
2740
normal! zo
2741
normal! zo
2819
normal! zo
2960
normal! zo
2977
normal! zo
2979
normal! zo
let s:l = 1436 - ((16 * winheight(0) + 16) / 33)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1436
normal! 068|
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
let s:l = 20861 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
20861
normal! 0
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
let s:l = 16 - ((0 * winheight(0) + 2) / 5)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
16
normal! 03|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
3wincmd w
exe 'vert 1resize ' . ((&columns * 23 + 54) / 108)
exe '2resize ' . ((&lines * 6 + 26) / 52)
exe 'vert 2resize ' . ((&columns * 84 + 54) / 108)
exe '3resize ' . ((&lines * 33 + 26) / 52)
exe 'vert 3resize ' . ((&columns * 84 + 54) / 108)
exe '4resize ' . ((&lines * 1 + 26) / 52)
exe 'vert 4resize ' . ((&columns * 84 + 54) / 108)
exe '5resize ' . ((&lines * 1 + 26) / 52)
exe 'vert 5resize ' . ((&columns * 84 + 54) / 108)
exe '6resize ' . ((&lines * 5 + 26) / 52)
exe 'vert 6resize ' . ((&columns * 84 + 54) / 108)
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
3wincmd w

" vim: ft=vim ro nowrap smc=128
