""" A definitely-not-complete list of some useful constants for generating an
    ELF64 file
"""

ET_EXEC = 2

EV_CURRENT = 1

# see https://software.intel.com/sites/default/files/article/402129/mpx-linux64-abi.pdf
EM_X86_64 = 62

SHN_UNDEF=0

PT_LOAD=1

PF_X = 0x1
PF_W = 0x2
PF_R = 0x4
