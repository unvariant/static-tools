import json
import shutil
from _build._util import Path
from argparse import ArgumentParser

parser = ArgumentParser("clean", description="helper to delete module source files")
parser.add_argument("--config", default="config.json")

args = parser.parse_args()

with open(args.config, "rb") as fp:
    config = json.load(fp)

for module, options in config["modules"].items():
    module = Path(module)

    if module.exists():
        # dont want to accidentally delete something important
        assert len(module.parts) == 1
        assert not module.is_symlink()
        assert module.is_dir()

        shutil.rmtree(module)