# file: text.py
# vim:fileencoding=utf-8:ft=python:fdm=marker
# Copyright © 2011-2021 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause
# Created: 2011-03-27 13:59:17 +0200
# Last modified: 2021-08-10T14:40:58+0200
"""Text output routines for lamprop."""

from .version import __version__
import lp.core as core

# Data

_t = [
    "thickness: {0:.2f} mm, density: {1:4.2f} g/cm³",
    "laminate weight: {0:.0f} g/m², resin consumption: {1:.0f} g/m²",
    "ν_xy = {0:7.5f}",
    "ν_yx = {0:7.5f}",
    "α_x = {0:9.4g} K⁻¹, α_y = {1:9.4g} K⁻¹",
    "    [g/m²]   [°]  [%]",
]


def out(lam, eng, mat, fea):  # {{{1
    """Return the output as a list of lines."""
    lines = [
        "Generated by lamprop {0}".format(__version__),
        "laminate: {0}".format(lam.name),
        _t[0].format(lam.thickness, lam.ρ),
        f"fiber volume fraction: {lam.vf*100:.3g}%, fiber weight fraction: {lam.wf*100:.3g}%",
        _t[1].format(lam.fiber_weight + lam.resin_weight, lam.resin_weight),
        "num weight angle   vf fiber",
        _t[5],
    ]
    s = "{0:3} {1:6g} {2:5g} {3:4.3g} {4}"
    ln = 1
    for la in lam.layers:
        if isinstance(la, str):
            lines.append(la)
            continue
        lines.append(
            s.format(ln, la.fiber_weight, la.angle, la.vf * 100, la.fiber.name)
        )
        ln += 1
    if eng:
        lines += _engprop(lam)
    if mat:
        lines += _matrices(lam)
    if fea:
        lines += _fea(lam)
    lines.append("")
    return lines


def _engprop(l):  # {{{1
    """Return the engineering properties as a plain text table in the form of
    a list of lines."""
    lines = ["In-plane engineering properties:"]
    lines += [
        f"E_x  = {l.Ex:.0f} MPa, E_y  = {l.Ey:.0f} MPa, E_z  = {l.Ez:.0f} MPa ",
        f"G_xy  = {l.Gxy:.0f} MPa, G_xz  = {l.Gxz:.0f} MPa, G_yz  = {l.Gyz:.0f} MPa ",
        _t[2].format(l.νxy),
        _t[4].format(l.αx, l.αy),
    ]
    lines.append("Engineering properties derived from 3D stiffness matrix:")
    lines.append(f"E_x = {l.tEx:.0f} MPa, E_y = {l.tEy:.0f} MPa, E_z = {l.tEz:.0f} MPa")
    lines.append(
        f"G_xy = {l.tGxy:.0f} MPa, G_xz = {l.tGxz:.0f} MPa, G_yz = {l.tGyz:.0f} MPa"
    )
    lines.append(f"ν_xy = {l.tνxy:.3f}, ν_xz = {l.tνxz:.3f}, ν_yz = {l.tνyz:.3f}")
    return lines


def _matrices(l):  # {{{1
    """Return the ABD, abd, H and h matrices as plain text."""
    lines = ["In-plane stiffness (ABD) matrix:"]
    matstr = "|{:< 10.4} {:< 10.4} {:< 10.4} {:< 10.4} {:< 10.4} {:< 10.4}|"
    hstr = "|{:< 10.4} {:< 10.4}|"
    for n in range(6):
        m = matstr.format(
            l.ABD[n][0], l.ABD[n][1], l.ABD[n][2], l.ABD[n][3], l.ABD[n][4], l.ABD[n][5]
        )
        lines.append(m)
    lines.append("Transverse (H) stiffness matrix:")
    for n in range(2):
        h = hstr.format(l.H[n][0], l.H[n][1])
        lines.append(h)
    lines += ["3D stiffness tensor [C], contracted notation:"]
    lines.append("(indices for stress/strain are in the order 11, 22, 33, 23, 13, 12)")
    matstr = "|{:< 10.4} {:< 10.4} {:< 10.4} {:< 10.4} {:< 10.4} {:< 10.4}|"
    for row in l.C:
        lines.append(matstr.format(row[0], row[1], row[2], row[3], row[4], row[5]))
    return lines


def _fea(l):  # {{{1
    """Return the material data for FEA."""
    lines = ["** Material data for CalculiX / Abaqus (SI units):"]
    D = core.toabaqusi(l.C)
    lines.append(f"*MATERIAL,NAME={l.name}")
    if core.isortho(l.C):
        # Convert to abaqus format and SI units
        lines.append("*ELASTIC,TYPE=ORTHO")
        lines.append(
            f"{D[0][0]:.4g},{D[0][1]:.4g},{D[1][1]:.4g},"
            f"{D[0][2]:.4g},{D[1][2]:.4g},{D[2][2]:.4g},"
            f"{D[3][3]:.4g},{D[4][4]:.4g},"
        )
        lines.append(f"{D[5][5]:.4g},293")
    else:
        lines.append("*ELASTIC,TYPE=ANISO")
        lines.append(
            f"{D[0][0]:.4g},{D[0][1]:.4g},{D[1][1]:.4g},"
            f"{D[0][2]:.4g},{D[1][2]:.4g},{D[2][2]:.4g},"
            f"{D[0][3]:.4g},{D[1][3]:.4g},"
        )
        lines.append(
            f"{D[2][3]:.4g},{D[3][3]:.4g},{D[0][4]:.4g},"
            f"{D[1][4]:.4g},{D[2][4]:.4g},{D[3][4]:.4g},"
            f"{D[4][4]:.4g},{D[0][5]:.4g},"
        )
        lines.append(
            f"{D[1][5]:.4g},{D[2][5]:.4g},{D[3][5]:.4g},"
            f"{D[4][5]:.4g},{D[5][5]:.4g},293"
        )
    lines.append("*DENSITY")
    lines.append(f"{l.ρ*1000:.0f}")
    return lines
