#!/usr/bin/env python

from redbaron import RedBaron

def main(filename):
    with open(filename, 'rt') as f:
        source = f.read()

    red = RedBaron(source)

    for assign in red.find_all('assignment'):
        target = assign.target.name
        constant = assign.value.find(['string', 'int', 'list'])

        print('{} = {}'.format(target, constant))

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
