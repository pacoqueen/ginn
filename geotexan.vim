" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 18 diciembre 2013 at 17:31:08.
" Open this file in Vim and run :source % to restore your session.

set guioptions=aegimrLtT
silent! set guifont=Inconsolata\ 10
if exists('g:syntax_on') != 1 | syntax on | endif
if exists('g:did_load_filetypes') != 1 | filetype on | endif
if exists('g:did_load_ftplugin') != 1 | filetype plugin on | endif
if exists('g:did_indent_on') != 1 | filetype indent on | endif
if &background != 'light'
	set background=light
endif
if !exists('g:colors_name') || g:colors_name != 'github' | colorscheme github | endif
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
badd +353 ginn/formularios/consulta_producido.py
badd +1 ginn/__init__.py
badd +266 ginn/formularios/clientes.py
badd +991 ginn/formularios/productos_compra.py
badd +39 ginn/formularios/productos_de_venta_balas.py
badd +525 ginn/formularios/recibos.py
badd +603 ginn/formularios/productos_de_venta_rollos.py
badd +382 ginn/formularios/productos_de_venta_rollos_geocompuestos.py
badd +417 ginn/formularios/productos_de_venta_especial.py
badd +3401 ginn/formularios/partes_de_fabricacion_balas.py
badd +901 ginn/formularios/partes_de_fabricacion_bolsas.py
badd +1706 ginn/formularios/partes_de_fabricacion_rollos.py
badd +446 ginn/formularios/proveedores.py
badd +547 ~/workspace/CICAN/src/formularios/menu.py
badd +117 ginn/formularios/launcher.py
badd +625 ginn/formularios/empleados.py
badd +38 ginn/formularios/resultados_geotextiles.py
badd +760 ginn/formularios/menu.py
badd +142 ginn/formularios/autenticacion.py
badd +3063 ginn/informes/geninformes.py
badd +233 ginn/informes/informe_certificado_calidad.py
badd +1518 informes/geninformes.py
badd +2322 ginn/formularios/facturas_venta.py
badd +419 ginn/framework/configuracion.py
badd +4 bin/ginn.sh
badd +10 ginn/main.py
badd +750 ginn/formularios/ventana.py
badd +363 ginn/formularios/pedidos_de_venta.py
badd +3876 db/tablas.sql
badd +2029 ginn/formularios/albaranes_de_salida.py
badd +227 ginn/formularios/presupuesto.py
badd +2876 ginn/formularios/presupuestos.py
badd +97 ginn/informes/carta_compromiso.py
badd +367 ginn/formularios/tarifas_de_precios.py
badd +88 ginn/formularios/logviewer.py
badd +238 ginn/formularios/facturas_compra.py
badd +1950 ginn/formularios/utils.py
badd +648 ginn/formularios/resultados_fibra.py
badd +955 ginn/formularios/albaranes_de_entrada.py
badd +751 ginn/formularios/consulta_ventas.py
badd +37 ginn/formularios/__init__.py
badd +907 ginn/formularios/pagares_pagos.py
badd +331 ginn/formularios/ausencias.py
badd +67 ginn/formularios/partes_no_bloqueados.py
badd +218 ginn/formularios/gtkexcepthook.py
badd +402 ginn/framework/seeker.py
badd +13 ginn/formularios/crm_seguimiento_impagos.py
badd +203 ginn/formularios/productos.py
badd +1064 ginn/formularios/trazabilidad_articulos.py
badd +363 ginn/formularios/consulta_pagos.py
badd +13 ginn/formularios/consulta_vencimientos_pago.py
badd +500 ginn/formularios/trazabilidad.py
badd +1 ginn/framework/pclases/__init__.py
badd +494 ginn/framework/pclases/superfacturaventa.py
badd +61 ginn/framework/pclases/facturaventa.py
badd +694 ginn/formularios/consulta_mensual_nominas.py
badd +88 ginn/informes/treeview2pdf.py
badd +129 ginn/formularios/balas_cable.py
badd +13 ginn/informes/nied.py
badd +82 ginn/informes/norma2013.py
badd +65 ginn/formularios/widgets.py
badd +1 ginn/informes/ekotex.py
badd +7 ~/.vim/ftplugin/python.vim
badd +140 ginn/formularios/listado_balas.py
badd +254 ginn/formularios/consulta_pendientes_servir.py
badd +130 ginn/formularios/facturas_no_bloqueadas.py
badd +221 ginn/formularios/consumo_balas_partida.py
badd +324 ginn/formularios/categorias_laborales.py
badd +411 ginn/formularios/nominas.py
badd +383 ginn/framework/pclases/cliente.py
badd +1 ginn/formularios/consulta_cobros.py
badd +1020 ginn/formularios/pagares_cobros.py
badd +24 extra/patches/calcular_credito_disponible.sql
badd +301 ginn/formularios/pclase2tv.py
badd +94 ginn/formularios/consulta_control_horas.py
badd +533 ginn/formularios/horas_trabajadas.py
badd +550 ginn/formularios/horas_trabajadas_dia.py
badd +1 ginn/formularios/pedidos_de_compra.glade
badd +523 ginn/formularios/postomatic.py
badd +36 ginn/formularios/custom_widgets/cellrendererautocomplete.py
badd +47 ginn/formularios/custom_widgets/__init__.py
badd +449 ginn/informes/presupuesto2.py
badd +61 ginn/informes/albaran_multipag.py
badd +192 ginn/formularios/silos.py
badd +1 ginn/framework/__init__.py
badd +1 ginn/formularios/vencimientos_pendientes_por_cliente.glade
badd +416 ginn/formularios/consulta_productividad.py
badd +212 ginn/formularios/mail_sender.py
badd +1143 ginn/formularios/abonos_venta.py
badd +306 ginn/formularios/ventana_progreso.py
badd +993 ginn/formularios/control_personal.py
badd +195 ginn/formularios/listado_rollos.py
badd +85 ginn/formularios/consulta_existenciasRollos.py
badd +91 ginn/formularios/listado_rollos_defectuosos.py
badd +3498 ginn/formularios/consulta_global.py
badd +195 ginn/formularios/rollos_c.py
badd +56 extra/scripts/enviar_exitencias_geotextiles_a_comerciales.py
badd +1 ginn/informes/presupuesto.py
badd +112 ginn/formularios/consulta_libro_iva.py
badd +298 ginn/formularios/consulta_ofertas.py
badd +24 extra/patches/create_ventana_consultas.py
badd +203 ginn/lib/ezodf/ezodf/const.py
badd +61 ginn/lib/ezodf/ezodf/xmlns.py
badd +21 ginn/lib/simple_odspy/simpleodspy/sodsods.py
badd +17 ginn/lib/simple_odspy/simpleodspy/sodsspreadsheet.py
badd +41 ginn/lib/simple_odspy/simpleodspy/sodstable.py
badd +66 ginn/lib/odfpy/contrib/odscell/odscell
badd +127 ginn/lib/odfpy/contrib/odscell/odscell.py
badd +76 ginn/formularios/consulta_ofertas_pendientes_validar.py
badd +392 ginn/formularios/consulta_ofertas_estudio.py
badd +1075 ginn/formularios/confirmings.py
badd +177 ginn/formularios/transferencias.py
badd +66 ginn/formularios/cuentas_destino.py
badd +509 ginn/formularios/facturacion_por_cliente_y_fechas.py
badd +1 ginn/formularios/presupuestos.glade
badd +24 ginn/lib/simple_odspy/simpleodspy/sodsxls.py
badd +1 ginn/formularios/ofer
badd +1 ginn/formularios/usuarios.glade
badd +251 ginn/formularios/usuarios.py
badd +7 ginn/lib/xlutils/xlutils/copy.py
badd +108 ginn/lib/xlutils/xlutils/filter.py
badd +10 ginn/lib/xlutils/xlutils/display.py
badd +8 ginn/lib/xlutils/xlutils/margins.py
badd +1 ginn/lib/xlutils/xlutils/filter.pyç
badd +381 ginn/lib/xlrd/xlrd/__init__.py
badd +9 ginn/lib/xlwt/xlwt/__init__.py
badd +659 ginn/lib/xlwt/xlwt/Workbook.py
args formularios/auditviewer.py
set lines=45 columns=102
edit ginn/framework/pclases/__init__.py
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
exe 'vert 1resize ' . ((&columns * 21 + 51) / 102)
exe '2resize ' . ((&lines * 6 + 22) / 45)
exe 'vert 2resize ' . ((&columns * 80 + 51) / 102)
exe '3resize ' . ((&lines * 17 + 22) / 45)
exe 'vert 3resize ' . ((&columns * 80 + 51) / 102)
exe '4resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 4resize ' . ((&columns * 80 + 51) / 102)
exe '5resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 5resize ' . ((&columns * 80 + 51) / 102)
exe '6resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 6resize ' . ((&columns * 80 + 51) / 102)
exe '7resize ' . ((&lines * 12 + 22) / 45)
exe 'vert 7resize ' . ((&columns * 80 + 51) / 102)
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
270
normal! zo
2450
normal! zo
3525
normal! zo
3833
normal! zo
3925
normal! zo
3932
normal! zo
3933
normal! zo
3933
normal! zo
3933
normal! zo
3933
normal! zo
3933
normal! zo
3933
normal! zo
4088
normal! zo
4155
normal! zo
4564
normal! zo
5840
normal! zo
6006
normal! zo
7521
normal! zo
7574
normal! zo
9051
normal! zo
9746
normal! zo
9786
normal! zo
9839
normal! zo
9842
normal! zo
9846
normal! zo
9846
normal! zo
9846
normal! zo
9862
normal! zo
9995
normal! zo
10235
normal! zo
10367
normal! zo
10516
normal! zo
10519
normal! zo
10522
normal! zo
10522
normal! zo
10522
normal! zo
10542
normal! zo
10579
normal! zo
10779
normal! zo
11034
normal! zo
11120
normal! zo
11937
normal! zo
11937
normal! zo
11937
normal! zo
13374
normal! zo
13374
normal! zo
13374
normal! zo
13389
normal! zo
13390
normal! zo
13544
normal! zo
13544
normal! zo
13544
normal! zo
13570
normal! zo
13571
normal! zo
13675
normal! zo
13675
normal! zo
13675
normal! zo
13691
normal! zo
13692
normal! zo
14322
normal! zo
15057
normal! zo
15661
normal! zo
16263
normal! zo
17016
normal! zo
17040
normal! zo
17045
normal! zo
17050
normal! zo
17057
normal! zo
17404
normal! zo
17550
normal! zo
19604
normal! zo
19616
normal! zo
19621
normal! zo
19927
normal! zo
let s:l = 10006 - ((0 * winheight(0) + 3) / 6)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
10006
normal! 035|
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
61
normal! zo
62
normal! zo
70
normal! zo
70
normal! zo
70
normal! zo
70
normal! zo
199
normal! zo
214
normal! zo
268
normal! zo
269
normal! zo
279
normal! zo
396
normal! zo
405
normal! zo
426
normal! zo
451
normal! zo
462
normal! zo
471
normal! zo
532
normal! zo
865
normal! zo
1058
normal! zo
1074
normal! zo
1090
normal! zo
1090
normal! zo
1090
normal! zo
1090
normal! zo
1090
normal! zo
1090
normal! zo
1184
normal! zo
1294
normal! zo
1446
normal! zo
2450
normal! zo
2535
normal! zo
2541
normal! zo
2568
normal! zo
2647
normal! zo
2673
normal! zo
2705
normal! zo
2705
normal! zo
2705
normal! zo
2784
normal! zo
2788
normal! zo
2789
normal! zo
2789
normal! zo
2789
normal! zo
2847
normal! zo
2861
normal! zo
2862
normal! zo
2868
normal! zo
2878
normal! zo
2866
normal! zo
2869
normal! zo
2870
normal! zo
2870
normal! zo
2870
normal! zo
2872
normal! zo
2877
normal! zo
2879
normal! zo
2879
normal! zo
2880
normal! zo
2880
normal! zo
2885
normal! zo
2886
normal! zo
2893
normal! zo
3152
normal! zo
3168
normal! zo
3168
normal! zo
3168
normal! zo
3168
normal! zo
3173
normal! zo
3174
normal! zo
3174
normal! zo
3174
normal! zo
3178
normal! zo
3179
normal! zo
3179
normal! zo
3183
normal! zo
3184
normal! zo
3184
normal! zo
3190
normal! zo
3190
normal! zo
3190
normal! zo
3234
normal! zo
3235
normal! zo
3247
normal! zo
3248
normal! zo
3251
normal! zo
3251
normal! zo
3252
normal! zo
3269
normal! zo
3273
normal! zo
3274
normal! zo
3274
normal! zo
3274
normal! zo
3282
normal! zo
3172
normal! zo
3173
normal! zo
3173
normal! zo
3173
normal! zo
3177
normal! zo
3178
normal! zo
3178
normal! zo
3182
normal! zo
3183
normal! zo
3183
normal! zo
3189
normal! zo
3189
normal! zo
3189
normal! zo
3233
normal! zo
3234
normal! zo
3246
normal! zo
3247
normal! zo
3250
normal! zo
3250
normal! zo
3251
normal! zo
3265
normal! zo
3265
normal! zo
3266
normal! zo
3266
normal! zo
3266
normal! zo
3273
normal! zo
3277
normal! zo
3278
normal! zo
3282
normal! zo
let s:l = 3100 - ((12 * winheight(0) + 8) / 17)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3100
normal! 043|
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/consulta_cobros.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
50
normal! zo
274
normal! zo
let s:l = 317 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
317
normal! 0264|
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/ventana.py
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
104
normal! zo
105
normal! zo
105
normal! zo
137
normal! zo
154
normal! zo
155
normal! zo
161
normal! zo
210
normal! zo
210
normal! zo
210
normal! zo
210
normal! zo
210
normal! zo
210
normal! zo
210
normal! zo
211
normal! zo
211
normal! zo
211
normal! zo
211
normal! zo
922
normal! zo
1068
normal! zo
let s:l = 926 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
926
normal! 020|
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/framework/configuracion.py
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
85
normal! zo
435
normal! zo
461
normal! zo
461
normal! zo
461
normal! zo
503
normal! zo
let s:l = 525 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
525
normal! 0
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/launcher.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
51
normal! zo
67
normal! zo
71
normal! zo
98
normal! zo
101
normal! zo
112
normal! zo
let s:l = 68 - ((0 * winheight(0) + 6) / 12)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
68
normal! 053|
wincmd w
3wincmd w
exe 'vert 1resize ' . ((&columns * 21 + 51) / 102)
exe '2resize ' . ((&lines * 6 + 22) / 45)
exe 'vert 2resize ' . ((&columns * 80 + 51) / 102)
exe '3resize ' . ((&lines * 17 + 22) / 45)
exe 'vert 3resize ' . ((&columns * 80 + 51) / 102)
exe '4resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 4resize ' . ((&columns * 80 + 51) / 102)
exe '5resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 5resize ' . ((&columns * 80 + 51) / 102)
exe '6resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 6resize ' . ((&columns * 80 + 51) / 102)
exe '7resize ' . ((&lines * 12 + 22) / 45)
exe 'vert 7resize ' . ((&columns * 80 + 51) / 102)
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
3wincmd w

" vim: ft=vim ro nowrap smc=128
