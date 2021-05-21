import sys
from sh import docker, cp
from pytest import fail
from pathlib import Path

def test_container_build():
    res = docker('build', '-t', 'pu-md:latest', '.')
    print(res)
    assert res

def test_hello_world(tmp_path):
    cp('-r', 'test/example_docs', tmp_path)
    doc_path = '%s/example_docs' % tmp_path
    print("Reading the doc path %s" % doc_path)
    res = docker('run', '--rm', '-v','%s:/app' % doc_path, 'pu-md', _out=sys.stdout, _err=sys.stderr)
    assert res.exit_code == 0, "We should successfully run the formatter"
    # TODO: maybe there is something better? to test this with i mean
    assert Path('%s/diagram.png' % doc_path).is_file(), "Default path diagram is parsed"
