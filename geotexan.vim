" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 10 junio 2014 at 08:17:25.
" Open this file in Vim and run :source % to restore your session.

set guioptions=aegimrLtT
silent! set guifont=Source\ Code\ Pro\ 9
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
badd +1 extra/scripts/balas_basura_reembaladas.py
badd +19 ginn/informes/nied.py
badd +129 ginn/informes/ekotex.py
badd +1 formularios/auditviewer.py
badd +248 ginn/formularios/gtkexcepthook.py
badd +133 ginn/formularios/partes_de_fabricacion_bolsas.py
badd +1 ginn/formularios/partes_de_fabricacion_gtx.py
badd +1 ginn/formularios/partes_de_ancho_multiple.py
badd +1 ginn/formularios/consulta_producido.py
badd +247 ginn/formularios/consulta_consumo.py
badd +41 ginn/framework/memoize.py
badd +596 ginn/formularios/presupuesto.py
badd +47 ginn/formularios/consulta_productividad.py
badd +590 ginn/formularios/listado_rollos.py
badd +3049 ginn/informes/geninformes.py
badd +402 ginn/informes/norma2013.py
badd +99 ginn/formularios/consulta_ventas.py
badd +1 ginn/formularios/consumo_balas_partida.py
badd +696 ginn/formularios/utils.py
badd +847 ginn/framework/pclases/cliente.py
badd +1094 ginn/formularios/consulta_global.py
badd +1 ginn/formularios/consulta_global.glade
badd +1 ginn/framework/pclases/__init__.py
badd +57 ginn/formularios/consumo_fibra_por_partida_gtx.py
badd +1 extra/scripts/clouseau.glade
badd +1 ginn/formularios/presupuestos.py
badd +8 ginn/lib/pygal/__init__.py
badd +14 ginn/lib/pygal/pygal/__init__.py
badd +26 ginn/lib/pygal/pygal/config.py
badd +25 ginn/lib/pygal/pygal/style.py
badd +25 ginn/lib/pygal/pygal/adapters.py
badd +1 ginn/lib/pygal/pygal/ghost.py
badd +27 ginn/lib/pygal/pygal/graph/line.py
badd +33 ginn/lib/pygal/pygal/graph/graph.py
badd +21 ginn/lib/pygal/pygal/graph/base.py
badd +36 ginn/lib/pygal/pygal/svg.py
badd +0 ginn/formularios/custom_widgets/mapamundi.py
args formularios/auditviewer.py
set lines=48 columns=117
edit extra/scripts/balas_basura_reembaladas.py
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
wincmd _ | wincmd |
split
wincmd _ | wincmd |
split
wincmd _ | wincmd |
split
13wincmd k
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
exe '3resize ' . ((&lines * 1 + 24) / 48)
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
exe '10resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 10resize ' . ((&columns * 85 + 58) / 117)
exe '11resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 11resize ' . ((&columns * 85 + 58) / 117)
exe '12resize ' . ((&lines * 9 + 24) / 48)
exe 'vert 12resize ' . ((&columns * 85 + 58) / 117)
exe '13resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 13resize ' . ((&columns * 85 + 58) / 117)
exe '14resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 14resize ' . ((&columns * 85 + 58) / 117)
exe '15resize ' . ((&lines * 12 + 24) / 48)
exe 'vert 15resize ' . ((&columns * 85 + 58) / 117)
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
45
normal! zo
52
normal! zo
60
normal! zo
60
normal! zo
60
normal! zo
60
normal! zo
65
normal! zo
68
normal! zo
71
normal! zo
71
normal! zo
71
normal! zo
71
normal! zo
71
normal! zo
71
normal! zo
71
normal! zo
80
normal! zo
102
normal! zo
103
normal! zo
106
normal! zo
107
normal! zo
110
normal! zo
111
normal! zo
118
normal! zo
127
normal! zo
132
normal! zo
134
normal! zo
134
normal! zo
134
normal! zo
136
normal! zo
136
normal! zo
136
normal! zo
136
normal! zo
136
normal! zo
142
normal! zo
147
normal! zo
147
normal! zo
147
normal! zo
147
normal! zo
147
normal! zo
147
normal! zo
173
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
196
normal! zo
206
normal! zo
209
normal! zo
217
normal! zo
224
normal! zo
225
normal! zo
225
normal! zo
225
normal! zo
225
normal! zo
225
normal! zo
240
normal! zo
249
normal! zo
252
normal! zo
258
normal! zo
263
normal! zo
268
normal! zo
298
normal! zo
299
normal! zo
let s:l = 69 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
69
normal! 044|
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
16629
normal! zo
16736
normal! zo
let s:l = 17294 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
17294
normal! 018|
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
let s:l = 30 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
30
normal! 0
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/partes_de_fabricacion_gtx.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
84
normal! zo
84
normal! zc
157
normal! zo
157
normal! zc
205
normal! zo
206
normal! zo
218
normal! zo
218
normal! zo
218
normal! zo
320
normal! zo
912
normal! zo
1269
normal! zo
1411
normal! zo
1697
normal! zo
2412
normal! zo
2419
normal! zo
let s:l = 506 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
506
normal! 043|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/consumo_balas_partida.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
51
normal! zo
150
normal! zo
let s:l = 159 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
159
normal! 059|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/consulta_ventas.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
55
normal! zo
60
normal! zo
246
normal! zo
let s:l = 106 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
106
normal! 031|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/consumo_fibra_por_partida_gtx.py
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
70
normal! zo
70
normal! zo
70
normal! zo
72
normal! zo
72
normal! zo
160
normal! zo
169
normal! zo
170
normal! zo
231
normal! zo
239
normal! zo
239
normal! zo
239
normal! zo
239
normal! zo
239
normal! zo
239
normal! zo
239
normal! zo
239
normal! zo
246
normal! zo
252
normal! zo
259
normal! zo
260
normal! zo
277
normal! zo
311
normal! zo
312
normal! zo
312
normal! zo
332
normal! zo
338
normal! zo
341
normal! zo
349
normal! zo
352
normal! zo
360
normal! zo
363
normal! zo
373
normal! zo
382
normal! zo
445
normal! zo
449
normal! zo
456
normal! zo
let s:l = 422 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
422
normal! 033|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/lib/pygal/__init__.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 21 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
21
normal! 0
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/custom_widgets/mapamundi.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
40
normal! zo
65
normal! zo
71
normal! zo
let s:l = 58 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
58
normal! 09|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/lib/pygal/pygal/svg.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
38
normal! zo
43
normal! zo
71
normal! zo
72
normal! zo
83
normal! zo
87
normal! zo
92
normal! zo
95
normal! zo
97
normal! zo
191
normal! zo
203
normal! zo
204
normal! zo
209
normal! zo
214
normal! zo
214
normal! zo
228
normal! zo
238
normal! zo
239
normal! zo
239
normal! zo
239
normal! zo
239
normal! zo
let s:l = 98 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
98
normal! 057|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/lib/pygal/__init__.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 15 - ((3 * winheight(0) + 4) / 9)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
15
normal! 030|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/lib/pygal/pygal/ghost.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
42
normal! zo
47
normal! zo
48
normal! zo
57
normal! zo
58
normal! zo
77
normal! zo
92
normal! zo
93
normal! zo
94
normal! zo
95
normal! zo
96
normal! zo
109
normal! zo
110
normal! zo
140
normal! zo
145
normal! zo
151
normal! zo
172
normal! zo
173
normal! zo
173
normal! zo
173
normal! zo
177
normal! zo
let s:l = 43 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
43
normal! 046|
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
67
normal! zo
68
normal! zo
160
normal! zo
160
normal! zo
160
normal! zo
423
normal! zo
432
normal! zo
475
normal! zo
476
normal! zo
481
normal! zo
482
normal! zo
492
normal! zo
500
normal! zo
576
normal! zo
578
normal! zo
579
normal! zo
580
normal! zo
699
normal! zo
708
normal! zo
710
normal! zo
713
normal! zo
830
normal! zo
849
normal! zo
882
normal! zo
2687
normal! zo
let s:l = 473 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
473
normal! 013|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/consulta_producido.py
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
75
normal! zo
75
normal! zo
75
normal! zo
1132
normal! zo
1384
normal! zo
1384
normal! zo
let s:l = 83 - ((0 * winheight(0) + 6) / 12)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
83
normal! 048|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
12wincmd w
exe 'vert 1resize ' . ((&columns * 31 + 58) / 117)
exe '2resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 85 + 58) / 117)
exe '3resize ' . ((&lines * 1 + 24) / 48)
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
exe '10resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 10resize ' . ((&columns * 85 + 58) / 117)
exe '11resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 11resize ' . ((&columns * 85 + 58) / 117)
exe '12resize ' . ((&lines * 9 + 24) / 48)
exe 'vert 12resize ' . ((&columns * 85 + 58) / 117)
exe '13resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 13resize ' . ((&columns * 85 + 58) / 117)
exe '14resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 14resize ' . ((&columns * 85 + 58) / 117)
exe '15resize ' . ((&lines * 12 + 24) / 48)
exe 'vert 15resize ' . ((&columns * 85 + 58) / 117)
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
12wincmd w

" vim: ft=vim ro nowrap smc=128
