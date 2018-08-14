BITS 64 ; 64-bit mode

SECTION .text
  global main

main:
  mov rax, 60  ; exit
  mov rdi, rsp ; rsp value
  syscall;
