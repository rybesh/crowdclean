#! /usr/bin/env python
# Runs a cleaning function on a set of pages,
# and produces patches with the changes made.

import difflib
import os

def process_page(page, cleaner):
    before = page.splitlines(True)
    after = cleaner(page).splitlines(True)
    patch = difflib.unified_diff(before, after)
    html = difflib.HtmlDiff(wrapcolumn=25).make_file(before, after)
    return patch, html

def process_file(f, cleaner):
    patch, html = process_page(f.read(), cleaner)
    filename = os.path.splitext(f.name)[0] + '-%s.diff' % cleaner.name
    with open(filename, 'w') as patchfile:
        patchfile.writelines(patch)
    with open(filename + '.html', 'w') as htmlfile:
        htmlfile.write(html)

def load_cleaner(name):
    fname = 'clean_%s' % name
    imp = __import__('cleaners', globals(), locals(), [ fname ])
    cleaner = getattr(imp, fname)
    cleaner.name = name
    return cleaner

def main():
    import sys
    try:
        cleaner = load_cleaner(sys.argv[1])
    except AttributeError:
        sys.exit("No cleaner named '%s'" % sys.argv[1])
    for arg in sys.argv[2:]:
        try:
            with open(arg) as f:
                process_file(f, cleaner)
        except IOError as e:
            sys.exit(e)

if __name__ == '__main__':
    main()
