# vim:fileencoding=utf-8
# Copyright © 2011-2015 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

"""Text output routines for lamprop."""

__version__ = '2.0.0'

import sys

_t = ["thickness: {0:.2f} mm, density: {1:4.2f} g/cm³",
      "laminate weight: {0:.0f} g/m², resin consumption: {1:.0f} g/m²",
      "ν_xy = {0:7.5f}", "ν_yx = {0:7.5f}",
      "α_x = {0:9.4g} K⁻¹, α_y = {1:9.4g} K⁻¹"]

# Platforms that don't support UTF-8 get ASCII text.
if sys.stdout.encoding.lower() != 'utf-8':
    _t = ["thickness: {0:.2f} mm, density: {1:4.2f} g/cm3",
          "laminate weight: {0:.0f} g/m2, resin consumption: {1:.0f} g/m2",
          "v_xy = {0:7.5f}", "v_yx = {0:7.5f}",
          "a_x = {0:9.4g} 1/K, a_y = {1:9.4g} 1/K"]


def out(lam, eng, mat):
    """Plain text main output function."""
    if eng:
        _engprop(lam)
    if mat:
        _matrices(lam, not eng)
    print('')


def _engprop(l):
    """Prints the engineering properties as a plain text table."""
    print("Generated by lamprop {0}".format(__version__))
    print("laminate: {0}".format(l.name))
    print(_t[0].format(l.thickness, l.ρ))
    s = "fiber volume fraction: {0:.1f}%, fiber weight fraction: {1:.1f}%"
    print(s.format(l.vf*100, l.wf*100))
    print(_t[1].format(l.fiber_weight+l.resin_weight, l.resin_weight))
    print("num weight angle   vf fiber")
    for ln, la in enumerate(l.layers):
        s = "{0:3} {1:6g} {2:5g} {3:4g} {4}"
        print(s.format(ln+1, la.fiber_weight, la.angle, la.vf, la.fiber.name))
    print("E_x  = {0:.0f} MPa".format(l.Ex))
    print("E_y  = {0:.0f} MPa".format(l.Ey))
    print("G_xy = {0:.0f} MPa".format(l.Gxy))
    print(_t[2].format(l.νxy))
    print(_t[3].format(l.νyx))
    print(_t[4].format(l.αx, l.αy))


def _matrices(l, printheader):
    """Prints the ABD and abd matrices as plain text."""
    if printheader is True:
        print("Generated by lamprop {0}".format(__version__))
        print("laminate: {0}".format(l.name))
    print("Stiffness (ABD) matrix:")
    matstr = "|{:> 10.4e} {:> 10.4e} {:> 10.4e} " \
             "{:> 10.4e} {:> 10.4e} {:> 10.4e}|"
    for n in range(6):
        m = matstr.format(l.ABD[n, 0], l.ABD[n, 1], l.ABD[n, 2],
                          l.ABD[n, 3], l.ABD[n, 4], l.ABD[n, 5])
        print(m.replace('e+00', '    '))
    print("Compliance (abd) matrix:")
    for n in range(6):
        m = matstr.format(l.abd[n, 0], l.abd[n, 1], l.abd[n, 2],
                          l.abd[n, 3], l.abd[n, 4], l.abd[n, 5])
        print(m.replace('e+00', '    '))
