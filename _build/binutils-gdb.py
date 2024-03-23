from ._util import *
from shutil import copyfile

defaults = {}

def build(main, options):
    source = download(options, defaults)

    artifacts = source / "_build"
    gdb = source / "gdb"

    if not artifacts.exists():
        artifacts.mkdir()

        main.genconfig(source)
        
        host = main.config.get("host")
        prefix = (artifacts / "_prefix").absolute()

        mpfr = main.request("mpfr")
        gmp = main.request("gmp")
        cpython = main.request("cpython")
        mpdecimal = main.request("mpdecimal")
        b2 = main.request("b2")
        zlib = main.request("zlib")
        ffi = main.request("ffi")
        env = main.dependon([mpfr, gmp, mpdecimal, b2, zlib, ffi, cpython])

        deps = " -lmpfr -lgmp -lmpdec -lmpdec++ -lb2 -lz -lffi "
        env["CFLAGS"] += deps
        env["LDFLAGS"] += deps
        env["CXXFLAGS"] += deps
        env["SILENCE_FLAG"] = " "

        python = cpython / "bin" / "python3.11"

        source.run(f"""
                   ./configure
                   --enable-static
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
                   --with-system-gdbinit=/etc/gdb/gdbinit
                   """,
                      env=env)

        with open(gdb / "silent-rules.mk", "a+") as f:
            f.write("\nSILENT_FLAG =\n")
        
        logfile = artifacts / "_build.log"
        search = "libtool: link: "
        log: str = source.run(f"make -j6 2>&1 | tee {logfile} | grep '^{search}'", env=env, capture=True).stdout
        source.run(f"make install")

        logs = log.splitlines()
        for log in logs:
            if " gdb.o" in log:
                break

        if log.startswith(search):
            log = log[len(search):]

        log = log.replace(".so ", ".a ")
        log += deps + " -static "

        gdb.run(log)
        
        copyfile(gdb / "gdb", Path("_gdb") / f"{host}-gdb")