BITS 64 ; 64-bit mode

SECTION .text
  global main

main:
  ; put "hello world\n" on the stack
  ; a .data section? what's that?
  mov rax, 0x0a646c72
  push rax
  mov rax, 0x6f77206f6c6c6568
  push rax

  ; write(1, rsp, 16)
  mov rax, 1   ; write
  mov rdi, 1   ; fd = stdout
  mov rsi, rsp ; buf = rsp
  mov rdx, 12  ; len("hello world\n")
  syscall;

  ; exit(0)
  mov rax, 60  ; exit
  mov rdi, r10 ; success
  syscall
