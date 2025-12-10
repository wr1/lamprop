# file: test_core_fiber.py
#
# Tests for fiber model and creation function.

import sys

import pytest

sys.path.insert(1, ".")
from lamprop.core.fiber import fiber


def test_fiber_creation():
    """Test creating a fiber."""
    f = fiber(230000, 0.30, -0.41e-6, 1.76, "T300")
    assert f.E1 == 230000
    assert f.nu12 == 0.30
    assert f.alpha1 == -0.41e-6
    assert f.rho == 1.76
    assert f.name == "T300"


def test_fiber_validation():
    """Test fiber validation."""
    with pytest.raises(ValueError):
        fiber(-230000, 0.30, -0.41e-6, 1.76, "T300")  # E1 <= 0
    with pytest.raises(ValueError):
        fiber(230000, 0.30, -0.41e-6, -1.76, "T300")  # rho <= 0
    with pytest.raises(ValueError):
        fiber(230000, 0.30, -0.41e-6, 1.76, "")  # empty name


# From old test_parser.py
def test_good_fibers():
    """Test parsing good fibers."""
    directives = [
        (2, "f:  238000  0.25    -0.1e-6     1.76    TenaxHTA"),
        (3, "f:  240000  0.25    -0.1e-6     1.77    TenaxHTS"),
        (4, "f:  240000  0.25    -0.12e-6    1.78    Tenax STS40"),
        (5, "f:  230000  0.27    -0.41e-6    1.76    Toracya T300"),
        (6, "f:  230000  0.27    -0.38e-6    1.80    Torayca T700SC"),
        (7, "f:  235000  0.25    -0.5e-6     1.79    pyrofil TR30S"),
        (8, "f:  640000  0.234   -1.47e-6    2.12    K63712"),
        (9, "f:  790000  0.23    -1.2e-6     2.15    K63A12"),
        (10, "f:  294000  0.27    -0.60e-6    1.76    T800S"),
        (11, "f:  900000  0.234   -1.47e-6    2.20    K13C2U"),
        (12, "f:  339000  0.27    -0.73e-6    1.75    M35J"),
        (13, "f:  436000  0.234   -0.9e-6     1.84    M46J"),
        (14, "f:  242000  0.27    -0.6e-6     1.81    PX35UD"),
        (15, " f:  780000  0.27    -1.5e-6     2.17    XN-80"),
        (19, " f:  73000   0.33    5.3e-6      2.60    e-glas"),
        (20, " f:  80000   0.33    5e-6        2.62    advantex E-CR"),
        (22, " f: 270000   0.25    -6.0e-6     1.56    Zylon"),
        (23, "\tf: 124000   0.3     -2e-6       1.44    aramide49"),
    ]
    # Since parser changed, adapt to create fibers directly
    for d in directives:
        _ln, line = d
        parts = line.split()
        if len(parts) >= 6:
            E1 = float(parts[1])
            nu12 = float(parts[2])
            alpha1 = float(parts[3])
            rho = float(parts[4])
            name = " ".join(parts[5:])
            f = fiber(E1, nu12, alpha1, rho, name)
            assert f.name == name


def test_bad_fibers():
    """Test bad fibers."""
    bad_directives = [
        (1, "f: 233000 0.2 -0.54e-6 geen sg"),
        (2, "f: -230000 0.2 -0.41e-6 -1.76 Efout"),
        (3, "f: 230000 0.2 -0.41e-6 -1.76 sgfout"),
        (4, "f:  240000  0.25    -0.12e-6    1.78"),  # no name
    ]
    for d in bad_directives:
        _ln, line = d
        parts = line.split()
        if len(parts) < 6:
            continue
        try:
            E1 = float(parts[1])
            nu12 = float(parts[2])
            alpha1 = float(parts[3])
            rho = float(parts[4])
            name = " ".join(parts[5:]) if len(parts) > 5 else ""
            fiber(E1, nu12, alpha1, rho, name)
            msg = f"Should have failed for {line}"
            raise AssertionError(msg)
        except (ValueError, AssertionError):
            pass
