"""Generic resins and fibers definitions."""
from .core.fiber import Fiber
from .core.resin import Resin

resins = [
    ("generic-epoxy", Resin(E=2900.0, nu=0.25, alpha=40e-6, rho=1.15, name="generic-epoxy")),
    ("generic-polyester", Resin(E=4000.0, nu=0.36, alpha=40e-6, rho=1.20, name="generic-polyester")),
    ("generic-vinylester", Resin(E=3500.0, nu=0.36, alpha=51.5e-6, rho=1.10, name="generic-vinylester")),
]

fibers = [
    ("generic-e-glas", Fiber(E1=73000.0, nu12=0.33, alpha1=5.3e-6, rho=2.60, name="generic-e-glas")),
    ("generic-carbon", Fiber(E1=230000.0, nu12=0.27, alpha1=-0.38e-6, rho=1.80, name="generic-carbon")),
    ("generic-aramid49", Fiber(E1=124000.0, nu12=0.36, alpha1=-4.9e-6, rho=1.44, name="generic-aramid49")),
]
