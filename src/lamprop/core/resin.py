"""Resin model and creation function."""
from pydantic import BaseModel, Field

class Resin(BaseModel):
    """Represents a resin material."""
    E: float = Field(..., gt=0, description="Young's modulus in MPa")
    nu: float = Field(..., description="Poisson's constant")
    alpha: float = Field(..., description="CTE in K^-1")
    rho: float = Field(..., gt=0, description="Specific gravity in g/cm^3")
    name: str = Field(..., min_length=1, description="Name of the resin")

def resin(E: float, nu: float, alpha: float, rho: float, name: str) -> Resin:
    """Create a Resin instance."""
    return Resin(E=E, nu=nu, alpha=alpha, rho=rho, name=name)
