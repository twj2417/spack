##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import pytest
import subprocess
import os
import tempfile
from spack.util.module_cmd import get_path_from_module, module
from spack.util.module_cmd import get_argument_from_module_line


typeset_func = subprocess.Popen('module avail',
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True)
typeset_func.wait()
typeset = typeset_func.stderr.read()
MODULE_DEFINED = b'not found' not in typeset

test_module_lines = ['prepend-path LD_LIBRARY_PATH /path/to/lib',
                     'setenv MOD_DIR /path/to',
                     'setenv LDFLAGS -Wl,-rpath/path/to/lib',
                     'setenv LDFLAGS -L/path/to/lib',
                     'prepend-path PATH /path/to/bin']


@pytest.fixture
def save_env():
    old_PATH = os.environ.get('PATH', None)
    old_bash_func = os.environ.get('BASH_FUNC_module()', None)

    yield

    if old_PATH:
        os.environ['PATH'] = old_PATH
    if old_bash_func:
        os.environ['BASH_FUNC_module()'] = old_bash_func


@pytest.fixture
def tmp_module():
    module_dir = tempfile.mkdtemp()
    module_file = os.path.join(module_dir, 'mod')

    module('use', module_dir)

    yield module_file

    module('unuse', module_dir)
    os.remove(module_file)
    os.rmdir(module_dir)


@pytest.mark.skipif(not MODULE_DEFINED, reason='Requires module() function')
def test_get_path_from_module(tmp_module):
    for line in test_module_lines:
        with open(tmp_module, 'w') as f:
            f.truncate()
            f.write('#%Module1.0\n')
            f.write(line)

        path = get_path_from_module(os.path.basename(tmp_module))
        assert path == '/path/to'


@pytest.mark.skipif(MODULE_DEFINED, reason='Only works if module() undefined')
def test_get_path_from_module_faked(save_env):
    for line in test_module_lines:
        module_func = '() { eval `echo ' + line + ' bash filler`\n}'
        os.environ['BASH_FUNC_module()'] = module_func
        path = get_path_from_module('mod')

        assert path == '/path/to'

    os.environ['BASH_FUNC_module()'] = '() { eval $(echo fill bash $*)\n}'
    path = get_path_from_module('mod')

    assert path is None


def test_get_argument_from_module_line():
    lines = ['prepend-path LD_LIBRARY_PATH /lib/path',
             'prepend-path  LD_LIBRARY_PATH  /lib/path',
             "prepend_path('PATH' , '/lib/path')",
             'prepend_path( "PATH" , "/lib/path" )',
             'prepend_path("PATH",' + "'/lib/path')"]

    bad_lines = ['prepend_path(PATH,/lib/path)',
                 'prepend-path (LD_LIBRARY_PATH) /lib/path']

    assert all(get_argument_from_module_line(l) == '/lib/path' for l in lines)
    for bl in bad_lines:
        with pytest.raises(ValueError):
            get_argument_from_module_line(bl)
