from Cython.Distutils import build_ext
from distutils.core import setup
from distutils.extension import Extension
from glob import iglob
import os
import sys


# python cython_setup.py build_ext --inplace
if len(sys.argv) == 1:  # If no CLI args are included, add some by default
    sys.argv.append("build_ext")
    sys.argv.append("--inplace")

option = {}
if os.name == "nt":
    option['extra_compile_args'] = [
        '/EHsc', # 警告回避
        '/MT', # /MDオプション上書き
        ]

for pyxname in iglob("go/*.pyx"):
    name, ext = os.path.splitext(pyxname)
    name = name.replace(os.sep, ".")
    ext_modules = [Extension(name, [pyxname], **option)]
    setup(
        name = name,
        cmdclass = {'build_ext': build_ext},
        ext_modules = ext_modules
    )
