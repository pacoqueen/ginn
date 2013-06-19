" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 19 junio 2013 at 18:12:31.
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
badd +10 ginn/formularios/dynconsulta.py
badd +1 ginn/framework/pclases.py
badd +43 ginn/formularios/historico_existencias_compra.py
badd +39 ginn/formularios/historico_existencias.py
badd +46 ginn/formularios/consulta_incidencias.py
badd +39 ginn/formularios/consulta_producido.py
badd +1 ginn/__init__.py
badd +1542 ginn/formularios/clientes.py
badd +314 ginn/formularios/productos_compra.py
badd +323 ginn/formularios/productos_de_venta_balas.py
badd +525 ginn/formularios/recibos.py
badd +2147 ginn/formularios/productos_de_venta_rollos.py
badd +643 ginn/formularios/productos_de_venta_rollos_geocompuestos.py
badd +305 ginn/formularios/productos_de_venta_especial.py
badd +590 ginn/formularios/partes_de_fabricacion_balas.py
badd +1927 ginn/formularios/partes_de_fabricacion_bolsas.py
badd +2315 ginn/formularios/partes_de_fabricacion_rollos.py
badd +669 ginn/formularios/proveedores.py
badd +547 ~/workspace/CICAN/src/formularios/menu.py
badd +68 ginn/formularios/launcher.py
badd +492 ginn/formularios/empleados.py
badd +38 ginn/formularios/resultados_geotextiles.py
badd +854 ginn/formularios/menu.py
badd +142 ginn/formularios/autenticacion.py
badd +1246 ginn/informes/geninformes.py
badd +233 ginn/informes/informe_certificado_calidad.py
badd +1518 informes/geninformes.py
badd +371 ginn/formularios/facturas_venta.py
badd +468 ginn/framework/configuracion.py
badd +4 bin/ginn.sh
badd +10 ginn/main.py
badd +570 ginn/formularios/ventana.py
badd +2469 ginn/formularios/pedidos_de_venta.py
badd +867 db/tablas.sql
badd +2045 ginn/formularios/albaranes_de_salida.py
badd +1 ginn/formularios/presupuesto.py
badd +359 ginn/formularios/presupuestos.py
badd +412 ginn/informes/presupuesto2.py
badd +367 ginn/formularios/tarifas_de_precios.py
badd +381 ginn/formularios/logviewer.py
badd +2403 ginn/formularios/facturas_compra.py
badd +2658 ginn/formularios/utils.py
badd +648 ginn/formularios/resultados_fibra.py
badd +812 ginn/formularios/albaranes_de_entrada.py
badd +553 ginn/formularios/consulta_ventas.py
args formularios/auditviewer.py
set lines=70 columns=80
edit ginn/formularios/clientes.py
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
exe 'vert 1resize ' . ((&columns * 30 + 40) / 80)
exe '2resize ' . ((&lines * 33 + 35) / 70)
exe 'vert 2resize ' . ((&columns * 49 + 40) / 80)
exe '3resize ' . ((&lines * 26 + 35) / 70)
exe 'vert 3resize ' . ((&columns * 49 + 40) / 80)
exe '4resize ' . ((&lines * 1 + 35) / 70)
exe 'vert 4resize ' . ((&columns * 49 + 40) / 80)
exe '5resize ' . ((&lines * 1 + 35) / 70)
exe 'vert 5resize ' . ((&columns * 49 + 40) / 80)
exe '6resize ' . ((&lines * 1 + 35) / 70)
exe 'vert 6resize ' . ((&columns * 49 + 40) / 80)
exe '7resize ' . ((&lines * 1 + 35) / 70)
exe 'vert 7resize ' . ((&columns * 49 + 40) / 80)
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
66
normal! zo
1369
normal! zo
1510
normal! zo
1517
normal! zo
1518
normal! zo
1776
normal! zo
1895
normal! zo
let s:l = 1514 - ((15 * winheight(0) + 16) / 33)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1514
normal! 021|
wincmd w
argglobal
edit ginn/formularios/consulta_ventas.py
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
1187
normal! zo
1214
normal! zo
1228
normal! zo
1240
normal! zo
1242
normal! zo
1251
normal! zo
1252
normal! zo
let s:l = 1226 - ((16 * winheight(0) + 13) / 26)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1226
normal! 053|
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
265
normal! zo
411
normal! zo
420
normal! zo
583
normal! zo
589
normal! zo
1163
normal! zo
1172
normal! zo
1272
normal! zo
1281
normal! zo
1381
normal! zo
1390
normal! zo
1490
normal! zo
1499
normal! zo
2043
normal! zo
2219
normal! zo
2236
normal! zo
2240
normal! zo
2552
normal! zo
2593
normal! zo
2598
normal! zo
3132
normal! zo
3283
normal! zo
3780
normal! zo
4035
normal! zo
4692
normal! zo
4705
normal! zo
4709
normal! zo
4732
normal! zo
5285
normal! zo
6066
normal! zo
6229
normal! zo
6392
normal! zo
6652
normal! zo
6770
normal! zo
6939
normal! zo
6950
normal! zo
7432
normal! zo
7485
normal! zo
7609
normal! zo
7703
normal! zo
7704
normal! zo
7713
normal! zo
7725
normal! zo
7725
normal! zo
7725
normal! zo
7725
normal! zo
7725
normal! zo
7725
normal! zo
7726
normal! zo
7726
normal! zo
7726
normal! zo
7726
normal! zo
7728
normal! zo
7762
normal! zo
8250
normal! zo
8347
normal! zo
8635
normal! zo
8833
normal! zo
8868
normal! zo
8951
normal! zo
9645
normal! zo
9661
normal! zo
9685
normal! zo
9691
normal! zo
9692
normal! zo
9695
normal! zo
9703
normal! zo
9705
normal! zo
9718
normal! zo
9726
normal! zo
9729
normal! zo
9733
normal! zo
9834
normal! zo
9841
normal! zo
9932
normal! zo
9944
normal! zo
10126
normal! zo
10417
normal! zo
10803
normal! zo
10911
normal! zo
11170
normal! zo
11170
normal! zo
11265
normal! zo
11319
normal! zo
12622
normal! zo
13222
normal! zo
13238
normal! zo
13243
normal! zo
13244
normal! zo
13245
normal! zo
13245
normal! zo
13245
normal! zo
13245
normal! zo
13245
normal! zo
13245
normal! zo
13245
normal! zo
13245
normal! zo
13245
normal! zo
13245
normal! zo
13251
normal! zo
13255
normal! zo
13258
normal! zo
13258
normal! zo
13258
normal! zo
13258
normal! zo
13258
normal! zo
13258
normal! zo
13258
normal! zo
13258
normal! zo
13258
normal! zo
13672
normal! zo
13893
normal! zo
14670
normal! zo
14683
normal! zo
14709
normal! zo
15060
normal! zo
15129
normal! zo
15349
normal! zo
15358
normal! zo
15359
normal! zo
15570
normal! zo
15724
normal! zo
16129
normal! zo
16162
normal! zo
16167
normal! zo
16449
normal! zo
16544
normal! zo
16613
normal! zo
17146
normal! zo
17155
normal! zo
17447
normal! zo
17491
normal! zo
17506
normal! zo
17520
normal! zo
17526
normal! zo
19550
normal! zo
19689
normal! zo
19696
normal! zo
20390
normal! zo
20411
normal! zo
20573
normal! zo
20655
normal! zo
21139
normal! zo
21799
normal! zo
21903
normal! zo
21921
normal! zo
21925
normal! zo
21928
normal! zo
21930
normal! zo
21934
normal! zo
21940
normal! zo
21941
normal! zo
21944
normal! zo
22090
normal! zo
22095
normal! zo
22095
normal! zo
22108
normal! zo
22120
normal! zo
22130
normal! zo
22142
normal! zo
22142
normal! zo
22221
normal! zo
let s:l = 15077 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
15077
normal! 011|
wincmd w
argglobal
edit ginn/formularios/dynconsulta.py
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
114
normal! zo
114
normal! zo
132
normal! zo
132
normal! zo
157
normal! zo
215
normal! zo
let s:l = 270 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
270
normal! 019|
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
41
normal! zo
67
normal! zo
68
normal! zo
68
normal! zo
105
normal! zo
152
normal! zo
275
normal! zo
340
normal! zo
383
normal! zo
561
normal! zo
569
normal! zo
595
normal! zo
612
normal! zo
640
normal! zo
640
normal! zo
640
normal! zo
640
normal! zo
678
normal! zo
679
normal! zo
807
normal! zo
818
normal! zo
879
normal! zo
908
normal! zo
914
normal! zo
1039
normal! zo
let s:l = 157 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
157
normal! 013|
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
176
normal! zo
176
normal! zo
let s:l = 2727 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2727
normal! 05|
wincmd w
2wincmd w
exe 'vert 1resize ' . ((&columns * 30 + 40) / 80)
exe '2resize ' . ((&lines * 33 + 35) / 70)
exe 'vert 2resize ' . ((&columns * 49 + 40) / 80)
exe '3resize ' . ((&lines * 26 + 35) / 70)
exe 'vert 3resize ' . ((&columns * 49 + 40) / 80)
exe '4resize ' . ((&lines * 1 + 35) / 70)
exe 'vert 4resize ' . ((&columns * 49 + 40) / 80)
exe '5resize ' . ((&lines * 1 + 35) / 70)
exe 'vert 5resize ' . ((&columns * 49 + 40) / 80)
exe '6resize ' . ((&lines * 1 + 35) / 70)
exe 'vert 6resize ' . ((&columns * 49 + 40) / 80)
exe '7resize ' . ((&lines * 1 + 35) / 70)
exe 'vert 7resize ' . ((&columns * 49 + 40) / 80)
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
