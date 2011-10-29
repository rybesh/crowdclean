#! /usr/bin/env python
# Splits a text file with page breaks into separate files for each page.

import os

def split_file(f):
    head, tail = os.path.split(f.name)
    pagesdir = os.path.join(head, tail.replace('.', '_') + '-pages') 
    if not os.path.exists(pagesdir):
        os.mkdir(pagesdir)
    for i, page in enumerate(f.read().split('\f')):
        path = os.path.join(pagesdir, 'page-%s' % (str(i).rjust(2, '0')))
        with open(path + '.txt', 'w') as pagefile:
            pagefile.write(page)

def main():
    import sys
    for arg in sys.argv[1:]:
        try:
            with open(arg) as f:
                split_file(f)
        except IOError as e:
            sys.exit(e)

if __name__ == '__main__':
    main()
