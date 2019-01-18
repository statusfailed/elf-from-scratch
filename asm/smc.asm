BITS 64 ; 64-bit mode

SECTION .text
  global main

; some silly self modifying code.
; prints "hur", then changes itself to print "dur", then exits.
;
; NOTE: extremely brittle, because it bakes in exact addresses when doing
; self-modification. Nasm probably has a way to make this nicer?
main:
  ; put "hur\n" on the stack
  mov rax, 0x0a727568
  push rax

  ; Print the string stored at RSP
  mov rax, 1   ; write
  mov rdi, 1   ; fd = stdout
  mov rsi, rsp ; buf = rsp
  mov rdx, 4  ; len("hur\n")
  syscall;

  pop rax

  ;;;; if line 10 writes "dur", skip to end.
  ; load 2nd byte of program + examine
  mov al, byte [0x400079] ; address of main if you compile with main.py (lool)
  cmp al, 0x64 ; rax == 'd' ?
  je end

  ; modify code (x86-64 stores 4-byte constant @ main+1, so we modify the first
  ; byte.
  ; change to write "dur\n" instead, and then jump there + execute it.
  mov byte [0x400079], 0x64 ; WARNING: more baked in offsets
  jmp main

end:
  ; exit(0)
  mov rax, 60  ; exit
  mov rdi, r10 ; success
  syscall
