" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 19 julio 2013 at 15:11:20.
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
badd +1947 ginn/formularios/partes_de_fabricacion_bolsas.py
badd +121 ginn/formularios/partes_de_fabricacion_rollos.py
badd +550 ginn/formularios/proveedores.py
badd +547 ~/workspace/CICAN/src/formularios/menu.py
badd +105 ginn/formularios/launcher.py
badd +155 ginn/formularios/empleados.py
badd +38 ginn/formularios/resultados_geotextiles.py
badd +872 ginn/formularios/menu.py
badd +142 ginn/formularios/autenticacion.py
badd +11926 ginn/informes/geninformes.py
badd +233 ginn/informes/informe_certificado_calidad.py
badd +1518 informes/geninformes.py
badd +1 ginn/formularios/facturas_venta.py
badd +404 ginn/framework/configuracion.py
badd +4 bin/ginn.sh
badd +10 ginn/main.py
badd +21 ginn/formularios/ventana.py
badd +2286 ginn/formularios/pedidos_de_venta.py
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
badd +249 ginn/informes/norma2013.py
badd +65 ginn/formularios/widgets.py
badd +1 ginn/informes/ekotex.py
badd +7 ~/.vim/ftplugin/python.vim
badd +921 ginn/formularios/listado_balas.py
badd +254 ginn/formularios/consulta_pendientes_servir.py
badd +130 ginn/formularios/facturas_no_bloqueadas.py
args formularios/auditviewer.py
set lines=57 columns=111
edit ginn/formularios/facturas_venta.py
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
exe '2resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 2resize ' . ((&columns * 80 + 55) / 111)
exe '3resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 3resize ' . ((&columns * 80 + 55) / 111)
exe '4resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 4resize ' . ((&columns * 80 + 55) / 111)
exe '5resize ' . ((&lines * 39 + 28) / 57)
exe 'vert 5resize ' . ((&columns * 80 + 55) / 111)
exe '6resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 6resize ' . ((&columns * 80 + 55) / 111)
exe '7resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 7resize ' . ((&columns * 80 + 55) / 111)
exe '8resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 8resize ' . ((&columns * 80 + 55) / 111)
exe '9resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 9resize ' . ((&columns * 80 + 55) / 111)
exe '10resize ' . ((&lines * 1 + 28) / 57)
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
104
silent! normal zo
419
silent! normal zo
436
silent! normal zo
436
silent! normal zo
436
silent! normal zo
436
silent! normal zo
436
silent! normal zo
436
silent! normal zo
436
silent! normal zo
436
silent! normal zo
436
silent! normal zo
444
silent! normal zo
let s:l = 3289 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3289
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
silent! normal zo
768
silent! normal zo
778
silent! normal zo
1789
silent! normal zo
1801
silent! normal zo
1819
silent! normal zo
1828
silent! normal zo
1853
silent! normal zo
1858
silent! normal zo
1861
silent! normal zo
1862
silent! normal zo
1862
silent! normal zo
1862
silent! normal zo
1862
silent! normal zo
1873
silent! normal zo
1901
silent! normal zo
1919
silent! normal zo
1920
silent! normal zo
1928
silent! normal zo
1931
silent! normal zo
let s:l = 1935 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1935
normal! 024l
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
silent! normal zo
1213
silent! normal zo
3410
silent! normal zo
3410
silent! normal zo
3410
silent! normal zo
3410
silent! normal zo
3410
silent! normal zo
3410
silent! normal zo
3410
silent! normal zo
3423
silent! normal zo
3429
silent! normal zo
3433
silent! normal zo
3499
silent! normal zo
3499
silent! normal zo
3499
silent! normal zo
3499
silent! normal zo
3499
silent! normal zo
3499
silent! normal zo
3499
silent! normal zo
3499
silent! normal zo
3526
silent! normal zo
let s:l = 3538 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3538
normal! 023l
wincmd w
argglobal
edit ginn/formularios/utils.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
688
silent! normal zo
700
silent! normal zo
701
silent! normal zo
706
silent! normal zo
707
silent! normal zo
let s:l = 707 - ((22 * winheight(0) + 19) / 39)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
707
normal! 021l
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
5805
silent! normal zo
5961
silent! normal zo
5971
silent! normal zo
6104
silent! normal zo
6230
silent! normal zo
6245
silent! normal zo
6252
silent! normal zo
6252
silent! normal zo
6252
silent! normal zo
6252
silent! normal zo
6252
silent! normal zo
6252
silent! normal zo
6252
silent! normal zo
6252
silent! normal zo
6255
silent! normal zo
6255
silent! normal zo
6255
silent! normal zo
6255
silent! normal zo
6255
silent! normal zo
6255
silent! normal zo
6255
silent! normal zo
6255
silent! normal zo
6255
silent! normal zo
6275
silent! normal zo
6391
silent! normal zo
6399
silent! normal zo
6415
silent! normal zo
6446
silent! normal zo
6469
silent! normal zo
6476
silent! normal zo
6494
silent! normal zo
6501
silent! normal zo
6509
silent! normal zo
6536
silent! normal zo
6536
silent! normal zo
6536
silent! normal zo
6536
silent! normal zo
6536
silent! normal zo
6554
silent! normal zo
6560
silent! normal zo
6560
silent! normal zo
6579
silent! normal zo
6587
silent! normal zo
6587
silent! normal zo
6591
silent! normal zo
6595
silent! normal zo
6612
silent! normal zo
6613
silent! normal zo
6613
silent! normal zo
6619
silent! normal zo
6624
silent! normal zo
6645
silent! normal zo
6658
silent! normal zo
6677
silent! normal zo
6683
silent! normal zo
6687
silent! normal zo
6691
silent! normal zo
6706
silent! normal zo
6714
silent! normal zo
6726
silent! normal zo
6734
silent! normal zo
6740
silent! normal zo
6740
silent! normal zo
6740
silent! normal zo
6740
silent! normal zo
6740
silent! normal zo
6740
silent! normal zo
6740
silent! normal zo
6752
silent! normal zo
6758
silent! normal zo
6766
silent! normal zo
6779
silent! normal zo
6785
silent! normal zo
7539
silent! normal zo
8178
silent! normal zo
8178
silent! normal zo
8178
silent! normal zo
8178
silent! normal zo
8178
silent! normal zo
8178
silent! normal zo
8178
silent! normal zo
8206
silent! normal zo
8213
silent! normal zo
8220
silent! normal zo
9016
silent! normal zo
9376
silent! normal zo
10516
silent! normal zo
10698
silent! normal zo
10707
silent! normal zo
10726
silent! normal zo
10779
silent! normal zo
10794
silent! normal zo
10835
silent! normal zo
11418
silent! normal zo
11418
silent! normal zo
11418
silent! normal zo
11623
silent! normal zo
11623
silent! normal zo
11623
silent! normal zo
11623
silent! normal zo
11654
silent! normal zo
11657
silent! normal zo
11658
silent! normal zo
11666
silent! normal zo
11670
silent! normal zo
11671
silent! normal zo
12004
silent! normal zo
12004
silent! normal zo
12004
silent! normal zo
12004
silent! normal zo
12004
silent! normal zo
12040
silent! normal zo
12041
silent! normal zo
12042
silent! normal zo
12062
silent! normal zo
12088
silent! normal zo
12089
silent! normal zo
12183
silent! normal zo
12184
silent! normal zo
12223
silent! normal zo
12224
silent! normal zo
12302
silent! normal zo
12302
silent! normal zo
12302
silent! normal zo
12302
silent! normal zo
12302
silent! normal zo
12302
silent! normal zo
12302
silent! normal zo
12302
silent! normal zo
12314
silent! normal zo
12329
silent! normal zo
12331
silent! normal zo
12336
silent! normal zo
12341
silent! normal zo
12342
silent! normal zo
12342
silent! normal zo
12342
silent! normal zo
12377
silent! normal zo
12377
silent! normal zo
12416
silent! normal zo
12417
silent! normal zo
12418
silent! normal zo
12434
silent! normal zo
12478
silent! normal zo
12479
silent! normal zo
12539
silent! normal zo
12540
silent! normal zo
12600
silent! normal zo
12601
silent! normal zo
12741
silent! normal zo
12742
silent! normal zo
12743
silent! normal zo
12744
silent! normal zo
12744
silent! normal zo
12764
silent! normal zo
12765
silent! normal zo
12766
silent! normal zo
12766
silent! normal zo
12778
silent! normal zo
12779
silent! normal zo
12780
silent! normal zo
12780
silent! normal zo
12797
silent! normal zo
12798
silent! normal zo
12799
silent! normal zo
12800
silent! normal zo
12800
silent! normal zo
12821
silent! normal zo
12822
silent! normal zo
12823
silent! normal zo
12823
silent! normal zo
12835
silent! normal zo
12836
silent! normal zo
12837
silent! normal zo
12837
silent! normal zo
12913
silent! normal zo
12914
silent! normal zo
12915
silent! normal zo
12916
silent! normal zo
12916
silent! normal zo
12937
silent! normal zo
12938
silent! normal zo
12939
silent! normal zo
12939
silent! normal zo
12951
silent! normal zo
12952
silent! normal zo
12953
silent! normal zo
12953
silent! normal zo
12969
silent! normal zo
12970
silent! normal zo
12971
silent! normal zo
12972
silent! normal zo
12972
silent! normal zo
12993
silent! normal zo
12994
silent! normal zo
12995
silent! normal zo
12995
silent! normal zo
13007
silent! normal zo
13008
silent! normal zo
13009
silent! normal zo
13009
silent! normal zo
13093
silent! normal zo
13095
silent! normal zo
13096
silent! normal zo
13097
silent! normal zo
13097
silent! normal zo
13108
silent! normal zo
13109
silent! normal zo
13110
silent! normal zo
13110
silent! normal zo
13125
silent! normal zo
13126
silent! normal zo
13127
silent! normal zo
13128
silent! normal zo
13128
silent! normal zo
13139
silent! normal zo
13140
silent! normal zo
13141
silent! normal zo
13141
silent! normal zo
13762
silent! normal zo
13773
silent! normal zo
13784
silent! normal zo
13803
silent! normal zo
13854
silent! normal zo
13891
silent! normal zo
13892
silent! normal zo
14055
silent! normal zo
14097
silent! normal zo
14925
silent! normal zo
14929
silent! normal zo
14929
silent! normal zo
14929
silent! normal zo
14929
silent! normal zo
14929
silent! normal zo
14944
silent! normal zo
14963
silent! normal zo
14975
silent! normal zo
14978
silent! normal zo
14978
silent! normal zo
14978
silent! normal zo
14978
silent! normal zo
14986
silent! normal zo
15010
silent! normal zo
15018
silent! normal zo
15020
silent! normal zo
15033
silent! normal zo
15042
silent! normal zo
15053
silent! normal zo
15054
silent! normal zo
15063
silent! normal zo
15063
silent! normal zo
15070
silent! normal zo
15079
silent! normal zo
15083
silent! normal zo
15084
silent! normal zo
15096
silent! normal zo
15115
silent! normal zo
15137
silent! normal zo
15142
silent! normal zo
15143
silent! normal zo
15143
silent! normal zo
15146
silent! normal zo
15147
silent! normal zo
15147
silent! normal zo
15147
silent! normal zo
15150
silent! normal zo
15150
silent! normal zo
15150
silent! normal zo
15154
silent! normal zo
15154
silent! normal zo
15154
silent! normal zo
15154
silent! normal zo
15154
silent! normal zo
15154
silent! normal zo
15154
silent! normal zo
15154
silent! normal zo
15154
silent! normal zo
15159
silent! normal zo
15187
silent! normal zo
15207
silent! normal zo
15214
silent! normal zo
15217
silent! normal zo
15220
silent! normal zo
15239
silent! normal zo
15260
silent! normal zo
15278
silent! normal zo
15285
silent! normal zo
15299
silent! normal zo
15314
silent! normal zo
15333
silent! normal zo
15344
silent! normal zo
15356
silent! normal zo
15374
silent! normal zo
15384
silent! normal zo
15389
silent! normal zo
15389
silent! normal zo
15389
silent! normal zo
15389
silent! normal zo
15389
silent! normal zo
15389
silent! normal zo
15389
silent! normal zo
15389
silent! normal zo
15389
silent! normal zo
15389
silent! normal zo
15389
silent! normal zo
15391
silent! normal zo
15391
silent! normal zo
15391
silent! normal zo
15395
silent! normal zo
15396
silent! normal zo
15404
silent! normal zo
15418
silent! normal zo
15434
silent! normal zo
15443
silent! normal zo
15451
silent! normal zo
15454
silent! normal zo
15459
silent! normal zo
15473
silent! normal zo
15483
silent! normal zo
15487
silent! normal zo
15492
silent! normal zo
15498
silent! normal zo
15504
silent! normal zo
15504
silent! normal zo
15504
silent! normal zo
15506
silent! normal zo
15506
silent! normal zo
15506
silent! normal zo
15512
silent! normal zo
15516
silent! normal zo
15517
silent! normal zo
15517
silent! normal zo
15517
silent! normal zo
15517
silent! normal zo
15517
silent! normal zo
15517
silent! normal zo
15524
silent! normal zo
15525
silent! normal zo
15525
silent! normal zo
15537
silent! normal zo
15537
silent! normal zo
15537
silent! normal zo
15567
silent! normal zo
15568
silent! normal zo
15568
silent! normal zo
15568
silent! normal zo
15568
silent! normal zo
15568
silent! normal zo
15568
silent! normal zo
15570
silent! normal zo
15575
silent! normal zo
15581
silent! normal zo
15588
silent! normal zo
15589
silent! normal zo
15589
silent! normal zo
15592
silent! normal zo
15597
silent! normal zo
15603
silent! normal zo
15614
silent! normal zo
15631
silent! normal zo
15642
silent! normal zo
15643
silent! normal zo
15643
silent! normal zo
15645
silent! normal zo
15646
silent! normal zo
15646
silent! normal zo
15652
silent! normal zo
15653
silent! normal zo
15654
silent! normal zo
15655
silent! normal zo
15655
silent! normal zo
15655
silent! normal zo
15655
silent! normal zo
15661
silent! normal zo
15662
silent! normal zo
15663
silent! normal zo
15663
silent! normal zo
15663
silent! normal zo
15663
silent! normal zo
15670
silent! normal zo
15681
silent! normal zo
15688
silent! normal zo
15735
silent! normal zo
15794
silent! normal zo
15832
silent! normal zo
15847
silent! normal zo
15858
silent! normal zo
15858
silent! normal zo
17659
silent! normal zo
17666
silent! normal zo
17671
silent! normal zo
17671
silent! normal zo
17671
silent! normal zo
18360
silent! normal zo
18381
silent! normal zo
18543
silent! normal zo
18701
silent! normal zo
18744
silent! normal zo
19113
silent! normal zo
19201
silent! normal zo
19219
silent! normal zo
19580
silent! normal zo
19738
silent! normal zo
let s:l = 15860 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
15860
normal! 033l
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
silent! normal zo
122
silent! normal zo
134
silent! normal zo
134
silent! normal zo
134
silent! normal zo
174
silent! normal zo
189
silent! normal zo
218
silent! normal zo
254
silent! normal zo
264
silent! normal zo
285
silent! normal zo
286
silent! normal zo
288
silent! normal zo
288
silent! normal zo
288
silent! normal zo
288
silent! normal zo
291
silent! normal zo
293
silent! normal zo
295
silent! normal zo
295
silent! normal zo
321
silent! normal zo
321
normal zc
329
normal zc
337
silent! normal zo
339
silent! normal zo
342
silent! normal zo
344
silent! normal zo
349
normal zc
363
silent! normal zo
363
normal zc
403
silent! normal zo
405
silent! normal zo
403
normal zc
431
silent! normal zo
431
normal zc
470
silent! normal zo
470
normal zc
492
silent! normal zo
496
silent! normal zo
501
silent! normal zo
492
normal zc
630
silent! normal zo
638
silent! normal zo
641
silent! normal zo
654
silent! normal zo
657
silent! normal zo
658
silent! normal zo
661
silent! normal zo
664
silent! normal zo
665
silent! normal zo
668
silent! normal zo
671
silent! normal zo
672
silent! normal zo
672
silent! normal zo
672
silent! normal zo
672
silent! normal zo
672
silent! normal zo
672
silent! normal zo
676
silent! normal zo
677
silent! normal zo
677
silent! normal zo
677
silent! normal zo
677
silent! normal zo
677
silent! normal zo
677
silent! normal zo
682
silent! normal zo
683
silent! normal zo
692
silent! normal zo
703
silent! normal zo
706
silent! normal zo
709
silent! normal zo
712
silent! normal zo
715
silent! normal zo
718
silent! normal zo
723
silent! normal zo
726
silent! normal zo
727
silent! normal zo
760
silent! normal zo
896
silent! normal zo
900
silent! normal zo
902
silent! normal zo
906
silent! normal zo
910
silent! normal zo
911
silent! normal zo
911
silent! normal zo
924
silent! normal zo
926
silent! normal zo
929
silent! normal zo
933
silent! normal zo
937
silent! normal zo
938
silent! normal zo
938
silent! normal zo
1124
silent! normal zo
1158
silent! normal zo
1176
silent! normal zo
1185
silent! normal zo
1186
silent! normal zo
1186
silent! normal zo
1186
silent! normal zo
1194
silent! normal zo
1194
silent! normal zo
1194
silent! normal zo
1194
silent! normal zo
1194
silent! normal zo
1194
silent! normal zo
1194
silent! normal zo
1194
silent! normal zo
1210
silent! normal zo
1337
silent! normal zo
1366
silent! normal zo
1386
silent! normal zo
1471
silent! normal zo
1842
silent! normal zo
1900
silent! normal zo
1915
silent! normal zo
1956
silent! normal zo
2004
silent! normal zo
2005
silent! normal zo
2008
silent! normal zo
2263
silent! normal zo
2266
silent! normal zo
2273
silent! normal zo
2516
silent! normal zo
2524
silent! normal zo
2525
silent! normal zo
2546
silent! normal zo
2559
silent! normal zo
2560
silent! normal zo
2582
silent! normal zo
2651
silent! normal zo
2651
silent! normal zo
2651
silent! normal zo
2651
silent! normal zo
2656
silent! normal zo
2785
silent! normal zo
2805
silent! normal zo
2806
silent! normal zo
2806
silent! normal zo
2806
silent! normal zo
let s:l = 2293 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2293
normal! 036l
wincmd w
5wincmd w
exe 'vert 1resize ' . ((&columns * 30 + 55) / 111)
exe '2resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 2resize ' . ((&columns * 80 + 55) / 111)
exe '3resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 3resize ' . ((&columns * 80 + 55) / 111)
exe '4resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 4resize ' . ((&columns * 80 + 55) / 111)
exe '5resize ' . ((&lines * 39 + 28) / 57)
exe 'vert 5resize ' . ((&columns * 80 + 55) / 111)
exe '6resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 6resize ' . ((&columns * 80 + 55) / 111)
exe '7resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 7resize ' . ((&columns * 80 + 55) / 111)
exe '8resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 8resize ' . ((&columns * 80 + 55) / 111)
exe '9resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 9resize ' . ((&columns * 80 + 55) / 111)
exe '10resize ' . ((&lines * 1 + 28) / 57)
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
5wincmd w

" vim: ft=vim ro nowrap smc=128
