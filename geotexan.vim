" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 27 junio 2014 at 12:09:13.
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
badd +696 ginn/formularios/utils.py
badd +95 ginn/framework/pclases/cliente.py
badd +1094 ginn/formularios/consulta_global.py
badd +1 ginn/formularios/consulta_global.glade
badd +528 ginn/formularios/consumo_fibra_por_partida_gtx.py
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
badd +108 ginn/formularios/facturas_venta.py
badd +1 ginn/framework/pclases/superfacturaventa.py
badd +1867 ginn/formularios/facturas_compra.py
badd +111 ginn/formularios/prefacturas.py
badd +1020 ginn/formularios/pedidos_de_venta.py
badd +5 ginn/formularios/launcher.py
badd +1 ginn/framework/pclases/__init__.py
badd +0 ginn/formularios/presupuestos.py
argglobal
silent! argdel *
argadd formularios/auditviewer.py
set lines=58 columns=86
edit extra/scripts/balas_basura_reembaladas.py
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
10wincmd k
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
exe '1resize ' . ((&lines * 4 + 29) / 58)
exe '2resize ' . ((&lines * 3 + 29) / 58)
exe '3resize ' . ((&lines * 1 + 29) / 58)
exe '4resize ' . ((&lines * 1 + 29) / 58)
exe '5resize ' . ((&lines * 1 + 29) / 58)
exe '6resize ' . ((&lines * 31 + 29) / 58)
exe '7resize ' . ((&lines * 1 + 29) / 58)
exe '8resize ' . ((&lines * 1 + 29) / 58)
exe '9resize ' . ((&lines * 1 + 29) / 58)
exe '10resize ' . ((&lines * 1 + 29) / 58)
exe '11resize ' . ((&lines * 1 + 29) / 58)
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
let s:l = 69 - ((0 * winheight(0) + 2) / 4)
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
let s:l = 28 - ((0 * winheight(0) + 1) / 3)
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
edit ~/Geotexan/src/Geotex-INN/ginn/framework/pclases/__init__.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
2807
normal! zo
2808
normal! zo
2878
normal! zo
3142
normal! zo
3157
normal! zo
let s:l = 3157 - ((1 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3157
normal! 017|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/framework/pclases/superfacturaventa.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
52
normal! zo
57
normal! zo
73
normal! zo
868
normal! zo
879
normal! zo
912
normal! zo
936
normal! zo
950
normal! zo
995
normal! zo
1001
normal! zo
1008
normal! zo
let s:l = 1001 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1001
normal! 037|
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
944
normal! zo
1026
normal! zo
1274
normal! zo
1612
normal! zo
1640
normal! zo
1729
normal! zo
1740
normal! zo
1777
normal! zo
1850
normal! zo
1850
normal! zo
1850
normal! zo
1972
normal! zo
2309
normal! zo
2692
normal! zo
let s:l = 2783 - ((20 * winheight(0) + 15) / 31)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2783
normal! 051|
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
104
normal! zo
107
normal! zo
108
normal! zo
128
normal! zo
128
normal! zo
128
normal! zo
146
normal! zo
633
normal! zo
824
normal! zo
843
normal! zo
868
normal! zo
873
normal! zo
929
normal! zo
931
normal! zo
938
normal! zo
939
normal! zo
2245
normal! zo
2327
normal! zo
2336
normal! zo
2365
normal! zo
2370
normal! zo
2433
normal! zo
2446
normal! zo
2462
normal! zo
2465
normal! zo
2755
normal! zo
2770
normal! zo
2772
normal! zo
2773
normal! zo
3043
normal! zo
3066
normal! zo
3080
normal! zo
3080
normal! zo
3080
normal! zo
3176
normal! zo
3179
normal! zo
3180
normal! zo
3184
normal! zo
3186
normal! zo
3187
normal! zo
3246
normal! zo
3257
normal! zo
3262
normal! zo
3280
normal! zo
3327
normal! zo
3337
normal! zo
3348
normal! zo
let s:l = 2770 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2770
normal! 040|
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
68
normal! zo
79
normal! zo
82
normal! zo
85
normal! zo
86
normal! zo
703
normal! zo
704
normal! zo
706
normal! zo
712
normal! zo
713
normal! zo
722
normal! zo
723
normal! zo
729
normal! zo
730
normal! zo
738
normal! zo
739
normal! zo
743
normal! zo
744
normal! zo
747
normal! zo
748
normal! zo
751
normal! zo
752
normal! zo
756
normal! zo
757
normal! zo
760
normal! zo
761
normal! zo
766
normal! zo
767
normal! zo
775
normal! zo
776
normal! zo
779
normal! zo
780
normal! zo
783
normal! zo
784
normal! zo
789
normal! zo
790
normal! zo
793
normal! zo
798
normal! zo
816
normal! zo
824
normal! zo
829
normal! zo
849
normal! zo
855
normal! zo
855
normal! zo
855
normal! zo
855
normal! zo
855
normal! zo
855
normal! zo
855
normal! zo
858
normal! zo
863
normal! zo
1019
normal! zo
1104
normal! zo
1125
normal! zo
1126
normal! zo
1135
normal! zo
1136
normal! zo
1168
normal! zo
1169
normal! zo
1197
normal! zo
1198
normal! zo
1200
normal! zo
1200
normal! zo
1200
normal! zo
1200
normal! zo
1200
normal! zo
1200
normal! zo
1200
normal! zo
1205
normal! zo
1206
normal! zo
1218
normal! zo
1219
normal! zo
1227
normal! zo
1228
normal! zo
1233
normal! zo
1234
normal! zo
1237
normal! zo
1238
normal! zo
1267
normal! zo
1268
normal! zo
1350
normal! zo
1457
normal! zo
1498
normal! zo
1499
normal! zo
1528
normal! zo
1529
normal! zo
1540
normal! zo
1541
normal! zo
1558
normal! zo
1559
normal! zo
1585
normal! zo
1586
normal! zo
1590
normal! zo
1591
normal! zo
1604
normal! zo
1605
normal! zo
1608
normal! zo
1609
normal! zo
1625
normal! zo
1626
normal! zo
1626
normal! zo
1627
normal! zo
1627
normal! zo
1644
normal! zo
1645
normal! zo
1649
normal! zo
1650
normal! zo
1889
normal! zo
1920
normal! zo
1935
normal! zo
1944
normal! zo
1964
normal! zo
1966
normal! zo
let s:l = 1614 - ((1 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1614
normal! 024|
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
let s:l = 53 - ((1 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
53
normal! 044|
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
let s:l = 183 - ((1 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
183
normal! 022|
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
let s:l = 377 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
377
normal! 041|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
6wincmd w
exe '1resize ' . ((&lines * 4 + 29) / 58)
exe '2resize ' . ((&lines * 3 + 29) / 58)
exe '3resize ' . ((&lines * 1 + 29) / 58)
exe '4resize ' . ((&lines * 1 + 29) / 58)
exe '5resize ' . ((&lines * 1 + 29) / 58)
exe '6resize ' . ((&lines * 31 + 29) / 58)
exe '7resize ' . ((&lines * 1 + 29) / 58)
exe '8resize ' . ((&lines * 1 + 29) / 58)
exe '9resize ' . ((&lines * 1 + 29) / 58)
exe '10resize ' . ((&lines * 1 + 29) / 58)
exe '11resize ' . ((&lines * 1 + 29) / 58)
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
6wincmd w

" vim: ft=vim ro nowrap smc=128
