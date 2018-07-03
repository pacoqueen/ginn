" ~/Geotexan/src/Geotex-INN/geotexan.vim:
" Vim session script.
" Created by session.vim 2.13.1 on 03 julio 2018 at 11:54:02.
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
call setqflist([{'lnum': 42, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/tests/sr_lobo.py', 'text': 'E402: module level import not at top of file'}, {'lnum': 43, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/tests/sr_lobo.py', 'text': 'E402: module level import not at top of file'}, {'lnum': 44, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/tests/sr_lobo.py', 'text': 'E402: module level import not at top of file'}, {'lnum': 108, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/tests/sr_lobo.py', 'text': 'E501: line too long (85 > 79 characters)'}, {'lnum': 112, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/tests/sr_lobo.py', 'text': 'E501: line too long (84 > 79 characters)'}, {'lnum': 114, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/tests/sr_lobo.py', 'text': 'E501: line too long (88 > 79 characters)'}, {'lnum': 121, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/tests/sr_lobo.py', 'text': 'E501: line too long (87 > 79 characters)'}, {'lnum': 179, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/tests/sr_lobo.py', 'text': 'E501: line too long (80 > 79 characters)'}, {'lnum': 344, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/tests/sr_lobo.py', 'text': 'E501: line too long (94 > 79 characters)'}, {'lnum': 366, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/tests/sr_lobo.py', 'text': 'E501: line too long (82 > 79 characters)'}, {'lnum': 370, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/tests/sr_lobo.py', 'text': 'E501: line too long (83 > 79 characters)'}, {'lnum': 395, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'W', 'module': '', 'filename': 'api/tests/sr_lobo.py', 'text': 'fixme: TODO: ¿Un tick o algo al log para saber que ha hecho acierto de caché?'}, {'lnum': 395, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/tests/sr_lobo.py', 'text': 'E501: line too long (80 > 79 characters)'}, {'lnum': 402, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/tests/sr_lobo.py', 'text': 'E501: line too long (81 > 79 characters)'}, {'lnum': 686, 'col': 47, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/tests/sr_lobo.py', 'text': 'E712: comparison to True should be ''if cond is True:'' or ''if cond:'''}, {'lnum': 702, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/tests/sr_lobo.py', 'text': 'E501: line too long (80 > 79 characters)'}, {'lnum': 703, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/tests/sr_lobo.py', 'text': 'E501: line too long (80 > 79 characters)'}, {'lnum': 707, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/tests/sr_lobo.py', 'text': 'E501: line too long (81 > 79 characters)'}, {'lnum': 713, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/tests/sr_lobo.py', 'text': 'E501: line too long (82 > 79 characters)'}, {'lnum': 750, 'col': 36, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/tests/sr_lobo.py', 'text': 'E712: comparison to False should be ''if cond is False:'' or ''if not cond:'''}, {'lnum': 753, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/tests/sr_lobo.py', 'text': 'E501: line too long (81 > 79 characters)'}, {'lnum': 816, 'col': 47, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/tests/sr_lobo.py', 'text': 'E712: comparison to True should be ''if cond is True:'' or ''if cond:'''}, {'lnum': 874, 'col': 12, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'W', 'module': '', 'filename': 'api/tests/sr_lobo.py', 'text': 'len-as-condition: Do not use `len(SEQUENCE)` to determine if a sequence is empty'}, {'lnum': 875, 'col': 13, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/tests/sr_lobo.py', 'text': 'E127: continuation line over-indented for visual indent'}, {'lnum': 39, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/tests/ramanujan.py', 'text': 'E402: module level import not at top of file'}, {'lnum': 40, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/tests/ramanujan.py', 'text': 'E402: module level import not at top of file'}, {'lnum': 41, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/tests/ramanujan.py', 'text': 'E402: module level import not at top of file'}, {'lnum': 42, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/tests/ramanujan.py', 'text': 'E402: module level import not at top of file'}, {'lnum': 43, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/tests/ramanujan.py', 'text': 'E402: module level import not at top of file'}, {'lnum': 44, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/tests/ramanujan.py', 'text': 'E402: module level import not at top of file'}, {'lnum': 48, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'W', 'module': '', 'filename': 'api/tests/ramanujan.py', 'text': 'fixme: TODO: Hacer un parámetro para demonio o algo que saque la consulta de'}, {'lnum': 50, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'W', 'module': '', 'filename': 'api/tests/ramanujan.py', 'text': 'fixme: TODO: Hacer un chequeo por A, B y C antes de los totales para detectar'}, {'lnum': 103, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'W', 'module': '', 'filename': 'api/tests/ramanujan.py', 'text': 'fixme: TODO: Productos sin trazabilidad no deberían analizarse. O bien hacerlo de'}, {'lnum': 103, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/tests/ramanujan.py', 'text': 'E501: line too long (80 > 79 characters)'}, {'lnum': 104, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/tests/ramanujan.py', 'text': 'E501: line too long (80 > 79 characters)'}, {'lnum': 108, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/tests/ramanujan.py', 'text': 'E501: line too long (80 > 79 characters)'}, {'lnum': 220, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/tests/ramanujan.py', 'text': 'E501: line too long (80 > 79 characters)'}, {'lnum': 307, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'W', 'module': '', 'filename': 'api/tests/ramanujan.py', 'text': 'fixme: TODO: También podría recibir un fichero de inventario para calcular'}, {'lnum': 408, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/tests/ramanujan.py', 'text': 'E501: line too long (86 > 79 characters)'}, {'lnum': 497, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/tests/ramanujan.py', 'text': 'E302: expected 2 blank lines, found 1'}, {'lnum': 544, 'col': 59, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/tests/ramanujan.py', 'text': 'E261: at least two spaces before inline comment'}, {'lnum': 544, 'col': 60, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/tests/ramanujan.py', 'text': 'E262: inline comment should start with ''# '''}, {'lnum': 704, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/tests/ramanujan.py', 'text': 'E303: too many blank lines (3)'}, {'lnum': 705, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/tests/ramanujan.py', 'text': 'E302: expected 2 blank lines, found 3'}, {'lnum': 782, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/tests/ramanujan.py', 'text': 'E501: line too long (242 > 79 characters)'}, {'lnum': 832, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/tests/ramanujan.py', 'text': 'E302: expected 2 blank lines, found 1'}, {'lnum': 879, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/tests/ramanujan.py', 'text': 'E501: line too long (80 > 79 characters)'}, {'lnum': 937, 'col': 8, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/tests/ramanujan.py', 'text': 'E713: test for membership should be ''not in'''}, {'lnum': 994, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/tests/ramanujan.py', 'text': 'E501: line too long (80 > 79 characters)'}, {'lnum': 9, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'W', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'line-too-long: Line too long (108/100)'}, {'lnum': 9, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'W', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'fixme: TODO: No sincroniza el campo que indica que el geotextil es C en los productos de venta de tipo Geotextil.'}, {'lnum': 9, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'E501: line too long (108 > 79 characters)'}, {'lnum': 23, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'E402: module level import not at top of file'}, {'lnum': 24, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'E402: module level import not at top of file'}, {'lnum': 25, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'E402: module level import not at top of file'}, {'lnum': 26, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'E402: module level import not at top of file'}, {'lnum': 27, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'E402: module level import not at top of file'}, {'lnum': 39, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'E402: module level import not at top of file'}, {'lnum': 489, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'W', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'fixme: TODO: Debería mirar los campos módulo y función de Murano y dejar todo'}, {'lnum': 498, 'col': 45, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'E261: at least two spaces before inline comment'}, {'lnum': 498, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'E501: line too long (82 > 79 characters)'}, {'lnum': 1143, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'bad-option-value: Bad option value ''redefined-variable-type'''}, {'lnum': 1177, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'bad-option-value: Bad option value ''redefined-variable-type'''}, {'lnum': 1233, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'E501: line too long (80 > 79 characters)'}, {'lnum': 1236, 'col': 13, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'E127: continuation line over-indented for visual indent'}, {'lnum': 1325, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'bad-option-value: Bad option value ''redefined-variable-type'''}, {'lnum': 1359, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'bad-option-value: Bad option value ''redefined-variable-type'''}, {'lnum': 1449, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'bad-option-value: Bad option value ''redefined-variable-type'''}, {'lnum': 1483, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'bad-option-value: Bad option value ''redefined-variable-type'''}, {'lnum': 1498, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'W', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'inconsistent-return-statements: Either all return statements in a function should return an expression, or none of them should.'}, {'lnum': 1578, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'bad-option-value: Bad option value ''redefined-variable-type'''}, {'lnum': 1587, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'W', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'inconsistent-return-statements: Either all return statements in a function should return an expression, or none of them should.'}, {'lnum': 1671, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'bad-option-value: Bad option value ''redefined-variable-type'''}, {'lnum': 1680, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'W', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'inconsistent-return-statements: Either all return statements in a function should return an expression, or none of them should.'}, {'lnum': 1761, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'bad-option-value: Bad option value ''redefined-variable-type'''}, {'lnum': 1785, 'col': 13, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'E127: continuation line over-indented for visual indent'}, {'lnum': 1818, 'col': 25, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'E261: at least two spaces before inline comment'}, {'lnum': 1818, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'E501: line too long (80 > 79 characters)'}, {'lnum': 1848, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'bad-option-value: Bad option value ''redefined-variable-type'''}, {'lnum': 1870, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'bad-option-value: Bad option value ''redefined-variable-type'''}, {'lnum': 1906, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'bad-option-value: Bad option value ''redefined-variable-type'''}, {'lnum': 1922, 'col': 27, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'W', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'len-as-condition: Do not use `len(SEQUENCE)` to determine if a sequence is empty'}, {'lnum': 1946, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'W', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'fixme: TODO: Ojo porque si cambio a calidad C probablemente implique un'}, {'lnum': 1953, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'W', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'bad-whitespace: Exactly one space required around assignment'}, {'lnum': 1953, 'col': 31, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'E225: missing whitespace around operator'}, {'lnum': 1959, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'E501: line too long (84 > 79 characters)'}, {'lnum': 1963, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'W', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'bad-continuation: Wrong continued indentation (add 14 spaces).'}, {'lnum': 1963, 'col': 21, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'E128: continuation line under-indented for visual indent'}, {'lnum': 1964, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'W', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'bad-continuation: Wrong continued indentation (add 14 spaces).'}, {'lnum': 1964, 'col': 21, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'E128: continuation line under-indented for visual indent'}, {'lnum': 2243, 'col': 13, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'E127: continuation line over-indented for visual indent'}, {'lnum': 2244, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'W', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'fixme: TODO: ¿Y al descontar existencias? ¿Comprobar también que existan antes?'}, {'lnum': 2414, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'bad-option-value: Bad option value ''redefined-variable-type'''}, {'lnum': 2576, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'W', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'fixme: FIXME: Implementar otra forma de que la relación sea biyectiva.'}, {'lnum': 2637, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'W', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'fixme: FIXME: Ojo porque puede crear 2 registros con el mismo texto y guid. ¿Mismo sysStatus también? Espero que sí... Preguntar a Sage.'}, {'lnum': 2637, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'W', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'line-too-long: Line too long (139/100)'}, {'lnum': 2637, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'E501: line too long (139 > 79 characters)'}, {'lnum': 2689, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'E501: line too long (82 > 79 characters)'}, {'lnum': 2707, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'E501: line too long (80 > 79 characters)'}, {'lnum': 2741, 'col': 5, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'E266: too many leading ''#'' for block comment'}, {'lnum': 2743, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'E501: line too long (90 > 79 characters)'}, {'lnum': 2744, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'E501: line too long (89 > 79 characters)'}, {'lnum': 2745, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'E501: line too long (83 > 79 characters)'}, {'lnum': 2746, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'E501: line too long (93 > 79 characters)'}, {'lnum': 2748, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'W', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'fixme: XXX: [20170601] Por algún motivo que ni Félix ni yo'}, {'lnum': 2756, 'col': 5, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'E266: too many leading ''#'' for block comment'}, {'lnum': 2813, 'col': 13, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'E266: too many leading ''#'' for block comment'}, {'lnum': 2828, 'col': 9, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'E266: too many leading ''#'' for block comment'}, {'lnum': 3087, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'bad-option-value: Bad option value ''redefined-variable-type'''}, {'lnum': 3112, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'bad-option-value: Bad option value ''redefined-variable-type'''}, {'lnum': 3162, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'W', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'fixme: TODO: Hasta que lea directamente el producto de Murano'}, {'lnum': 3352, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'W', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'fixme: TODO: PORASQUI'}, {'lnum': 3374, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'W', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'bad-continuation: Wrong hanging indentation (remove 4 spaces).'}, {'lnum': 3494, 'col': 1, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'api/murano/ops.py', 'text': 'bad-option-value: Bad option value ''redefined-variable-type'''}])
let SessionLoad = 1
if &cp | set nocp | endif
let s:so_save = &so | let s:siso_save = &siso | set so=0 siso=0
let v:this_session=expand("<sfile>:p")
silent only
cd ~/Geotexan/src/Geotex-INN/ginn
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
badd +1 ~/Geotexan/src/Geotex-INN/geotexan.vim
badd +1 api/tests/sr_lobo.py
badd +1 api/tests/ramanujan.py
badd +947 formularios/menu.py
badd +1641 formularios/partes_de_fabricacion_bolsas.py
badd +1 api/murano/ops.py
argglobal
silent! argdel *
$argadd ~/Geotexan/src/Geotex-INN/geotexan.vim
edit api/murano/ops.py
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
3wincmd k
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
exe 'vert 1resize ' . ((&columns * 27 + 67) / 134)
exe '2resize ' . ((&lines * 17 + 28) / 57)
exe 'vert 2resize ' . ((&columns * 106 + 67) / 134)
exe '3resize ' . ((&lines * 17 + 28) / 57)
exe 'vert 3resize ' . ((&columns * 106 + 67) / 134)
exe '4resize ' . ((&lines * 17 + 28) / 57)
exe 'vert 4resize ' . ((&columns * 106 + 67) / 134)
exe '5resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 5resize ' . ((&columns * 106 + 67) / 134)
argglobal
enew
file __Tagbar__.1
wincmd w
argglobal
let s:l = 2217 - ((8 * winheight(0) + 8) / 17)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2217
normal! 041|
wincmd w
argglobal
if bufexists('api/tests/ramanujan.py') | buffer api/tests/ramanujan.py | else | edit api/tests/ramanujan.py | endif
let s:l = 410 - ((9 * winheight(0) + 8) / 17)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
410
normal! 024|
wincmd w
argglobal
if bufexists('api/tests/sr_lobo.py') | buffer api/tests/sr_lobo.py | else | edit api/tests/sr_lobo.py | endif
let s:l = 49 - ((3 * winheight(0) + 8) / 17)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
49
normal! 07|
wincmd w
argglobal
enew
wincmd w
2wincmd w
exe 'vert 1resize ' . ((&columns * 27 + 67) / 134)
exe '2resize ' . ((&lines * 17 + 28) / 57)
exe 'vert 2resize ' . ((&columns * 106 + 67) / 134)
exe '3resize ' . ((&lines * 17 + 28) / 57)
exe 'vert 3resize ' . ((&columns * 106 + 67) / 134)
exe '4resize ' . ((&lines * 17 + 28) / 57)
exe 'vert 4resize ' . ((&columns * 106 + 67) / 134)
exe '5resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 5resize ' . ((&columns * 106 + 67) / 134)
tabnext 1
if exists('s:wipebuf') && s:wipebuf != bufnr('%')
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

5wincmd w
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
1resize 55|vert 1resize 27|2resize 17|vert 2resize 106|3resize 17|vert 3resize 106|4resize 17|vert 4resize 106|5resize 1|vert 5resize 106|
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
