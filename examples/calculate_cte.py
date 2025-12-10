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
    rv = (a1f * E1f * vf + am * Em * vm) / (E1f * vf + Em * vm)
    print(f"vf = {vf}, α1 = {rv:.3g}")


def a2(vf):
    """Calculate transverse CTE."""
    vm = 1 - vf
    E1 = E1f * vf + Em * vm
    p1 = am
    p2 = (a2f - am) * vf
    p3 = ((E1f * vm - Em * v12f) / E1) * (am - a1f) * vm * vf
    s = "α2(1) = {}, α2(2) = {}, α2(3) = {},\n α2(1-3) = {}, α2(1,3) = {}, {}"
    print(s.format(p1, p2, p3, p1 + p2 + p3, p1 + p3, (p1 + p2 + p3) / (p1 + p3)))


def a2alt(vf):
    """Alternative calculation for transverse CTE."""
    vm = 1 - vf
    E1 = E1f * vf + Em * vm
    p1 = am * vm
    p3 = ((E1f * vm - Em * v12f) / E1) * (am - a1f) * vm * vf
    s = "alt α2(1) = {}, α2(3) = {},\n α2(1,3) = {}"
    print(s.format(p1, p3, p1 + p3))


if __name__ == "__main__":
    for v in range(1, 6):
        vf = v * 0.1
        a1(vf)
        a2(vf)
        a2alt(vf)
