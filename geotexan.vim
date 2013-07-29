" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 29 julio 2013 at 14:51:06.
" Open this file in Vim and run :source % to restore your session.

set guioptions=aegimrLtT
silent! set guifont=Droid\ Sans\ Mono\ Slashed\ 10
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
badd +163 ~/.vimrc
badd +1 formularios/auditviewer.py
badd +13 ~/.vim/plugin/ack.vim
badd +249 formularios/consulta_existenciasBolsas.py
badd +1 formularios/dynconsulta.py
badd +1 framework/pclases.py
badd +168 formularios/gestor_mensajes.py
badd +181 formularios/menu.py
badd +85 formularios/autenticacion.py
badd +1 formularios/dynconsulta.glade
badd +179 formularios/consulta_facturas_sin_doc_pago.py
badd +73 formularios/utils_almacen.py
badd +1 ginn/formularios/dynconsulta.glade
badd +279 ginn/formularios/dynconsulta.py
badd +77 ginn/framework/pclases.py
badd +201 ginn/formularios/historico_existencias_compra.py
badd +39 ginn/formularios/historico_existencias.py
badd +46 ginn/formularios/consulta_incidencias.py
badd +392 ginn/formularios/consulta_producido.py
badd +1 ginn/__init__.py
badd +1247 ginn/formularios/clientes.py
badd +991 ginn/formularios/productos_compra.py
badd +310 ginn/formularios/productos_de_venta_balas.py
badd +525 ginn/formularios/recibos.py
badd +2258 ginn/formularios/productos_de_venta_rollos.py
badd +507 ginn/formularios/productos_de_venta_rollos_geocompuestos.py
badd +578 ginn/formularios/productos_de_venta_especial.py
badd +1608 ginn/formularios/partes_de_fabricacion_balas.py
badd +1947 ginn/formularios/partes_de_fabricacion_bolsas.py
badd +121 ginn/formularios/partes_de_fabricacion_rollos.py
badd +550 ginn/formularios/proveedores.py
badd +547 ~/workspace/CICAN/src/formularios/menu.py
badd +105 ginn/formularios/launcher.py
badd +155 ginn/formularios/empleados.py
badd +38 ginn/formularios/resultados_geotextiles.py
badd +230 ginn/formularios/menu.py
badd +142 ginn/formularios/autenticacion.py
badd +11926 ginn/informes/geninformes.py
badd +233 ginn/informes/informe_certificado_calidad.py
badd +1518 informes/geninformes.py
badd +443 ginn/formularios/facturas_venta.py
badd +404 ginn/framework/configuracion.py
badd +4 bin/ginn.sh
badd +10 ginn/main.py
badd +21 ginn/formularios/ventana.py
badd +663 ginn/formularios/pedidos_de_venta.py
badd +1294 db/tablas.sql
badd +2869 ginn/formularios/albaranes_de_salida.py
badd +1 ginn/formularios/presupuesto.py
badd +9 ginn/formularios/presupuestos.py
badd +382 ginn/informes/presupuesto2.py
badd +367 ginn/formularios/tarifas_de_precios.py
badd +88 ginn/formularios/logviewer.py
badd +724 ginn/formularios/facturas_compra.py
badd +4395 ginn/formularios/utils.py
badd +648 ginn/formularios/resultados_fibra.py
badd +812 ginn/formularios/albaranes_de_entrada.py
badd +1134 ginn/formularios/consulta_ventas.py
badd +37 ginn/formularios/__init__.py
badd +685 ginn/formularios/pagares_pagos.py
badd +509 ginn/formularios/ausencias.py
badd +67 ginn/formularios/partes_no_bloqueados.py
badd +46 ginn/formularios/gtkexcepthook.py
badd +512 ginn/framework/seeker.py
badd +13 ginn/formularios/crm_seguimiento_impagos.py
badd +203 ginn/formularios/productos.py
badd +1064 ginn/formularios/trazabilidad_articulos.py
badd +363 ginn/formularios/consulta_pagos.py
badd +611 ginn/formularios/consulta_vencimientos_pago.py
badd +500 ginn/formularios/trazabilidad.py
badd +9324 ginn/framework/pclases/__init__.py
badd +398 ginn/framework/pclases/superfacturaventa.py
badd +4 ginn/framework/pclases/facturaventa.py
badd +647 ginn/formularios/consulta_mensual_nominas.py
badd +269 ginn/informes/treeview2pdf.py
badd +129 ginn/formularios/balas_cable.py
badd +13 ginn/informes/nied.py
badd +249 ginn/informes/norma2013.py
badd +65 ginn/formularios/widgets.py
badd +1 ginn/informes/ekotex.py
badd +7 ~/.vim/ftplugin/python.vim
badd +921 ginn/formularios/listado_balas.py
badd +254 ginn/formularios/consulta_pendientes_servir.py
badd +130 ginn/formularios/facturas_no_bloqueadas.py
badd +1 ginn/formularios/consumo_balas_partida.py
badd +27 ginn/informes/albaran_porte.py
args formularios/auditviewer.py
set lines=66 columns=111
edit ginn/informes/geninformes.py
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
8wincmd k
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
exe 'vert 1resize ' . ((&columns * 30 + 55) / 111)
exe '2resize ' . ((&lines * 48 + 33) / 66)
exe 'vert 2resize ' . ((&columns * 80 + 55) / 111)
exe '3resize ' . ((&lines * 1 + 33) / 66)
exe 'vert 3resize ' . ((&columns * 80 + 55) / 111)
exe '4resize ' . ((&lines * 1 + 33) / 66)
exe 'vert 4resize ' . ((&columns * 80 + 55) / 111)
exe '5resize ' . ((&lines * 1 + 33) / 66)
exe 'vert 5resize ' . ((&columns * 80 + 55) / 111)
exe '6resize ' . ((&lines * 1 + 33) / 66)
exe 'vert 6resize ' . ((&columns * 80 + 55) / 111)
exe '7resize ' . ((&lines * 1 + 33) / 66)
exe 'vert 7resize ' . ((&columns * 80 + 55) / 111)
exe '8resize ' . ((&lines * 1 + 33) / 66)
exe 'vert 8resize ' . ((&columns * 80 + 55) / 111)
exe '9resize ' . ((&lines * 1 + 33) / 66)
exe 'vert 9resize ' . ((&columns * 80 + 55) / 111)
exe '10resize ' . ((&lines * 1 + 33) / 66)
exe 'vert 10resize ' . ((&columns * 80 + 55) / 111)
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
11273
normal! zo
11281
normal! zo
11429
normal! zo
11458
normal! zo
11460
normal! zo
let s:l = 11460 - ((45 * winheight(0) + 24) / 48)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
11460
normal! 067|
wincmd w
argglobal
edit ginn/formularios/consumo_balas_partida.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
346
normal! zo
let s:l = 633 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
633
normal! 0
wincmd w
argglobal
edit ginn/formularios/partes_de_fabricacion_bolsas.py
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
768
normal! zo
778
normal! zo
1789
normal! zo
1801
normal! zo
1819
normal! zo
1828
normal! zo
1853
normal! zo
1858
normal! zo
1861
normal! zo
1862
normal! zo
1862
normal! zo
1862
normal! zo
1862
normal! zo
1873
normal! zo
1901
normal! zo
1919
normal! zo
1920
normal! zo
1928
normal! zo
1931
normal! zo
let s:l = 1935 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1935
normal! 025|
wincmd w
argglobal
edit db/tablas.sql
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
1200
normal! zo
1213
normal! zo
3410
normal! zo
3410
normal! zo
3410
normal! zo
3410
normal! zo
3410
normal! zo
3410
normal! zo
3410
normal! zo
3423
normal! zo
3429
normal! zo
3433
normal! zo
3499
normal! zo
3499
normal! zo
3499
normal! zo
3499
normal! zo
3499
normal! zo
3499
normal! zo
3499
normal! zo
3499
normal! zo
3526
normal! zo
3526
normal! zo
3526
normal! zo
3526
normal! zo
3526
normal! zo
3526
normal! zo
3526
normal! zo
3526
normal! zo
3526
normal! zo
let s:l = 3538 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3538
normal! 024|
wincmd w
argglobal
edit ginn/formularios/ventana.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
66
normal! zo
75
normal! zo
82
normal! zo
88
normal! zo
104
normal! zo
105
normal! zo
105
normal! zo
let s:l = 140 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
140
normal! 021|
wincmd w
argglobal
edit ginn/framework/pclases/__init__.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
720
normal! zo
732
normal! zo
736
normal! zo
737
normal! zo
741
normal! zo
742
normal! zo
742
normal! zo
742
normal! zo
742
normal! zo
1077
normal! zo
1605
normal! zo
1625
normal! zo
1828
normal! zo
1878
normal! zo
1967
normal! zo
1977
normal! zo
2806
normal! zo
3106
normal! zo
3115
normal! zo
3806
normal! zo
3996
normal! zo
3996
normal! zo
4019
normal! zo
4046
normal! zo
4061
normal! zo
4270
normal! zo
4300
normal! zo
4762
normal! zo
4939
normal! zo
4953
normal! zo
4959
normal! zo
4975
normal! zo
4986
normal! zo
5090
normal! zo
5177
normal! zo
5807
normal! zo
5963
normal! zo
5973
normal! zo
6106
normal! zo
6232
normal! zo
6247
normal! zo
6254
normal! zo
6254
normal! zo
6254
normal! zo
6254
normal! zo
6254
normal! zo
6254
normal! zo
6254
normal! zo
6254
normal! zo
6257
normal! zo
6257
normal! zo
6257
normal! zo
6257
normal! zo
6257
normal! zo
6257
normal! zo
6257
normal! zo
6257
normal! zo
6257
normal! zo
6277
normal! zo
6393
normal! zo
6401
normal! zo
6417
normal! zo
6448
normal! zo
6471
normal! zo
6478
normal! zo
6496
normal! zo
6503
normal! zo
6511
normal! zo
6538
normal! zo
6538
normal! zo
6538
normal! zo
6538
normal! zo
6538
normal! zo
6556
normal! zo
6562
normal! zo
6562
normal! zo
6581
normal! zo
6589
normal! zo
6589
normal! zo
6593
normal! zo
6597
normal! zo
6614
normal! zo
6615
normal! zo
6615
normal! zo
6621
normal! zo
6626
normal! zo
6647
normal! zo
6660
normal! zo
6679
normal! zo
6685
normal! zo
6689
normal! zo
6693
normal! zo
6708
normal! zo
6716
normal! zo
6728
normal! zo
6736
normal! zo
6742
normal! zo
6742
normal! zo
6742
normal! zo
6742
normal! zo
6742
normal! zo
6742
normal! zo
6742
normal! zo
6754
normal! zo
6760
normal! zo
6768
normal! zo
6781
normal! zo
6787
normal! zo
7541
normal! zo
8180
normal! zo
8180
normal! zo
8180
normal! zo
8180
normal! zo
8180
normal! zo
8180
normal! zo
8180
normal! zo
8208
normal! zo
8215
normal! zo
8222
normal! zo
9018
normal! zo
9379
normal! zo
10519
normal! zo
10701
normal! zo
10710
normal! zo
10729
normal! zo
10782
normal! zo
10797
normal! zo
10838
normal! zo
11421
normal! zo
11421
normal! zo
11421
normal! zo
11626
normal! zo
11626
normal! zo
11626
normal! zo
11626
normal! zo
11657
normal! zo
11660
normal! zo
11661
normal! zo
11669
normal! zo
11673
normal! zo
11674
normal! zo
12007
normal! zo
12007
normal! zo
12007
normal! zo
12007
normal! zo
12007
normal! zo
12043
normal! zo
12044
normal! zo
12045
normal! zo
12065
normal! zo
12091
normal! zo
12092
normal! zo
12186
normal! zo
12187
normal! zo
12226
normal! zo
12227
normal! zo
12305
normal! zo
12305
normal! zo
12305
normal! zo
12305
normal! zo
12305
normal! zo
12305
normal! zo
12305
normal! zo
12305
normal! zo
12317
normal! zo
12332
normal! zo
12334
normal! zo
12339
normal! zo
12344
normal! zo
12345
normal! zo
12345
normal! zo
12345
normal! zo
12380
normal! zo
12380
normal! zo
12419
normal! zo
12420
normal! zo
12421
normal! zo
12437
normal! zo
12481
normal! zo
12482
normal! zo
12542
normal! zo
12543
normal! zo
12603
normal! zo
12604
normal! zo
12744
normal! zo
12745
normal! zo
12746
normal! zo
12747
normal! zo
12747
normal! zo
12767
normal! zo
12768
normal! zo
12769
normal! zo
12769
normal! zo
12781
normal! zo
12782
normal! zo
12783
normal! zo
12783
normal! zo
12800
normal! zo
12801
normal! zo
12802
normal! zo
12803
normal! zo
12803
normal! zo
12824
normal! zo
12825
normal! zo
12826
normal! zo
12826
normal! zo
12838
normal! zo
12839
normal! zo
12840
normal! zo
12840
normal! zo
12916
normal! zo
12917
normal! zo
12918
normal! zo
12919
normal! zo
12919
normal! zo
12940
normal! zo
12941
normal! zo
12942
normal! zo
12942
normal! zo
12954
normal! zo
12955
normal! zo
12956
normal! zo
12956
normal! zo
12972
normal! zo
12973
normal! zo
12974
normal! zo
12975
normal! zo
12975
normal! zo
12996
normal! zo
12997
normal! zo
12998
normal! zo
12998
normal! zo
13010
normal! zo
13011
normal! zo
13012
normal! zo
13012
normal! zo
13096
normal! zo
13098
normal! zo
13099
normal! zo
13100
normal! zo
13100
normal! zo
13111
normal! zo
13112
normal! zo
13113
normal! zo
13113
normal! zo
13128
normal! zo
13129
normal! zo
13130
normal! zo
13131
normal! zo
13131
normal! zo
13142
normal! zo
13143
normal! zo
13144
normal! zo
13144
normal! zo
13765
normal! zo
13776
normal! zo
13787
normal! zo
13806
normal! zo
13857
normal! zo
13894
normal! zo
13895
normal! zo
14058
normal! zo
14100
normal! zo
14928
normal! zo
14932
normal! zo
14932
normal! zo
14932
normal! zo
14932
normal! zo
14932
normal! zo
14947
normal! zo
14966
normal! zo
14978
normal! zo
14981
normal! zo
14981
normal! zo
14981
normal! zo
14981
normal! zo
14989
normal! zo
15013
normal! zo
15021
normal! zo
15023
normal! zo
15036
normal! zo
15045
normal! zo
15056
normal! zo
15057
normal! zo
15066
normal! zo
15066
normal! zo
15073
normal! zo
15082
normal! zo
15086
normal! zo
15087
normal! zo
15099
normal! zo
15118
normal! zo
15140
normal! zo
15145
normal! zo
15146
normal! zo
15146
normal! zo
15149
normal! zo
15150
normal! zo
15150
normal! zo
15150
normal! zo
15153
normal! zo
15153
normal! zo
15153
normal! zo
15157
normal! zo
15157
normal! zo
15157
normal! zo
15157
normal! zo
15157
normal! zo
15157
normal! zo
15157
normal! zo
15157
normal! zo
15157
normal! zo
15162
normal! zo
15190
normal! zo
15210
normal! zo
15217
normal! zo
15220
normal! zo
15223
normal! zo
15242
normal! zo
15263
normal! zo
15281
normal! zo
15288
normal! zo
15302
normal! zo
15317
normal! zo
15336
normal! zo
15347
normal! zo
15359
normal! zo
15377
normal! zo
15387
normal! zo
15392
normal! zo
15392
normal! zo
15392
normal! zo
15392
normal! zo
15392
normal! zo
15392
normal! zo
15392
normal! zo
15392
normal! zo
15392
normal! zo
15392
normal! zo
15392
normal! zo
15394
normal! zo
15394
normal! zo
15394
normal! zo
15398
normal! zo
15399
normal! zo
15407
normal! zo
15421
normal! zo
15437
normal! zo
15446
normal! zo
15454
normal! zo
15457
normal! zo
15462
normal! zo
15476
normal! zo
15486
normal! zo
15490
normal! zo
15495
normal! zo
15501
normal! zo
15507
normal! zo
15507
normal! zo
15507
normal! zo
15509
normal! zo
15509
normal! zo
15509
normal! zo
15515
normal! zo
15519
normal! zo
15520
normal! zo
15520
normal! zo
15520
normal! zo
15520
normal! zo
15520
normal! zo
15520
normal! zo
15527
normal! zo
15528
normal! zo
15528
normal! zo
15540
normal! zo
15540
normal! zo
15540
normal! zo
15570
normal! zo
15571
normal! zo
15571
normal! zo
15571
normal! zo
15571
normal! zo
15571
normal! zo
15571
normal! zo
15573
normal! zo
15578
normal! zo
15584
normal! zo
15591
normal! zo
15592
normal! zo
15592
normal! zo
15595
normal! zo
15600
normal! zo
15606
normal! zo
15617
normal! zo
15634
normal! zo
15645
normal! zo
15646
normal! zo
15646
normal! zo
15648
normal! zo
15649
normal! zo
15649
normal! zo
15655
normal! zo
15656
normal! zo
15657
normal! zo
15658
normal! zo
15658
normal! zo
15658
normal! zo
15658
normal! zo
15664
normal! zo
15665
normal! zo
15666
normal! zo
15666
normal! zo
15666
normal! zo
15666
normal! zo
15673
normal! zo
15684
normal! zo
15691
normal! zo
15738
normal! zo
15797
normal! zo
15835
normal! zo
15850
normal! zo
15861
normal! zo
15861
normal! zo
17662
normal! zo
17669
normal! zo
17674
normal! zo
17674
normal! zo
17674
normal! zo
18363
normal! zo
18384
normal! zo
18546
normal! zo
18704
normal! zo
18747
normal! zo
19116
normal! zo
19204
normal! zo
19222
normal! zo
19583
normal! zo
19741
normal! zo
let s:l = 5209 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
5209
normal! 022|
wincmd w
argglobal
edit ginn/formularios/ventana.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
66
normal! zo
75
normal! zo
82
normal! zo
88
normal! zo
let s:l = 24 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
24
normal! 0
wincmd w
argglobal
edit ginn/formularios/launcher.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
34
normal! zo
51
normal! zo
66
normal! zo
89
normal! zo
100
normal! zo
let s:l = 82 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
82
normal! 020|
wincmd w
argglobal
edit ginn/formularios/pedidos_de_venta.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
121
normal! zo
122
normal! zo
134
normal! zo
134
normal! zo
134
normal! zo
174
normal! zo
189
normal! zo
218
normal! zo
254
normal! zo
264
normal! zo
285
normal! zo
286
normal! zo
288
normal! zo
288
normal! zo
288
normal! zo
288
normal! zo
291
normal! zo
293
normal! zo
295
normal! zo
295
normal! zo
321
normal! zo
321
normal! zc
329
normal! zc
337
normal! zo
339
normal! zo
342
normal! zo
344
normal! zo
349
normal! zc
363
normal! zo
363
normal! zc
403
normal! zo
405
normal! zo
403
normal! zc
431
normal! zo
431
normal! zc
470
normal! zo
470
normal! zc
492
normal! zo
496
normal! zo
501
normal! zo
492
normal! zc
630
normal! zo
638
normal! zo
641
normal! zo
654
normal! zo
657
normal! zo
658
normal! zo
661
normal! zo
664
normal! zo
665
normal! zo
668
normal! zo
671
normal! zo
672
normal! zo
672
normal! zo
672
normal! zo
672
normal! zo
672
normal! zo
672
normal! zo
676
normal! zo
677
normal! zo
677
normal! zo
677
normal! zo
677
normal! zo
677
normal! zo
677
normal! zo
682
normal! zo
683
normal! zo
692
normal! zo
703
normal! zo
706
normal! zo
709
normal! zo
712
normal! zo
715
normal! zo
718
normal! zo
723
normal! zo
726
normal! zo
727
normal! zo
760
normal! zo
896
normal! zo
900
normal! zo
902
normal! zo
906
normal! zo
910
normal! zo
911
normal! zo
911
normal! zo
924
normal! zo
926
normal! zo
929
normal! zo
933
normal! zo
937
normal! zo
938
normal! zo
938
normal! zo
1124
normal! zo
1158
normal! zo
1176
normal! zo
1185
normal! zo
1186
normal! zo
1186
normal! zo
1186
normal! zo
1194
normal! zo
1194
normal! zo
1194
normal! zo
1194
normal! zo
1194
normal! zo
1194
normal! zo
1194
normal! zo
1194
normal! zo
1210
normal! zo
1337
normal! zo
1366
normal! zo
1386
normal! zo
1471
normal! zo
1842
normal! zo
1900
normal! zo
1915
normal! zo
1956
normal! zo
2004
normal! zo
2005
normal! zo
2008
normal! zo
2263
normal! zo
2266
normal! zo
2273
normal! zo
2516
normal! zo
2524
normal! zo
2525
normal! zo
2546
normal! zo
2559
normal! zo
2560
normal! zo
2582
normal! zo
2651
normal! zo
2651
normal! zo
2651
normal! zo
2651
normal! zo
2656
normal! zo
2785
normal! zo
2805
normal! zo
2806
normal! zo
2806
normal! zo
2806
normal! zo
let s:l = 2293 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2293
normal! 037|
wincmd w
2wincmd w
exe 'vert 1resize ' . ((&columns * 30 + 55) / 111)
exe '2resize ' . ((&lines * 48 + 33) / 66)
exe 'vert 2resize ' . ((&columns * 80 + 55) / 111)
exe '3resize ' . ((&lines * 1 + 33) / 66)
exe 'vert 3resize ' . ((&columns * 80 + 55) / 111)
exe '4resize ' . ((&lines * 1 + 33) / 66)
exe 'vert 4resize ' . ((&columns * 80 + 55) / 111)
exe '5resize ' . ((&lines * 1 + 33) / 66)
exe 'vert 5resize ' . ((&columns * 80 + 55) / 111)
exe '6resize ' . ((&lines * 1 + 33) / 66)
exe 'vert 6resize ' . ((&columns * 80 + 55) / 111)
exe '7resize ' . ((&lines * 1 + 33) / 66)
exe 'vert 7resize ' . ((&columns * 80 + 55) / 111)
exe '8resize ' . ((&lines * 1 + 33) / 66)
exe 'vert 8resize ' . ((&columns * 80 + 55) / 111)
exe '9resize ' . ((&lines * 1 + 33) / 66)
exe 'vert 9resize ' . ((&columns * 80 + 55) / 111)
exe '10resize ' . ((&lines * 1 + 33) / 66)
exe 'vert 10resize ' . ((&columns * 80 + 55) / 111)
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
2wincmd w

" vim: ft=vim ro nowrap smc=128
