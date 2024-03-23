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

        gmp = main.request("gmp")
        iconv = main.request("iconv")
        intl = main.request("intl")
        ltdl = main.request("ltdl")
        unistring = main.request("unistring")
        gc = main.request("gc")
        ffi = main.request("ffi")

        env = main.dependon([gmp, iconv, intl, ltdl, unistring, gc, ffi])

        source.run(f"""
                      ./configure --enable-shared --enable-static --host={host} --prefix={prefix}
                      """,
                      env=env)
        source.run(f"make -j6")
        source.run(f"make install")