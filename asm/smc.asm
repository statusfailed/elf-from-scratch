BITS 64 ; 64-bit mode

SECTION .text
  global main

; some silly self modifying code.
; prints "hur", then changes itself to print "dur", then exits.
;
; NOTE: extremely brittle, because it bakes in exact addresses when doing
; self-modification. Nasm probably has a way to make this nicer?
;
; When using elf-from-scratch, main will be loaded into memory at 0x400078.
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

  ; Pop the stack
  ; NOTE: on lines 37+38, this & the following instruction are overwritten
  ; with a 2-byte relative JMP to line 44 (the exit syscall @ "end").
  pop rax

  ; modify code (x86-64 encodes the 4-byte constant of the first instruction @
  ; address main+1, so we modify the first byte to be "d" instead of "h".
  mov byte [0x400079], 0x64 ; WARNING: more baked in offsets

  ; modify "pop rax" to instead jump to end.
  ; here we directly write the instruction encoding:
  ;   * 0xEB for JMP relative,
  ;   * 0x19 for 8-bit relative offset
  ; see here for reference: https://www.felixcloutier.com/x86/jmp
  mov byte [0x400092], 0xEB ; opcode for relative jump
  mov byte [0x400093], 0x19 ; relative offset (calculated using gdb)

  ; now jump back to main and execute the new (modified) code:
  ;   * print "dur"
  ;   * jump directly to end
  jmp main

end:
  ; exit(0)
  mov rax, 60  ; exit
  mov rdi, r10 ; success
  syscall
