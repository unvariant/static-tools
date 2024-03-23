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

        env = main.dependon([])
        env["CHOST"] = host
        env["CFLAGS"] += "-fPIC "
        env["LDFLAGS"] += "-fPIC "

        artifacts.run(f"""
                      ../configure --static --prefix={prefix}
                      """,
                      env=env)
        artifacts.run(f"make -j6")
        artifacts.run(f"make install")

        artifacts.run(f"""
                      ../configure --prefix={prefix}
                      """,
                      env=env)
        artifacts.run(f"make -j6")
        artifacts.run(f"make install")