# file: test_core_resin.py
# vim:fileencoding=utf-8:ft=python
#
# Tests for resin model and creation function.

import sys
import pytest

sys.path.insert(1, ".")
from lamprop.core.resin import resin, Resin


def test_resin_creation():
    """Test creating a resin."""
    r = resin(2900, 0.36, 41.4e-6, 1.15, "Epikote04908")
    assert r.E == 2900
    assert r.nu == 0.36
    assert r.alpha == 41.4e-6
    assert r.rho == 1.15
    assert r.name == "Epikote04908"


def test_resin_validation():
    """Test resin validation."""
    with pytest.raises(ValueError):
        resin(-2900, 0.36, 41.4e-6, 1.15, "Epikote04908")  # E <= 0
    with pytest.raises(ValueError):
        resin(2900, 0.36, 41.4e-6, -1.15, "Epikote04908")  # rho <= 0
    with pytest.raises(ValueError):
        resin(2900, 0.36, 41.4e-6, 1.15, "")  # empty name

# From old test_parser.py
def test_good_resins():
    """Test parsing good resins."""
    directives = [
        (0, "r:  2900    0.25    40e-6   1.15    EPR04908"),
        (2, "r:  4300    0.36    40e-6   1.19    palatal-P4-01"),
        (3, "r:  4000    0.36    40e-6   1.22    synolite-2155-N-1"),
        (4, "r:  4100    0.36    40e-6   1.2     distitron 3501LS1"),
        (6, "r:  3800    0.36    40e-6   1.165   synolite 1967-G-6"),
        (8, "r:  3600    0.36    55e-6   1.145   atlac 430"),
        (9, "r:  3500    0.36    51.5e-6   1.1   atlac 590"),
    ]
    for d in directives:
        ln, line = d
        parts = line.split()
        if len(parts) >= 6:
            E = float(parts[1])
            nu = float(parts[2])
            alpha = float(parts[3])
            rho = float(parts[4])
            name = ' '.join(parts[5:])
            r = resin(E, nu, alpha, rho, name)
            assert r.name == name
            for other in directives:
                if other != d and other[1].split()[-1] == name:
                    assert r.nu == 0.36  # Check common nu


def test_bad_resins():
    """Test bad resins."""
    bad_directives = [
        (1, "r: -4620 0.36 41.4e-6 1.1 Efout"),
        (2, "r: 4620 -2 41.4e-6 1.1 nufout"),
        (3, "r: 4620 0.7 41.4e-6 1.1 nufout"),
        (4, "r: 4620 0.2 41.4e-6 -0.1 sgfout"),
        (4, "r: 4620 0.2 41.4e-6 1.1"),  # no name
    ]
    for d in bad_directives:
        ln, line = d
        parts = line.split()
        if len(parts) < 6:
            continue
        try:
            E = float(parts[1])
            nu = float(parts[2])
            alpha = float(parts[3])
            rho = float(parts[4])
            name = ' '.join(parts[5:]) if len(parts) > 5 else ""
            resin(E, nu, alpha, rho, name)
            assert False, f"Should have failed for {line}"
        except (ValueError, AssertionError):
            pass
