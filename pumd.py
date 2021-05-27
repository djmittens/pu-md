import re
import sys
from pathlib import PurePath
from sh import rg, cat, java, ErrorReturnCode_2, ErrorReturnCode_1
# TODO: Create ci pipeline, and publish an artifact to github
# TODO: Add argparse library
# TODO: Add logging library
# TODO: Think through how i want to handle doc root. (eg what to treat as the root of the documentation)
# TODO: Multiplex plantuml file processing.
# TODO: add assertions on the files being present in the right location.
# BUG: Fix a bug where the directory path must exist or somethign.
# BUG: Scans all files in the directory, add feature to support filtering only files in the staged changeset.
# BUG: Relative paths can point to a folder not included in the mount.
# cat: can't open '/app/<!-- ./diagram.pu': No such file or directory
# Generating diagram /app/app.pu => /app/diagram.png
# Generating diagram /app/<!-- ./diagram.pu => /app/assets/diagram.svg -->
# BUG: Filetypes are not properly parsed, eg `.svg` extension produces a `png` file.

reg = re.compile('(.+):(.+)')

def find_all_files():
    res = rg('-N', '!\\[(.*\\.pu)\\]\\((.*)\\)', '-r', '$1:$2', '/app')
    files = {}
    file = ''
    for line in res:
        r = read_rg_output(line)
        if type(r) is tuple:
            files[file].append(r)
        else:
            file = r
            files[file] = []
    return files

def read_rg_output(s):
    # Either a new file name, or pu:file pair.
    res = reg.match(s)
    if res:
        return (res.group(1), res.group(2))
    else:
        # new file
        return s

def full_source_path(md, pu):
    return PurePath(md).parent.joinpath(pu)

def gen_image(src, dest):
    print('Generating diagram %s => %s' % (src, dest))
    java(cat(src, _piped=True), '-jar', '/plantuml.jar', '-pipe', _out=str(dest), _err=sys.stdout)

if __name__ == "__main__":
    # TODO: Refactor this bad boii
    try:
        files = find_all_files()
        for src, dsts in files.items():
            for dst in dsts:
                gen_image(full_source_path(src, dst[0]),full_source_path(src, '/app/' + dst[1]))
    except(ErrorReturnCode_1):
        print("Something went wrong with rg or something")
        pass

    except(ErrorReturnCode_2):
        # In case we have not found any files to do, dont do anything
        print("Did not find any files to generate")
        pass

def test_read_rg_output():
    res = read_rg_output("hello")
    assert type(res) is str
    res = read_rg_output('fuck.p:you')
    assert type(res) is tuple

def test_full_source_path():
    res = full_source_path('/home/ghosts/Fuckface.md', '../something/fuckfile.pu')
    assert res == PurePath('/home/ghosts/../something/fuckfile.pu')
