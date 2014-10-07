" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 06 octubre 2014 at 17:30:48.
" Open this file in Vim and run :source % to restore your session.

set guioptions=aegimrLtT
silent! set guifont=Source\ Code\ Pro\ 10
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
badd +19 ginn/informes/nied.py
badd +129 ginn/informes/ekotex.py
badd +1 formularios/auditviewer.py
badd +248 ginn/formularios/gtkexcepthook.py
badd +893 ginn/formularios/partes_de_fabricacion_bolsas.py
badd +1 ginn/formularios/partes_de_ancho_multiple.py
badd +427 ginn/formularios/consulta_producido.py
badd +126 ginn/formularios/consulta_consumo.py
badd +41 ginn/framework/memoize.py
badd +596 ginn/formularios/presupuesto.py
badd +44 ginn/formularios/listado_rollos.py
badd +89 ginn/informes/norma2013.py
badd +2711 ginn/formularios/consulta_global.py
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
badd +111 ginn/formularios/prefacturas.py
badd +1020 ginn/formularios/pedidos_de_venta.py
badd +5 ginn/formularios/launcher.py
badd +19059 ginn/framework/pclases/__init__.py
badd +1 ginn/formularios/abonos_venta.glade
badd +513 ginn/formularios/crm_detalles_factura.py
badd +406 ginn/formularios/crm_seguimiento_impagos.py
badd +1 extra/scripts/clouseau-gtk.py
badd +1 ginn/formularios/partes_de_fabricacion_rollos.py
badd +1 ginn/formularios/consulta_producciones_estandar.py
badd +606 ginn/formularios/consulta_pendientes_servir.py
badd +504 ginn/formularios/consulta_pagos_realizados.py
badd +21 ginn/lib/myprint.py
badd +926 ginn/formularios/consumo_balas_partida.py
badd +399 ginn/formularios/auditviewer.py
badd +1 ginn/formularios/partes_de_fabricacion_bolsas.glade
badd +115 ginn/formularios/consulta_existenciasBolsas.py
badd +23 extra/scripts/bash_completion_ginn
badd +1200 ginn/formularios/consulta_ventas.py
badd +631 ginn/formularios/pagares_cobros.py
badd +217 ginn/framework/pclases/superfacturaventa.py
badd +433 ginn/formularios/utils.py
badd +812 ginn/formularios/ventana.py
badd +5 ginn/formularios/consulta_pagos.py
badd +2234 ginn/formularios/facturas_venta.py
badd +63 ginn/formularios/clientes.py
badd +289 ginn/formularios/pclase2tv.py
args formularios/auditviewer.py
set lines=42 columns=102
edit ginn/formularios/partes_de_ancho_multiple.py
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
5wincmd k
wincmd w
wincmd w
wincmd w
wincmd w
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
exe 'vert 1resize ' . ((&columns * 18 + 51) / 102)
exe '2resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 2resize ' . ((&columns * 83 + 51) / 102)
exe '3resize ' . ((&lines * 5 + 21) / 42)
exe 'vert 3resize ' . ((&columns * 83 + 51) / 102)
exe '4resize ' . ((&lines * 2 + 21) / 42)
exe 'vert 4resize ' . ((&columns * 83 + 51) / 102)
exe '5resize ' . ((&lines * 25 + 21) / 42)
exe 'vert 5resize ' . ((&columns * 83 + 51) / 102)
exe '6resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 6resize ' . ((&columns * 83 + 51) / 102)
exe '7resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 7resize ' . ((&columns * 83 + 51) / 102)
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
let s:l = 26 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
26
normal! 0
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
287
normal! zo
287
normal! zo
287
normal! zo
328
normal! zo
330
normal! zo
332
normal! zo
let s:l = 326 - ((0 * winheight(0) + 2) / 5)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
326
normal! 013|
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
238
normal! zo
254
normal! zo
408
normal! zo
415
normal! zo
430
normal! zo
437
normal! zo
445
normal! zo
449
normal! zo
450
normal! zo
520
normal! zo
524
normal! zo
529
normal! zo
535
normal! zo
563
normal! zo
569
normal! zo
569
normal! zo
569
normal! zo
593
normal! zo
1149
normal! zo
1253
normal! zo
1253
normal! zo
1253
normal! zo
1253
normal! zo
1253
normal! zo
1253
normal! zo
1253
normal! zo
1253
normal! zo
1253
normal! zo
1253
normal! zo
1516
normal! zo
let s:l = 465 - ((0 * winheight(0) + 1) / 2)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
465
normal! 021|
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
314
normal! zo
359
normal! zo
386
normal! zo
415
normal! zo
577
normal! zo
1686
normal! zo
1807
normal! zo
1849
normal! zo
1960
normal! zo
1993
normal! zo
2001
normal! zo
2003
normal! zo
2009
normal! zo
2009
normal! zo
2009
normal! zo
2009
normal! zo
2030
normal! zo
2041
normal! zo
2041
normal! zo
2136
normal! zo
2185
normal! zo
2871
normal! zo
3281
normal! zo
3315
normal! zo
3318
normal! zo
3432
normal! zo
3843
normal! zo
3874
normal! zo
3874
normal! zo
3874
normal! zo
3874
normal! zo
3874
normal! zo
3874
normal! zo
3874
normal! zo
3874
normal! zo
3874
normal! zo
3874
normal! zo
3874
normal! zo
3876
normal! zo
3876
normal! zo
3876
normal! zo
3876
normal! zo
3876
normal! zo
3876
normal! zo
3876
normal! zo
3876
normal! zo
3876
normal! zo
3876
normal! zo
3876
normal! zo
3878
normal! zo
3878
normal! zo
3878
normal! zo
3878
normal! zo
3878
normal! zo
3878
normal! zo
3878
normal! zo
3878
normal! zo
3878
normal! zo
3878
normal! zo
3878
normal! zo
3880
normal! zo
3880
normal! zo
3880
normal! zo
3880
normal! zo
3880
normal! zo
3880
normal! zo
3880
normal! zo
3880
normal! zo
3880
normal! zo
3880
normal! zo
3880
normal! zo
3882
normal! zo
3882
normal! zo
3882
normal! zo
3882
normal! zo
3882
normal! zo
3882
normal! zo
3882
normal! zo
3882
normal! zo
3882
normal! zo
3882
normal! zo
3882
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
3884
normal! zo
3887
normal! zo
3894
normal! zo
3895
normal! zo
3895
normal! zo
3895
normal! zo
3895
normal! zo
3895
normal! zo
3897
normal! zo
3898
normal! zo
3903
normal! zo
3904
normal! zo
3918
normal! zo
3923
normal! zo
3924
normal! zo
3924
normal! zo
3924
normal! zo
3929
normal! zo
3929
normal! zo
3929
normal! zo
3932
normal! zo
3938
normal! zo
3944
normal! zo
4199
normal! zo
4583
normal! zo
4609
normal! zo
4620
normal! zo
4628
normal! zo
4682
normal! zo
5962
normal! zo
6027
normal! zo
6036
normal! zo
6036
normal! zo
6036
normal! zo
6036
normal! zo
6036
normal! zo
6036
normal! zo
6038
normal! zo
6626
normal! zo
6727
normal! zo
6727
normal! zo
6727
normal! zo
6727
normal! zo
6727
normal! zo
6917
normal! zo
7015
normal! zo
7360
normal! zo
7378
normal! zo
7474
normal! zo
7496
normal! zo
7795
normal! zo
7919
normal! zo
7919
normal! zo
7919
normal! zo
7919
normal! zo
7919
normal! zo
7919
normal! zo
7988
normal! zo
7995
normal! zo
8001
normal! zo
8485
normal! zo
9288
normal! zo
10086
normal! zo
10126
normal! zo
10179
normal! zo
10182
normal! zo
10579
normal! zo
10886
normal! zo
10889
normal! zo
10925
normal! zo
10933
normal! zo
11020
normal! zo
11024
normal! zo
11027
normal! zo
11404
normal! zo
11791
normal! zo
11791
normal! zo
11791
normal! zo
11791
normal! zo
11791
normal! zo
12005
normal! zo
12164
normal! zo
12164
normal! zo
12321
normal! zo
12321
normal! zo
12321
normal! zo
12335
normal! zo
12437
normal! zo
12437
normal! zo
12437
normal! zo
12437
normal! zo
12437
normal! zo
12787
normal! zo
12787
normal! zo
12787
normal! zo
12787
normal! zo
12787
normal! zo
12787
normal! zo
12787
normal! zo
12820
normal! zo
12821
normal! zo
12824
normal! zo
12838
normal! zo
14788
normal! zo
15280
normal! zo
15309
normal! zo
15951
normal! zo
16000
normal! zo
16006
normal! zo
16007
normal! zo
16010
normal! zo
16323
normal! zo
16462
normal! zo
16471
normal! zo
16479
normal! zo
16480
normal! zo
16481
normal! zo
16502
normal! zo
16566
normal! zo
16566
normal! zo
16566
normal! zo
16764
normal! zo
16833
normal! zo
16847
normal! zo
16853
normal! zo
16856
normal! zo
16857
normal! zo
16872
normal! zo
16879
normal! zo
16880
normal! zo
16889
normal! zo
16900
normal! zo
16900
normal! zo
16900
normal! zo
16907
normal! zo
16907
normal! zo
16907
normal! zo
16955
normal! zo
16963
normal! zo
16968
normal! zo
17082
normal! zo
17103
normal! zo
17122
normal! zo
17130
normal! zo
17131
normal! zo
17140
normal! zo
17156
normal! zo
17166
normal! zo
17169
normal! zo
17378
normal! zo
17467
normal! zo
17481
normal! zo
17484
normal! zo
17488
normal! zo
17489
normal! zo
17749
normal! zo
17773
normal! zo
17778
normal! zo
17949
normal! zo
18019
normal! zo
18243
normal! zo
19104
normal! zo
19154
normal! zo
19333
normal! zo
19360
normal! zo
19370
normal! zo
19371
normal! zo
19371
normal! zo
19371
normal! zo
19371
normal! zo
19371
normal! zo
19371
normal! zo
19388
normal! zo
19434
normal! zo
19444
normal! zo
19445
normal! zo
19445
normal! zo
19445
normal! zo
19445
normal! zo
19445
normal! zo
19445
normal! zo
19910
normal! zo
20983
normal! zo
21553
normal! zo
21563
normal! zo
21612
normal! zo
21613
normal! zo
21613
normal! zo
let s:l = 582 - ((15 * winheight(0) + 12) / 25)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
582
normal! 050|
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
1815
normal! zo
1827
normal! zo
1830
normal! zo
1831
normal! zo
2958
normal! zo
2976
normal! zo
3039
normal! zo
3092
normal! zo
3109
normal! zo
3114
normal! zo
3114
normal! zo
3114
normal! zo
3114
normal! zo
3114
normal! zo
3117
normal! zo
3117
normal! zo
3122
normal! zo
3123
normal! zo
3125
normal! zo
3125
normal! zo
3125
normal! zo
3125
normal! zo
3127
normal! zo
3130
normal! zo
3130
normal! zo
3136
normal! zo
3142
normal! zo
3147
normal! zo
3154
normal! zo
3160
normal! zo
3166
normal! zo
3175
normal! zo
3217
normal! zo
3238
normal! zo
3240
normal! zo
3417
normal! zo
3429
normal! zo
3466
normal! zo
3474
normal! zo
3475
normal! zo
3476
normal! zo
3481
normal! zo
3482
normal! zo
3500
normal! zo
3500
normal! zo
3500
normal! zo
3520
normal! zo
3523
normal! zo
3523
normal! zo
3523
normal! zo
3523
normal! zo
3534
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
3539
normal! zo
3541
normal! zo
3541
normal! zo
3541
normal! zo
3541
normal! zo
3544
normal! zo
3545
normal! zo
3545
normal! zo
3545
normal! zo
3546
normal! zo
3549
normal! zo
3552
normal! zo
3556
normal! zo
3561
normal! zo
3562
normal! zo
3562
normal! zo
3566
normal! zo
3581
normal! zo
3638
normal! zo
3646
normal! zo
3648
normal! zo
3651
normal! zo
3653
normal! zo
3712
normal! zo
3720
normal! zo
3721
normal! zo
3731
normal! zo
3732
normal! zo
3736
normal! zo
3737
normal! zo
3754
normal! zo
3799
normal! zo
3799
normal! zo
3799
normal! zo
3806
normal! zo
3842
normal! zo
3864
normal! zo
3883
normal! zo
3884
normal! zo
3886
normal! zo
3891
normal! zo
3891
normal! zo
3891
normal! zo
3891
normal! zo
3891
normal! zo
3926
normal! zo
3951
normal! zo
3952
normal! zo
3956
normal! zo
3958
normal! zo
3958
normal! zo
3960
normal! zo
3960
normal! zo
3960
normal! zo
let s:l = 1835 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1835
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
let s:l = 217 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
217
normal! 025|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
5wincmd w
exe 'vert 1resize ' . ((&columns * 18 + 51) / 102)
exe '2resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 2resize ' . ((&columns * 83 + 51) / 102)
exe '3resize ' . ((&lines * 5 + 21) / 42)
exe 'vert 3resize ' . ((&columns * 83 + 51) / 102)
exe '4resize ' . ((&lines * 2 + 21) / 42)
exe 'vert 4resize ' . ((&columns * 83 + 51) / 102)
exe '5resize ' . ((&lines * 25 + 21) / 42)
exe 'vert 5resize ' . ((&columns * 83 + 51) / 102)
exe '6resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 6resize ' . ((&columns * 83 + 51) / 102)
exe '7resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 7resize ' . ((&columns * 83 + 51) / 102)
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
5wincmd w

" vim: ft=vim ro nowrap smc=128
