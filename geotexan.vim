" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 20 junio 2013 at 18:47:34.
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
badd +463 ginn/formularios/consulta_producido.py
badd +1 ginn/__init__.py
badd +631 ginn/formularios/clientes.py
badd +314 ginn/formularios/productos_compra.py
badd +323 ginn/formularios/productos_de_venta_balas.py
badd +525 ginn/formularios/recibos.py
badd +2147 ginn/formularios/productos_de_venta_rollos.py
badd +643 ginn/formularios/productos_de_venta_rollos_geocompuestos.py
badd +305 ginn/formularios/productos_de_venta_especial.py
badd +1401 ginn/formularios/partes_de_fabricacion_balas.py
badd +1927 ginn/formularios/partes_de_fabricacion_bolsas.py
badd +2315 ginn/formularios/partes_de_fabricacion_rollos.py
badd +669 ginn/formularios/proveedores.py
badd +547 ~/workspace/CICAN/src/formularios/menu.py
badd +68 ginn/formularios/launcher.py
badd +155 ginn/formularios/empleados.py
badd +38 ginn/formularios/resultados_geotextiles.py
badd +964 ginn/formularios/menu.py
badd +142 ginn/formularios/autenticacion.py
badd +1246 ginn/informes/geninformes.py
badd +233 ginn/informes/informe_certificado_calidad.py
badd +1518 informes/geninformes.py
badd +371 ginn/formularios/facturas_venta.py
badd +468 ginn/framework/configuracion.py
badd +4 bin/ginn.sh
badd +10 ginn/main.py
badd +664 ginn/formularios/ventana.py
badd +1047 ginn/formularios/pedidos_de_venta.py
badd +867 db/tablas.sql
badd +3585 ginn/formularios/albaranes_de_salida.py
badd +1 ginn/formularios/presupuesto.py
badd +359 ginn/formularios/presupuestos.py
badd +412 ginn/informes/presupuesto2.py
badd +367 ginn/formularios/tarifas_de_precios.py
badd +381 ginn/formularios/logviewer.py
badd +1359 ginn/formularios/facturas_compra.py
badd +2746 ginn/formularios/utils.py
badd +648 ginn/formularios/resultados_fibra.py
badd +812 ginn/formularios/albaranes_de_entrada.py
badd +1228 ginn/formularios/consulta_ventas.py
badd +37 ginn/formularios/__init__.py
badd +416 ginn/formularios/pagares_pagos.py
badd +0 ginn/formularios/ausencias.py
args formularios/auditviewer.py
set lines=58 columns=80
edit ginn/informes/geninformes.py
set splitbelow splitright
wincmd _ | wincmd |
split
1wincmd k
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
exe '1resize ' . ((&lines * 39 + 29) / 58)
exe '2resize ' . ((&lines * 16 + 29) / 58)
argglobal
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
152
silent! normal zo
159
silent! normal zo
166
silent! normal zo
7541
silent! normal zo
7548
silent! normal zo
8992
silent! normal zo
9833
silent! normal zo
let s:l = 7549 - ((17 * winheight(0) + 19) / 39)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
7549
normal! 031l
wincmd w
argglobal
edit ginn/formularios/ausencias.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
52
silent! normal zo
129
silent! normal zo
132
silent! normal zo
133
silent! normal zo
133
silent! normal zo
133
silent! normal zo
139
silent! normal zo
147
silent! normal zo
148
silent! normal zo
149
silent! normal zo
149
silent! normal zo
149
silent! normal zo
161
silent! normal zo
164
silent! normal zo
165
silent! normal zo
165
silent! normal zo
165
silent! normal zo
171
silent! normal zo
179
silent! normal zo
180
silent! normal zo
181
silent! normal zo
181
silent! normal zo
181
silent! normal zo
207
silent! normal zo
210
silent! normal zo
212
silent! normal zo
212
silent! normal zo
212
silent! normal zo
212
silent! normal zo
212
silent! normal zo
212
silent! normal zo
212
silent! normal zo
212
silent! normal zo
213
silent! normal zo
213
silent! normal zo
213
silent! normal zo
213
silent! normal zo
213
silent! normal zo
213
silent! normal zo
213
silent! normal zo
213
silent! normal zo
215
silent! normal zo
216
silent! normal zo
218
silent! normal zo
218
silent! normal zo
218
silent! normal zo
218
silent! normal zo
218
silent! normal zo
218
silent! normal zo
218
silent! normal zo
221
silent! normal zo
222
silent! normal zo
222
silent! normal zo
222
silent! normal zo
let s:l = 219 - ((9 * winheight(0) + 8) / 16)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
219
normal! 064l
wincmd w
exe '1resize ' . ((&lines * 39 + 29) / 58)
exe '2resize ' . ((&lines * 16 + 29) / 58)
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
1wincmd w

" vim: ft=vim ro nowrap smc=128
