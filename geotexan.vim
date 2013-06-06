" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 05 junio 2013 at 12:02:38.
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
call setqflist([{'lnum': 0, 'col': 0, 'valid': 0, 'vcol': 0, 'nr': -1, 'type': '', 'pattern': '', 'filename': 'formularios/auditviewer.py', 'text': 'ginn/formularios/pedidos_de_compra.py:445:                    if self.usuario.nivel <= 1:'}, {'lnum': 0, 'col': 0, 'valid': 0, 'vcol': 0, 'nr': -1, 'type': '', 'pattern': '', 'filename': 'formularios/auditviewer.py', 'text': 'ginn/formularios/consumo_balas_partida.py:220:                if self.usuario.nivel <= 1:'}, {'lnum': 0, 'col': 0, 'valid': 0, 'vcol': 0, 'nr': -1, 'type': '', 'pattern': '', 'filename': 'formularios/auditviewer.py', 'text': 'ginn/formularios/facturas_venta.py:1443:                    condicion_modificacion or self.usuario.nivel <= 1)'}, {'lnum': 0, 'col': 0, 'valid': 0, 'vcol': 0, 'nr': -1, 'type': '', 'pattern': '', 'filename': 'formularios/auditviewer.py', 'text': 'ginn/formularios/facturas_venta.py:2595:                    condicion_modificacion = condicion_modificacion or self.usuario.nivel <= 1'}, {'lnum': 0, 'col': 0, 'valid': 0, 'vcol': 0, 'nr': -1, 'type': '', 'pattern': '', 'filename': 'formularios/auditviewer.py', 'text': 'ginn/formularios/contadores.py:87:        self.wids[''b_modificar''].set_sensitive(self.usuario == None or self.usuario.nivel <= 1)'}, {'lnum': 0, 'col': 0, 'valid': 0, 'vcol': 0, 'nr': -1, 'type': '', 'pattern': '', 'filename': 'formularios/auditviewer.py', 'text': 'ginn/formularios/ventana.py:917:                    if self.usuario.nivel <= 1:'}, {'lnum': 0, 'col': 0, 'valid': 0, 'vcol': 0, 'nr': -1, 'type': '', 'pattern': '', 'filename': 'formularios/auditviewer.py', 'text': 'ginn/formularios/productos_compra.py:288:            (not self.usuario) or (self.usuario.nivel <= 1))'}, {'lnum': 0, 'col': 0, 'valid': 0, 'vcol': 0, 'nr': -1, 'type': '', 'pattern': '', 'filename': 'formularios/auditviewer.py', 'text': 'ginn/formularios/facturas_compra.py:205:                    if self.usuario.nivel <= 1:'}, {'lnum': 0, 'col': 0, 'valid': 0, 'vcol': 0, 'nr': -1, 'type': '', 'pattern': '', 'filename': 'formularios/auditviewer.py', 'text': 'ginn/formularios/abonos_venta.py:193:            s = s and (self.usuario == None or self.usuario.nivel <= 1)'}, {'lnum': 0, 'col': 0, 'valid': 0, 'vcol': 0, 'nr': -1, 'type': '', 'pattern': '', 'filename': 'formularios/auditviewer.py', 'text': 'ginn/formularios/partes_de_fabricacion_rollos.py:779:        s = (s and ((self.usuario and self.usuario.nivel <= 1) '}, {'lnum': 0, 'col': 0, 'valid': 0, 'vcol': 0, 'nr': -1, 'type': '', 'pattern': '', 'filename': 'formularios/auditviewer.py', 'text': 'ginn/formularios/partes_de_fabricacion_rollos.py:2732:            # NEW!: Los partes bloqueados solo los pueden desbloquear usuarios con nivel <= 1.'}, {'lnum': 0, 'col': 0, 'valid': 0, 'vcol': 0, 'nr': -1, 'type': '', 'pattern': '', 'filename': 'formularios/auditviewer.py', 'text': 'ginn/formularios/partes_de_fabricacion_rollos.py:2734:                if self.usuario and self.usuario.nivel <= 1: # and self.objeto.bloqueado and not ch.get_active():'}, {'lnum': 0, 'col': 0, 'valid': 0, 'vcol': 0, 'nr': -1, 'type': '', 'pattern': '', 'filename': 'formularios/auditviewer.py', 'text': 'ginn/formularios/partes_de_fabricacion_balas.py:809:        s = s and ((self.usuario != None and self.usuario.nivel <= 1) or not self.objeto.bloqueado or self.usuario == None)'}, {'lnum': 0, 'col': 0, 'valid': 0, 'vcol': 0, 'nr': -1, 'type': '', 'pattern': '', 'filename': 'formularios/auditviewer.py', 'text': 'ginn/formularios/partes_de_fabricacion_balas.py:2976:            # NEW!: Los partes bloqueados solo los pueden desbloquear usuarios con nivel <= 1.'}, {'lnum': 0, 'col': 0, 'valid': 0, 'vcol': 0, 'nr': -1, 'type': '', 'pattern': '', 'filename': 'formularios/auditviewer.py', 'text': 'ginn/formularios/partes_de_fabricacion_balas.py:2978:                if self.usuario and self.usuario.nivel <= 1: # and self.objeto.bloqueado and not ch.get_active():'}, {'lnum': 0, 'col': 0, 'valid': 0, 'vcol': 0, 'nr': -1, 'type': '', 'pattern': '', 'filename': 'formularios/auditviewer.py', 'text': 'ginn/formularios/albaranes_de_salida.py:2841:        if ((self.usuario == None or self.usuario.nivel <= 1) '}, {'lnum': 0, 'col': 0, 'valid': 0, 'vcol': 0, 'nr': -1, 'type': '', 'pattern': '', 'filename': 'formularios/auditviewer.py', 'text': 'ginn/formularios/silos.py:107:            self.usuario == None or self.usuario.nivel <= 1)'}, {'lnum': 0, 'col': 0, 'valid': 0, 'vcol': 0, 'nr': -1, 'type': '', 'pattern': '', 'filename': 'formularios/auditviewer.py', 'text': 'ginn/formularios/prefacturas.py:1062:                condicion_modificacion = condicion_modificacion or self.usuario.nivel <= 1'}, {'lnum': 0, 'col': 0, 'valid': 0, 'vcol': 0, 'nr': -1, 'type': '', 'pattern': '', 'filename': 'formularios/auditviewer.py', 'text': 'ginn/formularios/prefacturas.py:1940:                    condicion_modificacion = condicion_modificacion or self.usuario.nivel <= 1'}, {'lnum': 0, 'col': 0, 'valid': 0, 'vcol': 0, 'nr': -1, 'type': '', 'pattern': '', 'filename': 'formularios/auditviewer.py', 'text': 'ginn/formularios/pedidos_de_venta.py:858:                    if self.usuario.nivel <= 1:'}, {'lnum': 0, 'col': 0, 'valid': 0, 'vcol': 0, 'nr': -1, 'type': '', 'pattern': '', 'filename': 'formularios/auditviewer.py', 'text': 'ginn/formularios/partes_de_fabricacion_bolsas.py:390:        s = s and ((self.usuario and self.usuario.nivel <= 1) '}, {'lnum': 0, 'col': 0, 'valid': 0, 'vcol': 0, 'nr': -1, 'type': '', 'pattern': '', 'filename': 'formularios/auditviewer.py', 'text': 'ginn/formularios/partes_de_fabricacion_bolsas.py:901:            and (not self.usuario or self.usuario.nivel <= 1)'}, {'lnum': 0, 'col': 0, 'valid': 0, 'vcol': 0, 'nr': -1, 'type': '', 'pattern': '', 'filename': 'formularios/auditviewer.py', 'text': 'ginn/formularios/partes_de_fabricacion_bolsas.py:1459:            if not self.usuario or self.usuario.nivel <= 1:'}, {'lnum': 0, 'col': 0, 'valid': 0, 'vcol': 0, 'nr': -1, 'type': '', 'pattern': '', 'filename': 'formularios/auditviewer.py', 'text': 'ginn/formularios/partes_de_fabricacion_bolsas.py:1518:            # usuarios con nivel <= 1.'}, {'lnum': 0, 'col': 0, 'valid': 0, 'vcol': 0, 'nr': -1, 'type': '', 'pattern': '', 'filename': 'formularios/auditviewer.py', 'text': 'ginn/formularios/partes_de_fabricacion_bolsas.py:1520:                if self.usuario and self.usuario.nivel <= 1: # and self.objeto.bloqueado and not ch.get_active():'}])
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
badd +107 ginn/framework/pclases.py
badd +43 ginn/formularios/historico_existencias_compra.py
badd +39 ginn/formularios/historico_existencias.py
badd +46 ginn/formularios/consulta_incidencias.py
badd +39 ginn/formularios/consulta_producido.py
badd +1 ginn/__init__.py
badd +1542 ginn/formularios/clientes.py
badd +444 ginn/formularios/productos_compra.py
badd +323 ginn/formularios/productos_de_venta_balas.py
badd +525 ginn/formularios/recibos.py
badd +2147 ginn/formularios/productos_de_venta_rollos.py
badd +643 ginn/formularios/productos_de_venta_rollos_geocompuestos.py
badd +305 ginn/formularios/productos_de_venta_especial.py
badd +3998 ginn/formularios/partes_de_fabricacion_balas.py
badd +1927 ginn/formularios/partes_de_fabricacion_bolsas.py
badd +961 ginn/formularios/partes_de_fabricacion_rollos.py
badd +669 ginn/formularios/proveedores.py
badd +547 ~/workspace/CICAN/src/formularios/menu.py
badd +1 ginn/formularios/launcher.py
badd +492 ginn/formularios/empleados.py
badd +38 ginn/formularios/resultados_geotextiles.py
badd +58 ginn/formularios/menu.py
badd +142 ginn/formularios/autenticacion.py
badd +1502 ginn/informes/geninformes.py
badd +233 ginn/informes/informe_certificado_calidad.py
badd +1518 informes/geninformes.py
badd +0 ginn/formularios/facturas_venta.py
args formularios/auditviewer.py
set lines=45 columns=80
edit ginn/formularios/facturas_venta.py
set splitbelow splitright
wincmd _ | wincmd |
split
wincmd _ | wincmd |
split
2wincmd k
wincmd w
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
exe '1resize ' . ((&lines * 15 + 22) / 45)
exe '2resize ' . ((&lines * 16 + 22) / 45)
exe '3resize ' . ((&lines * 10 + 22) / 45)
argglobal
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
105
silent! normal zo
363
silent! normal zo
let s:l = 378 - ((13 * winheight(0) + 7) / 15)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
378
normal! 022l
wincmd w
argglobal
edit ginn/formularios/menu.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
150
silent! normal zo
151
silent! normal zo
let s:l = 160 - ((7 * winheight(0) + 8) / 16)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
160
normal! 08l
wincmd w
argglobal
edit ginn/formularios/productos_compra.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 320 - ((4 * winheight(0) + 5) / 10)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
320
normal! 08l
wincmd w
2wincmd w
exe '1resize ' . ((&lines * 15 + 22) / 45)
exe '2resize ' . ((&lines * 16 + 22) / 45)
exe '3resize ' . ((&lines * 10 + 22) / 45)
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
