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
ansMsg byte "结果是%d", 0ah, 0dh, 0

.code
main PROC
	call sumof
	call sumofRecurrent
    INVOKE ExitProcess, 0
main ENDP

;----------------
;非循环方式求和
;----------------
sumof PROC
	mov eax, 0
	add ax, intArray
	add ax, intArray + TYPE intArray
	add ax, intArray + 2 * TYPE intArray
	add ax, intArray + 3 * TYPE intArray
	add ax, intArray + 4 * TYPE intArray
	INVOKE printf, offset ansMsg, eax
    ret
sumof ENDP


;----------------
;循环方式求和
;----------------
sumofRecurrent PROC
	mov esi, offset intArray
	mov ecx, lengthof intArray
	mov eax, 0
	L1:
	add ax, [esi]
	add esi, TYPE intArray
	loop L1
	INVOKE printf, offset ansMsg, eax
    ret
sumofRecurrent ENDP

END main