"""
Nuitkaが、numpy/scipyが持つ共有ライブラリのrpathのうち"@loader_path/"で始まるものをビルド中に処理しようとして、エラーが出てビルドが出来ない。
それを防ぐために"@loader_path/"をあらかじめ解決しておく事前処理スクリプト

引数で指定したbase_directory以下にある.dylib/.soファイルのrpathをチェックし、
"@loader_path/"で始まるものを、<target_path(引数で指定したもの)>/<dylib name>に置き換える
"""

import argparse
import sys
from pathlib import Path
from typing import List, Set

from build_util_macos.shlib_tools import SharedLib, change_rpath_to_new_path, get_dylib_paths, get_so_paths

start_path = "@loader_path/"
parser = argparse.ArgumentParser()
parser.add_argument(
    "base_directory", help="fix the rpaths of the dylib/so under base_directory", type=str
)
parser.add_argument(
    "-t", "--target_path", help=f"alternative path of \"{start_path}\"", type=str, required=True
)
args = parser.parse_args()
base_dir_path = Path(args.base_directory)
target_path = Path(args.target_path)

if not (base_dir_path.exists() and base_dir_path.is_dir()):
    print("could not find the directory:", str(base_dir_path), file=sys.stderr)
    exit(1)

# base_dir_path以下の全てのサブディレクトリを探索して得た共有ライブラリのリスト
internal_shared_paths: List[Path] = get_so_paths(base_dir_path) + get_dylib_paths(base_dir_path)
# 全ての共有ライブラリファイル名のリスト
internal_shared_names: List[str] = [path.name for path in internal_shared_paths]

# @loader_path/で始まるrpathを持つ共有ライブラリのリスト
has_rpath_started_with_loader_path_shared: List[SharedLib] = []
for internal_shared_path in internal_shared_paths:
    lib = SharedLib(internal_shared_path)
    for rpath in lib.rpaths:
        if str(rpath).startswith(start_path):
            has_rpath_started_with_loader_path_shared.append(lib)
            break

# @loader_path/で始まるrpathの集合
rpaths_started_with_loader_path: Set[Path] = set()
for shared_lib in has_rpath_started_with_loader_path_shared:
    rpaths: Set[Path] = set([rpath for rpath in shared_lib.rpaths if str(rpath).startswith(start_path)])
    rpaths_started_with_loader_path = rpaths_started_with_loader_path.union(rpaths)

# @loader_path/で始まるrpathを、base_dir_path以下の共有ライブラリを指すように変更
for shared_lib in has_rpath_started_with_loader_path_shared:
    for dylib_path in shared_lib.rpaths:
        if not str(dylib_path).startswith(start_path):
            continue
        for replace_rpath in rpaths_started_with_loader_path:
            if dylib_path.name == replace_rpath.name:
                change_rpath_to_new_path(replace_rpath, target_path / dylib_path.name, shared_lib.path)
