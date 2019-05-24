" ~/Geotexan/src/Geotex-INN/geotexan.vim:
" Vim session script.
" Created by session.vim 2.13.1 on 24 mayo 2019 at 15:56:02.
" Open this file in Vim and run :source % to restore your session.

set guioptions=aegimrLtT
silent! set guifont=Menlo\ For\ Powerline
if exists('g:syntax_on') != 1 | syntax on | endif
if exists('g:did_load_filetypes') != 1 | filetype on | endif
if exists('g:did_load_ftplugin') != 1 | filetype plugin on | endif
if exists('g:did_indent_on') != 1 | filetype indent on | endif
if &background != 'light'
	set background=light
endif
if !exists('g:colors_name') || g:colors_name != 'summerfruit256' | colorscheme summerfruit256 | endif
call setqflist([{'lnum': 1612, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/tests/ramanujan.py', 'text': 'E501: line too long (134 > 79 characters)'}, {'lnum': 54, 'col': 14, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E261: at least two spaces before inline comment'}, {'lnum': 80, 'col': 52, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E261: at least two spaces before inline comment'}, {'lnum': 121, 'col': 25, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E128: continuation line under-indented for visual indent'}, {'lnum': 151, 'col': 39, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E711: comparison to None should be ''if cond is not None:'''}, {'lnum': 159, 'col': 13, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E265: block comment should start with ''# '''}, {'lnum': 160, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E501: line too long (86 > 79 characters)'}, {'lnum': 161, 'col': 13, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E265: block comment should start with ''# '''}, {'lnum': 184, 'col': 23, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E127: continuation line over-indented for visual indent'}, {'lnum': 187, 'col': 25, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E128: continuation line under-indented for visual indent'}, {'lnum': 188, 'col': 25, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E128: continuation line under-indented for visual indent'}, {'lnum': 189, 'col': 25, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E128: continuation line under-indented for visual indent'}, {'lnum': 198, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E501: line too long (81 > 79 characters)'}, {'lnum': 208, 'col': 13, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E265: block comment should start with ''# '''}, {'lnum': 232, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E501: line too long (83 > 79 characters)'}, {'lnum': 238, 'col': 9, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E265: block comment should start with ''# '''}, {'lnum': 242, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E501: line too long (80 > 79 characters)'}, {'lnum': 246, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E501: line too long (87 > 79 characters)'}, {'lnum': 247, 'col': 9, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E265: block comment should start with ''# '''}, {'lnum': 304, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E501: line too long (82 > 79 characters)'}, {'lnum': 305, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E501: line too long (87 > 79 characters)'}, {'lnum': 341, 'col': 13, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E127: continuation line over-indented for visual indent'}, {'lnum': 343, 'col': 13, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E127: continuation line over-indented for visual indent'}, {'lnum': 345, 'col': 13, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E127: continuation line over-indented for visual indent'}, {'lnum': 347, 'col': 13, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E127: continuation line over-indented for visual indent'}, {'lnum': 350, 'col': 13, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E127: continuation line over-indented for visual indent'}, {'lnum': 356, 'col': 21, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E127: continuation line over-indented for visual indent'}, {'lnum': 358, 'col': 20, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E124: closing bracket does not match visual indentation'}, {'lnum': 362, 'col': 20, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E124: closing bracket does not match visual indentation'}, {'lnum': 365, 'col': 13, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E127: continuation line over-indented for visual indent'}, {'lnum': 376, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E302: expected 2 blank lines, found 1'}, {'lnum': 389, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E501: line too long (80 > 79 characters)'}, {'lnum': 403, 'col': 14, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E261: at least two spaces before inline comment'}, {'lnum': 425, 'col': 58, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E261: at least two spaces before inline comment'}, {'lnum': 425, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E501: line too long (86 > 79 characters)'}, {'lnum': 452, 'col': 25, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E128: continuation line under-indented for visual indent'}, {'lnum': 482, 'col': 39, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E711: comparison to None should be ''if cond is not None:'''}, {'lnum': 494, 'col': 21, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E128: continuation line under-indented for visual indent'}, {'lnum': 494, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E501: line too long (80 > 79 characters)'}, {'lnum': 497, 'col': 49, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E116: unexpected indentation (comment)'}, {'lnum': 506, 'col': 23, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E127: continuation line over-indented for visual indent'}, {'lnum': 509, 'col': 25, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E128: continuation line under-indented for visual indent'}, {'lnum': 510, 'col': 25, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E128: continuation line under-indented for visual indent'}, {'lnum': 511, 'col': 25, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E128: continuation line under-indented for visual indent'}, {'lnum': 530, 'col': 13, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E265: block comment should start with ''# '''}, {'lnum': 546, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E302: expected 2 blank lines, found 1'}, {'lnum': 559, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E501: line too long (82 > 79 characters)'}, {'lnum': 573, 'col': 14, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E261: at least two spaces before inline comment'}, {'lnum': 589, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E501: line too long (80 > 79 characters)'}, {'lnum': 590, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E501: line too long (83 > 79 characters)'}, {'lnum': 595, 'col': 58, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E261: at least two spaces before inline comment'}, {'lnum': 595, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E501: line too long (86 > 79 characters)'}, {'lnum': 614, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E501: line too long (86 > 79 characters)'}, {'lnum': 624, 'col': 25, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E128: continuation line under-indented for visual indent'}, {'lnum': 654, 'col': 39, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E711: comparison to None should be ''if cond is not None:'''}, {'lnum': 667, 'col': 21, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E128: continuation line under-indented for visual indent'}, {'lnum': 667, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E501: line too long (80 > 79 characters)'}, {'lnum': 670, 'col': 53, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E116: unexpected indentation (comment)'}, {'lnum': 684, 'col': 23, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E127: continuation line over-indented for visual indent'}, {'lnum': 687, 'col': 25, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E128: continuation line under-indented for visual indent'}, {'lnum': 688, 'col': 25, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E128: continuation line under-indented for visual indent'}, {'lnum': 689, 'col': 25, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E128: continuation line under-indented for visual indent'}, {'lnum': 708, 'col': 13, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E265: block comment should start with ''# '''}, {'lnum': 724, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E302: expected 2 blank lines, found 1'}, {'lnum': 737, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E501: line too long (99 > 79 characters)'}, {'lnum': 747, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E302: expected 2 blank lines, found 1'}, {'lnum': 796, 'col': 51, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E228: missing whitespace around modulo operator'}, {'lnum': 797, 'col': 43, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E251: unexpected spaces around keyword / parameter equals'}, {'lnum': 797, 'col': 45, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E251: unexpected spaces around keyword / parameter equals'}, {'lnum': 803, 'col': 5, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E265: block comment should start with ''# '''}, {'lnum': 805, 'col': 5, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E265: block comment should start with ''# '''}, {'lnum': 832, 'col': 62, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E251: unexpected spaces around keyword / parameter equals'}, {'lnum': 832, 'col': 64, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E251: unexpected spaces around keyword / parameter equals'}, {'lnum': 867, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E501: line too long (83 > 79 characters)'}, {'lnum': 868, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E501: line too long (82 > 79 characters)'}, {'lnum': 872, 'col': 47, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E265: block comment should start with ''# '''}, {'lnum': 873, 'col': 47, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E265: block comment should start with ''# '''}, {'lnum': 874, 'col': 51, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E251: unexpected spaces around keyword / parameter equals'}, {'lnum': 874, 'col': 53, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E251: unexpected spaces around keyword / parameter equals'}, {'lnum': 875, 'col': 53, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E251: unexpected spaces around keyword / parameter equals'}, {'lnum': 875, 'col': 55, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E251: unexpected spaces around keyword / parameter equals'}, {'lnum': 876, 'col': 13, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E265: block comment should start with ''# '''}, {'lnum': 882, 'col': 13, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E265: block comment should start with ''# '''}, {'lnum': 910, 'col': 5, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E265: block comment should start with ''# '''}, {'lnum': 913, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E302: expected 2 blank lines, found 1'}, {'lnum': 922, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E302: expected 2 blank lines, found 1'}, {'lnum': 931, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'informes/norma2013.py', 'text': 'E302: expected 2 blank lines, found 1'}])
let SessionLoad = 1
if &cp | set nocp | endif
let s:so_save = &so | let s:siso_save = &siso | set so=0 siso=0
let v:this_session=expand("<sfile>:p")
silent only
silent tabonly
cd ~/Geotexan/src/Geotex-INN/ginn
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
argglobal
%argdel
$argadd ~/Geotexan/src/Geotex-INN/geotexan.vim
edit informes/norma2013.py
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
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
exe 'vert 1resize ' . ((&columns * 29 + 65) / 130)
exe '2resize ' . ((&lines * 25 + 29) / 58)
exe 'vert 2resize ' . ((&columns * 100 + 65) / 130)
exe '3resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 3resize ' . ((&columns * 100 + 65) / 130)
exe '4resize ' . ((&lines * 20 + 29) / 58)
exe 'vert 4resize ' . ((&columns * 100 + 65) / 130)
exe '5resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 5resize ' . ((&columns * 100 + 65) / 130)
exe '6resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 6resize ' . ((&columns * 100 + 65) / 130)
exe '7resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 7resize ' . ((&columns * 100 + 65) / 130)
exe '8resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 8resize ' . ((&columns * 100 + 65) / 130)
argglobal
enew
file __Tagbar__.1
wincmd w
argglobal
let s:l = 362 - ((22 * winheight(0) + 12) / 25)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
362
normal! 013|
wincmd w
argglobal
if bufexists("api/tests/efcodd.py") | buffer api/tests/efcodd.py | else | edit api/tests/efcodd.py | endif
let s:l = 30 - ((1 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
30
normal! 031|
wincmd w
argglobal
if bufexists("api/murano/ops.py") | buffer api/murano/ops.py | else | edit api/murano/ops.py | endif
let s:l = 528 - ((1 * winheight(0) + 10) / 20)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
528
normal! 040|
wincmd w
argglobal
if bufexists("api/tests/sr_lobo.py") | buffer api/tests/sr_lobo.py | else | edit api/tests/sr_lobo.py | endif
let s:l = 968 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
968
normal! 046|
wincmd w
argglobal
if bufexists("api/tests/ramanujan.py") | buffer api/tests/ramanujan.py | else | edit api/tests/ramanujan.py | endif
let s:l = 1238 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1238
normal! 05|
wincmd w
argglobal
if bufexists("api/tests/clouseau.py") | buffer api/tests/clouseau.py | else | edit api/tests/clouseau.py | endif
let s:l = 366 - ((1 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
366
normal! 037|
wincmd w
argglobal
enew
wincmd w
2wincmd w
exe 'vert 1resize ' . ((&columns * 29 + 65) / 130)
exe '2resize ' . ((&lines * 25 + 29) / 58)
exe 'vert 2resize ' . ((&columns * 100 + 65) / 130)
exe '3resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 3resize ' . ((&columns * 100 + 65) / 130)
exe '4resize ' . ((&lines * 20 + 29) / 58)
exe 'vert 4resize ' . ((&columns * 100 + 65) / 130)
exe '5resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 5resize ' . ((&columns * 100 + 65) / 130)
exe '6resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 6resize ' . ((&columns * 100 + 65) / 130)
exe '7resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 7resize ' . ((&columns * 100 + 65) / 130)
exe '8resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 8resize ' . ((&columns * 100 + 65) / 130)
tabnext 1
badd +1 api/tests/efcodd.py
badd +1 ~/Geotexan/src/Geotex-INN/geotexan.vim
badd +0 api/murano/ops.py
badd +1 api/tests/sr_lobo.py
badd +1 api/tests/ramanujan.py
badd +1 api/tests/clouseau.py
badd +0 informes/norma2013.py
if exists('s:wipebuf') && len(win_findbuf(s:wipebuf)) == 0
"   silent exe 'bwipe ' . s:wipebuf
endif
" unlet! s:wipebuf
set winheight=1 winwidth=1 shortmess=aoOc
set winminheight=1 winminwidth=1
let s:sx = expand("<sfile>:p:r")."x.vim"
if file_readable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &so = s:so_save | let &siso = s:siso_save

" Support for special windows like quick-fix and plug-in windows.
" Everything down here is generated by vim-session (not supported
" by :mksession out of the box).

8wincmd w
tabnext 1
let s:bufnr_save = bufnr("%")
let s:cwd_save = getcwd()
cwindow
if !getbufvar(s:bufnr_save, '&modified')
  let s:wipebuflines = getbufline(s:bufnr_save, 1, '$')
  if len(s:wipebuflines) <= 1 && empty(get(s:wipebuflines, 0, ''))
    silent execute 'bwipeout' s:bufnr_save
  endif
endif
execute "cd" fnameescape(s:cwd_save)
1resize 56|vert 1resize 29|2resize 25|vert 2resize 100|3resize 1|vert 3resize 100|4resize 20|vert 4resize 100|5resize 1|vert 5resize 100|6resize 1|vert 6resize 100|7resize 1|vert 7resize 100|8resize 1|vert 8resize 100|
2wincmd w
tabnext 1
if exists('s:wipebuf')
  if empty(bufname(s:wipebuf))
if !getbufvar(s:wipebuf, '&modified')
  let s:wipebuflines = getbufline(s:wipebuf, 1, '$')
  if len(s:wipebuflines) <= 1 && empty(get(s:wipebuflines, 0, ''))
    silent execute 'bwipeout' s:wipebuf
  endif
endif
  endif
endif
doautoall SessionLoadPost
unlet SessionLoad
" vim: ft=vim ro nowrap smc=128
