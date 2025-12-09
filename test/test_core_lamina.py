# file: test_core_lamina.py
# vim:fileencoding=utf-8:ft=python
#
# Tests for lamina model and creation function.

import sys
import math

sys.path.insert(1, ".")
from lamprop.core.fiber import fiber
from lamprop.core.resin import resin
from lamprop.core.lamina import lamina

hf = fiber(233000, 0.2, -0.54e-6, 1.76, "Hyer's carbon fiber")
hr = resin(4620, 0.36, 41.4e-6, 1.1, "Hyer's resin")


def areclose(a, b):
    for x, y in zip(a, b):
        assert math.isclose(x, y, rel_tol=0.01)


def test_lamina():
    """Test lamina creation."""
    f = fiber(230000, 0.30, -0.41e-6, 1.76, "T300")
    r = resin(2900, 0.36, 41.4e-6, 1.15, "Epikote04908")
    la = lamina(f, r, 100, 0, 0.5)
    areclose(
        (la.E1, la.E2, la.G12, la.nu12, la.alpha_x, la.alpha_y, la.rho),
        (116450.0, 9714.87, 3198.53, 0.33, 1.106e-07, 2.07e-05, 1.455),
    )
    areclose(
        (la.Q11_bar, la.Q12_bar, la.Q16_bar, la.Q22_bar, la.Q26_bar, la.Q66_bar),
        (117517.65, 3235.30, 0.0, 9803.95, 0.0, 3198.53),
    )

# From old test_parser.py
def test_good_lamina():
    """Test good lamina."""
    directives = [
        (1, "l: 200 0 carbon"),
        (2, "l: 302 -23.2 0.3 carbon"),
        (3, "l: 200 0 test 3"),
        (4, "l: 302 -23.2 0.3 test 3"),
    ]
    fdict = {
        "carbon": fiber(240000, 0.2, -0.2e-6, 1.76, "carbon"),
        "test 3": fiber(240000, 0.2, -0.2e-6, 1.76, "test 3"),
    }
    r = resin(3000, 0.3, 20e-6, 1.2, "resin")
    layers = []
    for d in directives:
        ln, line = d
        parts = line.split()
        if len(parts) >= 4:
            weight = float(parts[1])
            angle = float(parts[2])
            try:
                vf = float(parts[3])
                fname = ' '.join(parts[4:])
            except ValueError:
                vf = 0.5
                fname = ' '.join(parts[3:])
            if fname in fdict:
                la = lamina(fdict[fname], r, weight, angle, vf)
                layers.append(la)
    assert len(layers) == 4
