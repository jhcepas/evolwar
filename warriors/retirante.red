;Name Retirante
;Author	Rodrigo Setti
;Strat Mant�m um processo de mudan�a constante
;Strat de endere�o na mem�ria, o que o torna
;Strat dif�cil de ser localizado.

mov.i   $0,     $1002	;copia instru��o
jmz.b	>-1,	}-1	;verifica fim e incrementa copia
jmp.b	$-2,	#0	;pula para copia
