" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 17 julio 2013 at 20:31:36.
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
badd +1947 ginn/formularios/productos_de_venta_rollos.py
badd +507 ginn/formularios/productos_de_venta_rollos_geocompuestos.py
badd +578 ginn/formularios/productos_de_venta_especial.py
badd +1608 ginn/formularios/partes_de_fabricacion_balas.py
badd +12 ginn/formularios/partes_de_fabricacion_bolsas.py
badd +121 ginn/formularios/partes_de_fabricacion_rollos.py
badd +550 ginn/formularios/proveedores.py
badd +547 ~/workspace/CICAN/src/formularios/menu.py
badd +109 ginn/formularios/launcher.py
badd +155 ginn/formularios/empleados.py
badd +38 ginn/formularios/resultados_geotextiles.py
badd +770 ginn/formularios/menu.py
badd +142 ginn/formularios/autenticacion.py
badd +2919 ginn/informes/geninformes.py
badd +233 ginn/informes/informe_certificado_calidad.py
badd +1518 informes/geninformes.py
badd +1 ginn/formularios/facturas_venta.py
badd +498 ginn/framework/configuracion.py
badd +4 bin/ginn.sh
badd +10 ginn/main.py
badd +21 ginn/formularios/ventana.py
badd +2326 ginn/formularios/pedidos_de_venta.py
badd +1294 db/tablas.sql
badd +412 ginn/formularios/albaranes_de_salida.py
badd +1 ginn/formularios/presupuesto.py
badd +9 ginn/formularios/presupuestos.py
badd +382 ginn/informes/presupuesto2.py
badd +367 ginn/formularios/tarifas_de_precios.py
badd +88 ginn/formularios/logviewer.py
badd +724 ginn/formularios/facturas_compra.py
badd +1686 ginn/formularios/utils.py
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
badd +49 ginn/formularios/trazabilidad_articulos.py
badd +363 ginn/formularios/consulta_pagos.py
badd +611 ginn/formularios/consulta_vencimientos_pago.py
badd +64 ginn/formularios/trazabilidad.py
badd +15873 ginn/framework/pclases/__init__.py
badd +398 ginn/framework/pclases/superfacturaventa.py
badd +4 ginn/framework/pclases/facturaventa.py
badd +647 ginn/formularios/consulta_mensual_nominas.py
badd +269 ginn/informes/treeview2pdf.py
badd +129 ginn/formularios/balas_cable.py
badd +13 ginn/informes/nied.py
badd +1 ginn/informes/norma2013.py
badd +65 ginn/formularios/widgets.py
badd +1 ginn/informes/ekotex.py
badd +7 ~/.vim/ftplugin/python.vim
badd +1 ginn/formularios/listado_balas.py
badd +544 ginn/formularios/consulta_pendientes_servir.py
badd +52 ginn/formularios/facturacion_por_cliente_y_fechas.py
args formularios/auditviewer.py
set lines=78 columns=111
edit ginn/formularios/listado_balas.py
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
exe 'vert 1resize ' . ((&columns * 30 + 55) / 111)
exe '2resize ' . ((&lines * 7 + 39) / 78)
exe 'vert 2resize ' . ((&columns * 80 + 55) / 111)
exe '3resize ' . ((&lines * 7 + 39) / 78)
exe 'vert 3resize ' . ((&columns * 80 + 55) / 111)
exe '4resize ' . ((&lines * 7 + 39) / 78)
exe 'vert 4resize ' . ((&columns * 80 + 55) / 111)
exe '5resize ' . ((&lines * 7 + 39) / 78)
exe 'vert 5resize ' . ((&columns * 80 + 55) / 111)
exe '6resize ' . ((&lines * 6 + 39) / 78)
exe 'vert 6resize ' . ((&columns * 80 + 55) / 111)
exe '7resize ' . ((&lines * 7 + 39) / 78)
exe 'vert 7resize ' . ((&columns * 80 + 55) / 111)
exe '8resize ' . ((&lines * 6 + 39) / 78)
exe 'vert 8resize ' . ((&columns * 80 + 55) / 111)
exe '9resize ' . ((&lines * 7 + 39) / 78)
exe 'vert 9resize ' . ((&columns * 80 + 55) / 111)
exe '10resize ' . ((&lines * 6 + 39) / 78)
exe 'vert 10resize ' . ((&columns * 80 + 55) / 111)
exe '11resize ' . ((&lines * 7 + 39) / 78)
exe 'vert 11resize ' . ((&columns * 80 + 55) / 111)
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
53
normal! zo
54
normal! zo
62
normal! zo
62
normal! zo
99
normal! zo
108
normal! zo
124
normal! zo
150
normal! zo
156
normal! zo
165
normal! zo
167
normal! zo
585
normal! zo
593
normal! zo
863
normal! zo
887
normal! zo
let s:l = 141 - ((0 * winheight(0) + 3) / 7)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
141
normal! 021|
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
85
normal! zo
776
normal! zo
1852
normal! zo
1862
normal! zo
1880
normal! zo
1901
normal! zo
1915
normal! zo
let s:l = 1918 - ((0 * winheight(0) + 3) / 7)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1918
normal! 039|
wincmd w
argglobal
edit ginn/informes/norma2013.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
21
normal! zo
79
normal! zo
80
normal! zo
98
normal! zo
114
normal! zo
119
normal! zo
119
normal! zo
119
normal! zo
119
normal! zo
119
normal! zo
119
normal! zo
119
normal! zo
151
normal! zo
151
normal! zo
151
normal! zo
151
normal! zo
151
normal! zo
151
normal! zo
151
normal! zo
151
normal! zo
151
normal! zo
161
normal! zo
162
normal! zo
162
normal! zo
175
normal! zo
201
normal! zo
232
normal! zo
234
normal! zo
let s:l = 239 - ((6 * winheight(0) + 3) / 7)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
239
normal! 0
wincmd w
argglobal
edit ginn/informes/geninformes.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
11897
normal! zo
let s:l = 7938 - ((0 * winheight(0) + 3) / 7)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
7938
normal! 05|
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
408
normal! zo
498
normal! zo
1123
normal! zo
1196
normal! zo
1199
normal! zo
1199
normal! zo
1199
normal! zo
1202
normal! zo
1202
normal! zo
1202
normal! zo
1209
normal! zo
1261
normal! zo
1261
normal! zo
1261
normal! zo
1261
normal! zo
1261
normal! zo
1331
normal! zo
1385
normal! zo
1421
normal! zo
1943
normal! zo
2133
normal! zo
2331
normal! zo
2508
normal! zo
2566
normal! zo
3093
normal! zo
3408
normal! zo
3408
normal! zo
3408
normal! zo
3408
normal! zo
3408
normal! zo
3408
normal! zo
3408
normal! zo
3421
normal! zo
3427
normal! zo
3431
normal! zo
3450
normal! zo
3497
normal! zo
3497
normal! zo
3497
normal! zo
3497
normal! zo
3497
normal! zo
3497
normal! zo
3497
normal! zo
3497
normal! zo
3502
normal! zo
3509
normal! zo
3509
normal! zo
3509
normal! zo
3509
normal! zo
3509
normal! zo
3509
normal! zo
3509
normal! zo
3509
normal! zo
3524
normal! zo
3524
normal! zo
3524
normal! zo
3524
normal! zo
3524
normal! zo
3524
normal! zo
3524
normal! zo
3524
normal! zo
3524
normal! zo
3532
normal! zo
3532
normal! zo
3532
normal! zo
3532
normal! zo
3532
normal! zo
3532
normal! zo
3532
normal! zo
3532
normal! zo
3532
normal! zo
let s:l = 1293 - ((0 * winheight(0) + 3) / 6)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1293
normal! 026|
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
let s:l = 65 - ((1 * winheight(0) + 3) / 7)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
65
normal! 013|
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
6104
normal! zo
6230
normal! zo
6245
normal! zo
6252
normal! zo
6252
normal! zo
6252
normal! zo
6252
normal! zo
6252
normal! zo
6252
normal! zo
6252
normal! zo
6252
normal! zo
6255
normal! zo
6255
normal! zo
6255
normal! zo
6255
normal! zo
6255
normal! zo
6255
normal! zo
6255
normal! zo
6255
normal! zo
6255
normal! zo
6275
normal! zo
6399
normal! zo
6415
normal! zo
6446
normal! zo
6469
normal! zo
6476
normal! zo
6494
normal! zo
6501
normal! zo
6509
normal! zo
6536
normal! zo
6536
normal! zo
6536
normal! zo
6536
normal! zo
6536
normal! zo
6554
normal! zo
6560
normal! zo
6560
normal! zo
6579
normal! zo
6587
normal! zo
6587
normal! zo
6591
normal! zo
6595
normal! zo
6612
normal! zo
6613
normal! zo
6613
normal! zo
6619
normal! zo
6624
normal! zo
6645
normal! zo
6658
normal! zo
6677
normal! zo
6683
normal! zo
6687
normal! zo
6691
normal! zo
6706
normal! zo
6714
normal! zo
6726
normal! zo
6734
normal! zo
6740
normal! zo
6740
normal! zo
6740
normal! zo
6740
normal! zo
6740
normal! zo
6740
normal! zo
6740
normal! zo
6752
normal! zo
6758
normal! zo
6766
normal! zo
6779
normal! zo
6785
normal! zo
7539
normal! zo
8178
normal! zo
8178
normal! zo
8178
normal! zo
8178
normal! zo
8178
normal! zo
8178
normal! zo
8178
normal! zo
8206
normal! zo
8213
normal! zo
8220
normal! zo
10516
normal! zo
10698
normal! zo
10707
normal! zo
10726
normal! zo
10779
normal! zo
10794
normal! zo
10835
normal! zo
11418
normal! zo
11418
normal! zo
11418
normal! zo
11623
normal! zo
11623
normal! zo
11623
normal! zo
11623
normal! zo
11654
normal! zo
11657
normal! zo
11658
normal! zo
11666
normal! zo
11670
normal! zo
11671
normal! zo
12004
normal! zo
12004
normal! zo
12004
normal! zo
12004
normal! zo
12004
normal! zo
12040
normal! zo
12041
normal! zo
12042
normal! zo
12062
normal! zo
12088
normal! zo
12089
normal! zo
12183
normal! zo
12184
normal! zo
12223
normal! zo
12224
normal! zo
12377
normal! zo
12377
normal! zo
12416
normal! zo
12417
normal! zo
12418
normal! zo
12434
normal! zo
12478
normal! zo
12479
normal! zo
12539
normal! zo
12540
normal! zo
12600
normal! zo
12601
normal! zo
12741
normal! zo
12742
normal! zo
12743
normal! zo
12744
normal! zo
12744
normal! zo
12764
normal! zo
12765
normal! zo
12766
normal! zo
12766
normal! zo
12778
normal! zo
12779
normal! zo
12780
normal! zo
12780
normal! zo
12797
normal! zo
12798
normal! zo
12799
normal! zo
12800
normal! zo
12800
normal! zo
12821
normal! zo
12822
normal! zo
12823
normal! zo
12823
normal! zo
12835
normal! zo
12836
normal! zo
12837
normal! zo
12837
normal! zo
12913
normal! zo
12914
normal! zo
12915
normal! zo
12916
normal! zo
12916
normal! zo
12937
normal! zo
12938
normal! zo
12939
normal! zo
12939
normal! zo
12951
normal! zo
12952
normal! zo
12953
normal! zo
12953
normal! zo
12969
normal! zo
12970
normal! zo
12971
normal! zo
12972
normal! zo
12972
normal! zo
12993
normal! zo
12994
normal! zo
12995
normal! zo
12995
normal! zo
13007
normal! zo
13008
normal! zo
13009
normal! zo
13009
normal! zo
13093
normal! zo
13095
normal! zo
13096
normal! zo
13097
normal! zo
13097
normal! zo
13108
normal! zo
13109
normal! zo
13110
normal! zo
13110
normal! zo
13125
normal! zo
13126
normal! zo
13127
normal! zo
13128
normal! zo
13128
normal! zo
13139
normal! zo
13140
normal! zo
13141
normal! zo
13141
normal! zo
13762
normal! zo
13773
normal! zo
13784
normal! zo
13803
normal! zo
13854
normal! zo
13891
normal! zo
13892
normal! zo
14055
normal! zo
14097
normal! zo
14925
normal! zo
14929
normal! zo
14929
normal! zo
14929
normal! zo
14929
normal! zo
14929
normal! zo
14944
normal! zo
14963
normal! zo
14975
normal! zo
14978
normal! zo
14978
normal! zo
14978
normal! zo
14978
normal! zo
14986
normal! zo
15010
normal! zo
15018
normal! zo
15020
normal! zo
15033
normal! zo
15042
normal! zo
15053
normal! zo
15054
normal! zo
15063
normal! zo
15063
normal! zo
15070
normal! zo
15079
normal! zo
15083
normal! zo
15084
normal! zo
15096
normal! zo
15115
normal! zo
15137
normal! zo
15142
normal! zo
15143
normal! zo
15143
normal! zo
15146
normal! zo
15147
normal! zo
15147
normal! zo
15147
normal! zo
15150
normal! zo
15150
normal! zo
15150
normal! zo
15154
normal! zo
15154
normal! zo
15154
normal! zo
15154
normal! zo
15154
normal! zo
15154
normal! zo
15154
normal! zo
15154
normal! zo
15154
normal! zo
15159
normal! zo
15187
normal! zo
15207
normal! zo
15214
normal! zo
15217
normal! zo
15220
normal! zo
15239
normal! zo
15260
normal! zo
15278
normal! zo
15285
normal! zo
15299
normal! zo
15314
normal! zo
15333
normal! zo
15344
normal! zo
15356
normal! zo
15374
normal! zo
15384
normal! zo
15389
normal! zo
15389
normal! zo
15389
normal! zo
15389
normal! zo
15389
normal! zo
15389
normal! zo
15389
normal! zo
15389
normal! zo
15389
normal! zo
15389
normal! zo
15389
normal! zo
15391
normal! zo
15391
normal! zo
15391
normal! zo
15395
normal! zo
15396
normal! zo
15404
normal! zo
15418
normal! zo
15434
normal! zo
15443
normal! zo
15451
normal! zo
15454
normal! zo
15459
normal! zo
15473
normal! zo
15483
normal! zo
15487
normal! zo
15492
normal! zo
15498
normal! zo
15504
normal! zo
15504
normal! zo
15504
normal! zo
15506
normal! zo
15506
normal! zo
15506
normal! zo
15512
normal! zo
15516
normal! zo
15517
normal! zo
15517
normal! zo
15517
normal! zo
15517
normal! zo
15517
normal! zo
15517
normal! zo
15524
normal! zo
15525
normal! zo
15525
normal! zo
15537
normal! zo
15537
normal! zo
15537
normal! zo
15567
normal! zo
15568
normal! zo
15568
normal! zo
15568
normal! zo
15568
normal! zo
15568
normal! zo
15568
normal! zo
15570
normal! zo
15575
normal! zo
15581
normal! zo
15588
normal! zo
15589
normal! zo
15589
normal! zo
15592
normal! zo
15597
normal! zo
15603
normal! zo
15614
normal! zo
15631
normal! zo
15642
normal! zo
15643
normal! zo
15643
normal! zo
15645
normal! zo
15646
normal! zo
15646
normal! zo
15652
normal! zo
15653
normal! zo
15654
normal! zo
15655
normal! zo
15655
normal! zo
15655
normal! zo
15655
normal! zo
15661
normal! zo
15662
normal! zo
15663
normal! zo
15663
normal! zo
15663
normal! zo
15663
normal! zo
15670
normal! zo
15681
normal! zo
15688
normal! zo
17659
normal! zo
17666
normal! zo
17671
normal! zo
17671
normal! zo
17671
normal! zo
18360
normal! zo
18381
normal! zo
18543
normal! zo
18701
normal! zo
18744
normal! zo
19113
normal! zo
19201
normal! zo
19219
normal! zo
19580
normal! zo
19738
normal! zo
let s:l = 110 - ((0 * winheight(0) + 3) / 6)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
110
normal! 0
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
let s:l = 24 - ((0 * winheight(0) + 3) / 7)
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
let s:l = 82 - ((0 * winheight(0) + 3) / 6)
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
let s:l = 2329 - ((5 * winheight(0) + 3) / 7)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2329
normal! 011|
wincmd w
11wincmd w
exe 'vert 1resize ' . ((&columns * 30 + 55) / 111)
exe '2resize ' . ((&lines * 7 + 39) / 78)
exe 'vert 2resize ' . ((&columns * 80 + 55) / 111)
exe '3resize ' . ((&lines * 7 + 39) / 78)
exe 'vert 3resize ' . ((&columns * 80 + 55) / 111)
exe '4resize ' . ((&lines * 7 + 39) / 78)
exe 'vert 4resize ' . ((&columns * 80 + 55) / 111)
exe '5resize ' . ((&lines * 7 + 39) / 78)
exe 'vert 5resize ' . ((&columns * 80 + 55) / 111)
exe '6resize ' . ((&lines * 6 + 39) / 78)
exe 'vert 6resize ' . ((&columns * 80 + 55) / 111)
exe '7resize ' . ((&lines * 7 + 39) / 78)
exe 'vert 7resize ' . ((&columns * 80 + 55) / 111)
exe '8resize ' . ((&lines * 6 + 39) / 78)
exe 'vert 8resize ' . ((&columns * 80 + 55) / 111)
exe '9resize ' . ((&lines * 7 + 39) / 78)
exe 'vert 9resize ' . ((&columns * 80 + 55) / 111)
exe '10resize ' . ((&lines * 6 + 39) / 78)
exe 'vert 10resize ' . ((&columns * 80 + 55) / 111)
exe '11resize ' . ((&lines * 7 + 39) / 78)
exe 'vert 11resize ' . ((&columns * 80 + 55) / 111)
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
