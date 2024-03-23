import json
import shutil
import os
import traceback
from _build._util import Path, download
from argparse import ArgumentParser

def warn(msg):
    print(f"[-] WARNING: {msg}")

class Main:
    def __init__(self, config):
        self.config = config
        self.modules = config["modules"]
        self.env = dict(os.environ)
        self.cwd = Path(".").absolute()

    def request(self, module: str):
        print(f"[+] building {module}")

        if options := self.modules.get(module):
            options.setdefault("name", module)

            try:
                spec = __import__(f"_build.{module}", fromlist=("_build", ))

                try:
                    spec.build(self, options)
                    return self.cwd / module / "_build" / "_prefix"
                except Exception as e:
                    print(traceback.format_exc())
                    warn(f"error building override {module}: {e}")

            except ImportError as e:

                try:
                    self.defaultbuild(module, options)
                    return self.cwd / module / "_build" / "_prefix"
                except Exception as e:
                    warn(f"error building default {module}: {e}")
        else:
            warn(f"module {module} does not exist")
            return

        raise RuntimeError(f"failed to build {module}")
    
    def genconfig(self, source: Path):
        autogen = source / "autogen.sh"
        configure = source / "configure"

        if not configure.exists():
            if autogen.exists():
                source.run("./autogen.sh")
            else:
                raise RuntimeError(f"could not determine how to build {source}")
            

    def dependon(self, installs: list[Path]):
        env = dict(os.environ)
        ldflags = " "
        cflags = " "
        pkgconfigs = []

        for install in installs:
            lib, lib32, lib64 = install / "lib", install / "lib32", install / "lib64"
            include = install / "include"
            ldflags += f"-L{lib} -L{lib32} -L{lib64} "
            cflags += f"-I{include} "
            pkgconfigs.append(lib / "pkgconfig")

        pkgconfigs = map(lambda p: str(p.absolute()), pkgconfigs)
        pkgconfigs = ":".join(pkgconfigs)

        env.setdefault("LDFLAGS", "")
        env.setdefault("CFLAGS", "")
        env.setdefault("CPPFLAGS", "")
        env.setdefault("CXXFLAGS", "")
        env.setdefault("PKG_CONFIG_PATH", "")
        env["LDFLAGS"] += ldflags
        env["CFLAGS"] += cflags
        env["CFLAGS"] += "-fno-builtin "
        env["LDFLAGS"] += "-fno-builtin "

        return env
    
    def defaultbuild(self, module: str, options):
        source = download(options, {})

        artifacts = source / "_build"

        if not artifacts.exists():
            artifacts.mkdir()

            self.genconfig(source)
            
            host = self.config.get("host")
            prefix = (artifacts / "_prefix").absolute()

            depends = options.get("depends", [])
            depends = map(lambda dep: main.request(dep), depends)
            env = self.dependon(depends)
            env["CFLAGS"] += "-fPIC "

            artifacts.run(f"""
                          ../configure --enable-shared --enable-static --host={host} --prefix={prefix}
                          """,
                          env=env)
            artifacts.run(f"make -j6")
            artifacts.run(f"make install")

parser = ArgumentParser("build", description="builds specified module and all their dependencies")
parser.add_argument("module")
parser.add_argument("--config", default="./config.json")

args = parser.parse_args()

with open(args.config, "rb") as fp:
    config = json.load(fp)

main = Main(config)
main.request(args.module)
