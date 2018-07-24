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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install gate
#
# You can edit this file again by typing:
#
#     spack edit gate
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class Gate(CMakePackage):
    """GATE is an advanced opensource software developed by the international OpenGATE collaboration and dedicated to numerical simulations in medical imaging and radiotherapy. It currently supports simulations of Emission Tomography (Positron Emission Tomography - PET and Single Photon Emission Computed Tomography - SPECT), Computed Tomography (CT), Optical Imaging (Bioluminescence and Fluorescence) and Radiotherapy experiments. Using an easy-to-learn macro mechanism to configurate simple or highly sophisticated experimental settings, GATE now plays a key role in the design of new medical imaging devices, in the optimization of acquisition protocols and in the development and assessment of image reconstruction algorithms and correction techniques. It can also be used for dose calculation in radiotherapy experiments."""

    homepage = "http://www.example.com"
    url      = "https://github.com/OpenGATE/Gate/archive/v7.2.tar.gz"

    version('8.1.p01', '20df9ae70db75c1a96f962b9248d24a8')
    version('8.1',     'd0e0224609b84beee37449d995d8e573')
    version('8.0',     '5297e3a67d53e98548cc71b1491435e8')
    version('7.2',     '6b15b179ccc79065a4aef63156b3e5de')
    version('7.0',     '9f98126c8adf9eaf421e23f7f47c014a')

    depends_on('techpi.geant4')
    depends_on('root')
    depends_on('clhep')

    def cmake_args(self):
        args = ['-DGATE_USE_OPTICAL=ON',
                '-DGATE_USE_STDC11=ON',
                '-DGATE_USE_GEANT4_UIVIS=ON']
        return args
