"""Create a material database from lamprop test files."""
import argparse
import json
import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, "src")

from lamprop import fiber, resin, lamina, laminate


def main():
    """Main function to create material database."""
    parser = argparse.ArgumentParser()
    parser.add_argument("lp_testdir", nargs="?", default="test", help="directory where the lamprop test files are")
    parser.add_argument("--output", default="__matdb.json")
    args = parser.parse_args()

    lp_testdir = Path(args.lp_testdir)

    lm = list(lp_testdir.glob("*lam"))

    fibers = {}
    resins = {}
    for i in lm:
        for j in i.read_text().splitlines():
            if j.startswith(("f:", "r:")):
                try:
                    s = j.split()
                    sp = [float(j) for j in s[1:5]]
                    name = j.split(s[4])[-1].strip()
                    if j.startswith("f:"):
                        fb = fiber(sp[0], sp[1], sp[2], sp[3], name)
                        fibers[name] = fb
                    elif j.startswith("r:"):
                        rs = resin(sp[0], sp[1], sp[2], sp[3], name)
                        resins[name] = rs
                except (ValueError, IndexError):
                    pass

    # check later if there should also be a loop over different ply thicknesses
    fiber_weight = 200.0
    angles = [90, -90, 45, -45, 30, -30, 15, -15, 10, -10, 0]
    vfs = np.arange(0.50, 0.85, 0.05)
    laminae = {}
    for angle in angles:
        for vf in vfs:
            for fb in fibers:
                for rs in resins:
                    key = (fb, rs, fiber_weight, angle, vf)
                    laminae[key] = lamina(
                        fibers[fb], resins[rs], fiber_weight, angle, vf
                    )

    stacks = {
        "ud": [0, 0],
        "hoop": [90, 90],
        "biax090": [0, 90, 90, 0],
        "biax45": [45, -45, -45, 45],
        "triax45": [0, 45, 90, -45, 0],
        "triax30": [0, 30, 90, -30, 0],
        "biax15": [-15, 15, 15, -15],
    }

    def todict(lam):
        """Convert laminate to dict."""
        sub = vars(lam)
        sub["ABD"] = sub["ABD"].tolist()
        sub["abd"] = sub["abd"].tolist()
        sub["H"] = sub["H"].tolist()
        sub["h"] = sub["h"].tolist()
        sub["C"] = sub["C"].tolist()
        sub["S"] = sub["S"].tolist()
        sub["layers"] = [vars(i) for i in sub["layers"]]
        for i in range(len(sub["layers"])):
            if hasattr(sub["layers"][i]["C"], "tolist"):
                sub["layers"][i]["C"] = sub["layers"][i]["C"].tolist()
            if not isinstance(sub["layers"][i]["resin"], dict):
                sub["layers"][i]["resin"] = vars(sub["layers"][i]["resin"])
            if not isinstance(sub["layers"][i]["fiber"], dict):
                sub["layers"][i]["fiber"] = vars(sub["layers"][i]["fiber"])
        return sub

    all_laminates = {}

    for s in stacks:
        for vf in vfs:
            for fb in fibers:
                for rs in resins:
                    this_stack = [
                        laminae[(fb, rs, fiber_weight, ang, vf)] for ang in stacks[s]
                    ]
                    try:
                        lam = laminate(
                            f"{s}_{fb}_{rs}_{int(100 * vf)}", this_stack
                        )
                        all_laminates[lam.name] = todict(lam)
                    except (ValueError, TypeError, ZeroDivisionError):
                        pass

    Path(args.output).write_text(json.dumps(all_laminates, indent=4))


if __name__ == "__main__":
    main()
