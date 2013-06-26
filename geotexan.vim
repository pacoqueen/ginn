" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 25 junio 2013 at 18:24:34.
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
badd +175 ~/.vimrc
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
badd +1197 ginn/framework/pclases.py
badd +201 ginn/formularios/historico_existencias_compra.py
badd +39 ginn/formularios/historico_existencias.py
badd +46 ginn/formularios/consulta_incidencias.py
badd +392 ginn/formularios/consulta_producido.py
badd +1 ginn/__init__.py
badd +2031 ginn/formularios/clientes.py
badd +314 ginn/formularios/productos_compra.py
badd +323 ginn/formularios/productos_de_venta_balas.py
badd +525 ginn/formularios/recibos.py
badd +2147 ginn/formularios/productos_de_venta_rollos.py
badd +643 ginn/formularios/productos_de_venta_rollos_geocompuestos.py
badd +305 ginn/formularios/productos_de_venta_especial.py
badd +1401 ginn/formularios/partes_de_fabricacion_balas.py
badd +1927 ginn/formularios/partes_de_fabricacion_bolsas.py
badd +117 ginn/formularios/partes_de_fabricacion_rollos.py
badd +669 ginn/formularios/proveedores.py
badd +547 ~/workspace/CICAN/src/formularios/menu.py
badd +109 ginn/formularios/launcher.py
badd +155 ginn/formularios/empleados.py
badd +38 ginn/formularios/resultados_geotextiles.py
badd +642 ginn/formularios/menu.py
badd +142 ginn/formularios/autenticacion.py
badd +7583 ginn/informes/geninformes.py
badd +233 ginn/informes/informe_certificado_calidad.py
badd +1518 informes/geninformes.py
badd +1 ginn/formularios/facturas_venta.py
badd +468 ginn/framework/configuracion.py
badd +4 bin/ginn.sh
badd +10 ginn/main.py
badd +602 ginn/formularios/ventana.py
badd +377 ginn/formularios/pedidos_de_venta.py
badd +3031 db/tablas.sql
badd +3581 ginn/formularios/albaranes_de_salida.py
badd +1 ginn/formularios/presupuesto.py
badd +359 ginn/formularios/presupuestos.py
badd +412 ginn/informes/presupuesto2.py
badd +367 ginn/formularios/tarifas_de_precios.py
badd +88 ginn/formularios/logviewer.py
badd +1359 ginn/formularios/facturas_compra.py
badd +2746 ginn/formularios/utils.py
badd +648 ginn/formularios/resultados_fibra.py
badd +812 ginn/formularios/albaranes_de_entrada.py
badd +1228 ginn/formularios/consulta_ventas.py
badd +37 ginn/formularios/__init__.py
badd +416 ginn/formularios/pagares_pagos.py
badd +509 ginn/formularios/ausencias.py
badd +67 ginn/formularios/partes_no_bloqueados.py
badd +1 ginn/formularios/gtkexcepthook.py
badd +0 ginn/framework/seeker.py
badd +0 ginn/formularios/crm_seguimiento_impagos.py
args formularios/auditviewer.py
set lines=58 columns=80
edit ginn/formularios/gtkexcepthook.py
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
exe '1resize ' . ((&lines * 1 + 29) / 58)
exe '2resize ' . ((&lines * 1 + 29) / 58)
exe '3resize ' . ((&lines * 1 + 29) / 58)
exe '4resize ' . ((&lines * 1 + 29) / 58)
exe '5resize ' . ((&lines * 44 + 29) / 58)
exe '6resize ' . ((&lines * 1 + 29) / 58)
exe '7resize ' . ((&lines * 1 + 29) / 58)
argglobal
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
155
silent! normal zo
169
silent! normal zo
let s:l = 266 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
266
normal! 019l
wincmd w
argglobal
edit ginn/framework/seeker.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
235
silent! normal zo
478
silent! normal zo
485
silent! normal zo
let s:l = 492 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
492
normal! 049l
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
560
silent! normal zo
568
silent! normal zo
583
silent! normal zo
594
silent! normal zo
613
silent! normal zo
641
silent! normal zo
679
silent! normal zo
680
silent! normal zo
808
silent! normal zo
819
silent! normal zo
let s:l = 31 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
31
normal! 0
wincmd w
argglobal
edit ginn/formularios/crm_seguimiento_impagos.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 13 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
13
normal! 041l
wincmd w
argglobal
edit ginn/framework/pclases.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
3132
silent! normal zo
3283
silent! normal zo
7485
silent! normal zo
7904
silent! normal zo
9647
silent! normal zo
9687
silent! normal zo
9693
silent! normal zo
9705
silent! normal zo
9715
silent! normal zo
9722
silent! normal zo
9737
silent! normal zo
10130
silent! normal zo
10138
silent! normal zo
13676
silent! normal zo
13882
silent! normal zo
13887
silent! normal zo
13891
silent! normal zo
14713
silent! normal zo
15064
silent! normal zo
15090
silent! normal zo
15099
silent! normal zo
15129
silent! normal zo
15295
silent! normal zo
15302
silent! normal zo
15303
silent! normal zo
15313
silent! normal zo
15315
silent! normal zo
15324
silent! normal zo
15326
silent! normal zo
15335
silent! normal zo
15340
silent! normal zo
15349
silent! normal zo
15351
silent! normal zo
15352
silent! normal zo
15490
silent! normal zo
15528
silent! normal zo
15540
silent! normal zo
15752
silent! normal zo
15987
silent! normal zo
16210
silent! normal zo
16477
silent! normal zo
16706
silent! normal zo
19239
silent! normal zo
21387
silent! normal zo
21473
silent! normal zo
let s:l = 15854 - ((22 * winheight(0) + 22) / 44)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
15854
normal! 034l
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
332
silent! normal zo
334
silent! normal zo
621
silent! normal zo
629
silent! normal zo
632
silent! normal zo
639
silent! normal zo
640
silent! normal zo
640
silent! normal zo
640
silent! normal zo
645
silent! normal zo
648
silent! normal zo
649
silent! normal zo
652
silent! normal zo
655
silent! normal zo
656
silent! normal zo
659
silent! normal zo
663
silent! normal zo
663
silent! normal zo
663
silent! normal zo
663
silent! normal zo
663
silent! normal zo
663
silent! normal zo
663
silent! normal zo
663
silent! normal zo
663
silent! normal zo
667
silent! normal zo
668
silent! normal zo
668
silent! normal zo
668
silent! normal zo
668
silent! normal zo
668
silent! normal zo
668
silent! normal zo
673
silent! normal zo
674
silent! normal zo
683
silent! normal zo
694
silent! normal zo
697
silent! normal zo
700
silent! normal zo
703
silent! normal zo
706
silent! normal zo
709
silent! normal zo
714
silent! normal zo
717
silent! normal zo
718
silent! normal zo
751
silent! normal zo
1114
silent! normal zo
1148
silent! normal zo
1166
silent! normal zo
1175
silent! normal zo
1176
silent! normal zo
1176
silent! normal zo
1176
silent! normal zo
1184
silent! normal zo
1184
silent! normal zo
1184
silent! normal zo
1184
silent! normal zo
1184
silent! normal zo
1184
silent! normal zo
1184
silent! normal zo
1184
silent! normal zo
1200
silent! normal zo
1324
silent! normal zo
1373
silent! normal zo
1829
silent! normal zo
1887
silent! normal zo
1902
silent! normal zo
1943
silent! normal zo
1991
silent! normal zo
1992
silent! normal zo
1995
silent! normal zo
2530
silent! normal zo
2543
silent! normal zo
2544
silent! normal zo
2566
silent! normal zo
2635
silent! normal zo
2640
silent! normal zo
2769
silent! normal zo
2789
silent! normal zo
2790
silent! normal zo
2790
silent! normal zo
2790
silent! normal zo
let s:l = 283 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
283
normal! 035l
wincmd w
argglobal
edit ginn/formularios/albaranes_de_salida.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
98
silent! normal zo
159
silent! normal zo
164
silent! normal zo
385
silent! normal zo
393
silent! normal zo
414
silent! normal zo
415
silent! normal zo
415
silent! normal zo
415
silent! normal zo
416
silent! normal zo
416
silent! normal zo
420
silent! normal zo
446
silent! normal zo
2012
silent! normal zo
2033
silent! normal zo
2034
silent! normal zo
2034
silent! normal zo
2034
silent! normal zo
2035
silent! normal zo
2035
silent! normal zo
2046
silent! normal zo
2051
silent! normal zo
2086
silent! normal zo
2089
silent! normal zo
2100
silent! normal zo
2100
silent! normal zo
2100
silent! normal zo
2111
silent! normal zo
2116
silent! normal zo
2116
silent! normal zo
2116
silent! normal zo
2128
silent! normal zo
2133
silent! normal zo
2133
silent! normal zo
2138
silent! normal zo
2142
silent! normal zo
2151
silent! normal zo
2208
silent! normal zo
2243
silent! normal zo
2255
silent! normal zo
2266
silent! normal zo
2268
silent! normal zo
2272
silent! normal zo
2274
silent! normal zo
2274
silent! normal zo
2275
silent! normal zo
2275
silent! normal zo
2282
silent! normal zo
2283
silent! normal zo
2310
silent! normal zo
2772
silent! normal zo
2861
silent! normal zo
2992
silent! normal zo
3285
silent! normal zo
3535
silent! normal zo
3536
silent! normal zo
3544
silent! normal zo
3545
silent! normal zo
3545
silent! normal zo
3545
silent! normal zo
3546
silent! normal zo
3546
silent! normal zo
3556
silent! normal zo
3570
silent! normal zo
3582
silent! normal zo
3825
silent! normal zo
let s:l = 3100 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3100
normal! 033l
wincmd w
5wincmd w
exe '1resize ' . ((&lines * 1 + 29) / 58)
exe '2resize ' . ((&lines * 1 + 29) / 58)
exe '3resize ' . ((&lines * 1 + 29) / 58)
exe '4resize ' . ((&lines * 1 + 29) / 58)
exe '5resize ' . ((&lines * 44 + 29) / 58)
exe '6resize ' . ((&lines * 1 + 29) / 58)
exe '7resize ' . ((&lines * 1 + 29) / 58)
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
