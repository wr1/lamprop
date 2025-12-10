# file: test_core_laminate.py
#
# Tests for laminate model and creation function.

import math
import sys

sys.path.insert(1, ".")
from lamprop.core.fiber import fiber
from lamprop.core.lamina import lamina
from lamprop.core.laminate import laminate
from lamprop.core.resin import resin

hf = fiber(233000, 0.2, -0.54e-6, 1.76, "Hyer's carbon fiber")
hr = resin(4620, 0.36, 41.4e-6, 1.1, "Hyer's resin")


def test_ud():
    """Test unidirectional laminate."""
    la = lamina(hf, hr, 100, 0, 0.5)
    ud = laminate("ud", [la, la, la, la])
    assert math.isclose(ud.thickness, 0.4545, rel_tol=0.01)
    assert math.isclose(ud.rho, 1.43, rel_tol=0.01)
    assert ud.vf == 0.5
    assert math.isclose(ud.wf, 0.615, rel_tol=0.01)
    assert math.isclose(ud.Ex, 118810, rel_tol=0.01)
    assert math.isclose(ud.Ey, 15109.06, rel_tol=0.01)
    assert math.isclose(ud.Ez, 15109.06, rel_tol=0.01)
    assert math.isclose(ud.Gxy, 5095.588, rel_tol=0.01)
    assert math.isclose(ud.Gxz, 4246.32, rel_tol=0.01)
    assert math.isclose(ud.Gyz, 4233.40, rel_tol=0.01)
    assert math.isclose(ud.nu_xy, 0.28, rel_tol=0.01)
    assert math.isclose(ud.nu_yx, 0.0356, rel_tol=0.01)
    assert math.isclose(ud.alpha_x, 2.75e-07, rel_tol=0.01)
    assert math.isclose(ud.alpha_y, 2.07e-05, rel_tol=0.01)
    assert math.isclose(ud.tEx, 118810.0, rel_tol=0.01)
    assert math.isclose(ud.tEy, 15109.06, rel_tol=0.01)
    assert math.isclose(ud.tEz, 15109.06, rel_tol=0.01)
    assert math.isclose(ud.tGxy, 5095.59, rel_tol=0.01)
    assert math.isclose(ud.tGyz, 5080.08, rel_tol=0.01)
    assert math.isclose(ud.tGxz, 5095.58, rel_tol=0.01)
    assert math.isclose(ud.t_nu_xy, 0.2800, rel_tol=0.01)
    assert math.isclose(ud.t_nu_xz, 0.2799, rel_tol=0.01)
    assert math.isclose(ud.t_nu_yz, 0.4871, rel_tol=0.01)


def test_plain_weave():
    """Test plain weave laminate."""
    A = lamina(hf, hr, 100, 0, 0.5)
    B = lamina(hf, hr, 100, 90, 0.5)
    pw = laminate("pw", [A, B, B, A])
    assert math.isclose(pw.thickness, 0.4545, rel_tol=0.01)
    assert math.isclose(pw.rho, 1.43, rel_tol=0.01)
    assert pw.vf == 0.5
    assert math.isclose(pw.wf, 0.615, rel_tol=0.01)
    assert math.isclose(pw.Ex, 67363.86, rel_tol=0.01)
    assert math.isclose(pw.Ey, 67363.86, rel_tol=0.01)
    assert math.isclose(pw.Ez, 15109.06, rel_tol=0.01)
    assert math.isclose(pw.Gxy, 5095.588, rel_tol=0.01)
    assert math.isclose(pw.Gxz, 4237.439, rel_tol=0.01)
    assert math.isclose(pw.Gyz, 4242.285, rel_tol=0.01)
    assert math.isclose(pw.nu_xy, 0.063, rel_tol=0.01)
    assert math.isclose(pw.nu_yx, 0.063, rel_tol=0.01)
    assert math.isclose(pw.alpha_x, 3.0497e-06, rel_tol=0.01)
    assert math.isclose(pw.alpha_y, 3.0497e-06, rel_tol=0.01)
    assert math.isclose(pw.tEx, 67402.13, rel_tol=0.01)
    assert math.isclose(pw.tEy, 67402.13, rel_tol=0.01)
    assert math.isclose(pw.tEz, 18205.69, rel_tol=0.01)
    assert math.isclose(pw.tGxy, 5095.588, rel_tol=0.01)
    assert math.isclose(pw.tGyz, 5087.835, rel_tol=0.01)
    assert math.isclose(pw.tGxz, 5087.835, rel_tol=0.01)
    assert math.isclose(pw.t_nu_xy, 0.0626, rel_tol=0.01)
    assert math.isclose(pw.t_nu_xz, 0.4324, rel_tol=0.01)
    assert math.isclose(pw.t_nu_yz, 0.4324, rel_tol=0.01)


