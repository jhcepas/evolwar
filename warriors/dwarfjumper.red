;Name Dwarf Jumper
;Author	Rodrigo Setti
;Strat Lan�a c�digos de "pris�o" pela mem�ria
;Strat que mant�m os processos inimigos
;Strat paralizados, por�m, n�o � mortal.


org 1

mov.i	$1,	>2
jmp.f   $-1,    >1
