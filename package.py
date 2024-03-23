from argparse import ArgumentParser, BooleanOptionalAction
from _build._util import Path
import shutil

parser = ArgumentParser("package", description="package gdb for specified target")
parser.add_argument("target")
parser.add_argument("--force", action=BooleanOptionalAction)

args = parser.parse_args()

target = args.target
force = args.force

packages = Path("_packages").absolute()
gdbs = Path("_gdb").absolute()
cpython = Path("cpython").absolute()
binutils = Path("binutils-gdb").absolute()
docker = Path("_docker").absolute()
dist = packages / f"{target}-dist.tar.xz"

if not packages.exists():
    packages.mkdir()

gdb = gdbs / f"{target}-gdb"
if not gdb.exists():
    print(f"[-] {gdb} not found, cannot package")
    exit(1)

package = packages / f"{target}-dist"
if not args.force and package.exists():
    print(f"[-] {package} already exists")
    exit(1)

package.mkdir(exist_ok=True)

package_gdb = package / "gdb"
package_python_files = package / "python-files"
package_gdb_files = package / "gdb-files"
package_glibc_lang_stuff = package / "en"
package_run = package / "run.sh"
package_gdbinit = package / ".gdbinit"
package_gef = package / ".gdbinit-gef.py"

shutil.copyfile(gdb, package_gdb)
shutil.copytree(cpython / "Lib", package_python_files, dirs_exist_ok=True)
shutil.copytree(binutils / "gdb" / "data-directory", package_gdb_files, dirs_exist_ok=True)
shutil.copytree(docker / "en", package_glibc_lang_stuff, dirs_exist_ok=True)
shutil.copyfile(docker / "run.sh", package_run)
shutil.copyfile(docker / ".gdbinit", package_gdbinit)
shutil.copyfile(docker / ".gdbinit-gef.py", package_gef)
shutil.rmtree(package_python_files / "test")

package.run(f"{target}-strip gdb")

package_gdb.chmod(0o755)
package_run.chmod(0o755)

packages.run(f"tar cvfJ {dist} {package.relative_to(packages)}")

print(f"[+] done packaging {package}")