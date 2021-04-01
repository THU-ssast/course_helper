.386
.model flat, stdcall
option casemap:none
include windows.inc
include kernel32.inc
include user32.inc
includelib kernel32.lib
includelib user32.lib
includelib msvcrt.lib

printf          PROTO C :ptr sbyte, :VARARG
scanf           PROTO C :ptr sbyte, :VARARG

.data
scanMsg         byte    "%s", 0, 0
buffer          byte    100 DUP(?), 0, 0
idMsg           byte    "请输入学号：", 0
nameMsg         byte    "请输入姓名：", 0
birthdayMsg     byte    "请输入生日：", 0 
continueMsg     byte    "是否继续？y/n: ", 0 

filename        byte    "students.txt", 0, 0
filehandle      DWORD    ?
bytesRead       DWORD    ?
bytesWrite      DWORD    ?
stdInHandle     HANDLE   ?
enterMsg        byte    0ah

.code

scanfandwrite PROC
	invoke GetStdHandle, STD_INPUT_HANDLE
	mov stdInHandle, eax
	invoke ReadConsole, stdInHandle, ADDR buffer, 100, ADDR bytesRead, 0
	invoke WriteFile, filehandle, offset buffer, bytesRead, bytesWrite, NULL

	ret
scanfandwrite ENDP


main PROC
	invoke CreateFile, 
	ADDR filename,
	GENERIC_WRITE,
	0,                     ;DO_NOT_SHARE
	NULL,
	CREATE_ALWAYS,
	FILE_ATTRIBUTE_NORMAL,
	0

	mov filehandle, eax

	.REPEAT
	invoke printf, offset idMsg
	invoke scanfandwrite
	invoke printf, offset nameMsg
	invoke scanfandwrite
	invoke printf, offset birthdayMsg
	invoke scanfandwrite

	invoke printf, offset continueMsg
	invoke GetStdHandle, STD_INPUT_HANDLE
	mov stdInHandle, eax
	invoke ReadConsole, stdInHandle, ADDR buffer, 100, ADDR bytesRead, 0
	invoke WriteFile, filehandle, offset enterMsg, 1, bytesWrite, NULL
	.UNTIL [buffer] != 'y'


	invoke CloseHandle, filehandle



    INVOKE ExitProcess, 0
main ENDP

END main