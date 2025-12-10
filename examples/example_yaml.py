"""Example of loading laminate from YAML and printing with rich."""

import sys

sys.path.insert(0, "src")

import argparse
from pathlib import Path

from rich.console import Console
from rich.table import Table

from lamprop import parse

parser = argparse.ArgumentParser(description="Load and display laminates from YAML.")
parser.add_argument("yaml_file", nargs="?", help="Path to the YAML file (optional, runs all if not provided)")
args = parser.parse_args()

console = Console()

if args.yaml_file:
    yaml_files = [args.yaml_file]
else:
    yaml_files = [str(p) for p in Path("test").glob("*.yaml")]

for yaml_file in yaml_files:
    console.print(f"\nProcessing {yaml_file}")
    try:
        laminates = parse(yaml_file)
        for lam in laminates:
            console.print(f"Laminate: {lam.name}")
            console.print(f"Thickness: {lam.thickness:.2f} mm")
            console.print(f"Density: {lam.rho:.2f} g/cm³")

            # Engineering properties table
            table = Table(title="Engineering Properties")
            table.add_column("Property", style="cyan")
            table.add_column("Value", style="magenta")
            table.add_column("Unit", style="green")

            table.add_row("E_x", f"{lam.Ex:.0f}", "MPa")
            table.add_row("E_y", f"{lam.Ey:.0f}", "MPa")
            table.add_row("E_z", f"{lam.Ez:.0f}", "MPa")
            table.add_row("G_xy", f"{lam.Gxy:.0f}", "MPa")
            table.add_row("nu_xy", f"{lam.nu_xy:.3f}", "-")

            table.add_row("alpha_x", f"{lam.alpha_x:.2e}", "K⁻¹")
            table.add_row("alpha_y", f"{lam.alpha_y:.2e}", "K⁻¹")

            console.print(table)
    except Exception as e:
        console.print(f"Error processing {yaml_file}: {e}", style="red")
