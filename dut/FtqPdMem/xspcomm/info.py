import os
import sys
from .pyxspcomm import version

def path_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def path_include():
    return os.path.join(path_root(), "include")

def path_lib():
    return os.path.join(path_root(), "lib")

def path():
    return "XSPCOMM_ROOT=%s XSPCOMM_INCLUDE=%s XSPCOMM_LIB=%s" % (path_root(), path_include(), path_lib())

def export_path():
    print("export %s" % path())

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "--export":
            export_path()
        if sys.argv[1] == "--version":
            print(version())
        if sys.argv[1] == "--root":
            print(path_root())
        if sys.argv[1] == "--include":
            print(path_include())
        if sys.argv[1] == "--lib":
            print(path_lib())
        if sys.argv[1] == "--path":
            print(path())
        if sys.argv[1] == "--help":
            print("Usage: python -m xspcomm.info [option]")
            print("--help:    print this help")
            print("--export:  print export cmd of XSPCOMM_ROOT, XSPCOMM_INCLUDE, XSPCOMM_LIB")
            print("--version: print python wrapper version")
            print("--root:    print xcomm root path")
            print("--include: print xcomm include path")
            print("--lib:     print xcomm lib path")
            print("--path:    print xcomm all path [default]")
    else:
        print(path())

if __name__ == "__main__":
    main()
