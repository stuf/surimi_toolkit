#!/usr/bin/env python
from argparse import ArgumentParser
from PIL import Image
from PIL.ImageOps import invert
from pathlib import Path


class Config:
    path: str
    suffix: str
    verbose: bool
    dry_run: bool


config = Config()


def process(cfg: Config):
    IN_DIR = cfg.path
    SUFFIX = cfg.suffix

    files = Path(IN_DIR).rglob('*.png')
    file_list = [f for f in files if f.stem.endswith(SUFFIX)]

    total_file_count = len(file_list)
    processed_file_count = 0

    print(f'Using directory {IN_DIR}')
    print(f'Found {total_file_count} files.')

    for file in file_list:
        if cfg.verbose:
            print(f'{file.stem}')

        im = Image.open(file)

        if im.mode == 'RGBA':
            r, g, b, a = im.split()
            rr, gr, br, ar = im.getextrema()

            # Get the min/max values of the blue channel
            bmin, bmax = br

            # We can assume the channel will be the same value
            # If the minimum value of the blue channel is 0
            # let's invert the blue channel and save the image
            if bmin == 0:
                if cfg.verbose:
                    print(' - inverting blue channel')
                b = invert(b)

                im_ = Image.merge('RGBA', (r, g, b, a))

                if cfg.dry_run:
                    if cfg.verbose:
                        print(' - skipping actual operation')
                else:
                    im_.save(file)

                processed_file_count += 1

    print(f'Done. Processed {processed_file_count} file(s)')
    if cfg.dry_run:
        print(' - but because `dry run` was specified no files were actually changed.')


def main():
    parser = ArgumentParser(
        description="Ensure normalmaps point outward (simple)")

    parser.add_argument('path')
    parser.add_argument('-n', '--dry-run', action='store_true',
                        help='run as usual except without writing any files')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='print verbose information')
    parser.add_argument('--suffix', default='Nrm',
                        help='Suffix identifying normal maps')

    args = parser.parse_args(namespace=config)

    process(args)


if __name__ == '__main__':
    main()
