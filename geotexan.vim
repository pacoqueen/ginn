" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 04 diciembre 2015 at 14:38:28.
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
badd +16 ginn/formularios/partes_de_ancho_multiple.py
badd +4159 ginn/formularios/partes_de_fabricacion_balas.py
badd +1 fugitive:///home/bogado/Geotexan/src/Geotex-INN/.git//0/ginn/formularios/utils.py
badd +9 ginn/lib/fuzzywuzzy/fuzzywuzzy/utils.py
badd +1 formularios/auditviewer.py
badd +4608 ginn/formularios/utils.py
badd +38 ginn/informes/treeview2pdf.py
badd +138 ginn/formularios/listado_rollos.py
badd +2 ginn/lib/fuzzywuzzy/fuzzywuzzy/__init__.py
badd +706 ginn/formularios/consulta_ventas.py
badd +367 ginn/formularios/productos_compra.py
badd +902 ginn/formularios/productos_de_venta_rollos.py
badd +552 ginn/formularios/proveedores.py
badd +517 ginn/framework/pclases/cliente.py
badd +914 ginn/formularios/ventana.py
badd +17 ginn/formularios/custom_widgets/cellrendererautocomplete.py
badd +1 ginn/formularios/consulta_saldo_proveedores.py
badd +123 ginn/lib/charting.py
badd +1868 ginn/formularios/partes_de_fabricacion_rollos.py
badd +72 ginn/formularios/consulta_existenciasRollos.py
badd +14 ginn/formularios/consulta_existenciasBalas.py
badd +5011 ginn/informes/geninformes.py
badd +452 db/tablas.sql
badd +1 ginn/framework/__init__.py
badd +3136 ginn/formularios/facturas_venta.py
badd +10 ginn/informes/alians_trade.py
badd +52 ginn/informes/barcode/EANBarCode.py
badd +63 ginn/informes/barcode/_barcode.py
badd +227 ginn/informes/barcode/common.py
badd +53 ginn/informes/presupuesto.py
badd +1205 ginn/formularios/abonos_venta.py
badd +3507 ginn/formularios/albaranes_de_salida.py
badd +19 ginn/formularios/consulta_ofertas.py
badd +1134 ginn/formularios/pagares_pagos.py
badd +1272 ginn/formularios/pedidos_de_compra.py
badd +3667 ginn/formularios/presupuestos.py
badd +1316 ginn/formularios/facturas_compra.py
badd +20861 ginn/framework/pclases/__init__.py
badd +37 ginn/api/murano/connection.py
badd +1 ginn/api/murano/__init__.py
badd +466 ginn/api/murano/ops.py
badd +175 ginn/formularios/mail_sender.py
badd +42 ginn/informes/presupuesto2.py
badd +1 ginn/lib/xlutils/jenkins
badd +12 ginn/api/tests/murano_tests.py
argglobal
silent! argdel *
argadd formularios/auditviewer.py
set lines=48 columns=107
edit ginn/api/murano/ops.py
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
exe 'vert 1resize ' . ((&columns * 23 + 53) / 107)
exe '2resize ' . ((&lines * 14 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 83 + 53) / 107)
exe '3resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 3resize ' . ((&columns * 83 + 53) / 107)
exe '4resize ' . ((&lines * 27 + 24) / 48)
exe 'vert 4resize ' . ((&columns * 83 + 53) / 107)
exe '5resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 5resize ' . ((&columns * 83 + 53) / 107)
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
23
normal! zo
23
normal! zo
108
normal! zo
108
normal! zo
108
normal! zo
170
normal! zo
180
normal! zo
188
normal! zo
197
normal! zo
205
normal! zo
211
normal! zo
214
normal! zo
214
normal! zo
214
normal! zo
214
normal! zo
214
normal! zo
214
normal! zo
219
normal! zo
227
normal! zo
236
normal! zo
247
normal! zo
262
normal! zo
271
normal! zo
277
normal! zo
284
normal! zo
288
normal! zo
293
normal! zo
300
normal! zo
305
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
306
normal! zo
312
normal! zo
341
normal! zo
342
normal! zo
347
normal! zo
362
normal! zo
367
normal! zo
367
normal! zo
367
normal! zo
367
normal! zo
378
normal! zo
378
normal! zo
378
normal! zo
378
normal! zo
378
normal! zo
378
normal! zo
391
normal! zo
402
normal! zo
407
normal! zo
407
normal! zo
407
normal! zo
407
normal! zo
418
normal! zo
418
normal! zo
418
normal! zo
418
normal! zo
418
normal! zo
418
normal! zo
431
normal! zo
445
normal! zo
450
normal! zo
450
normal! zo
450
normal! zo
450
normal! zo
461
normal! zo
461
normal! zo
461
normal! zo
461
normal! zo
461
normal! zo
461
normal! zo
475
normal! zo
486
normal! zo
491
normal! zo
491
normal! zo
491
normal! zo
491
normal! zo
502
normal! zo
502
normal! zo
502
normal! zo
502
normal! zo
502
normal! zo
502
normal! zo
516
normal! zo
529
normal! zo
551
normal! zo
584
normal! zo
593
normal! zo
612
normal! zo
613
normal! zo
613
normal! zo
613
normal! zo
623
normal! zo
660
normal! zo
660
normal! zo
660
normal! zo
660
normal! zo
678
normal! zo
686
normal! zo
691
normal! zo
692
normal! zo
695
normal! zo
696
normal! zo
696
normal! zo
696
normal! zo
700
normal! zo
705
normal! zo
711
normal! zo
711
normal! zo
711
normal! zo
711
normal! zo
719
normal! zo
719
normal! zo
719
normal! zo
719
normal! zo
719
normal! zo
719
normal! zo
let s:l = 677 - ((7 * winheight(0) + 7) / 14)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
677
normal! 0
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/api/murano/connection.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
12
normal! zo
13
normal! zo
17
normal! zo
23
normal! zo
29
normal! zo
29
normal! zo
39
normal! zo
42
normal! zo
45
normal! zo
49
normal! zo
50
normal! zo
50
normal! zo
51
normal! zo
56
normal! zo
57
normal! zo
57
normal! zo
57
normal! zo
57
normal! zo
59
normal! zo
60
normal! zo
60
normal! zo
60
normal! zo
60
normal! zo
71
normal! zo
81
normal! zo
90
normal! zo
93
normal! zo
96
normal! zo
97
normal! zo
98
normal! zo
99
normal! zo
102
normal! zo
108
normal! zo
114
normal! zo
let s:l = 108 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
108
normal! 035|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/api/murano/__init__.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 46 - ((14 * winheight(0) + 13) / 27)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
46
normal! 071|
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
7784
normal! zo
7802
normal! zo
7807
normal! zo
7809
normal! zo
7810
normal! zo
7811
normal! zo
7851
normal! zo
8663
normal! zo
8666
normal! zo
11598
normal! zo
16530
normal! zo
16619
normal! zo
16971
normal! zo
17028
normal! zo
17737
normal! zo
17757
normal! zo
17758
normal! zo
17758
normal! zo
17758
normal! zo
17758
normal! zo
17758
normal! zo
17954
normal! zo
18494
normal! zo
18551
normal! zo
19336
normal! zo
19343
normal! zo
21582
normal! zo
21606
normal! zo
let s:l = 17320 - ((1 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
17320
normal! 05|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
4wincmd w
exe 'vert 1resize ' . ((&columns * 23 + 53) / 107)
exe '2resize ' . ((&lines * 14 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 83 + 53) / 107)
exe '3resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 3resize ' . ((&columns * 83 + 53) / 107)
exe '4resize ' . ((&lines * 27 + 24) / 48)
exe 'vert 4resize ' . ((&columns * 83 + 53) / 107)
exe '5resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 5resize ' . ((&columns * 83 + 53) / 107)
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
4wincmd w

" vim: ft=vim ro nowrap smc=128
