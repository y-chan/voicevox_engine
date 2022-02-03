"""
引数で指定したbase_directory以下にある.dylibのinstall idを、<base_directory>/<dylib name>に置き換える
"""
import argparse
import sys
from pathlib import Path
from typing import List

from build_util_macos.shlib_tools import change_install_id, get_dylib_paths

parser = argparse.ArgumentParser()
parser.add_argument(
    "base_directory",
    help="fix the install id of the dylib under base_directory",
    type=str,
)
args = parser.parse_args()
base_dir_path = Path(args.base_directory)

if not (base_dir_path.exists() and base_dir_path.is_dir()):
    print("could not find the directory:", str(base_dir_path), file=sys.stderr)
    exit(1)

dylib_paths: List[Path] = get_dylib_paths(base_dir_path)

for dylib_path in dylib_paths:
    change_install_id(base_dir_path / dylib_path.name, dylib_path)
