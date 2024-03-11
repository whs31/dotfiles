#!/bin/python

import os
from shutil import *


def copytree(src, dst, symlinks=False, ignore=None):
    names = os.listdir(src)
    if ignore is not None:
        ignored_names = ignore(src, names)
    else:
        ignored_names = set()

    if not os.path.isdir(dst): # This one line does the trick
        os.makedirs(dst)
    errors = []
    for name in names:
        if name in ignored_names:
            continue
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                copytree(srcname, dstname, symlinks, ignore)
            else:
                # Will raise a SpecialFileError for unsupported file types
                copy2(srcname, dstname)
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except (Error, err):
            errors.extend(err.args[0])
        except (EnvironmentError, why):
            errors.append((srcname, dstname, str(why)))
    try:
        copystat(src, dst)
    except (OSError, why):
        if WindowsError is not None and isinstance(why, WindowsError):
            # Copying file access times may fail on Windows
            pass
        else:
            errors.extend((src, dst, str(why)))
    if errors:
        raise (Error, errors)


if __name__ == '__main__':
    copytree(os.path.expanduser('~/.config/kitty'), './kitty')
    copytree(os.path.expanduser('~/.config/hypr'), './hypr')
    copyfile(os.path.expanduser('~/.zshrc'), './.zshrc')