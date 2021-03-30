import argparse
from pathlib import Path
from sys import stderr


class CpError(Exception):
    pass

def dump(src: Path, dest: Path):
    with open(src, 'rb') as s, open(dest,'wb') as d:
        d.write(s.read())

def copy_directory(src: Path, dest: Path):
    print('cp dir')


def copy_file(src: Path, dest: Path, override=False):
    if dest.is_dir():
        dest = dest / src.name
    if dest.is_file() and not override:
        raise CpError(f'Cannot override {dest}, specify -o or --override option')
    dest.touch()
    dump(src,dest)


def copy(src: str, dest: str,override=False):
    if(src.is_file()):
        copy_file(src, dest,override)
    elif src.is_dir():
        copy_directory(src, dest)
    else:
        raise CpError('File type not supported')


def cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog='cp',
        description='cp command implementation in Python'
    )
    parser.add_argument(
        '-o', '--override',
        action='store_true',
        help='Override destination files if they already exists'
    )
    parser.add_argument(
        'source',
        type=Path,
        help='Source directory or file'
    )
    parser.add_argument(
        'destination',
        type=Path,
        help='Destination directory or file'
    )

    return parser.parse_args()


def main():
    args = cli()
    try:
        copy(args.source, args.destination,args.override)
    except CpError as e:
        print(e, file=stderr)
        exit(1)


if __name__ == '__main__':
    main()
