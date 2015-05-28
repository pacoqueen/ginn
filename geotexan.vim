" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 28 mayo 2015 at 17:15:08.
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
badd +1 ginn/framework/pclases/__init__.py
badd +1406 ginn/formularios/partes_de_fabricacion_balas.py
badd +1 ginn/formularios/facturas_compra.py
badd +1 fugitive:///home/bogado/Geotexan/src/Geotex-INN/.git//0/ginn/formularios/utils.py
badd +9 ginn/lib/fuzzywuzzy/fuzzywuzzy/utils.py
badd +1 formularios/auditviewer.py
badd +2621 ginn/formularios/utils.py
badd +38 ginn/informes/treeview2pdf.py
badd +138 ginn/formularios/listado_rollos.py
badd +2 ginn/lib/fuzzywuzzy/fuzzywuzzy/__init__.py
badd +1 ginn/formularios/consulta_ventas.py
badd +185 ginn/formularios/consulta_partes_de_visita.py
badd +367 ginn/formularios/productos_compra.py
badd +630 ginn/formularios/partes_de_visita.py
badd +902 ginn/formularios/productos_de_venta_rollos.py
badd +357 ginn/formularios/proveedores.py
badd +79 ginn/framework/pclases/cliente.py
badd +914 ginn/formularios/ventana.py
badd +17 ginn/formularios/custom_widgets/cellrendererautocomplete.py
badd +1 ginn/formularios/consulta_saldo_proveedores.py
badd +1 ginn/lib/charting.py
badd +1 ginn/formularios/partes_de_fabricacion_rollos.py
badd +1253 ginn/informes/geninformes.py
badd +72 ginn/formularios/consulta_existenciasRollos.py
badd +0 ginn/formularios/clientes.py
argglobal
silent! argdel *
argadd formularios/auditviewer.py
set lines=48 columns=117
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
7wincmd k
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
exe 'vert 1resize ' . ((&columns * 31 + 58) / 117)
exe '2resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 85 + 58) / 117)
exe '3resize ' . ((&lines * 32 + 24) / 48)
exe 'vert 3resize ' . ((&columns * 85 + 58) / 117)
exe '4resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 4resize ' . ((&columns * 85 + 58) / 117)
exe '5resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 5resize ' . ((&columns * 85 + 58) / 117)
exe '6resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 6resize ' . ((&columns * 85 + 58) / 117)
exe '7resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 7resize ' . ((&columns * 85 + 58) / 117)
exe '8resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 8resize ' . ((&columns * 85 + 58) / 117)
exe '9resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 9resize ' . ((&columns * 85 + 58) / 117)
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
let s:l = 20947 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
20947
normal! 05|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/clientes.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
67
normal! zo
2129
normal! zo
2134
normal! zo
2135
normal! zo
2139
normal! zo
2144
normal! zo
2155
normal! zo
2156
normal! zo
let s:l = 2141 - ((10 * winheight(0) + 16) / 32)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2141
normal! 021|
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
522
normal! zo
531
normal! zo
536
normal! zo
538
normal! zo
560
normal! zo
563
normal! zo
563
normal! zo
563
normal! zo
1215
normal! zo
1221
normal! zo
1666
normal! zo
1673
normal! zo
1683
normal! zo
1708
normal! zo
1715
normal! zo
1726
normal! zo
1895
normal! zo
2282
normal! zo
2303
normal! zo
4240
normal! zo
let s:l = 528 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
528
normal! 038|
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
16931
normal! zo
16956
normal! zo
18003
normal! zo
18022
normal! zo
18035
normal! zo
18036
normal! zo
18038
normal! zo
18044
normal! zo
let s:l = 16953 - ((3 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
16953
normal! 044|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/lib/charting.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 103 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
103
normal! 0
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/partes_de_visita.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
61
normal! zo
62
normal! zo
213
normal! zo
221
normal! zo
221
normal! zo
221
normal! zo
221
normal! zo
221
normal! zo
223
normal! zo
244
normal! zo
263
normal! zo
267
normal! zo
267
normal! zo
267
normal! zo
267
normal! zo
267
normal! zo
281
normal! zo
281
normal! zo
281
normal! zo
283
normal! zo
288
normal! zo
292
normal! zo
292
normal! zo
292
normal! zo
292
normal! zo
292
normal! zo
292
normal! zc
297
normal! zo
298
normal! zo
302
normal! zo
306
normal! zo
306
normal! zo
306
normal! zo
306
normal! zo
306
normal! zo
311
normal! zo
316
normal! zo
323
normal! zo
323
normal! zo
340
normal! zo
390
normal! zo
390
normal! zo
390
normal! zo
390
normal! zo
390
normal! zo
390
normal! zo
411
normal! zo
412
normal! zo
461
normal! zo
462
normal! zo
464
normal! zo
471
normal! zo
473
normal! zo
474
normal! zo
474
normal! zo
474
normal! zo
477
normal! zo
483
normal! zo
483
normal! zo
483
normal! zo
483
normal! zo
483
normal! zo
486
normal! zo
495
normal! zo
541
normal! zo
553
normal! zo
568
normal! zo
577
normal! zo
582
normal! zo
596
normal! zo
597
normal! zo
610
normal! zo
617
normal! zo
617
normal! zo
617
normal! zo
617
normal! zo
617
normal! zo
632
normal! zo
639
normal! zo
641
normal! zo
665
normal! zo
684
normal! zo
688
normal! zo
721
normal! zo
727
normal! zo
727
normal! zo
727
normal! zo
727
normal! zo
727
normal! zo
731
normal! zo
734
normal! zo
734
normal! zo
let s:l = 464 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
464
normal! 041|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/consulta_partes_de_visita.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
56
normal! zo
61
normal! zo
83
normal! zo
84
normal! zo
88
normal! zo
96
normal! zo
96
normal! zo
96
normal! zo
96
normal! zo
101
normal! zo
107
normal! zo
109
normal! zo
109
normal! zo
140
normal! zo
150
normal! zo
150
normal! zo
150
normal! zo
150
normal! zo
150
normal! zo
150
normal! zo
150
normal! zo
150
normal! zo
150
normal! zo
150
normal! zo
150
normal! zo
156
normal! zo
172
normal! zo
173
normal! zo
173
normal! zo
185
normal! zo
186
normal! zo
186
normal! zo
186
normal! zo
186
normal! zo
186
normal! zo
186
normal! zo
186
normal! zo
186
normal! zo
188
normal! zo
188
normal! zo
196
normal! zo
196
normal! zo
196
normal! zo
196
normal! zo
196
normal! zo
196
normal! zo
196
normal! zo
205
normal! zo
207
normal! zo
210
normal! zo
218
normal! zo
224
normal! zo
224
normal! zo
229
normal! zo
242
normal! zo
270
normal! zo
273
normal! zo
279
normal! zo
291
normal! zo
291
normal! zo
291
normal! zo
291
normal! zo
let s:l = 139 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
139
normal! 09|
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
let s:l = 4 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
4
normal! 03|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
3wincmd w
exe 'vert 1resize ' . ((&columns * 31 + 58) / 117)
exe '2resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 85 + 58) / 117)
exe '3resize ' . ((&lines * 32 + 24) / 48)
exe 'vert 3resize ' . ((&columns * 85 + 58) / 117)
exe '4resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 4resize ' . ((&columns * 85 + 58) / 117)
exe '5resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 5resize ' . ((&columns * 85 + 58) / 117)
exe '6resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 6resize ' . ((&columns * 85 + 58) / 117)
exe '7resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 7resize ' . ((&columns * 85 + 58) / 117)
exe '8resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 8resize ' . ((&columns * 85 + 58) / 117)
exe '9resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 9resize ' . ((&columns * 85 + 58) / 117)
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
