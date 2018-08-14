#!/usr/bin/env python3

""" TODO
  1. Why phdr has to include ELF file??
"""

import numbers
from constants import *

DEFAULT_ENTRY_POINT = 0x400000

#    ELF HEADER
# ----------------
#  Prog Hdr table
# ----------------
#     Segment
# ----------------
#       ...
# ----------------
# Section Hdr Tbl

def uint(n, x):
    return x.to_bytes(n, 'little')

ELF64_TYPE_SIZE = {
    'addr': 8, # 8 unsigned program address
    'off': 8, # 8 unsigned file offset
    'half': 2, # 2 unsigned medium integer
    'word': 4, # 4 unsigned integer
    'sword': 4, # 4 signed integer
    'xword': 8, # 8 unsigned long integer
    'sxword': 8, # 8 signed long integer
    'unsigned_char': 1, # 1 unsigned small integer
}

def to_size(elf64_type):
    result = ELF64_TYPE_SIZE.get(elf64_type, elf64_type)
    if not isinstance(result, numbers.Number):
        raise Exception("{} is not a size".format(elf64_type))
    return result

def serialize(x, elf64_type):
    """ elf64_type is either:
            str in ELF64_TYPE_SIZE.keys()
            number (length in bytes)
    """
    size = to_size(elf64_type)

    if isinstance(x, numbers.Number):
        return x.to_bytes(size, 'little')

    elif isinstance(x, bytes):
        if len(x) != size:
            raise Exception("data length {} != type {} length of {}".format(len(x), elf64_type, size))
        return x

    raise Exception("can't serialize {} of type {}".format(x, elf64_type))

ELF64_EHDR = [
    ('e_ident', 16), # ELF identification (actually 16-length array of unsigned char)
    ('e_type', 'half'), #   Object file type
    ('e_machine', 'half'), #   Machine type
    ('e_version', 'word'), #   Object file version
    ('e_entry', 'addr'), #   Entry point address
    ('e_phoff', 'off'), #   Program header offset
    ('e_shoff', 'off'), #   Section header offset
    ('e_flags', 'word'), #   Processor-specific flags
    ('e_ehsize', 'half'), #   ELF header size
    ('e_phentsize', 'half'), #   Size of program header entry
    ('e_phnum', 'half'), #   Number of program header entries
    ('e_shentsize', 'half'), #   Size of section header entry
    ('e_shnum', 'half'), #   Number of section header entries
    ('e_shstrndx', 'half'), #   Section name string table index
]

def e_ident():
    return b''.join([
        b'\x7FELF', # magic
        b'\x02', # ELF64
        b'\x01', # Little-endian
        b'\x01', # EI_ABIVERSION
        b'\x00', # ELFOSABI_HPUX ?? # ELFOSABI_SYSV (TODO \x04 instead? LINUX?)
        b'\x00', # epends on EI_ABIVERSION
        b'\x00' * 6, # Padding
        b'\x00', # size of e_ident ??
    ])

def serialize_struct(layout, values):
    result = b''
    for key, field_type in layout:
        result += serialize(values[key], field_type)
    return result

def struct_len(layout):
    return sum(to_size(t) for _, t in layout)

def elf64_ehdr():
    # TODO: why does this have to happen :[
    prefix_size = struct_len(ELF64_EHDR) + struct_len(ELF64_PHDR)
    entry_point = DEFAULT_ENTRY_POINT + prefix_size # virtual addr

    phlen = len(program_header()) # quicc check
    e_ehsize = struct_len(ELF64_EHDR) # size of ELF64 header
    e_phoff  = struct_len(ELF64_EHDR) # prog header offset
    e_shoff  = 0 # no sections

    return serialize_struct(ELF64_EHDR, dict(
        e_ident=e_ident(),
        e_type=ET_EXEC,
        e_machine=EM_X86_64,
        e_version=EV_CURRENT,
        e_entry=entry_point,  # virtual addr entry point
        e_phoff=e_phoff,      # file offset for program header
        e_shoff=e_shoff,      # File offset for section header
        e_flags=0,            # processor specific flags
        e_ehsize=e_ehsize,    # size in bytes of ELF header. (constant!)
        e_phentsize=phlen,    # size in bytes of prog header table entry
        e_phnum=1,            # num entries in prog header
        e_shentsize=0,        # size in bytes of section header table entry
        e_shnum=0,            # num entries in section header
        e_shstrndx=SHN_UNDEF  # no section name strings table
    ))

ELF64_PHDR = [
    ('p_type', 'word'), # Type of segment
    ('p_flags', 'word'), # Segment attributes
    ('p_offset', 'off'), # Offset in file
    ('p_vaddr', 'addr'), # Virtual address in memory
    ('p_paddr', 'addr'), # Reserved
    ('p_filesz', 'xword'), # Size of segment in file
    ('p_memsz', 'xword'), # Size of segment in memory
    ('p_align', 'xword'), # Alignment of segment
]

def program_header(code=b''):
    prefix_size = struct_len(ELF64_EHDR) + struct_len(ELF64_PHDR)
    p_vaddr = DEFAULT_ENTRY_POINT
    p_paddr = p_vaddr
    p_offset = 0 # load whole ELF file. TODO: why can't I just load the code? :(
    p_filesz = len(code)
    p_memsz  = len(code)
    return serialize_struct(ELF64_PHDR, dict(
        p_type=PT_LOAD,
        p_flags=PF_R | PF_W | PF_X,
        p_offset=p_offset,  # Offset in bytes from start of file
        p_vaddr=p_vaddr,    # virtual address in memory
        p_paddr=p_paddr,    # unused? reserved for physical addressing
        p_filesz=p_filesz,  # size in bytes of *file image* of segment
        p_memsz=p_memsz,    # size in bytes of *memory image* of segment
        p_align=0x4         # alignment (136/4)
    ))

# awesome syscalls table:
# http://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/

# Hello world program
# see asm_to_str script
code = b'\xb8rld\nPH\xb8hello woP\xb8\x01\x00\x00\x00\xbf\x01\x00\x00\x00H\x89\xe6\xba\x0c\x00\x00\x00\x0f\x05\xb8<\x00\x00\x00L\x89\xd7\x0f\x05'

if __name__ == "__main__":
    import sys
    data = b''.join([
        elf64_ehdr(),
        program_header(code),
        code
    ])
    # print(len(data))
    sys.stdout.buffer.write(data)
