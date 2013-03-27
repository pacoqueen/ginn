" ~/Geotexan/src/ginn/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 27 marzo 2013 at 17:56:02.
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
cd ~/Geotexan/src/ginn
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
badd +1 formularios/auditviewer.py
badd +113 formularios/consulta_existenciasBolsas.py
badd +1403 formularios/dynconsulta.py
args formularios/auditviewer.py
set lines=47 columns=80
edit -MiniBufExplorer-
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
exe '1resize ' . ((&lines * 1 + 23) / 47)
exe '2resize ' . ((&lines * 7 + 23) / 47)
exe '3resize ' . ((&lines * 35 + 23) / 47)
argglobal
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 1 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
wincmd w
argglobal
edit formularios/consulta_existenciasBolsas.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
54
silent! normal zo
55
silent! normal zo
65
silent! normal zo
65
silent! normal zo
65
silent! normal zo
65
silent! normal zo
65
silent! normal zo
55
silent! normal zo
54
silent! normal zo
let s:l = 242 - ((1 * winheight(0) + 3) / 7)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
242
normal! 04l
wincmd w
argglobal
edit formularios/auditviewer.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
54
silent! normal zo
58
silent! normal zo
68
silent! normal zo
68
silent! normal zo
68
silent! normal zo
68
silent! normal zo
68
silent! normal zo
77
silent! normal zo
58
silent! normal zo
54
silent! normal zo
104
silent! normal zo
104
silent! normal zo
104
silent! normal zo
128
silent! normal zo
133
silent! normal zo
135
silent! normal zo
137
silent! normal zo
137
silent! normal zo
137
silent! normal zo
137
silent! normal zo
137
silent! normal zo
137
silent! normal zo
137
silent! normal zo
137
silent! normal zo
137
silent! normal zo
137
silent! normal zo
137
silent! normal zo
137
silent! normal zo
137
silent! normal zo
137
silent! normal zo
137
silent! normal zo
137
silent! normal zo
137
silent! normal zo
137
silent! normal zo
137
silent! normal zo
128
silent! normal zo
141
silent! normal zo
142
silent! normal zo
144
silent! normal zo
146
silent! normal zo
142
silent! normal zo
141
silent! normal zo
104
silent! normal zo
147
silent! normal zo
147
silent! normal zo
147
silent! normal zo
148
silent! normal zo
150
silent! normal zo
147
silent! normal zo
147
silent! normal zo
164
silent! normal zo
169
silent! normal zo
171
silent! normal zo
171
silent! normal zo
164
silent! normal zo
217
silent! normal zo
217
silent! normal zo
236
silent! normal zo
236
silent! normal zo
300
silent! normal zo
308
silent! normal zo
309
silent! normal zo
309
silent! normal zo
308
silent! normal zo
300
silent! normal zo
147
silent! normal zo
321
silent! normal zo
322
silent! normal zo
323
silent! normal zo
325
silent! normal zo
327
silent! normal zo
328
silent! normal zo
328
silent! normal zo
328
silent! normal zo
328
silent! normal zo
328
silent! normal zo
327
silent! normal zo
330
silent! normal zo
332
silent! normal zo
333
silent! normal zo
333
silent! normal zo
333
silent! normal zo
332
silent! normal zo
337
silent! normal zo
338
silent! normal zo
339
silent! normal zo
337
silent! normal zo
341
silent! normal zo
342
silent! normal zo
341
silent! normal zo
345
silent! normal zo
322
silent! normal zo
321
silent! normal zo
let s:l = 337 - ((19 * winheight(0) + 17) / 35)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
337
normal! 042l
wincmd w
exe '1resize ' . ((&lines * 1 + 23) / 47)
exe '2resize ' . ((&lines * 7 + 23) / 47)
exe '3resize ' . ((&lines * 35 + 23) / 47)
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
