" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 02 julio 2014 at 17:10:55.
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
badd +151 ginn/lib/cagraph/cagraph/ca_graph_file.py
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
badd +1 ginn/formularios/presupuestos.py
argglobal
silent! argdel *
argadd formularios/auditviewer.py
set lines=57 columns=86
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
exe '1resize ' . ((&lines * 1 + 28) / 57)
exe '2resize ' . ((&lines * 1 + 28) / 57)
exe '3resize ' . ((&lines * 1 + 28) / 57)
exe '4resize ' . ((&lines * 1 + 28) / 57)
exe '5resize ' . ((&lines * 1 + 28) / 57)
exe '6resize ' . ((&lines * 1 + 28) / 57)
exe '7resize ' . ((&lines * 1 + 28) / 57)
exe '8resize ' . ((&lines * 1 + 28) / 57)
exe '9resize ' . ((&lines * 1 + 28) / 57)
exe '10resize ' . ((&lines * 1 + 28) / 57)
exe '11resize ' . ((&lines * 35 + 28) / 57)
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
let s:l = 70 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
70
normal! 076|
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
let s:l = 882 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
882
normal! 050|
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
392
normal! zo
1652
normal! zo
1773
normal! zo
1815
normal! zo
1925
normal! zo
1992
normal! zo
2096
normal! zo
2145
normal! zo
2784
normal! zo
2808
normal! zo
2878
normal! zo
3142
normal! zo
3157
normal! zo
6860
normal! zo
6886
normal! zo
6892
normal! zo
7738
normal! zo
7862
normal! zo
7862
normal! zo
7862
normal! zo
7862
normal! zo
7862
normal! zo
7862
normal! zo
7931
normal! zo
7938
normal! zo
7944
normal! zo
8428
normal! zo
11347
normal! zo
11734
normal! zo
11734
normal! zo
11734
normal! zo
11734
normal! zo
11734
normal! zo
11948
normal! zo
11973
normal! zo
11977
normal! zo
11977
normal! zo
11978
normal! zo
11979
normal! zo
11979
normal! zo
12107
normal! zo
12107
normal! zo
12148
normal! zo
12148
normal! zo
12148
normal! zo
12148
normal! zo
12148
normal! zo
12152
normal! zo
12153
normal! zo
12153
normal! zo
12153
normal! zo
12153
normal! zo
12153
normal! zo
12153
normal! zo
12190
normal! zo
12192
normal! zo
12197
normal! zo
12264
normal! zo
12264
normal! zo
12264
normal! zo
12278
normal! zo
let s:l = 11924 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
11924
normal! 013|
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
let s:l = 914 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
914
normal! 09|
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
69
normal! zo
161
normal! zo
161
normal! zo
161
normal! zo
403
normal! zo
945
normal! zo
983
normal! zo
998
normal! zo
1008
normal! zo
1027
normal! zo
1076
normal! zo
1083
normal! zo
1083
normal! zo
1088
normal! zo
1089
normal! zo
1094
normal! zo
1096
normal! zo
1208
normal! zo
1215
normal! zo
1217
normal! zo
1245
normal! zo
1275
normal! zo
1600
normal! zo
1604
normal! zo
1607
normal! zo
1613
normal! zo
1613
normal! zo
1613
normal! zo
1613
normal! zo
1613
normal! zo
1613
normal! zo
1641
normal! zo
1730
normal! zo
1741
normal! zo
1778
normal! zo
1786
normal! zo
1804
normal! zo
1807
normal! zo
1851
normal! zo
1851
normal! zo
1851
normal! zo
1973
normal! zo
2126
normal! zo
2312
normal! zo
2318
normal! zo
2319
normal! zo
2529
normal! zo
2535
normal! zo
2541
normal! zo
2542
normal! zo
2543
normal! zo
2696
normal! zo
2884
normal! zo
2887
normal! zo
2895
normal! zo
3228
normal! zo
3242
normal! zo
let s:l = 1 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
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
3246
normal! zo
3246
normal! zo
3246
normal! zo
3246
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
let s:l = 1614 - ((0 * winheight(0) + 0) / 1)
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
55
normal! zo
59
normal! zo
81
normal! zo
81
normal! zo
95
normal! zo
95
normal! zo
95
normal! zo
95
normal! zo
95
normal! zo
95
normal! zo
95
normal! zo
95
normal! zo
159
normal! zo
186
normal! zo
200
normal! zo
206
normal! zo
219
normal! zo
219
normal! zo
238
normal! zo
243
normal! zo
243
normal! zo
243
normal! zo
243
normal! zo
251
normal! zo
252
normal! zo
309
normal! zo
321
normal! zo
321
normal! zo
321
normal! zo
321
normal! zo
let s:l = 59 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
59
normal! 011|
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
4625
normal! zo
5905
normal! zo
5970
normal! zo
5979
normal! zo
5979
normal! zo
5979
normal! zo
5979
normal! zo
5979
normal! zo
5979
normal! zo
5981
normal! zo
11347
normal! zo
14731
normal! zo
15252
normal! zo
16250
normal! zo
16690
normal! zo
17071
normal! zo
17081
normal! zo
17084
normal! zo
17664
normal! zo
17688
normal! zo
17693
normal! zo
17864
normal! zo
let s:l = 5982 - ((1 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
5982
normal! 034|
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
let s:l = 391 - ((27 * winheight(0) + 17) / 35)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
391
normal! 025|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
11wincmd w
exe '1resize ' . ((&lines * 1 + 28) / 57)
exe '2resize ' . ((&lines * 1 + 28) / 57)
exe '3resize ' . ((&lines * 1 + 28) / 57)
exe '4resize ' . ((&lines * 1 + 28) / 57)
exe '5resize ' . ((&lines * 1 + 28) / 57)
exe '6resize ' . ((&lines * 1 + 28) / 57)
exe '7resize ' . ((&lines * 1 + 28) / 57)
exe '8resize ' . ((&lines * 1 + 28) / 57)
exe '9resize ' . ((&lines * 1 + 28) / 57)
exe '10resize ' . ((&lines * 1 + 28) / 57)
exe '11resize ' . ((&lines * 35 + 28) / 57)
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
11wincmd w

" vim: ft=vim ro nowrap smc=128
