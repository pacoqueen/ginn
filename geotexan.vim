" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 03 julio 2015 at 14:00:59.
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
badd +21376 ginn/framework/pclases/__init__.py
badd +4174 ginn/formularios/partes_de_fabricacion_balas.py
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
badd +902 ginn/formularios/productos_de_venta_rollos.py
badd +357 ginn/formularios/proveedores.py
badd +517 ginn/framework/pclases/cliente.py
badd +914 ginn/formularios/ventana.py
badd +17 ginn/formularios/custom_widgets/cellrendererautocomplete.py
badd +1 ginn/formularios/consulta_saldo_proveedores.py
badd +123 ginn/lib/charting.py
badd +192 ginn/formularios/partes_de_fabricacion_rollos.py
badd +72 ginn/formularios/consulta_existenciasRollos.py
badd +259 ginn/formularios/clientes.py
badd +17 ginn/formularios/consulta_existenciasBalas.py
badd +6783 ginn/informes/geninformes.py
badd +452 db/tablas.sql
badd +1 ginn/framework/__init__.py
badd +2682 ginn/formularios/facturas_venta.py
badd +1084 ginn/framework/pclases/superfacturaventa.py
argglobal
silent! argdel *
argadd formularios/auditviewer.py
set lines=48 columns=113
edit ginn/formularios/partes_de_fabricacion_rollos.py
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
exe 'vert 1resize ' . ((&columns * 28 + 56) / 113)
exe '2resize ' . ((&lines * 16 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 84 + 56) / 113)
exe '3resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 3resize ' . ((&columns * 84 + 56) / 113)
exe '4resize ' . ((&lines * 23 + 24) / 48)
exe 'vert 4resize ' . ((&columns * 84 + 56) / 113)
exe '5resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 5resize ' . ((&columns * 84 + 56) / 113)
exe '6resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 6resize ' . ((&columns * 84 + 56) / 113)
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
let s:l = 1809 - ((8 * winheight(0) + 8) / 16)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1809
normal! 054|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/facturas_compra.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
79
normal! zo
1043
normal! zo
let s:l = 882 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
882
normal! 038|
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
1537
normal! zo
1697
normal! zo
1710
normal! zo
1711
normal! zo
1979
normal! zo
2103
normal! zo
let s:l = 2118 - ((15 * winheight(0) + 11) / 23)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2118
normal! 017|
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
let s:l = 150 - ((1 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
150
normal! 050|
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
let s:l = 10 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
10
normal! 041|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
2wincmd w
exe 'vert 1resize ' . ((&columns * 28 + 56) / 113)
exe '2resize ' . ((&lines * 16 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 84 + 56) / 113)
exe '3resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 3resize ' . ((&columns * 84 + 56) / 113)
exe '4resize ' . ((&lines * 23 + 24) / 48)
exe 'vert 4resize ' . ((&columns * 84 + 56) / 113)
exe '5resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 5resize ' . ((&columns * 84 + 56) / 113)
exe '6resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 6resize ' . ((&columns * 84 + 56) / 113)
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
