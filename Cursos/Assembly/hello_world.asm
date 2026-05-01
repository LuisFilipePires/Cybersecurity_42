; compilacao
; nasm -f elf64 hello_world.asm 
; Linkeditar - Transformar o programa em linguagem maquina para um executavel
; ld -s -o <nome_desejado> <nome_da_imagem (.o gerada em cima)>



section .data

;section .bss

section .text

global _start

_start:
	;hexadecimal base 1 2 3 4 5 6 7 8 9 A B C D E F
	;assembly funciona como falar por walkitalk ~cambio
	;mov = destino, origem
	mov eax, 0x1 ;SO (operative system) estou terminando etc
	mov EBX, 0x0
	int 0x80



