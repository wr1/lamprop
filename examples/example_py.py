#!/usr/bin/env python3
"""Example of using lamprop programmatically in Python."""

import sys
sys.path.insert(0, "src")

from lamprop import fiber, resin, lamina, laminate
from rich.console import Console
from rich.table import Table

# Create fiber and resin
fiber_obj = fiber(E1=230000, nu12=0.27, alpha1=-0.38e-6, rho=1.80, name="Carbon")
resin_obj = resin(E=4000, nu=0.36, alpha=40e-6, rho=1.20, name="Epoxy")

# Create laminas
la1 = lamina(fiber_obj, resin_obj, 100, 0, 0.5)
la2 = lamina(fiber_obj, resin_obj, 100, 90, 0.5)

# Create laminate
lam = laminate("Example Laminate", [la1, la2, la2, la1])

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