def test_pm45():
    """Test +/-45 laminate."""
    A = lamina(hf, hr, 100, 45, 0.5)
    B = lamina(hf, hr, 100, -45, 0.5)
    pm45 = laminate("pm45", [A, B, B, A])
    assert math.isclose(pm45.thickness, 0.4545, rel_tol=0.01)
    assert math.isclose(pm45.rho, 1.43, rel_tol=0.01)
    assert pm45.vf == 0.5
    assert math.isclose(pm45.wf, 0.615, rel_tol=0.01)
    assert math.isclose(pm45.Ex, 17899.5, rel_tol=0.01)
    assert math.isclose(pm45.Ey, 17899.5, rel_tol=0.01)
    assert math.isclose(pm45.Ez, 15109.06, rel_tol=0.01)
    assert math.isclose(pm45.Gxy, 31928.0, rel_tol=0.01)
    assert math.isclose(pm45.Gxz, 4239.86, rel_tol=0.01)
    assert math.isclose(pm45.Gyz, 4239.86, rel_tol=0.01)
    assert math.isclose(pm45.nu_xy, 0.756, rel_tol=0.01)
    assert math.isclose(pm45.nu_yx, 0.756, rel_tol=0.01)
    assert math.isclose(pm45.alpha_x, 3.0497e-06, rel_tol=0.01)
    assert math.isclose(pm45.alpha_y, 3.0497e-06, rel_tol=0.01)
    assert math.isclose(pm45.tEx, 17852.21, rel_tol=0.01)
    assert math.isclose(pm45.tEy, 17852.21, rel_tol=0.01)
    assert math.isclose(pm45.tEz, 18205.69, rel_tol=0.01)
    assert math.isclose(pm45.tGxy, 31714.22, rel_tol=0.01)
    assert math.isclose(pm45.tGyz, 5087.84, rel_tol=0.01)
    assert math.isclose(pm45.tGxz, 5087.84, rel_tol=0.01)
    assert math.isclose(pm45.t_nu_xy, 0.7517, rel_tol=0.01)
    assert math.isclose(pm45.t_nu_xz, 0.1145, rel_tol=0.01)
    assert math.isclose(pm45.t_nu_yz, 0.1145, rel_tol=0.01)


def test_qi():
    """Test quasi-isotropic laminate."""
    A = lamina(hf, hr, 100, 0, 0.5)
    B = lamina(hf, hr, 100, 90, 0.5)
    C = lamina(hf, hr, 100, 45, 0.5)
    D = lamina(hf, hr, 100, -45, 0.5)
    qi = laminate("qi", [A, B, C, D, D, C, B, A])
    assert math.isclose(qi.thickness, 0.9090, rel_tol=0.01)
    assert math.isclose(qi.rho, 1.43, rel_tol=0.01)
    assert qi.vf == 0.5
    assert math.isclose(qi.wf, 0.615, rel_tol=0.01)
    assert math.isclose(qi.Ex, 48663.52, rel_tol=0.01)
    assert math.isclose(qi.Ey, 48663.52, rel_tol=0.01)
    assert math.isclose(qi.Ez, 15109.06, rel_tol=0.01)
    assert math.isclose(qi.Gxy, 18387.97, rel_tol=0.01)
    assert math.isclose(qi.Gxz, 4238.95, rel_tol=0.01)
    assert math.isclose(qi.Gyz, 4240.77, rel_tol=0.01)
    assert math.isclose(qi.nu_xy, 0.32324, rel_tol=0.01)
    assert math.isclose(qi.nu_yx, 0.32324, rel_tol=0.01)
    assert math.isclose(qi.alpha_x, 3.049e-06, rel_tol=0.01)
    assert math.isclose(qi.alpha_y, 3.049e-06, rel_tol=0.01)
    assert math.isclose(qi.tEx, 48693.169, rel_tol=0.01)
    assert math.isclose(qi.tEy, 48693.169, rel_tol=0.01)
    assert math.isclose(qi.tEz, 18205.69, rel_tol=0.01)
    assert math.isclose(qi.tGxy, 18404.90, rel_tol=0.01)
    assert math.isclose(qi.tGyz, 5087.83, rel_tol=0.01)
    assert math.isclose(qi.tGxz, 5087.83, rel_tol=0.01)
    assert math.isclose(qi.t_nu_xy, 0.32283, rel_tol=0.01)
    assert math.isclose(qi.t_nu_xz, 0.31239, rel_tol=0.01)
    assert math.isclose(qi.t_nu_yz, 0.31239, rel_tol=0.01)
