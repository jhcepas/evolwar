;Name Polen
;Author Rodrigo Setti
;Strat Lan�a v�rios "esporos" com processos
;Strat pela mem�ria, dif�ceis de serem localizados
;Strat e exterminados, por�m s�o inofensivos.

org 2

jmp.f   #0,     <-3

slt.b	$1,	#4
mov.i	$-2,	$973
spl.f   @-1,    }1
add.ab	#971,	$-2
jmp.f   $-4,    #0
