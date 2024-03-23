from ._util import *

defaults = {}

def build(main, options):
    raise RuntimeError("this does not work. use binutils-gdb instead to build gdb")

    main.request("binutils-gdb")

    host = main.config.get("host")
    source = Path("binutils-gdb").absolute() / "gdb"
    artifacts = source / "_build"
    prefix = artifacts / "_prefix"

    if not artifacts.exists():
        artifacts.mkdir()

        main.genconfig(source)

        gmp = main.request("gmp")
        mpfr = main.request("mpfr")
        cpython = main.request("cpython")
        readline = main.request("readline")
        zlib = main.request("zlib")
        mpdecimal = main.request("mpdecimal")
        ffi = main.request("ffi")
        b2 = main.request("b2")
        env = main.dependon([gmp, mpfr, cpython, readline, zlib, mpdecimal, ffi, b2])

        stuff = "-static-libgcc -lgmp -lmpfr -lz -lmpdec -lmpdec++ -lb2 -lffi -static -Wl,-static "

        env["CXXFLAGS"] += env["LDFLAGS"] + env["CFLAGS"]
        env["CXXFLAGS"] += stuff
        env["LDFLAGS"] += stuff
        env["CFLAGS"] += stuff
        env["ECHO_CXXLD"] = "echo"

        python = cpython / "bin" / "python3.11"

        version = source / "version-t.t"
        if not version.exists():
            version.symlink_to("./version.c")

        source.run(f"""
                    ./configure
                    --enable-static
                    --disable-shared
                    --host={host}
                    --prefix={prefix}
                    --disable-nls
                    --disable-gprofng
                    --disable-source-highlight
                    --disable-guile
                    --disable-debuginfod
                    --with-python={python}
                    --with-gmp={gmp}
                    --with-mpfr={mpfr}
                    --with-readline={readline}
                    --with-system-gdbinit=/etc/gdb/gdbinit
                    --enable-targets={host}
                    """, env=env)
        
        source.run("make -j6", env=env)