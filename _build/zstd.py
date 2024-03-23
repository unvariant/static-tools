from ._util import *

defaults = {}

def build(main, options):
    source = download(options, defaults)

    artifacts = source / "_build"

    if not artifacts.exists():
        artifacts.mkdir()
        
        host = main.config.get("host")
        prefix = (artifacts / "_prefix").absolute()

        env = main.dependon([])
        env["CC"] = f"{host}-gcc"
        env["CXX"] = f"{host}-g++"

        artifacts.run(f"cmake -DCMAKE_INSTALL_PREFIX={prefix} ../build/cmake", env=env)
        artifacts.run("make -j6")
        artifacts.run("make install")