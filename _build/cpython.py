from ._util import *

defaults = {}

def build(main, options):
    source = download(options, defaults)

    artifacts = source / "_build"

    if not artifacts.exists():
        artifacts.mkdir()

        main.genconfig(source)
        
        host = main.config.get("host")
        prefix = (artifacts / "_prefix").absolute()

        with open(source / "Modules" / "Setup.local", "w+") as setup:
            setup.write(
"""
# Edit this file for local setup changes
*static*

_blake2 _blake2/blake2module.c _blake2/blake2b_impl.c _blake2/blake2s_impl.c
_md5 md5module.c
_sha1 sha1module.c
_sha256 sha256module.c
_sha512 sha512module.c
_sha3 _sha3/sha3module.c

# _codecs_cn cjkcodecs/_codecs_cn.c
# _codecs_hk cjkcodecs/_codecs_hk.c
_codecs_iso2022 cjkcodecs/_codecs_iso2022.c
# _codecs_jp cjkcodecs/_codecs_jp.c
# _codecs_kr cjkcodecs/_codecs_kr.c
# _codecs_tw cjkcodecs/_codecs_tw.c
_multibytecodec cjkcodecs/multibytecodec.c
unicodedata unicodedata.c

_asyncio _asynciomodule.c
_bisect _bisectmodule.c
_contextvars _contextvarsmodule.c
_csv _csv.c
_datetime _datetimemodule.c
_decimal _decimal/_decimal.c
_heapq _heapqmodule.c
_json _json.c
_lsprof _lsprof.c rotatingtree.c
_multiprocessing -I$(srcdir)/Modules/_multiprocessing _multiprocessing/multiprocessing.c _multiprocessing/semaphore.c
_opcode _opcode.c
_pickle _pickle.c
_queue _queuemodule.c
_random _randommodule.c
_socket socketmodule.c
_statistics _statisticsmodule.c
_struct _struct.c
_typing _typingmodule.c
_zoneinfo _zoneinfo.c
array arraymodule.c
audioop audioop.c
binascii binascii.c
cmath cmathmodule.c
math mathmodule.c
mmap mmapmodule.c
select selectmodule.c

_posixsubprocess _posixsubprocess.c
_posixshmem -I$(srcdir)/Modules/_multiprocessing _multiprocessing/posixshmem.c -lrt
fcntl fcntlmodule.c
grp grpmodule.c
ossaudiodev ossaudiodev.c
resource resource.c
spwd spwdmodule.c
syslog syslogmodule.c
termios termios.c

zlib  zlibmodule.c -lz
_ctypes _ctypes/_ctypes.c _ctypes/callbacks.c _ctypes/callproc.c _ctypes/stgdict.c _ctypes/cfield.c -ldl -lffi -lc -DHAVE_FFI_PREP_CIF_VAR -DHAVE_FFI_PREP_CLOSURE_LOC -DHAVE_FFI_CLOSURE_ALLOC
"""
            )

        site = (artifacts / "config.site").absolute()
        with open(artifacts / "config.site", "w+") as f:
            f.write(
"""
ac_cv_file__dev_ptmx=no
ac_cv_file__dev_ptc=no
""")

        ffi = main.request("ffi")
        b2 = main.request("b2")
        zlib = main.request("zlib")
        readline = main.request("readline")
        mpdecimal = main.request("mpdecimal")

        # build shared

        env = main.dependon([ffi, b2, zlib, readline, mpdecimal])
        env["CONFIG_SITE"] = site
        source.run(f"""
                      ./configure
                      --prefix={prefix}
                      --host={host}
                      --enable-shared
                      --build=x86_64-linux-gnu
                      --with-build-python=python3.11
                      --disable-ipv6
                      --enable-optimizations
                      """,
                      env=env)
        source.run(f"make -j6", env=env)
        source.run(f"make install", env=env)

        # build static

        env = main.dependon([ffi, b2, zlib, readline, mpdecimal])
        env["CFLAGS"] += "-fPIC "
        env["LDFLAGS"] += "-static -Wl,-no-export-dynamic -static-libgcc -fPIC "
        env["CPPFLAGS"] += "-static -fPIC "
        env["DYNLOADFILE"] = "dynload_stub.o"
        env["CONFIG_SITE"] = site
        env["LINKFORSHARED"] = " "

        source.run(f"""
                      ./configure
                      --prefix={prefix}
                      --host={host}
                      --build=x86_64-linux-gnu
                      --with-static-libpython
                      --with-build-python=python3.11
                      --disable-ipv6
                      --enable-optimizations
                      """,
                      env=env)
        source.run(f"make -j6", env=env)
        source.run(f"make install", env=env)

        staticlibpython = prefix / "lib" / "libpython3.11.a"
        source.run(f"cp libpython3.11.a {staticlibpython}")