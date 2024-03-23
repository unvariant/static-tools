from ._util import *

defaults = {}

def build(main, options):
    source = download(options, defaults)

    artifacts = source / "_build"

    if not artifacts.exists():
        artifacts.mkdir()

        atomic_ops = main.request("atomic_ops")
        atomic_ops = main.cwd / "atomic_ops"
        (source / "libatomic_ops").symlink_to(atomic_ops, target_is_directory=True)
        
        main.genconfig(source)
        
        host = main.config.get("host")
        prefix = (artifacts / "_prefix").absolute()


        gmp = main.request("gmp")
        unistring = main.request("unistring")
        env = main.dependon([gmp, unistring])

        artifacts.run(f"""
                      ../configure --enable-shared --enable-static --host={host} --prefix={prefix}
                      """,
                      env=env)
        artifacts.run(f"make -j6")
        artifacts.run(f"make install")