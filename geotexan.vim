" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 25 junio 2014 at 14:59:54.
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
badd +85 ginn/formularios/consulta_producido.py
badd +247 ginn/formularios/consulta_consumo.py
badd +41 ginn/framework/memoize.py
badd +596 ginn/formularios/presupuesto.py
badd +47 ginn/formularios/consulta_productividad.py
badd +590 ginn/formularios/listado_rollos.py
badd +3049 ginn/informes/geninformes.py
badd +402 ginn/informes/norma2013.py
badd +1 ginn/formularios/consumo_balas_partida.py
badd +696 ginn/formularios/utils.py
badd +847 ginn/framework/pclases/cliente.py
badd +1094 ginn/formularios/consulta_global.py
badd +1 ginn/formularios/consulta_global.glade
badd +10312 ginn/framework/pclases/__init__.py
badd +57 ginn/formularios/consumo_fibra_por_partida_gtx.py
badd +1 extra/scripts/clouseau.glade
badd +27 ginn/lib/pygal/pygal/__init__.py
badd +25 ginn/lib/pygal/pygal/config.py
badd +25 ginn/lib/pygal/pygal/style.py
badd +25 ginn/lib/pygal/pygal/adapters.py
badd +42 ginn/lib/pygal/pygal/ghost.py
badd +25 ginn/lib/pygal/pygal/graph/line.py
badd +28 ginn/lib/pygal/pygal/graph/graph.py
badd +29 ginn/lib/pygal/pygal/graph/base.py
badd +98 ginn/lib/pygal/pygal/svg.py
badd +90 ginn/formularios/custom_widgets/mapamundi.py
badd +329 ginn/lib/pygal/pygal/util.py
badd +25 ginn/lib/pygal/pygal/graph/stackedline.py
badd +26 ginn/lib/pygal/pygal/graph/xy.py
badd +26 ginn/lib/pygal/pygal/graph/bar.py
badd +24 ginn/lib/pygal/pygal/graph/horizontalbar.py
badd +1 ginn/lib/pygal/pygal/graph/horizontal.p
badd +24 ginn/lib/pygal/pygal/graph/horizontal.py
badd +27 ginn/lib/pygal/pygal/graph/stackedbar.py
badd +24 ginn/lib/pygal/pygal/graph/horizontalstackedbar.py
badd +27 ginn/lib/pygal/pygal/graph/pie.py
badd +28 ginn/lib/pygal/pygal/graph/radar.py
badd +1 ginn/lib/pygal/pygal/graph/funel.py
badd +27 ginn/lib/pygal/pygal/graph/funnel.py
badd +25 ginn/lib/pygal/pygal/graph/pyramid.py
badd +26 ginn/lib/pygal/pygal/graph/verticalpyramid.py
badd +27 ginn/lib/pygal/pygal/graph/dot.py
badd +27 ginn/lib/pygal/pygal/graph/gauge.py
badd +42 ginn/lib/pygal/pygal/graph/datey.py
badd +28 ginn/lib/pygal/pygal/graph/worldmap.py
badd +28 ginn/lib/pygal/pygal/graph/supranationalworldmap.py
badd +26 ginn/lib/pygal/pygal/graph/histogram.py
badd +26 ginn/lib/pygal/pygal/graph/box.py
badd +36 ginn/formularios/custom_widgets/cairoplot.py
badd +1 ginn/lib/cairoplot/cairoplot.py
badd +1 ginn/formularios/consulta_pedidos_clientes.py
badd +1230 ginn/formularios/clientes.py
badd +147 ginn/lib/cagraph/cagraph/ca_graph.py
badd +107 ginn/lib/cagraph/cagraph/ca_graph_file.py
badd +93 ginn/lib/cagraph/cagraph/axis/yaxis.py
badd +111 ginn/formularios/widgets.py
badd +335 ginn/formularios/custom_widgets/gtkcairoplot.py
badd +1 ginn/lib/cairoplot/__init__.py
badd +1 ginn/lib/cagraph/cagraph/series/__init__.py
badd +84 ginn/lib/cagraph/cagraph/series/dna.py
badd +1 ginn/formularios/facturas_venta.py
badd +1 ginn/framework/pclases/superfacturaventa.py
badd +0 ginn/formularios/albaranes_de_salida.py
args formularios/auditviewer.py
set lines=48 columns=87
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
9wincmd k
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
exe 'vert 1resize ' . ((&columns * 30 + 43) / 87)
exe '2resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 56 + 43) / 87)
exe '3resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 3resize ' . ((&columns * 56 + 43) / 87)
exe '4resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 4resize ' . ((&columns * 56 + 43) / 87)
exe '5resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 5resize ' . ((&columns * 56 + 43) / 87)
exe '6resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 6resize ' . ((&columns * 56 + 43) / 87)
exe '7resize ' . ((&lines * 28 + 24) / 48)
exe 'vert 7resize ' . ((&columns * 56 + 43) / 87)
exe '8resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 8resize ' . ((&columns * 56 + 43) / 87)
exe '9resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 9resize ' . ((&columns * 56 + 43) / 87)
exe '10resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 10resize ' . ((&columns * 56 + 43) / 87)
exe '11resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 11resize ' . ((&columns * 56 + 43) / 87)
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
normal! 060|
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
let s:l = 28 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
28
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
let s:l = 163 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
163
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
414
normal! zo
445
normal! zo
449
normal! zo
456
normal! zo
let s:l = 537 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
537
normal! 0
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/albaranes_de_salida.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
98
normal! zo
4172
normal! zo
4206
normal! zo
4378
normal! zo
4392
normal! zo
let s:l = 4385 - ((6 * winheight(0) + 14) / 28)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
4385
normal! 044|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/facturas_venta.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
106
normal! zo
107
normal! zo
127
normal! zo
127
normal! zo
127
normal! zo
145
normal! zo
823
normal! zo
928
normal! zo
930
normal! zo
2871
normal! zo
2886
normal! zo
let s:l = 2473 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2473
normal! 05|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/consulta_pedidos_clientes.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
58
normal! zo
62
normal! zo
84
normal! zo
84
normal! zo
98
normal! zo
98
normal! zo
98
normal! zo
98
normal! zo
98
normal! zo
98
normal! zo
98
normal! zo
98
normal! zo
162
normal! zo
189
normal! zo
203
normal! zo
209
normal! zo
222
normal! zo
222
normal! zo
241
normal! zo
246
normal! zo
246
normal! zo
246
normal! zo
246
normal! zo
254
normal! zo
255
normal! zo
312
normal! zo
324
normal! zo
324
normal! zo
324
normal! zo
324
normal! zo
let s:l = 57 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
57
normal! 0
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/lib/cagraph/cagraph/ca_graph_file.py
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
60
normal! zo
let s:l = 180 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
180
normal! 08|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/custom_widgets/gtkcairoplot.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
71
normal! zo
75
normal! zo
149
normal! zo
159
normal! zo
225
normal! zo
234
normal! zo
274
normal! zo
278
normal! zo
281
normal! zo
294
normal! zo
308
normal! zo
309
normal! zo
310
normal! zo
311
normal! zo
311
normal! zo
329
normal! zo
345
normal! zo
350
normal! zo
392
normal! zo
let s:l = 385 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
385
normal! 033|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
7wincmd w
exe 'vert 1resize ' . ((&columns * 30 + 43) / 87)
exe '2resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 56 + 43) / 87)
exe '3resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 3resize ' . ((&columns * 56 + 43) / 87)
exe '4resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 4resize ' . ((&columns * 56 + 43) / 87)
exe '5resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 5resize ' . ((&columns * 56 + 43) / 87)
exe '6resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 6resize ' . ((&columns * 56 + 43) / 87)
exe '7resize ' . ((&lines * 28 + 24) / 48)
exe 'vert 7resize ' . ((&columns * 56 + 43) / 87)
exe '8resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 8resize ' . ((&columns * 56 + 43) / 87)
exe '9resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 9resize ' . ((&columns * 56 + 43) / 87)
exe '10resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 10resize ' . ((&columns * 56 + 43) / 87)
exe '11resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 11resize ' . ((&columns * 56 + 43) / 87)
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
7wincmd w

" vim: ft=vim ro nowrap smc=128
