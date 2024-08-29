#!/usr/bin/env python
import subprocess
import textwrap
import time
from pprint import pprint
from argparse import ArgumentParser
from glob import glob
from pathlib import Path
from textwrap import indent

INDENT_STEP = 2
INDENT_CHAR = ' '
I1 = INDENT_CHAR * INDENT_STEP
I2 = INDENT_CHAR * (INDENT_STEP * 2)
I3 = INDENT_CHAR * (INDENT_STEP * 3)


if __name__ == '__main__':
    parser = ArgumentParser(description='Converts DAE files to FBX')

    parser.add_argument('path')
    parser.add_argument('-t', '--tool', dest='tool',
                        action='store_const',
                        help='Path to DAE to FBX converter tool',
                        default=r'C:\Program Files\Autodesk\FBX\FBX Converter\2013.3\bin\FbxConverter.exe')
    parser.add_argument('-r', '--recursive',
                        help='Search in subdirectories',
                        action='store_true')

    #

    args = parser.parse_args()
    path = Path(args.path)
    glob_pattern = '**/*.dae' if args.recursive else '*.dae'
    print(f'Searching path {path} for files')

    start_time = time.time()
    timing = []

    t1 = time.time()
    files = [Path(path / p) for p in glob(
        glob_pattern, root_dir=args.path, recursive=args.recursive)]
    t2 = time.time() - t1
    timing.append(('file search', t2))

    file_count = len(files)

    convertable: list[tuple[Path, Path]] = []
    directories = set()

    t1 = time.time()
    # Collect files to convert
    for f in files:
        fbx_file = f.with_suffix('.fbx')
        directories.add(f.parent)

        if not fbx_file.exists():
            convertable.append((f, fbx_file))
    t2 = time.time() - t1
    timing.append(('determine convertable', t2))

    to_convert_count = len(convertable)
    dir_count = len(directories)
    converted = 0
    convert_time_total = 0

    print(f'Found {file_count} .dae file(s) in {dir_count} folder(s)')

    t1 = time.time()
    if to_convert_count:
        print(indent(f'- Found {to_convert_count} file(s) to process.', I1))

        for dae, fbx in convertable:
            dae_ = dae.relative_to(path)
            fbx_ = fbx.relative_to(path)

            print(indent(f'Convert: {dae_} -> {fbx_}', I2))

            tc1 = time.time()
            subprocess.run([args.tool, str(dae), str(fbx)])
            print(indent('Done.', I3))
            tc2 = time.time() - tc1
            convert_time_total += tc2
            converted += 1
    t2 = time.time() - t1
    timing.append(('conversion', t2))
    timing.append(('conversion (mean per file)',
                  convert_time_total / converted))

    if to_convert_count and converted:
        print('')
        print(f'Converted {converted} file(s).')

    pprint(timing)
