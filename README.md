# elf-from-scratch

This was a challenge to myself: build an ELF64 file from scratch without using
a toolchain (other than an assembler to get raw `x86_64` instructions)

[main.py](main.py) will write to stdout an executable ELF64 file with a single program header
table entry, and no sections.

[main.py](main.py) currently hardcodes the program to write- it's "hello world".
See [asm/hello.asm](asm/hello.asm) for a program listing.

[go.sh](go.sh) will run the main script, call `readelf -a` on the output, and run the
ELF64 file.

Here's what `readelf` has to say about the produced ELF:

		ELF Header:
			Magic:   7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00
			Class:                             ELF64
			Data:                              2's complement, little endian
			Version:                           1 (current)
			OS/ABI:                            UNIX - System V
			ABI Version:                       0
			Type:                              EXEC (Executable file)
			Machine:                           Advanced Micro Devices X86-64
			Version:                           0x1
			Entry point address:               0x400078
			Start of program headers:          64 (bytes into file)
			Start of section headers:          0 (bytes into file)
			Flags:                             0x0
			Size of this header:               64 (bytes)
			Size of program headers:           56 (bytes)
			Number of program headers:         1
			Size of section headers:           0 (bytes)
			Number of section headers:         0
			Section header string table index: 0

		There are no sections in this file.

		There are no sections to group in this file.

		Program Headers:
			Type           Offset             VirtAddr           PhysAddr
										 FileSiz            MemSiz              Flags  Align
			LOAD           0x0000000000000000 0x0000000000400000 0x0000000000400000
										 0x000000000000002f 0x000000000000002f  RWE    0x4

		There is no dynamic section in this file.

		There are no relocations in this file.

		The decoding of unwind sections for machine type Advanced Micro Devices X86-64 is not currently supported.

		Dynamic symbol information is not available for displaying symbols.

		No version information found in this file.

# TODO

* Why does my program header table entry have to have an offset of 0? I get segfaults otherwise :(
  - Might be due to [this][1] - seems like `p_offset` must be page aligned?

[1]: https://stackoverflow.com/questions/5104060/elf-program-header-offset

# references

Links I found useful while making this:

- [ELF-64 Object File Format](https://www.uclibc.org/docs/elf-64-gen.pdf)
- [Linux X86_64 syscalls table](http://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/)

# useful commands

see [util/](util/) folder for handy scripts using the below commands.

nasm assembler

    # compile only x86_64 instructions
    nasm -f bin -o out.bin in.asm

    # compile to linkable elf
    nasm -f elf64 -o out.o in.asm

link `out.o` file without stdlib and gcc cruft:

    gcc out.o -o out.elf -nostartfiles -nostdinc -nostdlib
