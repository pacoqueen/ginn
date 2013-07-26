" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 26 julio 2013 at 14:49:14.
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
badd +1957 ginn/formularios/partes_de_fabricacion_bolsas.py
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
badd +2310 ginn/formularios/pedidos_de_venta.py
badd +3537 db/tablas.sql
badd +2229 ginn/formularios/albaranes_de_salida.py
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
badd +907 ginn/formularios/pagares_pagos.py
badd +509 ginn/formularios/ausencias.py
badd +67 ginn/formularios/partes_no_bloqueados.py
badd +46 ginn/formularios/gtkexcepthook.py
badd +512 ginn/framework/seeker.py
badd +13 ginn/formularios/crm_seguimiento_impagos.py
badd +203 ginn/formularios/productos.py
badd +1064 ginn/formularios/trazabilidad_articulos.py
badd +363 ginn/formularios/consulta_pagos.py
badd +13 ginn/formularios/consulta_vencimientos_pago.py
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
badd +221 ginn/formularios/consumo_balas_partida.py
badd +0 ginn/formularios/categorias_laborales.py
args formularios/auditviewer.py
set lines=44 columns=111
edit ginn/formularios/categorias_laborales.py
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
7wincmd k
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
exe '2resize ' . ((&lines * 28 + 22) / 44)
exe 'vert 2resize ' . ((&columns * 80 + 55) / 111)
exe '3resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 3resize ' . ((&columns * 80 + 55) / 111)
exe '4resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 4resize ' . ((&columns * 80 + 55) / 111)
exe '5resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 5resize ' . ((&columns * 80 + 55) / 111)
exe '6resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 6resize ' . ((&columns * 80 + 55) / 111)
exe '7resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 7resize ' . ((&columns * 80 + 55) / 111)
exe '8resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 8resize ' . ((&columns * 80 + 55) / 111)
exe '9resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 9resize ' . ((&columns * 80 + 55) / 111)
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
56
silent! normal zo
131
silent! normal zo
147
silent! normal zo
430
silent! normal zo
450
silent! normal zo
let s:l = 53 - ((12 * winheight(0) + 14) / 28)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
53
normal! 0445l
wincmd w
argglobal
edit ginn/formularios/empleados.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
58
silent! normal zo
59
silent! normal zo
66
silent! normal zo
66
silent! normal zo
329
silent! normal zo
let s:l = 616 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
616
normal! 0
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
551
silent! normal zo
564
silent! normal zo
587
silent! normal zo
587
silent! normal zo
587
silent! normal zo
587
silent! normal zo
587
silent! normal zo
587
silent! normal zo
621
silent! normal zo
1204
silent! normal zo
1217
silent! normal zo
3414
silent! normal zo
3414
silent! normal zo
3414
silent! normal zo
3414
silent! normal zo
3414
silent! normal zo
3414
silent! normal zo
3414
silent! normal zo
3427
silent! normal zo
3433
silent! normal zo
3437
silent! normal zo
3503
silent! normal zo
3503
silent! normal zo
3503
silent! normal zo
3503
silent! normal zo
3503
silent! normal zo
3503
silent! normal zo
3503
silent! normal zo
3503
silent! normal zo
3530
silent! normal zo
3530
silent! normal zo
3530
silent! normal zo
3530
silent! normal zo
3530
silent! normal zo
3530
silent! normal zo
3530
silent! normal zo
3530
silent! normal zo
3530
silent! normal zo
let s:l = 589 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
589
normal! 060l
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
silent! normal zo
75
silent! normal zo
82
silent! normal zo
88
silent! normal zo
104
silent! normal zo
105
silent! normal zo
105
silent! normal zo
let s:l = 140 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
140
normal! 020l
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
270
silent! normal zo
720
silent! normal zo
732
silent! normal zo
736
silent! normal zo
737
silent! normal zo
741
silent! normal zo
742
silent! normal zo
742
silent! normal zo
742
silent! normal zo
742
silent! normal zo
1077
silent! normal zo
1605
silent! normal zo
1625
silent! normal zo
1828
silent! normal zo
1878
silent! normal zo
1967
silent! normal zo
1977
silent! normal zo
2806
silent! normal zo
3106
silent! normal zo
3115
silent! normal zo
3806
silent! normal zo
3996
silent! normal zo
3996
silent! normal zo
4019
silent! normal zo
4046
silent! normal zo
4061
silent! normal zo
4270
silent! normal zo
4300
silent! normal zo
4762
silent! normal zo
4939
silent! normal zo
4953
silent! normal zo
4959
silent! normal zo
4975
silent! normal zo
4986
silent! normal zo
5090
silent! normal zo
5177
silent! normal zo
5807
silent! normal zo
5963
silent! normal zo
5973
silent! normal zo
6106
silent! normal zo
6232
silent! normal zo
6247
silent! normal zo
6254
silent! normal zo
6254
silent! normal zo
6254
silent! normal zo
6254
silent! normal zo
6254
silent! normal zo
6254
silent! normal zo
6254
silent! normal zo
6254
silent! normal zo
6257
silent! normal zo
6257
silent! normal zo
6257
silent! normal zo
6257
silent! normal zo
6257
silent! normal zo
6257
silent! normal zo
6257
silent! normal zo
6257
silent! normal zo
6257
silent! normal zo
6277
silent! normal zo
6393
silent! normal zo
6401
silent! normal zo
6417
silent! normal zo
6448
silent! normal zo
6471
silent! normal zo
6478
silent! normal zo
6496
silent! normal zo
6503
silent! normal zo
6511
silent! normal zo
6538
silent! normal zo
6538
silent! normal zo
6538
silent! normal zo
6538
silent! normal zo
6538
silent! normal zo
6556
silent! normal zo
6562
silent! normal zo
6562
silent! normal zo
6581
silent! normal zo
6589
silent! normal zo
6589
silent! normal zo
6593
silent! normal zo
6597
silent! normal zo
6614
silent! normal zo
6615
silent! normal zo
6615
silent! normal zo
6621
silent! normal zo
6626
silent! normal zo
6647
silent! normal zo
6660
silent! normal zo
6679
silent! normal zo
6685
silent! normal zo
6689
silent! normal zo
6693
silent! normal zo
6708
silent! normal zo
6716
silent! normal zo
6728
silent! normal zo
6736
silent! normal zo
6742
silent! normal zo
6742
silent! normal zo
6742
silent! normal zo
6742
silent! normal zo
6742
silent! normal zo
6742
silent! normal zo
6742
silent! normal zo
6754
silent! normal zo
6760
silent! normal zo
6768
silent! normal zo
6781
silent! normal zo
6787
silent! normal zo
7541
silent! normal zo
8180
silent! normal zo
8180
silent! normal zo
8180
silent! normal zo
8180
silent! normal zo
8180
silent! normal zo
8180
silent! normal zo
8180
silent! normal zo
8208
silent! normal zo
8215
silent! normal zo
8222
silent! normal zo
9018
silent! normal zo
9379
silent! normal zo
10519
silent! normal zo
10701
silent! normal zo
10710
silent! normal zo
10729
silent! normal zo
10782
silent! normal zo
10797
silent! normal zo
10838
silent! normal zo
11421
silent! normal zo
11421
silent! normal zo
11421
silent! normal zo
11626
silent! normal zo
11626
silent! normal zo
11626
silent! normal zo
11626
silent! normal zo
11657
silent! normal zo
11660
silent! normal zo
11661
silent! normal zo
11669
silent! normal zo
11673
silent! normal zo
11674
silent! normal zo
12007
silent! normal zo
12007
silent! normal zo
12007
silent! normal zo
12007
silent! normal zo
12007
silent! normal zo
12043
silent! normal zo
12044
silent! normal zo
12045
silent! normal zo
12065
silent! normal zo
12091
silent! normal zo
12092
silent! normal zo
12186
silent! normal zo
12187
silent! normal zo
12226
silent! normal zo
12227
silent! normal zo
12305
silent! normal zo
12305
silent! normal zo
12305
silent! normal zo
12305
silent! normal zo
12305
silent! normal zo
12305
silent! normal zo
12305
silent! normal zo
12305
silent! normal zo
12317
silent! normal zo
12332
silent! normal zo
12334
silent! normal zo
12339
silent! normal zo
12344
silent! normal zo
12345
silent! normal zo
12345
silent! normal zo
12345
silent! normal zo
12380
silent! normal zo
12380
silent! normal zo
12419
silent! normal zo
12420
silent! normal zo
12421
silent! normal zo
12437
silent! normal zo
12481
silent! normal zo
12482
silent! normal zo
12542
silent! normal zo
12543
silent! normal zo
12603
silent! normal zo
12604
silent! normal zo
12744
silent! normal zo
12745
silent! normal zo
12746
silent! normal zo
12747
silent! normal zo
12747
silent! normal zo
12767
silent! normal zo
12768
silent! normal zo
12769
silent! normal zo
12769
silent! normal zo
12781
silent! normal zo
12782
silent! normal zo
12783
silent! normal zo
12783
silent! normal zo
12800
silent! normal zo
12801
silent! normal zo
12802
silent! normal zo
12803
silent! normal zo
12803
silent! normal zo
12824
silent! normal zo
12825
silent! normal zo
12826
silent! normal zo
12826
silent! normal zo
12838
silent! normal zo
12839
silent! normal zo
12840
silent! normal zo
12840
silent! normal zo
12916
silent! normal zo
12917
silent! normal zo
12918
silent! normal zo
12919
silent! normal zo
12919
silent! normal zo
12940
silent! normal zo
12941
silent! normal zo
12942
silent! normal zo
12942
silent! normal zo
12954
silent! normal zo
12955
silent! normal zo
12956
silent! normal zo
12956
silent! normal zo
12972
silent! normal zo
12973
silent! normal zo
12974
silent! normal zo
12975
silent! normal zo
12975
silent! normal zo
12996
silent! normal zo
12997
silent! normal zo
12998
silent! normal zo
12998
silent! normal zo
13010
silent! normal zo
13011
silent! normal zo
13012
silent! normal zo
13012
silent! normal zo
13096
silent! normal zo
13098
silent! normal zo
13099
silent! normal zo
13100
silent! normal zo
13100
silent! normal zo
13111
silent! normal zo
13112
silent! normal zo
13113
silent! normal zo
13113
silent! normal zo
13128
silent! normal zo
13129
silent! normal zo
13130
silent! normal zo
13131
silent! normal zo
13131
silent! normal zo
13142
silent! normal zo
13143
silent! normal zo
13144
silent! normal zo
13144
silent! normal zo
13765
silent! normal zo
13776
silent! normal zo
13787
silent! normal zo
13806
silent! normal zo
13857
silent! normal zo
13894
silent! normal zo
13895
silent! normal zo
14058
silent! normal zo
14100
silent! normal zo
14928
silent! normal zo
14932
silent! normal zo
14932
silent! normal zo
14932
silent! normal zo
14932
silent! normal zo
14932
silent! normal zo
14947
silent! normal zo
14966
silent! normal zo
14978
silent! normal zo
14981
silent! normal zo
14981
silent! normal zo
14981
silent! normal zo
14981
silent! normal zo
14989
silent! normal zo
15013
silent! normal zo
15021
silent! normal zo
15023
silent! normal zo
15036
silent! normal zo
15045
silent! normal zo
15056
silent! normal zo
15057
silent! normal zo
15066
silent! normal zo
15066
silent! normal zo
15073
silent! normal zo
15082
silent! normal zo
15086
silent! normal zo
15087
silent! normal zo
15099
silent! normal zo
15118
silent! normal zo
15140
silent! normal zo
15145
silent! normal zo
15146
silent! normal zo
15146
silent! normal zo
15149
silent! normal zo
15150
silent! normal zo
15150
silent! normal zo
15150
silent! normal zo
15153
silent! normal zo
15153
silent! normal zo
15153
silent! normal zo
15157
silent! normal zo
15157
silent! normal zo
15157
silent! normal zo
15157
silent! normal zo
15157
silent! normal zo
15157
silent! normal zo
15157
silent! normal zo
15157
silent! normal zo
15157
silent! normal zo
15162
silent! normal zo
15190
silent! normal zo
15210
silent! normal zo
15217
silent! normal zo
15220
silent! normal zo
15223
silent! normal zo
15242
silent! normal zo
15263
silent! normal zo
15281
silent! normal zo
15288
silent! normal zo
15302
silent! normal zo
15317
silent! normal zo
15336
silent! normal zo
15347
silent! normal zo
15359
silent! normal zo
15377
silent! normal zo
15387
silent! normal zo
15392
silent! normal zo
15392
silent! normal zo
15392
silent! normal zo
15392
silent! normal zo
15392
silent! normal zo
15392
silent! normal zo
15392
silent! normal zo
15392
silent! normal zo
15392
silent! normal zo
15392
silent! normal zo
15392
silent! normal zo
15394
silent! normal zo
15394
silent! normal zo
15394
silent! normal zo
15398
silent! normal zo
15399
silent! normal zo
15407
silent! normal zo
15421
silent! normal zo
15437
silent! normal zo
15446
silent! normal zo
15454
silent! normal zo
15457
silent! normal zo
15462
silent! normal zo
15476
silent! normal zo
15486
silent! normal zo
15490
silent! normal zo
15495
silent! normal zo
15501
silent! normal zo
15507
silent! normal zo
15507
silent! normal zo
15507
silent! normal zo
15509
silent! normal zo
15509
silent! normal zo
15509
silent! normal zo
15515
silent! normal zo
15519
silent! normal zo
15520
silent! normal zo
15520
silent! normal zo
15520
silent! normal zo
15520
silent! normal zo
15520
silent! normal zo
15520
silent! normal zo
15527
silent! normal zo
15528
silent! normal zo
15528
silent! normal zo
15540
silent! normal zo
15540
silent! normal zo
15540
silent! normal zo
15570
silent! normal zo
15571
silent! normal zo
15571
silent! normal zo
15571
silent! normal zo
15571
silent! normal zo
15571
silent! normal zo
15571
silent! normal zo
15573
silent! normal zo
15578
silent! normal zo
15584
silent! normal zo
15591
silent! normal zo
15592
silent! normal zo
15592
silent! normal zo
15595
silent! normal zo
15600
silent! normal zo
15606
silent! normal zo
15617
silent! normal zo
15634
silent! normal zo
15645
silent! normal zo
15646
silent! normal zo
15646
silent! normal zo
15648
silent! normal zo
15649
silent! normal zo
15649
silent! normal zo
15655
silent! normal zo
15656
silent! normal zo
15657
silent! normal zo
15658
silent! normal zo
15658
silent! normal zo
15658
silent! normal zo
15658
silent! normal zo
15664
silent! normal zo
15665
silent! normal zo
15666
silent! normal zo
15666
silent! normal zo
15666
silent! normal zo
15666
silent! normal zo
15673
silent! normal zo
15684
silent! normal zo
15691
silent! normal zo
15738
silent! normal zo
15797
silent! normal zo
15835
silent! normal zo
15850
silent! normal zo
15861
silent! normal zo
15861
silent! normal zo
17662
silent! normal zo
17669
silent! normal zo
17674
silent! normal zo
17674
silent! normal zo
17674
silent! normal zo
18363
silent! normal zo
18384
silent! normal zo
18546
silent! normal zo
18704
silent! normal zo
18747
silent! normal zo
19116
silent! normal zo
19204
silent! normal zo
19222
silent! normal zo
19583
silent! normal zo
19741
silent! normal zo
let s:l = 441 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
441
normal! 04l
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
silent! normal zo
75
silent! normal zo
82
silent! normal zo
88
silent! normal zo
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
silent! normal zo
51
silent! normal zo
66
silent! normal zo
89
silent! normal zo
100
silent! normal zo
let s:l = 82 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
82
normal! 019l
wincmd w
argglobal
edit ginn/formularios/partes_de_fabricacion_rollos.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
229
silent! normal zo
230
silent! normal zo
262
silent! normal zo
262
silent! normal zo
339
silent! normal zo
340
silent! normal zo
345
silent! normal zo
350
silent! normal zo
351
silent! normal zo
356
silent! normal zo
362
silent! normal zo
467
silent! normal zo
579
silent! normal zo
595
silent! normal zo
725
silent! normal zo
734
silent! normal zo
834
silent! normal zo
850
silent! normal zo
850
silent! normal zo
850
silent! normal zo
850
silent! normal zo
961
silent! normal zo
966
silent! normal zo
1531
silent! normal zo
1727
silent! normal zo
1728
silent! normal zo
1728
silent! normal zo
1728
silent! normal zo
1728
silent! normal zo
1739
silent! normal zo
1740
silent! normal zo
1744
silent! normal zo
1744
silent! normal zo
1745
silent! normal zo
1752
silent! normal zo
1753
silent! normal zo
1804
silent! normal zo
3253
silent! normal zo
3260
silent! normal zo
3265
silent! normal zo
3272
silent! normal zo
3276
silent! normal zo
3281
silent! normal zo
3282
silent! normal zo
3282
silent! normal zo
3282
silent! normal zo
3288
silent! normal zo
3293
silent! normal zo
3294
silent! normal zo
3299
silent! normal zo
let s:l = 1750 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1750
normal! 060l
wincmd w
2wincmd w
exe 'vert 1resize ' . ((&columns * 30 + 55) / 111)
exe '2resize ' . ((&lines * 28 + 22) / 44)
exe 'vert 2resize ' . ((&columns * 80 + 55) / 111)
exe '3resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 3resize ' . ((&columns * 80 + 55) / 111)
exe '4resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 4resize ' . ((&columns * 80 + 55) / 111)
exe '5resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 5resize ' . ((&columns * 80 + 55) / 111)
exe '6resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 6resize ' . ((&columns * 80 + 55) / 111)
exe '7resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 7resize ' . ((&columns * 80 + 55) / 111)
exe '8resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 8resize ' . ((&columns * 80 + 55) / 111)
exe '9resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 9resize ' . ((&columns * 80 + 55) / 111)
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
