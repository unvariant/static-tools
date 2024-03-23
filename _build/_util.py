import subprocess
import pathlib
import os

def run(cmd, capture=False, check=True, cwd=None, **kwargs):
    if capture:
        kwargs["capture_output"] = True
        kwargs["encoding"] = "utf-8"

    kwargs["check"] = check
    kwargs["cwd"] = cwd
    
    handle = subprocess.run(cmd.replace("\n", " "), shell=True, **kwargs)
    return handle

def download(options, defaults):
    name = options.get("name")
    source = Path(name).absolute()

    if source.exists():
        # print(f"[-] WARNING: {source} already exists")
        return source
    
    for strategy, val in options.items():
        if strategy == "git":
            try:
                url = val
                branch = options.get("branch")
                run(f"git clone --depth 1 --branch {branch} {url} {source}")
                break
            except subprocess.CalledProcessError as e:
                print(f"[-] WARNING: git failed with {e}")
                pass

        elif strategy == "tarball":
            try:
                source.mkdir()

                tarballs = Path("_tarballs")
                tarballs.mkdir(exist_ok=True)

                url = val
                tarball = tarballs / f"{name}.tar"

                if not tarball.exists():
                    run(f"wget {url} -O {tarball}")

                run(f"tar -xf {tarball} -C {source}")

                files = list(source.glob("*"))
                for file in files[0].glob("*"):
                    file.rename(source / file.name)
                files[0].rmdir()

                break
            except subprocess.CalledProcessError:
                print(f"[-] WARNING: tarball failed with {e}")
                source.rmdir()
                pass

    else:
        raise RuntimeError(f"failed to download source for {name}")
    
    return source

class Path(type(pathlib.Path())):
    def run(self, cmd, **kwargs):
        if self.is_dir():
            return run(cmd, cwd=self, **kwargs)
        else:
            raise IsADirectoryError("expected a directory")