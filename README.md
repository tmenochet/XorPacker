# XorPacker

XorPacker encrypts regularly compiled PE files. The resulting PE uses a bruteforce attack to decrypt the payload and evade sandbox.

## Usage

1. Generate the encoded PE:

```
./xorpacker.py mimikatz.exe
```

2. Compile the resulting GO code:

```
# Build x64 version
GOOS=windows GOARCH=amd64 CGO_ENABLED=1 CC=x86_64-w64-mingw32-gcc go build payload.go
# Build x86 version
GOOS=windows GOARCH=386 CGO_ENABLED=1 CC=i686-w64-mingw32-gcc go build payload.go
```

## Install

* Install required packages:

```
apt-get install cmake
apt-get install golang-go-linux-386 golang-go-windows-386 golang-go-windows-amd64
apt-get install g++-mingw-w64-x86-64 g++-mingw-w64-i686 gcc-mingw-w64-i686 gcc-mingw-w64-x86-64
```

* Build Memory Module (x64 version):

```
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

## Credits

* https://github.com/Sogeti-Pentest/Encrypter-Metasploit
* https://github.com/vyrus001/go-mimikatz
