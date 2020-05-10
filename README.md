# XorPacker

XorPacker encrypts regularly compiled payloads. The resulting PE uses a bruteforce attack to decrypt the payload and evade sandbox.


## Packing unmanaged PE

1. Build Memory Module (x64 version):

```
apt install cmake
apt install g++-mingw-w64-x86-64 gcc-mingw-w64-x86-64 g++-mingw-w64-i686 gcc-mingw-w64-i686
git clone --recurse-submodules https://github.com/tmenochet/XorPacker
cd XorPacker/MemoryModule
mkdir build; cd build
cmake ..
make MemoryModule
```

Change the following line in CMakeLists.txt to build x86 version:

```
set (PLATFORM "i686" CACHE STRING "Platform to compile for")
```

2. Generate the packed PE:

```
python3 ./xorpacker.py -f mimikatz.exe -t UNMANAGED
```

3. Compile the resulting GO code:

```
apt install golang-go-windows-amd64 golang-go-windows-386
# Build x64 version
GOOS=windows GOARCH=amd64 CGO_ENABLED=1 CC=x86_64-w64-mingw32-gcc go build payload.go
# Build x86 version
GOOS=windows GOARCH=386 CGO_ENABLED=1 CC=i686-w64-mingw32-gcc go build payload.go
```


## Packing managed PE

1. Install Donut's Python extension:

```
pip3 install donut-shellcode
```

2. Generate the packed PE:

```
python3 ./xorpacker.py -f Grunt.exe -t MANAGED -a x64
```

3. Compile the resulting GO code:

```
GOOS=windows GOARCH=amd64 CGO_ENABLED=1 CC=x86_64-w64-mingw32-gcc go build payload.go
```


## Credits

* https://github.com/Sogeti-Pentest/Encrypter-Metasploit
* https://github.com/vyrus001/go-mimikatz
