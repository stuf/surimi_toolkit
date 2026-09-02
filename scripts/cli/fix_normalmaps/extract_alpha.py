#!/usr/bin/env python
from argparse import ArgumentParser
from PIL import Image
from PIL.ImageOps import invert
from pathlib import Path
from pprint import pprint, pp


class Config:
    path: str
    suffix: str
    opa_suffix: str
    verbose: bool
    dry_run: bool

    def __repr__(self):
        return f'Config( ' \
            f'path={self.path}, ' \
            f'suffix={self.suffix}, ' \
            f'opa_suffix={self.opa_suffix}' \
            f'verbose={self.verbose}, ' \
            f'dry_run={self.dry_run})'


config = Config()


def process(cfg: Config):
    files = Path(cfg.path).rglob('*.png')
    file_list = [f for f in files if f.stem.endswith(cfg.suffix)]

    for f in file_list:
        im = Image.open(f)
        fp = Path(f)
        opa_tex = ''.join([fp.stem.replace(cfg.suffix, ''), cfg.opa_suffix])

        fpp = list(fp.parts)
        fpp[-1] = f'{opa_tex}{fp.suffix}'
        fp2 = Path(*fpp)

        if fp2.exists():
            if cfg.verbose:
                print(f' - exists? {fp2=} {fp2.exists()}')
                print(f'   skipping')
            continue

        alpha = im.getchannel('A')

        pix_min, pix_max = alpha.getextrema()

        if pix_min == 255:
            if cfg.verbose:
                print(' - No transparency in image')
            continue

        bg = Image.new('RGBA', im.size, (0, 0, 0, 255))
        bg.paste(alpha, mask=alpha)
        bg.convert('L')

        print(f' - Saving opacity texture: {fp2.relative_to(cfg.path)}')

        if not cfg.dry_run:
            bg.save(str(fp2))
        # pp(file_list)


def main():
    parser = ArgumentParser(
        description='Extract image alpha into its own file')

    parser.add_argument('path')
    parser.add_argument('-n', '--dry-run', action='store_true')
    parser.add_argument('-v', '--verbose', action='store_true')

    parser.add_argument('--suffix', default='Alb')
    parser.add_argument('--opa-suffix', default='Opa')

    args = parser.parse_args(namespace=config)

    process(args)


if __name__ == '__main__':
    main()


def asd():
    IN_DIR = r'W:\assets\Decals\Stickers'

    SUFFIX = 'Opa'

    files = Path(IN_DIR).rglob('*.png')

    file_list = [f for f in files if not f.stem.endswith(SUFFIX)]

    for f in file_list:
        im = Image.open(f)
        fp = Path(f)
        opa_tex = '_'.join([fp.stem, SUFFIX])

        fpp = list(fp.parts)
        fpp[-1] = f'{opa_tex}{fp.suffix}'
        fp2 = Path(*fpp)

        if fp2.exists():
            print(f' - exists? {fp2=} {fp2.exists()}')
            print(f'   skipping')
            continue

        alpha = im.getchannel('A')

        pix_min, pix_max = alpha.getextrema()

        if pix_min == 255:
            print(' - No transparency in image')
            continue

        bg = Image.new('RGBA', im.size, (0, 0, 0, 255))
        bg.paste(alpha, mask=alpha)
        bg.convert('L')

        print(f' - Saving opacity texture: {fp2.relative_to(IN_DIR)}')
        bg.save(str(fp2))
