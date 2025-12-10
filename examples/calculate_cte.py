"""Example script to calculate thermal expansion coefficients for composites."""

import sys

sys.path.insert(0, "src")

# Fiber properties
E1f = 233000.0
E2f = 23100.0
v12f = 0.2
v23f = 0.4
G12f = 8960
G23f = 8270
a1f = -0.54e-6
a2f = 10.1e-6

# Matrix properties
Em = 4620.0
vm = 0.36
am = 41.4e-6


def a1(vf):
    """Calculate longitudinal CTE."""
    vm = 1 - vf
    (a1f * E1f * vf + am * Em * vm) / (E1f * vf + Em * vm)


def a2(vf):
    """Calculate transverse CTE."""
    vm = 1 - vf
    E1 = E1f * vf + Em * vm
    (a2f - am) * vf
    ((E1f * vm - Em * v12f) / E1) * (am - a1f) * vm * vf


def a2alt(vf):
    """Alternative calculation for transverse CTE."""
    vm = 1 - vf
    E1 = E1f * vf + Em * vm
    am * vm
    ((E1f * vm - Em * v12f) / E1) * (am - a1f) * vm * vf


if __name__ == "__main__":
    for v in range(1, 6):
        vf = v * 0.1
        a1(vf)
        a2(vf)
        a2alt(vf)
