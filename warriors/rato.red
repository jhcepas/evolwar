;Name   Rato Replicante
;Author Rodrigo Setti
;Strat  Mant�m um processo ininterrupto de
;Strat  cria��o de c�pias funcionais.

org inicio

vetores dat.f   $0,         $2981       ;vetores de copia
inicio  mov.i   }vetores,   >vetores    ;copia instru��o e incrementa vetores
        jmn.b   $inicio,    *vetores    ;loop de c�pia -> enquanto nao encontrou um zero em B
        spl.b   <vetores,   {vetores    ;cria processo na c�pia (ajuda a reestruturar ponteiro)
        add.x   #-31,       $-4         ;reestrutura ponteiros
        jmz.a   $inicio,    {vetores    ;loop do programa (ajuda a reestruturar ponteiro)
                                        ;ou se suicida se o programa estiver alterado
