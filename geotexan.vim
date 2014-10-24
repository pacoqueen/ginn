" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 24 octubre 2014 at 14:30:26.
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
badd +302 ginn/formularios/consulta_consumo.py
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
badd +1 ginn/lib/cairoplot/__init__.py
badd +1 ginn/lib/cagraph/cagraph/series/__init__.py
badd +84 ginn/lib/cagraph/cagraph/series/dna.py
badd +111 ginn/formularios/prefacturas.py
badd +11 ginn/formularios/pedidos_de_venta.py
badd +5 ginn/formularios/launcher.py
badd +1 ginn/formularios/abonos_venta.glade
badd +513 ginn/formularios/crm_detalles_factura.py
badd +406 ginn/formularios/crm_seguimiento_impagos.py
badd +1 extra/scripts/clouseau-gtk.py
badd +1 ginn/formularios/partes_de_fabricacion_rollos.py
badd +1 ginn/formularios/consulta_producciones_estandar.py
badd +606 ginn/formularios/consulta_pendientes_servir.py
badd +504 ginn/formularios/consulta_pagos_realizados.py
badd +21 ginn/lib/myprint.py
badd +399 ginn/formularios/auditviewer.py
badd +1 ginn/formularios/partes_de_fabricacion_bolsas.glade
badd +115 ginn/formularios/consulta_existenciasBolsas.py
badd +23 extra/scripts/bash_completion_ginn
badd +1200 ginn/formularios/consulta_ventas.py
badd +631 ginn/formularios/pagares_cobros.py
badd +217 ginn/framework/pclases/superfacturaventa.py
badd +812 ginn/formularios/ventana.py
badd +5 ginn/formularios/consulta_pagos.py
badd +2234 ginn/formularios/facturas_venta.py
badd +239 ginn/framework/pclases/facturaventa.py
badd +86 ginn/formularios/consulta_existencias.py
badd +1 ginn/framework/pclases/__init__.py
badd +1 ginn/formularios/partes_de_fabricacion_balas.py
badd +2204 ginn/formularios/albaranes_de_salida.py
badd +1 ginn/formularios/presupuestos.py
badd +174 ginn/formularios/mail_sender.py
badd +54 ginn/formularios/consulta_pedidos_clientes.py
badd +52 ginn/formularios/consulta_productividad.py
badd +1 ginn/formularios/mail_sender.glade
badd +1542 ginn/formularios/facturas_compra.py
badd +0 ginn/informes/presupuesto2.py
args formularios/auditviewer.py
set lines=42 columns=101
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
wincmd _ | wincmd |
split
6wincmd k
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
exe 'vert 1resize ' . ((&columns * 18 + 50) / 101)
exe '2resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 2resize ' . ((&columns * 82 + 50) / 101)
exe '3resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 3resize ' . ((&columns * 82 + 50) / 101)
exe '4resize ' . ((&lines * 28 + 21) / 42)
exe 'vert 4resize ' . ((&columns * 82 + 50) / 101)
exe '5resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 5resize ' . ((&columns * 82 + 50) / 101)
exe '6resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 6resize ' . ((&columns * 82 + 50) / 101)
exe '7resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 7resize ' . ((&columns * 82 + 50) / 101)
exe '8resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 8resize ' . ((&columns * 82 + 50) / 101)
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
let s:l = 22 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
22
normal! 011|
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
3317
normal! zo
3317
normal! zo
3317
normal! zo
3317
normal! zo
3317
normal! zo
3317
normal! zo
3328
normal! zo
3333
normal! zo
3358
normal! zo
3362
normal! zo
let s:l = 3383 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3383
normal! 026|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/informes/presupuesto2.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
324
normal! zo
348
normal! zo
349
normal! zo
416
normal! zo
416
normal! zo
416
normal! zo
416
normal! zo
416
normal! zo
601
normal! zo
604
normal! zo
let s:l = 350 - ((20 * winheight(0) + 14) / 28)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
350
normal! 0122|
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
75
normal! zo
253
normal! zo
354
normal! zo
655
normal! zo
657
normal! zo
658
normal! zo
659
normal! zo
819
normal! zo
828
normal! zo
830
normal! zo
950
normal! zo
969
normal! zo
977
normal! zo
1002
normal! zo
1006
normal! zo
1007
normal! zo
1244
normal! zo
1257
normal! zo
1258
normal! zo
1262
normal! zo
1276
normal! zo
2111
normal! zo
2123
normal! zo
2861
normal! zo
3582
normal! zo
3587
normal! zo
3593
normal! zo
3593
normal! zo
3593
normal! zo
3593
normal! zo
3593
normal! zo
3593
normal! zo
3593
normal! zo
3593
normal! zo
3593
normal! zo
3593
normal! zo
3593
normal! zo
let s:l = 3589 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3589
normal! 05|
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
112
normal! zo
312
normal! zo
667
normal! zo
1845
normal! zo
2526
normal! zo
2534
normal! zo
2539
normal! zo
2545
normal! zo
2552
normal! zo
2575
normal! zo
4176
normal! zo
let s:l = 529 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
529
normal! 017|
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
300
normal! zo
318
normal! zo
325
normal! zo
326
normal! zo
1694
normal! zo
1816
normal! zo
1858
normal! zo
1892
normal! zo
1919
normal! zo
1929
normal! zo
1929
normal! zo
1929
normal! zo
1929
normal! zo
1929
normal! zo
3954
normal! zo
3988
normal! zo
3990
normal! zo
4209
normal! zo
4692
normal! zo
4703
normal! zo
5251
normal! zo
5338
normal! zo
5360
normal! zo
5360
normal! zo
5360
normal! zo
5360
normal! zo
5360
normal! zo
5423
normal! zo
5431
normal! zo
5432
normal! zo
5435
normal! zo
5437
normal! zo
5458
normal! zo
5464
normal! zo
6467
normal! zo
6638
normal! zo
6661
normal! zo
9300
normal! zo
12345
normal! zo
13307
normal! zo
13346
normal! zo
13347
normal! zo
13348
normal! zo
13350
normal! zo
14812
normal! zo
15086
normal! zo
15128
normal! zo
15528
normal! zo
16788
normal! zo
16813
normal! zo
16829
normal! zo
16834
normal! zo
16834
normal! zo
16834
normal! zo
16835
normal! zo
16840
normal! zo
16903
normal! zo
16942
normal! zo
16949
normal! zo
16950
normal! zo
16998
normal! zo
17008
normal! zo
17092
normal! zo
17173
normal! zo
17192
normal! zo
17347
normal! zo
17360
normal! zo
17361
normal! zo
17362
normal! zo
17363
normal! zo
17368
normal! zo
17372
normal! zo
17374
normal! zo
17385
normal! zo
17448
normal! zo
17500
normal! zo
17607
normal! zo
17614
normal! zo
17619
normal! zo
17726
normal! zo
17783
normal! zo
17806
normal! zo
17815
normal! zo
17816
normal! zo
17816
normal! zo
17840
normal! zo
18040
normal! zo
18140
normal! zo
18228
normal! zo
18238
normal! zo
18258
normal! zo
18374
normal! zo
18595
normal! zo
18604
normal! zo
18605
normal! zo
18606
normal! zo
18608
normal! zo
18608
normal! zo
18608
normal! zo
18611
normal! zo
18613
normal! zo
18613
normal! zo
18613
normal! zo
18616
normal! zo
18617
normal! zo
18617
normal! zo
18617
normal! zo
18617
normal! zo
18617
normal! zo
let s:l = 338 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
338
normal! 09|
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
3282
normal! zo
3294
normal! zo
3310
normal! zo
3318
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
let s:l = 3324 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3324
normal! 067|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
4wincmd w
exe 'vert 1resize ' . ((&columns * 18 + 50) / 101)
exe '2resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 2resize ' . ((&columns * 82 + 50) / 101)
exe '3resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 3resize ' . ((&columns * 82 + 50) / 101)
exe '4resize ' . ((&lines * 28 + 21) / 42)
exe 'vert 4resize ' . ((&columns * 82 + 50) / 101)
exe '5resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 5resize ' . ((&columns * 82 + 50) / 101)
exe '6resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 6resize ' . ((&columns * 82 + 50) / 101)
exe '7resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 7resize ' . ((&columns * 82 + 50) / 101)
exe '8resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 8resize ' . ((&columns * 82 + 50) / 101)
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
4wincmd w

" vim: ft=vim ro nowrap smc=128
