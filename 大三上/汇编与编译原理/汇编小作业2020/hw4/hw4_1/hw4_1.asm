.386
.model flat, stdcall
option casemap:none
include windows.inc
include kernel32.inc
include user32.inc
includelib kernel32.lib
includelib user32.lib
includelib      msvcrt.lib
printf          PROTO C :ptr sbyte, :VARARG
scanf           PROTO C :ptr sbyte, :VARARG

.data
intArray WORD 500h, 400h, 300h, 200h, 100h
beginMsg byte "Stack parameters:",0ah, 0dh,  "---------------------------",  0ah, 0dh, 0
paramMsg byte "Address %x = %x", 0ah, 0dh, 0

.code
;----------------
;ShowParams
;----------------
ShowParams PROC,
	paramCount: DWORD
	;print
	pushad
	invoke  printf, offset beginMsg
	popad

	pushad
	mov ecx, paramCount
	mov eax, ebp
	add eax, 16
	L1:
	add eax, 4
	mov ebx, [eax]

	;print
	pushad
	invoke  printf, offset paramMsg, eax, ebx
	popad

	loop L1

	popad
    ret
ShowParams ENDP

;----------------
;MySample
;----------------
MySample PROC,
	first: DWORD, second: DWORD, third: DWORD
	INVOKE ShowParams, 3
	ret
MySample ENDP

main PROC
	INVOKE MySample, 1234h, 5000h, 6543h
    INVOKE ExitProcess, 0
main ENDP

END main