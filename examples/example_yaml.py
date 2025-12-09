#!/usr/bin/env python3
"""Example of loading laminate from YAML and printing with rich."""

import sys
sys.path.insert(0, "src")

from lamprop import parse
from rich.console import Console
from rich.table import Table

# Load from YAML
laminates = parse("test/generic.yaml")
lam = laminates[0]

# Print with rich
console = Console()
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
