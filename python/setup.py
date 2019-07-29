#!/usr/bin/env python3

'''
Setup for SWIG Python bindings for lex-tools
'''
import platform
from os import path
from distutils.core import Extension, setup
from distutils.command.build import build
import distutils.cygwinccompiler


class CustomBuild(build):
    if platform.system() == 'Windows':
        distutils.cygwinccompiler.get_msvcr = lambda: []

        def initialize_options(self):
            super(CustomBuild, self).initialize_options()
            self.compiler = 'mingw32'

    sub_commands = [
        ('build_ext', build.has_ext_modules),
        ('build_py', build.has_pure_modules),
        ('build_clib', build.has_c_libraries),
        ('build_scripts', build.has_scripts),
    ]


def get_sources():
    sources = ['lex_tools.i']
    cc_sources = ['lrx_processor.cc']
    rel_path = '..'
    sources.extend(path.join(rel_path, f) for f in cc_sources)
    return sources

def get_include_dirs():
    # Remove '-I' from Flags, as python add '-I' on its own
    dirs = '-I/usr/local/include/lttoolbox-3.5 -I/usr/local/lib/lttoolbox-3.5/include -I/usr/include/libxml2 '.replace('-I', '').split()
    dirs += '-lxml2 '.replace('-I', '').split()
    return dirs + ['..']


lextools_module = Extension(
    name='_lextools',
    sources=get_sources(),
    swig_opts=['-c++', '-I..', '-Wall']+\
        '-I../../lttoolbox/lttoolbox -I../../lttoolbox '.split(),
    include_dirs=[
    '..',
    '../../lttoolbox',
    '../../lttoolbox/lttoolbox',
    '../../externallibs/win64/libxml2-2.9.3-win32-x86_64/include/libxml2',
    '../utf8',
    '../../externallibs/win64/iconv-1.14-win32-x86_64/include',
    ],
    library_dirs= [
    '../../externallibs/win64/libxml2-2.9.3-win32-x86_64/lib',
    '../../externallibs/win64/local-build',
    ],
    extra_compile_args='-Wall -Wextra -g -O2 -std=c++2a'.split(),
    extra_link_args=['-lxml2', '-llttoolbox3'],
)

setup(
    name='apertium-lex-tools',
    version='0.2.1',
    description='SWIG interface to apertium-lex-tools',
    long_description='SWIG interface to apertium-lex-tools for use in apertium-python',
    # TODO: author, maintainer, url
    author_email='ftyers@prompsit.com',
    license='GPL-3.0+',
    maintainer_email='ftyers@prompsit.com',
    cmdclass={'build': CustomBuild},
    ext_modules=[lextools_module],
    py_modules=['lextools'],
)
