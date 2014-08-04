" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 01 agosto 2014 at 14:26:37.
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
badd +1119 ginn/formularios/consulta_producido.py
badd +126 ginn/formularios/consulta_consumo.py
badd +41 ginn/framework/memoize.py
badd +596 ginn/formularios/presupuesto.py
badd +44 ginn/formularios/listado_rollos.py
badd +89 ginn/informes/norma2013.py
badd +95 ginn/framework/pclases/cliente.py
badd +145 ginn/formularios/consulta_global.py
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
badd +151 ginn/lib/cagraph/cagraph/ca_graph_file.py
badd +93 ginn/lib/cagraph/cagraph/axis/yaxis.py
badd +111 ginn/formularios/widgets.py
badd +335 ginn/formularios/custom_widgets/gtkcairoplot.py
badd +1 ginn/lib/cairoplot/__init__.py
badd +1 ginn/lib/cagraph/cagraph/series/__init__.py
badd +84 ginn/lib/cagraph/cagraph/series/dna.py
badd +562 ginn/formularios/facturas_venta.py
badd +1867 ginn/formularios/facturas_compra.py
badd +111 ginn/formularios/prefacturas.py
badd +1020 ginn/formularios/pedidos_de_venta.py
badd +5 ginn/formularios/launcher.py
badd +9974 ginn/framework/pclases/__init__.py
badd +1 ginn/formularios/pclase2tv.py
badd +1 ginn/formularios/abonos_venta.glade
badd +513 ginn/formularios/crm_detalles_factura.py
badd +406 ginn/formularios/crm_seguimiento_impagos.py
badd +1 extra/scripts/clouseau-gtk.py
badd +1 extra/scripts/clouseau.py
badd +1 ginn/framework/configuracion.py
badd +1 ginn/formularios/partes_de_fabricacion_rollos.py
badd +1 ginn/formularios/consulta_producciones_estandar.py
badd +1 ginn/formularios/albaranes_de_salida.py
badd +1 ginn/formularios/consulta_cobros.py
badd +411 ginn/formularios/pagares_pagos.py
badd +1 ginn/formularios/consulta_pendientes_servir.py
args formularios/auditviewer.py
set lines=48 columns=86
edit extra/scripts/clouseau.py
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
exe 'vert 1resize ' . ((&columns * 30 + 43) / 86)
exe '2resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 55 + 43) / 86)
exe '3resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 3resize ' . ((&columns * 55 + 43) / 86)
exe '4resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 4resize ' . ((&columns * 55 + 43) / 86)
exe '5resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 5resize ' . ((&columns * 55 + 43) / 86)
exe '6resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 6resize ' . ((&columns * 55 + 43) / 86)
exe '7resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 7resize ' . ((&columns * 55 + 43) / 86)
exe '8resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 8resize ' . ((&columns * 55 + 43) / 86)
exe '9resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 9resize ' . ((&columns * 55 + 43) / 86)
exe '10resize ' . ((&lines * 20 + 24) / 48)
exe 'vert 10resize ' . ((&columns * 55 + 43) / 86)
exe '11resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 11resize ' . ((&columns * 55 + 43) / 86)
exe '12resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 12resize ' . ((&columns * 55 + 43) / 86)
exe '13resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 13resize ' . ((&columns * 55 + 43) / 86)
exe '14resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 14resize ' . ((&columns * 55 + 43) / 86)
exe '15resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 15resize ' . ((&columns * 55 + 43) / 86)
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
let s:l = 31 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
31
normal! 063|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/extra/scripts/balas_basura_reembaladas.py
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
let s:l = 313 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
313
normal! 029|
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
779
normal! zo
805
normal! zo
811
normal! zo
815
normal! zo
824
normal! zo
872
normal! zo
874
normal! zo
877
normal! zo
912
normal! zo
1045
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
3031
normal! zo
3047
normal! zo
3061
normal! zo
3064
normal! zo
3064
normal! zo
3070
normal! zo
3076
normal! zo
3086
normal! zo
3092
normal! zo
3145
normal! zo
3166
normal! zo
3168
normal! zo
3345
normal! zo
3357
normal! zo
3394
normal! zo
3402
normal! zo
3405
normal! zo
3422
normal! zo
3422
normal! zo
3422
normal! zo
3456
normal! zo
3463
normal! zo
3467
normal! zo
3474
normal! zo
3622
normal! zo
3630
normal! zo
3631
normal! zo
3641
normal! zo
3646
normal! zo
3709
normal! zo
3709
normal! zo
3709
normal! zo
3716
normal! zo
let s:l = 3727 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3727
normal! 024|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/pclase2tv.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
178
normal! zo
185
normal! zo
185
normal! zo
207
normal! zo
287
normal! zo
287
normal! zo
287
normal! zo
let s:l = 23 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
23
normal! 058|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/framework/configuracion.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
93
normal! zo
102
normal! zo
let s:l = 96 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
96
normal! 07|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/framework/configuracion.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
29
normal! zo
29
normal! zo
29
normal! zo
29
normal! zo
29
normal! zo
29
normal! zo
29
normal! zo
31
normal! zo
31
normal! zo
31
normal! zo
31
normal! zo
31
normal! zo
31
normal! zo
31
normal! zo
35
normal! zo
35
normal! zo
35
normal! zo
35
normal! zo
35
normal! zo
35
normal! zo
35
normal! zo
38
normal! zo
38
normal! zo
38
normal! zo
38
normal! zo
38
normal! zo
38
normal! zo
38
normal! zo
42
normal! zo
42
normal! zo
42
normal! zo
42
normal! zo
42
normal! zo
42
normal! zo
42
normal! zo
44
normal! zo
44
normal! zo
44
normal! zo
44
normal! zo
44
normal! zo
44
normal! zo
44
normal! zo
46
normal! zo
46
normal! zo
46
normal! zo
46
normal! zo
46
normal! zo
46
normal! zo
46
normal! zo
49
normal! zo
49
normal! zo
49
normal! zo
49
normal! zo
49
normal! zo
49
normal! zo
49
normal! zo
52
normal! zo
52
normal! zo
52
normal! zo
52
normal! zo
52
normal! zo
52
normal! zo
52
normal! zo
55
normal! zo
55
normal! zo
55
normal! zo
55
normal! zo
55
normal! zo
55
normal! zo
55
normal! zo
58
normal! zo
58
normal! zo
58
normal! zo
58
normal! zo
58
normal! zo
58
normal! zo
58
normal! zo
63
normal! zo
63
normal! zo
63
normal! zo
63
normal! zo
63
normal! zo
63
normal! zo
63
normal! zo
65
normal! zo
65
normal! zo
65
normal! zo
65
normal! zo
65
normal! zo
65
normal! zo
65
normal! zo
68
normal! zo
68
normal! zo
68
normal! zo
68
normal! zo
68
normal! zo
68
normal! zo
68
normal! zo
70
normal! zo
70
normal! zo
70
normal! zo
70
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
72
normal! zo
72
normal! zo
72
normal! zo
72
normal! zo
72
normal! zo
75
normal! zo
75
normal! zo
75
normal! zo
75
normal! zo
75
normal! zo
75
normal! zo
75
normal! zo
79
normal! zo
79
normal! zo
79
normal! zo
79
normal! zo
79
normal! zo
79
normal! zo
79
normal! zo
82
normal! zo
82
normal! zo
82
normal! zo
82
normal! zo
82
normal! zo
82
normal! zo
82
normal! zo
85
normal! zo
85
normal! zo
85
normal! zo
85
normal! zo
85
normal! zo
85
normal! zo
85
normal! zo
93
normal! zo
108
normal! zo
115
normal! zo
200
normal! zo
211
normal! zo
242
normal! zo
255
normal! zo
269
normal! zo
458
normal! zo
478
normal! zo
let s:l = 535 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
535
normal! 036|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/consulta_global.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
1208
normal! zo
let s:l = 144 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
144
normal! 030|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/consulta_pendientes_servir.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
102
normal! zo
126
normal! zo
132
normal! zo
132
normal! zo
134
normal! zo
134
normal! zo
178
normal! zo
343
normal! zo
344
normal! zo
351
normal! zo
351
normal! zo
351
normal! zo
353
normal! zo
353
normal! zo
390
normal! zo
392
normal! zo
442
normal! zo
498
normal! zo
498
normal! zo
505
normal! zo
557
normal! zo
573
normal! zo
574
normal! zo
574
normal! zo
574
normal! zo
582
normal! zo
596
normal! zo
596
normal! zo
596
normal! zo
596
normal! zo
596
normal! zo
596
normal! zo
596
normal! zo
596
normal! zo
596
normal! zo
596
normal! zo
599
normal! zo
605
normal! zo
606
normal! zo
613
normal! zo
613
normal! zo
613
normal! zo
613
normal! zo
613
normal! zo
613
normal! zo
613
normal! zo
613
normal! zo
613
normal! zo
613
normal! zo
613
normal! zo
let s:l = 591 - ((13 * winheight(0) + 10) / 20)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
591
normal! 039|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/consulta_cobros.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
50
normal! zo
274
normal! zo
let s:l = 335 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
335
normal! 034|
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
100
normal! zo
101
normal! zo
123
normal! zo
123
normal! zo
123
normal! zo
1244
normal! zo
2063
normal! zo
2236
normal! zo
2245
normal! zo
2262
normal! zo
2263
normal! zo
2278
normal! zo
2304
normal! zo
2306
normal! zo
2309
normal! zo
2329
normal! zo
2329
normal! zo
let s:l = 2280 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2280
normal! 034|
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
89
normal! zo
89
normal! zo
89
normal! zo
89
normal! zo
89
normal! zo
296
normal! zo
359
normal! zo
386
normal! zo
415
normal! zo
1675
normal! zo
1796
normal! zo
1838
normal! zo
1949
normal! zo
1982
normal! zo
1990
normal! zo
1992
normal! zo
1998
normal! zo
1998
normal! zo
1998
normal! zo
1998
normal! zo
2019
normal! zo
2030
normal! zo
2030
normal! zo
2125
normal! zo
2174
normal! zo
2860
normal! zo
3832
normal! zo
3863
normal! zo
3863
normal! zo
3863
normal! zo
3863
normal! zo
3863
normal! zo
3863
normal! zo
3863
normal! zo
3863
normal! zo
3863
normal! zo
3863
normal! zo
3863
normal! zo
3865
normal! zo
3865
normal! zo
3865
normal! zo
3865
normal! zo
3865
normal! zo
3865
normal! zo
3865
normal! zo
3865
normal! zo
3865
normal! zo
3865
normal! zo
3865
normal! zo
3867
normal! zo
3867
normal! zo
3867
normal! zo
3867
normal! zo
3867
normal! zo
3867
normal! zo
3867
normal! zo
3867
normal! zo
3867
normal! zo
3867
normal! zo
3867
normal! zo
3869
normal! zo
3869
normal! zo
3869
normal! zo
3869
normal! zo
3869
normal! zo
3869
normal! zo
3869
normal! zo
3869
normal! zo
3869
normal! zo
3869
normal! zo
3869
normal! zo
3871
normal! zo
3871
normal! zo
3871
normal! zo
3871
normal! zo
3871
normal! zo
3871
normal! zo
3871
normal! zo
3871
normal! zo
3871
normal! zo
3871
normal! zo
3871
normal! zo
3873
normal! zo
3873
normal! zo
3873
normal! zo
3873
normal! zo
3873
normal! zo
3873
normal! zo
3873
normal! zo
3873
normal! zo
3873
normal! zo
3873
normal! zo
3873
normal! zo
3876
normal! zo
3883
normal! zo
3884
normal! zo
3884
normal! zo
3884
normal! zo
3884
normal! zo
3884
normal! zo
3886
normal! zo
3887
normal! zo
3892
normal! zo
3893
normal! zo
3907
normal! zo
3912
normal! zo
3913
normal! zo
3913
normal! zo
3913
normal! zo
3918
normal! zo
3918
normal! zo
3918
normal! zo
3921
normal! zo
3927
normal! zo
4668
normal! zo
5948
normal! zo
6013
normal! zo
6022
normal! zo
6022
normal! zo
6022
normal! zo
6022
normal! zo
6022
normal! zo
6022
normal! zo
6024
normal! zo
6612
normal! zo
6713
normal! zo
6713
normal! zo
6713
normal! zo
6713
normal! zo
6713
normal! zo
7001
normal! zo
7346
normal! zo
7364
normal! zo
7460
normal! zo
7482
normal! zo
7781
normal! zo
7905
normal! zo
7905
normal! zo
7905
normal! zo
7905
normal! zo
7905
normal! zo
7905
normal! zo
7974
normal! zo
7981
normal! zo
7987
normal! zo
8471
normal! zo
9274
normal! zo
10072
normal! zo
10112
normal! zo
10165
normal! zo
10168
normal! zo
10565
normal! zo
10872
normal! zo
10875
normal! zo
10919
normal! zo
11390
normal! zo
11777
normal! zo
11777
normal! zo
11777
normal! zo
11777
normal! zo
11777
normal! zo
11991
normal! zo
12150
normal! zo
12150
normal! zo
12307
normal! zo
12307
normal! zo
12307
normal! zo
12321
normal! zo
12423
normal! zo
12423
normal! zo
12423
normal! zo
12423
normal! zo
12423
normal! zo
12773
normal! zo
12773
normal! zo
12773
normal! zo
12773
normal! zo
12773
normal! zo
12773
normal! zo
12773
normal! zo
12806
normal! zo
12807
normal! zo
12810
normal! zo
12824
normal! zo
14774
normal! zo
15266
normal! zo
15295
normal! zo
16293
normal! zo
16432
normal! zo
16441
normal! zo
16449
normal! zo
16450
normal! zo
16451
normal! zo
16472
normal! zo
16536
normal! zo
16536
normal! zo
16536
normal! zo
16734
normal! zo
16803
normal! zo
16817
normal! zo
16823
normal! zo
16826
normal! zo
16827
normal! zo
16842
normal! zo
16849
normal! zo
16850
normal! zo
16859
normal! zo
16870
normal! zo
16870
normal! zo
16870
normal! zo
16877
normal! zo
16877
normal! zo
16877
normal! zo
16925
normal! zo
16933
normal! zo
16938
normal! zo
17052
normal! zo
17073
normal! zo
17092
normal! zo
17126
normal! zo
17136
normal! zo
17139
normal! zo
17348
normal! zo
17437
normal! zo
17451
normal! zo
17454
normal! zo
17458
normal! zo
17459
normal! zo
17719
normal! zo
17743
normal! zo
17748
normal! zo
17919
normal! zo
18213
normal! zo
19039
normal! zo
19089
normal! zo
21484
normal! zo
21494
normal! zo
21543
normal! zo
21544
normal! zo
21544
normal! zo
let s:l = 10919 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
10919
normal! 032|
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
113
normal! zo
128
normal! zo
130
normal! zo
132
normal! zo
132
normal! zo
132
normal! zo
132
normal! zo
132
normal! zo
132
normal! zo
132
normal! zo
132
normal! zo
235
normal! zo
236
normal! zo
306
normal! zo
307
normal! zo
1075
normal! zo
1094
normal! zo
1114
normal! zo
1115
normal! zo
1115
normal! zo
1118
normal! zo
1119
normal! zo
1119
normal! zo
1122
normal! zo
1123
normal! zo
1123
normal! zo
1126
normal! zo
1127
normal! zo
1127
normal! zo
2954
normal! zo
2972
normal! zo
3035
normal! zo
3088
normal! zo
3105
normal! zo
3110
normal! zo
3110
normal! zo
3110
normal! zo
3110
normal! zo
3110
normal! zo
3113
normal! zo
3113
normal! zo
3118
normal! zo
3119
normal! zo
3121
normal! zo
3121
normal! zo
3121
normal! zo
3121
normal! zo
3123
normal! zo
3126
normal! zo
3126
normal! zo
3132
normal! zo
3138
normal! zo
3143
normal! zo
3150
normal! zo
3156
normal! zo
3162
normal! zo
3171
normal! zo
3213
normal! zo
3234
normal! zo
3236
normal! zo
3413
normal! zo
3425
normal! zo
3462
normal! zo
3470
normal! zo
3471
normal! zo
3472
normal! zo
3477
normal! zo
3478
normal! zo
3496
normal! zo
3496
normal! zo
3496
normal! zo
3516
normal! zo
3519
normal! zo
3519
normal! zo
3519
normal! zo
3519
normal! zo
3530
normal! zo
3534
normal! zo
3534
normal! zo
3534
normal! zo
3534
normal! zo
3534
normal! zo
3535
normal! zo
3537
normal! zo
3537
normal! zo
3537
normal! zo
3537
normal! zo
3540
normal! zo
3541
normal! zo
3541
normal! zo
3541
normal! zo
3542
normal! zo
3545
normal! zo
3548
normal! zo
3552
normal! zo
3557
normal! zo
3558
normal! zo
3558
normal! zo
3562
normal! zo
3577
normal! zo
3634
normal! zo
3642
normal! zo
3644
normal! zo
3647
normal! zo
3649
normal! zo
3708
normal! zo
3716
normal! zo
3717
normal! zo
3727
normal! zo
3728
normal! zo
3732
normal! zo
3733
normal! zo
3750
normal! zo
3795
normal! zo
3795
normal! zo
3795
normal! zo
3802
normal! zo
3838
normal! zo
3860
normal! zo
3879
normal! zo
3880
normal! zo
3882
normal! zo
3887
normal! zo
3887
normal! zo
3887
normal! zo
3887
normal! zo
3887
normal! zo
3922
normal! zo
3947
normal! zo
3948
normal! zo
3952
normal! zo
3954
normal! zo
3954
normal! zo
3956
normal! zo
3956
normal! zo
3956
normal! zo
let s:l = 306 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
306
normal! 013|
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
72
normal! zo
76
normal! zo
97
normal! zo
97
normal! zo
97
normal! zo
180
normal! zo
191
normal! zo
205
normal! zo
212
normal! zo
224
normal! zo
232
normal! zo
244
normal! zo
277
normal! zo
286
normal! zo
326
normal! zo
330
normal! zo
333
normal! zo
346
normal! zo
360
normal! zo
361
normal! zo
362
normal! zo
363
normal! zo
363
normal! zo
381
normal! zo
397
normal! zo
402
normal! zo
421
normal! zo
425
normal! zo
425
normal! zo
447
normal! zo
let s:l = 197 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
197
normal! 033|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
10wincmd w
exe 'vert 1resize ' . ((&columns * 30 + 43) / 86)
exe '2resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 55 + 43) / 86)
exe '3resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 3resize ' . ((&columns * 55 + 43) / 86)
exe '4resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 4resize ' . ((&columns * 55 + 43) / 86)
exe '5resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 5resize ' . ((&columns * 55 + 43) / 86)
exe '6resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 6resize ' . ((&columns * 55 + 43) / 86)
exe '7resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 7resize ' . ((&columns * 55 + 43) / 86)
exe '8resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 8resize ' . ((&columns * 55 + 43) / 86)
exe '9resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 9resize ' . ((&columns * 55 + 43) / 86)
exe '10resize ' . ((&lines * 20 + 24) / 48)
exe 'vert 10resize ' . ((&columns * 55 + 43) / 86)
exe '11resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 11resize ' . ((&columns * 55 + 43) / 86)
exe '12resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 12resize ' . ((&columns * 55 + 43) / 86)
exe '13resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 13resize ' . ((&columns * 55 + 43) / 86)
exe '14resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 14resize ' . ((&columns * 55 + 43) / 86)
exe '15resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 15resize ' . ((&columns * 55 + 43) / 86)
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
10wincmd w

" vim: ft=vim ro nowrap smc=128
