" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 07 julio 2014 at 14:53:15.
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
badd +590 ginn/formularios/listado_rollos.py
badd +7346 ginn/informes/geninformes.py
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
badd +151 ginn/lib/cagraph/cagraph/ca_graph_file.py
badd +93 ginn/lib/cagraph/cagraph/axis/yaxis.py
badd +111 ginn/formularios/widgets.py
badd +335 ginn/formularios/custom_widgets/gtkcairoplot.py
badd +1 ginn/lib/cairoplot/__init__.py
badd +1 ginn/lib/cagraph/cagraph/series/__init__.py
badd +84 ginn/lib/cagraph/cagraph/series/dna.py
badd +562 ginn/formularios/facturas_venta.py
badd +1 ginn/framework/pclases/superfacturaventa.py
badd +1867 ginn/formularios/facturas_compra.py
badd +111 ginn/formularios/prefacturas.py
badd +1020 ginn/formularios/pedidos_de_venta.py
badd +5 ginn/formularios/launcher.py
badd +17415 ginn/framework/pclases/__init__.py
badd +1 ginn/formularios/presupuestos.py
badd +3551 ginn/formularios/albaranes_de_salida.py
badd +1 ginn/formularios/pclase2tv.py
badd +1 ginn/formularios/abonos_venta.glade
badd +428 ginn/formularios/clientes.py
badd +513 ginn/formularios/crm_detalles_factura.py
badd +406 ginn/formularios/crm_seguimiento_impagos.py
args formularios/auditviewer.py
set lines=48 columns=115
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
exe 'vert 1resize ' . ((&columns * 27 + 57) / 115)
exe '2resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 87 + 57) / 115)
exe '3resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 3resize ' . ((&columns * 87 + 57) / 115)
exe '4resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 4resize ' . ((&columns * 87 + 57) / 115)
exe '5resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 5resize ' . ((&columns * 87 + 57) / 115)
exe '6resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 6resize ' . ((&columns * 87 + 57) / 115)
exe '7resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 7resize ' . ((&columns * 87 + 57) / 115)
exe '8resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 8resize ' . ((&columns * 87 + 57) / 115)
exe '9resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 9resize ' . ((&columns * 87 + 57) / 115)
exe '10resize ' . ((&lines * 26 + 24) / 48)
exe 'vert 10resize ' . ((&columns * 87 + 57) / 115)
exe '11resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 11resize ' . ((&columns * 87 + 57) / 115)
exe '12resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 12resize ' . ((&columns * 87 + 57) / 115)
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
edit ~/Geotexan/src/Geotex-INN/ginn/framework/pclases/superfacturaventa.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
53
normal! zo
58
normal! zo
74
normal! zo
508
normal! zo
518
normal! zo
527
normal! zo
527
normal! zo
527
normal! zo
527
normal! zo
527
normal! zo
527
normal! zo
539
normal! zo
869
normal! zo
880
normal! zo
899
normal! zo
900
normal! zo
903
normal! zo
905
normal! zo
913
normal! zo
937
normal! zo
951
normal! zo
996
normal! zo
1002
normal! zo
1009
normal! zo
let s:l = 41 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
41
normal! 012|
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
let s:l = 323 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
323
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
1084
normal! zo
2900
normal! zo
3117
normal! zo
3433
normal! zo
3441
normal! zo
3441
normal! zo
3441
normal! zo
3441
normal! zo
3441
normal! zo
3441
normal! zo
3538
normal! zo
3538
normal! zo
3538
normal! zo
3538
normal! zo
3538
normal! zo
3538
normal! zo
3538
normal! zo
3541
normal! zo
3541
normal! zo
3541
normal! zo
3541
normal! zo
3541
normal! zo
3550
normal! zo
4725
normal! zo
4744
normal! zo
4760
normal! zo
let s:l = 4767 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
4767
normal! 014|
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
271
normal! zo
334
normal! zo
361
normal! zo
390
normal! zo
1650
normal! zo
1771
normal! zo
1813
normal! zo
1924
normal! zo
1957
normal! zo
1965
normal! zo
1967
normal! zo
1973
normal! zo
1973
normal! zo
1973
normal! zo
1973
normal! zo
1994
normal! zo
2005
normal! zo
2005
normal! zo
2100
normal! zo
2149
normal! zo
2168
normal! zo
2169
normal! zo
2169
normal! zo
2169
normal! zo
2169
normal! zo
3807
normal! zo
3838
normal! zo
3838
normal! zo
3838
normal! zo
3838
normal! zo
3838
normal! zo
3838
normal! zo
3838
normal! zo
3838
normal! zo
3838
normal! zo
3838
normal! zo
3838
normal! zo
3840
normal! zo
3840
normal! zo
3840
normal! zo
3840
normal! zo
3840
normal! zo
3840
normal! zo
3840
normal! zo
3840
normal! zo
3840
normal! zo
3840
normal! zo
3840
normal! zo
3842
normal! zo
3842
normal! zo
3842
normal! zo
3842
normal! zo
3842
normal! zo
3842
normal! zo
3842
normal! zo
3842
normal! zo
3842
normal! zo
3842
normal! zo
3842
normal! zo
3844
normal! zo
3844
normal! zo
3844
normal! zo
3844
normal! zo
3844
normal! zo
3844
normal! zo
3844
normal! zo
3844
normal! zo
3844
normal! zo
3844
normal! zo
3844
normal! zo
3846
normal! zo
3846
normal! zo
3846
normal! zo
3846
normal! zo
3846
normal! zo
3846
normal! zo
3846
normal! zo
3846
normal! zo
3846
normal! zo
3846
normal! zo
3846
normal! zo
3848
normal! zo
3848
normal! zo
3848
normal! zo
3848
normal! zo
3848
normal! zo
3848
normal! zo
3848
normal! zo
3848
normal! zo
3848
normal! zo
3848
normal! zo
3848
normal! zo
3851
normal! zo
3858
normal! zo
3859
normal! zo
3859
normal! zo
3859
normal! zo
3859
normal! zo
3859
normal! zo
3861
normal! zo
3862
normal! zo
3867
normal! zo
3868
normal! zo
3882
normal! zo
3887
normal! zo
3888
normal! zo
3888
normal! zo
3888
normal! zo
3893
normal! zo
3893
normal! zo
3893
normal! zo
3896
normal! zo
3902
normal! zo
4643
normal! zo
5923
normal! zo
5988
normal! zo
5997
normal! zo
5997
normal! zo
5997
normal! zo
5997
normal! zo
5997
normal! zo
5997
normal! zo
5999
normal! zo
6587
normal! zo
6688
normal! zo
6976
normal! zo
7321
normal! zo
7339
normal! zo
7435
normal! zo
7457
normal! zo
7756
normal! zo
7880
normal! zo
7949
normal! zo
7956
normal! zo
7962
normal! zo
8446
normal! zo
11365
normal! zo
11752
normal! zo
11966
normal! zo
12125
normal! zo
12125
normal! zo
12282
normal! zo
12282
normal! zo
12296
normal! zo
12398
normal! zo
12748
normal! zo
12781
normal! zo
12782
normal! zo
12785
normal! zo
12799
normal! zo
14749
normal! zo
15241
normal! zo
15270
normal! zo
16268
normal! zo
16446
normal! zo
16510
normal! zo
16708
normal! zo
17089
normal! zo
17099
normal! zo
17102
normal! zo
17400
normal! zo
17414
normal! zo
17417
normal! zo
17421
normal! zo
17422
normal! zo
17682
normal! zo
17706
normal! zo
17711
normal! zo
17882
normal! zo
let s:l = 3959 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3959
normal! 046|
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
1469
normal! zo
1627
normal! zo
1636
normal! zo
1684
normal! zo
1688
normal! zo
1692
normal! zo
1694
normal! zo
1695
normal! zo
1695
normal! zo
1698
normal! zo
1702
normal! zo
1703
normal! zo
1709
normal! zo
1715
normal! zo
1715
normal! zo
1717
normal! zo
1795
normal! zo
1808
normal! zo
1813
normal! zo
1813
normal! zo
1813
normal! zo
1813
normal! zo
1813
normal! zo
1813
normal! zo
1850
normal! zo
1850
normal! zo
1850
normal! zo
1850
normal! zo
1850
normal! zo
1909
normal! zo
1992
normal! zo
1993
normal! zo
1993
normal! zo
1993
normal! zo
2056
normal! zo
2061
normal! zo
2062
normal! zo
2062
normal! zo
2062
normal! zo
2069
normal! zo
2076
normal! zo
2077
normal! zo
2083
normal! zo
2102
normal! zo
2104
normal! zo
2119
normal! zo
2127
normal! zo
2127
normal! zo
2127
normal! zo
2127
normal! zo
2131
normal! zo
2131
normal! zo
2134
normal! zo
2134
normal! zo
2134
normal! zo
2134
normal! zo
2134
normal! zo
2136
normal! zo
2136
normal! zo
2139
normal! zo
2141
normal! zo
2151
normal! zo
2188
normal! zo
2189
normal! zo
let s:l = 1633 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1633
normal! 038|
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
68
normal! zo
423
normal! zo
1003
normal! zo
1018
normal! zo
1028
normal! zo
1096
normal! zo
1103
normal! zo
1108
normal! zo
1109
normal! zo
1114
normal! zo
1116
normal! zo
1228
normal! zo
1235
normal! zo
1237
normal! zo
1295
normal! zo
1993
normal! zo
2039
normal! zo
2040
normal! zo
2068
normal! zo
2071
normal! zo
2072
normal! zo
2146
normal! zo
2177
normal! zo
2186
normal! zo
2186
normal! zo
2239
normal! zo
2302
normal! zo
2306
normal! zo
2308
normal! zo
2575
normal! zo
2621
normal! zo
2640
normal! zo
2648
normal! zo
2716
normal! zo
2733
normal! zo
2735
normal! zo
let s:l = 2733 - ((3 * winheight(0) + 13) / 26)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2733
normal! 039|
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
62
normal! zo
63
normal! zo
76
normal! zo
76
normal! zo
76
normal! zo
117
normal! zo
121
normal! zo
127
normal! zo
167
normal! zo
192
normal! zo
308
normal! zo
308
normal! zo
308
normal! zo
308
normal! zo
479
normal! zo
480
normal! zo
484
normal! zo
660
normal! zo
681
normal! zo
let s:l = 56 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
56
normal! 054|
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
369
normal! zo
373
normal! zo
373
normal! zo
395
normal! zo
let s:l = 402 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
402
normal! 040|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
exe 'vert 1resize ' . ((&columns * 27 + 57) / 115)
exe '2resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 87 + 57) / 115)
exe '3resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 3resize ' . ((&columns * 87 + 57) / 115)
exe '4resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 4resize ' . ((&columns * 87 + 57) / 115)
exe '5resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 5resize ' . ((&columns * 87 + 57) / 115)
exe '6resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 6resize ' . ((&columns * 87 + 57) / 115)
exe '7resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 7resize ' . ((&columns * 87 + 57) / 115)
exe '8resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 8resize ' . ((&columns * 87 + 57) / 115)
exe '9resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 9resize ' . ((&columns * 87 + 57) / 115)
exe '10resize ' . ((&lines * 26 + 24) / 48)
exe 'vert 10resize ' . ((&columns * 87 + 57) / 115)
exe '11resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 11resize ' . ((&columns * 87 + 57) / 115)
exe '12resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 12resize ' . ((&columns * 87 + 57) / 115)
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
1wincmd w

" vim: ft=vim ro nowrap smc=128
