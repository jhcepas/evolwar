;Name IMPTTres
;Author Rodrigo Setti
;Strat Se move pela mem�ria linearmente,
;Strat an�logo ao IMP.

mov.i   $0,     $3
seq.ab  }-1,    #-2
jmp.b   $-2,    >-2
